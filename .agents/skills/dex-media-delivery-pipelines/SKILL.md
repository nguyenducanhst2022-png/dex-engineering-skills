---
name: dex-media-delivery-pipelines
description: Engineer modern responsive media pipelines supporting next-gen image formats (AVIF, WebP), adaptive audio, responsive picture elements, CDN image transformations, and blurhash placeholders. Use when optimizing media-heavy web apps, portfolio sites, or e-commerce catalogs.
---

# dex-media-delivery-pipelines

## 1. Purpose & Scope
Thiết kế và triển khai đường ống phân phối đa phương tiện (Media Delivery Pipeline) hiện đại; hỗ trợ các định dạng hình ảnh thế hệ mới (AVIF, WebP), thẻ `<picture>` responsive thông minh, cơ chế chuyển đổi ảnh động qua CDN và chuỗi giữ chỗ làm mờ (Blurhash placeholders) triệt tiêu độ trễ hiển thị.

## 2. When to Use
- Khi ứng dụng web có nhiều hình ảnh khiến dung lượng tải trang vượt quá 3MB.
- Khi chỉ số Largest Contentful Paint (LCP) bị chậm do thời gian tải ảnh banner chính quá lâu.
- Khi xây dựng trang thương mại điện tử hoặc cổng tin tức đa phương tiện.

## 3. When NOT to Use
- Khi ứng dụng chỉ chứa các icon vector SVG nhỏ.
- Khi tối ưu hóa các tệp tài liệu văn bản tĩnh thuần túy.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Hạ tầng lưu trữ hình ảnh (S3, Cloudflare Images), thư viện tối ưu ảnh (Sharp), CDN hỗ trợ chuyển đổi tham số URL.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Modern Format Negotiation:** Ưu tiên AVIF (tiết kiệm thêm 30% dung lượng so với WebP) với fallback tự động về WebP và JPEG.
- **Resolution Switching (`srcset` & `sizes`):** Cung cấp đúng độ phân giải ảnh tương ứng với kích thước màn hình và DPI của thiết bị.
- **Cumulative Layout Shift Elimination:** Luôn khai báo `width` và `height` rõ ràng để trình duyệt đặt chỗ trước tỷ lệ khung hình (Aspect Ratio).

## 6. Step-by-Step Execution Workflow
1. Tự động nén ảnh gốc sang các định dạng AVIF và WebP với mức chất lượng tối ưu (Quality 75-80).
2. Sinh mã chuỗi Blurhash siêu nhẹ (dưới 30 byte) để hiển thị nền mờ trong lúc ảnh nét đang tải về.
3. Bọc hình ảnh trong thẻ `<picture>` với đầy đủ các thẻ `<source type='image/avif'>` và `sizes` chính xác.
4. Thêm thuộc tính `fetchpriority='high'` cho ảnh LCP đầu trang và `loading='lazy'` cho các ảnh phía dưới màn hình cuộn.
5. Kiểm tra chỉ số Core Web Vitals trên PageSpeed Insights.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```html
<!-- High-Performance Responsive Picture Pipeline -->
<picture>
  <source srcset="banner-384.avif 384w, banner-768.avif 768w, banner-1200.avif 1200w"
          type="image/avif" sizes="(max-width: 768px) 100vw, 1200px">
  <source srcset="banner-384.webp 384w, banner-768.webp 768w, banner-1200.webp 1200w"
          type="image/webp" sizes="(max-width: 768px) 100vw, 1200px">
  <img src="banner-768.jpg" width="1200" height="675" alt="Summer Promo"
       fetchpriority="high" decoding="async" class="object-cover w-full h-auto">
</picture>
```

## 8. Anti-Patterns & Common Traps
- Tải một bức ảnh gốc độ phân giải 4000x3000px nặng 8MB rồi dùng CSS co lại thành kích thước hiển thị 300x200px trên điện thoại.
- Dùng `loading='lazy'` cho cả bức ảnh banner chính trên cùng làm chậm chỉ số LCP nghiêm trọng.
- Không khai báo thuộc tính `width` và `height` trên thẻ `<img>` gây giật nảy giao diện khi ảnh tải xong (lỗi CLS).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tổng dung lượng hình ảnh trên trang chủ giảm tối thiểu 60% sau khi áp dụng pipeline nén.
- QG-02: Điểm chỉ số LCP đạt mức 'Good' (<2.5s) trên thiết bị di động kết nối mạng 4G tiêu chuẩn.
- QG-03: Chỉ số CLS (Cumulative Layout Shift) duy trì bằng 0 liên quan đến việc nạp ảnh.

## 10. Security & Safety Boundaries
- Lọc bỏ toàn bộ siêu dữ liệu EXIF nhạy cảm (tọa độ GPS, thông tin máy ảnh) khỏi ảnh tải lên của người dùng trước khi xuất bản ra CDN.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Script tự động nén và tạo srcset hình ảnh `optimize-media.js`.
1. Component React/Vue chuẩn `ResponsiveImage` tích hợp Blurhash.

## 13. Related & Complementary Skills
- [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md)
- [`dex-caching-strategies`](.agents/skills/dex-caching-strategies/SKILL.md)
- [`dex-storage-lifecycle`](.agents/skills/dex-storage-lifecycle/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trang sản phẩm thời trang có tốc độ tải trang chậm do mỗi sản phẩm tải ảnh JPEG 2MB. Sử dụng `dex-media-delivery-pipelines` để tự động chuyển đổi toàn bộ thư viện ảnh sang AVIF/WebP qua CDN, giảm kích thước trung bình xuống 120KB và cải thiện chỉ số LCP từ 5.4s xuống 1.8s.
