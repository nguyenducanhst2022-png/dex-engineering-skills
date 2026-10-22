---
name: dex-managed-assembly-inspection
description: Inspect compiled .NET Common Intermediate Language (CIL/MSIL) and Java/JVM bytecode metadata, type definitions, method signatures, embedded resources, and compiler attributes using ILDasm / javap. Use when auditing managed enterprise plugins, third-party NuGet/Maven dependencies, or cross-platform framework runtimes. (Strictly authorized/defensive).
---

# dex-managed-assembly-inspection

## 1. Purpose & Scope
Kiểm toán và phân tích cấu trúc siêu dữ liệu của các tệp mã nguồn trung gian được quản lý: Common Intermediate Language (CIL/MSIL trong .NET) và Java Bytecode (JVM); trích xuất bảng kiểu dữ liệu, chữ ký phương thức, tài nguyên nhúng và các thuộc tính biên dịch bằng các tiện ích chuẩn như `ildasm` và `javap`; phục vụ việc kiểm toán an toàn cho các plugin doanh nghiệp và gói phụ thuộc bên thứ ba.

## 2. When to Use
- Khi kiểm toán một gói thư viện NuGet (.dll) hoặc Maven (.jar) từ nguồn mở trước khi tích hợp vào dự án tài chính.
- Khi cần kiểm tra xem thư viện đã biên dịch có chứa mã độc kích hoạt cửa sau (Backdoor) hoặc các lệnh nạp mã động hay không.
- Khi xác minh tính toàn vẹn của các ứng dụng đa nền tảng viết bằng .NET MAUI hoặc Spring Boot.

## 3. When NOT to Use
- Khi làm việc với các ứng dụng nhị phân thuần túy viết bằng C/C++ hoặc Rust (không dùng máy ảo).
- Khi cố tình phá hoại các cơ chế bảo vệ phần mềm quản lý bản quyền.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp `.dll` (.NET Assembly) hoặc `.class`/`.jar` (Java), công cụ dòng lệnh `javap` (thuộc JDK) hoặc `ildasm` (thuộc .NET SDK).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Managed Metadata Tables:** Bảng lưu trữ cấu trúc TypeDef, MethodDef, ParamDef và AssemblyRef trong header tệp.
- **Intermediate Language Operations:** Các lệnh bytecode hướng ngăn xếp (như `ldarg.0`, `callvirt`, `invokevirtual`).
- **Embedded Resources Audit:** Rà soát các tài nguyên tệp được nhúng ẩn bên trong assembly (hình ảnh, cấu hình XML, payload mã hóa).

## 6. Step-by-Step Execution Workflow
1. Trích xuất thông tin manifest và siêu dữ liệu phiên bản của assembly bằng `ildasm /metadata` hoặc `javap -verbose`.
2. Liệt kê tất cả các lớp công khai và phương thức kèm chữ ký tham số.
3. Tìm kiếm các lệnh nguy hiểm như `Assembly.Load(byte[])` trong .NET hoặc `ClassLoader.defineClass` trong Java.
4. Trích xuất và kiểm tra tính an toàn của toàn bộ các tài nguyên nhúng (Embedded Resources).
5. Lập biên bản đánh giá an toàn mã bytecode `BYTECODE_SECURITY_AUDIT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Inspecting Java Class Bytecode via javap
javap -c -p -constants com.enterprise.auth.TokenValidator.class

# Inspecting .NET Assembly IL via ildasm CLI (or ilverify)
ildasm /text /item:EnterprisePlugin.Security::VerifyToken Plugin.dll

# Verifying managed assembly type safety
ilverify Plugin.dll
```

## 8. Anti-Patterns & Common Traps
- Nhúng các plugin bên thứ ba vào ứng dụng mà không kiểm tra xem chúng có gọi các API hệ thống nguy hiểm (`System.Diagnostics.Process.Start`) hay không.
- Lưu trữ chuỗi kết nối cơ sở dữ liệu hoặc khóa API nhạy cảm bên trong chuỗi hằng số (String Constants) của mã bytecode.
- Bỏ qua việc kiểm tra tính tương thích phiên bản khung làm việc (.NET Framework vs .NET Core/8).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Không phát hiện bất kỳ lệnh nạp mã động không kiểm soát nào trong toàn bộ bytecode của thư viện.
- QG-02: Danh sách các phụ thuộc bên ngoài (Assembly References) được lập danh mục đầy đủ và đối chiếu với SBOM.
- QG-03: Vượt qua công cụ xác thực an toàn kiểu dữ liệu `ilverify` với 0 lỗi vi phạm.

## 10. Security & Safety Boundaries
- Phát hiện và ngăn chặn các cuộc tấn công chuỗi cung ứng thông qua việc chèn mã độc vào các gói phụ thuộc mã nguồn mở phổ biến.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm toán mã bytecode `BYTECODE_SECURITY_AUDIT.md`.
1. Danh mục phụ thuộc và tài nguyên nhúng của assembly.

## 13. Related & Complementary Skills
- [`dex-dotnet-application-engineering`](.agents/skills/dex-dotnet-application-engineering/SKILL.md)
- [`dex-jvm-performance-diagnostics`](.agents/skills/dex-jvm-performance-diagnostics/SKILL.md)
- [`dex-supply-chain-security`](.agents/skills/dex-supply-chain-security/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Doanh nghiệp chuẩn bị tích hợp một plugin xử lý PDF dạng .NET DLL từ nhà cung cấp ngoài. Kỹ sư kích hoạt `dex-managed-assembly-inspection`, quét mã CIL bằng `ildasm`, phát hiện plugin có một phương thức ẩn gửi thông tin cấu hình máy chủ về một IP lạ ở nước ngoài, kịp thời ngăn chặn rủi ro rò rỉ dữ liệu doanh nghiệp.
