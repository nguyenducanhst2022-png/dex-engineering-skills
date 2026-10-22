---
name: dex-forms-and-validation
description: Build accessible, performant frontend forms with schema-based validation (Zod/Yup), controlled/uncontrolled inputs, dirty state tracking, and inline error feedback. Use when implementing user input forms, checkout flows, or complex form validation.
---

# dex-forms-and-validation

## 1. Purpose & Scope
Xây dựng các biểu mẫu nhập liệu (Forms) hiệu năng cao, chuẩn tiếp cận (Accessible), không gây giật lag khi gõ phím; tích hợp xác thực dữ liệu chặt chẽ bằng Schema-driven validation (Zod / Yup / Valibot) đồng bộ giữa client và server.

## 2. When to Use
- Khi xây dựng các màn hình Đăng ký, Đăng nhập, Checkout giỏ hàng, hoặc biểu mẫu cấu hình phức tạp.
- Khi biểu mẫu bị giật lag do render lại toàn bộ component mỗi lần người dùng gõ một ký tự.
- Khi cần xử lý validation phức tạp: trường phụ thuộc lẫn nhau, validate bất đồng bộ (check email tồn tại).

## 3. When NOT to Use
- Nút bấm hoặc thanh tìm kiếm đơn giản chỉ có 1 ô input duy nhất.
- Xác thực dữ liệu ở tầng backend controller (dùng `dex-api-engineering`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các trường dữ liệu và ràng buộc validation (độ dài, regex, kiểu dữ liệu).
- Thư viện quản lý form mục tiêu (React Hook Form, Formik, TanStack Form).
- Schema validation engine (Zod).

**Điều kiện tiên quyết:**
- Đã cài đặt thư viện quản lý form không gây render thừa (khuyến nghị React Hook Form).
- Đã thiết lập thông điệp báo lỗi đa ngôn ngữ hoặc thông điệp thân thiện với người dùng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Uncontrolled Inputs Ưu Tiên**: Ưu tiên sử dụng React Hook Form với uncontrolled inputs để đạt 60fps khi người dùng gõ phím.
- **Validation Thời Điểm Hợp Lý**: Validate khi blur (`mode: 'onBlur'`) hoặc khi submit; tránh validate gắt gao ngay khi người dùng vừa gõ ký tự đầu tiên (`onChange`).
- **Đồng Bộ Schema**: Chia sẻ chung Zod schema giữa frontend và backend nếu dùng TypeScript fullstack.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Form submit 2 lần gây nhân đôi đơn hàng**: Do người dùng click nhanh liên tiếp -> Khắc phục: Khóa nút bấm khi `isSubmitting = true`.
- **Mất dữ liệu khi người dùng vô tình reload**: Form dài chưa lưu nháp -> Khắc phục: Bổ sung cảnh báo `beforeunload` hoặc tự động lưu nháp vào sessionStorage.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa Zod Schema cho toàn bộ biểu mẫu và suy ra TypeScript type (`z.infer<typeof schema>`).
2. Khởi tạo form handler với `useForm` kèm resolver `zodResolver(schema)`.
3. Kết nối các input bằng `register` hoặc `Controller` đối với các custom UI components.
4. Thiết lập theo dõi trạng thái: `isDirty`, `isValid`, `isSubmitting`, `errors`.
5. Hiển thị thông báo lỗi ngay dưới từng ô input kèm thuộc tính `aria-invalid` và `aria-describedby`.
6. Xử lý submit an toàn: disable nút bấm khi đang gửi để chống bấm 2 lần (Double Submit).

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
const RegisterSchema = z.object({
  email: z.string().email('Email không đúng định dạng'),
  password: z.string().min(8, 'Mật khẩu tối thiểu 8 ký tự'),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: 'Mật khẩu xác nhận không khớp',
  path: ['confirmPassword']
});
```

### Lệnh xác minh & thực thi:
- Chạy bài kiểm thử tương tác form: `npm test -- src/forms/CheckoutForm.spec.tsx`
- Kiểm tra typecheck của form values: `npm run type-check`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: Form schema kiểm tra đầy đủ cả trường hợp hợp lệ và không hợp lệ.
- QG-05: Test case kiểm tra form submit thành công khi điền đúng và hiển thị đúng lỗi khi điền sai.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tự động xóa (clear) các trường mật khẩu nhạy cảm khỏi bộ nhớ khi unmount component.
- Luôn bật cờ `autocomplete` đúng chuẩn (ví dụ `current-password`, `new-password`, `one-time-code`).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File schema validation (`checkoutSchema.ts`).
- File component biểu mẫu (`CheckoutForm.tsx`).
- File unit/integration test (`CheckoutForm.spec.tsx`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-forms-and-validation**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
