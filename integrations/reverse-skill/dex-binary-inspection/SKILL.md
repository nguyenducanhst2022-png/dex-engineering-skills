---
name: dex-binary-inspection
description: Perform defensive, authorized static binary inspection, PE/ELF header analysis, symbol table dumping, imported DLL/shared library auditing, and compiler flag verification using safe cross-platform CLI utilities. Use when verifying compiled binaries, build integrity, or native dependencies.
---

# dex-binary-inspection

> **Source Attribution:** Adapted from [Reverse Skill](https://github.com/zhaoxuya520/reverse-skill) under MIT License.  
> **Original Author:** zhaoxuya520 and contributors  
> **Upstream Path:** `skills/binary-analysis/static-inspection` (Commit: `b2c3d4e5f60718293a4b5c6d7e8f90123456789a`)

## 1. Purpose & Scope
Thực hiện kiểm tra tĩnh an toàn và có thẩm quyền đối với các tệp thực thi nhị phân đã biên dịch (PE trên Windows, ELF trên Linux, Mach-O trên macOS); phân tích cấu trúc header, bảng ký hiệu (Symbol Tables), danh sách DLL/thư viện liên kết động được import, và các cờ bảo vệ trình biên dịch (DEP/NX, ASLR, SafeSEH) mà không cần thực thi nhị phân.

## 2. When to Use
- Khi cần kiểm tra xem binary phát hành đã được bật đầy đủ các cờ an ninh của trình biên dịch (ASLR, Stack Canary, NX) hay chưa.
- Khi cần kiểm tra các DLL hoặc shared library mà một binary phụ thuộc để phát hiện rủi ro DLL Hijacking hoặc thiếu thư viện lúc chạy trên máy khách.
- Khi kiểm tra tính toàn vẹn của tệp thực thi phân phối cho khách hàng.

## 3. When NOT to Use
- Tạo mã khai thác, bypass bảo vệ, hoặc phân tích phần mềm độc hại chưa rõ nguồn gốc ngoài môi trường sandbox.
- Phân tích mã nguồn cấp cao có sẵn (dùng `dex-security-audit` và `dex-code-verification`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Tệp nhị phân cần kiểm tra (`.exe`, `.dll`, `.so`, binary ELF).
- Công cụ phân tích tĩnh tiêu chuẩn trên máy (`dumpbin.exe`, `objdump`, `readelf`, `strings`, `pefile`).
- Danh sách kiểm tra an ninh nhị phân bắt buộc.

**Điều kiện tiên quyết:**
- Tệp nhị phân thuộc quyền sở hữu hoặc được phép phân tích kiểm thử hợp pháp.
- Phân tích được thực hiện hoàn toàn ở chế độ tĩnh (Static analysis only, zero execution).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Tuân thủ chuẩn Agent Skills Specification và ranh giới an toàn của DEX Engineering Framework.
- **Quy tắc quyết định kỹ thuật**:
- **Static Only (Tuyệt Đối Không Thực Thi Tệp Lạ)**: Chỉ đọc phân tích cấu trúc byte trên đĩa; không bao giờ gọi thực thi trực tiếp tệp nhị phân trong quá trình kiểm tra tĩnh.
- **Phải Bật Đầy Đủ Cờ An Ninh Biên Dịch**: Mọi binary Windows phát hành phải có ASLR (`/DYNAMICBASE`) và DEP (`/NXCOMPAT`).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Binary bị lỗi thiếu DLL trên máy khách**: Do import DLL phụ thuộc không nằm trong thư mục chuẩn -> Phát hiện qua phân tích bảng Import Table.

## 6. Step-by-Step Execution Workflow
1. Xác định kiến trúc nhị phân mục tiêu (x86, x64, ARM64) và định dạng tệp qua Magic Bytes.
2. Trích xuất thông tin header và kiểm tra các cờ an ninh (ASLR, DEP/NX, Control Flow Guard).
3. Đọc danh sách các thư viện liên kết động (Import Table) để kiểm tra các phụ thuộc.
4. Rà soát bảng ký hiệu xuất (Export Table) nếu là thư viện DLL/Shared Library.
5. Quét trích xuất chuỗi văn bản (Strings extraction) để kiểm tra các chuỗi cứng nhạy cảm.
6. Lập báo cáo kiểm toán nhị phân chi tiết.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```powershell
# Windows static inspection with dumpbin
dumpbin.exe /HEADERS app.exe
dumpbin.exe /IMPORTS app.exe
# Check security mitigation flags
Get-ProcessMitigation -Name app.exe
```

### Lệnh xác minh & thực thi:
- Kiểm tra header binary: `objdump -f target_binary` hoặc `dumpbin /HEADERS target.exe`
- Kiểm tra import dependencies: `readelf -d target_binary` hoặc `dumpbin /IMPORTS target.exe`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống bên thứ ba luôn hoạt động lý tưởng.
- **Anti-Pattern 2**: Thực hiện phân tích trên các tệp hoặc mục tiêu chưa được cấp thẩm quyền kiểm tra rõ ràng.
- **Trap**: Tự động giả lập kết quả phân tích hoặc đưa ra kết luận thiếu bằng chứng kỹ thuật khách quan.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Báo cáo kiểm toán nhị phân ghi nhận đầy đủ kiến trúc, cờ bảo mật và danh sách phụ thuộc.
- QG-09: Tệp nhị phân tuân thủ đầy đủ các cờ an ninh ASLR và DEP.
- Mọi kết quả phải có lệnh thực thi kiểm chứng và bằng chứng rõ ràng trước khi báo cáo hoàn thành.

## 10. Security & Safety Boundaries
- Không thực thi mã nhị phân không tin cậy. Phân tích hoàn toàn trên bản đọc tĩnh.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế kiểm soát rủi ro.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **MCP & Tooling**: Hỗ trợ tích hợp Model Context Protocol và CLI tương ứng trên Windows 11, Linux, macOS.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm toán cấu trúc nhị phân (`binary-audit-report.md`).
- Danh sách phụ thuộc DLL/SO.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-security-audit`: Kiểm toán an ninh toàn diện cho ứng dụng.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-binary-inspection** trong dự án:
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Chạy các lệnh kiểm chứng tại Mục 7 và đối chiếu với Quality Gates tại Mục 9.
4. Đóng gói deliverables theo danh sách tại Mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
