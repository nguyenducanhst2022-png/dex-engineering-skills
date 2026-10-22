---
name: dex-plugin-architecture
description: Architect extensible plugin systems, micro-kernel architectures, extension lifecycle hooks, manifest specifications, sandboxed runtime execution, and dynamic loading. Use when designing extensibility layers for platforms or developer tools.
---

# dex-plugin-architecture

## 1. Purpose & Scope
Thiết kế và hiện thực hóa Kiến trúc Tiện ích Mở rộng (Plugin Architecture / Microkernel Pattern) cho phép các nhà phát triển thứ ba mở rộng tính năng của hệ thống lõi mà không cần chỉnh sửa mã nguồn gốc; định nghĩa vòng đời plugin, cơ chế đăng ký hook, kiểm tra tương thích phiên bản (Manifest Specification) và cách ly thực thi an toàn (Sandbox Execution).

## 2. When to Use
- Khi ứng dụng cần hỗ trợ các adapter, connector hoặc giao diện người dùng tùy biến từ bên thứ ba.
- Khi hệ thống lõi quá cồng kềnh và cần chuyển các module chuyên biệt (ví dụ: Thanh toán, Định dạng xuất file) thành các plugin tải động.
- Khi cần hỗ trợ cơ chế 'Hot Reloading' hoặc bật/tắt module linh hoạt lúc runtime.

## 3. When NOT to Use
- Ứng dụng nguyên khối nhỏ không có kế hoạch mở rộng cho bên thứ ba (dùng `dex-code-organization`).
- Tách hệ thống thành các microservices độc lập qua mạng (dùng `dex-software-architecture`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Điểm mở rộng của hệ thống lõi (Extension Points / Hook Registry).
- Bản đặc tả plugin manifest (Tên, phiên bản tương thích, quyền hạn, dependencies).
- Môi trường chạy plugin (In-process qua Dynamic Import, WebAssembly sandbox, hoặc Out-of-process qua gRPC).

**Điều kiện tiên quyết:**
- Hệ thống lõi đã định nghĩa sẵn các interface/contracts trừu tượng.
- Có cơ chế xử lý lỗi khi plugin của bên thứ ba bị sập mà không làm crash ứng dụng chính.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Kernel Độc Lập Với Plugin**: Ứng dụng chính phải khởi động và hoạt động trơn tru ở chế độ tối thiểu ngay cả khi không có bất kỳ plugin nào được nạp.
- **Crash Isolation (Cách Ly Sập Đổ)**: Một plugin gặp lỗi nghiêm trọng (Unhandled Exception) không bao giờ được phép làm sập toàn bộ ứng dụng lõi.
- **Kiểm Tra Phiên Bản API Nghiêm Ngặt**: Plugin phải khai báo phiên bản SDK tương thích (ví dụ: `^3.0.0`). Nếu phiên bản Kernel không khớp, từ chối nạp và ghi log cảnh báo rõ ràng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Plugin bên thứ ba chạy vòng lặp vô tận làm đóng băng hệ thống**: Do chạy trên main thread -> Khắc phục: Chạy plugin trong Worker Thread / WebAssembly sandbox kèm Timeout (tối đa 5000ms mỗi hook).
- **Xung đột phiên bản thư viện giữa 2 plugin**: Cả 2 cùng import 2 phiên bản lodash khác nhau -> Khắc phục: Đóng gói dependency riêng biệt trong plugin bundle hoặc dùng ESM scoped imports.

## 6. Step-by-Step Execution Workflow
1. Thiết kế Kernel tối giản chỉ chứa các chức năng nền tảng: Hook Registry, Event Bus, Plugin Loader.
2. Định nghĩa giao diện lập trình Plugin API (SDK/Interfaces) cho các extension point.
3. Xây dựng quy chuẩn tệp mô tả plugin (`plugin.manifest.json`): Tên, ID duy nhất, phiên bản hỗ trợ, hooks đăng ký.
4. Triển khai cơ chế nạp plugin (Dynamic Loader): Quét thư mục plugins hoặc tải từ kho plugin registry.
5. Quản lý vòng đời plugin: `install()`, `initialize()`, `activate()`, `deactivate()`, `uninstall()`.
6. Thiết lập ranh giới an toàn: Cách ly plugin lỗi bằng khối `try/catch` có giới hạn thời gian (Timeout Guard) hoặc WebAssembly (Wasm sandbox).
7. Cung cấp CLI hoặc API cho phép người dùng quản lý: Liệt kê, cài đặt, bật/tắt và gỡ bỏ plugin.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// plugin-contract.ts
export interface DexPlugin {
  id: string;
  version: string;
  name: string;
  activate(context: PluginContext): Promise<void>;
  deactivate(): Promise<void>;
}

export interface PluginContext {
  registerHook(event: string, callback: (...args: any[]) => any): void;
  logger: { info: (msg: string) => void; error: (msg: string) => void };
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính hợp lệ của Plugin Manifest: `dex plugin validate ./my-plugin`
- Chạy kiểm thử tích hợp plugin với mock kernel: `npm run test:plugin`
- Liệt kê các plugin đang hoạt động: `dex plugin list`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: Plugin tuân thủ đúng 100% các interface của Kernel.
- QG-07: Hệ thống lõi cô lập thành công và không bị gián đoạn khi một plugin ném exception.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Giới hạn quyền truy cập hệ thống file và network của plugin thông qua mô hình cấp quyền tường minh (Permissions Manifest: `allow-net`, `allow-fs`).
- Xác thực chữ ký số (Cryptographic Signature) của plugin trước khi nạp vào hệ thống sản xuất.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Bản đặc tả Plugin Manifest Schema (`manifest.schema.json`).
- Module Plugin Loader & Registry trong mã nguồn lõi.
- Mẫu Plugin mẫu (Starter Example Plugin) hướng dẫn cho nhà phát triển.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-plugin-architecture**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
