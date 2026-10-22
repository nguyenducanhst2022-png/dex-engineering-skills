---
name: dex-skill-retirement-governance
description: Govern the graceful deprecation, sunsetting, and archival lifecycle of obsolete Agent Skills, decoupling downstream dependencies, redirecting semantic intents, and maintaining historical provenance. Use when retiring legacy skills without breaking existing workflows.
---

# dex-skill-retirement-governance

## 1. Purpose & Scope
Quản trị toàn bộ vòng đời bãi bỏ, ngừng hỗ trợ và lưu trữ (Deprecation, Sunsetting & Archival Lifecycle) cho các kỹ năng AI Agent đã lỗi thời; tách rời an toàn các phụ thuộc hạ nguồn, tự động chuyển hướng ý định ngữ nghĩa sang kỹ năng thay thế hiện đại hơn và duy trì sổ cái nguồn gốc lịch sử; đảm bảo việc loại bỏ kỹ năng cũ diễn ra êm đẹp không làm vỡ các quy trình tự động hóa sẵn có.

## 2. When to Use
- Khi một kỹ năng cũ đã được thay thế hoàn toàn bởi một kỹ năng mới mạnh mẽ hơn (ví dụ: chuyển từ kỹ năng MV2 sang MV3).
- Khi một công cụ hoặc API bên thứ ba mà kỹ năng dựa vào đã bị nhà cung cấp khai tử vĩnh viễn.
- Khi tinh gọn danh mục kỹ năng để loại bỏ các kỹ năng trùng lặp hoặc không còn giá trị thực tế.

## 3. When NOT to Use
- Khi kỹ năng vẫn đang được sử dụng tích cực trong các quy trình quan trọng.
- Khi chỉ tạm thời vô hiệu hóa kỹ năng trong một khoảng thời gian ngắn để bảo trì.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kỹ năng thay thế đã sẵn sàng và được kiểm chứng, danh sách các kỹ năng phụ thuộc, chính sách thông báo lỗi thời (Sunsetting Policy).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Graceful Deprecation Phases:** Giai đoạn 1: Thông báo lỗi thời (Deprecated Warning) kèm gợi ý kỹ năng mới -> Giai đoạn 2: Ngừng hỗ trợ (Sunsetting) -> Giai đoạn 3: Lưu trữ lịch sử (Archived).
- **Intent Redirection:** Khi người dùng hoặc Agent yêu cầu kỹ năng cũ đã bị bãi bỏ, bộ định tuyến tự động chuyển hướng sang kỹ năng thay thế mới kèm thông báo giải thích.
- **Historical Provenance Preservation:** Không xóa vĩnh viễn mã nguồn kỹ năng cũ mà di chuyển vào thư mục lưu trữ `archive/` để phục vụ tra cứu lịch sử.

## 6. Step-by-Step Execution Workflow
1. Đánh dấu trạng thái `status: deprecated` và trường `superseded_by: new-skill-id` trong frontmatter của kỹ năng.
2. Cập nhật Master Orchestrator để tự động chuyển hướng các lệnh gọi kỹ năng cũ sang kỹ năng mới.
3. Rà soát và cập nhật toàn bộ các kỹ năng khác đang liên kết tới kỹ năng cũ trong Mục 13.
4. Duy trì giai đoạn thông báo lỗi thời trong tối thiểu 30 ngày trước khi chính thức lưu trữ.
5. Di dời thư mục kỹ năng vào kho lưu trữ lịch sử và cập nhật `SKILLS_INDEX.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```yaml
# Deprecated Skill Frontmatter Header
---
name: dex-legacy-manifest-v2
description: (DEPRECATED) Legacy Manifest V2 browser extension skill. Superseded by dex-browser-extension-mv3.
status: deprecated
deprecated_at: "2026-10-22"
superseded_by: dex-browser-extension-mv3
---

> [!WARNING]
> Kỹ năng này đã chính thức ngừng hỗ trợ (Deprecated). 
> Vui lòng sử dụng kỹ năng thay thế hiện đại hơn: [`dex-browser-extension-mv3`](.agents/skills/dex-browser-extension-mv3/SKILL.md).
```

## 8. Anti-Patterns & Common Traps
- Xóa bỏ đột ngột một kỹ năng khỏi kho mà không có thông báo trước, làm sập toàn bộ các kịch bản tự động hóa đang gọi kỹ năng đó.
- Bãi bỏ kỹ năng cũ khi chưa có kỹ năng mới sẵn sàng thay thế hoàn chỉnh.
- Không chuyển hướng ý định trong bộ định tuyến khiến người dùng nhận được thông báo lỗi không tìm thấy kỹ năng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các kỹ năng bãi bỏ đều có trường chỉ định kỹ năng thay thế `superseded_by` hợp lệ.
- QG-02: Bộ định tuyến tự động chuyển hướng thành công các yêu cầu kỹ năng cũ sang kỹ năng mới đạt tỷ lệ 100%.
- QG-03: Không còn bất kỳ kỹ năng đang hoạt động nào phụ thuộc vào kỹ năng đã bãi bỏ.

## 10. Security & Safety Boundaries
- Ngăn chặn việc kẻ xấu khai thác các kỹ năng cũ chứa mã lỗi thời bằng cách vô hiệu hóa hoàn toàn quyền thực thi của các kỹ năng trong kho lưu trữ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Chính sách bãi bỏ và chuyển hướng kỹ năng `SKILL_RETIREMENT_POLICY.md`.
1. Kho lưu trữ kỹ năng lịch sử `archive/legacy-skills/`.

## 13. Related & Complementary Skills
- [`dex-skill-upgrade-migrations`](.agents/skills/dex-skill-upgrade-migrations/SKILL.md)
- [`dex-skill-catalog-taxonomy`](.agents/skills/dex-skill-catalog-taxonomy/SKILL.md)
- [`dex-master-orchestrator`](.agents/skills/dex-master-orchestrator/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
DEX Framework chuẩn hóa lên v6.0 và cần bãi bỏ các kỹ năng thử nghiệm cũ. Kỹ sư kích hoạt `dex-skill-retirement-governance`, đánh dấu deprecated cho 3 kỹ năng cũ, cấu hình Master Orchestrator tự động chuyển hướng sang các kỹ năng Group W mới, di dời mã cũ vào archive, giúp toàn bộ hệ sinh thái chuyển mình sang phiên bản mới êm đẹp mà không có bất kỳ lỗi gián đoạn nào.
