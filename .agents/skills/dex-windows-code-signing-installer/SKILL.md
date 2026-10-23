---
name: dex-windows-code-signing-installer
description: Sign, timestamp, and verify Windows executables, DLLs, and installers (MSI, MSIX, NSIS, Inno Setup). Enforce Authenticode integrity, RFC 3161 timestamps, and smart UAC elevation handling.
---

# dex-windows-code-signing-installer

## 1. Purpose & Scope
Thiết kế và tự động hóa quy trình ký số mã nguồn (Code Signing) và đóng gói bộ cài đặt trên Windows; ký số điện tử theo tiêu chuẩn Microsoft Authenticode cho các tệp thực thi (`.exe`), thư viện (`.dll`) và gói cài đặt (`.msi`, `.msix`, NSIS, Inno Setup); cấu hình dấu thời gian hợp lệ theo chuẩn RFC 3161 (Secure Timestamping), loại bỏ cảnh báo Windows Defender SmartScreen và bảo đảm tính toàn vẹn của ứng dụng.

## 2. When to Use
- Khi chuẩn bị xuất bản phần mềm desktop Windows ra thị trường hoặc phân phối nội bộ doanh nghiệp.
- Khi ứng dụng bị Windows Defender SmartScreen chặn với thông báo cảnh báo màu xanh "Windows protected your PC / Unknown Publisher".
- Khi cần xác minh chữ ký số tự động trong pipeline CI/CD trước khi phát hành phiên bản mới.

## 3. When NOT to Use
- Khi đóng gói ứng dụng cho các nền tảng di động (Android APK / iOS IPA) có quy trình ký số riêng biệt của Google/Apple.
- Khi chỉ chạy thử nghiệm nội bộ trên máy phát triển cá nhân đã bật chế độ Developer Mode.

## 4. Prerequisites & Input Context
- **Chứng chỉ ký số:** Chứng chỉ Code Signing hợp lệ (EV Code Signing Certificate trên Hardware Token hoặc Cloud HSM như Azure Key Vault / AWS KMS).
- **Công cụ ký:** Microsoft `signtool.exe` trong Windows SDK.

## 5. Core Concepts & Taxonomy
- **Authenticode & PKCS #7:** Tiêu chuẩn mật mã của Microsoft nhúng chữ ký số và chứng chỉ X.509 vào phần thư mục bảo mật (Security Directory) của tệp định dạng PE.
- **RFC 3161 Timestamping:** Cơ chế đóng dấu thời gian độc lập từ một Time Stamping Authority (TSA) chứng minh mã nguồn đã được ký trước khi chứng chỉ hết hạn, giúp chữ ký có hiệu lực vĩnh viễn.
- **SmartScreen Reputation Score:** Chỉ số uy tín được tính toán bởi thuật toán đám mây của Microsoft dựa trên khối lượng tải về và chữ ký EV/Standard.

## 6. Step-by-Step Execution Workflow
1. Biên dịch toàn bộ các tệp `.exe` và `.dll` ở cấu hình Release.
2. Thực hiện ký số song song từng tệp nhị phân con bằng `signtool.exe` sử dụng thuật toán băm SHA-256.
3. Đóng gói các tệp nhị phân đã ký vào bộ cài đặt (NSIS, Inno Setup, hoặc WiX Toolset MSI).
4. Ký số chính tệp cài đặt cuối cùng kèm URL dấu thời gian RFC 3161 uy tín (DigiCert, Sectigo).
5. Kiểm tra tính hợp lệ của chữ ký bằng lệnh `signtool verify /pa /v installer.exe`.
6. Kiểm tra giao diện xác thực người dùng (UAC Prompt) để khẳng định tên nhà phát hành (Verified Publisher) hiển thị chuẩn xác.

## 7. Concrete Examples
### Kich ban PowerShell ky so tu dong va dong dau thoi gian RFC 3161 bang signtool:
```powershell
param(
    [string]$TargetFile = "bin\Release\DEXDesktopApp.exe",
    [string]$CertThumbprint = "a1b2c3d4e5f6...",
    [string]$TimestampServer = "http://timestamp.digicert.com"
)

$signtool = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"

Write-Host "Signing and Timestamping: $TargetFile"

# Ky so SHA-256 voi RFC 3161 Timestamp
& $signtool sign /sha1 $CertThumbprint `
                 /fd sha256 `
                 /tr $TimestampServer `
                 /td sha256 `
                 /v $TargetFile

if ($LASTEXITCODE -ne 0) {
    Write-Error "Code signing failed!"
    exit 1
}

# Xac minh chu ky vua ky
& $signtool verify /pa /v $TargetFile
if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Authenticode signature is 100% valid." -ForegroundColor Green
} else {
    Write-Error "Signature verification FAILED!"
    exit 1
}
```

## 8. Anti-Patterns & Common Traps
- **Omission of RFC 3161 Timestamp:** Ký số nhưng quên đóng dấu thời gian `/tr`, khiến ứng dụng bị Windows coi là không hợp lệ ngay khi chứng chỉ hết hạn 1 năm sau.
- **Using Deprecated SHA-1 Hash:** Dùng thuật toán băm SHA-1 yếu (`/fd sha1`) bị Windows 10/11 chặn mặc định.
- **Signing Installer but Not Bundled Binaries:** Chỉ ký tệp installer bên ngoài nhưng để các tệp `.exe` và `.dll` bên trong không có chữ ký, dẫn đến việc phần mềm diệt virus cách ly các tệp con.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các tệp `.exe`, `.dll` và bộ cài đặt đều có chữ ký số hợp lệ với thuật toán băm SHA-256.
- **QG-02**: Mọi chữ ký đều chứa dấu thời gian RFC 3161 hợp lệ từ một TSA được chứng nhận.
- **QG-03**: Hộp thoại UAC hiển thị đúng tên Verified Publisher mà không xuất hiện cảnh báo "Unknown Publisher".

## 10. Security & Safety Boundaries
- Bảo vệ tuyệt đối Private Key; không lưu chứng chỉ trong Git; sử dụng Hardware Security Module (HSM) hoặc Azure Key Vault để ký từ xa.

## 11. Platform Adapters
- **Runtimes**: Microsoft signtool.exe, Azure Trusted Signing, Inno Setup, WiX Toolset, NSIS.

## 12. Deliverables & Output Artifacts
- Kịch bản ký số tự động tích hợp CI/CD (`sign_release_artifacts.ps1`).
- Báo cáo kiểm định chữ ký số và chuỗi chứng chỉ (`code_signing_audit.json`).

## 13. Related & Complementary Skills
dex-windows-service-recovery, dex-windows-usb-portability, dex-windows-app-crash-dumps

## 14. Realistic Usage Example
```powershell
# Kiem tra chu ky so Authenticode bang PowerShell cmdlet
Get-AuthenticodeSignature -FilePath ".\setup.exe" | Format-List
```
