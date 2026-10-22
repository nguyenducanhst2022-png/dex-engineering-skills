---
name: dex-desktop-update-delivery
description: Manage desktop application auto-updates, update channels (alpha/beta/stable), cryptographic artifact signatures (codesign/minisign), delta updates, and atomic rollbacks. Use when delivering reliable updates to desktop apps.
---

# dex-desktop-update-delivery

## 1. Purpose & Scope
Thiết kế, triển khai và vận hành hệ thống phân phối bản cập nhật tự động an toàn (Secure Auto-Update Delivery) cho ứng dụng máy tính (Windows, macOS, Linux); quản lý các kênh phát hành (Release Channels: Alpha, Beta, Stable), xác thực chữ ký mật mã học của gói cài đặt (Cryptographic Signature Verification bằng Minisign / Ed25519 / Code Signing Certificate), áp dụng cập nhật vi sai (Differential / Delta Updates) để giảm 90% băng thông tải về, và thực thi cơ chế thay thế tệp nguyên tử (Atomic File Replacement) kèm khả năng tự động khôi phục (Rollback) khi bản cập nhật bị crash lúc khởi động.

## 2. When to Use
- Khi ứng dụng desktop đã được phân phối tới hàng chục nghìn người dùng và cần cơ chế vá lỗi bảo mật khẩn cấp từ xa.
- Khi quá trình cập nhật ứng dụng thường xuyên bị lỗi gián đoạn do file đang bị khóa hoặc mất kết nối mạng giữa chừng.
- Khi cần ngăn chặn triệt để nguy cơ kẻ tấn công thực hiện tấn công Man-in-the-Middle (MITM) để đẩy bản cập nhật chứa mã độc cho người dùng.

## 3. When NOT to Use
- Ứng dụng web được cập nhật tức thì trên máy chủ máy chủ (dùng `dex-zero-downtime-rollouts`).
- Ứng dụng di động được quản lý cập nhật qua Google Play và App Store (dùng `dex-mobile-release-pipelines`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Bộ cài đặt binary mới đã được biên dịch.
- Khóa ký số (Code Signing Certificate cho Windows/macOS, Ed25519 private key cho Tauri/Electron updater).
- Tệp manifest mô tả phiên bản (`latest.json` hoặc `update.xml`).
- **Điều kiện tiên quyết**:
- Máy chủ lưu trữ bản cập nhật (S3 Bucket, Cloudflare R2, GitHub Releases) có hỗ trợ HTTPS.
- Công cụ ký số mã nguồn (`signtool.exe` trên Windows, `codesign` trên macOS, hoặc `minisign`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Signature Verification Before Execution**: Ứng dụng tải bản cập nhật về thư mục tạm, kiểm tra hàm băm SHA256 và xác thực chữ ký số bằng Public Key được nhúng sẵn trong ứng dụng; nếu chữ ký không khớp, lập tức hủy bỏ và xóa tệp tải về.
- **Atomic Binary Swap**: Ứng dụng mới được giải nén sẵn; khi người dùng khởi động lại, script helper thực hiện thao tác đổi tên/thay thế tệp trong một thao tác duy nhất (Atomic rename), không ghi đè từng phần.
- **Startup Health Check & Self-Rollback**: Sau khi cập nhật, ứng dụng mới có 10 giây để khởi động và gửi tín hiệu 'Healthy'; nếu app bị crash hoặc deadlock trước mốc này, hệ thống tự động đổi lại binary phiên bản cũ để cứu người dùng.
- **Quy tắc quyết định kỹ thuật**:
- **Bắt Buộc Xác Thực Chữ Ký Số**: Tuyệt đối không thực thi bất kỳ gói cập nhật nào nếu thiếu chữ ký số hợp lệ từ nhà phát triển.
- **Tải Cập Nhật Ở Chế Độ Chạy Ngầm Không Chặn Người Dùng**: Quá trình tải gói cập nhật phải diễn ra ngầm với độ ưu tiên I/O thấp, chỉ hiển thị thông báo khởi động lại khi tải xong.
- **Hỗ Trợ Kênh Cập Nhật Phân Tách**: Cho phép nhân viên nội bộ đăng ký kênh `alpha` hoặc `beta` để kiểm thử trước khi phát hành cho toàn bộ người dùng ở kênh `stable`.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Ứng dụng bị hỏng hoàn toàn (Bricked) do mất điện khi đang ghi đè file `.exe`**: Do ghi đè trực tiếp -> Khắc phục: Tải vào thư mục `.update_staging`, chỉ hoán đổi thư mục bằng lệnh atomic move khi đã hoàn tất.
- **Người dùng tải nhầm bản cập nhật giả mạo do DNS bị đầu độc**: Do updater không kiểm tra chữ ký số -> Khắc phục: Nhúng cứng khóa công khai Public Key (Ed25519) vào mã nguồn ứng dụng để xác thực tệp trước khi chạy installer.

## 6. Step-by-Step Execution Workflow
1. Biên dịch bộ cài đặt ứng dụng cho từng nền tảng: `.exe` (Windows), `.dmg` (macOS), `.AppImage` (Linux).
2. Thực hiện ký số binary bằng chứng chỉ uy tín (DigiCert EV Code Signing hoặc Apple Developer ID).
3. Ký số tệp lưu trữ bằng Minisign / Tauri CLI: `tauri signer sign -k ./tauri.key bundle.tar.gz`.
4. Sinh tệp manifest `latest.json` chứa phiên bản, ghi chú thay đổi, URL tải về và chữ ký mã hóa.
5. Đẩy tệp manifest và các gói cài đặt lên CDN phân phối an toàn qua HTTPS.
6. Ứng dụng desktop định kỳ kiểm tra `latest.json`: Tải ngầm bản cập nhật, xác thực chữ ký và lưu vào bộ đệm.
7. Hiển thị thông báo: 'Đã có bản cập nhật mới. Khởi động lại ngay để áp dụng' và thực thi atomic swap.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```json
// latest.json - Cryptographically Signed Update Manifest
{
  "version": "v4.0.0",
  "notes": "Nâng cấp bảo mật và sửa lỗi hiệu năng trong module xuất báo cáo.",
  "pub_date": "2026-10-22T14:30:00Z",
  "platforms": {
    "windows-x86_64": {
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6IHNpZ25hdHVyZSBmcm9tIHRhdXJpIHNlY3JldCBrZXkKUldUUW1v...",
      "url": "https://updates.example.com/releases/v4.0.0/myapp_x64_en-US.msi.zip"
    },
    "darwin-aarch64": {
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6IHNpZ25hdHVyZSBmcm9tIHRhdXJpIHNlY3JldCBrZXkKUldSOG...",
      "url": "https://updates.example.com/releases/v4.0.0/myapp_aarch64.app.tar.gz"
    }
  }
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra chữ ký số file cài đặt Windows: `signtool verify /pa /v myapp-setup.exe`
- Kiểm tra chữ ký số macOS: `spctl --assess --type execute --verbose myapp.app`
- Xác minh tính toàn vẹn chữ ký Minisign: `minisign -V -p public.key -m update.zip -s update.zip.sig`

## 8. Anti-Patterns & Common Traps
- **Bắt người dùng dừng công việc và chờ thanh loading cập nhật**: Gây gián đoạn trải nghiệm người dùng.
- **Lưu trữ Private Key ký số trực tiếp trên server build công cộng**: Rủi ro lộ key dẫn tới hacker phát hành phần mềm độc hại mạo danh.
- **Không có cơ chế Rollback**: Khi bản cập nhật có lỗi nghiêm trọng làm crash app ngay khi khởi động, người dùng không thể tự mở app để nhận bản vá tiếp theo.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các file cập nhật đều có chữ ký số hợp lệ và được xác minh thành công trước khi cài đặt.
- QG-07: Cơ chế cập nhật vi sai (Delta updates) giảm dung lượng tải về tối thiểu 60% đối với các bản vá nhỏ.
- QG-11: Quá trình chuyển đổi phiên bản diễn ra nguyên tử (Atomic), không để lại file rác hoặc trạng thái hỏng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Private Key dùng để ký bản cập nhật phải được lưu trong Hardware Security Module (HSM) hoặc GitHub Encrypted Secrets.
- Mọi kênh tải bản cập nhật bắt buộc phải thực thi qua giao thức TLS 1.3.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Tệp manifest phiên bản `latest.json` có chữ ký mật mã.
- Pipeline tự động ký số và xuất bản artifact cập nhật.
- Báo cáo kiểm tra xác thực chữ ký trên cả Windows và macOS.

## 13. Related & Complementary Skills
- `dex-windows-packaging`: Đóng gói installer MSI/NSIS cho Windows.
- `dex-tauri-desktop-integration`: Tích hợp Tauri auto-updater plugin.
- `dex-supply-chain-security`: Bảo vệ pipeline phát hành chống tấn công chuỗi cung ứng.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng máy tính kế toán cần cập nhật biểu mẫu thuế mới cho 50,000 doanh nghiệp. Áp dụng `dex-desktop-update-delivery`, đội ngũ cấu hình Tauri updater có ký số bằng khóa Ed25519. Bản cập nhật vi sai chỉ nặng 4.5MB (thay vì 60MB toàn bộ app) được tải ngầm khi người dùng đang làm việc. Khi người dùng tắt máy vào cuối ngày, ứng dụng tự động hoán đổi binary nguyên tử trong 1 giây, sẵn sàng cho phiên làm việc mới vào sáng hôm sau mà không gặp bất kỳ lỗi gián đoạn nào.
