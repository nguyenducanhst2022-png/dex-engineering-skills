---
name: dex-typescript-type-safety
description: Architect strict, bulletproof TypeScript systems leveraging branded types, template literals, conditional types, and runtime schema boundaries (Zod) without resorting to 'any'. Use when building high-integrity TypeScript codebases.
---

# dex-typescript-type-safety

## 1. Purpose & Scope
Thiết kế, xây dựng và nâng cao tính an toàn kiểu dữ liệu trong TypeScript (Type Safety); khai thác triệt để các tính năng nâng cao (Branded/Nominal Types, Template Literal Types, Conditional Types, Discriminated Unions) kết hợp với các bộ kiểm tra ranh giới runtime (Zod/Valibot), loại bỏ hoàn toàn việc lạm dụng kiểu `any` và ép kiểu không an toàn (`as`).

## 2. When to Use
- Codebase TypeScript tràn ngập kiểu `any`, `unknown` hoặc ép kiểu bừa bãi `as unknown as Type`.
- Xảy ra lỗi runtime `TypeError: Cannot read property of undefined` dù code đã compile thành công.
- Cần bảo đảm tính toàn vẹn của dữ liệu nhận được từ bên ngoài (API, Database, User Input).

## 3. When NOT to Use
- Không thiết kế hệ thống kiểu quá phức tạp đến mức làm tê liệt trình biên dịch TypeScript (Type instantiation is excessively deep).
- Không dùng TypeScript type checker để thay thế cho việc xác thực dữ liệu khi runtime.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File cấu hình `tsconfig.json` của dự án.
- Lược đồ dữ liệu nghiệp vụ và các interface hiện có.
- Thư viện xác thực runtime (Zod, Valibot, Typia).
- **Điều kiện tiên quyết**:
- `tsconfig.json` đã bật cờ `"strict": true` và `"noImplicitAny": true`.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Branded Types (Nominal Typing): Phân biệt hai chuỗi ký tự có kiểu dữ liệu khác nhau về mặt ngữ nghĩa (ví dụ: `UserId` không thể vô tình gán nhầm cho `OrderId`).
- Parse, Don't Validate: Thay vì kiểm tra xem dữ liệu có đúng không, hãy parse dữ liệu từ nguồn không tin cậy thành một kiểu dữ liệu có cấu trúc an toàn thông qua Zod.
- Discriminated Unions: Mẫu hình chuẩn mực để mô hình hóa trạng thái (Loading, Success, Error) giúp trình biên dịch tự động thu hẹp kiểu (Type Narrowing) chính xác 100%.
- **Quy tắc quyết định kỹ thuật**:
- Tuyệt đối cấm sử dụng từ khóa `any` trong toàn bộ codebase; sử dụng `unknown` nếu chưa rõ kiểu và bắt buộc phải narrow kiểu trước khi dùng.
- Mọi dữ liệu đi vào từ network (API response, request body) bắt buộc phải qua Zod schema parse.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Sử dụng ép kiểu mù quáng `const user = res.data as User;`, khi backend đổi API trả về null thì ứng dụng bị crash ngay khi truy cập `user.id`.

## 6. Step-by-Step Execution Workflow
1. Bật toàn bộ các chế độ kiểm tra nghiêm ngặt trong `tsconfig.json` (`strict`, `noUncheckedIndexedAccess`).
2. Cấu hình ESLint rule cấm `any` (`@typescript-eslint/no-explicit-any: error`).
3. Áp dụng Branded Types cho các định danh ID cốt lõi.
4. Xây dựng Zod schemas cho toàn bộ các điểm giao tiếp API bên ngoài.
5. Chạy TypeScript type-checker trong CI để đảm bảo không có bất kỳ lỗi biên dịch nào.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
import { z } from 'zod';

// 1. Branded Type cho UserId chống gán nhầm lẫn
type UserId = string & { readonly __brand: unique symbol };

// 2. Runtime Schema với Zod
const UserSchema = z.object({
  id: z.string().transform((val) => val as UserId),
  email: z.string().email(),
  role: z.enum(['ADMIN', 'USER']),
});

type User = z.infer<typeof UserSchema>;

// 3. Hàm xử lý an toàn: Parse, Don't Validate
export function parseUserData(input: unknown): User {
  return UserSchema.parse(input); // Ném lỗi nếu sai cấu trúc ngay lập tức
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra toàn bộ lỗi kiểu dữ liệu nghiêm ngặt trong dự án
npx tsc --noEmit
```

## 8. Anti-Patterns & Common Traps
- Dùng toán tử ép kiểu không an toàn `!` (Non-null assertion operator) để qua mặt compiler thay vì kiểm tra null rõ ràng.
- Viết generic types lồng nhau quá 5 tầng khiến lập trình viên khác không thể đọc hiểu.

## 9. Quality Gates & Acceptance Criteria
- 0 lỗi biên dịch `tsc --noEmit` và 0 từ khóa `any` xuất hiện trong mã nguồn mới.
- 100% API responses từ bên thứ ba đều được bảo vệ bằng runtime schema parser.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Ngăn chặn lỗ hổng Prototype Pollution bằng cách lọc bỏ các thuộc tính không mong muốn qua `z.object().strip()`.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Cấu hình `tsconfig.json` tối ưu độ an toàn.
- Bộ modules Zod schemas và Branded types chuẩn mực.

## 13. Related & Complementary Skills
dex-nodejs-runtime-diagnostics, dex-frontend-data-flow, dex-contract-first-development

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty fintech thường xuyên bị lỗi chuyển tiền nhầm tài khoản do lập trình viên truyền nhầm tham số hàm `transfer(targetAccountId, sourceAccountId)` vì cả hai đều là kiểu `string`. Sau khi chuyển sang dùng Branded Types `SourceAccountId` và `TargetAccountId`, trình biên dịch TypeScript đã tự động bắt lỗi ngay khi gán nhầm, loại bỏ hoàn toàn các lỗi sai sót nghiêm trọng.
