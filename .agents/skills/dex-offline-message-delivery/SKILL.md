---
name: dex-offline-message-delivery
description: Design client-side outbox queues with persistent storage (IndexedDB/SQLite), automatic retry loops with jitter, idempotency token headers, and optimistic UI synchronization. Use when engineering mobile apps, field operation clients, or offline-first collaborative tools.
---

# dex-offline-message-delivery

## 1. Purpose & Scope
Thiết kế và hiện thực hóa hàng đợi xuất bản ngoại tuyến phía máy khách (Client-Side Outbox Queue) có lưu trữ bền bỉ (IndexedDB trên web hoặc SQLite trên mobile); tích hợp vòng lặp gửi lại tự động có độ trễ ngẫu nhiên (Jittered Retry), gắn mã định danh bất biến (Idempotency Token Headers) và đồng bộ hóa trạng thái giao diện lạc quan (Optimistic UI Synchronization); phục vụ các ứng dụng hoạt động ngoại tuyến (Offline-First).

## 2. When to Use
- Khi người dùng cần thực hiện các thao tác (tạo bài viết, thích bài, gửi tin nhắn, điền biên bản) ngay cả khi không có kết nối mạng.
- Khi ứng dụng cần phản hồi lập tức trên giao diện mà không để người dùng phải chờ đợi vòng phản hồi mạng.
- Khi cần đảm bảo mọi hành động của người dùng thực hiện khi mất mạng đều được gửi an toàn lên máy chủ ngay khi có mạng trở lại.

## 3. When NOT to Use
- Khi thao tác bắt buộc phải có xác nhận tức thời từ máy chủ (ví dụ giao dịch trừ tiền trong ví thực tế).
- Khi ứng dụng web nội bộ chạy trên máy trạm luôn có cáp mạng ổn định.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bộ nhớ lưu trữ cục bộ có hỗ trợ giao dịch (IndexedDB qua thư viện `idb` hoặc SQLite), trình nghe sự kiện mạng `navigator.onLine`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Client Outbox Pattern:** Tách rời thao tác người dùng khỏi việc gửi mạng: hành động được ghi vào Outbox trên đĩa trước, sau đó tiến trình nền mới đọc và gửi đi.
- **Optimistic UI Mutation:** Hiển thị ngay trạng thái hoàn thành kèm icon đồng hồ cát 'đang đồng bộ', tự động chuyển sang tích xanh khi server xác nhận.
- **Idempotency Key Injection:** Gắn UUID duy nhất cho mỗi thao tác ngoại tuyến để server biết cách bỏ qua nếu gói tin bị gửi lại nhiều lần.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo cơ sở dữ liệu IndexedDB với bảng `outbox_queue` có khóa chính tự tăng và trạng thái `pending`.
2. Khi người dùng thực hiện hành động, tạo một bản ghi outbox kèm UUID và lưu vào IndexedDB.
3. Cập nhật giao diện người dùng ngay lập tức (Optimistic Update) và gắn cờ tạm thời.
4. Lắng nghe sự kiện `window.addEventListener('online')` hoặc chạy tiến trình gửi nền theo chu kỳ.
5. Gửi tuần tự từng bản ghi trong outbox kèm header `Idempotency-Key`, xóa bản ghi khỏi queue sau khi nhận được mã 200 OK.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { openDB } from 'idb';

export class ClientOutboxSync {
  private dbPromise = openDB('dex-outbox-db', 1, {
    upgrade(db) {
      db.createObjectStore('outbox', { keyPath: 'id' });
    }
  });

  async enqueueAction(actionType: string, payload: any) {
    const db = await this.dbPromise;
    const actionId = crypto.randomUUID();
    const item = { id: actionId, actionType, payload, createdAt: Date.now() };
    await db.put('outbox', item);
    this.flush(); // Attempt flush immediately if online
    return item;
  }

  async flush() {
    if (!navigator.onLine) return;
    const db = await this.dbPromise;
    const items = await db.getAll('outbox');

    for (const item of items) {
      try {
        const res = await fetch('/api/sync-action', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Idempotency-Key': item.id
          },
          body: JSON.stringify(item)
        });
        if (res.ok) {
          await db.delete('outbox', item.id);
        }
      } catch (err) {
        console.warn('Sync failed, will retry later...', err);
        break; // Stop loop and wait for next online event
      }
    }
  }
}
```

## 8. Anti-Patterns & Common Traps
- Lưu hàng đợi tạm thời trên biến bộ nhớ RAM khiến toàn bộ hành động người dùng thực hiện khi mất mạng bị mất sạch nếu họ đóng tab trình duyệt.
- Không gửi kèm `Idempotency-Key` khiến các thao tác bị nhân đôi trên máy chủ nếu mạng bị chập chờn gửi lại nhiều lần.
- Xóa bản ghi khỏi hàng đợi trước khi máy chủ xác nhận thành công.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% dữ liệu thao tác của người dùng khi ngoại tuyến được lưu trữ bền bỉ trong IndexedDB.
- QG-02: Tự động xả hàng đợi và gửi dữ liệu lên máy chủ trong vòng tối đa 2 giây sau khi mạng hồi phục.
- QG-03: Không bị trùng lặp dữ liệu trên máy chủ dù mạng gặp sự cố chập chờn.

## 10. Security & Safety Boundaries
- Mã hóa các payload nhạy cảm trong IndexedDB nếu ứng dụng chạy trên máy tính dùng chung (Shared Device).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module quản lý hàng đợi xuất bản ngoại tuyến `ClientOutboxSync.ts`.
1. Component React hiển thị trạng thái đồng bộ dữ liệu `SyncIndicator.tsx`.

## 13. Related & Complementary Skills
- [`dex-progressive-web-apps`](.agents/skills/dex-progressive-web-apps/SKILL.md)
- [`dex-idempotent-operations`](.agents/skills/dex-idempotent-operations/SKILL.md)
- [`dex-mobile-offline-sync`](.agents/skills/dex-mobile-offline-sync/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Nhân viên kiểm kê hàng hóa trong kho lạnh bị mất hoàn toàn kết nối Wi-Fi. Nhờ `dex-offline-message-delivery`, nhân viên vẫn quét mã vạch và ghi nhận hàng trăm thùng hàng bình thường trên giao diện, dữ liệu được xếp vào IndexedDB và tự động đồng bộ trọn vẹn lên máy chủ trung tâm ngay khi họ bước ra khỏi kho lạnh.
