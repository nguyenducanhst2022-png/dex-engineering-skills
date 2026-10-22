---
name: dex-mobile-release-pipelines
description: Automate mobile release pipelines with Fastlane, Android keystore signing, iOS provisioning profiles & certificates, semantic version codes, and store submission. Use when automating mobile build, test, and release processes.
---

# dex-mobile-release-pipelines

## 1. Purpose & Scope
Tự động hóa hoàn toàn quy trình đóng gói, ký số và phát hành ứng dụng di động (Mobile CI/CD Release Pipelines) bằng Fastlane và GitHub Actions; quản lý chứng chỉ ký an toàn (Android Keystore, iOS Distribution Certificate, Provisioning Profiles qua Fastlane Match), tự động tăng số phiên bản và mã build (Semantic Versioning & Build Codes), biên dịch môi trường sạch (Clean Hermetic Builds) và phân phối tự động tới Google Play Console (Internal/Alpha/Production tracks) và Apple App Store / TestFlight.

## 2. When to Use
- Khi quy trình phát hành ứng dụng di động đang phải làm thủ công bằng Xcode / Android Studio (mất 2-3 tiếng mỗi lần release).
- Khi các thành viên trong đội ngũ bị lỗi chứng chỉ ký số (Code Signing Mismatch) hoặc hết hạn chứng chỉ provisioning profile.
- Khi cần thiết lập luồng phát hành tự động: Merge vào nhánh `main` -> Tự động đóng gói và đẩy lên TestFlight / Play Console Internal.

## 3. When NOT to Use
- Xây dựng tính năng bên trong ứng dụng Android/iOS (dùng `dex-android-app-architecture` hoặc `dex-ios-app-architecture`).
- Đóng gói ứng dụng desktop Windows/macOS (dùng `dex-windows-packaging` hoặc `dex-tauri-desktop-integration`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mã nguồn ứng dụng di động (React Native, Flutter, Kotlin Multiplatform hoặc Native Android/iOS).
- Thông tin tài khoản lập trình viên: Google Play Service Account JSON, Apple App Store Connect API Key.
- Secrets ký số: Keystore Base64, Match Git repository URL và encryption password.
- **Điều kiện tiên quyết**:
- Máy runner macOS (đối với build iOS) và Linux/macOS (đối với Android).
- Công cụ Fastlane phiên bản 2.215+ được cài đặt.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Fastlane Match Centralized Signing**: Lưu trữ chứng chỉ ký và provisioning profile trong một Git repository riêng biệt được mã hóa bằng OpenSSL; toàn bộ đội ngũ và CI dùng chung một nguồn chứng chỉ duy nhất.
- **Hermetic Build Isolation**: Quá trình build không phụ thuộc vào trạng thái máy của lập trình viên cá nhân; mọi SDK và chứng chỉ được inject động qua biến môi trường CI.
- **Staged Track Promotion**: Bản build đầu tiên chỉ lên kênh thử nghiệm nội bộ (TestFlight / Internal Testing); sau khi pass QA mới được thăng hạng (promote) lên kênh công khai.
- **Quy tắc quyết định kỹ thuật**:
- **Tuyệt Đối Không Commit File Keystore Lên Git**: File `.keystore` hoặc `.jks` phải được mã hóa Base64 và lưu trong CI Secrets.
- **Không Lưu Mật Khẩu Ký Trong Mã Nguồn**: Mật khẩu alias và keystore phải truyền qua biến môi trường (`ANDROID_KEYSTORE_PASSWORD`).
- **Tự Động Tăng Version Code**: Mỗi lần chạy pipeline release, `versionCode` (Android) và `buildNumber` (iOS) phải tự động tăng dựa trên số commit Git hoặc Run ID.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Build iOS thất bại trên CI do thiếu Provisioning Profile**: Do profile mới chưa được đồng bộ -> Khắc phục: Chạy `fastlane match appstore --readonly` trong pipeline để tải profile chuẩn xác.
- **Google Play từ chối file AAB do trùng version code**: Do lập trình viên quên tăng số build -> Khắc phục: Tự động lấy build number mới nhất từ Play Console bằng Fastlane plugin `google_play_track_version_codes`.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo cấu trúc Fastlane: `fastlane/Fastfile`, `fastlane/Appfile` cho cả thư mục `android/` và `ios/`.
2. Thiết lập cơ chế quản lý chứng chỉ ký số: Cấu hình `match` cho iOS và giải mã keystore từ base64 cho Android.
3. Định nghĩa lane `build_android`: Chạy lint, test, tăng version code, assemble Release AAB và ký số.
4. Định nghĩa lane `build_ios`: Đồng bộ certs qua `match`, tăng build number, build IPA qua `gym`.
5. Cấu hình upload tự động: Sử dụng `upload_to_play_store` và `upload_to_testflight`.
6. Tích hợp pipeline CI trên GitHub Actions: Kích hoạt khi có tag `v*.*.*` hoặc push nhánh `release/*`.
7. Gửi thông báo hoàn tất phát hành kèm link tải vào kênh Slack/Discord của đội ngũ.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```ruby
# fastlane/Fastfile
default_platform(:android)

platform :android do
  desc "Build and deploy to Google Play Internal Track"
  lane :internal do
    # Tự động lấy mã build lớn nhất từ Play Store và tăng 1
    current_version = google_play_track_version_codes(track: "internal")[0]
    new_version_code = current_version + 1
    
    gradle(
      task: "bundle",
      build_type: "Release",
      properties: {
        "android.injected.version.code" => new_version_code
      }
    )
    
    upload_to_play_store(
      track: "internal",
      aab: "app/build/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end
end
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính hợp lệ của Fastfile: `bundle exec fastlane lanes`
- Thử nghiệm build cục bộ không upload: `bundle exec fastlane android build_check`
- Kiểm tra trạng thái chứng chỉ iOS: `bundle exec fastlane match nuke --dry_run`

## 8. Anti-Patterns & Common Traps
- **Ký ứng dụng bằng Debug Key đưa lên store**: Khiến ứng dụng bị từ chối hoặc không thể nâng cấp sau này.
- **Mỗi lập trình viên tự tạo 1 Development Certificate riêng trên Apple Developer Portal**: Làm cạn kiệt giới hạn chứng chỉ tối đa của tài khoản.
- **Bỏ qua bước chạy unit test trước khi build release**: Đóng gói cả mã nguồn có lỗi lên store.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Pipeline tự động hóa 100% từ commit code tới khi artifact xuất hiện trên TestFlight / Play Console.
- QG-07: Không có bất kỳ keystore, password hay private key nào bị rò rỉ trong log CI.
- QG-11: Bản build vượt qua khâu kiểm tra chữ ký số (Signature Verification) thành công.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Khóa quyền truy cập repository chứa chứng chỉ Fastlane Match chỉ cho tài khoản CI và Tech Lead.
- Thiết lập cảnh báo bảo mật khi có người truy cập trái phép vào Google Play API Service Account.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Tệp cấu hình `Fastfile`, `Appfile`, `Matchfile`.
- Workflow GitHub Actions (`release-mobile.yml`).
- Artifact phát hành `.aab` và `.ipa` được ký số hoàn chỉnh.

## 13. Related & Complementary Skills
- `dex-semantic-version-automation`: Quản lý quy chuẩn tăng phiên bản semver.
- `dex-cicd-automation`: Thiết lập runner và môi trường pipeline CI.
- `dex-supply-chain-security`: Xác thực tính toàn vẹn của dependencies di động.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một startup di động tốn nửa ngày làm việc của kỹ sư trưởng mỗi tuần chỉ để ngồi export IPA và upload APK thủ công. Áp dụng `dex-mobile-release-pipelines`, họ cấu hình Fastlane Match cho iOS và quản lý keystore qua GitHub Secrets cho Android. Khi có commit merge vào nhánh release, pipeline tự động chạy test, build AAB/IPA, tăng build number và đẩy thẳng lên TestFlight và Google Play Internal trong vòng 20 phút mà không cần con người can thiệp.
