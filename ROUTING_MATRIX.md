# DEX Skill Routing Matrix & Quality Gates Specification

Ma trận định tuyến và quyết định kỹ thuật của **Master Orchestrator** trong DEX Engineering Skills Pack v1.0.0.

---

## 1. Ma Trận Quyết Định Theo Loại Công Việc (Task Decision Matrix)

| Loại Công Việc (Task Category) | Chế Độ Thực Thi Đề Xuất | Chuỗi Kỹ Năng Kích Hoạt Theo Thứ Tự | Quality Gates Bắt Buộc | Nguy Cơ Chính Cần Kiểm Soát |
|:---|:---|:---|:---|:---|
| **Sửa Lỗi Nhanh (Bug Fix)** | **QUICK MODE** (nếu <=2 files)<br>**STANDARD MODE** (nếu logic phức tạp) | 1. `dex-root-cause-debugging`<br>2. `dex-code-verification`<br>3. `dex-testing-engineering`<br>4. `dex-git-workflow` | QG-01, QG-05, QG-06, QG-08, QG-10 | Sửa triệu chứng mà bỏ qua nguyên nhân gốc; gây lỗi hồi quy ở nơi khác. |
| **Phát Triển Tính Năng Mới (Feature)** | **STANDARD MODE** | 1. `dex-specification-driven`<br>2. `dex-change-impact-analysis`<br>3. `dex-development-workflow`<br>4. `dex-testing-engineering`<br>5. `dex-code-review`<br>6. `dex-git-workflow` | QG-01, QG-02, QG-03, QG-04, QG-05, QG-08, QG-10 | Hiểu sai yêu cầu người dùng; phình to phạm vi (Scope creep); thiếu test. |
| **Tối Ưu Hóa Hiệu Năng (Performance)** | **STANDARD MODE** | 1. `dex-performance-optimization`<br>2. `dex-testing-engineering`<br>3. `dex-code-review`<br>4. `dex-git-workflow` | QG-01, QG-02, QG-05, QG-06, QG-08, QG-10 | Tối ưu cảm tính; làm code khó đọc; làm sai lệch kết quả tính toán. |
| **Kiểm Toán & Vá Lỗ Hổng Bảo Mật** | **STRICT MODE** | 1. `dex-security-audit`<br>2. `dex-root-cause-debugging`<br>3. `dex-testing-engineering`<br>4. `dex-git-workflow` | QG-01, QG-02, QG-05, QG-07, QG-08, QG-10 | Lộ bí mật trong commit; vá hời hợt; để lọt lỗ hổng injection nguy hiểm. |
| **Tái Cấu Trúc Mã Nguồn (Refactoring)** | **STANDARD MODE** | 1. `dex-technical-debt-refactoring`<br>2. `dex-change-impact-analysis`<br>3. `dex-testing-engineering`<br>4. `dex-code-review`<br>5. `dex-git-workflow` | QG-01, QG-03, QG-05, QG-06, QG-08 | Thay đổi hành vi cũ của hệ thống; không có test bảo vệ trước khi sửa. |
| **Thay Đổi Database / Schema Migration** | **STRICT MODE** | 1. `dex-database-engineering`<br>2. `dex-change-impact-analysis`<br>3. `dex-testing-engineering`<br>4. `dex-code-review`<br>5. `dex-git-workflow` | QG-01, QG-02, QG-04, QG-05, QG-06, QG-08, QG-10 | Mất mát dữ liệu; khóa bảng gây gián đoạn dịch vụ; thiếu hàm rollback. |
| **Xây Dựng / Cập Nhật API** | **STANDARD MODE** | 1. `dex-api-engineering`<br>2. `dex-specification-driven`<br>3. `dex-testing-engineering`<br>4. `dex-git-workflow` | QG-01, QG-02, QG-03, QG-05, QG-08 | Phá vỡ tính tương thích ngược; thiếu validate input; mã lỗi sai chuẩn. |
| **Đóng Gói & Phát Hành (Production Release)** | **STRICT MODE** | 1. `dex-testing-engineering`<br>2. `dex-security-audit`<br>3. `dex-release-engineering`<br>4. `dex-production-monitoring`<br>5. `dex-git-workflow` | **Toàn bộ 10 Gates** (QG-01 đến QG-10) | Phát hành code lỗi; không thể rollback; thiếu ghi nhận changelog. |
| **Khởi Tạo Dự Án Mới (Greenfield)** | **STANDARD MODE** hoặc **STRICT MODE** | 1. `dex-specification-driven`<br>2. `dex-software-architecture`<br>3. `dex-code-organization`<br>4. `dex-task-delegation`<br>5. `dex-development-workflow`<br>6. `dex-testing-engineering`<br>7. `dex-git-workflow` | QG-01, QG-02, QG-03, QG-04, QG-05, QG-08, QG-09 | Kiến trúc phức tạp quá mức; dồn code vào god-file; thiếu định hướng. |
| **Phát Triển Toàn Vòng Đời (End-to-End)** | **STRICT MODE** | 1. `dex-end-to-end-engineering` (phối hợp toàn chuỗi 30 skills) | **Toàn bộ 10 Gates** (QG-01 đến QG-10) | Mất kiểm soát tiến độ; thiếu đồng bộ giữa các tầng kiến trúc. |

---

## 2. Ánh Xạ Chi Tiết 10 Quality Gates Vào Từng Chế Độ

| Quality Gate | Tiêu Chí Kiểm Chứng | QUICK MODE | STANDARD MODE | STRICT MODE |
|:---|:---|:---:|:---:|:---:|
| **QG-01: Scope Defined** | Phạm vi file được phép sửa được xác định rõ ràng. | **BẮT BUỘC** | **BẮT BUỘC** | **BẮT BUỘC** |
| **QG-02: Spec Compliant** | Đáp ứng 100% Acceptance Criteria đã đề ra. | Tùy chọn | **BẮT BUỘC** | **BẮT BUỘC** |
| **QG-03: Lint & Typecheck** | Không có lỗi cú pháp, linting hoặc type check. | Khuyến nghị | **BẮT BUỘC** | **BẮT BUỘC** |
| **QG-04: Build Succeeded** | Biên dịch thành công production build artifact. | Tùy chọn | **BẮT BUỘC** | **BẮT BUỘC** |
| **QG-05: Tests PASS** | 100% các bài kiểm thử liên quan đạt PASS. | **BẮT BUỘC** | **BẮT BUỘC** | **BẮT BUỘC** |
| **QG-06: No Regressions** | Không làm phát sinh lỗi trên các tính năng hiện có. | Khuyến nghị | **BẮT BUỘC** | **BẮT BUỘC** |
| **QG-07: Security Audit** | 0 secrets bị lộ, 0 lỗ hổng Critical/High. | Tùy chọn | Khuyến nghị | **BẮT BUỘC** |
| **QG-08: Diff Reviewed** | Git diff sạch sẽ, không có console log hay rác. | **BẮT BUỘC** | **BẮT BUỘC** | **BẮT BUỘC** |
| **QG-09: Docs Updated** | Tài liệu dự án hoặc changelog được cập nhật. | Tùy chọn | Khuyến nghị | **BẮT BUỘC** |
| **QG-10: Verified Evidence** | Có log terminal thực tế chứng minh kết quả. | Khuyến nghị | **BẮT BUỘC** | **BẮT BUỘC** |

---

## 3. Quy Tắc Giải Quyết Xung Đột & Rẽ Nhánh
- **Khi một Quality Gate bị FAIL**: Master Orchestrator lập tức dừng quy trình chuyển tiếp, kích hoạt kỹ năng tương ứng (ví dụ `dex-root-cause-debugging` nếu QG-05 rớt, hoặc `dex-security-audit` nếu QG-07 rớt) để khắc phục dứt điểm.
- **Quy tắc không nhảy cóc**: Nghiêm cấm việc bỏ qua bài kiểm tra để thực hiện commit hoặc release. Nếu môi trường không thể chạy test, trạng thái cổng phải được ghi rõ là `NOT VERIFIED` kèm lý do.
