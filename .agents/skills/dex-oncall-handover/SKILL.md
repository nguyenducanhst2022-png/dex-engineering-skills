---
name: dex-oncall-handover
description: Structure and execute comprehensive on-call shifts, handovers, runbook updates, and incident post-shift briefings with zero knowledge loss. Use to professionalize engineering reliability operations.
---

# dex-oncall-handover

## 1. Purpose & Scope
Thiết lập quy trình bàn giao ca trực vận hành (On-call Handover) có cấu trúc, chuyên nghiệp và liền mạch; bảo đảm chuyển giao đầy đủ thông tin về các sự cố đang diễn ra, các cảnh báo bất thường, các thay đổi triển khai gần nhất và cập nhật runbook thực tế mà không làm thất thoát tri thức giữa các kỹ sư trực ca.

## 2. When to Use
- Thay đổi ca trực hàng tuần giữa các kỹ sư SRE / Dev on-call.
- Sau một tuần trực có nhiều sự cố lớn hoặc các cảnh báo liên tục tái diễn.
- Chuẩn bị cho các kỳ nghỉ lễ dài ngày đòi hỏi sự sẵn sàng cao độ.

## 3. When NOT to Use
- Không biến buổi bàn giao thành cuộc họp phê bình cá nhân về các sai sót trong ca trực.
- Không bàn giao qua loa chỉ bằng một tin nhắn 'Mọi thứ ổn' trên Slack.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Nhật ký sự cố PagerDuty trong 7 ngày qua.
- Danh sách các release/deployment và thay đổi cấu hình hạ tầng trong ca trực.
- Trạng thái các sự cố chưa giải quyết dứt điểm (Unresolved / Mitigated but not Root-caused).
- **Điều kiện tiên quyết**:
- Có template bàn giao ca trực chuẩn hóa trong công cụ tài liệu (Confluence, Notion, Markdown repo).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Handover Meeting: Cuộc gặp ngắn 15-30 phút giữa kỹ sư sắp hết ca (Outgoing) và kỹ sư nhận ca mới (Incoming).
- Actionable Follow-ups: Mọi giải pháp tạm thời (workaround) áp dụng trong ca trực bắt buộc phải được tạo ticket Jira để giải quyết triệt để.
- Runbook Hygiene: Nếu một sự cố xảy ra mà runbook không có hoặc viết sai, kỹ sư trong ca trực có trách nhiệm cập nhật runbook trước khi bàn giao.
- **Quy tắc quyết định kỹ thuật**:
- Nếu có sự cố mức SEV-1/SEV-2 chưa đóng: kỹ sư outgoing phải ở lại cùng phối hợp cho đến khi hệ thống ổn định hoặc được sự đồng thuận bàn giao của lead.
- Kiểm tra quyền truy cập (VPN, PagerDuty schedule, Cloud access) của kỹ sư incoming ngay trong buổi bàn giao.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Kỹ sư hết ca tắt máy đi ngủ trong khi một sự cố nghiêm trọng đang âm ỉ diễn ra nhưng kỹ sư mới vào ca chưa nắm được bối cảnh.

## 6. Step-by-Step Execution Workflow
1. Kỹ sư outgoing điền thông tin vào Handover Template trước giờ bàn giao 2 tiếng.
2. Tổ chức buổi trao đổi trực tiếp (hoặc async call) đi qua từng mục trong biên bản.
3. Rà soát danh sách alert silences và scheduled maintenances sắp tới.
4. Kỹ sư incoming xác nhận nhận ca và kiểm tra công cụ nhận cảnh báo (điện thoại, app).
5. Lưu trữ biên bản bàn giao vào kho lưu trữ nội bộ để phục vụ kiểm toán vận hành.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# On-Call Handover Report
**Ca trực:** Tuần 42 (15/10 - 22/10)
**Outgoing:** Alex Nguyen | **Incoming:** John Doe

### 1. Tổng kết sự cố (Incidents):
- INC-102 (SEV-2): DB connection pool timeout lúc 02:00 sáng thứ Ba. Đã tăng pool lên 200. Ticket xử lý gốc: JIRA-4521.

### 2. Các cảnh báo cần lưu ý:
- Alert `HighDiskUsage` trên node `worker-04` đang bị silence 24h để chờ bảo trì.

### 3. Deployments sắp tới:
- Migration database lớn vào 20:00 thứ Tư.
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra lịch trực PagerDuty và xác nhận ca trực hiện tại
pd schedule list-shifts --schedule-id=P123456
```

## 8. Anti-Patterns & Common Traps
- Giấu giếm các sự cố nhỏ hoặc các thao tác thủ công không chuẩn trong ca trực.
- Để kỹ sư mới vào công ty trực ca chính một mình mà không có shadow/mentor dự phòng.

## 9. Quality Gates & Acceptance Criteria
- 100% các sự cố trong ca trực đều có liên kết tới Post-mortem hoặc Jira action item.
- Kỹ sư nhận ca xác nhận đã truy cập được toàn bộ hệ thống giám sát và paging.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Thu hồi các quyền truy cập tạm thời (Elevated break-glass access) đã cấp cho kỹ sư trong ca trực khi hết phiên.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Biên bản bàn giao ca trực hoàn chỉnh theo mẫu chuẩn.
- Danh sách cập nhật tài liệu Runbooks cho các sự cố mới.

## 13. Related & Complementary Skills
dex-incident-postmortems, dex-alert-quality-engineering, dex-operational-game-days

## 14. Realistic Usage Example
### Tình huống thực tế:
Một sự cố thanh toán bị lặp lại 3 lần trong 1 tháng vì mỗi lần kỹ sư trực chỉ khởi động lại pod mà không ghi lại. Sau khi áp dụng quy trình Handover chuẩn, kỹ sư ca trước ghi rõ cảnh báo rò rỉ bộ nhớ, kỹ sư ca sau đã chủ động phân tích heap dump và tìm ra lỗi leak trong thư viện HTTP client.
