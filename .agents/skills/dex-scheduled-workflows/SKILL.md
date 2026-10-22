---
name: dex-scheduled-workflows
description: Architect scheduled cron workflows, distributed recurring jobs, time-zone handling, missed-execution recovery, and distributed schedule locks. Use when scheduling periodic jobs, daily reports, data aggregations, or cleanup routines.
---

# dex-scheduled-workflows

## 1. Purpose & Scope
Thiết kế, triển khai và quản trị các quy trình định kỳ theo lịch trình (Scheduled Workflows & Cron Jobs) an toàn trong môi trường phân tán; quản lý chuẩn xác múi giờ (Time-zone awareness), xử lý phục hồi khi bị lỡ lượt chạy (Missed execution recovery), và ngăn chặn việc chạy trùng lặp nhiều lần (Duplicate execution) khi ứng dụng được triển khai trên nhiều máy chủ cùng lúc.

## 2. When to Use
- Khi cần chạy các tác vụ định kỳ tự động: Sao lưu database mỗi đêm lúc 2:00 AM, gửi báo cáo doanh thu mỗi sáng thứ Hai lúc 8:00 AM, dọn dẹp các file rác và token hết hạn sau 30 ngày.
- Khi hệ thống mở rộng lên 3 máy chủ chạy song song và phát hiện tác vụ cronjob gửi email bị chạy thành 3 lần cho cùng một khách hàng.
- Khi ứng dụng bị sập trong khung giờ chạy cron và cần cơ chế tự động bù lại lượt chạy đã bị bỏ lỡ.

## 3. When NOT to Use
- Xử lý các tác vụ phát sinh theo sự kiện tức thời do người dùng kích hoạt (dùng `dex-background-job-queues`).
- Các vòng lặp ngắn trong bộ nhớ chỉ chạy trong vài giây.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Biểu thức lịch trình chuẩn Cron (Standard 5-field hoặc 6-field Cron Expression: `0 2 * * *`).
- Múi giờ chuẩn xác (ví dụ: `Asia/Ho_Chi_Minh` hoặc `UTC`).
- Cơ chế khóa phân tán (Redis Distributed Lock hoặc Bảng khóa cơ sở dữ liệu).

**Điều kiện tiên quyết:**
- Đồng hồ hệ thống trên các máy chủ được đồng bộ chuẩn mực qua NTP (Network Time Protocol).
- Có cơ chế lưu trữ lịch sử trạng thái của các lần chạy (Audit log: Start time, End time, Status, Error).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Luôn Dùng Múi Giờ Tường Minh**: Tuyệt đối không để Cronjob chạy theo múi giờ mặc định của máy chủ vì khi di chuyển container sang hạ tầng khác (từ Cloud VN sang Cloud US) giờ chạy sẽ bị nhảy lệch.
- **Không Chạy Tác Vụ Nặng Quá Lâu Trong 1 Luồng**: Nếu tác vụ định kỳ cần xử lý 100,000 khách hàng, Cronjob chỉ làm nhiệm vụ quét ID và đẩy 100,000 sub-jobs vào Queue để Worker xử lý song song; không bao giờ chạy vòng lặp 100,000 lượt trong chính tiến trình Cron.
- **Khóa Phải Có Thời Gian Tự Giải Phóng (Lock TTL)**: Khóa lịch trình bắt buộc phải có thời gian sống (TTL) lớn hơn thời gian chạy dự kiến một chút để tránh kẹt vĩnh viễn nếu máy chủ bị mất điện giữa chừng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Chạy trùng lặp trên 5 containers**: 5 máy chủ cùng gửi 5 email giống hệt nhau cho cùng 1 người lúc 8:00 sáng -> Khắc phục: Sử dụng Distributed Lock qua Redis `SET NX` trước khi bắt đầu công việc.
- **Cronjob bị treo làm tắc nghẽn các lượt chạy sau**: Tác vụ lúc 2:00 AM bị đơ kết nối DB chạy mãi đến 3:00 AM -> Khắc phục: Thiết lập Timeout tối đa cho từng Job (ví dụ: tối đa 30 phút).

## 6. Step-by-Step Execution Workflow
1. Khai báo biểu thức Cron kèm theo múi giờ tường minh (luôn khai báo rõ `timezone: 'Asia/Ho_Chi_Minh'` hoặc chạy trên `UTC`).
2. Triển khai **Distributed Schedule Lock (Khóa Lịch Trình Phân Tán)**: Khi đến giờ chạy, máy chủ nào giành được khóa trong Redis trước (`SET lock:cron:daily-report 'LOCKED' NX EX 3600`) sẽ là máy chủ DUY NHẤT được phép chạy tác vụ đó.
3. Các máy chủ còn lại khi thấy khóa đã tồn tại sẽ tự động bỏ qua mà không chạy trùng lặp.
4. Thực hiện tác vụ theo từng Batch nhỏ để không làm nghẽn CPU hoặc cạn kiệt bộ nhớ RAM.
5. Ghi nhận nhật ký thực thi vào bảng `cron_job_history` kèm thời gian thực tế và kết quả.
6. Xử lý phục hồi khi bị lỡ (Catch-up / Missed Job): Khi máy chủ bật lại sau sự cố, kiểm tra xem tác vụ bắt buộc của ngày hôm nay đã chạy chưa; nếu chưa, tự động chạy bù một cách an toàn.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/scheduler/dailyReportJob.ts
export async function runDailyReportJob() {
  const lockKey = `lock:cron:daily-report:${new Date().toISOString().slice(0, 10)}`;
  const acquired = await redis.set(lockKey, 'LOCKED', 'NX', 'EX', 7200); // Khóa trong 2 giờ
  
  if (!acquired) {
    logger.info('Node khác đang hoặc đã chạy báo cáo ngày này. Bỏ qua.');
    return;
  }
  
  try {
    await generateAndSendDailyReport();
    await logCronSuccess('daily-report');
  } catch (error) {
    await logCronFailure('daily-report', error);
    throw error;
  }
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra biểu thức Cron hợp lệ: `npx cron-parser '0 2 * * *'`
- Chạy thử nghiệm kích hoạt thủ công (Manual Trigger): `npm run cron:trigger -- daily-report`
- Xem nhật ký các lần chạy định kỳ: `SELECT * FROM cron_job_history ORDER BY executed_at DESC LIMIT 5;`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Biểu thức Cron có chỉ định múi giờ tường minh 100%.
- QG-05: Kịch bản giả lập 2 tiến trình cùng kích hoạt một tác vụ định kỳ chỉ có DUY NHẤT 1 tiến trình được thực thi.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Các endpoint kích hoạt thủ công tác vụ định kỳ (Manual Trigger APIs) bắt buộc phải được bảo vệ bằng quyền Quản trị viên cấp cao nhất hoặc secret token nội bộ.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File định nghĩa các lịch trình định kỳ (`src/scheduler/cronRegistry.ts`).
- Module khóa lịch trình phân tán (`src/scheduler/distributedLock.ts`).
- File kiểm thử xác minh cơ chế khóa phân tán.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-scheduled-workflows**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
