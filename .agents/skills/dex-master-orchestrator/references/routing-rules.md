# DEX Skill Routing Rules & Dependency Matrix

## 1. Nguyên tắc Định tuyến (Routing Principles)
- **Tối thiểu hóa (Minimal Activation)**: Chỉ kích hoạt những kỹ năng thực sự cần thiết để giải quyết nhiệm vụ. Không bao giờ kích hoạt toàn bộ 30 kỹ năng cùng lúc.
- **Tuần tự theo phụ thuộc (Dependency Driven)**: Kỹ năng tạo đầu vào (Inputs) phải hoàn thành trước kỹ năng tiêu thụ đầu vào.
- **Chặn theo Cổng Chất lượng (Gate Blocking)**: Kỹ năng tiếp theo chỉ được bắt đầu khi kỹ năng trước đó đã vượt qua Quality Gate tương ứng.

---

## 2. Bảng Định tuyến Chuẩn theo Loại Nhiệm vụ

| Loại Nhiệm vụ | Danh sách Skills cần Kích hoạt theo Thứ tự | Chế độ Đề xuất | Quality Gates Bắt buộc |
|:---|:---|:---|:---|
| **Sửa lỗi khẩn / Bug Fix** | 1. `dex-root-cause-debugging`<br>2. `dex-code-verification`<br>3. `dex-testing-engineering`<br>4. `dex-git-workflow` | QUICK hoặc STANDARD | QG-01, QG-05, QG-06, QG-08 |
| **Thêm tính năng mới (Feature)** | 1. `dex-specification-driven`<br>2. `dex-change-impact-analysis`<br>3. `dex-development-workflow`<br>4. `dex-testing-engineering`<br>5. `dex-code-review`<br>6. `dex-git-workflow` | STANDARD | QG-01, QG-02, QG-03, QG-04, QG-05, QG-08 |
| **Tối ưu Hiệu năng (Performance)** | 1. `dex-performance-optimization`<br>2. `dex-testing-engineering`<br>3. `dex-code-review`<br>4. `dex-git-workflow` | STANDARD | QG-01, QG-05, QG-06, QG-08, QG-10 |
| **Kiểm toán Bảo mật (Security Audit)** | 1. `dex-security-audit`<br>2. `dex-root-cause-debugging`<br>3. `dex-testing-engineering`<br>4. `dex-git-workflow` | STRICT | QG-01, QG-02, QG-05, QG-07, QG-08 |
| **Tái cấu trúc / Trả nợ kỹ thuật** | 1. `dex-technical-debt-refactoring`<br>2. `dex-change-impact-analysis`<br>3. `dex-testing-engineering`<br>4. `dex-code-review`<br>5. `dex-git-workflow` | STANDARD hoặc STRICT | QG-01, QG-03, QG-05, QG-06, QG-08 |
| **Thay đổi Database / Schema** | 1. `dex-database-engineering`<br>2. `dex-change-impact-analysis`<br>3. `dex-testing-engineering`<br>4. `dex-code-review`<br>5. `dex-git-workflow` | STRICT | QG-01, QG-02, QG-04, QG-05, QG-06, QG-08 |
| **Thiết kế Kiến trúc Hệ thống** | 1. `dex-specification-driven`<br>2. `dex-software-architecture`<br>3. `dex-code-organization`<br>4. `dex-task-delegation` | STRICT | QG-01, QG-02, QG-09 |
| **Đóng gói & Phát hành (Release)** | 1. `dex-testing-engineering`<br>2. `dex-security-audit`<br>3. `dex-release-engineering`<br>4. `dex-production-monitoring`<br>5. `dex-git-workflow` | STRICT | QG-01 đến QG-10 (Toàn bộ) |
| **Khởi tạo Dự án Mới (Greenfield)** | 1. `dex-specification-driven`<br>2. `dex-software-architecture`<br>3. `dex-code-organization`<br>4. `dex-task-delegation`<br>5. `dex-development-workflow`<br>6. `dex-testing-engineering`<br>7. `dex-git-workflow` | STANDARD hoặc STRICT | QG-01, QG-02, QG-03, QG-04, QG-05, QG-08, QG-09 |
| **Dự án Lớn Toàn diện (End-to-End)** | 1. `dex-end-to-end-engineering` (kết hợp Master Orchestrator điều phối toàn chuỗi 30 skills) | STRICT | QG-01 đến QG-10 (Toàn bộ) |

---

## 3. Điều phối Đa Agent (Multi-Agent Routing)
Khi nhiệm vụ có quy mô lớn đòi hỏi chạy song song:
1. `dex-multi-agent-orchestration` được kích hoạt để chia nhỏ các vùng mã nguồn độc lập.
2. Mỗi Agent con áp dụng `dex-task-delegation` và `dex-agent-engineering`.
3. Agent điều phối trung tâm giữ vai trò tổng hợp, yêu cầu `dex-code-review` chéo trước khi hợp nhất vào nhánh chính.
