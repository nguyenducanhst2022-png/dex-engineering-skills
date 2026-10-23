---
name: dex-upstream-license-diffing
description: Continuously track, diff, and audit upstream open-source license changes, copyright notices, and patent clauses across imported and integrated skills. Use when preventing copyleft contamination and ensuring legal compliance.
---

# dex-upstream-license-diffing

## 1. Purpose & Scope
Liên tục theo dõi, so sánh sai khác (diffing) và kiểm toán các thay đổi về giấy phép bản quyền mã nguồn mở (Open Source Licenses), thông báo bản quyền và các điều khoản sáng chế từ các nguồn tích hợp thượng nguồn; ngăn ngừa rủi ro lây nhiễm giấy phép Copyleft mạnh và bảo đảm tuân thủ pháp lý 100%.

## 2. When to Use
- Khi tích hợp các kỹ năng hoặc công cụ từ các kho mã nguồn mở bên ngoài (Agentic Awesome Skills, Reverse Skill, REA, UI/UX Pro Max).
- Khi một dự án thượng nguồn bất ngờ thay đổi giấy phép từ giấy phép thông thoáng (MIT, Apache 2.0) sang giấy phép hạn chế thương mại (SSPL, BSL, AGPLv3).
- Khi chuẩn bị phát hành phiên bản thương mại của sản phẩm và cần lập danh mục thông báo bên thứ ba (Third-Party Notices).

## 3. When NOT to Use
- Khi toàn bộ mã nguồn được phát triển nội bộ 100% không sử dụng bất kỳ thành phần mã nguồn mở nào bên ngoài.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh mục các kho mã nguồn thượng nguồn, tệp `THIRD_PARTY_NOTICES.md`, công cụ quét giấy phép (licensee, scancode-toolkit).
- **Quyền hạn truy cập:** Quyền đọc mã nguồn thượng nguồn và cập nhật tài liệu pháp lý của repository.

## 5. Core Concepts & Taxonomy
- **Copyleft Contamination:** Nguy cơ mã nguồn độc quyền của doanh nghiệp bị buộc phải mở mã nguồn công khai do tích hợp các thư viện mang giấy phép GPL/AGPL.
- **License Drift Detection:** Tự động phát hiện khi tác giả thượng nguồn âm thầm thay đổi nội dung file `LICENSE` hoặc bổ sung các điều khoản hạn chế mới.
- **Third-Party Notices Generation:** Tự động tổng hợp danh sách đầy đủ tất cả các bản quyền, giấy phép và liên kết kho mã nguồn gốc để đính kèm trong bản phát hành.

## 6. Step-by-Step Execution Workflow
1. Khảo sát danh sách tất cả các nguồn tích hợp bên thứ ba và lưu trữ mã commit hash gốc.
2. Chạy công cụ quét giấy phép tự động (Licensee hoặc Scancode) trên từng nguồn thượng nguồn.
3. So sánh nội dung giấy phép hiện tại với bản ghi lịch sử để phát hiện thay đổi (Diffing).
4. Gắn cờ cảnh báo đỏ nếu phát hiện sự xuất hiện của các giấy phép không tương thích thương mại (GPLv3, AGPL, SSPL).
5. Tự động sinh tệp tài liệu thông báo bản quyền `THIRD_PARTY_NOTICES.md` chuẩn hóa.
6. Lưu trữ bằng chứng kiểm toán bản quyền phục vụ công tác thẩm định pháp lý (Due Diligence).

## 7. Concrete Examples
### Kịch bản tự động quét và kiểm tra tính tương thích giấy phép trong Python:
```python
import subprocess
import json

COMPATIBLE_LICENSES = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense"]

def audit_upstream_licenses(upstream_dirs: list[str]):
    violations = []
    
    for directory in upstream_dirs:
        # Chay cong cu licensee de nhan dien giay phep
        result = subprocess.run(["licensee", "detect", directory, "--json"], capture_output=True, text=True)
        data = json.loads(result.stdout)
        
        detected_license = data.get("licenses", [{}])[0].get("spdx_id", "UNKNOWN")
        print(f"Thu muc: {directory} | Giay phep nhan dien: {detected_license}")
        
        if detected_license not in COMPATIBLE_LICENSES:
            violations.append({"dir": directory, "license": detected_license})
            
    if violations:
        raise PermissionError(f"CANH BAO PHAP LY: Phat hien giay phep khong tuong thich: {violations}")
        
    print("Kiem toan giay phep thanh cong! 100% nguon tich hop hop le.")
```

## 8. Anti-Patterns & Common Traps
- **Silent Upstream Pulls:** Cập nhật mã nguồn từ repo bên ngoài mà không kiểm tra xem họ có vừa đổi giấy phép bản quyền hay không.
- **Stripping Copyright Headers:** Tự ý xóa bỏ các dòng ghi chú bản quyền gốc của tác giả vi phạm điều khoản của giấy phép MIT/Apache.
- **Mixing AGPL with Proprietary Code:** Đưa mã nguồn mang giấy phép AGPL vào cùng một tiến trình ứng dụng độc quyền.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các thành phần tích hợp bên ngoài đều có giấy phép được phê duyệt (Permissive Licenses).
- **QG-04**: Tệp `THIRD_PARTY_NOTICES.md` được cập nhật đồng bộ phản ánh chính xác các nguồn tích hợp.
- **QG-09**: 0% mã nguồn mang giấy phép Copyleft mạnh (GPL/AGPL) bị trộn lẫn vào native skills.

## 10. Security & Safety Boundaries
- Triệt tiêu hoàn toàn các rủi ro kiện tụng pháp lý và bảo vệ giá trị sở hữu trí tuệ của tổ chức.

## 11. Platform Adapters
- **Tools**: licensee, scancode-toolkit, cargo-deny, license-checker, FOSSA.

## 12. Deliverables & Output Artifacts
- Tệp tài liệu `THIRD_PARTY_NOTICES.md` cập nhật đầy đủ.
- Báo cáo đối chiếu thay đổi giấy phép thượng nguồn.
- Pipeline CI tự động phát hiện vi phạm bản quyền.

## 13. Related & Complementary Skills
dex-skill-catalog-reconciliation, dex-binary-provenance-matching, dex-sbom-binary-correlation

## 14. Realistic Usage Example
```powershell
# Quét giấy phép các tích hợp bằng licensee
licensee detect integrations/dex-api-mocking-virtualization

# Kiểm tra tính toàn vẹn của THIRD_PARTY_NOTICES.md
python scripts/audit_licenses.py
```
