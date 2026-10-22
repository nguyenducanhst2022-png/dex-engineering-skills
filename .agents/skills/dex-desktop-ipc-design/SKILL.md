---
name: dex-desktop-ipc-design
description: Design secure, type-safe desktop inter-process communication (IPC) interfaces using JSON Schema/Zod/Protobuf, bi-directional event buses, strict main-process validation, and privilege boundaries. Use when designing communications between desktop processes.
---

# dex-desktop-ipc-design

## 1. Purpose & Scope
Thiết kế và chuẩn hóa giao thức truyền thông liên tiến trình (Inter-Process Communication - IPC) an toàn, hiệu năng cao và có kiểm tra kiểu dữ liệu tĩnh (Type-Safe) cho các ứng dụng máy tính (Electron, Tauri, Native Multi-process); xây dựng các kênh truyền tin hai chiều (Bi-directional Message Buses), áp dụng hợp đồng dữ liệu chuẩn hóa (Zod / JSON Schema / Protobuf), kiểm soát chặt chẽ ranh giới quyền hạn giữa Renderer (Untrusted) và Host/Main process (Privileged), áp dụng cơ chế điều tiết lưu lượng (Rate Limiting) và chống tấn công leo thang đặc quyền (Privilege Escalation).

## 2. When to Use
- Khi ứng dụng desktop có nhiều tiến trình (Main, Renderer, Worker, Helper processes) cần trao đổi dữ liệu với nhau.
- Khi hệ thống IPC hiện tại sử dụng chuỗi string tự do (`ipcRenderer.send('do-something', data)`) dẫn tới lỗi runtime khó phát hiện.
- Khi cần ngăn chặn tiến trình Renderer không đáng tin cậy lừa tiến trình Main thực thi các lệnh nguy hiểm của hệ điều hành.

## 3. When NOT to Use
- Giao tiếp mạng giữa client và server từ xa qua HTTP/gRPC (dùng `dex-api-engineering`).
- Quản lý trạng thái cục bộ bên trong một tiến trình giao diện đơn lẻ (dùng `dex-frontend-data-flow`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các kênh truyền tin (Channels/Endpoints) và tác vụ tương ứng.
- Cấu trúc payload gửi đi và kết quả phản hồi mong đợi.
- Mức độ bảo mật của từng tác vụ (Đọc file, ghi file, thực thi lệnh shell, tương tác phần cứng).
- **Điều kiện tiên quyết**:
- TypeScript hoặc Rust hỗ trợ kiểm tra kiểu dữ liệu tĩnh.
- Thư viện validate dữ liệu runtime (Zod, TypeBox, Serde).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Zero-Trust Renderer Principle**: Tiến trình Main coi mọi thông điệp đến từ Renderer là dữ liệu độc hại tiềm tàng; mọi payload bắt buộc phải được validate cấu trúc trước khi thực thi.
- **Type-Safe Contract Sharing**: Sử dụng chung một định nghĩa kiểu (Interface / Zod Schema) cho cả 2 đầu gửi và nhận; đổi tên kênh hoặc sửa trường dữ liệu sẽ báo lỗi ngay khi biên dịch code.
- **Asynchronous Request-Response Correlated by UUID**: Mỗi request gửi qua IPC được gắn một correlation ID duy nhất để ánh xạ chính xác với phản hồi tương ứng, tránh tình trạng race condition khi gửi nhiều request song song.
- **Quy tắc quyết định kỹ thuật**:
- **Cấm Kênh IPC Đa Năng Không Định Kiểu**: Không tạo các kênh kiểu `ipc.send('eval', code)` hay `ipc.send('execute-command', cmd)`.
- **Input Validation Bắt Buộc Tại Main Process**: Mọi tham số nhận được trong `ipcMain.handle` phải được kiểm tra qua Zod schema; nếu không hợp lệ phải ném ngoại lệ ngay.
- **Kiểm Soát Rate Limit Đối Với Các Tác Vụ Nặng**: Áp dụng giới hạn tần suất gọi IPC từ Renderer đối với các thao tác I/O đĩa cứng hoặc mật mã học để tránh DoS tiến trình Main.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗ hổng Arbitrary File Write qua IPC**: Renderer gửi đường dẫn `../../../../etc/passwd` vào kênh lưu file -> Khắc phục: Chuẩn hóa đường dẫn bằng `path.resolve` và kiểm tra đường dẫn bắt buộc phải nằm trong thư mục cho phép (Safe Sandboxed Directory).
- **Ứng dụng bị đơ toàn bộ vì IPC bị tắc nghẽn**: Renderer gửi liên tục 10,000 sự kiện/giây qua IPC -> Khắc phục: Áp dụng cơ chế gom lô (Batching) hoặc Debounce/Throttle tại nguồn phát.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo tệp hợp đồng IPC chung (`ipc-contracts.ts`): Định nghĩa danh sách kênh và schema Zod tương ứng.
2. Sinh kiểu dữ liệu TypeScript tự động từ schema: `type SaveFileRequest = z.infer<typeof SaveFileSchema>`.
3. Xây dựng Type-Safe Client wrapper cho Renderer: Gói các lệnh gọi `ipcRenderer.invoke` có kiểm tra kiểu tham số đầu vào và kiểu kết quả trả về.
4. Xây dựng Type-Safe Router cho Main process: Tự động validate payload bằng Zod trước khi chuyển tới controller nghiệp vụ.
5. Xử lý chuẩn hóa mã lỗi IPC: Bọc lỗi thành cấu trúc `{ success: false, code: 'INVALID_PATH', message: string }`.
6. Kiểm thử tự động hợp đồng IPC bằng unit tests giả lập truyền tin.
7. Tài liệu hóa danh mục các kênh IPC và ma trận phân quyền tương ứng.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// shared/ipc-contracts.ts - Type-Safe IPC Contract Definition
import { z } from 'zod';

export const WriteNoteSchema = z.object({
  noteId: z.string().uuid(),
  title: z.string().min(1).max(200),
  content: z.string().max(1_000_000),
});
export type WriteNoteInput = z.infer<typeof WriteNoteSchema>;

export interface IpcChannelMap {
  'notes:save': { input: WriteNoteInput; output: { success: boolean; updatedAt: number } };
  'notes:delete': { input: { noteId: string }; output: { success: boolean } };
}

// main/ipc-handler.ts - Main Process Safe Receiver
import { ipcMain } from 'electron';
import { WriteNoteSchema } from '../shared/ipc-contracts';

export function registerIpcHandlers(notesService: NotesService) {
  ipcMain.handle('notes:save', async (_event, rawInput) => {
    // Validate chặt chẽ bằng Zod ở phía Main Process
    const parseResult = WriteNoteSchema.safeParse(rawInput);
    if (!parseResult.success) {
      throw new Error(`IPC_VALIDATION_FAILED: ${parseResult.error.message}`);
    }
    const { noteId, title, content } = parseResult.data;
    return await notesService.saveNote(noteId, title, content);
  });
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra kiểu dữ liệu toàn bộ hợp đồng IPC: `npx tsc --noEmit`
- Chạy unit test kiểm tra từ chối payload sai: `npm run test -- test/ipc-contracts.test.ts`
- Thử nghiệm gửi payload vượt ngưỡng dung lượng để kiểm tra cơ chế chặn

## 8. Anti-Patterns & Common Traps
- **Truyền trực tiếp đối tượng không thể serialize**: Truyền Function, DOM Node, hoặc đối tượng có tham chiếu vòng (Circular Reference) qua IPC.
- **Dùng IPC đồng bộ (`ipcRenderer.sendSync`)**: Gây khóa cứng toàn bộ giao diện người dùng cho tới khi tiến trình Main phản hồi.
- **Bỏ qua kiểm tra nguồn gốc của event sender**: Không kiểm tra `event.senderFrame` để xác định cửa sổ nào gửi tin nhắn.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các kênh IPC đều có định nghĩa kiểu dữ liệu tĩnh và schema validation runtime.
- QG-07: Không có kênh IPC nào cho phép truyền đường dẫn file tùy ý hoặc lệnh shell trực tiếp.
- QG-11: Toàn bộ các lệnh gọi IPC đều là bất đồng bộ (Non-blocking Asynchronous).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Kiểm tra xác thực frame gửi thông điệp (`event.senderFrame.url`) để tránh bị tấn công từ iframes nhúng ngoài.
- Giới hạn kích thước tối đa của mỗi thông điệp IPC (không quá 10MB/message).
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Tệp định nghĩa hợp đồng IPC `ipc-contracts.ts`.
- Wrapper client và handler phía Main process có validation.
- Bộ unit tests xác nhận tính toàn vẹn của hợp đồng.

## 13. Related & Complementary Skills
- `dex-electron-security`: Rào chắn an toàn khi thiết lập IPC trong Electron.
- `dex-tauri-desktop-integration`: Tận dụng cơ chế type-safe IPC của Tauri qua Serde.
- `dex-api-contract-evolution`: Quản lý sự thay đổi phiên bản của các hợp đồng IPC.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng máy tính tài liệu văn phòng cần tính năng lưu file từ webview. Thay vì mở hàm `fs.writeFile` tự do cho webview, kỹ sư áp dụng `dex-desktop-ipc-design`. Họ định nghĩa Zod schema cho kênh `document:save`, quy định rõ file ID và nội dung văn bản. Phía Main process kiểm tra Zod, tự động sinh tên file an toàn trong thư mục sandbox được chỉ định và ghi đĩa, chặn đứng nguy cơ Renderer gửi chuỗi path traversal ghi đè file hệ thống.
