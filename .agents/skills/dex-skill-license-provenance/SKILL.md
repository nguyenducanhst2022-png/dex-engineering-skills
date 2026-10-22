---
name: dex-skill-license-provenance
description: Track, audit, and document open-source licenses, author attributions, and exact upstream commit provenance for third-party imported skills. Use to maintain legal compliance and intellectual property integrity.
---

# dex-skill-license-provenance

## 1. Purpose & Scope
Theo dõi, kiểm toán và ghi nhận chứng cứ xuất xứ (Provenance Tracking), bản quyền mã nguồn mở (Open Source Licenses) và sự thừa nhận quyền tác giả (Attribution Requirements) cho các kỹ năng được tích hợp từ các nguồn bên ngoài; bảo đảm tuân thủ pháp lý tuyệt đối về sở hữu trí tuệ, ngăn chặn việc vi phạm các giấy phép lây nhiễm (GPL Copyleft contamination) và duy trì file `THIRD_PARTY_NOTICES.md` minh bạch.

## 2. When to Use
- Tích hợp hoặc tham khảo kỹ năng từ các repository bên thứ ba (Agentic Awesome Skills, Reverse Skill, REA).
- Chuẩn bị phát hành bản phân phối thương mại hoặc mã nguồn mở của bộ kỹ năng.
- Định kỳ rà soát tuân thủ giấy phép phần mềm của tổ chức.

## 3. When NOT to Use
- Không xóa bỏ hoặc chỉnh sửa các thông báo bản quyền (Copyright notices) nguyên bản của tác giả gốc khi nhập skill.
- Không tự tiện gắn giấy phép MIT cho các đoạn mã được lấy từ nguồn có giấy phép hạn chế hơn mà không có sự cho phép.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các nguồn thượng nguồn (Upstream Sources: URL, Commit SHA, License Type).
- File mã nguồn và tài liệu của skill cần nhập.
- Danh mục các giấy phép được phép sử dụng (Permitted Licenses: MIT, Apache 2.0, BSD).
- **Điều kiện tiên quyết**:
- Có quyền truy cập vào thông tin commit gốc của kho lưu trữ thượng nguồn.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Provenance Metadata: Mỗi kỹ năng nhập khẩu bắt buộc phải lưu giữ metadata gồm: URL gốc, Commit SHA chính xác tại thời điểm nhập, Ngày nhập, Giấy phép bản quyền, và Danh sách các thay đổi nội địa (Local Modifications).
- Permissive vs Copyleft Licenses:
  + Permissive (MIT, Apache 2.0, BSD): Cho phép tái sử dụng, chỉnh sửa và đóng gói thương mại với điều kiện giữ nguyên thông báo bản quyền.
  + Copyleft (GPL, AGPL): Yêu cầu bất kỳ sản phẩm phái sinh nào cũng phải mở mã nguồn dưới cùng giấy phép, tiềm ẩn rủi ro lây nhiễm cho toàn bộ dự án.
- Segregated Integration: Các kỹ năng bên thứ ba phải được lưu trữ trong thư mục riêng (`integrations/`) tách biệt với bộ kỹ năng bản địa để tránh nhầm lẫn pháp lý.
- **Quy tắc quyết định kỹ thuật**:
- Chỉ chấp nhận nhập các kỹ năng có giấy phép Permissive (MIT, Apache 2.0, BSD-2/3-Clause).
- Tuyệt đối từ chối nhập các kỹ năng không có giấy phép (Unlicensed / All Rights Reserved) hoặc giấy phép Copyleft mạnh (GPLv3).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Sao chép một skill từ GitHub nhưng không ghi lại commit SHA gốc, khi tác giả cập nhật bản vá bảo mật hoặc đổi giấy phép thì không thể đối soát được nguồn gốc.

## 6. Step-by-Step Execution Workflow
1. Kiểm tra file `LICENSE` tại thư mục gốc và headers bản quyền của từng file trong repository nguồn.
2. Xác định chính xác Commit SHA hiện tại của upstream repository.
3. Ghi nhận thông tin xuất xứ vào file kê khai `manifests/upstream-sources.json`.
4. Trích xuất toàn bộ thông báo bản quyền của tác giả vào file `THIRD_PARTY_NOTICES.md`.
5. Chạy script kiểm toán tự động để đảm bảo 100% kỹ năng ngoại nhập đều có hồ sơ pháp lý đầy đủ.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```json
// manifests/upstream-sources.json - Khai báo nguồn gốc xuất xứ chuẩn mực
{
  "upstream_id": "source-a-aas",
  "name": "Agentic Awesome Skills",
  "repository_url": "https://github.com/sickn33/agentic-awesome-skills",
  "pinned_commit": "7b4e28f192a837c4d5e901a2f6b8c4d3e2a1b9c8",
  "license": "MIT",
  "imported_date": "2026-10-22",
  "target_directory": "integrations/aas",
  "attribution_required": true
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm toán tính đầy đủ của thông báo bản quyền bên thứ ba
python scripts/audit_skills.py --check-licenses
```

## 8. Anti-Patterns & Common Traps
- Tự ý thay đổi tên tác giả gốc thành tên mình trong file tài liệu của skill ngoại nhập.
- Không khóa cố định Commit SHA (Pinned Commit) dẫn đến việc không thể tái lập lại bản build.

## 9. Quality Gates & Acceptance Criteria
- 100% kỹ năng bên thứ ba có hồ sơ xuất xứ kèm commit SHA và giấy phép rõ ràng.
- 0 thành phần nào vi phạm chính sách giấy phép Copyleft bị lọt vào dự án.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi mã nguồn nhập từ bên thứ ba phải được kiểm tra qua quy trình rà soát bảo mật trước khi nhập vào hệ thống.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- File kê khai xuất xứ `manifests/upstream-sources.json`.
- Tài liệu thông báo bản quyền đầy đủ `THIRD_PARTY_NOTICES.md`.

## 13. Related & Complementary Skills
dex-skill-discovery-indexer, dex-skill-security-screening, dex-skill-import-packaging

## 14. Realistic Usage Example
### Tình huống thực tế:
Một tập đoàn tài chính tiến hành thẩm định mã nguồn trước khi mua lại một dự án AI Agent. Nhờ áp dụng quy trình Skill License Provenance ghi lại chính xác từng commit SHA và nguồn gốc giấy phép MIT/Apache 2.0 trong `THIRD_PARTY_NOTICES.md`, dự án đã vượt qua bài kiểm toán pháp lý của các luật sư trong 1 buổi làm việc mà không có bất kỳ tranh chấp nào.
