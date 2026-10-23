---
name: dex-supabase-auth-ssr-integration
description: Architect, implement, and verify Supabase Auth integrations in Server-Side Rendering (SSR) frameworks (Next.js App Router, Remix, SvelteKit). Handle secure cookie chunking, PKCE code exchange, and protected route middleware. Use when building SSR web apps with Supabase.
---

# dex-supabase-auth-ssr-integration

## 1. Purpose & Scope
Thiết kế, tích hợp và kiểm chứng cơ chế xác thực Supabase Auth trong các ứng dụng web Server-Side Rendering (SSR) hiện đại (Next.js App Router, Remix, Nuxt, SvelteKit); quản lý an toàn vòng đời Cookie phiên và JWT; triển khai cơ chế Cookie Chunking cho token kích thước lớn; thực thi giao thức PKCE Code Exchange; và bảo vệ các tuyến đường nội bộ (Protected Routes) thông qua Middleware.

## 2. When to Use
- Khi xây dựng ứng dụng web Next.js App Router hoặc Remix sử dụng Supabase làm nhà cung cấp xác thực người dùng.
- Khi gặp sự cố mất phiên làm việc (Session Drop) giữa Server Components và Client Components.
- Khi cần xử lý lỗi giới hạn dung lượng Cookie trình duyệt (Cookie Header Size Exceeded) khi JWT chứa nhiều metadata.

## 3. When NOT to Use
- Khi ứng dụng là Mobile Native (React Native, Flutter, Swift) lưu token vào Secure Store hoặc Keychain.
- Khi hệ thống là Single Page Application thuần túy chạy trên client không có tầng máy chủ SSR.

## 4. Prerequisites & Input Context
- **Thư viện chính thức:** `@supabase/ssr` (phiên bản mới thay thế cho `@supabase/auth-helpers-nextjs` đã cũ).
- **Biến môi trường:** `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`.

## 5. Core Concepts & Taxonomy
- **PKCE (Proof Key for Code Exchange):** Cơ thức trao đổi mã xác thực an toàn trong môi trường web, ngăn chặn tấn công đánh cắp Authorization Code.
- **Cookie Chunking:** Cơ chế tự động chia nhỏ JWT thành nhiều cookie nhỏ (`sb-access-token.0`, `sb-access-token.1`) khi kích thước vượt quá giới hạn 4KB của trình duyệt.
- **Server Component Session Synchronization:** Kỹ thuật đọc phiên làm việc từ Cookie trong Server Components bằng `createServerClient` với các adapter cookie tương ứng.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo tiện ích tạo client Supabase chuẩn hóa cho Server Components, Client Components, Server Actions và Middleware bằng `@supabase/ssr`.
2. Cấu hình middleware (`middleware.ts` trong Next.js) để tự động làm mới (refresh) access token đã hết hạn trước khi yêu cầu đến được Server Component.
3. Xây dựng route handler xác thực OAuth/Magic Link (`/auth/callback/route.ts`) thực thi hàm `exchangeCodeForSession(code)`.
4. Bảo đảm cookie được gán các cờ bảo mật bắt buộc: `HttpOnly`, `Secure`, `SameSite=Lax`.
5. Viết kịch bản kiểm thử E2E xác minh rằng khi người dùng chưa đăng nhập truy cập trang `/dashboard`, middleware sẽ tự động chuyển hướng về `/login`.

## 7. Concrete Examples
### Cấu hình Middleware Next.js làm mới Supabase Session chuẩn tắc:
```typescript
// middleware.ts
import { createServerClient, type CookieOptions } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request: { headers: request.headers } });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({ name, value, ...options });
          response = NextResponse.next({ request: { headers: request.headers } });
          response.cookies.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({ name, value: '', ...options });
          response = NextResponse.next({ request: { headers: request.headers } });
          response.cookies.set({ name, value: '', ...options });
        },
      },
    }
  );

  // Lam moi phien lam viec neu access token da het han
  const { data: { user } } = await supabase.auth.getUser();

  // Chan nguoi dung chua xac thuc vao trang bao ve
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return response;
}
```

## 8. Anti-Patterns & Common Traps
- **Using getSession() in Server Components for Authorization:** Sử dụng `supabase.auth.getSession()` để kiểm tra quyền truy cập trên Server thay vì `supabase.auth.getUser()`. `getSession()` chỉ đọc token từ cookie mà không xác thực chữ ký mật mã với server Supabase, có thể bị giả mạo cookie.
- **Missing Cookie Handlers in Middleware:** Quên cập nhật cookie phản hồi (response cookies) trong middleware, khiến token mới được làm mới không được lưu vào trình duyệt của người dùng.
- **Storing Auth Tokens in LocalStorage on SSR Apps:** Lưu token vào `localStorage` khiến Server Components không thể đọc được thông tin xác thực trong lần render đầu tiên, gây ra hiện tượng Flash of Unauthenticated Content (FOUC).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các kiểm tra phân quyền trên Server Components hoặc Server Actions đều sử dụng `getUser()` thay vì `getSession()`.
- **QG-02**: Cookie xác thực luôn có các cờ `HttpOnly = true`, `Secure = true`, và `SameSite = Lax`.
- **QG-03**: Không có mã nguồn nào lộ lọt `SUPABASE_SERVICE_ROLE_KEY` vào bundle phía client (`NEXT_PUBLIC_`).

## 10. Security & Safety Boundaries
- Chống tấn công CSRF, Token Impersonation, và Man-in-the-Middle đối với các phiên làm việc của người dùng trên web.

## 11. Platform Adapters
- **Frameworks**: Next.js (App Router & Pages Router), Remix, SvelteKit, Nuxt 3, Astro SSR.

## 12. Deliverables & Output Artifacts
- Module khởi tạo Supabase SSR client thống nhất (`lib/supabase/server.ts`, `client.ts`).
- Tệp cấu hình middleware bảo vệ route (`middleware.ts`).
- Route handler xử lý callback PKCE OAuth (`app/auth/callback/route.ts`).

## 13. Related & Complementary Skills
dex-auth-session-lifecycle, dex-supabase-adapter, dex-nextjs-app-router-data-cache

## 14. Realistic Usage Example
```bash
# Kiem tra ma nguon co bi ro ri service role key len client khong
grep -rn "SUPABASE_SERVICE_ROLE_KEY" src/app/

# Chay bo kiem thu E2E quy trinh SSR login va cookie refresh bang Playwright
npx playwright test tests/e2e/auth-ssr.spec.ts
```
