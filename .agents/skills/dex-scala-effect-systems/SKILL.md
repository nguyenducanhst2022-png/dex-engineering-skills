---
name: dex-scala-effect-systems
description: Architect purely functional, concurrent Scala applications using modern effect systems (ZIO, Cats Effect) with typed error channels, resource safety, and fiber supervision. Use when building high-throughput asynchronous backend systems.
---

# dex-scala-effect-systems

## 1. Purpose & Scope
Thiết kế và xây dựng các ứng dụng Scala hướng chức năng thuần túy (Purely Functional Programming) sử dụng hệ thống hiệu ứng hiện đại (Effect Systems như ZIO hoặc Cats Effect); quản lý an toàn vòng đời tài nguyên (`Scope`/`Resource`), kênh lỗi được định kiểu tường minh (Typed Error Channel), và giám sát luồng ảo (Fibers Supervision).

## 2. When to Use
- Khi xây dựng các hệ thống backend phân tán yêu cầu thông lượng cao, xử lý hàng trăm ngàn tác vụ đồng thời mà không bị nghẽn thread của hệ điều hành.
- Khi cần quản lý an toàn tuyệt đối các tài nguyên có thể rò rỉ (file handles, database connections, sockets) kể cả khi có exception hoặc bị hủy tác vụ đột ngột.
- Khi muốn mô hình hóa các lỗi nghiệp vụ một cách minh bạch trong hệ thống kiểu (Type System) thay vì ném các ngoại lệ không kiểm soát (Unchecked Exceptions).

## 3. When NOT to Use
- Khi phát triển các script đơn giản hoặc ứng dụng hướng đối tượng truyền thống không sử dụng tư duy lập trình hàm thuần túy.
- Khi đội ngũ kỹ sư chưa nắm vững các khái niệm Monad, Referential Transparency và Effect Systems.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn Scala 3, công cụ build sbt, thư viện ZIO 2.x hoặc Cats Effect 3.x.
- **Quyền hạn truy cập:** Quyền biên dịch và chạy sbt console.

## 5. Core Concepts & Taxonomy
- **Effect as a Value (ZIO[R, E, A]):** Một chương trình mô tả việc thực thi cần môi trường `R`, có thể thất bại với lỗi `E`, hoặc thành công trả về kết quả `A`; bản thân effect là một giá trị bất biến, chỉ được chạy tại `unsafeRun` ở biên của thế giới (End of the World).
- **Fibers (Green Threads):** Các luồng ảo siêu nhẹ do runtime của Effect System quản lý, tiêu tốn chỉ vài trăm bytes bộ nhớ, cho phép khởi tạo hàng triệu fibers đồng thời.
- **Resource Safety (`ZIO.scoped` / `Resource`):** Đảm bảo hàm giải phóng tài nguyên (Finalizer) luôn luôn được thực thi trong mọi tình huống (thành công, thất bại, hoặc bị gián đoạn/interrupted).

## 6. Step-by-Step Execution Workflow
1. Khai báo các mô hình dữ liệu bất biến (`case class`, `enum`) và các lỗi nghiệp vụ trong một kênh lỗi được định kiểu cụ thể.
2. Thiết kế các dịch vụ (Services) dưới dạng ZIO Layers (ZLayer) để quản lý phụ thuộc (Dependency Injection) tại thời điểm biên dịch.
3. Quản lý các kết nối database hoặc socket bằng `ZIO.acquireRelease` để bảo đảm tự động đóng tài nguyên.
4. Thực thi các tác vụ song song bằng các toán tử đồng thời có cấu trúc như `ZIO.collectAllPar` hoặc `race`.
5. Cài đặt cơ chế xử lý lỗi tường minh bằng hàm `catchAll` hoặc `foldZIO` để xử lý từng nhánh lỗi cụ thể.
6. Kiểm thử logic chức năng bằng `ZIOSpecDefault` với môi trường giả lập (TestClock, TestRandom) mà không cần chờ đợi thời gian thực tế.

## 7. Concrete Examples
### Ví dụ quản lý an toàn tài nguyên và concurrency bằng ZIO 2 trong Scala 3:
```scala
import zio.*
import java.io.IOException

// 1. Định nghĩa lỗi nghiệp vụ tường minh
enum OrderError:
  case DatabaseFailure(msg: String)
  case InsufficientFunds(amount: Double)

// 2. Tác vụ đọc ghi tài nguyên có bảo đảm giải phóng an toàn
def makeManagedConnection: ZIO[Scope, IOException, String] =
  ZIO.acquireRelease(
    ZIO.succeed("Acquired DB Connection").debug
  )(conn => ZIO.succeed(s"Released $conn").debug)

// 3. Quy trình xử lý song song với Fiber có giám sát
def processOrders(orderIds: List[String]): ZIO[Any, OrderError, List[String]] =
  ZIO.scoped {
    for
      conn <- makeManagedConnection.mapError(e => OrderError.DatabaseFailure(e.getMessage))
      // Chạy song song có kiểm soát số lượng luồng đồng thời tối đa là 4
      results <- ZIO.foreachPar(orderIds) { id =>
        ZIO.succeed(s"Order $id processed via $conn")
      }.withParallelism(4)
    yield results
  }
```

## 8. Anti-Patterns & Common Traps
- **Breaking Referential Transparency:** Gọi các hàm có side-effect (như ghi file, in màn hình) trực tiếp ngoài luồng Effect mà không bọc trong `ZIO.attempt`.
- **Catching Throwable Blindly:** Bắt bừa bãi mọi ngoại lệ làm nuốt mất tín hiệu gián đoạn tác vụ (`InterruptedException`), khiến các fibers không thể bị hủy bỏ khi timeout.
- **Blocking Threads on Global Pool:** Chạy các tác vụ I/O chặn (Blocking I/O) trên thread pool tính toán của CPU làm nghẽn toàn bộ ứng dụng.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: 100% các hàm nghiệp vụ trả về kiểu Effect (ZIO/IO) có kênh lỗi tường minh, không ném Unchecked Exceptions.
- **QG-05**: Mã nguồn biên dịch thành công trên Scala 3 compiler với cờ `-Xfatal-warnings`.
- **QG-09**: Tất cả các tài nguyên bên ngoài đều được giải phóng an toàn trong bài test giả lập gián đoạn tác vụ (Interruption Test).

## 10. Security & Safety Boundaries
- Sử dụng hệ thống kiểu mạnh của Scala để ngăn ngừa các lỗi rò rỉ dữ liệu hoặc sai lệch trạng thái tại thời điểm biên dịch.
- Không để lọt các thông tin nhạy cảm vào chuỗi thông báo lỗi nghiệp vụ trong Error Channel.

## 11. Platform Adapters
- **Frameworks**: ZIO 2.x, Cats Effect 3.x, Fs2 (Functional Streams for Scala).
- **Build**: sbt, Mill, Scala-CLI.

## 12. Deliverables & Output Artifacts
- Mã nguồn ứng dụng Scala hướng chức năng thuần túy.
- Cấu hình Dependency Injection bằng ZIO Layers.
- Bộ kiểm thử ZIO Test chứng minh tính an toàn tài nguyên khi bị ngắt luồng.

## 13. Related & Complementary Skills
dex-concurrency-state, dex-distributed-consistency, dex-jvm-performance-diagnostics

## 14. Realistic Usage Example
```powershell
# Biên dịch và chạy toàn bộ ZIO Test Suite bằng sbt
sbt test
```
