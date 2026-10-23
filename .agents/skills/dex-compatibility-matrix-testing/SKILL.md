---
name: dex-compatibility-matrix-testing
description: Define, automate, and execute matrix-based compatibility testing across operating systems, runtime versions, browsers, and dependency sets. Use when publishing open-source libraries, CLI tools, or multi-platform applications.
---

# dex-compatibility-matrix-testing

## 1. Purpose & Scope
Xác định ma trận tương thích, tự động hóa và thực thi kiểm thử trên nhiều hệ điều hành (Ubuntu, macOS, Windows 11), nhiều phiên bản runtime (Node 18/20/22, Python 3.9/3.11/3.13) và các trình duyệt mục tiêu nhằm bảo đảm sản phẩm hoạt động ổn định trên mọi môi trường được hỗ trợ.

## 2. When to Use
- Phát hành thư viện mã nguồn mở hoặc SDK cho bên thứ ba.
- Ứng dụng desktop hoặc CLI tool hỗ trợ cả Windows, macOS và Linux.
- Chuẩn bị deprecate hoặc nâng cấp phiên bản runtime tối thiểu trong chính sách hỗ trợ.

## 3. When NOT to Use
- Không cần ma trận rộng cho ứng dụng web nội bộ chỉ chạy trên một phiên bản Docker container cố định.
- Không chạy toàn bộ ma trận cho mọi commit nhỏ (dùng pull request filter).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách OS, architectures (x86_64, arm64) và runtime versions cần hỗ trợ.
- File cấu hình CI (GitHub Actions matrix).
- Bộ test suite tích hợp của dự án.
- **Điều kiện tiên quyết**:
- Test suite có thể chạy không lỗi trên ít nhất một môi trường cơ sở.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Combinatorial Matrix: Số lượng trường hợp kiểm thử là tích của các biến (OS x Runtime x Architecture). Cần lược bớt các tổ hợp ít rủi ro để tối ưu chi phí CI.
- Fast-Fail Matrix: Hủy toàn bộ các job còn lại nếu một job trong ma trận bị lỗi nghiêm trọng để tiết kiệm tài nguyên.
- **Quy tắc quyết định kỹ thuật**:
- Trên commit nhánh feature: chỉ chạy trên 1 OS chính (Ubuntu) và 1 runtime mới nhất.
- Trên PR vào main hoặc Release tag: bắt buộc chạy 100% ma trận tương thích.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Mã nguồn sử dụng đường dẫn file phân cách bằng dấu gạch chéo `/` cứng, chạy tốt trên Linux nhưng fail hoàn toàn trên Windows (dùng `path.join` hoặc `pathlib.Path`).

## 6. Step-by-Step Execution Workflow
1. Khảo sát tỉ lệ người dùng thực tế trên các nền tảng.
2. Định nghĩa file cấu hình matrix trong GitHub Actions workflow.
3. Xử lý các điểm khác biệt về OS (đường dẫn file, line endings CRLF vs LF, biến môi trường).
4. Chạy ma trận và theo dõi các lỗi đặc thù theo từng nền tảng.
5. Bổ sung các bản vá tương thích và cập nhật tài liệu chính thức.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node-version: [18.x, 20.x, 22.x]
    exclude:
      - os: macos-latest
        node-version: 18.x
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm thử đa phiên bản cục bộ bằng tox cho Python:
tox -e py310,py311,py312
```

## 8. Anti-Patterns & Common Traps
- Giả định mọi môi trường đều có sẵn Bash shell hoặc các lệnh GNU coreutils.
- Chạy ma trận quá cồng kềnh ngốn hết hạn mức CI phút hàng tháng.

## 9. Quality Gates & Acceptance Criteria
- 100% jobs trong ma trận quy định phải PASS trước khi tạo bản release chính thức.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Đảm bảo các runners độc lập không chia sẻ file tạm có chứa secrets.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- File workflow ma trận CI (`.github/workflows/compat.yml`).
- Bảng ma trận hỗ trợ chính thức trong tài liệu README.

## 13. Related & Complementary Skills
dex-cicd-automation, dex-cli-engineering, dex-python-project-engineering

## 14. Realistic Usage Example
### Tình huống thực tế:
Một CLI tool bằng Node.js hoạt động tốt trên Mac của dev nhưng người dùng Windows báo lỗi không mở được file config. Sau khi đưa Windows runner vào ma trận test, nhóm phát hiện lỗi đọc ký tự xuống dòng CRLF và giải quyết triệt để.
