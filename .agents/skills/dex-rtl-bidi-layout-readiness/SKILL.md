---
name: dex-rtl-bidi-layout-readiness
description: Audit, refactor, and automate bidirectional (BiDi) layout mirroring for Right-to-Left (RTL) scripts including Arabic, Hebrew, and Persian. Use when globalizing web and mobile interfaces.
---

# dex-rtl-bidi-layout-readiness

## 1. Purpose & Scope
Kiểm toán, tái cấu trúc và tự động hóa cơ chế phản chiếu giao diện hai chiều (BiDi) cho các hệ chữ viết từ Phải qua Trái (Right-to-Left - RTL) như tiếng Ả Rập, Hebrew và Ba Tư; thay thế các thuộc tính CSS vật lý bằng các thuộc tính logic (CSS Logical Properties).

## 2. When to Use
- Khi mở rộng sản phẩm sang thị trường Trung Đông và Bắc Phi (MENA region).
- Khi giao diện hiển thị các khối nội dung hỗn hợp kết hợp cả chữ tiếng Anh và tiếng Ả Rập.
- Khi phát hiện các biểu tượng điều hướng (như mũi tên quay lại) hoặc lề căn chỉnh bị ngược chiều.

## 3. When NOT to Use
- Khi ứng dụng chỉ phục vụ thị trường bản địa thuần LTR và không có kế hoạch mở rộng thị trường Ả Rập.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Codebase giao diện hiện tại, tài liệu định nghĩa danh sách ngôn ngữ RTL hỗ trợ.
- **Quyền hạn truy cập:** Quyền sửa đổi CSS framework và component templates.

## 5. Core Concepts & Taxonomy
- **CSS Logical Properties:** Thay thế các thuộc tính vật lý cố định (`margin-left`, `padding-right`, `left`, `right`) bằng các thuộc tính logic (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`).
- **Directional Icon Mirroring:** Một số biểu tượng thể hiện hướng di chuyển theo thời gian (như mũi tên back/forward) phải lật ngược trong RTL, trong khi biểu tượng đồng hồ hoặc media controls thì giữ nguyên.
- **BiDi Isolation:** Sử dụng thẻ `<bdi>` hoặc thuộc tính `unicode-bidi: isolate` để cách ly các chuỗi văn bản hỗn hợp (như số điện thoại, mã đơn hàng) khỏi việc bị đảo lộn ký tự.

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ codebase để phát hiện và gắn cờ các thuộc tính CSS định hướng vật lý (`left`, `right`, `margin-left`, `float: left`).
2. Thay thế hàng loạt bằng CSS Logical Properties (`inline-start`, `inline-end`, `inset-inline`).
3. Cấu hình thuộc tính `dir="rtl"` tự động trên thẻ `<html>` dựa trên ngôn ngữ người dùng lựa chọn.
4. Phân loại danh mục biểu tượng: Biểu tượng cần phản chiếu (Back, Forward, Chevron) vs Biểu tượng bất biến (Play, Pause, Download).
5. Bọc các chuỗi dữ liệu động hỗn hợp (tên người dùng kèm số) bằng thẻ `<bdi>` để tránh lỗi vỡ thứ tự hiển thị.
6. Kiểm thử tự động trên cả hai chế độ LTR và RTL bằng công cụ chụp ảnh so sánh trực quan (Visual Regression Testing).

## 7. Concrete Examples
### Chuyển đổi thuộc tính vật lý sang CSS Logical Properties:
```css
/* Trước đây: Phụ thuộc chiều cố định (Lỗi hiển thị trên RTL) */
.user-card {
  margin-left: 16px;
  padding-right: 24px;
  text-align: left;
  border-left: 4px solid var(--color-primary);
}

/* Hiện đại: Sử dụng CSS Logical Properties (Tự động thích ứng cả LTR và RTL) */
.user-card {
  margin-inline-start: 16px;
  padding-inline-end: 24px;
  text-align: start;
  border-inline-start: 4px solid var(--color-primary);
}

/* Phản chiếu biểu tượng điều hướng trong ngữ cảnh RTL */
[dir="rtl"] .icon-directional {
  transform: scaleX(-1);
}
```

## 8. Anti-Patterns & Common Traps
- **Mirroring Everything Blindly:** Lật ngược cả thanh điều khiển media (nút Play/Pause) hoặc đồ thị thời gian theo trục ngang gây bối rối cho người dùng bản địa.
- **Hardcoded Direction Attribute:** Ghi cứng `dir="ltr"` trên các component con làm vô hiệu hóa thuộc tính RTL của trang cha.
- **Phone Number Reversal:** Không cách ly số điện thoại khiến dấu cộng và các chữ số bị đảo vị trí hiển thị trong văn bản tiếng Ả Rập.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 0% thuộc tính CSS vật lý (`margin-left/right`, `left/right`) còn sót lại trong các file style chung.
- **QG-04**: Toàn bộ các trang kiểm thử hiển thị chính xác ở cả hai thuộc tính `dir="ltr"` và `dir="rtl"`.
- **QG-07**: Các chuỗi văn bản hỗn hợp (số, mã đơn, email) hiển thị nguyên vẹn thứ tự ký tự.

## 10. Security & Safety Boundaries
- Tránh các cuộc tấn công Trojan Source bằng cách kiểm tra và loại bỏ các ký tự điều khiển BiDi ẩn (như `U+202E` Right-to-Left Override) trong đầu vào người dùng.

## 11. Platform Adapters
- **Tools**: postcss-logical, stylelint-use-logical-spec, rtlcss, BiDi Checker.

## 12. Deliverables & Output Artifacts
- Bộ quy tắc PostCSS chuyển đổi logical properties.
- Cấu hình Stylelint phát hiện thuộc tính vật lý.
- Báo cáo kiểm thử trực quan trên môi trường RTL.

## 13. Related & Complementary Skills
dex-typography-scale-localization, dex-cross-platform-ui-parity, dex-design-token-migration

## 14. Realistic Usage Example
```powershell
# Chạy Stylelint để phát hiện các thuộc tính vật lý cần chuyển sang Logical Properties
npx stylelint "src/**/*.css" --config .stylelintrc-logical.json

# Tạo tự động phiên bản RTL stylesheet bằng RTLCSS
npx rtlcss src/styles/main.css dist/styles/main.rtl.css
```
