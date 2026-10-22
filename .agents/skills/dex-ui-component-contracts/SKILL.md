---
name: dex-ui-component-contracts
description: Define and enforce strict UI component contracts, TypeScript props interfaces, component state boundaries, and accessible slots. Use when architecting UI components, establishing design system primitives, or preventing component regressions.
---

# dex-ui-component-contracts

## 1. Purpose & Scope
Thiết lập và kiểm soát các giao ước hợp đồng (Component Contracts) chặt chẽ cho các thành phần giao diện người dùng (UI Components), bao gồm giao diện thuộc tính (Props interface), kiểu dữ liệu sự kiện (Event emitters/callbacks), ranh giới trạng thái (State boundaries) và các điểm gắn nội dung (Slots/Children), đảm bảo component có thể tái sử dụng tối đa và không bị gãy khi nâng cấp.

## 2. When to Use
- Khi thiết kế hoặc tái cấu trúc các component dùng chung (Design System Primitives, Buttons, Modals, Tables, Forms).
- Khi cần chuẩn hóa giao diện Props và Types cho các component trong dự án React, Vue, hoặc Svelte.
- Khi phát hiện hiện tượng prop-drilling hoặc component nhận quá nhiều props không liên quan (Component Bloat).

## 3. When NOT to Use
- Xây dựng các trang tĩnh hiển thị nội dung một lần không có tính tái sử dụng.
- Xử lý các logic nghiệp vụ thuần túy ở tầng dữ liệu backend hoặc database.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bản đặc tả thiết kế (Figma / UI Specs).
- Framework UI mục tiêu (React / Vue / Svelte / Angular) và phiên bản TypeScript.
- Danh sách các biến thể giao diện (Variants: size, color, disabled, loading, active).

**Điều kiện tiên quyết:**
- TypeScript được cấu hình ở chế độ `strict: true`.
- Đã thiết lập thư viện kiểm thử component (React Testing Library, Vitest, hoặc Playwright Component Test).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tối giản Props**: Một component không nên nhận quá 10 props; nếu vượt quá, hãy cân nhắc áp dụng Compound Components Pattern.
- **Không Hardcode CSS Clashes**: Luôn cho phép truyền `className` hoặc `style` phụ trợ nhưng phải kiểm soát xung đột qua công cụ như `tailwind-merge` hoặc `clsx`.
- **Bất biến Props**: Props là bất biến (Read-only); tuyệt đối không mutate props trực tiếp bên trong component con.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Gãy giao diện khi truyền props thiếu**: Component crash vì `props.data` bị undefined -> Khắc phục: Bổ sung default props, optional chaining (`props.data?.title`), và kiểu dữ liệu strict.
- **Component re-render vô tận**: Do truyền hàm callback inline hoặc object mới ở mỗi render -> Khắc phục: Sử dụng `useCallback`, `useMemo` hoặc tách ranh giới state.

## 6. Step-by-Step Execution Workflow
1. Khảo sát yêu cầu hiển thị và các trạng thái biến thể của component.
2. Định nghĩa TypeScript Props Interface rõ ràng với JSDoc giải thích từng thuộc tính.
3. Phân biệt rành mạch giữa Controlled Props (do cha quản lý) và Uncontrolled Props (nội bộ component quản lý).
4. Thiết lập giá trị mặc định an toàn cho tất cả optional props.
5. Tách biệt hoàn toàn Presentation Layer (hiển thị) khỏi Business Data Fetching Logic.
6. Kiểm thử tính toàn vẹn của hợp đồng Props và các sự kiện callback.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// Button.types.ts
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
}

// Button.tsx
export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  children,
  disabled,
  className,
  ...rest
}) => (
  <button
    disabled={disabled || isLoading}
    className={cn('btn', `btn-${variant}`, `btn-${size}`, className)}
    {...rest}
  >
    {isLoading ? <Spinner size={size} /> : leftIcon}
    <span>{children}</span>
  </button>
);
```

### Lệnh xác minh & thực thi:
- Kiểm tra kiểu dữ liệu tĩnh: `npm run type-check` hoặc `tsc --noEmit`
- Chạy component unit tests: `npm test -- src/components/Button/Button.spec.tsx`
- Chạy Storybook test runner nếu có: `npm run test-storybook`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% Props có kiểu dữ liệu TypeScript tường minh, không sử dụng `any`.
- QG-03: Không có warning từ linter về thiếu key hoặc vi phạm react-hooks rules.
- QG-05: Đạt 100% PASS cho các kịch bản render với props đầy đủ, props tối thiểu và props biên.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Mọi chuỗi ký tự hiển thị từ props người dùng phải được escape chống XSS.
- Cấm render HTML thô qua `dangerouslySetInnerHTML` trừ khi đã được làm sạch qua DOMPurify.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File định nghĩa Component (`Button.tsx`) kèm Interface (`Button.types.ts`).
- File kiểm thử hợp đồng (`Button.spec.tsx`).
- File tài liệu hoặc Storybook story (`Button.stories.tsx`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-ui-component-contracts**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
