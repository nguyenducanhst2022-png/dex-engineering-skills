---
name: dex-configuration-schema-design
description: Design strictly typed, validated application configuration schemas with layered precedence, environment variable overrides, and secret leakage prevention. Use when bootstrapping applications or standardizing enterprise config management.
---

# dex-configuration-schema-design

## 1. Purpose & Scope
Thiết kế và chuẩn hóa schema cấu hình ứng dụng được định kiểu nghiêm ngặt (Strictly Typed Configuration Schema); quản lý độ ưu tiên đa tầng (Defaults < File < Env Vars < CLI flags), tự động xác thực tính hợp lệ lúc khởi động (fail-fast), và tuyệt đối ngăn ngừa rò rỉ secrets.

## 2. When to Use
- Khi khởi tạo dự án mới cần hệ thống cấu hình vững chắc, tránh lỗi runtime do thiếu biến môi trường.
- Khi chuẩn hóa cấu hình cho ứng dụng triển khai trên nhiều môi trường khác nhau (Local, Staging, Production, Multi-Cloud).
- Khi bảo vệ các thông tin bí mật không bị in ra log hoặc serialize nhầm vào response.

## 3. When NOT to Use
- Khi chỉ cần lưu trữ các cờ bật/tắt tính năng động theo thời gian thực (nên sử dụng feature flag system như LaunchDarkly/Unleash).
- Khi lưu trữ dữ liệu nghiệp vụ có tính thay đổi liên tục của người dùng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách các tham số cấu hình, kiểu dữ liệu, giá trị mặc định an toàn, và nguồn cung cấp (Environment Variables, YAML/JSON file, Vault).
- **Quyền hạn truy cập:** Quyền định nghĩa tệp cấu hình và biến môi trường của ứng dụng.

## 5. Core Concepts & Taxonomy
- **Fail-Fast Startup Validation:** Ứng dụng từ chối khởi động ngay lập tức nếu thiếu bất kỳ biến cấu hình bắt buộc nào hoặc sai định dạng.
- **Layered Configuration Precedence:** Thứ tự ưu tiên ghi đè rõ ràng: CLI arguments > Environment Variables > `.env` file > `config.yaml` > Hardcoded Safe Defaults.
- **Secret Masking & Redaction:** Tự động che giấu các trường nhạy cảm (`password`, `secret`, `api_key`) trong hàm `toString()` và logging formatter.

## 6. Step-by-Step Execution Workflow
1. Khai báo schema cấu hình bằng thư viện schema validation (Zod, Pydantic, Joi, hoặc JSON Schema).
2. Gán các ràng buộc kiểm tra chi tiết (độ dài, khoảng giá trị cổng mạng 1-65535, định dạng URI hợp lệ, regex).
3. Tải cấu hình theo thứ tự ưu tiên đa tầng và nạp giá trị vào schema.
4. Thực hiện xác thực schema trong hàm `main()` hoặc entrypoint trước khi khởi tạo bất kỳ kết nối mạng hoặc database nào.
5. Đánh dấu các trường nhạy cảm để loại bỏ khỏi output khi in cấu hình lúc khởi động ứng dụng.

## 7. Concrete Examples
### Ví dụ schema cấu hình nghiêm ngặt bằng Pydantic v2 trong Python:
```python
from pydantic import BaseModel, Field, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class DatabaseConfig(BaseModel):
    dsn: PostgresDsn = Field(..., description="PostgreSQL connection URI")
    max_connections: int = Field(default=20, ge=1, le=100)
    timeout_seconds: float = Field(default=5.0, ge=0.5)

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="forbid" # Từ chối khởi động nếu có biến lạ không khai báo
    )

    environment: Literal["local", "staging", "production"] = "local"
    port: int = Field(default=8080, ge=1024, le=65535)
    database: DatabaseConfig
    api_secret_key: str = Field(..., min_length=32)

    def print_safe_summary(self):
        dump = self.model_dump()
        dump["api_secret_key"] = "[REDACTED]"
        dump["database"]["dsn"] = str(self.database.dsn).split("@")[-1] # Giấu credentials
        return dump

# Khi khởi động ứng dụng:
# settings = AppSettings() -> Tự động ném lỗi nếu thiếu biến bắt buộc!
```

## 8. Anti-Patterns & Common Traps
- **Lazy Configuration Evaluation:** Đọc biến môi trường `process.env.MY_VAR` rải rác bên trong các hàm sâu, khiến lỗi chỉ xuất hiện khi khách hàng gọi vào luồng đó.
- **Permissive Defaults for Secrets:** Đặt giá trị mặc định cho secret key là chuỗi `change-me-in-prod` và quên đổi trên production.
- **Printing Unredacted Config:** In toàn bộ đối tượng cấu hình ra stdout lúc khởi động làm lộ connection string chứa mật khẩu database trong log.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Schema cấu hình có kiểu dữ liệu tường minh 100%, không sử dụng kiểu `any` hoặc chuỗi tự do.
- **QG-06**: Quá trình khởi động kiểm tra không có secret key nào bị hardcode trong mã nguồn Git.
- **QG-07**: Thời gian parse và validate cấu hình lúc khởi động dưới 100ms.

## 10. Security & Safety Boundaries
- Bắt buộc mã hóa các biến môi trường nhạy cảm khi lưu trữ trên CI/CD và quản lý thông qua Secret Managers (AWS Secrets Manager, HashiCorp Vault).
- Khóa quyền truy cập tệp `.env` chỉ cho phép người dùng sở hữu tiến trình đọc được (chmod 600).

## 11. Platform Adapters
- **Python**: Pydantic Settings.
- **Node/TypeScript**: Zod, Envalid.
- **Go**: Viper, envconfig.
- **Java**: Spring Boot ConfigurationProperties, Quarkus Config.

## 12. Deliverables & Output Artifacts
- Mã nguồn khai báo Schema cấu hình được định kiểu chặt chẽ.
- Tệp cấu hình mẫu `.env.example` với đầy đủ chú thích.
- Bộ unit test kiểm tra cơ chế fail-fast khi thiếu biến môi trường.

## 13. Related & Complementary Skills
dex-secrets-management, dex-code-organization, dex-development-workflow

## 14. Realistic Usage Example
```powershell
# Chạy kiểm thử xác minh tính hợp lệ của schema cấu hình
pytest tests/config/test_configuration_schema.py -v
```
