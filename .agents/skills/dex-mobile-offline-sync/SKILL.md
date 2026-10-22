---
name: dex-mobile-offline-sync
description: Design offline-first mobile/desktop architectures using local databases (SQLite/WatermelonDB/Realm), mutation sync queues, conflict resolution (LWW, CRDTs), and background workers. Use when building apps that must function seamlessly without internet.
---

# dex-mobile-offline-sync

## 1. Purpose & Scope
Thiết kế và hiện thực hóa kiến trúc ưu tiên ngoại tuyến (Offline-First Architecture) cho ứng dụng di động và máy tính; đảm bảo người dùng có thể đọc, tạo mới, chỉnh sửa dữ liệu bình thường khi mất kết nối mạng; lưu trữ dữ liệu tại chỗ qua local database (SQLite / WatermelonDB / Realm / Room), duy trì hàng đợi đồng bộ bất biến (Append-Only Mutation Queue), giải quyết xung đột dữ liệu đa máy (Conflict Resolution: Last-Write-Wins, Field-Level Merging, CRDTs) và đồng bộ tự động qua Background Workers khi có mạng trở lại.

## 2. When to Use
- Khi ứng dụng được sử dụng trong điều kiện mạng chập chờn (Kỹ sư ngoài hiện trường, kho vận, ứng dụng ghi chú cá nhân).
- Khi người dùng phàn nàn ứng dụng bị khóa màn hình hoặc báo lỗi mất mạng không cho thao tác.
- Khi cần đồng bộ dữ liệu hai chiều (Bi-directional Sync) giữa máy khách và máy chủ với cơ chế giải quyết xung đột.

## 3. When NOT to Use
- Ứng dụng giao dịch chứng khoán thời gian thực bắt buộc kiểm tra số dư trực tiếp từ server.
- Thao tác chỉ đọc thuần túy có thể dùng HTTP cache đơn giản.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Cấu trúc thực thể dữ liệu (Entities schema).
- Chiến lược giải quyết xung đột (Conflict Resolution Strategy: LWW hay CRDTs).
- Tần suất và điều kiện kích hoạt đồng bộ (Wi-Fi only, cắm sạc, định kỳ).
- **Điều kiện tiên quyết**:
- Cơ sở dữ liệu cục bộ hỗ trợ giao dịch (Transactions & ACID).
- Background Job Scheduler của hệ điều hành (Android WorkManager, iOS BackgroundTasks).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Optimistic UI Updates**: Giao diện cập nhật ngay lập tức vào database cục bộ trong 16ms; tác vụ đồng bộ với server được đẩy vào hàng đợi ngầm mà không bắt người dùng chờ đợi.
- **Idempotent Mutation Queue**: Hàng đợi các thao tác thay đổi (Create, Update, Delete) được gắn UUID duy nhất và tem thời gian logic; nếu đồng bộ bị đứt đoạn giữa chừng, việc gửi lại không làm nhân đôi dữ liệu.
- **Conflict Resolution Hierarchy**: Xác định quy tắc khi 2 thiết bị cùng sửa 1 bản ghi: Last-Write-Wins (LWW) dựa trên vector clocks, hoặc phân giải theo từng trường (Field-level merging).
- **Quy tắc quyết định kỹ thuật**:
- **Local DB Luôn Là Nguồn Sự Thật Của UI**: Mọi màn hình ứng dụng chỉ quan sát (observe) dữ liệu từ Local DB; không bao giờ hiển thị trực tiếp dữ liệu từ Network response lên UI.
- **Trạng Thái Đồng Bộ Phải Được Đánh Dấu Rõ Ràng**: Mỗi bản ghi cục bộ phải có cờ `sync_status`: `SYNCED`, `PENDING_INSERT`, `PENDING_UPDATE`, `PENDING_DELETE`.
- **Không Xóa Cứng Bản Ghi Khi Offline**: Thao tác xóa khi offline phải là Soft Delete (`is_deleted = true, sync_status = PENDING_DELETE`) để có thể gửi lệnh xóa lên server.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Dữ liệu mới trên server bị ghi đè bởi dữ liệu cũ từ máy vừa kết nối mạng**: Xung đột Last-Write-Wins do sai lệch đồng hồ phần cứng -> Khắc phục: Sử dụng số phiên bản tăng dần (Revision Counter / Lamport Timestamp) thay vì timestamp thời gian thực của client.
- **Hàng đợi đồng bộ bị nghẽn bởi 1 request lỗi 400**: Server từ chối request khiến các request sau không thể gửi -> Khắc phục: Phân loại lỗi; lỗi 4xx chuyển vào hàng đợi lỗi (Dead Letter Queue) kèm thông báo cho người dùng, tiếp tục đồng bộ các tác vụ còn lại.

## 6. Step-by-Step Execution Workflow
1. Thiết kế Schema cơ sở dữ liệu cục bộ có kèm các metadata: `id`, `rev`, `updated_at`, `sync_status`, `is_deleted`.
2. Thiết lập bảng `mutation_queue` lưu trữ tuần tự các payload thay đổi chưa đồng bộ.
3. Khi người dùng thao tác: Mở transaction cục bộ, cập nhật dữ liệu bảng chính và ghi 1 bản ghi vào `mutation_queue`.
4. Đăng ký Network Listener: Khi phát hiện có kết nối Internet, kích hoạt Sync Engine.
5. Sync Engine gửi batch mutations lên server: Server kiểm tra `rev`, phát hiện xung đột và trả về phiên bản hợp nhất.
6. Sync Engine cập nhật dữ liệu server trả về vào Local DB và xóa các item đã xử lý khỏi `mutation_queue`.
7. Cấu hình WorkManager / BackgroundTasks định kỳ chạy đồng bộ ngầm khi ứng dụng đóng.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// Mutation Queue Entity Structure
interface MutationRecord {
  id: string; // UUID
  entity: 'order' | 'note' | 'profile';
  entityId: string;
  operation: 'INSERT' | 'UPDATE' | 'DELETE';
  payload: string; // JSON stringified
  clientTimestamp: number;
  attempts: number;
}

// Sync Engine Process Queue Function
async function processSyncQueue(queue: MutationRecord[], apiClient: ApiClient, db: LocalDB) {
  for (const record of queue) {
    try {
      const result = await apiClient.syncMutation({
        mutationId: record.id,
        operation: record.operation,
        entity: record.entity,
        data: JSON.parse(record.payload),
      });
      // Thành công -> xóa khỏi queue và cập nhật sync_status = SYNCED
      await db.runTransaction(async (tx) => {
        await tx.deleteMutation(record.id);
        await tx.updateSyncStatus(record.entity, record.entityId, 'SYNCED', result.newRev);
      });
    } catch (error) {
      if (isTerminalError(error)) {
        await db.moveToDeadLetterQueue(record, error.message);
      } else {
        await db.incrementAttempts(record.id);
        break; // Tạm dừng đồng bộ nếu là lỗi mạng tạm thời
      }
    }
  }
}
```

### Lệnh xác minh & thực thi:
- Kiểm thử chế độ Airplane Mode: Tắt Wi-Fi/4G, thực hiện tạo 5 bản ghi, kiểm tra hiển thị tức thì trên UI
- Kiểm tra hàng đợi: `SELECT COUNT(*) FROM mutation_queue` (phải trả về 5 bản ghi)
- Bật lại mạng: Kiểm tra toàn bộ 5 bản ghi được đồng bộ lên server và queue trở về 0

## 8. Anti-Patterns & Common Traps
- **Hiển thị hộp thoại Loading bắt người dùng đợi khi mạng chập chờn**: Làm mất hoàn toàn lợi ích của Offline-first.
- **Không giới hạn kích thước hàng đợi đột biến**: Tích lũy hàng ngàn mutations gây quá tải bộ nhớ khi đồng bộ.
- **Tin tưởng tuyệt đối giờ của thiết bị khách**: Dễ bị gian lận hoặc sai lệch múi giờ.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các tính năng cốt lõi hoạt động trơn tru khi không có kết nối Internet.
- QG-08: Không bao giờ làm mất dữ liệu người dùng khi ứng dụng bị tắt đột ngột lúc đang có mutation chờ đồng bộ.
- QG-11: Tự động phục hồi và giải quyết xung đột khi kết nối mạng được tái lập.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Mã hóa cơ sở dữ liệu cục bộ (SQLCipher) để bảo vệ dữ liệu khi thiết bị bị mất cắp.
- Kiểm tra tính hợp lệ của token trước khi giải phóng dữ liệu trong hàng đợi đồng bộ.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Schema cơ sở dữ liệu offline và bảng mutation queue.
- Module Sync Engine hai chiều với thuật toán xử lý xung đột.
- Bộ kiểm thử tự động giả lập mất mạng và phục hồi kết nối.

## 13. Related & Complementary Skills
- `dex-android-app-architecture`: Tích hợp Room DB và WorkManager trên Android.
- `dex-ios-app-architecture`: Tích hợp SwiftData và BackgroundTasks trên iOS.
- `dex-idempotent-operations`: Đảm bảo API server xử lý idempotent các mutation gửi lên.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng kiểm tra công trình cho kỹ sư xây dựng tại tầng hầm không có sóng điện thoại. Sử dụng `dex-mobile-offline-sync`, kỹ sư vẫn chụp ảnh, nhập biên bản nghiệm thu và ký tên bình thường vào cơ sở dữ liệu SQLite cục bộ. Khi kỹ sư bước lên mặt đất có sóng 4G, WorkManager tự động phát hiện mạng và âm thầm đẩy 25 biên bản lên server theo lô (batch), cập nhật trạng thái đồng bộ thành công mà không làm gián đoạn công việc của kỹ sư.
