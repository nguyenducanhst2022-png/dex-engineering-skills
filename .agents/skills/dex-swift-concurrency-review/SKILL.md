---
name: dex-swift-concurrency-review
description: Audit Swift codebases for Swift 6 structured concurrency compliance, actor isolation boundaries, @Sendable conformance, and data-race safety. Use when upgrading iOS/macOS applications to Swift 6 or diagnosing async deadlocks.
---

# dex-swift-concurrency-review

## 1. Purpose & Scope
Kiểm toán và nâng cấp mã nguồn Swift tuân thủ chuẩn đồng thời có cấu trúc (Structured Concurrency) trong Swift 6; rà soát ranh giới cách ly của Actor (`actor isolation`), kiểm tra tính tương thích của giao thức `@Sendable`, và loại bỏ hoàn toàn các nguy cơ tranh chấp dữ liệu (Data Races) tại thời điểm biên dịch.

## 2. When to Use
- Khi chuẩn bị nâng cấp dự án iOS/macOS lên Xcode 16 và bật chế độ kiểm tra nghiêm ngặt Swift 6 Concurrency (`-strict-concurrency=complete`).
- Khi ứng dụng gặp các lỗi crash ngẫu nhiên hoặc trạng thái dữ liệu không nhất quán do nhiều thread cùng đọc/ghi vào biến dùng chung.
- Khi chuyển đổi các hàm bất đồng bộ cũ sử dụng completion handlers (closure callbacks) sang cú pháp hiện đại `async`/`await`.

## 3. When NOT to Use
- Khi dự án là ứng dụng viết bằng Objective-C thuần túy không chứa mã nguồn Swift.
- Khi mã nguồn chỉ là các script tính toán đơn luồng tuần tự không có tác vụ bất đồng bộ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn Swift của dự án, cờ biên dịch `-strict-concurrency=complete` trong Build Settings, trình biên dịch Swift 5.10 hoặc Swift 6.
- **Quyền hạn truy cập:** Quyền sửa đổi cấu hình dự án Xcode và mã nguồn Swift.

## 5. Core Concepts & Taxonomy
- **Data-Race Safety by Default:** Trong Swift 6, trình biên dịch tự động phát hiện và cấm mọi hành vi chia sẻ trạng thái có thể thay đổi (mutable state) giữa các threads mà không có cơ chế đồng bộ hóa.
- **Actor Isolation:** Actor là một kiểu tham chiếu bảo vệ trạng thái nội bộ của nó chỉ cho phép một tác vụ truy cập tại một thời điểm, ngăn chặn tuyệt đối data race.
- **`@Sendable` Closures & Types:** Ràng buộc kiểu dữ liệu có thể truyền qua lại an toàn giữa các ranh giới đồng thời (ví dụ: kiểu giá trị `struct`, kiểu bất biến, hoặc kiểu được bọc bởi `actor`).

## 6. Step-by-Step Execution Workflow
1. Bật cờ kiểm tra đồng thời nghiêm ngặt trong Xcode: `SWIFT_STRICT_CONCURRENCY = complete`.
2. Chạy biên dịch để thu thập toàn bộ các cảnh báo và lỗi liên quan tới Sendable và Actor isolation.
3. Thay thế các biến toàn cục có thể thay đổi (`var`) bằng `actor` hoặc bọc trong `@MainActor` nếu biến đó phục vụ cập nhật giao diện UI.
4. Đánh dấu các struct và dữ liệu truyền qua thread là tuân thủ giao thức `Sendable`.
5. Chuyển đổi các callback closures lồng nhau sang cấu hình Task có cấu trúc (`async let`, `TaskGroup`).
6. Xác nhận dự án biên dịch thành công với 0 cảnh báo vi phạm Concurrency trên Swift 6 compiler.

## 7. Concrete Examples
### Ví dụ bảo vệ trạng thái bằng Actor và xử lý Sendable trong Swift 6:
```swift
// 1. Chuyển đổi lớp chia sẻ trạng thái thành Actor để đảm bảo an toàn luồng
public actor BankAccountManager {
    private var balance: Double = 0.0

    public init(initialBalance: Double) {
        self.balance = initialBalance
    }

    public func deposit(amount: Double) {
        balance += amount
    }

    public func getBalance() -> Double {
        return balance
    }
}

// 2. Định nghĩa DTO truyền qua các Task phải tuân thủ Sendable
public struct TransactionRecord: Sendable {
    public let id: UUID
    public let amount: Double
    public let timestamp: Date
}

// 3. Hàm xử lý bất đồng bộ sử dụng TaskGroup có cấu trúc
public func processTransactions(records: [TransactionRecord], manager: BankAccountManager) async {
    await withTaskGroup(of: Void.self) { group in
        for record in records {
            group.addTask {
                // An toàn tuyệt đối: Mỗi task gọi vào actor qua await
                await manager.deposit(amount: record.amount)
            }
        }
    }
}
```

## 8. Anti-Patterns & Common Traps
- **Unchecked Sendable Abuse:** Lạm dụng `@unchecked Sendable` để tắt cảnh báo của compiler mà không thực sự cài đặt lock an toàn bên trong lớp.
- **Blocking the MainActor:** Chạy các tác vụ I/O nặng hoặc xử lý file trên `@MainActor` làm đơ giao diện người dùng (Jank / UI Freezes).
- **Unstructured Task Detachment:** Sử dụng `Task.detached` bừa bãi làm mất quyền kế thừa ưu tiên (Priority) và mất cơ chế hủy bỏ tác vụ (Cancellation propagation).

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Dự án biên dịch thành công với cờ `SWIFT_STRICT_CONCURRENCY=complete` với 0 warnings.
- **QG-05**: Không sử dụng `@unchecked Sendable` ngoại trừ các trường hợp bọc thư viện C legacy đã được review an toàn.
- **QG-10**: 100% các tác vụ cập nhật UI đều được thực thi trên `@MainActor`.

## 10. Security & Safety Boundaries
- Ngăn chặn việc rò rỉ phiên đăng nhập hoặc dữ liệu nhạy cảm giữa các luồng xử lý nền.
- Đảm bảo cơ chế hủy bỏ tác vụ (`Task.isCancelled`) được kiểm tra định kỳ trong các vòng lặp dài để giải phóng tài nguyên CPU.

## 11. Platform Adapters
- **Toolchain**: Apple Swift Compiler (`swiftc`), Xcode Build System (`xcodebuild`).
- **Frameworks**: SwiftUI, Combine, Swift Async Algorithms.

## 12. Deliverables & Output Artifacts
- Mã nguồn Swift đã được tái cấu trúc tuân thủ chuẩn Swift 6 Concurrency.
- Cấu hình Build Settings cập nhật `SWIFT_STRICT_CONCURRENCY = complete`.
- Báo cáo kiểm toán 0 Data Races từ công cụ Thread Sanitizer (TSan).

## 13. Related & Complementary Skills
dex-ios-app-architecture, dex-concurrency-state, dex-mobile-performance-profiling

## 14. Realistic Usage Example
```powershell
# Chạy kiểm tra biên dịch Swift Concurrency nghiêm ngặt qua dòng lệnh
xcodebuild clean build -scheme AppScheme -destination "generic/platform=iOS" OTHER_SWIFT_FLAGS="-strict-concurrency=complete"
```
