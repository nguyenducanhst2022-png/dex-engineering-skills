---
name: dex-task-delegation
description: Structure and delegate engineering tasks clearly to AI coding agents with defined goals, explicit scope boundaries, technical constraints, verification criteria, and reporting standards. Use when assigning tasks, breaking down user instructions, or preparing autonomous agent execution contexts.
---

# DEX Task Delegation

## 1. Purpose
Quy chuẩn hóa cách giao việc cho AI Coding Agent nhằm loại bỏ sự mơ hồ, tránh việc AI tự suy diễn sai hướng và giảm thiểu số lần phải sửa đi sửa lại.

Quy trình giao việc chuẩn:
`Mục tiêu → Phạm vi → Ràng buộc → Viết code → Kiểm tra → Báo cáo`

Nguyên tắc cốt lõi: **Một nhiệm vụ tại một thời điểm. Hướng dẫn càng cụ thể, AI thực hiện càng chính xác.**

## 2. When to Use
- Trước khi bắt đầu viết code cho bất kỳ yêu cầu nào.
- Khi chuyển đổi yêu cầu từ ngôn ngữ tự nhiên của người dùng thành chỉ dẫn kỹ thuật cho AI.
- Khi giao việc giữa các Agent trong mô hình đa Agent (Multi-Agent).

## 3. When Not to Use
- Khi nhiệm vụ đã có bản đặc tả kỹ thuật (SDD) đầy đủ và đang ở bước thực thi mã nguồn.
- Khi thực hiện các câu lệnh kiểm tra trạng thái chỉ đọc (như `git status`, `ls`).

## 4. Inputs
- Yêu cầu thô từ người dùng hoặc Product Owner.
- Cấu trúc thư mục dự án và công nghệ đang sử dụng.
- Danh sách các file dự kiến cần sửa đổi hoặc tạo mới.

## 5. Workflow

### Bước 1: Xác định Mục tiêu Duy nhất (Single Objective)
- Nêu rõ đích đến của nhiệm vụ trong 1-2 câu ngắn gọn.
- Tập trung vào giá trị cụ thể cần đạt được, không ôm đồm nhiều việc khác nhau cùng lúc.

### Bước 2: Thiết lập Phạm vi Rõ ràng (Scope Definition)
- Liệt kê chính xác các file và thư mục ĐƯỢC PHÉP chỉnh sửa.
- Nêu rõ các file/vùng mã nguồn CẤM CHẠM VÀO (ví dụ: schema database lõi, config production).

### Bước 3: Định nghĩa Ràng buộc Kỹ thuật (Technical Constraints)
- Chỉ định thư viện, công nghệ và phiên bản bắt buộc tuân thủ.
- Ràng buộc về kiến trúc: không thêm dependency ngoài, giữ nguyên kiểu dữ liệu trả về, tuân thủ TypeScript strict mode...

### Bước 4: Hướng dẫn Viết Code (Implementation Guidance)
- Cung cấp mô tả luồng logic hoặc interface mẫu nếu có.
- Yêu cầu AI chỉ viết mã trong phạm vi đã xác định ở Bước 2.

### Bước 5: Tiêu chí Kiểm tra (Verification Criteria)
- Chỉ định rõ lệnh kiểm thử cần chạy (ví dụ: `npm test -- tests/auth.test.ts`).
- Nêu rõ kết quả mong đợi (ví dụ: 5/5 test pass, không có warning).

### Bước 6: Định dạng Báo cáo (Reporting Format)
- Yêu cầu AI báo cáo: file đã tạo/sửa, kết quả chạy lệnh kiểm tra, diff tóm tắt và ghi chú rủi ro nếu có.

## 6. Quality Gates
- **QG-01 (Scope Bound)**: 100% các file sửa đổi nằm trong danh sách phạm vi đã thỏa thuận.
- **QG-02 (Constraint Checked)**: Không vi phạm bất kỳ ràng buộc kỹ thuật nào đã nêu.
- **QG-10 (Report Completed)**: Báo cáo đầy đủ theo đúng cấu trúc 6 phần.

## 7. Safety Rules
- **Nguyên tắc "Một việc một lúc"**: Cấm giao đồng thời 3 tính năng lớn trong cùng một prompt duy nhất.
- **Không suy diễn ngoài phạm vi**: AI không được tự ý "tiện tay" dọn dẹp hoặc refactor file khác nằm ngoài phạm vi được giao.
- **Phải có tiêu chí nghiệm thu**: Không bao giờ giao việc mà không nêu rõ cách kiểm chứng kết quả.

## 8. Expected Outputs
Bản chỉ dẫn nhiệm vụ (Task Delegation Brief) chuẩn hóa gồm 6 trường:
1. `Mục tiêu (Objective)`
2. `Phạm vi (Scope: Allowed & Forbidden)`
3. `Ràng buộc (Constraints)`
4. `Yêu cầu triển khai (Implementation)`
5. `Kiểm tra (Verification)`
6. `Báo cáo (Report Format)`

## 9. Failure Handling
- Nếu AI hiểu sai mục tiêu hoặc sửa lan man ra ngoài phạm vi: Dừng ngay lập tức, rollback mã nguồn và tái cấu trúc lại Task Brief với ràng buộc chặt chẽ hơn trước khi cho AI thử lại.

## 10. Completion Criteria
- Nhiệm vụ được AI thực hiện chính xác theo mục tiêu, không vi phạm ràng buộc và có báo cáo kiểm chứng đầy đủ.

---

## Real-world Example
```markdown
### TASK BRIEF: Sửa lỗi hiển thị ngày tháng bài viết
1. **Mục tiêu**: Chuyển định dạng ngày bài viết từ timestamp sang định dạng 'DD/MM/YYYY'.
2. **Phạm vi**: 
   - Được phép sửa: `src/components/PostDate.vue`
   - Cấm sửa: `src/api/**`, `src/utils/date.ts`
3. **Ràng buộc**: Sử dụng hàm `formatDisplayDate` đã có sẵn trong `src/utils/date.ts`, không cài thêm thư viện date mới (như moment, dayjs).
4. **Kiểm tra**: Chạy `npm run test:unit tests/PostDate.spec.ts`.
5. **Báo cáo**: Nêu rõ file đã sửa và kết quả kiểm tra PASS.
```
