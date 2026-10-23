---
name: dex-supabase-realtime-delivery
description: Architect, optimize, and diagnose Supabase Realtime subscriptions. Configure PostgreSQL Change Data Capture (CDC) filters, manage WebSocket channels, and handle reconnection states without data loss. Use when building live collaborative and streaming applications.
---

# dex-supabase-realtime-delivery

## 1. Purpose & Scope
Thiết kế, tối ưu hóa và chẩn đoán hạ tầng truyền nhận dữ liệu thời gian thực Supabase Realtime; cấu hình bộ lọc Change Data Capture (CDC) tại tầng PostgreSQL để giảm tải băng thông WebSocket; quản lý vòng đời kết nối kênh (Channels, Presence, Broadcast); xử lý tình huống mất mạng và đồng bộ hóa trạng thái khi kết nối lại; và ngăn chặn rò rỉ dữ liệu qua Realtime RLS.

## 2. When to Use
- Khi xây dựng các tính năng tương tác trực tiếp: Chat, thông báo đẩy thời gian thực, bảng tin tức cập nhật tự động, tính năng hiển thị người đang xem (Presence).
- Khi tải trên máy chủ Realtime tăng vọt do client đăng ký lắng nghe toàn bộ bảng dữ liệu mà không có bộ lọc.
- Khi cần xử lý bài toán khôi phục trạng thái client sau khi mất kết nối mạng di động.

## 3. When NOT to Use
- Khi ứng dụng chỉ cần cập nhật dữ liệu định kỳ vài phút một lần (nên dùng Polling hoặc SWR/React Query).
- Khi hệ thống truyền nhận khối lượng dữ liệu khổng lồ hàng nghìn tin nhắn mỗi giây giữa các server (nên dùng Apache Kafka hoặc RabbitMQ).

## 4. Prerequisites & Input Context
- **Cơ sở dữ liệu:** Bảng cần phát sự kiện phải được thêm vào publication `supabase_realtime`.
- **Chính sách an ninh:** Đã bật RLS trên bảng để Supabase Realtime lọc dữ liệu theo quyền của người nhận.

## 5. Core Concepts & Taxonomy
- **Realtime CDC Filters:** Thay vì lắng nghe mọi thay đổi trên bảng, client chỉ định rõ bộ lọc tại nguồn (ví dụ: `filter: 'room_id=eq.123'`), giúp server Realtime chỉ gửi các thông điệp phù hợp.
- **Presence State Synchronization:** Cơ chế chia sẻ trạng thái tạm thời giữa các client (ai đang online, vị trí chuột) thông qua thuật toán CRDT (Conflict-free Replicated Data Types) mà không cần ghi vào database.
- **Reconnection Catch-up:** Quy trình kết hợp giữa WebSocket realtime và HTTP query: Khi kết nối lại sau khi mất mạng, client truy vấn các bản ghi có `created_at > last_received_timestamp` để bù đắp các sự kiện bị bỏ lỡ.

## 6. Step-by-Step Execution Workflow
1. Bật tính năng Realtime cho bảng dữ liệu cụ thể trong migration: `ALTER PUBLICATION supabase_realtime ADD TABLE messages;`.
2. Thiết lập chính sách RLS trên bảng `messages` để bảo đảm client chỉ nhận được sự kiện nếu họ có quyền `SELECT` trên bản ghi đó.
3. Khởi tạo kênh Realtime trên client với bộ lọc chi tiết theo ID phòng hoặc ID người dùng.
4. Lắng nghe các sự kiện `INSERT`, `UPDATE`, `DELETE` và cập nhật state cục bộ một cách tối ưu.
5. Bổ sung bộ lắng nghe trạng thái kết nối (`CHANNEL_ERROR`, `CLOSED`, `SUBSCRIBED`); khi nhận tín hiệu `SUBSCRIBED` sau khi ngắt kết nối, kích hoạt truy vấn đồng bộ bù (Catch-up Fetch).
6. Hủy đăng ký kênh (`supabase.removeChannel(channel)`) khi component unmount để tránh rò rỉ bộ nhớ.

## 7. Concrete Examples
### Đăng ký lắng nghe sự kiện Realtime có lọc và tự động bù dữ liệu khi reconnect:
```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

export function subscribeToRoomMessages(roomId: string, onNewMessage: (msg: any) => void) {
  let lastTimestamp = new Date().toISOString();

  const channel = supabase
    .channel(`room_${roomId}`)
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'messages',
        filter: `room_id=eq.${roomId}` // Bat buoc: Loc tai nguon de giam tai
      },
      (payload) => {
        lastTimestamp = payload.new.created_at;
        onNewMessage(payload.new);
      }
    )
    .subscribe(async (status) => {
      if (status === 'SUBSCRIBED') {
        // Bu du lieu bi lo trong quang thoi gian reconnect
        const { data } = await supabase
          .from('messages')
          .select('*')
          .eq('room_id', roomId)
          .gt('created_at', lastTimestamp)
          .order('created_at', { ascending: true });
          
        if (data && data.length > 0) {
          data.forEach(onNewMessage);
        }
      }
    });

  return () => {
    supabase.removeChannel(channel);
  };
}
```

## 8. Anti-Patterns & Common Traps
- **Unfiltered Table-Wide Subscriptions:** Đăng ký lắng nghe toàn bộ bảng lớn bằng `table: 'messages'` không có `filter`, buộc server phải broadcast hàng triệu message không liên quan tới client.
- **Missing Component Cleanup:** Quên gọi `removeChannel()` trong `useEffect` cleanup của React, khiến mỗi lần người dùng chuyển trang lại tạo thêm một kết nối WebSocket mồ côi.
- **Assuming Zero Message Drop:** Giả định kết nối WebSocket không bao giờ đứt và không xây dựng cơ chế query bù dữ liệu, khiến giao diện người dùng bị lệch dữ liệu khi mạng chập chờn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các kênh `postgres_changes` đều có mệnh đề `filter` cụ thể (không đăng ký lắng nghe toàn bảng).
- **QG-02**: Tất cả các bảng tham gia Realtime đều có chính sách RLS bảo vệ để ngăn chặn rò rỉ sự kiện tới người dùng trái phép.
- **QG-03**: Có cơ chế khôi phục dữ liệu thiếu hụt (Catch-up sync) sau mỗi lần kết nối lại.

## 10. Security & Safety Boundaries
- Bảo đảm tính bảo mật của dữ liệu truyền phát trực tiếp; ngăn ngừa việc nghe lén tin nhắn của phòng khác qua WebSocket.

## 11. Platform Adapters
- **Client SDKs**: Supabase JS v2, Flutter Supabase, Swift Supabase, React/Vue Hooks.

## 12. Deliverables & Output Artifacts
- Module quản lý kênh Realtime có cơ chế tự phục hồi (`realtime_manager.ts`).
- Lược đồ phân quyền RLS cho các bảng truyền phát thời gian thực.
- Báo cáo đo lường độ trễ và số lượng kết nối đồng thời.

## 13. Related & Complementary Skills
dex-supabase-adapter, dex-realtime-protocols, dex-websocket-session-recovery

## 14. Realistic Usage Example
```bash
# Kiem tra publication supabase_realtime co chua dung cac bang can thiet
psql "$DATABASE_URL" -c "SELECT * FROM pg_publication_tables WHERE pubname = 'supabase_realtime';"

# Kiem tra ket noi Realtime WebSocket bang kịch bản Node.js
node scripts/test_realtime_connection.mjs
```
