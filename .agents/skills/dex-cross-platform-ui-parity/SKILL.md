---
name: dex-cross-platform-ui-parity
description: Establish and automate cross-platform design parity audits across Web, iOS, Android, and Desktop ensuring consistent brand expression while honoring native platform UX conventions. Use when maintaining multi-platform product suites.
---

# dex-cross-platform-ui-parity

## 1. Purpose & Scope
Thiết lập quy trình kiểm toán và tự động hóa tính tương đương về thiết kế đa nền tảng (Cross-Platform UI Parity) giữa Web, iOS, Android và Desktop; bảo đảm trải nghiệm thương hiệu đồng nhất trong khi vẫn tôn trọng các quy ước UX bản địa của từng hệ điều hành.

## 2. When to Use
- Khi phát triển song song ứng dụng trên nhiều nền tảng (React Web, React Native / Flutter, Swift iOS, Kotlin Android).
- Khi người dùng phản ánh tính năng hoặc giao diện trên Android hoạt động khác biệt bất thường so với iOS.
- Khi đồng bộ hóa hệ thống Design System giữa các nền tảng công nghệ khác nhau.

## 3. When NOT to Use
- Khi ứng dụng được thiết kế độc quyền cho một hệ điều hành duy nhất và tận dụng toàn bộ các API đặc thù của hệ điều hành đó.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bản thiết kế giao diện đa nền tảng, mã nguồn các ứng dụng client, danh mục tiêu chí đánh giá quy ước UX.
- **Quyền hạn truy cập:** Quyền truy cập các repository ứng dụng Web, iOS và Android.

## 5. Core Concepts & Taxonomy
- **Brand Consistency vs. Platform Conventions:** Giữ nguyên các giá trị cốt lõi của thương hiệu (màu sắc, typography, giọng điệu) nhưng tôn trọng quy ước nền tảng (nút Back trên Android, thanh Navigation Bar dưới đáy của iOS, Context Menu trên Desktop).
- **Parity Scorecard:** Bảng điểm đánh giá mức độ tương đương về tính năng, bố cục, luồng thao tác và khả năng tiếp cận giữa các nền tảng.
- **Token Mapping Layer:** Ánh xạ cùng một bộ Design Tokens sang các định dạng native: CSS Variables (Web), XML/Compose Colors (Android), Assets Catalogs / Swift (iOS).

## 6. Step-by-Step Execution Workflow
1. Xây dựng ma trận tính năng và màn hình đối sánh giữa Web, iOS, Android và Desktop.
2. Rà soát sự khác biệt về quy ước tương tác (Back button, Pull-to-refresh, Bottom Sheet vs Modal).
3. Tự động hóa quá trình xuất token từ nguồn duy nhất (Single Source of Truth) tới tất cả các nền tảng client.
4. Thực hiện chụp màn hình tự động (Visual Snapshots) trên các thiết bị thực tế hoặc giả lập.
5. Chấm điểm độ tương đương (Parity Index) và gắn cờ các sai lệch về bố cục hoặc hành vi.
6. Họp đồng bộ giữa các đội ngũ kỹ sư client để thống nhất lộ trình thu hẹp khoảng cách khác biệt.

## 7. Concrete Examples
### Bảng tiêu chí đánh giá Cross-Platform UI Parity:
| Tiêu chí | Web | iOS (SwiftUI) | Android (Jetpack Compose) | Trạng thái Parity |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Color** | `--color-brand-600` | `Color("Brand600")` | `MaterialTheme.colorScheme.primary` | Đạt chuẩn (100%) |
| **Typography Hierarchy** | Inter font scale | San Francisco | Roboto | Đạt chuẩn (Native) |
| **Navigation Pattern** | Top Header / Sidebar | Bottom TabBar | Bottom Navigation / Rail | Chuẩn quy ước |
| **Modal / Dialog** | Centered Modal Dialog | Action Sheet / Sheet | Bottom Sheet / AlertDialog | Chuẩn quy ước |
| **Swipe Dismiss** | Nút đóng rõ ràng | Vuốt xuống để đóng | Nút Back phần cứng/cử chỉ | Đạt chuẩn |


## 8. Anti-Patterns & Common Traps
- **Force iOS Patterns on Android:** Bắt buộc giao diện Android phải dùng thanh điều hướng và biểu tượng của iOS làm người dùng Android xa lạ.
- **Divergent Token Releases:** Cập nhật bảng màu trên Web nhưng bỏ quên ứng dụng Mobile trong 6 tháng khiến nhận diện thương hiệu bị phân mảnh.
- **Ignoring Desktop Scaling:** Mang nguyên vẹn giao diện ứng dụng di động kéo dãn lên màn hình Desktop 4K mà không tối ưu mật độ hiển thị.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% token thương hiệu (Brand Colors, Typography Scale) được phân phối đồng bộ từ cùng một nguồn mã nguồn.
- **QG-04**: Điểm số Parity Scorecard giữa các nền tảng đạt tối thiểu 90% tính năng cốt lõi.
- **QG-07**: Không có vi phạm quy ước cơ bản của hệ điều hành (như thiếu hỗ trợ nút Back trên Android).

## 10. Security & Safety Boundaries
- Bảo đảm các chính sách bảo mật sinh trắc học (FaceID, TouchID, Android Biometric) được triển khai nhất quán và an toàn trên các phiên bản client.

## 11. Platform Adapters
- **Build & Sync**: Style Dictionary, Fastlane, GitHub Actions.
- **Testing**: Appium, Maestro, Percy, BrowserStack.

## 12. Deliverables & Output Artifacts
- Ma trận đánh giá Cross-Platform UI Parity.
- Pipeline đồng bộ hóa Design Tokens đa nền tảng.
- Bộ kịch bản kiểm thử trực quan trên thiết bị thực tế.

## 13. Related & Complementary Skills
dex-design-token-migration, dex-component-state-matrix, dex-mobile-first-responsive-patterns

## 14. Realistic Usage Example
```powershell
# Chạy kiểm thử tự động so sánh giao diện đa nền tảng với Maestro
maestro test .maestro/cross-platform-flow.yaml

# Xuất tokens đồng bộ cho Web, iOS và Android
npm run build-tokens-all-platforms
```
