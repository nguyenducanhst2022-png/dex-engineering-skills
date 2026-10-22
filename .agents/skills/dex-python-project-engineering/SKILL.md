---
name: dex-python-project-engineering
description: Standardize production-grade Python projects using modern packaging (Poetry, Hatch, uv), strict type checking (Mypy, Pyright), linting (Ruff), and virtual environment isolation. Use to eradicate dependency hell and project fragmentation.
---

# dex-python-project-engineering

## 1. Purpose & Scope
Thiết kế, chuẩn hóa và tối ưu hóa quy trình kỹ thuật cho các dự án Python hiện đại (Production-grade Python Engineering); áp dụng công cụ quản lý gói thế hệ mới (`uv`, Poetry, Hatch), kiểm tra kiểu tĩnh nghiêm ngặt (Mypy, Pyright), linter siêu tốc (Ruff), quản lý môi trường ảo cô lập và thiết lập cấu hình `pyproject.toml` đạt chuẩn PEP.

## 2. When to Use
- Dự án Python gặp vấn đề 'dependency hell', xung đột phiên bản gói hoặc cài đặt thư viện quá chậm chạp trong CI.
- Codebase thiếu kiểm soát kiểu dữ liệu, liên tục phát sinh lỗi `AttributeError: 'NoneType' object has no attribute`.
- Các công cụ format và lint (Flake8, Black, Isort) chạy chậm và xung đột lẫn nhau.

## 3. When NOT to Use
- Không sử dụng các file `requirements.txt` không khóa phiên bản (unpinned) cho các ứng dụng production.
- Không tự tiện cài đặt thư viện trực tiếp vào môi trường Python toàn cục của hệ điều hành mà không có virtual environment.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File cấu hình dự án (`pyproject.toml`).
- Danh sách dependencies và dev-dependencies.
- Cấu hình type checker và linter.
- **Điều kiện tiên quyết**:
- Đã cài đặt công cụ quản lý gói hiện đại (`uv` hoặc `poetry`) trên máy phát triển.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- `pyproject.toml` as the Standard: Toàn bộ cấu hình công cụ (Ruff, Mypy, Pytest, Coverage) và metadata của gói được tập trung vào một file duy nhất theo chuẩn PEP 517/518/621.
- Fast Tooling with `uv` & `Ruff`: `uv` nhanh hơn pip 10-100 lần nhờ viết bằng Rust; `Ruff` thay thế hoàn toàn Black, Flake8, Isort với tốc độ xử lý hàng trăm ngàn dòng code trong chớp mắt.
- Strict Static Typing: Mypy với cờ `--strict` biến Python thành ngôn ngữ có độ tin cậy kiểu gần như các ngôn ngữ tĩnh.
- **Quy tắc quyết định kỹ thuật**:
- Bắt buộc cam kết file khóa phiên bản (`uv.lock` hoặc `poetry.lock`) vào Git để bảo đảm tính tái lập 100% của môi trường.
- Mọi hàm mới viết phải có đầy đủ Type Hints cho các tham số và giá trị trả về.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Một thư viện phụ thuộc cập nhật phiên bản minor nhưng làm thay đổi API ngầm, khiến ứng dụng sập trên production do dùng `requirements.txt` không khóa phiên bản chính xác.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo dự án chuẩn hóa bằng `uv init` và định cấu hình `pyproject.toml`.
2. Thiết lập cấu hình Ruff để vừa format code vừa kiểm tra quy chuẩn an ninh.
3. Cấu hình Mypy ở chế độ nghiêm ngặt (`disallow_untyped_defs = true`).
4. Tích hợp pre-commit hooks để tự động chạy Ruff và Mypy trước khi cho phép commit.
5. Tối ưu hóa Dockerfile đa tầng sử dụng `uv` để tạo container image siêu nhẹ và build trong vài giây.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```toml
# pyproject.toml chuẩn mực cho dự án Python hiện đại
[project]
name = "enterprise-ai-service"
version = "5.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110.0",
    "pydantic>=2.6.0",
]

[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "F", "I", "B", "UP", "S"] # Chặn cả lỗi cú pháp và lỗ hổng bảo mật

[tool.mypy]
python_version = "3.11"
strict = true
disallow_untyped_defs = true
ignore_missing_imports = true
```

### Lệnh xác minh & thực thi:
```bash
# Chạy linter và format siêu tốc bằng Ruff
uv run ruff check . --fix
# Kiểm tra kiểu dữ liệu tĩnh nghiêm ngặt bằng Mypy
uv run mypy src/
```

## 8. Anti-Patterns & Common Traps
- Sử dụng `from module import *` làm ô nhiễm namespace và vô hiệu hóa công cụ kiểm tra kiểu tĩnh.
- Bắt ngoại lệ chung chung `except Exception: pass` làm nuốt chửng các lỗi nghiêm trọng.

## 9. Quality Gates & Acceptance Criteria
- 100% mã nguồn vượt qua kiểm tra `mypy --strict` và `ruff check` không có lỗi.
- Quá trình cài đặt dependencies trong CI phải hoàn thành dưới 15 giây nhờ `uv`.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Kiểm tra lỗ hổng bảo mật trong dependencies bằng `uv run pip-audit` trước khi release.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- File `pyproject.toml` và `uv.lock` chuẩn hóa.
- Cấu hình Pre-commit hooks và Dockerfile tối ưu hóa tốc độ build.

## 13. Related & Complementary Skills
dex-unit-testing, dex-compatibility-matrix-testing, dex-ci-pipeline-optimization

## 14. Realistic Usage Example
### Tình huống thực tế:
Một đội ngũ Data Science gặp rắc rối vì code Python chạy trên máy của từng người cho kết quả khác nhau và build CI mất 8 phút. Chuyên gia chuyển đổi sang sử dụng `uv` và `pyproject.toml` chuẩn hóa kèm Ruff và Mypy. Thời gian build CI giảm từ 8 phút xuống còn 18 giây, và 100% các xung đột thư viện đã được loại bỏ hoàn toàn.
