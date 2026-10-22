---
name: dex-ios-app-architecture
description: Architect resilient iOS applications using SwiftUI, Swift Concurrency (async/await, Actor), NavigationStack, Observation framework, SwiftData/CoreData, and modular SPM. Use when designing, building, or refactoring modern iOS apps.
---

# dex-ios-app-architecture

## 1. Purpose & Scope
Thiết kế và hiện thực hóa kiến trúc ứng dụng iOS hiện đại theo chuẩn Apple Platform (Modern iOS Architecture); áp dụng SwiftUI kết hợp framework `@Observable`, quản lý xử lý bất đồng bộ và chống tương tranh (Data Race Safety) với Swift Concurrency (`async`/`await`, `actor`, `TaskGroup`), điều hướng phân cấp bằng `NavigationStack`, quản lý dữ liệu bền vững với SwiftData / Core Data và module hóa dự án thông qua Swift Package Manager (SPM).

## 2. When to Use
- Khi khởi tạo dự án iOS mới hoặc tái cấu trúc từ UIKit/Storyboards sang SwiftUI thuần túy.
- Khi gặp các lỗi Data Race (Thread Sanitizer cảnh báo) do gọi cập nhật giao diện ngoài Main Thread.
- Khi cấu trúc code monolith trong Xcode project khiến thời gian compile kéo dài.

## 3. When NOT to Use
- Xây dựng ứng dụng Android (dùng `dex-android-app-architecture`).
- Xây dựng ứng dụng web đa nền tảng (dùng `dex-ui-component-contracts`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Yêu cầu thiết kế theo Apple Human Interface Guidelines (HIG).
- Phiên bản iOS tối thiểu (`iOS 16+` hoặc `iOS 17+` cho SwiftData / Observation).
- Các quyền truy cập hệ thống cần khai báo trong `Info.plist`.
- **Điều kiện tiên quyết**:
- Xcode 15+ và Swift 5.9+ cài đặt trên macOS.
- Bật cờ kiểm tra tương tranh nghiêm ngặt: `Strict Concurrency Checking = Complete`.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Data Race Free Concurrency (Actors)**: Sử dụng `@MainActor` cho các class quản lý view/model giao diện và `actor` riêng biệt cho các tác vụ tính toán nền để đảm bảo an toàn luồng dữ liệu.
- **Swift Observation Framework**: Sử dụng macro `@Observable` (iOS 17+) thay thế cho `ObservableObject` và `@Published`, giúp SwiftUI chỉ re-render các View thực sự truy cập thuộc tính bị thay đổi.
- **Modular Swift Packages**: Chia dự án thành các package SPM nội bộ (`AppCore`, `FeatureAuth`, `FeatureCheckout`, `DesignSystem`) để tận dụng tính năng build song song.
- **Quy tắc quyết định kỹ thuật**:
- **Mọi Thay Đổi UI Phải Chạy Trên `@MainActor`**: ViewModel và State chứa thuộc tính hiển thị bắt buộc được đánh dấu `@MainActor`.
- **Cấm Force Unwrapping (`!`) Trong Code Sản Xuất**: Không dùng `!` khi giải nén optional hoặc ép kiểu; luôn dùng `guard let`, `if let` hoặc `nil coalescing`.
- **Tách Biệt View Khỏi Logic Nghiệp Vụ**: SwiftUI View chỉ đảm nhiệm render giao diện; logic gọi mạng và biến đổi dữ liệu phải nằm trong Model/Repository.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Ứng dụng crash ngẫu nhiên khi nhận response từ Network**: Do cập nhật state từ background thread -> Khắc phục: Gắn nhãn `@MainActor` cho ViewModel hoặc hàm xử lý kết quả.
- **SwiftUI View bị re-render liên tục gây giật lag (Dropped Frames)**: Do khởi tạo đối tượng nặng bên trong `body` của View -> Khắc phục: Đưa đối tượng vào `@State` hoặc ViewModel.

## 6. Step-by-Step Execution Workflow
1. Thiết lập cấu trúc workspace Xcode với các local SPM modules phân quyền rõ ràng.
2. Định nghĩa Model Layer và Schema lưu trữ cục bộ với SwiftData (`@Model`).
3. Xây dựng Network Service sử dụng `URLSession` và `async`/`await` với generic decoding.
4. Tạo Presentation Model sử dụng macro `@Observable` và gắn cờ `@MainActor`.
5. Xây dựng giao diện SwiftUI với `NavigationStack(path: $navPath)` hỗ trợ deep linking.
6. Kích hoạt Thread Sanitizer trong Xcode Scheme để phát hiện lỗi data race tiềm ẩn.
7. Viết XCTest unit tests và UI Tests xác nhận tính đúng đắn.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```swift
import SwiftUI
import Observation

// Model định nghĩa với Observation macro (iOS 17+)
@Observable
@MainActor
final class OrderViewModel {
    var orderState: ViewState = .idle
    private let orderRepository: OrderRepositoryProtocol

    init(orderRepository: OrderRepositoryProtocol) {
        self.orderRepository = orderRepository
    }

    func submitOrder(id: String) async {
        orderState = .loading
        do {
            let confirmedOrder = try await orderRepository.placeOrder(id: id)
            orderState = .success(confirmedOrder)
        } catch {
            orderState = .error(error.localizedDescription)
        }
    }

    enum ViewState {
        case idle, loading
        case success(Order)
        case error(String)
    }
}
```

### Lệnh xác minh & thực thi:
- Biên dịch và kiểm tra warnings: `xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15' build`
- Chạy unit tests với Thread Sanitizer: `xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15' -enableThreadSanitizer YES`
- Kiểm tra cú pháp bằng SwiftLint: `swiftlint lint`

## 8. Anti-Patterns & Common Traps
- **Sử dụng `DispatchQueue.main.async` lẫn lộn trong Swift Concurrency**: Nên đồng bộ sử dụng `MainActor.run` hoặc cấu trúc `async`/`await`.
- **Đặt toàn bộ state trong một ViewModel khổng lồ (God ViewModel)**: Làm mất đi tính module hóa và gây lag render.
- **Hardcode chuỗi UI Text không qua LocalizedStringKey**: Gây khó khăn khi bản địa hóa đa ngôn ngữ.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Dự án compile thành công với `SWIFT_STRICT_CONCURRENCY = complete` không có cảnh báo tương tranh.
- QG-07: Thread Sanitizer không phát hiện bất kỳ data race nào.
- QG-11: 100% các API gọi mạng sử dụng `async`/`await` hiện đại.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Mọi token nhạy cảm phải lưu trong iOS Keychain Services với cờ `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`.
- Bật tính năng App Transport Security (ATS) ngăn kết nối HTTP không bảo mật.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Cấu trúc Xcode project và SPM packages chuẩn hóa.
- Các Views, ViewModels và SwiftData models.
- Báo cáo kiểm thử XCTest với 0 cảnh báo data race.

## 13. Related & Complementary Skills
- `dex-mobile-release-pipelines`: Cấu hình Fastlane và chứng chỉ ký iOS Provisioning Profile.
- `dex-mobile-performance-profiling`: Sử dụng Instruments kiểm tra memory leaks và time profiling.
- `dex-native-device-integration`: Tích hợp FaceID/TouchID và camera trên iOS.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng ngân hàng số iOS gặp lỗi data race khi cập nhật số dư từ WebSocket. Kỹ sư sử dụng `dex-ios-app-architecture`, chuyển đổi module quản lý tài khoản sang `actor AccountStore`, đánh dấu UI ViewModel là `@MainActor`, bật Strict Concurrency Checking trong Xcode và dùng Thread Sanitizer phát hiện và loại bỏ triệt để 3 lỗi race condition nguy hiểm, bảo vệ tính toàn vẹn dữ liệu tiền tệ.
