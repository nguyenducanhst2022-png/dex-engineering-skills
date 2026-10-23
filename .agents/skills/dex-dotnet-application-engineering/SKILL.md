---
name: dex-dotnet-application-engineering
description: Architect, optimize, and diagnose modern cross-platform .NET (C# / ASP.NET Core) applications leveraging dependency injection lifetimes, async/await mechanics, Span<T>, and dotnet-dump/dotnet-trace. Use when building enterprise .NET systems.
---

# dex-dotnet-application-engineering

## 1. Purpose & Scope
Thiết kế, xây dựng và tối ưu hóa ứng dụng .NET hiện đại đa nền tảng (Modern .NET 8/9, C#, ASP.NET Core); quản trị vòng đời Dependency Injection (Transient, Scoped, Singleton), làm chủ cơ chế `async/await` không gây deadlock, khai thác tối đa cấu trúc `Span<T>` / `Memory<T>` không cấp phát bộ nhớ, và điều tra sự cố hiệu năng bằng các công cụ CLI chẩn đoán (`dotnet-dump`, `dotnet-trace`, `dotnet-gcdump`).

## 2. When to Use
- Dịch vụ ASP.NET Core chạy trên Linux/Kubernetes bị treo (hang) do ThreadPool Starvation hoặc Sync-over-Async.
- Nâng cấp ứng dụng .NET Framework cũ sang .NET 8 đa nền tảng.
- Cần tối ưu hóa thông lượng API xử lý dữ liệu lớn yêu cầu Zero-allocation.

## 3. When NOT to Use
- Không sử dụng các phương thức đồng bộ chặn luồng như `.Result` hoặc `.Wait()` trên Task (gây ra Deadlock và ThreadPool Starvation).
- Không đăng ký service Scoped vào bên trong một service Singleton (Captive Dependency bug).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mã nguồn C# / Solution `.sln`.
- File cấu hình `appsettings.json` và cấu hình runtime `runtimeconfig.json`.
- Bản ghi trace hoặc dump lấy từ môi trường Linux container.
- **Điều kiện tiên quyết**:
- Đã cài đặt .NET SDK 8.0+ và bộ công cụ chẩn đoán toàn cục `dotnet-dump`, `dotnet-trace`.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Captive Dependencies: Lỗi tiêm một Scoped service (như `DbContext`) vào một Singleton service, khiến DbContext không bao giờ được giải phóng và giữ kết nối DB vĩnh viễn.
- ThreadPool Starvation: Xảy ra khi lập trình viên gọi code đồng bộ chặn luồng (`Task.Wait()`), làm cạn kiệt các luồng xử lý của ThreadPool và làm tê liệt toàn bộ API server.
- `Span<T>` & Zero-Allocation: Cho phép thao tác cắt chuỗi, đọc byte trực tiếp trên vùng nhớ contiguous mà không cần cấp phát thêm đối tượng mới trên Heap, giảm áp lực cực lớn cho .NET GC.
- **Quy tắc quyết định kỹ thuật**:
- Bật chế độ phân tích Dependency Injection lúc khởi động (`ValidateScopes = true`, `ValidateOnBuild = true`).
- 100% các thao tác I/O (Database, HTTP, Disk) bắt buộc phải sử dụng API bất đồng bộ kèm `CancellationToken`.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Lỗi gọi `httpClient.GetAsync().Result` trong controller làm cạn kiệt ThreadPool của ASP.NET Core khi có tải đồng thời lớn.

## 6. Step-by-Step Execution Workflow
1. Cấu hình kiểm tra tính hợp lệ của DI container trong `Program.cs`.
2. Rà soát codebase loại bỏ hoàn toàn các anti-pattern Sync-over-Async.
3. Áp dụng `Span<T>` và `ArrayPool<T>` cho các hàm xử lý parser chuỗi và byte buffer.
4. Thu thập dữ liệu trace khi có tải bằng `dotnet-trace collect --process-id <PID>`.
5. Đóng gói container Linux tối giản sử dụng Alpine/Chiseled images.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```csharp
// Tối ưu hóa ASP.NET Core: Zero-Allocation parsing với ReadOnlySpan<char>
public static class DateParserFast
{
    public static bool TryParseYear(ReadOnlySpan<char> input, out int year)
    {
        // Không sinh ra chuỗi tạm (string allocation) trên Heap
        if (input.Length >= 4 && int.TryParse(input.Slice(0, 4), out year))
        {
            return true;
        }
        year = 0;
        return false;
    }
}
```

### Lệnh xác minh & thực thi:
```bash
# Thu thập heap dump từ tiến trình .NET trên Linux
dotnet-dump collect -p <PID>
# Phân tích dump tìm rò rỉ bộ nhớ
dotnet-dump analyze core_dump.dmp
```

## 8. Anti-Patterns & Common Traps
- Gọi `Task.Run()` bừa bãi cho các tác vụ I/O ngắn hạn trong ASP.NET Core.
- Không truyền `CancellationToken` xuống các câu lệnh truy vấn Entity Framework Core.

## 9. Quality Gates & Acceptance Criteria
- 0 lỗi Captive Dependency được phát hiện khi khởi động ứng dụng với `ValidateScopes = true`.
- Vượt qua kiểm thử tải không phát sinh hiện tượng ThreadPool Starvation.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mã hóa dữ liệu Data Protection Keys của ASP.NET Core bằng AWS KMS hoặc Azure Key Vault khi triển khai đa instance.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Solution .NET chuẩn mực kiến trúc Clean Architecture.
- Báo cáo phân tích hiệu năng và tài liệu cấu hình chẩn đoán production.

## 13. Related & Complementary Skills
dex-software-architecture, dex-load-and-stress-testing, dex-database-engineering

## 14. Realistic Usage Example
### Tình huống thực tế:
Một dịch vụ thanh toán ASP.NET Core trên Kubernetes bị timeout hàng loạt mỗi khi traffic đạt 2,000 RPS. Chạy `dotnet-trace`, đội ngũ phát hiện một hàm tiện ích cũ sử dụng `.GetAwaiter().GetResult()` gây nghẽn ThreadPool. Sau khi chuyển hoàn toàn sang `async/await` và áp dụng `Span<char>` để parse mã giao dịch, CPU server giảm 60% và hệ thống đáp ứng 8,000 RPS dễ dàng.
