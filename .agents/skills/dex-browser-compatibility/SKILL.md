---
name: dex-browser-compatibility
description: Ensure cross-browser CSS and JavaScript compatibility across Chrome, Safari, Firefox, Edge, and iOS WebKit. Use when resolving Safari-specific layout bugs, configuring Browserslist/Autoprefixer, orPolyfilling modern APIs.
---

# dex-browser-compatibility

## 1. Purpose & Scope
Đảm bảo tính tương thích trình duyệt chéo (Cross-Browser Compatibility) trên toàn bộ các trình duyệt phổ biến (Chrome, Safari/WebKit, Firefox, Edge) và các thiết bị di động (iOS Safari, Android Chrome); cấu hình Autoprefixer, Browserslist, xử lý triệt để các lỗi đặc thù của Safari (Safari Bugs), và bổ sung Polyfill cho các API hiện đại.

## 2. When to Use
- Khi giao diện hiển thị hoàn hảo trên Chrome nhưng bị vỡ layout, lệch flexbox hoặc mất gradient trên Safari / iPhone.
- Khi các hàm JavaScript hiện đại (`Array.at()`, `structuredClone`, `Intl`) gây crash trên các trình duyệt cũ hơn.
- Khi chuẩn bị phát hành ứng dụng cho công chúng và cần cam kết hỗ trợ danh mục trình duyệt mục tiêu (Browser Matrix).

## 3. When NOT to Use
- Ứng dụng nội bộ chạy trên một thiết bị kiosk cố định với một trình duyệt chuyên dụng được chỉ định trước.
- Xử lý các logic backend chạy trên môi trường Node.js cố định.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách trình duyệt và phiên bản mục tiêu (ví dụ: `> 0.5%, last 2 versions, not dead, not IE 11`).
- Báo cáo kiểm tra tính năng từ CanIUse.com.
- Các đoạn mã CSS hoặc JS bị lỗi trên trình duyệt mục tiêu.

**Điều kiện tiên quyết:**
- Đã thiết lập file `.browserslistrc` ở thư mục gốc của dự án.
- Môi trường build tích hợp PostCSS kèm plugin `autoprefixer` và Babel / SWC / esbuild transpiler.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Mobile Safari Là Ưu Tiên Hàng Đầu**: Mọi tính năng CSS mới (như Grid, Subgrid, CSS Nesting) phải được đối chiếu với CanIUse trước khi đưa vào mã nguồn sản xuất.
- **Không Dùng User-Agent Sniffing**: Tuyệt đối không phát hiện trình duyệt bằng cách đọc chuỗi `navigator.userAgent`; luôn dùng Feature Detection (`if ('IntersectionObserver' in window)` hoặc `@supports (display: grid)`).
- **Graceful Fallback**: Luôn cung cấp giá trị dự phòng trong CSS (ví dụ: `background: #2563eb; background: color(display-p3 0.1 0.4 0.9);`).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Thanh địa chỉ che mất nút bấm trên iPhone**: Do sử dụng `height: 100vh` -> Khắc phục: Sử dụng `height: 100dvh` (Dynamic Viewport Height) kết hợp với `env(safe-area-inset-bottom)`.
- **Lỗi Date NaN trên Safari**: Do Safari không hỗ trợ chuỗi ngày có dấu gạch ngang dạng `2026-10-22 14:00:00` -> Khắc phục: Chuẩn hóa sang định dạng chuẩn ISO 8601 (`2026-10-22T14:00:00Z`).

## 6. Step-by-Step Execution Workflow
1. Khảo sát tệp người dùng và cấu hình ma trận trình duyệt trong `.browserslistrc`.
2. Cấu hình PostCSS tự động thêm CSS Vendor Prefixes (`-webkit-`, `-moz-`) qua Autoprefixer.
3. Rà soát các lỗi kinh điển của Safari: Lỗi `100vh` trên mobile Safari (sử dụng `100dvh` hoặc CSS env `safe-area-inset`), lỗi flexbox co rút (`flex-shrink: 0`), lỗi date parsing `YYYY-MM-DD` gây Invalid Date.
4. Bổ sung Polyfill cần thiết cho các API web hiện đại (ví dụ: ResizeObserver, IntersectionObserver, Web Animations API).
5. Kiểm thử tự động trên nhiều engine trình duyệt khác nhau (Chromium, WebKit, Firefox) bằng Playwright Matrix.
6. Kiểm tra thủ công trên thiết bị thật (iOS / Android) nếu có.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```css
/* Hỗ trợ an toàn cho thanh tai thỏ và home indicator trên iPhone */
.footer-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding-bottom: env(safe-area-inset-bottom, 16px);
  min-height: 60px;
  min-height: 100dvh;
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra độ bao phủ trình duyệt: `npx browserslist`
- Chạy test trên cả 3 browser engines: `npx playwright test --project=chromium --project=firefox --project=webkit`
- Kiểm tra CSS prefix: `npx postcss src/styles.css --use autoprefixer -d dist/`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: Không có lỗi cú pháp hoặc hàm không hỗ trợ khi build target theo `.browserslistrc`.
- QG-05: Toàn bộ test suite chạy thành công trên cả 3 engine: Chromium, Firefox và WebKit.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Các polyfill nạp vào ứng dụng phải được cài qua npm package đã được kiểm toán bảo mật; không nhúng trực tiếp thẻ `<script>` từ các domain CDN bên thứ ba không có hash SRI (Subresource Integrity).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File cấu hình chuẩn hóa (`.browserslistrc`).
- Cấu hình PostCSS & Autoprefixer (`postcss.config.js`).
- File kiểm thử đa trình duyệt (`playwright.config.ts`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-browser-compatibility**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
