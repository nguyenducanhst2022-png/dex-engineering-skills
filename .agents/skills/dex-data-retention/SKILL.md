---
name: dex-data-retention
description: Implement data retention policies, automated PII data purging, soft-delete lifecycles, hard-delete schedules, and GDPR/CCPA right-to-be-forgotten compliance. Use when enforcing regulatory retention, purging stale audit logs, or cleaning up user data.
---

# dex-data-retention

## 1. Purpose & Scope
Thiết kế và triển khai chính sách lưu giữ và xóa bỏ dữ liệu có kiểm soát (Data Retention & Purging Policies); tự động hóa quy trình dọn dẹp dữ liệu hết hạn (Purge Stale Data), quản lý vòng đời xóa mềm (Soft-Delete) sang xóa cứng (Hard-Delete), tuân thủ quyền được lãng quên theo luật bảo vệ dữ liệu (GDPR / CCPA Right to be Forgotten) và ngăn chặn việc cơ sở dữ liệu bị phình to vô hạn.

## 2. When to Use
- Khi bảng log, audit trail, thông báo hoặc bảng token phiên đăng nhập phình to lên hàng trăm triệu dòng làm chậm hệ thống.
- Khi nhận được yêu cầu của người dùng muốn xóa vĩnh viễn tài khoản và toàn bộ thông tin cá nhân (GDPR Data Deletion Request).
- Khi doanh nghiệp cần tuân thủ quy định pháp luật: Chỉ được phép lưu giữ dữ liệu vị trí GPS của người dùng tối đa 90 ngày.

## 3. When NOT to Use
- Xóa dữ liệu tạm trong bộ nhớ RAM (dùng `dex-caching-strategies`).
- Xóa bảng dữ liệu trong một đợt refactor schema cơ sở dữ liệu (dùng `dex-database-engineering`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bảng quy định thời gian lưu giữ cho từng loại dữ liệu (Retention Matrix: Log = 30 ngày, Inactive Sessions = 7 ngày, Financial Records = 5 năm).
- Danh sách các bảng dữ liệu chứa thông tin định danh cá nhân (PII).
- Cơ chế xóa mục tiêu (Batch Deletion Worker, Database Partition Drop, hoặc Time-to-Live TTL).

**Điều kiện tiên quyết:**
- Đã xác định rõ ràng các ràng buộc khóa ngoại (Foreign Keys) để tránh lỗi vi phạm toàn vẹn khi xóa bản ghi cha.
- Có bản sao lưu dự phòng (Backup) độc lập trước khi kích hoạt quy trình xóa dữ liệu hàng loạt.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Cấm Xóa Hàng Loạt Trong Giờ Cao Điểm**: Các tác vụ Hard-Delete dữ liệu cũ phải được lên lịch chạy vào ban đêm (khung giờ thấp điểm 01:00 - 04:00 AM).
- **Ưu Tiên Drop Partition Thay Vì Delete Dòng**: Nếu bảng có dung lượng lớn và có chính sách xóa định kỳ, BẮT BUỘC phải thiết kế phân vùng (Partitioning) ngay từ đầu để dùng lệnh `DROP PARTITION` thay vì chạy `DELETE`.
- **Ẩn Danh Hóa Cho Dữ Liệu Báo Cáo**: Với các đơn hàng liên quan đến kế toán tài chính không được phép xóa theo luật, thay vì xóa dòng đơn hàng, hãy làm sạch thông tin PII: gán `customer_name = 'ANONYMIZED'`, `phone = '***'` để giữ nguyên số liệu doanh thu.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lệnh Delete làm khóa toàn bộ bảng khiến web server bị treo**: Do chạy câu lệnh `DELETE` xóa 2 triệu dòng một lúc làm khóa bảng trong 15 phút -> Khắc phục: Xóa theo vòng lặp batch nhỏ 1,000 dòng: `DELETE FROM logs WHERE id IN (SELECT id FROM logs WHERE ... LIMIT 1000)`.
- **Xóa nhầm dữ liệu đang hoạt động**: Do điều kiện `WHERE` bị viết sai -> Khắc phục: Luôn chạy thử bằng `SELECT count(*)` trước, yêu cầu review code nghiêm ngặt và kiểm tra trên staging.

## 6. Step-by-Step Execution Workflow
1. Xây dựng Ma trận Lưu giữ Dữ liệu (Data Retention Matrix) được phê duyệt bởi bộ phận Pháp chế và Kỹ thuật.
2. Phân biệt rõ Xóa Mềm và Xóa Cứng:
   - *Xóa mềm (Soft Delete)*: Cập nhật `deleted_at = NOW()`, ẩn dữ liệu khỏi giao diện người dùng nhưng vẫn giữ trong 30 ngày để người dùng có cơ hội khôi phục tài khoản nếu đổi ý.
   - *Xóa cứng (Hard Delete)*: Sau 30 ngày kể từ `deleted_at`, worker tự động xóa vĩnh viễn hoặc ẩn danh hóa (Anonymization) thông tin cá nhân.
3. Xóa theo từng mẻ nhỏ (Chunked / Batched Deletes): Tuyệt đối không chạy lệnh `DELETE FROM logs WHERE created_at < ...` xóa 10 triệu dòng một lúc; phải chia thành các mẻ nhỏ 1,000 dòng kết hợp `LIMIT` và giãn cách nghỉ (sleep) để không làm khóa bảng database.
4. Đối với dữ liệu dạng chuỗi thời gian lớn (Time-Series Logs): Áp dụng kỹ thuật phân vùng bảng theo tháng (Table Partitioning); khi dữ liệu hết hạn, chỉ cần chạy lệnh `DROP TABLE logs_y2025m01` diễn ra trong 0.1 giây mà không tốn tài nguyên CPU hay sinh rác database.
5. Xử lý yêu cầu GDPR: Xây dựng service chuyên trách tìm kiếm và xóa/ẩn danh hóa toàn bộ thông tin liên quan đến `userId` trên toàn bộ các bảng trong vòng 72 giờ.
6. Ghi nhật ký kiểm toán (Audit Trail) xác nhận việc xóa dữ liệu đã hoàn thành.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/workers/purgeLogsWorker.ts (Xóa theo batch an toàn)
export async function purgeOldLogsInBatches(daysToKeep = 90, batchSize = 1000) {
  let deletedRows = 0;
  const cutoffDate = new Date(Date.now() - daysToKeep * 24 * 60 * 60 * 1000);
  
  while (true) {
    const result = await db.query(
      `DELETE FROM audit_logs 
       WHERE id IN (
         SELECT id FROM audit_logs 
         WHERE created_at < $1 
         LIMIT $2
       )`,
      [cutoffDate, batchSize]
    );
    deletedRows += result.rowCount;
    if (result.rowCount < batchSize) break;
    await new Promise(r => setTimeout(r, 200)); // Nghỉ 200ms giữa các batch
  }
  logger.info(`Đã dọn dẹp thành công ${deletedRows} bản ghi cũ.`);
}
```

### Lệnh xác minh & thực thi:
- Chạy thử nghiệm tác vụ xóa ở chế độ Dry-Run (chỉ in số lượng sẽ xóa): `npm run purge:dry-run -- --table=audit_logs`
- Kiểm tra số lượng bản ghi đã được dọn dẹp: `SELECT count(*) FROM audit_logs WHERE created_at < NOW() - INTERVAL '90 days';`
- Chạy unit test kiểm tra luồng xóa mềm sang xóa cứng: `npm test -- tests/retention/userPurge.spec.ts`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Mọi bảng dữ liệu nhật ký đều có chính sách TTL hoặc Retention Policy rõ ràng.
- QG-06: Tác vụ xóa dữ liệu hàng loạt không làm tăng CPU cơ sở dữ liệu vượt quá ngưỡng 30% trong lúc chạy.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Toàn bộ quy trình xóa dữ liệu người dùng theo GDPR phải có biên bản ghi nhận mã băm (Cryptographic proof of deletion) để giải trình với cơ quan kiểm toán.
- Ngăn chặn triệt để nguy cơ tiêm nhiễm SQL trong các câu lệnh xóa dữ liệu động.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Worker dọn dẹp dữ liệu định kỳ (`src/workers/dataRetentionWorker.ts`).
- File migration thiết lập Table Partitioning theo thời gian.
- Bộ test xác minh tính năng ẩn danh hóa dữ liệu PI.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-data-retention**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
