---
name: dex-dependency-management
description: Deterministic dependency management, lockfile synchronization, runtime environment isolation, vulnerability scanning, and package bloat auditing. Prevents dependency drift, phantom dependencies, and supply-chain attacks. Use when adding packages, upgrading dependencies, or resolving lockfile conflicts.
---

# DEX Dependency Management

## 1. Purpose
Quản lý các thư viện phụ thuộc (Dependencies) và môi trường thực thi (Runtime Environment) một cách chặt chẽ, có thể tái lập 100% trên mọi máy tính (Reproducible Builds), ngăn chặn việc cài đặt thư viện bừa bãi gây phình to dự án (Package Bloat) hoặc rủi ro tấn công chuỗi cung ứng (Supply Chain Attacks).

Quy trình quản lý dependency chuẩn:
`Kiểm tra môi trường → Kiểm tra dependencies → Đồng bộ phiên bản → Cài đặt tái lập → Quét lỗ hổng → Tối ưu kích thước → Kiểm thử → Lưu Git`

Nguyên tắc cốt lõi: **Không thêm hoặc nâng cấp thư viện nếu không thực sự cần thiết. Tất cả các môi trường (Dev, CI, Staging, Production) phải chạy chính xác cùng một phiên bản thư viện và runtime.**
Ghi nhớ sống còn: **Thư viện thêm vào = Trách nhiệm bảo trì tăng lên. Ít dependency hơn = Ít lỗ hổng hơn + Build nhanh hơn + Dễ nâng cấp hơn.**

## 2. When to Use
- Khi cần cài đặt thêm một thư viện (package) mới vào dự án.
- Khi cập nhật phiên bản dependencies (Security patch / Minor upgrade).
- Khi gặp xung đột lockfile (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`).
- Khi chuẩn hóa môi trường runtime thông qua `.nvmrc`, `.python-version` hoặc Dockerfile.

## 3. When Not to Use
- Khi chức năng có thể dễ dàng tự viết bằng 5-10 dòng code chuẩn của ngôn ngữ (Vanilla JS / Standard Library) mà không cần kéo thêm một thư viện nặng.
- Cài đặt các gói công cụ toàn cục (`npm install -g`) trên máy người dùng mà không có sự cho phép.

## 4. Inputs
- File mô tả dự án (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`).
- File khóa phiên bản (Lockfile tương ứng).
- Báo cáo lỗ hổng từ các công cụ kiểm toán (`npm audit`, `pip-audit`, `cargo audit`).

## 5. Workflow

### Bước 1: Thẩm Định Nhu Cầu Cài Đặt (Dependency Evaluation)
- Trước khi cài bất kỳ gói nào, tự hỏi:
  - *Chức năng này thư viện chuẩn (Standard Library) của ngôn ngữ đã có sẵn chưa?* (Ví dụ: `fetch` đã có sẵn trong Node 18+, không cần cài `axios` hay `request`).
  - Thư viện dự kiến cài có uy tín không? (Số sao GitHub, lượng tải hàng tuần, lần cập nhật gần nhất).
  - Dung lượng bundle size của thư viện là bao nhiêu? Có hỗ trợ Tree-shaking không?

### Bước 2: Khóa Phiên Bản Chặt Chẽ (Deterministic Pinning)
- Ghim phiên bản cụ thể hoặc sử dụng toán tử an toàn:
  - Ưa chuộng phiên bản cố định hoặc caret `^` có lockfile đi kèm.
- CẤM sử dụng toán tử wildcard `*` hoặc `latest` trong file cấu hình.

### Bước 3: Cài Đặt Tái Lập Tuyệt Đối (Reproducible Installation)
- Trong môi trường CI/CD hoặc Production: LUÔN sử dụng lệnh cài đặt dựa trên lockfile:
  - Node.js: `npm ci` (thay vì `npm install`).
  - Python: `pip install --no-cache-dir -r requirements.lock` hoặc `poetry install --no-root`.
- Đảm bảo lockfile luôn được commit đồng thời cùng với file manifest.

### Bước 4: Quét Lỗ Hổng Bảo Mật (Vulnerability Scanning)
- Chạy lệnh kiểm toán bảo mật ngay sau khi cài đặt:
  ```bash
  npm audit --audit-level=moderate
  ```
- Nếu phát hiện lỗ hổng nghiêm trọng (CRITICAL/HIGH): Lập tức tìm giải pháp thay thế hoặc nâng cấp lên bản vá đã được sửa lỗi.

### Bước 5: Phân Biệt Rõ Dependency vs. DevDependency
- Phân loại chính xác:
  - `dependencies`: Chỉ chứa các thư viện thực sự cần thiết khi chạy ứng dụng trên Production (Express, Prisma, React).
  - `devDependencies`: Chứa các công cụ chỉ dùng trong lúc code và build (TypeScript, Jest, ESLint, Webpack).

### Bước 6: Kiểm Thử Toàn Diện & Lưu Git (Verification & Commit)
- Chạy build và test toàn bộ dự án để xác nhận thư viện mới không gây xung đột phiên bản hoặc làm tăng kích thước bundle vượt ngưỡng.
- Commit đồng thời cả file manifest và file lockfile trong cùng một commit.

## 6. Quality Gates
- **QG-03 (Lockfile Synced)**: File lockfile khớp 100% với manifest, không có cảnh báo lệch phiên bản.
- **QG-04 (Clean Install & Build)**: Dự án cài đặt sạch và build thành công không lỗi.
- **QG-07 (Zero High/Critical Vulnerabilities)**: Lệnh audit không phát hiện lỗ hổng mức độ cao hoặc nghiêm trọng.

## 7. Safety Rules
- **Cấm Xóa Lockfile Bừa Bãi**: Cấm hành vi xóa `package-lock.json` rồi chạy lại `npm install` một cách vô tội vạ khi gặp lỗi xung đột; phải điều tra và giải quyết từng xung đột cụ thể.
- **Chống Tấn Công Chuỗi Cung Ứng (Typosquatting)**: Kiểm tra kỹ tên gói package trước khi cài (tránh nhầm lẫn tên gần giống do tin tặc mạo danh).
- **Không Cài Đặt Thư Viện Chết (Abandonware)**: Tránh xa các thư viện không còn được bảo trì hoặc lần cập nhật cuối cùng đã cách đây hơn 2 năm.

## 8. Expected Outputs
1. File manifest và lockfile được đồng bộ nhất quán.
2. Báo cáo kiểm toán bảo mật sạch sẽ (0 vulnerabilities).
3. Kích thước bundle tối ưu, không có thư viện thừa.

## 9. Failure Handling
- Nếu việc nâng cấp dependency làm gãy build do breaking changes: Rollback lockfile ngay lập tức, đọc kỹ Migration Guide của thư viện đó trước khi thử lại trên nhánh riêng.

## 10. Completion Criteria
- Môi trường cài đặt thành công với cờ tái lập (`npm ci`).
- Dự án build và chạy test đạt 100% PASS. Không phát sinh lỗ hổng bảo mật mới.

---

## Real-world Example
Cần định dạng ngày tháng trong dự án TypeScript:
1. *Đánh giá*: Tránh cài `moment.js` (nặng 70KB, không tree-shaking).
2. *Lựa chọn*: Sử dụng hàm chuẩn `Intl.DateTimeFormat` có sẵn trong JavaScript (0KB phụ thuộc) hoặc dùng `date-fns` với import module nhỏ (2KB).
3. *Cài đặt*: `npm i date-fns` → Lockfile được cập nhật.
4. *Kiểm toán*: `npm audit` → 0 vulnerabilities found.
5. *Kiểm thử*: Chạy test định dạng ngày → PASS.
