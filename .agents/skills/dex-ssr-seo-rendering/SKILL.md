---
name: dex-ssr-seo-rendering
description: Implement Server-Side Rendering (SSR), Static Site Generation (SSG), Incremental Static Regeneration (ISR), dynamic Open Graph metadata, structured JSON-LD, and hydration error eradication. Use when optimizing Next.js/Nuxt applications for search engines or resolving hydration mismatches.
---

# dex-ssr-seo-rendering

## 1. Purpose & Scope
Thiết kế và triển khai các chiến lược hiển thị phía máy chủ (SSR, SSG, ISR) nhằm tối ưu hóa khả năng lập chỉ mục của công cụ tìm kiếm (SEO), chia sẻ mạng xã hội (Open Graph, Twitter Cards), dữ liệu có cấu trúc Schema.org (JSON-LD) và triệt tiêu hoàn toàn các lỗi lệch khớp dữ liệu khi tái tạo giao diện (Hydration Mismatches).

## 2. When to Use
- Khi xây dựng ứng dụng web hướng tới người dùng công cộng bằng Next.js, Nuxt, Astro, hoặc SvelteKit.
- Khi bài viết hoặc sản phẩm chia sẻ lên Facebook/Zalo không hiển thị đúng ảnh thumbnail hoặc tiêu đề.
- Khi console trình duyệt báo lỗi cảnh báo màu đỏ: `Hydration failed because the initial UI does not match what was rendered on the server`.

## 3. When NOT to Use
- Xây dựng hệ thống quản trị nội bộ (Admin Dashboard, B2B Portal) được bảo vệ sau màn hình đăng nhập không cần SEO.
- Xử lý các logic thuần túy ở tầng dữ liệu cơ sở dữ liệu.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Framework render mục tiêu (Next.js App Router / Pages Router, Nuxt 3).
- Danh sách các thẻ meta bắt buộc (Canonical URL, Robots, Open Graph, Twitter Card).
- Cấu trúc dữ liệu có cấu trúc Schema.org (Article, Product, BreadcrumbList).

**Điều kiện tiên quyết:**
- Ứng dụng chạy trên môi trường có hỗ trợ Node.js runtime phía máy chủ hoặc Edge runtime.
- Đã thiết lập các biến môi trường cho domain chính thức (`NEXT_PUBLIC_SITE_URL`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tách Biệt Server Component vs. Client Component**: Mặc định giữ component ở Server Component để không tốn bundle tải về client; chỉ chuyển sang Client Component (`'use client'`) khi cần xử lý tương tác sự kiện (onClick, onChange) hoặc dùng React hooks.
- **Không Gọi API Thừa Thãi**: Áp dụng cơ chế deduplication (React cache hoặc fetch cache) để không gửi 2 request giống hệt nhau trong cùng một chu kỳ render trang.
- **Canonical URL Nhất Quán**: Mọi trang đều phải có thẻ `<link rel='canonical'>` trỏ về URL chuẩn để tránh phạt lỗi trùng lặp nội dung.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗi Hydration Mismatch do múi giờ**: Server ở múi giờ UTC render ngày khác với client ở múi giờ GMT+7 -> Khắc phục: Sử dụng thư viện format ngày đồng bộ hoặc chỉ render phần ngày tháng nhạy cảm múi giờ sau khi mounted (`useEffect`).
- **Trang bị Google bỏ qua không index**: Do file `robots.txt` vô tình chặn `Disallow: /` trên môi trường production -> Khắc phục: Viết test tự động kiểm tra robots.txt trước khi release.

## 6. Step-by-Step Execution Workflow
1. Lựa chọn chiến lược hiển thị phù hợp cho từng trang: SSG cho trang tĩnh ít đổi, ISR cho trang tin tức/sản phẩm có cập nhật định kỳ, SSR cho trang cá nhân hóa cao.
2. Cấu hình hàm sinh metadata động (`generateMetadata` trong Next.js App Router) lấy dữ liệu từ backend.
3. Nhúng dữ liệu có cấu trúc JSON-LD chuẩn Schema.org vào thẻ `<head>`.
4. Rà soát các nguyên nhân gây lỗi Hydration: Sử dụng `typeof window !== 'undefined'`, dùng hàm tạo thời gian `new Date()` không đồng bộ, hoặc cấu trúc HTML lồng sai quy định (như đặt thẻ `<p>` bên trong thẻ `<p>` khác).
5. Kiểm tra sitemap XML và robots.txt tự động sinh.
6. Kiểm tra hiển thị bằng Google Rich Results Test và Facebook Sharing Debugger.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// app/posts/[slug]/page.tsx (Next.js 14)
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPostBySlug(params.slug);
  return {
    title: post.title,
    description: post.summary,
    openGraph: {
      title: post.title,
      description: post.summary,
      images: [{ url: post.coverImage }],
      type: 'article',
    },
    alternates: { canonical: `https://example.com/posts/${params.slug}` }
  };
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra build SSG/SSR: `npm run build`
- Kiểm tra cấu trúc metadata: `curl -s http://localhost:3000/posts/1 | grep -iE '(og:|twitter:|canonical)'`
- Kiểm tra sitemap: `curl -s http://localhost:3000/sitemap.xml`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: 0 lỗi Hydration Mismatch trong console trình duyệt.
- QG-04: Lệnh build production tạo đúng các trang Static / SSG mà không bị lỗi export.
- QG-09: Thẻ meta Open Graph và canonical URL hiển thị chính xác 100%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tuyệt đối không để lộ các biến môi trường nhạy cảm của server trong dữ liệu truyền xuống client qua props của Server Component.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Trang render phía server hoàn thiện (`page.tsx`).
- Cấu hình dynamic metadata và JSON-LD schema.
- File `sitemap.ts` và `robots.ts` chuẩn mực.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-ssr-seo-rendering**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
