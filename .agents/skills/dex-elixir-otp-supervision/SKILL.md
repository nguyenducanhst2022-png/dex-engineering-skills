---
name: dex-elixir-otp-supervision
description: Architect resilient, fault-tolerant Elixir/Erlang OTP actor systems with supervision trees, dynamic process registries, and state recovery. Use when designing highly available messaging servers or real-time distributed backends.
---

# dex-elixir-otp-supervision

## 1. Purpose & Scope
Thiết kế và cài đặt hệ thống diễn viên (Actor System) có khả năng tự phục hồi lỗi vượt trội với Elixir/Erlang OTP; xây dựng cây giám sát tiến trình (Supervision Trees), quản lý đăng ký tiến trình động (Dynamic Process Registry), và ứng dụng triết lý 'Let It Crash' để bảo đảm tính sẵn sàng 99.999%.

## 2. When to Use
- Khi phát triển hệ thống nhắn tin thời gian thực, máy chủ kết nối IoT, hoặc nền tảng viễn thông phục vụ hàng triệu kết nối đồng thời.
- Khi cần khả năng cô lập lỗi tuyệt đối: một tiến trình con bị lỗi không bao giờ làm sập các tiến trình khác hoặc toàn bộ hệ thống.
- Khi xây dựng các tiến trình duy trì trạng thái phân tán (Stateful Workers) có khả năng tự phục hồi lại trạng thái sau khi khởi động lại.

## 3. When NOT to Use
- Khi hệ thống chỉ là các tác vụ tính toán nặng về CPU hoặc xử lý ma trận số học (nên sử dụng Rust hoặc C++).
- Khi ứng dụng chỉ là các script CRUD đơn giản không có nhu cầu về tính đồng thời cao.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bản đồ tiến trình hệ thống, chiến lược khởi động lại (Restart Strategies: `one_for_one`, `one_for_all`, `rest_for_one`), Elixir/Erlang runtime (BEAM VM).
- **Quyền hạn truy cập:** Quyền chạy `mix` toolchain và truy cập BEAM console.

## 5. Core Concepts & Taxonomy
- **Actor Model on BEAM:** Mỗi tiến trình trong Elixir là một actor độc lập hoàn toàn, sở hữu vùng nhớ riêng biệt (không chia sẻ RAM) và chỉ giao tiếp qua truyền thông điệp bất đồng bộ.
- **Let It Crash Philosophy:** Thay vì cố gắng viết hàng ngàn dòng code bắt mọi ngoại lệ phòng thủ, hãy để tiến trình bị lỗi tự sập ngay lập tức và để Supervisor phục hồi nó về trạng thái sạch ban đầu.
- **Supervision Tree:** Cấu trúc cây phân cấp trong đó các tiến trình Supervisor giám sát các tiến trình Worker; nếu Worker chết, Supervisor sẽ tự động khởi động lại theo quy tắc đã định trước.

## 6. Step-by-Step Execution Workflow
1. Thiết kế các thành phần nghiệp vụ dưới dạng `GenServer` để quản lý trạng thái và tiếp nhận thông điệp (`handle_call`, `handle_cast`, `handle_info`).
2. Xây dựng cây giám sát `Supervisor`: lựa chọn chiến lược khởi động lại phù hợp cho từng nhánh tiến trình.
3. Sử dụng `DynamicSupervisor` và `Registry` cho các tiến trình có vòng đời động (ví dụ: mỗi người dùng kết nối WebSocket có một tiến trình riêng).
4. Thiết lập cơ chế lưu trữ snapshot trạng thái ra ETS (Erlang Term Storage) hoặc cơ sở dữ liệu để Worker có thể nạp lại trạng thái ngay sau khi được khởi động lại.
5. Cấu hình giới hạn tần suất sập (`max_restarts` và `max_seconds`) để ngăn chặn vòng lặp sập vô tận (CrashLoop) làm quá tải hệ thống.
6. Kiểm thử khả năng chịu lỗi bằng cách gửi tín hiệu `Process.exit(pid, :kill)` ngẫu nhiên và xác nhận hệ thống tự phục hồi trong mili-giây.

## 7. Concrete Examples
### Ví dụ cây giám sát Supervisor và Worker GenServer trong Elixir:
```elixir
defmodule MyApp.WorkerSupervisor do
  use Supervisor

  def start_link(init_arg) do
    Supervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    children = [
      # Quản lý đăng ký định danh tiến trình theo tên
      {Registry, keys: :unique, name: MyApp.ProcessRegistry},
      # DynamicSupervisor quản lý các phiên làm việc của người dùng
      {DynamicSupervisor, name: MyApp.SessionDynamicSupervisor, strategy: :one_for_one},
      # Worker quản lý cache dùng chung, tự khởi động lại nếu sập
      {MyApp.CacheWorker, []}
    ]

    # Chiến lược one_for_one: Nếu một tiến trình con chết, chỉ khởi động lại tiến trình đó
    Supervisor.init(children, strategy: :one_for_one, max_restarts: 5, max_seconds: 10)
  end
end
```

## 8. Anti-Patterns & Common Traps
- **Defensive Try-Catch Everywhere:** Bọc toàn bộ code Elixir trong các khối `try/rescue` làm mất đi lợi ích của cơ chế Supervisor và che giấu các lỗi nghiêm trọng.
- **Bottleneck GenServer:** Sử dụng một GenServer đơn lẻ để phục vụ toàn bộ các request của hệ thống, biến GenServer đó thành nút thắt cổ chai về hiệu năng.
- **State Loss on Crash:** Không lưu vết snapshot trạng thái quan trọng ra ngoài tiến trình, khiến mỗi lần Worker sập là khách hàng bị mất toàn bộ dữ liệu phiên làm việc.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Hệ thống tự động phục hồi Worker bị `kill` đột ngột và trở lại trạng thái sẵn sàng trong dưới 10ms.
- **QG-09**: Cây giám sát không bị sập dây chuyền (Cascade Failure) khi một worker con gặp lỗi nghiêm trọng.
- **QG-10**: Toàn bộ các cảnh báo sập tiến trình đều được ghi nhận đầy đủ vào hệ thống giám sát tập trung.

## 10. Security & Safety Boundaries
- Ngăn chặn việc gửi thông điệp tràn ngập (Mailbox Flooding) làm cạn kiệt bộ nhớ RAM của một tiến trình GenServer.
- Kiểm soát phân quyền các tiến trình có quyền giao tiếp và gửi thông điệp cho nhau trong cluster.

## 11. Platform Adapters
- **Runtime**: Erlang/OTP BEAM VM, Elixir Mix.
- **Frameworks**: Phoenix Framework (Channels/LiveView), Broadway, Oban.

## 12. Deliverables & Output Artifacts
- Cấu hình cây giám sát Supervision Tree hoàn chỉnh.
- Mã nguồn các GenServers và DynamicSupervisors.
- Kịch bản kiểm thử tiêm lỗi tự động chứng minh khả năng tự phục hồi của hệ thống.

## 13. Related & Complementary Skills
dex-distributed-consistency, dex-concurrency-state, dex-reliability-engineering

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử tự phục hồi lỗi của cây giám sát Elixir OTP
mix test test/supervision/fault_tolerance_test.exs
```
