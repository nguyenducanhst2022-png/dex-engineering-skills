---
name: dex-windows-packaging
description: Package and distribute applications for Windows environments, automating MSIX/InnoSetup builds, WinGet manifest publication, code signing with Authenticode, PowerShell automation scripts, and Windows Service management. Use when targeting Windows enterprise or desktop deployment.
---

# dex-windows-packaging

## 1. Purpose & Scope
Đóng gói, phân phối và triển khai ứng dụng chuyên nghiệp cho môi trường hệ điều hành Windows; tự động hóa quy trình tạo bộ cài đặt (MSIX, Inno Setup, WiX Toolset), xuất bản lên Windows Package Manager (WinGet), ký số mã nguồn (Authenticode Code Signing), viết script tự động hóa PowerShell chuẩn mực và quản lý tiến trình nền dạng Windows Service.

## 2. When to Use
- Khi cần phân phối ứng dụng desktop hoặc công cụ dòng lệnh cho người dùng Windows.
- Khi cần xuất bản phần mềm lên WinGet hoặc Microsoft Store để người dùng cài đặt bằng lệnh `winget install`.
- Khi ứng dụng bị Windows Defender SmartScreen chặn do thiếu chữ ký số hợp lệ.
- Khi cần chạy ứng dụng backend dạng dịch vụ nền tự khởi động cùng Windows (Windows Service).

## 3. When NOT to Use
- Triển khai container hóa trên Kubernetes/Docker (dùng `dex-cicd-automation`).
- Ứng dụng web chạy trên trình duyệt (dùng `dex-release-engineering`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Các file nhị phân đã biên dịch (`.exe`, `.dll`) hoặc ứng dụng đóng gói.
- Thông tin chứng chỉ ký số (Code Signing Certificate / Azure Trusted Signing).
- Cấu hình metadata: Tên, phiên bản, tác giả, icon, giấy phép.

**Điều kiện tiên quyết:**
- Môi trường Windows 11 / Windows Server có cài đặt Windows SDK, PowerShell 7+, hoặc công cụ đóng gói (Inno Setup / WiX).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Bắt Buộc Ký Số Code Signing**: Bộ cài đặt và file `.exe` phát hành cho người dùng cuối bắt buộc phải có chữ ký số hợp lệ kèm timestamp server.
- **Gỡ Cài Đặt Không Để Lại Rác (Clean Uninstall)**: Quá trình gỡ cài đặt phải dọn dẹp sạch sẽ các tệp tạm và mục registry đã đăng ký.
- **Hỗ Trợ Chế Độ Cài Đặt Tự Động (Headless / Silent Mode)**: Bộ cài phải hỗ trợ cài đặt không cần giao diện đồ họa phục vụ môi trường doanh nghiệp.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Windows Defender SmartScreen hiện cảnh báo đỏ chặn người dùng**: Do file không được ký số hoặc thiếu danh tiếng (reputation) -> Khắc phục: Ký số bằng chứng chỉ EV Code Signing hoặc Azure Trusted Signing.
- **WinGet PR bị từ chối**: Do sai mã băm SHA256 hoặc link tải không cố định -> Khắc phục: Tự động tính toán SHA256 bằng PowerShell `Get-FileHash -Algorithm SHA256` trong CI.

## 6. Step-by-Step Execution Workflow
1. Chuẩn bị file thực thi và các thư viện phụ thuộc (`dist/bin/`).
2. Xây dựng kịch bản đóng gói bộ cài (Inno Setup `.iss` script hoặc WiX `.wxs` template).
3. Biên dịch tạo tệp cài đặt `.exe` hoặc gói hiện đại `.msix`.
4. Thực hiện ký số mã nguồn (Authenticode) bằng công cụ `signtool.exe` hoặc Azure Trusted Signing để tránh cảnh báo SmartScreen.
5. Tạo manifest WinGet chuẩn (`dex.yaml`) mô tả đường link tải và mã băm SHA256 của bộ cài.
6. Kiểm thử cài đặt âm thầm (Silent Installation: `/VERYSILENT /SUPPRESSMSGBOXES`) và gỡ cài đặt sạch sẽ.
7. Viết script PowerShell tự động hóa việc đăng ký Windows Service nếu là ứng dụng nền.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```powershell
# Build and sign script: package-windows.ps1
$ErrorActionPreference = "Stop"
Write-Host "Building Inno Setup installer..."
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\installer.iss

$installerPath = ".\Output\DexSetup-v3.0.0.exe"
Write-Host "Signing executable with Authenticode..."
& signtool.exe sign /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 /a $installerPath

$hash = (Get-FileHash -Path $installerPath -Algorithm SHA256).Hash
Write-Host "Installer ready. SHA256: $hash"
```

### Lệnh xác minh & thực thi:
- Kiểm tra chữ ký số của file thực thi: `signtool verify /pa /v .\dist\setup.exe`
- Tính mã băm SHA256: `Get-FileHash -Path .\dist\setup.exe -Algorithm SHA256`
- Kiểm tra tính hợp lệ của WinGet manifest: `wingetvalidate .\manifests\dex.yaml`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Bộ cài đặt hoàn thành không lỗi và hỗ trợ cài đặt ở chế độ im lặng.
- QG-09: Chữ ký số Authenticode hợp lệ với timestamp được xác thực thành công.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tuyệt đối không lưu private key của chứng chỉ ký số trong mã nguồn Git; sử dụng Hardware Security Module (HSM) hoặc dịch vụ ký số trên đám mây.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Tệp kịch bản bộ cài đặt (`installer.iss` hoặc WiX manifest).
- WinGet package manifest (`manifests/d/dex/v3.0.0/dex.yaml`).
- File bộ cài đặt đã ký số sẵn sàng phân phối.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-windows-packaging**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
