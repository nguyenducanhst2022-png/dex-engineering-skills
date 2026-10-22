---
name: dex-development-workflow
description: Standard iterative development workflow for AI coding. Enforces breaking tasks down, writing modular code, verifying functionality, stabilizing before upgrading, and committing safe checkpoints. Use when executing software development tasks, building features incrementally, or preventing scope-creep.
---

# DEX Development Workflow

## 1. Purpose & Scope
Thiết lập quy trình phát triển phần mềm chuẩn mực cho AI Coding Agent dựa trên nguyên lý Vibe Coding cốt lõi:
`Chia nhỏ → Viết code → Kiểm tra → Sửa lỗi → Ổn định → Lưu Git → Nâng cấp`

Nguyên tắc tối thượng: **Không nâng cấp hoặc thêm tính năng mới khi chức năng hiện tại chưa chạy ổn định.**

## 2. When to Use
- Khi bắt tay vào lập trình bất kỳ tính năng, module hoặc đoạn mã nào.
- Khi người dùng giao một yêu cầu lớn cần được chia nhỏ thành nhiều bước khả thi.
- Khi cần đảm bảo mã nguồn luôn ở trạng thái ổn định (green/working state) sau mỗi chu kỳ làm việc.

## 3. When NOT to Use
- Chỉ đọc mã nguồn, trả lời câu hỏi giải thích hoặc tra cứu tài liệu mà không thay đổi code.
- Xử lý các sự cố khẩn cấp trên production đòi hỏi quy trình rollback tức thì (sử dụng `dex-release-engineering` hoặc `dex-root-cause-debugging`).

## 4. Prerequisites & Input Context
- Mô tả yêu cầu kỹ thuật hoặc user story cần triển khai.
- Danh sách file thuộc phạm vi chỉnh sửa (Scope).
- Điểm kiểm tra hiện tại (trạng thái tests và Git commit hash gần nhất).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Chia nhỏ Nhiệm vụ (Decomposition)
- Phân rã yêu cầu lớn thành các bước nhỏ độc lập có thời gian thực hiện ngắn.
- Xác định thứ tự logic: Tầng dữ liệu/Model → Tầng nghiệp vụ/Logic → Tầng giao diện/API.

### Bước 2: Viết Code Từng phần (Incremental Implementation)
- Chỉ viết code cho đúng một bước nhỏ tại một thời điểm.
- Giữ code đơn giản, tập trung vào mục tiêu duy nhất của bước đó.
- Không tự ý thêm tính năng phỏng đoán ngoài yêu cầu.

### Bước 3: Kiểm tra Ngay Lập tức (Immediate Verification)
- Chạy thử nghiệm ngay sau khi viết xong một phần mã (Unit test hoặc chạy script kiểm tra nhanh).
- Đảm bảo đoạn mã mới hoạt động đúng như mong đợi.

### Bước 4: Sửa lỗi Tức thời (Instant Bug Fixing)
- Nếu phát hiện lỗi hoặc test rớt, dừng lại và sửa lỗi ngay tại chỗ.
- Không chuyển sang bước kế tiếp khi bước hiện tại còn lỗi.

### Bước 5: Ổn định Mã nguồn (Stabilization)
- Rà soát toàn bộ chức năng vừa thêm: chạy type-check, linter và kiểm thử hồi quy.
- Xác nhận không có tác dụng phụ làm hỏng các phần khác.

### Bước 6: Lưu Điểm An toàn (Git Checkpoint)
- Tạo commit an toàn với thông điệp rõ ràng để ghi nhận trạng thái ổn định.
- Đây là điểm phục hồi (checkpoint) nếu các bước nâng cấp sau gặp sự cố.

### Bước 7: Nâng cấp Tiếp theo (Upgrade / Next Increment)
- Chỉ khi bước trước đã ổn định và lưu Git, mới chuyển sang bước nhỏ tiếp theo trong danh sách.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-development-workflow
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Scope Confined)**: Chỉ chỉnh sửa các file thuộc phạm vi bước hiện tại.
- **QG-03 (Clean Code)**: Không để sót lỗi cú pháp, linter hoặc type check.
- **QG-05 (Working Verified)**: Bước vừa làm phải có bằng chứng kiểm tra chạy thành công (PASS).
- **QG-08 (Clean Commit)**: Mỗi bước ổn định được ghi nhận bằng một commit gọn gàng.

## 10. Security & Safety Boundaries
- **Quy tắc Một Bước**: Tuyệt đối không yêu cầu hoặc cho phép AI viết toàn bộ hệ thống lớn trong một lần duy nhất.
- **Cấm Xây Dựng Trên Nền Hỏng**: Cấm viết thêm tính năng nâng cao khi nền tảng cơ bản chưa kiểm thử thành công.
- **Bảo toàn Mã nguồn Cũ**: Không viết lại toàn bộ file nếu chỉ cần sửa hoặc bổ sung một hàm.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Mã nguồn hoàn thiện theo từng phần tăng dần.
2. Bộ kiểm thử tương ứng cho từng chức năng mới.
3. Chuỗi các Git commits ổn định, minh bạch.
4. Báo cáo tiến độ hoàn thành theo từng bước nhỏ.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-development-workflow** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
