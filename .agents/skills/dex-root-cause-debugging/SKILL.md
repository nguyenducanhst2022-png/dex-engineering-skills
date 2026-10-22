---
name: dex-root-cause-debugging
description: Root cause analysis and deterministic bug resolution methodology. Reproduces defects with failing tests, isolates fundamental root causes, applies targeted fixes, and prevents regressions. Use when investigating bugs, fixing unexpected test failures, resolving exceptions, or eliminating persistent software defects.
---

# DEX Root Cause Debugging

## 1. Purpose & Scope
Điều tra, cô lập và giải quyết triệt để các lỗi phần mềm tận gốc rễ, ngăn chặn tình trạng "sửa mò", che giấu triệu chứng hoặc làm phát sinh lỗi hồi quy ở các phần khác.

Quy trình debug chuẩn:
`Phát hiện lỗi → Tái hiện lỗi → Phân tích nguyên nhân → Sửa tận gốc → Test lại → Kiểm tra hồi quy → Ổn định`

Nguyên tắc cốt lõi: **Không sửa mò, không che giấu lỗi, không chỉ sửa triệu chứng bề mặt mà bỏ qua nguyên nhân gốc.**
Ghi nhớ sống còn: **Sửa hết thông báo lỗi (Error message) ≠ Đã giải quyết được nguyên nhân gốc.**

## 2. When to Use
- Khi nhận được thông báo lỗi, exception stack trace hoặc hành vi sai khác kỳ vọng.
- Khi một bài kiểm thử tự động bị rớt (FAIL).
- Khi người dùng báo cáo lỗi chập chờn (flaky bug) hoặc dữ liệu bị sai lệch bất thường.
- Khi mã nguồn sửa trước đó làm phát sinh lỗi mới ở nơi khác.

## 3. When NOT to Use
- Thêm tính năng mới hoàn toàn khi hệ thống không có bug nào cần giải quyết.
- Tối ưu hóa hiệu năng thuần túy cho mã nguồn vốn dĩ đã chạy đúng (dùng `dex-performance-optimization`).

## 4. Prerequisites & Input Context
- Thông báo lỗi đầy đủ, Stack trace, file log hệ thống.
- Các bước thao tác dẫn đến lỗi (Steps to Reproduce) và dữ liệu đầu vào cụ thể.
- Mã nguồn tại các vị trí nghi ngờ phát sinh sự cố.

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Tiếp Nhận & Ghi Nhận Lỗi (Defect Triage)
- Đọc kỹ thông báo lỗi và stack trace: Xác định chính xác file, hàm và dòng code xảy ra sự cố.
- Phân biệt giữa lỗi cú pháp (Syntax), lỗi thực thi (Runtime exception) và lỗi logic nghiệp vụ (Logic bug).

### Bước 2: Tái Hiện Lỗi Xác Thực (Deterministic Reproduction)
- **Tạo một bài kiểm tra tự động bị rớt (Failing Test)** tái hiện chính xác 100% tình huống gây lỗi với dữ liệu cụ thể.
- Nếu không thể viết test ngay: Tạo một script kiểm thử độc lập ngắn gọn để kích hoạt lỗi.
- Không bao giờ bắt đầu sửa code khi chưa tái hiện được lỗi.

### Bước 3: Phân Tích Nguyên Nhân Gốc (Root Cause Analysis - 5 Whys)
- Đặt câu hỏi tìm nguyên nhân sâu xa:
  - *Tại sao biến bị undefined?* → Vì hàm `getUser` trả về null khi không tìm thấy ID.
  - *Tại sao ID không tìm thấy?* → Vì tham số truyền từ client bị thiếu padding số 0.
- Xác định điểm sai lệch gốc thay vì chỉ chèn `if (!x) return` để tắt thông báo lỗi.

### Bước 4: Sửa Lỗi Tận Gốc (Targeted Root Fix)
- Chỉnh sửa logic tại đúng nơi phát sinh nguyên nhân.
- Giữ giải pháp sửa lỗi tối giản, không viết lại những vùng code xung quanh không liên quan.
- Bổ sung validation hoặc xử lý biên đúng chuẩn mực.

### Bước 5: Kiểm Thử Lại (Test Verification)
- Chạy lại bài kiểm tra tái hiện lỗi ở Bước 2.
- Bài kiểm tra phải chuyển từ trạng thái `FAIL` sang `PASS` hoàn toàn.

### Bước 6: Kiểm Tra Hồi Quy Toàn Diện (Regression Testing)
- Chạy toàn bộ test suite của module và các module phụ thuộc.
- Xác nhận bản vá lỗi không làm rớt bất kỳ bài test nào đã có từ trước.

### Bước 7: Ổn Định & Lưu Git (Stabilization & Commit)
- Lưu commit chuẩn: `fix(scope): resolve root cause of [defect description]`.
- Giữ lại bài kiểm tra mới tạo ở Bước 2 trong repository để trở thành regression test vĩnh viễn ngăn lỗi tái diễn.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-root-cause-debugging
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Scope Confined)**: Bản sửa lỗi chỉ can thiệp vào các thành phần liên quan trực tiếp đến nguyên nhân gốc.
- **QG-05 (Failing Test Passes)**: Test case tái hiện lỗi chuyển từ FAIL sang PASS.
- **QG-06 (No Regressions)**: 100% các bài test cũ vẫn đạt PASS.
- **QG-08 (Clean Diff)**: Không để sót console log, debug print hoặc comment tạm thời.

## 10. Security & Safety Boundaries
- **Cấm Tuyệt Đối "Bịt Lỗ Hổng Ảo"**: Cấm dùng `catch (e) {}` rỗng hoặc `@ts-ignore` bừa bãi để dập tắt lỗi.
- **Không Đoán Mò**: Không thay đổi code ngẫu nhiên theo kiểu "thử xem có hết lỗi không" khi chưa hiểu nguyên nhân.
- **Bảo Vệ Dữ Liệu**: Không chạy các câu lệnh xóa hoặc cập nhật dữ liệu hàng loạt trên môi trường thật để debug.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Bản phân tích nguyên nhân gốc (Root Cause Summary).
2. Test case tái hiện lỗi mới được bổ sung vào bộ kiểm thử.
3. Bản vá lỗi mã nguồn sạch sẽ, dứt điểm.
4. Bằng chứng kiểm thử PASS sau khi sửa.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-root-cause-debugging** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
