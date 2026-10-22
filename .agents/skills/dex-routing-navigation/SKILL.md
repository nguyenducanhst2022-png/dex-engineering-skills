---
name: dex-routing-navigation
description: Architect single-page and multi-page routing, route guards, nested layouts, scroll restoration, code-splitting, and deep linking. Use when designing navigation flows, implementing authentication guards, or optimizing route-level code splitting.
---

# dex-routing-navigation

## 1. Purpose & Scope
Thiết kế và triển khai hệ thống điều hướng (Routing & Navigation) an toàn, mượt mà và tối ưu hiệu năng; quản lý các rào chắn bảo vệ (Route Guards / Protected Routes), phân chia code theo từng trang (Route-level Code Splitting), duy trì vị trí cuộn trang (Scroll Restoration) và hỗ trợ Deep Linking.

## 2. When to Use
- Khi thiết lập cấu trúc điều hướng cho ứng dụng Web SPA (React Router, TanStack Router) hoặc App Router (Next.js, Remix).
- Khi cần bảo vệ các tuyến đường riêng tư yêu cầu đăng nhập hoặc quyền hạn đặc thù (Admin / User roles).
- Khi cần tối ưu tốc độ tải trang đầu bằng cách lazy-load các màn hình ít sử dụng.

## 3. When NOT to Use
- Xây dựng một ứng dụng đơn trang chỉ có một màn hình duy nhất.
- Xử lý điều hướng HTTP request ở tầng server API gateway.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Sơ đồ cấu trúc cây điều hướng (Site Map / Navigation Flow).
- Danh sách các routes công khai (Public) và routes được bảo vệ (Protected).
- Chiến lược phân quyền theo vai trò (RBAC / Roles).

**Điều kiện tiên quyết:**
- Router framework đã được cài đặt và cấu hình ở root ứng dụng.
- Cơ chế xác thực người dùng (Auth Context / Store) có trạng thái `isAuthenticated` và `userRole`.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Code-Splitting Mọi Route Lớn**: Không bao giờ bundle toàn bộ các màn hình vào một file `main.js` duy nhất.
- **Không Lưu Thông Tin Xác Thực Lên URL**: Cấm truyền token đăng nhập hoặc dữ liệu nhạy cảm qua Search Params của URL.
- **Bảo Vệ Đa Tầng**: Route Guard ở frontend chỉ để cải thiện trải nghiệm người dùng; backend API vẫn bắt buộc phải kiểm tra quyền hạn độc lập.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Vòng lặp chuyển hướng vô tận (Infinite Redirect Loop)**: Người dùng chưa đăng nhập vào `/dashboard` bị đẩy sang `/login`, trang login lại tự động chuyển ngược lại -> Khắc phục: Kiểm tra điều kiện dừng rõ ràng và cờ `isLoading` của session.
- **Màn hình trắng xóa khi lazy load lỗi mạng**: Khi người dùng mất mạng lúc chuyển trang -> Khắc phục: Đặt `ErrorBoundary` bọc ngoài `Suspense` kèm nút 'Thử lại'.

## 6. Step-by-Step Execution Workflow
1. Thiết lập cây điều hướng phân cấp (Nested Routes) với các Layouts dùng chung.
2. Bọc các trang nặng trong `React.lazy` và `Suspense` với Loading Skeleton phù hợp.
3. Triển khai Protected Route Wrapper kiểm tra trạng thái đăng nhập; tự động lưu URL chuyển hướng (`redirect_to`).
4. Triển khai Role-based Route Guard từ chối truy cập trái phép và hiển thị trang 403 Forbidden.
5. Cấu hình trang lỗi 404 Not Found và Error Boundary bắt lỗi crash giao diện tại từng route con.
6. Kiểm tra tính năng Scroll Restoration khi người dùng bấm nút Back/Forward trên trình duyệt.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
export const ProtectedRoute: React.FC<{ allowedRoles?: string[] }> = ({ allowedRoles }) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <FullPageSkeleton />;
  if (!isAuthenticated) return <Navigate to='/login' state={{ from: location }} replace />;
  if (allowedRoles && !allowedRoles.includes(user.role)) return <Navigate to='/403' replace />;
  return <Outlet />;
};
```

### Lệnh xác minh & thực thi:
- Chạy tests điều hướng: `npm test -- src/routes/Navigation.spec.tsx`
- Kiểm tra phân tách bundle: `npx vite-bundle-visualizer` hoặc `npm run build`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các route nhạy cảm được bọc trong AuthGuard.
- QG-04: Build sinh ra các chunks độc lập cho từng route (không có chunk nào vượt quá 500KB).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Luôn làm sạch tham số URL trước khi sử dụng để tránh lỗi Open Redirect (chuyển hướng người dùng sang trang web lừa đảo).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File cấu hình router (`AppRoutes.tsx` hoặc `routes.ts`).
- Component bảo vệ tuyến đường (`ProtectedRoute.tsx`).
- File kiểm thử điều hướng (`routes.spec.tsx`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-routing-navigation**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
