---
name: dex-perceived-performance-patterns
description: Engineer perceived performance optimization strategies including skeleton screens, optimistic UI updates, staggered micro-transitions, and instant interaction feedback. Use when improving user-facing responsiveness during network latency.
---

# dex-perceived-performance-patterns

## 1. Purpose & Scope
Thiết kế và lập trình các chiến lược tối ưu hóa hiệu năng cảm nhận (Perceived Performance); áp dụng màn hình khung xương (skeleton screens), cập nhật giao diện lạc quan (optimistic UI), hiệu ứng vi chuyển đổi so le và phản hồi xúc giác ngay lập tức để xóa bỏ cảm giác chờ đợi do độ trễ mạng.

## 2. When to Use
- Khi các thao tác mạng (lưu dữ liệu, thích bài viết, gửi tin nhắn) có độ trễ từ 300ms - 2000ms gây gián đoạn trải nghiệm.
- Khi màn hình trắng xuất hiện trong lúc tải dữ liệu ban đầu khiến người dùng nghĩ ứng dụng bị treo.
- Khi cần nâng cao chỉ số Interaction to Next Paint (INP) và Core Web Vitals.

## 3. When NOT to Use
- Khi thao tác mang tính rủi ro cao hoặc không thể đảo ngược (như thanh toán tiền, xóa tài khoản vĩnh viễn) đòi hỏi phải chờ xác nhận từ server.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Luồng tương tác người dùng, API endpoints có độ trễ cao, thư viện quản lý trạng thái (React Query, SWR, Zustand).
- **Quyền hạn truy cập:** Quyền sửa đổi logic tương tác frontend và component loading.

## 5. Core Concepts & Taxonomy
- **Optimistic UI:** Cập nhật giao diện ngay lập tức như thể yêu cầu đã thành công trên máy chủ; tự động khôi phục (rollback) và hiển thị thông báo lỗi nếu API thất bại.
- **Skeleton Screens vs. Spinners:** Màn hình khung xương tạo cảm giác nội dung đang dần hiển thị và giảm thời gian chờ đợi nhận thức so với con trỏ xoay vòng đơn điệu.
- **Immediate Visual Feedback:** Cung cấp phản hồi xúc giác/thị giác trong vòng 50-100ms sau khi người dùng bấm chuột.

## 6. Step-by-Step Execution Workflow
1. Khảo sát các điểm chạm tương tác có độ trễ lớn trong ứng dụng.
2. Thiết kế skeleton screen có cấu trúc hình học khớp chính xác với nội dung thực tế để tránh xô lệch layout (CLS).
3. Triển khai cơ chế Optimistic Updates cho các thao tác like, bookmark, toggle, hoặc gửi bình luận.
4. Cài đặt cơ chế khôi phục trạng thái (rollback) an toàn kèm thông báo Toast khi request gặp lỗi.
5. Áp dụng hiệu ứng xuất hiện so le (staggered animations) nhẹ nhàng cho danh sách nội dung mới tải về.
6. Đo lường chỉ số thời gian tương tác cảm nhận và tỷ lệ người dùng thoát trang do chờ đợi.

## 7. Concrete Examples
### Cập nhật giao diện lạc quan (Optimistic Update) với TanStack Query:
```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function useOptimisticLike(postId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newLikedState: boolean) => api.toggleLike(postId, newLikedState),
    onMutate: async (newLikedState) => {
      // Hủy bỏ các truy vấn đang thực thi để tránh ghi đè dữ liệu lạc quan
      await queryClient.cancelQueries({ queryKey: ['post', postId] });
      const previousPost = queryClient.getQueryData(['post', postId]);

      // Cập nhật ngay lập tức giao diện người dùng
      queryClient.setQueryData(['post', postId], (old: any) => ({
        ...old,
        isLiked: newLikedState,
        likesCount: old.likesCount + (newLikedState ? 1 : -1),
      }));

      return { previousPost };
    },
    onError: (err, newLikedState, context) => {
      // Khôi phục lại trạng thái cũ nếu server báo lỗi
      if (context?.previousPost) {
        queryClient.setQueryData(['post', postId], context.previousPost);
      }
    },
  });
}
```

## 8. Anti-Patterns & Common Traps
- **Skeleton Layout Mismatch:** Kích thước skeleton không khớp với nội dung thực tế làm layout bị nhảy mạnh khi tải xong (gây tăng điểm CLS).
- **Optimistic Financial Transactions:** Tự ý hiển thị trạng thái chuyển tiền thành công trước khi có xác nhận từ cổng thanh toán.
- **Silent Rollback Without Feedback:** Khôi phục trạng thái cũ khi gặp lỗi mà không đưa ra bất kỳ thông báo nào cho người dùng biết thao tác đã thất bại.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Phản hồi thị giác tức thì xuất hiện trong vòng dưới 100ms kể từ khi người dùng click.
- **QG-03**: Cơ chế rollback hoạt động chính xác 100% trong điều kiện mạng giả lập ngoại tuyến (offline).
- **QG-05**: Không làm tăng điểm số CLS (Cumulative Layout Shift giữ ở mức < 0.1).

## 10. Security & Safety Boundaries
- Đảm bảo các dữ liệu hiển thị lạc quan không làm lộ thông tin bảo mật trước khi được server xác thực quyền truy cập.

## 11. Platform Adapters
- **Data Fetching**: TanStack Query, SWR, Apollo Client.
- **Animation**: CSS animations, Framer Motion.

## 12. Deliverables & Output Artifacts
- Component Skeleton Screen khớp layout.
- Hooks xử lý Optimistic UI kèm logic rollback hoàn chỉnh.
- Báo cáo đo lường Core Web Vitals (INP, CLS).

## 13. Related & Complementary Skills
dex-60fps-web-animation, dex-component-state-matrix, dex-high-density-dashboard-layout

## 14. Realistic Usage Example
```powershell
# Kiểm tra chỉ số Interaction to Next Paint (INP) bằng Lighthouse CLI
npx lighthouse http://localhost:3000 --only-categories=performance

# Giả lập nghẽn mạng chậm và kiểm tra cơ chế rollback giao diện
npx playwright test tests/e2e/optimistic-ui.spec.ts
```
