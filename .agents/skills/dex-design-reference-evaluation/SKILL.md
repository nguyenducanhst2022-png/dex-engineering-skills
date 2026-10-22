---
name: dex-design-reference-evaluation
description: Critically analyze visual design references, competitor benchmarks, and design inspiration against product requirements to extract reusable design principles without copyright infringement. Use during early product discovery, UI redesigns, or mood board evaluations.
---

# dex-design-reference-evaluation

## 1. Purpose & Scope
Phân tích, đánh giá có phê phán các nguồn cảm hứng thiết kế, mẫu giao diện đối thủ cạnh tranh và sản phẩm mẫu; chắt lọc các nguyên lý trải nghiệm xuất sắc, mô hình tương tác hiệu quả và quy chuẩn thị giác mà tuyệt đối không sao chép vi phạm bản quyền hay tài sản sở hữu trí tuệ.

## 2. When to Use
- Trong giai đoạn Product Discovery ban đầu hoặc chuẩn bị làm Moodboard cho dự án.
- Khi benchmark trải nghiệm người dùng của các sản phẩm hàng đầu trên thị trường.
- Khi cần giải thích cho stakeholder lý do nên hoặc không nên học tập một mô hình giao diện cụ thể.

## 3. When NOT to Use
- Khi chỉ muốn copy mã nguồn HTML/CSS nguyên mẫu của trang web khác vào dự án.
- Khi hệ thống đã có design system hoàn thiện và chỉ việc áp dụng các component sẵn có.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Ảnh chụp tham khảo, danh sách URL sản phẩm cần benchmark, tiêu chí kinh doanh và giá trị khác biệt của sản phẩm.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Functional Deconstruction:** Bóc tách giao diện thành các lớp độc lập: Layout, Color Palette, Typography, Information Flow.
- **Clean-Room Design Principle:** Tiếp thu ý tưởng giải quyết vấn đề của đối thủ nhưng tự tay thiết kế và lập trình lại toàn bộ từ đầu.
- **Context Appropriateness:** Đánh giá xem giải pháp của đối thủ có thực sự phù hợp với tập người dùng mục tiêu của mình hay không.

## 6. Step-by-Step Execution Workflow
1. Thu thập từ 3 đến 5 mẫu thiết kế xuất sắc trong và ngoài ngành liên quan đến bài toán.
2. Lập ma trận phân tích điểm mạnh, điểm yếu và các cơ hội cải tiến của từng mẫu tham khảo.
3. Bóc tách các pattern hành vi người dùng (User Mental Model) thành công từ các mẫu.
4. Lọc bỏ các yếu tố không phù hợp với nhận diện thương hiệu hoặc tài nguyên kỹ thuật hiện có.
5. Tổng hợp thành tài liệu kiến nghị nguyên lý thiết kế `DESIGN_BENCHMARK_SYNTHESIS.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```markdown
<!-- Design Reference Evaluation Matrix -->
| Reference Product | Layout Pattern | Hierarchy Strengths | Weaknesses / Risks | Applicable Principle for DEX |
| :--- | :--- | :--- | :--- | :--- |
| Product A | Asymmetric Bento | Clear focal hero metric | Heavy scroll on mobile | Adopt 2x2 hero card for stats |
| Product B | Left-hand Rail + Tabs | Excellent deep navigation | High cognitive overhead | Keep 1-level clean sidebar |
```

## 8. Anti-Patterns & Common Traps
- Sao chép nguyên xi giao diện của đối thủ (Pixel-for-pixel cloning) dẫn đến rủi ro pháp lý và đánh mất bản sắc thương hiệu.
- Áp dụng phong cách thiết kế thời thượng (Trend-chasing) nhưng làm hỏng khả năng sử dụng của đối tượng người dùng chính.
- Không đánh giá tính khả thi kỹ thuật khiến thiết kế tham khảo không thể triển khai trên thực tế.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tài liệu đánh giá tham khảo bao gồm tối thiểu 3 sản phẩm đối chuẩn độc lập.
- QG-02: Không chứa tài sản đồ họa, vector logo hoặc mã nguồn độc quyền của bên thứ ba.
- QG-03: Có phần phân tích rõ ràng về tính khác biệt (Differentiation Factor) của sản phẩm nội bộ.

## 10. Security & Safety Boundaries
- Tuân thủ nghiêm ngặt quyền sở hữu trí tuệ, luật thương hiệu và các quy định về bảo vệ bí mật kinh doanh.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo phân tích đối chuẩn `DESIGN_BENCHMARK_SYNTHESIS.md`.
1. Danh mục các nguyên lý tương tác được phê duyệt để áp dụng.

## 13. Related & Complementary Skills
- [`dex-design-brief-synthesis`](.agents/skills/dex-design-brief-synthesis/SKILL.md)
- [`dex-design-system-documentation`](.agents/skills/dex-design-system-documentation/SKILL.md)
- [`dex-ui-ux-pro-max-adapter`](.agents/skills/dex-ui-ux-pro-max-adapter/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Đội ngũ phát triển chuẩn bị làm lại tính năng quản lý giỏ hàng. Kỹ sư kích hoạt `dex-design-reference-evaluation` để phân tích luồng thanh toán của 4 nền tảng e-commerce lớn, nhận diện mẫu accordion một trang là tối ưu nhất và đề xuất triển khai với phong cách tối giản riêng biệt.
