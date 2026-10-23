---
name: dex-kotlin-multiplatform-builds
description: Architect and optimize Kotlin Multiplatform (KMP) shared modules, target compilation matrices (Android, iOS, JVM, Web, Desktop), and expect/actual declarations. Use when building cross-platform shared business logic.
---

# dex-kotlin-multiplatform-builds

## 1. Purpose & Scope
Thiết kế và tối ưu hóa quy trình đóng gói mã nguồn chia sẻ với Kotlin Multiplatform (KMP); quản lý ma trận biên dịch đa nền tảng (Android, iOS Frameworks qua CocoaPods/Swift Package Manager, JVM, WebAssembly/JS), và kiểm soát cơ chế khai báo `expect`/`actual` tuân thủ nguyên tắc cách ly nền tảng.

## 2. When to Use
- Khi phát triển ứng dụng di động đa nền tảng muốn chia sẻ 100% mã nguồn nghiệp vụ, networking và database giữa Android và iOS mà vẫn giữ nguyên UI native.
- Khi xây dựng SDK thư viện dùng chung cho cả backend JVM và ứng dụng client di động.
- Khi tối ưu hóa thời gian build và kích thước binary của các module chia sẻ KMP.

## 3. When NOT to Use
- Khi dự án là ứng dụng thuần Android hoặc thuần backend không có nhu cầu chia sẻ mã nguồn với nền tảng khác.
- Khi đội ngũ chỉ sử dụng Flutter hoặc React Native để chia sẻ cả tầng giao diện lẫn logic.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp cấu hình `build.gradle.kts` của KMP module, Gradle toolchain (JDK 17/21), Xcode toolchain (đối với target iOS).
- **Quyền hạn truy cập:** Quyền thực thi Gradle build commands và cấu hình target SDKs.

## 5. Core Concepts & Taxonomy
- **Common SourceSet (`commonMain`):** Thư mục chứa mã nguồn Kotlin thuần túy chạy được trên mọi nền tảng không phụ thuộc vào bất kỳ thư viện đặc thù hệ điều hành nào.
- **`expect` / `actual` Pattern:** Cơ chế cho phép khai báo một interface/class ở `commonMain` và cung cấp mã triển khai riêng biệt cho từng nền tảng (`androidMain`, `iosMain`, `jvmMain`).
- **XCFramework Packaging:** Định dạng đóng gói nhị phân cho phép mã Kotlin biên dịch thành framework native có thể nhúng trực tiếp vào dự án Xcode của iOS.

## 6. Step-by-Step Execution Workflow
1. Khai báo các target nền tảng trong block `kotlin { ... }` của tệp `build.gradle.kts` (androidTarget, iosArm64, iosSimulatorArm64, jvm).
2. Cấu hình phân cấp SourceSets kế thừa tự nhiên từ `commonMain`.
3. Đặt toàn bộ business logic, data models, serialization (kotlinx.serialization), và HTTP client (Ktor) bên trong `commonMain`.
4. Sử dụng cơ chế `expect`/`actual` một cách tối thiểu chỉ cho các thành phần truy cập phần cứng hoặc lưu trữ đặc thù (như file system, keychain).
5. Cấu hình task sinh XCFramework tự động để tích hợp vào dự án iOS qua SPM (Swift Package Manager).
6. Thiết lập CI pipeline tự động chạy unit test trên `commonTest` và kiểm tra biên dịch chéo trên tất cả các targets.

## 7. Concrete Examples
### Ví dụ cấu hình Kotlin Multiplatform trong `build.gradle.kts`:
```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
}

kotlin {
    // 1. Khai báo các targets mục tiêu
    androidTarget()
    jvm()
    
    listOf(
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "SharedCore"
            isStatic = true
        }
    }

    // 2. Cấu hình dependencies dùng chung
    sourceSets {
        commonMain.dependencies {
            implementation(libs.ktor.client.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.kotlinx.coroutines.core)
        }
        commonTest.dependencies {
            implementation(libs.kotlin.test)
        }
    }
}
```

## 8. Anti-Patterns & Common Traps
- **Leaking Platform Dependencies into Common:** Import thư viện `java.*` hoặc `android.*` vào `commonMain`, làm hỏng hoàn toàn khả năng biên dịch sang iOS.
- **Overusing expect/actual:** Lạm dụng `expect`/`actual` cho các logic nghiệp vụ thông thường thay vì sử dụng Dependency Injection với Interfaces.
- **Monolithic KMP Modules:** Gom toàn bộ logic của cả ứng dụng vào một module KMP duy nhất khiến thời gian biên dịch Gradle tăng vọt.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Mã nguồn trong `commonMain` vượt qua 100% các bài kiểm tra linter không chứa import đặc thù nền tảng.
- **QG-04**: Toàn bộ unit tests trong `commonTest` chạy pass trên cả target Android và iOS Simulator.
- **QG-07**: Task đóng gói XCFramework hoàn tất thành công và tạo ra binary hợp lệ cho Xcode.

## 10. Security & Safety Boundaries
- Bảo đảm các khóa API hoặc credentials bí mật không bị hardcode trong mã nguồn `commonMain`.
- Tận dụng lưu trữ bảo mật native của từng nền tảng (Android EncryptedSharedPreferences và iOS Keychain) cho dữ liệu nhạy cảm.

## 11. Platform Adapters
- **Build**: Gradle KMP Plugin, Kotlin Native Compiler (`kotlinc`).
- **Client Integration**: Swift Package Manager, CocoaPods, Android Gradle Plugin.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình `build.gradle.kts` chuẩn hóa cho dự án KMP.
- Mã nguồn module chia sẻ `commonMain` và các bản triển khai `actual` hợp lệ.
- Task tự động build XCFramework cho iOS.

## 13. Related & Complementary Skills
dex-android-app-architecture, dex-ios-app-architecture, dex-mobile-offline-sync

## 14. Realistic Usage Example
```powershell
# Chạy toàn bộ unit tests trên các targets của Kotlin Multiplatform module
./gradlew allTests

# Đóng gói XCFramework cho iOS
./gradlew assembleSharedCoreReleaseXCFramework
```
