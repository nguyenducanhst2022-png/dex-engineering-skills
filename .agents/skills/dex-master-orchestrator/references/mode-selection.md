# Intelligent Execution Mode Selection Guide

## 1. Giới thiệu
Master Orchestrator hỗ trợ 3 chế độ thực thi thông minh được thiết kế nhằm cân bằng tối ưu giữa **tốc độ phát triển** và **mức độ an toàn hệ thống**.

---

## 2. So sánh Tổng quan 3 Chế độ

| Tiêu chí | QUICK MODE | STANDARD MODE | STRICT MODE |
|:---|:---|:---|:---|
| **Mục đích** | Thay đổi nhỏ, sửa lỗi khẩn cấp, cập nhật UI/tài liệu | Phát triển tính năng thông thường, refactor vừa | Thay đổi cấu trúc, DB, bảo mật, release production |
| **Quy trình** | Analyze → Implement → Verify → Report | Analyze → Plan → Implement → Test → Review → Report | Spec → Impact → Risk → Plan → Implement → Tests → Security → Gates → Approval → Release |
| **Phạm vi file** | 1 - 2 files | 2 - 10 files | Bất kỳ quy mô nào có rủi ro cao |
| **Quality Gates** | QG-01, QG-05, QG-08 | QG-01 đến QG-06, QG-08, QG-10 | QG-01 đến QG-10 (Đầy đủ 10 Gates) |
| **Yêu cầu Duyệt từ Người dùng** | Tự động hoàn thành nếu test PASS | Báo cáo tóm tắt kế hoạch trước khi code | Bắt buộc xin phép trước khi sửa DB, cấu hình bảo mật hoặc push release |

---

## 3. Tiêu chí Lựa chọn Chi tiết

### Khi nào chọn QUICK MODE?
- Sửa lỗi cú pháp, sửa lỗi logic nhỏ có thể tái hiện ngay lập tức trong 1 hàm.
- Sửa đổi chuỗi giao diện người dùng (typo, màu sắc CSS đơn giản, label button).
- Bổ sung comment, cập nhật tài liệu nhỏ.
- **Ràng buộc an toàn**: Nếu trong quá trình sửa phát hiện bug phức tạp hơn dự kiến, Orchestrator **phải nâng cấp ngay** lên STANDARD MODE.

### Khi nào chọn STANDARD MODE?
- Viết API endpoint mới hoặc mở rộng tham số API hiện có.
- Thêm màn hình hoặc component giao diện người dùng mới.
- Tái cấu trúc logic trong nội bộ một module mà không thay đổi interface bên ngoài.
- Nâng cấp minor/patch version của dependencies thông thường.

### Khi nào chọn STRICT MODE?
- **Database**: Bất kỳ migration nào liên quan đến xóa cột, đổi kiểu dữ liệu, thêm ràng buộc unique hoặc khóa ngoại.
- **Bảo mật & Xác thực**: Sửa đổi cơ chế JWT, OAuth, hash mật khẩu, kiểm tra quyền hạn (RBAC), CORS.
- **Thanh toán & Giao dịch**: Bất kỳ logic nào liên quan đến tính toán tiền tệ, trừ số dư ví, checkout, tích hợp cổng thanh toán.
- **Hạ tầng & Release**: Thay đổi pipeline CI/CD, phát hành phiên bản Production mới, can thiệp biến môi trường nhạy cảm.

---

## 4. Nguyên tắc Không Hạ cấp Trái phép (No Downgrade Rule)
- Agent tuyệt đối không được tự ý chọn QUICK MODE chỉ để né tránh việc viết test hoặc bỏ qua bước kiểm tra bảo mật.
- Khi có bất kỳ nghi ngờ nào về mức độ ảnh hưởng của thay đổi, Orchestrator luôn chọn chế độ an toàn hơn (thà chọn STRICT/STANDARD hơn là chọn QUICK tùy tiện).
