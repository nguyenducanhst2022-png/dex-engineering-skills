---
name: dex-incident-postmortems
description: Facilitate blameless incident postmortems, timeline reconstruction, root cause analysis (5 Whys / Fishbone), corrective action item tracking, SLA/SLO impact calculation, and post-incident learning reviews. Use when analyzing production incidents or outages.
---

# dex-incident-postmortems

## 1. Purpose & Scope
Chủ trì và thực hiện quy trình Đánh giá Sự cố Không Đổ Lỗi (Blameless Incident Postmortems); tái hiện dòng thời gian diễn biến sự cố (Timeline Reconstruction), phân tích nguyên nhân gốc rễ (Root Cause Analysis bằng kỹ thuật 5 Whys và Biểu đồ Xương cá Fishbone), đo lường thiệt hại đối với cam kết mức dịch vụ (SLO / Error Budget Impact), và thiết lập các hành động khắc phục cụ thể có người chịu trách nhiệm và thời hạn hoàn thành.

## 2. When to Use
- Sau khi xảy ra sự cố ngừng dịch vụ (Outage), rò rỉ dữ liệu, hoặc suy giảm hiệu năng nghiêm trọng trên môi trường production.
- Khi một lỗi kỹ thuật lặp đi lặp lại nhiều lần dù đã từng được sửa tạm thời.
- Khi cần nâng cao văn hóa kỹ thuật, chuyển hóa sai lầm thành bài học kinh nghiệm để hệ thống trở nên kiên cố hơn.

## 3. When NOT to Use
- Đang trong lúc sự cố đang diễn ra (Lúc này cần tập trung dập lửa khôi phục dịch vụ, dùng `dex-root-cause-debugging` và `dex-production-monitoring`).
- Lập biên bản kỷ luật cá nhân (Vi phạm nguyên tắc Blameless Postmortem).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Lịch sử nhật ký sự cố (Slack/Teams incident channel history, PagerDuty alerts, Git commit logs, Dashboard screenshots).
- Thời điểm phát sinh lỗi, thời điểm phát hiện, thời điểm thông báo và thời điểm khôi phục hoàn toàn.
- Số lượng người dùng và số tiền giao dịch bị ảnh hưởng.

**Điều kiện tiên quyết:**
- Sự cố đã được giải quyết hoặc đã có biện pháp khắc phục tạm thời đưa hệ thống về trạng thái an toàn.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Văn Hóa Không Đổ Lỗi Tuyệt Đối (Strictly Blameless)**: Trọng tâm của phân tích là hoàn thiện hệ thống, công cụ và quy trình; cấm dùng từ ngữ quy trách nhiệm cá nhân trong tài liệu postmortem.
- **Không Chấp Nhận 'Lỗi Do Con Người' Là Nguyên Nhân Gốc**: 'Lỗi con người' (Human error) là triệu chứng, không phải nguyên nhân; nếu con người có thể gõ nhầm một lệnh làm sập database, đó là lỗi của hệ thống thiếu rào chắn an toàn (Guardrails).
- **Action Items Phải Được Đưa Vào Sprint Tiếp Theo**: Báo cáo postmortem vô giá trị nếu các hành động khắc phục không được đưa vào backlog và hoàn thành trong vòng 14 ngày.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Cùng một sự cố tái diễn sau 2 tháng**: Do các hành động khắc phục trong postmortem bị bỏ xó không ai làm -> Khắc phục: Tự động tạo Jira/GitHub issues cho từng Action Item và theo dõi trong cuộc họp kỹ thuật hàng tuần.
- **Buổi họp postmortem biến thành phiên tòa đổ lỗi khiến kỹ sư che giấu thông tin**: Do người chủ trì thiếu định hướng -> Khắc phục: Áp dụng bản mẫu và nguyên tắc chuẩn của Google SRE Postmortem.

## 6. Step-by-Step Execution Workflow
1. Thu thập dữ liệu khách quan từ mọi nguồn: Nhật ký cảnh báo, biểu đồ metrics, bản ghi chat của đội ứng cứu và commit lịch sử.
2. Tái hiện dòng thời gian chính xác (Chronological Timeline): Ghi nhận T0 (Lỗi phát sinh), T1 (Hệ thống cảnh báo), T2 (Đội ngũ vào cuộc), T3 (Tìm ra nguyên nhân), T4 (Áp dụng bản vá), T5 (Dịch vụ khôi phục 100%).
3. Tính toán các chỉ số ứng cứu cốt lõi: MTTD (Mean Time to Detect) và MTTR (Mean Time to Resolve).
4. Tổ chức buổi họp đánh giá không đổ lỗi (Blameless Review Meeting): Tập trung vào việc *Hệ thống đã thiếu cơ chế bảo vệ nào* thay vì *Ai là người gõ sai lệnh*.
5. Đào sâu nguyên nhân gốc bằng phương pháp 5 Whys để tìm ra căn nguyên ở tầng kiến trúc hoặc quy trình.
6. Xác định rõ: Điều gì đã diễn ra tốt (What went well), Điều gì diễn ra không tốt (What went wrong), và Nơi chúng ta gặp may mắn (Where we got lucky).
7. Đề xuất các hành động sửa chữa cụ thể (Action Items): Phân loại theo Ngăn chặn (Prevent), Phát hiện (Detect), và Giảm thiểu (Mitigate); gắn người phụ trách (Owner) và thời hạn hoàn thành (Due date).

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```markdown
# Incident Postmortem: 2026-10-22 Payment Gateway Outage

## Executive Summary
On Oct 22, 2026, the checkout API experienced a 42-minute outage affecting 3,400 customers due to an unindexed database migration locking the orders table.

## Timeline (UTC)
- 14:02 - Migration executed by deployment pipeline.
- 14:04 - DB CPU spiked to 100%; table lock triggered connection pool exhaustion.
- 14:07 - PagerDuty alert fired: High HTTP 500 error rate.
- 14:15 - Incident response team assembled on bridge.
- 14:26 - Root cause identified as exclusive lock on `orders` table.
- 14:38 - Migration cancelled and locked transactions killed.
- 14:44 - API traffic and DB CPU returned to normal (T5 Resolved).

## 5 Whys Analysis
1. Why did the checkout API fail? Connection pool timed out waiting for PostgreSQL.
2. Why was PostgreSQL unresponsive? The `orders` table was locked exclusively.
3. Why was it locked? A migration was adding an index synchronously.
4. Why was it synchronous? The PR lacked the `CONCURRENTLY` keyword.
5. Why did CI not catch it? Migration linter was not configured to block non-concurrent index creation.

## Action Items
- [ ] [Prevent] Configure `strong_migrations` linter in CI (Owner: @devops, Due: Oct 26)
- [ ] [Detect] Add alert for table locks lasting > 5 seconds (Owner: @dba, Due: Oct 28)
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính đầy đủ của tài liệu Postmortem: `dex postmortem validate docs/postmortems/2026-10-INC-01.md`
- Rà soát trạng thái các Action Items: `gh issue list --label postmortem-action`
- Đo lường ngân sách lỗi còn lại sau sự cố: `dex slo status`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tài liệu Postmortem hoàn thành trong vòng 48 giờ sau sự cố và có timeline chi tiết theo từng phút.
- QG-10: 100% Action Items có người chịu trách nhiệm và issue tracking cụ thể.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Khử các thông tin nhạy cảm của khách hàng (PII) hoặc bí mật hệ thống trước khi chia sẻ tài liệu postmortem rộng rãi trong công ty.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Tài liệu Đánh giá sự cố hoàn chỉnh (`docs/postmortems/2026-10-INCIDENT-01.md`).
- Danh sách Action Items được tạo thành GitHub/Jira Issues.
- Cập nhật tài liệu vận hành (Runbook) tương ứng.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-incident-postmortems**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
