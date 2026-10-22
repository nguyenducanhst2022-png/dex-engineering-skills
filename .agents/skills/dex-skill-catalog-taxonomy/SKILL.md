---
name: dex-skill-catalog-taxonomy
description: Govern multi-tier Agent Skill catalog taxonomies, classifying skills across domain groups (A-AD), capability primitives, operational risk levels, and progressive disclosure scopes. Use when scaling skill libraries past 300+ skills without routing confusion or context bloat.
---

# dex-skill-catalog-taxonomy

## 1. Purpose & Scope
Quản trị hệ thống phân loại danh mục kỹ năng AI Agent đa tầng (Multi-Tier Agent Skill Catalog Taxonomy); phân bổ chuẩn mực 300 kỹ năng trên 30 nhóm nghiệp vụ (Groups A đến AD), phân loại theo nguyên mẫu năng lực (Capability Primitives), mức độ rủi ro vận hành và phạm vi công bố tiệm tiến (Progressive Disclosure); ngăn ngừa hiện tượng quá tải ngữ cảnh và xung đột định tuyến khi kho kỹ năng mở rộng quy mô lớn.

## 2. When to Use
- Khi số lượng kỹ năng trong hệ thống vượt quá 200-300 skills và cần cấu trúc phân tầng khoa học.
- Khi bộ định tuyến Orchestrator bị nhầm lẫn giữa các kỹ năng có tên gọi hoặc phạm vi gần giống nhau.
- Khi cần sinh tự động tài liệu chỉ mục kỹ năng `SKILLS_INDEX.md` và bản đồ định tuyến `ROUTING_MATRIX.md`.

## 3. When NOT to Use
- Khi kho kỹ năng chỉ có một vài kỹ năng cơ bản dưới 10 skills.
- Khi quản lý danh mục sản phẩm hàng hóa kinh doanh.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tập hợp các tệp `SKILL.md` trong `.agents/skills/`, tệp siêu dữ liệu phân loại `manifests/dex-skills.json`, quy tắc đặt tên chuẩn.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Progressive Disclosure:** Không bao giờ nhồi nhét toàn bộ 300 kỹ năng vào lời nhắc của Agent cùng lúc; phân loại thành 30 nhóm tổng quát và chỉ nạp chi tiết các kỹ năng thuộc nhóm nghiệp vụ được kích hoạt.
- **Orthogonal Domain Separation:** Đảm bảo ranh giới giữa các nhóm A-AD là trực giao (không chồng chéo trách nhiệm lên nhau).
- **Hierarchical Skill Addressing:** Mỗi kỹ năng được định danh theo cấp bậc: Group -> Domain -> Specialized Skill ID.

## 6. Step-by-Step Execution Workflow
1. Phân tích toàn bộ kho kỹ năng và đối chiếu với bảng ánh xạ 30 nhóm nghiệp vụ (Groups A đến AD).
2. Gán nhãn phân loại chính xác cho từng kỹ năng vào cơ sở dữ liệu `manifests/dex-skills.json`.
3. Kiểm tra tính cân bằng số lượng (đảm bảo mỗi nhóm có đúng 10 kỹ năng chuyên môn).
4. Tự động sinh tài liệu mục lục phân loại có cấu trúc `SKILLS_INDEX.md`.
5. Xác nhận bộ định tuyến Master Orchestrator có thể tra cứu kỹ năng theo cấu trúc phân tầng mới.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```json
{
  "$schema": "https://dex.dev/schemas/skill-taxonomy.json",
  "taxonomyVersion": "6.0.0",
  "totalGroups": 30,
  "skillsPerGroup": 10,
  "groups": {
    "Group U": {
      "domain": "Visual Design Intelligence",
      "range": [201, 210],
      "riskProfile": "LOW_READ_WRITE"
    },
    "Group X": {
      "domain": "Authorized Reverse Engineering",
      "range": [231, 240],
      "riskProfile": "HIGH_READ_ONLY_AUDIT"
    }
  }
}
```

## 8. Anti-Patterns & Common Traps
- Để danh mục kỹ năng phát triển tự phát không có quy hoạch nhóm, dẫn đến trùng lặp chức năng giữa nhiều kỹ năng.
- Nhồi nhét nguyên văn nội dung của 300 file SKILL.md vào context window làm cạn kiệt bộ nhớ và gây ảo giác cho mô hình.
- Đặt tên kỹ năng mập mờ, chung chung như `dex-helper` hoặc `dex-tools` không thể hiện rõ năng lực chuyên ngành.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Toàn bộ 300 kỹ năng chuyên ngành được phân bổ chính xác tuyệt đối vào 30 nhóm (mỗi nhóm đúng 10 skills).
- QG-02: Không có bất kỳ kỹ năng nào bị mồ côi hoặc không thể tra cứu qua bảng phân loại taxonomy.
- QG-03: Tệp kê khai `manifests/dex-skills.json` vượt qua 100% tiêu chuẩn JSON Schema.

## 10. Security & Safety Boundaries
- Phân loại rõ các kỹ năng có quyền can thiệp hệ thống cao để áp dụng chính sách kiểm duyệt phù hợp trong bộ định tuyến.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bản kê phân loại danh mục máy đọc được `manifests/dex-skills.json`.
1. Tài liệu mục lục phân loại toàn diện `SKILLS_INDEX.md`.

## 13. Related & Complementary Skills
- [`dex-skill-discovery-indexer`](.agents/skills/dex-skill-discovery-indexer/SKILL.md)
- [`dex-skill-reference-graph`](.agents/skills/dex-skill-reference-graph/SKILL.md)
- [`dex-master-orchestrator`](.agents/skills/dex-master-orchestrator/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Hệ thống nâng cấp từ 200 kỹ năng lên 300 kỹ năng. Kỹ sư kích hoạt `dex-skill-catalog-taxonomy`, quy hoạch 10 nhóm nghiệp vụ mới từ Group U đến Group AD, đảm bảo mỗi nhóm có đúng 10 kỹ năng chuyên ngành với ranh giới rõ ràng, giúp Master Orchestrator định tuyến chính xác 100% không bị nhầm lẫn.
