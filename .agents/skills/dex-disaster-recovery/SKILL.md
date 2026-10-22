---
name: dex-disaster-recovery
description: Architect Disaster Recovery (DR) strategies, RPO/RTO SLAs, multi-region replication, automated database failover, and cold/warm backup drills. Use when planning business continuity, configuring multi-region failovers, or validating backup restores.
---

# dex-disaster-recovery

## 1. Purpose & Scope
Thiết kế, xây dựng và diễn tập quy trình phục hồi sau thảm họa (Disaster Recovery - DR) và duy trì tính liên tục của hoạt động kinh doanh (Business Continuity); xác lập mục tiêu điểm phục hồi (RPO) và mục tiêu thời gian phục hồi (RTO), triển khai cơ chế sao lưu đa vùng địa lý (Multi-Region Replication), tự động chuyển đổi dự phòng (Automated Failover) và tổ chức định kỳ các cuộc diễn tập khôi phục bản sao lưu thực tế.

## 2. When to Use
- Khi trung tâm dữ liệu chính (Data Center / Cloud Region) bị mất điện, lũ lụt, hoặc đứt cáp quang biển diện rộng.
- Khi cơ sở dữ liệu sản xuất bị tin tặc tấn công mã hóa tống tiền hoặc lập trình viên vô tình chạy nhầm lệnh `DROP DATABASE`.
- Khi cần chuẩn bị hồ sơ tuân thủ an toàn thông tin (ISO 27001, SOC 2) yêu cầu phải có kế hoạch DR được kiểm chứng thực nghiệm.

## 3. When NOT to Use
- Xử lý một lỗi logic nhỏ trong một hàm phần mềm (dùng `dex-root-cause-debugging`).
- Khôi phục một file văn bản bị xóa nhầm trong Git cục bộ (dùng `dex-git-workflow`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Mục tiêu RPO (Recovery Point Objective: Dữ liệu tối đa có thể chấp nhận mất mát, ví dụ: 5 phút).
- Mục tiêu RTO (Recovery Time Objective: Thời gian tối đa để hệ thống hoạt động trở lại, ví dụ: 30 phút).
- Vùng dự phòng thảm họa (Secondary Region: ví dụ Primary tại Singapore, Secondary tại Tokyo).

**Điều kiện tiên quyết:**
- Dữ liệu sao lưu (Backups) được tự động sao chép sang một tài khoản hoặc một vùng địa lý cách ly hoàn toàn.
- Đội ngũ kỹ thuật có tài liệu Runbook các bước phục hồi chi tiết từng lệnh.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Nguyên Tắc Bất Khả Biến: Bản Backup Chưa Được Khôi Phục Thử Là Bản Backup Vô Giá Trị**: Một bản sao lưu chỉ được coi là thành công khi đã được khôi phục thử nghiệm thực tế thành một database hoàn chỉnh và chạy thử câu lệnh `SELECT count(*)`.
- **Tài Khoản Cách Ly Cho Bản Sao Lưu (Air-Gapped Backups)**: Bản sao lưu phải được copy sang một tài khoản đám mây riêng biệt mà quyền admin của tài khoản chính không thể can thiệp xóa được (chống mã độc Ransomware).
- **Đồng Bộ Dữ Liệu Bất Đồng Bộ Giữa Các Vùng**: Do độ trễ địa lý (vài chục miligiây giữa các nước), cơ chế replicate giữa 2 vùng thường là bất đồng bộ (Asynchronous); cần chấp nhận một lượng nhỏ dữ liệu trong vài giây có thể bị mất (RPO > 0).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Cơ sở dữ liệu bị xóa nhầm nhưng bản backup bị lỗi không khôi phục được**: Do backup file bị hỏng mà không ai kiểm tra -> Khắc phục: Tự động hóa tác vụ khôi phục thử bản backup mỗi tuần trên máy chủ test độc lập.
- **DNS Failover chuyển nhầm khi mạng chỉ bị chập chờn 5 giây (Flapping)**: -> Khắc phục: Đặt ngưỡng kiểm tra sức khỏe của Route 53 (chỉ chuyển đổi khi kiểm tra thất bại 3 lần liên tiếp tại nhiều vị trí địa lý khác nhau).

## 6. Step-by-Step Execution Workflow
1. Lựa chọn chiến lược thảm họa theo chi phí và RTO/RPO:
   - *Backup & Restore (RTO: 12-24h, Chi phí thấp)*: Sao lưu định kỳ và khôi phục khi có sự cố.
   - *Pilot Light (RTO: 1-2h, Chi phí vừa)*: Database có replica chạy liên tục ở vùng 2, web servers chỉ bật lên khi có thảm họa.
   - *Warm Standby (RTO: vài phút, Chi phí cao)*: Hệ thống phiên bản thu nhỏ luôn chạy sẵn sàng ở vùng 2.
   - *Multi-Region Active-Active (RTO: 0 giây, Chi phí rất cao)*: Cả 2 vùng đều nhận traffic đồng thời.
2. Thiết lập cơ chế sao lưu tự động (Automated Backups): Chụp ảnh nhanh (Snapshot) hàng ngày kết hợp lưu trữ nhật ký giao dịch liên tục (WAL Archiving) để hỗ trợ khôi phục tại bất kỳ thời điểm nào (Point-in-Time Recovery - PITR).
3. Tự động hóa quá trình chuyển đổi dự phòng cơ sở dữ liệu (Automated DB Failover): Khi node Primary sập, cơ chế giám sát (như Patroni hoặc AWS RDS Multi-AZ) tự động nâng cấp Read Replica thành Primary trong vòng 60 giây.
4. Cấu hình DNS Failover (Cloudflare / AWS Route 53 Health Checks): Tự động định tuyến địa chỉ domain chính sang vùng thứ hai khi vùng thứ nhất không phản hồi HTTP.
5. Xây dựng tài liệu DR Runbook từng bước rõ ràng cho kỹ sư trực chiến.
6. Diễn tập khôi phục thảm họa định kỳ (DR Drill): Định kỳ 3-6 tháng, tiến hành giả lập mất toàn bộ vùng chính trên môi trường staging và khôi phục lại từ bản backup.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```markdown
# DISASTER RECOVERY RUNBOOK: Database Failure Recovery (PITR)
1. Xác định thời điểm xảy ra sự cố (ví dụ: 14:15:00 UTC).
2. Chạy lệnh phục hồi Point-In-Time đến thời điểm 14:14:00 UTC (1 phút trước sự cố):
   aws rds restore-db-instance-to-point-in-time \
     --source-db-instance-identifier prod-db \
     --target-db-instance-identifier prod-db-recovered \
     --restore-time 2026-10-22T14:14:00Z
3. Kiểm tra tính toàn vẹn của dữ liệu sau khi instance sẵn sàng.
4. Cập nhật Connection String của ứng dụng trỏ sang instance mới.
```

### Lệnh xác minh & thực thi:
- Chạy script tự động khôi phục bản backup gần nhất vào database test: `npm run dr:restore-test`
- Kiểm tra trạng thái đồng bộ Multi-AZ Replica: `aws rds describe-db-instances --db-instance-identifier prod-db`
- Kiểm tra cấu hình DNS Health Check: `aws route53 get-health-check-status --health-check-id xxx`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Thời gian khôi phục thực tế đạt chuẩn RTO cam kết (dưới 30 phút).
- QG-05: Toàn bộ dữ liệu sau khi khôi phục kiểm tra đạt 100% tính toàn vẹn (Checksums & row counts khớp).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Bản sao lưu thảm họa bắt buộc phải được mã hóa bằng khóa riêng biệt (AWS KMS Multi-Region Keys).
- Danh sách kỹ sư có quyền kích hoạt chuyển đổi thảm họa (Disaster Recovery Invocation) phải được giới hạn và có xác thực 2 lớp (MFA).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Tài liệu Kế hoạch Phục hồi Thảm họa (`docs/disaster_recovery_runbook.md`).
- Script tự động khôi phục và kiểm chứng tính toàn vẹn của bản sao lưu.
- Báo cáo kết quả diễn tập DR Drill định kỳ.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-disaster-recovery**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
