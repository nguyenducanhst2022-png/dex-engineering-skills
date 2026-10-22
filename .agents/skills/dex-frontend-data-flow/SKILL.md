---
name: dex-frontend-data-flow
description: Architect unidirectional frontend state management, server cache synchronization, optimistic UI updates, and normalized client stores. Use when managing client-server state, configuring React Query/Zustand, or resolving frontend race conditions.
---

# dex-frontend-data-flow

## 1. Purpose & Scope
Thiết kế và chuẩn hóa luồng dữ liệu một chiều (Unidirectional Data Flow) trên frontend; phân biệt rạch ròi giữa Server State (dữ liệu từ API cần cache và đồng bộ) và Client State (trạng thái tương tác cục bộ); triển khai cập nhật lạc quan (Optimistic UI) và loại bỏ xung đột race condition.

## 2. When to Use
- Khi ứng dụng frontend có luồng dữ liệu phức tạp giữa nhiều component phân tán.
- Khi cần tích hợp các giải pháp Server State Management như TanStack Query (React Query), SWR, hoặc RTK Query.
- Khi người dùng phàn nàn về tình trạng giao diện hiển thị dữ liệu cũ hoặc giật cục khi bấm nút lưu.

## 3. When NOT to Use
- Trang web tĩnh hoặc form đơn giản chỉ cần `useState` cục bộ.
- Thao tác trên luồng dữ liệu backend hoặc xử lý stream database.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các API endpoints và kiểu dữ liệu trả về.
- Yêu cầu về thời gian cache (Stale Time, Cache Time, Invalidation Triggers).
- Kịch bản cập nhật tức thì (Optimistic updates).

**Điều kiện tiên quyết:**
- Đã thống nhất kiến trúc state: Server Cache vs. Client Global State vs. Local Component State.
- HTTP Client (Axios/Fetch) có interceptor xử lý mã lỗi và authentication token.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Không Sao Chép Server State Vào Local State**: Tránh lưu dữ liệu fetch từ API vào `useState` vì sẽ làm mất khả năng tự động đồng bộ khi cache cập nhật.
- **Single Source of Truth**: Mỗi mẩu dữ liệu chỉ do một nơi duy nhất quản lý.
- **Bắt Buộc Hủy Request Khi Unmount**: Sử dụng `AbortSignal` để tránh rò rỉ bộ nhớ hoặc setState trên unmounted component.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗi hiển thị dữ liệu sai do Race Condition**: Người dùng tìm kiếm từ khóa 'A' rồi đổi sang 'B', nhưng kết quả 'A' trả về sau và ghi đè kết quả 'B' -> Khắc phục: Tự động hủy query trước bằng AbortSignal.
- **Giao diện không cập nhật sau khi tạo mới**: Do quên invalidate query key -> Khắc phục: Quản lý tập trung Query Key Factory.

## 6. Step-by-Step Execution Workflow
1. Phân loại trạng thái: Đưa dữ liệu API sang TanStack Query / SWR, dữ liệu UI toàn cục sang Zustand/Redux.
2. Chuẩn hóa Query Keys có cấu trúc phân cấp (ví dụ: `['posts', 'detail', postId]`).
3. Cấu hình thời gian `staleTime` hợp lý để tránh gọi API trùng lặp.
4. Triển khai Mutator với `onMutate` cập nhật UI tức thời (Optimistic update) và lưu bản snapshot để rollback nếu API lỗi.
5. Tự động vô hiệu hóa cache liên quan sau khi mutation thành công (`queryClient.invalidateQueries`).
6. Viết bài test giả lập kiểm chứng luồng dữ liệu.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// useUpdateTodo.ts
export const useUpdateTodo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateTodoApi,
    onMutate: async (newTodo) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previous = queryClient.getQueryData(['todos']);
      queryClient.setQueryData(['todos'], (old: Todo[] = []) =>
        old.map(t => t.id === newTodo.id ? { ...t, ...newTodo } : t)
      );
      return { previous };
    },
    onError: (err, newTodo, context) => {
      queryClient.setQueryData(['todos'], context?.previous);
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] })
  });
};
```

### Lệnh xác minh & thực thi:
- Chạy tests luồng dữ liệu: `npm test -- src/hooks/usePosts.spec.ts`
- Kiểm tra Network waterfall bằng React Query Devtools trong môi trường dev.

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% Query Keys được định nghĩa có cấu trúc qua Query Key Factory.
- QG-05: Kịch bản Optimistic Update có bài test kiểm tra rollback thành công khi API trả về lỗi 500.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Không lưu thông tin nhạy cảm (mật khẩu người dùng, số thẻ tín dụng) trong Client Cache hoặc LocalStorage không mã hóa.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Custom Hooks quản lý queries và mutations (`useUserOrders.ts`).
- File định nghĩa Query Keys (`queryKeys.ts`).
- Bộ test giả lập MSW (Mock Service Worker).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-frontend-data-flow**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
