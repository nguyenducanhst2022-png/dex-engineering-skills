---
name: dex-dependency-management
description: Deterministic dependency management, lockfile synchronization, runtime environment isolation, vulnerability scanning, and package bloat auditing. Prevents dependency drift, phantom dependencies, and supply-chain attacks. Use when adding packages, upgrading dependencies, or resolving lockfile conflicts.
---

# DEX Dependency Management

## 1. Purpose & Scope
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

## 3. When NOT to Use
- Khi chức năng có thể dễ dàng tự viết bằng 5-10 dòng code chuẩn của ngôn ngữ (Vanilla JS / Standard Library) mà không cần kéo thêm một thư viện nặng.
- Cài đặt các gói công cụ toàn cục (`npm install -g`) trên máy người dùng mà không có sự cho phép.

## 4. Prerequisites & Input Context
- File mô tả dự án (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`).
- File khóa phiên bản (Lockfile tương ứng).
- Báo cáo lỗ hổng từ các công cụ kiểm toán (`npm audit`, `pip-audit`, `cargo audit`).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
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

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-dependency-management
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-03 (Lockfile Synced)**: File lockfile khớp 100% với manifest, không có cảnh báo lệch phiên bản.
- **QG-04 (Clean Install & Build)**: Dự án cài đặt sạch và build thành công không lỗi.
- **QG-07 (Zero High/Critical Vulnerabilities)**: Lệnh audit không phát hiện lỗ hổng mức độ cao hoặc nghiêm trọng.

## 10. Security & Safety Boundaries
- **Cấm Xóa Lockfile Bừa Bãi**: Cấm hành vi xóa `package-lock.json` rồi chạy lại `npm install` một cách vô tội vạ khi gặp lỗi xung đột; phải điều tra và giải quyết từng xung đột cụ thể.
- **Chống Tấn Công Chuỗi Cung Ứng (Typosquatting)**: Kiểm tra kỹ tên gói package trước khi cài (tránh nhầm lẫn tên gần giống do tin tặc mạo danh).
- **Không Cài Đặt Thư Viện Chết (Abandonware)**: Tránh xa các thư viện không còn được bảo trì hoặc lần cập nhật cuối cùng đã cách đây hơn 2 năm.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. File manifest và lockfile được đồng bộ nhất quán.
2. Báo cáo kiểm toán bảo mật sạch sẽ (0 vulnerabilities).
3. Kích thước bundle tối ưu, không có thư viện thừa.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-dependency-management** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
