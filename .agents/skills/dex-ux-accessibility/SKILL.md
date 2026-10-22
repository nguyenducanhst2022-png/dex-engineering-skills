---
name: dex-ux-accessibility
description: User experience (UX) engineering, responsive design, accessibility (a11y) compliance (WCAG 2.1 AA), semantic HTML, keyboard navigation, and interface states. Prevents unusable UI, layout shifts, and inaccessible components. Use when building UI components, conducting a11y audits, or optimizing responsive layouts.
---

# DEX UX & Accessibility Engineering

## 1. Purpose & Scope
Hoàn thiện trải nghiệm người dùng (User Experience - UX) và đảm bảo tính tiếp cận (Accessibility - a11y) theo tiêu chuẩn quốc tế WCAG 2.1 AA; đảm bảo giao diện trực quan, rõ ràng, phản hồi tức thì, hiển thị hoàn hảo trên mọi kích thước màn hình (Mobile/Tablet/Desktop) và mọi người dùng (kể cả người khuyết tật sử dụng trình đọc màn hình) đều có thể sử dụng dễ dàng.

Quy trình UX & Accessibility chuẩn:
`Phân tích người dùng → Đánh giá giao diện → Xác định vấn đề → Cải tiến UX/UI → Kiểm tra Responsive → Kiểm tra Accessibility → Kiểm thử người dùng → Ổn định`

Nguyên tắc cốt lõi: **Giao diện phải dễ dùng, rõ ràng, phản hồi nhanh, chạy tốt trên mọi kích thước màn hình và mọi người dùng đều tiếp cận được.**
Ghi nhớ sống còn: **UI đẹp mắt ≠ UX tốt. UX tốt = Dễ hiểu + Phản hồi nhanh + Không gây nhầm lẫn + Ai cũng dùng được.**

## 2. When to Use
- Khi xây dựng mới hoặc cải tiến các thành phần giao diện người dùng (Web UI Components / Mobile screens).
- Khi kiểm tra tính tương thích Responsive trên thiết bị di động (Mobile-first responsive design).
- Khi thực hiện kiểm toán tính tiếp cận a11y (chạy Axe-core, Lighthouse Accessibility audit).
- Khi thiết kế các trạng thái tương tác của giao diện (Empty state, Loading skeleton, Error state, Success feedback).

## 3. When NOT to Use
- Phát triển các dịch vụ backend thuần túy, worker chạy ngầm hoặc CLI tools không có giao diện đồ họa.
- Áp đặt các thư viện UI nặng nề không cần thiết khi chỉ cần vài dòng CSS cơ bản.

## 4. Prerequisites & Input Context
- Bản thiết kế giao diện (Figma / Wireframe) hoặc component mã nguồn HTML/CSS/JS.
- Tiêu chuẩn WCAG 2.1 Level AA (Độ tương phản màu sắc >= 4.5:1, hỗ trợ điều hướng bằng phím Tab).
- Ma trận thiết bị cần hỗ trợ (Mobile 375px, Tablet 768px, Desktop 1280px+).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác kỹ thuật phải có thể kiểm chứng độc lập với số liệu rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Chuẩn Hóa HTML Ngữ Nghĩa (Semantic HTML First)
- Sử dụng đúng các thẻ HTML ngữ nghĩa thay vì lạm dụng `<div>` và `<span>`:
  - Dùng `<button>` cho hành động bấm, dùng `<a>` cho liên kết chuyển trang.
  - Dùng `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>`, `<section>`, `<article>`.
  - Dùng `<label for="...">` liên kết rõ ràng với các trường `<input>`.

### Bước 2: Thiết Kế Đủ 5 Trạng Thái Giao Diện (State Completeness)
- Bắt buộc phải thiết kế đủ 5 trạng thái cho mỗi màn hình/component:
  1. **Ideal State**: Trạng thái hiển thị lý tưởng khi có đầy đủ dữ liệu.
  2. **Loading State**: Trạng thái tải dữ liệu (sử dụng Skeleton loader thay vì spinner giật cục).
  3. **Empty State**: Trạng thái khi chưa có dữ liệu (kèm hướng dẫn hành động đầu tiên: "Chưa có đơn hàng nào. Hãy mua sắm ngay!").
  4. **Error State**: Trạng thái khi có lỗi mạng/lỗi hệ thống (kèm nút "Thử lại").
  5. **Partial State**: Trạng thái dữ liệu dài bất thường hoặc một phần thông tin bị thiếu.

### Bước 3: Đảm Bảo Tính Tương Thích Responsive (Mobile-First)
- Sử dụng CSS Flexbox / Grid và Media Queries linh hoạt.
- Đảm bảo các phần tử cảm ứng (Touch targets) trên thiết bị di động có kích thước tối thiểu `44x44px` hoặc `48x48px` để ngón tay dễ bấm trúng.
- Kiểm tra không xảy ra hiện tượng tràn chữ hoặc thanh cuộn ngang ngoài ý muốn (No horizontal overflow).

### Bước 4: Kiểm Soát Tính Tiếp Cận (WCAG Accessibility Verification)
- **Độ tương phản (Color Contrast)**: Tỷ lệ tương phản giữa chữ và nền tối thiểu là `4.5:1` cho chữ thường và `3:1` cho chữ lớn.
- **Điều hướng bằng bàn phím (Keyboard Navigation)**: Người dùng có thể dùng phím `Tab`, `Enter`, `Space`, `Escape` để duyệt và tương tác với toàn bộ trang mà không cần chuột.
- **Trạng thái Focus (Focus Visible)**: Giữ viền focus rõ ràng (`outline`), không bao giờ dùng `outline: none` mà không có kiểu thay thế.
- **Thuộc tính ARIA (WAI-ARIA)**: Bổ sung `aria-label`, `aria-expanded`, `role` cho các component phức tạp (modal dialog, dropdown).

### Bước 5: Kiểm Thử Tự Động Với Công Cụ a11y (Automated a11y Audit)
- Chạy công cụ kiểm tra tự động:
  ```bash
  npx axe-cli http://localhost:3000
  ```
- Hoặc chạy kiểm tra điểm Lighthouse trong CI: Điểm Accessibility phải đạt >= 90/100.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-ux-accessibility
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-03 (Semantic & a11y Clean)**: Không có cảnh báo lỗi a11y nghiêm trọng từ linter (`eslint-plugin-jsx-a11y` hoặc axe).
- **QG-05 (Responsive Verified)**: Giao diện hiển thị đúng trên cả 3 độ phân giải (Mobile, Tablet, Desktop).
- **QG-08 (No Invisible Focus)**: Các nút bấm và form inputs đều có viền focus hiển thị rõ khi bấm phím Tab.

## 10. Security & Safety Boundaries
- **Cấm Dùng `outline: none` Mù Quáng**: Tuyệt đối không xóa bỏ viền focus mặc định mà không cung cấp viền focus tương phản rõ ràng thay thế.
- **Không Dùng Màu Sắc Làm Kênh Thông Tin Duy Nhất**: Không bao giờ chỉ dùng màu đỏ/xanh để phân biệt đúng/sai (vì người mù màu sẽ không thấy được); luôn bổ sung kèm icon hoặc chữ mô tả.
- **Tránh Giật Layout (Cumulative Layout Shift - CLS)**: Luôn khai báo kích thước `width` và `height` cho hình ảnh để tránh giao diện bị nhảy khi ảnh đang tải.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Mã nguồn giao diện ngữ nghĩa chuẩn HTML5/CSS3.
2. Thiết kế đáp ứng đầy đủ 5 trạng thái (Ideal, Loading, Empty, Error, Partial).
3. Báo cáo kiểm toán a11y đạt điểm số cao (WCAG 2.1 AA compliant).

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-ux-accessibility** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
