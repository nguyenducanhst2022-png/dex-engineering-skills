---
name: dex-typography-scale-localization
description: Engineer scalable, multilingual typography systems supporting diverse script densities, character heights, diacritics, and vertical alignments across Latin, CJK, Arabic, and Indic scripts. Use when building global software interfaces.
---

# dex-typography-scale-localization

## 1. Purpose & Scope
Thiết kế và triển khai thang tỷ lệ typography có khả năng co giãn linh hoạt và bản địa hóa đa ngôn ngữ; xử lý hoàn hảo các đặc thù về mật độ chữ, dấu thanh phụ, chiều cao dòng (line-height) cho các hệ chữ viết khác nhau như Latin, Tiếng Việt, CJK, Ả Rập và Indic.

## 2. When to Use
- Khi mở rộng ứng dụng phục vụ thị trường toàn cầu với các ngôn ngữ có dấu hoặc ký tự phức tạp.
- Khi văn bản tiếng Việt bị cắt ngọn dấu thanh hoặc văn bản tiếng Đức bị tràn khối chứa (overflow).
- Khi cần thiết lập fallback font stack tối ưu hiệu năng hiển thị cho từng ngôn ngữ mục tiêu.

## 3. When NOT to Use
- Khi ứng dụng chỉ phục vụ duy nhất một ngôn ngữ nội bộ và không có kế hoạch quốc tế hóa.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách ngôn ngữ hỗ trợ (locales), font files hoặc webfont providers, bảng phân bổ font metrics.
- **Quyền hạn truy cập:** Quyền sửa đổi cấu hình theme typography và CSS global.

## 5. Core Concepts & Taxonomy
- **Font Metrics Override:** Điều chỉnh `ascent-override`, `descent-override`, và `line-gap-override` trong `@font-face` để triệt tiêu hiện tượng lệch dòng khi tải fallback font.
- **Script Expansion Factor:** Hệ số giãn nở độ dài chuỗi ký tự theo ngôn ngữ (ví dụ: tiếng Đức dài hơn tiếng Anh khoảng 30%, tiếng Phần Lan dài hơn 35%).
- **Diacritic Clearance:** Đảm bảo chiều cao dòng tối thiểu để các dấu thanh ghép tiếng Việt (như ể, ễ, ậ) hoặc dấu nguyên âm Ả Rập không bị chém mất.

## 6. Step-by-Step Execution Workflow
1. Khảo sát danh sách các ký tự đặc biệt và dấu thanh của toàn bộ locale cần hỗ trợ.
2. Thiết lập thang đo kiểu chữ sử dụng đơn vị tương đối `rem` và `clamp()` để đáp ứng hiển thị co giãn linh hoạt.
3. Cấu hình quy tắc `@font-face` kèm thuộc tính `unicode-range` để nạp chính xác subset font cần thiết cho từng ngôn ngữ.
4. Tinh chỉnh `line-height` cơ sở tối thiểu 1.4 - 1.6 cho các hệ chữ có dấu thanh cao (như tiếng Việt, Thái, Ả Rập).
5. Thiết lập cơ chế font fallback thông minh khớp với x-height và cap-height của web font để tránh Cumulative Layout Shift (CLS).
6. Kiểm thử tự động trên nhiều kích thước màn hình và ngôn ngữ giả lập (pseudo-localization) để phát hiện tràn viền.

## 7. Concrete Examples
### Cấu hình CSS @font-face tối ưu hóa metrics và subset tiếng Việt:
```css
/* Web Font chính */
@font-face {
  font-family: 'AppSans';
  src: url('/fonts/app-sans-vietnamese.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9;
}

/* Fallback Font căn chỉnh metrics để triệt tiêu CLS */
@font-face {
  font-family: 'AppSans-Fallback';
  src: local('Arial');
  ascent-override: 95%;
  descent-override: 25%;
  line-gap-override: 0%;
  size-adjust: 102%;
}

:root {
  --font-base: 'AppSans', 'AppSans-Fallback', -apple-system, BlinkMacSystemFont, sans-serif;
  --line-height-body: 1.5; /* Bảo vệ an toàn dấu thanh tiếng Việt */
}
```

## 8. Anti-Patterns & Common Traps
- **Hardcoded Line-Height in Pixels:** Đặt `line-height: 20px` cố định trong khi kích thước chữ là `18px`, khiến các dấu thanh phụ bị cắt ngọn trên trình duyệt.
- **Monolithic CJK Webfont Ingestion:** Nạp toàn bộ bộ font chữ Hán/Nhật/Hàn kích thước 15MB mà không chia cắt subset (dynamic font slicing).
- **Ignoring Text Truncation in Multi-language:** Sử dụng `text-overflow: ellipsis` trên một dòng cho các tiêu đề quan trọng trong giao diện đa ngôn ngữ.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: CLS (Cumulative Layout Shift) nhỏ hơn 0.05 khi chuyển đổi giữa fallback font và web font.
- **QG-03**: 100% các ký tự dấu thanh phụ tiếng Việt và CJK hiển thị đầy đủ, không bị cắt ngọn hoặc chồng đè lên dòng trên.
- **QG-06**: Tỷ lệ font subset tải xuống tiết kiệm tối thiểu 60% băng thông so với file font gốc.

## 10. Security & Safety Boundaries
- Nạp font từ các CDN uy tín có kiểm tra SRI (Subresource Integrity) hoặc tự host font trên cùng domain để ngăn ngừa rò rỉ dữ liệu.

## 11. Platform Adapters
- **Tools**: glyphhanger, fonttools, capsizecss, Font Squirrel Webfont Generator.

## 12. Deliverables & Output Artifacts
- Bảng cấu hình Typography Tokens đa ngôn ngữ.
- File CSS font-face tối ưu metrics chống nhảy layout (CLS).
- Báo cáo kiểm thử hiển thị trên các locale trọng điểm.

## 13. Related & Complementary Skills
dex-fluid-typography-engineering, dex-rtl-bidi-layout-readiness, dex-cross-platform-ui-parity

## 14. Realistic Usage Example
```powershell
# Tạo font subset woff2 chỉ chứa các ký tự cần thiết cho tiếng Việt
npx glyphhanger --subset=*.ttf --whitelist="A-Z,a-z,0-9,ĂÂĐÊÔƠƯăâđêôơư" --formats=woff2

# Kiểm tra Layout Shift bằng Lighthouse CI
npx lighthouserc autorun
```
