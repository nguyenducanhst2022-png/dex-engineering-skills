---
name: dex-frontend-performance
description: Profile and optimize Core Web Vitals (LCP, FID/INP, CLS), JavaScript bundle size, image assets, DOM size, and client-side rendering bottlenecks. Use when diagnosing slow page loads, poor Lighthouse scores, or sluggish frontend interactions.
---

# dex-frontend-performance

## 1. Purpose & Scope
Đo lường, phân tích và tối ưu hóa hiệu năng giao diện người dùng theo các chỉ số Core Web Vitals chuẩn mực của Google (LCP, INP, CLS); giảm kích thước JavaScript bundle, tối ưu hóa hình ảnh, giảm kích thước cây DOM và loại bỏ các tác vụ chặn luồng chính (Main Thread Blocking).

## 2. When to Use
- Khi điểm số Google Lighthouse dưới 90 hoặc chỉ số Core Web Vitals báo đỏ.
- Khi dung lượng bundle của ứng dụng web phình to vượt quá 1MB.
- Khi người dùng phàn nàn về tình trạng đơ giật khi thao tác (Laggy interactions / High INP).

## 3. When NOT to Use
- Tối ưu hóa vi mô code thuật toán trong các hàm chỉ chạy một lần lúc khởi động.
- Tối ưu hóa truy vấn cơ sở dữ liệu backend (dùng `dex-database-query-plans`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Báo cáo chỉ số Core Web Vitals từ Chrome DevTools Performance hoặc Web Vitals extension.
- Bản đồ phân tích bundle (Webpack Bundle Analyzer / Rollup Visualizer).
- Danh sách các tài nguyên tĩnh nặng (ảnh, font chữ, scripts bên thứ ba).

**Điều kiện tiên quyết:**
- Có thể build phiên bản production cục bộ để đo lường số liệu thực tế.
- Có công cụ đo lường tự động (Lighthouse CI hoặc WebPageTest).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Nguyên Tắc Dưới 200KB Gzip**: Cố gắng giữ initial bundle dưới 200KB gzipped cho trang landing.
- **Không Chặn Render**: Scripts phân tích bên thứ ba (Google Analytics, Hotjar) bắt buộc phải gắn `defer` hoặc nạp qua Web Worker (Partytown).
- **Không Gây Nhảy Layout**: Tuyệt đối không chèn nội dung động lên phía trên nội dung người dùng đang đọc.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Tối ưu hình ảnh nhưng ảnh bị mờ hoặc méo tỷ lệ**: Do dùng `width/height` không đúng tỷ lệ gốc -> Khắc phục: Dùng thuộc tính CSS `aspect-ratio` và `object-fit: cover`.
- **Thực hiện Dynamic Import nhưng làm chậm lúc người dùng bấm nút**: -> Khắc phục: Sử dụng prefetching khi người dùng hover chuột vào nút bấm.

## 6. Step-by-Step Execution Workflow
1. Đo lường hiện trạng (Baseline): Ghi nhận LCP (Largest Contentful Paint), INP (Interaction to Next Paint), CLS (Cumulative Layout Shift).
2. Tối ưu LCP (< 2.5s): Nén ảnh WebP/AVIF, đặt `fetchpriority='high'` cho ảnh hero, tự lưu trữ (self-host) font chữ.
3. Tối ưu CLS (< 0.1): Đặt kích thước cố định `width`/`height` cho tất cả ảnh và video; đặt min-height cho quảng cáo/banner động.
4. Tối ưu INP (< 200ms): Chia nhỏ các tác vụ dài (Long Tasks > 50ms) bằng `scheduler.yield()` hoặc Web Workers.
5. Tối ưu Bundle Size: Áp dụng Dynamic Import cho các thư viện nặng (moment.js -> date-fns; lodash -> lodash-es tree-shaking).
6. Đo lường lại và so sánh với baseline ban đầu.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```html
<!-- Tối ưu LCP & CLS chuẩn mực -->
<link rel='preload' as='image' href='/hero.webp' fetchpriority='high' />
<img 
  src='/hero.webp' 
  alt='Sản phẩm nổi bật' 
  width='1200' 
  height='600' 
  fetchpriority='high' 
  decoding='async'
  style='aspect-ratio: 2 / 1; width: 100%; height: auto;'
/>
```

### Lệnh xác minh & thực thi:
- Phân tích kích thước bundle: `npx vite-bundle-visualizer` hoặc `npm run analyze`
- Chạy kiểm tra Lighthouse tự động: `npx lhci autorun`
- Đo chỉ số web-vitals từ console: `npx web-vitals-cli http://localhost:3000`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: Điểm Lighthouse Performance đạt tối thiểu 90/100 trên thiết bị Mobile.
- QG-10: Có bảng số liệu Trước/Sau rõ ràng chứng minh LCP < 2.5s, CLS < 0.1, INP < 200ms.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tối ưu tải nhanh không được phép bỏ qua các header bảo mật quan trọng như CSP (Content Security Policy).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Bảng báo cáo hiệu năng Trước và Sau tối ưu (Before/After Web Vitals).
- Bản tối ưu mã nguồn cấu hình build và assets.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-frontend-performance**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
