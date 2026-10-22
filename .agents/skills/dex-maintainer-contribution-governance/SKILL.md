---
name: dex-maintainer-contribution-governance
description: Establish open-source maintainer governance, automated CODEOWNERS enforcement, Contributor License Agreements (CLA/DCO), PR review checklists, and branch protection rules. Use when scaling open-source communities, protecting codebase integrity, or formalizing contributor workflows.
---

# dex-maintainer-contribution-governance

## 1. Purpose & Scope
Thiết lập cấu trúc quản trị người duy trì dự án (Maintainer Contribution Governance) và cộng đồng mã nguồn mở; tự động hóa thực thi quyền sở hữu mã nguồn (`.github/CODEOWNERS`), thỏa thuận cấp phép người đóng góp (CLA / Developer Certificate of Origin - DCO), danh mục kiểm tra đánh giá Pull Request và các quy tắc bảo vệ nhánh (Branch Protection Rules); đảm bảo tính toàn vẹn của mã nguồn và tính bền vững của dự án.

## 2. When to Use
- Khi một dự án phần mềm bắt đầu mở rộng cho nhiều kỹ sư hoặc cộng đồng bên ngoài cùng đóng góp mã nguồn.
- Khi cần đảm bảo mọi thay đổi trong các thư mục quan trọng (như bảo mật, thanh toán) bắt buộc phải có sự phê duyệt của kỹ sư trưởng.
- Khi bảo vệ tính pháp lý của mã nguồn bằng cách yêu cầu người đóng góp xác nhận cam kết bản quyền DCO (Signed-off-by).

## 3. When NOT to Use
- Khi dự án cá nhân một người làm không có người đóng góp thứ hai.
- Khi xây dựng kịch bản tự động hóa hạ tầng phần cứng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kho lưu trữ GitHub/GitLab, tệp quy tắc `CODEOWNERS`, cấu hình bot kiểm tra DCO/CLA trong pull request.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Developer Certificate of Origin (DCO):** Cam kết pháp lý đơn giản của người đóng góp (thông qua dòng `Signed-off-by: Name <email>` trong commit message) xác nhận họ tự viết mã nguồn này hoặc có quyền đóng góp.
- **Granular CODEOWNERS Enforcement:** Tự động chỉ định người đánh giá PR dựa trên đường dẫn tệp tin bị thay đổi (ví dụ thư mục `auth/` do nhóm Security duyệt).
- **Strict Branch Protection:** Cấm push trực tiếp vào nhánh `main`, bắt buộc vượt qua 100% CI checks và có tối thiểu 2 lượt phê duyệt (Approve) từ người có thẩm quyền.

## 6. Step-by-Step Execution Workflow
1. Thiết lập tệp `.github/CODEOWNERS` phân công rõ ràng các thư mục chuyên trách cho từng nhóm.
2. Cài đặt GitHub Action kiểm tra cam kết DCO trên 100% các commit của pull request.
3. Khai báo các quy tắc bảo vệ nhánh `main`: cấm force-push, yêu cầu nhánh phải cập nhật mới nhất trước khi merge.
4. Xây dựng biểu mẫu Pull Request Template chuẩn hóa yêu cầu mô tả rõ mục đích, bằng chứng kiểm thử và tài liệu cập nhật.
5. Biên soạn tài liệu hướng dẫn người đóng góp `CONTRIBUTING.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```text
# .github/CODEOWNERS
# Global default owners for everything
*       @nguyenducanhst2022-png

# Security and Auth modules require Lead Security Auditor
/.agents/skills/dex-security*   @nguyenducanhst2022-png/security-team
/integrations/                  @nguyenducanhst2022-png/integration-team

# Core Orchestrator requires Principal Architect approval
/.agents/skills/dex-master-orchestrator/   @nguyenducanhst2022-png/architecture-leads
```

## 8. Anti-Patterns & Common Traps
- Cho phép bất kỳ ai cũng có thể push thẳng vào nhánh `main` mà không cần qua PR hay kiểm thử tự động.
- Tiếp nhận các đóng góp mã nguồn lớn từ người ngoài mà không có xác nhận DCO/CLA, dẫn đến nguy cơ bị kiện bản quyền sau này.
- Để các pull request của cộng đồng bị bỏ quên hàng tháng không ai phản hồi, làm triệt tiêu nhiệt huyết của người đóng góp.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Nhánh `main` được kích hoạt bảo vệ 100%: cấm push trực tiếp và cấm force-push.
- QG-02: 100% các commit từ bên ngoài đều có chữ ký cam kết DCO (`Signed-off-by`).
- QG-03: Tệp `CODEOWNERS` được cấu hình đầy đủ và tự động gán đúng người phụ trách khi mở PR.

## 10. Security & Safety Boundaries
- Ngăn chặn các cuộc tấn công chiếm quyền kho mã nguồn mở bằng cách yêu cầu tài khoản maintainer bắt buộc phải bật xác thực 2 yếu tố (2FA).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Tệp cấu hình sở hữu mã nguồn `.github/CODEOWNERS`.
1. Tài liệu hướng dẫn đóng góp `CONTRIBUTING.md` và PR Template `.github/PULL_REQUEST_TEMPLATE.md`.

## 13. Related & Complementary Skills
- [`dex-git-workflow`](.agents/skills/dex-git-workflow/SKILL.md)
- [`dex-code-review`](.agents/skills/dex-code-review/SKILL.md)
- [`dex-vulnerability-disclosure-workflows`](.agents/skills/dex-vulnerability-disclosure-workflows/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Dự án nguồn mở nhận được nhiều sự quan tâm từ cộng đồng nhưng mã nguồn bắt đầu bị hỗn loạn do các PR merge tùy tiện. Kỹ sư kích hoạt `dex-maintainer-contribution-governance`, thiết lập tệp CODEOWNERS, bật kiểm tra DCO tự động và khóa nhánh `main`, đưa quy trình đóng góp vào khuôn khổ chuyên nghiệp và bảo vệ an toàn cho dự án.
