---
name: dex-design-system-documentation
description: Author living design system documentation, component anatomies, token tables, interactive storybook examples, and usage do's and don'ts. Use when standardizing design system primitives, onboarding developers, or publishing UI style guides.
---

# dex-design-system-documentation

## 1. Purpose & Scope
Xây dựng tài liệu hệ thống thiết kế sống (Living Design System Documentation); mô tả giải phẫu component (Component Anatomy), bảng chỉ mục design tokens, ví dụ tương tác trực quan (Storybook) và các quy tắc nên/không nên làm (Do's & Don'ts); tạo tiếng nói chung giữa Designer và Developer.

## 2. When to Use
- Khi hoàn thành một component mới hoặc nâng cấp thư viện Design System của tổ chức.
- Khi cần đào tạo (onboarding) các lập trình viên frontend mới gia nhập dự án.
- Khi thiết lập tài liệu hướng dẫn phong cách UI (UI Style Guide) tập trung.

## 3. When NOT to Use
- Khi đang trong giai đoạn thử nghiệm prototype dùng một lần rồi bỏ.
- Khi tài liệu chỉ mô tả logic nghiệp vụ backend không liên quan đến component giao diện.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bộ component code đã hoàn thiện, danh sách props TypeScript, các token màu sắc/khoảng cách được sử dụng.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Component Anatomy:** Bóc tách rõ ràng các thành phần con cấu thành nên component (Icon, Label, Container, Badge).
- **Single Source of Truth:** Tài liệu tự động đồng bộ từ comment mã nguồn hoặc file định nghĩa token.
- **Usage Rules (Do's and Don'ts):** Cung cấp các ví dụ hình ảnh trực quan về cách sử dụng đúng và các lỗi thường gặp.

## 6. Step-by-Step Execution Workflow
1. Vẽ sơ đồ giải phẫu component và liệt kê tất cả các biến thể (Variants: Primary, Secondary, Destructive).
2. Đặc tả bảng thuộc tính TypeScript (Props Table) kèm kiểu dữ liệu, giá trị mặc định và mô tả công dụng.
3. Liệt kê danh sách Design Tokens liên kết với component (CSS variables).
4. Soạn thảo các trường hợp sử dụng chuẩn (Do's) và các trường hợp cấm kỵ (Don'ts).
5. Tích hợp tài liệu vào Storybook hoặc cổng tài liệu nội bộ.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```markdown
# Button Component

## Anatomy
1. **Container**: Chứa toàn bộ phần tử, quy định padding và border-radius.
2. **Icon (Tùy chọn)**: Kích thước cố định 16x16px, căn giữa theo trục dọc.
3. **Label**: Chữ in thường, font-weight 600, không bị ngắt dòng.

## Usage Guidelines
- **Nên (Do)**: Dùng duy nhất một Button variant `primary` trên mỗi nhóm hành động.
- **Không nên (Don't)**: Thay đổi màu nền của button bằng inline-style không qua token.
```

## 8. Anti-Patterns & Common Traps
- Viết tài liệu tĩnh trên file Word/Confluence rồi bỏ quên không cập nhật khi mã nguồn component đã thay đổi.
- Chỉ liệt kê props kỹ thuật mà không giải thích khi nào nên chọn variant nào.
- Thiếu ví dụ code mẫu khiến lập trình viên phải tự đoán cách import và sử dụng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% props công khai đều có mô tả chi tiết và ví dụ minh họa.
- QG-02: Có phần hướng dẫn tiếp cận bàn phím (Keyboard Navigation) và ARIA role tương ứng.
- QG-03: Tài liệu được biên soạn dưới dạng Markdown/MDX lưu trữ cùng mã nguồn.

## 10. Security & Safety Boundaries
- Không đưa các token xác thực thật, thông tin nội bộ mật vào các ví dụ minh họa trong tài liệu công khai.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Tài liệu component chuẩn `Button.doc.md`.
1. File cấu hình Storybook tương tác `Button.stories.tsx`.

## 13. Related & Complementary Skills
- [`dex-design-system-tokens`](.agents/skills/dex-design-system-tokens/SKILL.md)
- [`dex-ui-component-contracts`](.agents/skills/dex-ui-component-contracts/SKILL.md)
- [`dex-documentation-as-code`](.agents/skills/dex-documentation-as-code/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Hoàn thiện component DateRangePicker phức tạp cho Design System. Sử dụng `dex-design-system-documentation` để viết tài liệu MDX hoàn chỉnh, minh họa cấu trúc DOM, bảng 14 props, ma trận token màu và hướng dẫn sử dụng phím tắt bàn phím cho toàn bộ công ty.
