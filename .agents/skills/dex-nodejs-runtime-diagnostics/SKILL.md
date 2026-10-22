---
name: dex-nodejs-runtime-diagnostics
description: Diagnose and resolve Node.js event-loop delays, memory leaks, unhandled promise rejections, and async context tracking using Clinic.js, V8 heap snapshots, and perf_hooks. Use when Node.js services degrade under load.
---

# dex-nodejs-runtime-diagnostics

## 1. Purpose & Scope
Chẩn đoán, phân tích và xử lý các vấn đề hiệu năng chuyên sâu trong môi trường Node.js Runtime (Event Loop Delays, Memory Leaks, Unhandled Promise Rejections, GC Pauses); sử dụng các công cụ chuyên dụng (Clinic.js, Chrome DevTools Heap Snapshots, `perf_hooks`, `async_hooks`) để tối ưu hóa khả năng chịu tải và độ ổn định của ứng dụng.

## 2. When to Use
- Dịch vụ Node.js bị tăng đột biến độ trễ P99 dù CPU chỉ mới dùng 40%.
- Bộ nhớ RAM của tiến trình Node.js tăng dần theo thời gian và sập do `JavaScript heap out of memory`.
- Xuất hiện cảnh báo `UnhandledPromiseRejection` làm tiến trình bị crash đột ngột.

## 3. When NOT to Use
- Không thực hiện profiling trực tiếp trên container production đang phục vụ khách hàng mà không giới hạn thời gian (gây suy giảm 20-30% hiệu năng).
- Không dùng Node.js cho các tác vụ tính toán CPU-intensive kéo dài trong luồng chính (hãy dùng Worker Threads hoặc tách service riêng).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File heap snapshot (`.heapsnapshot`) hoặc CPU profile (`.cpuprofile`).
- Thông số Event Loop Delay từ Prometheus/OpenTelemetry.
- Mã nguồn nghi ngờ gây nghẽn luồng bất đồng bộ.
- **Điều kiện tiên quyết**:
- Ứng dụng Node.js có thể khởi động với cờ `--inspect` hoặc tích hợp agent thu thập metrics.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Event Loop Lag: Nếu một tác vụ đồng bộ chạy mất 100ms trên main thread (ví dụ: `JSON.parse` file 50MB, regex catastrophic backtracking), mọi kết nối khác đều bị đóng băng trong 100ms đó.
- Memory Leak Causes trong Node.js: Biến toàn cục (Global variables), Closures giữ tham chiếu tới object lớn, Quên hủy Event Listeners (`EventEmitter.on` không có `removeListener`), Cache in-memory không có TTL/LRU eviction.
- AsyncLocalStorage: Truy vết ngữ cảnh request (Trace ID, User Context) xuyên suốt các lời gọi async mà không phải truyền param thủ công.
- **Quy tắc quyết định kỹ thuật**:
- Nếu Event Loop Lag vượt quá 20ms: kích hoạt cảnh báo vàng; nếu > 100ms: kích hoạt cảnh báo đỏ.
- Luôn bật cờ `--unhandled-rejections=strict` để phát hiện và xử lý triệt để các Promise lỗi.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Lập trình viên sử dụng mảng tĩnh trong module scope để lưu log tạm, làm mảng phình to vô hạn và gây OOM crash sau 3 ngày chạy.

## 6. Step-by-Step Execution Workflow
1. Cấu hình thu thập chỉ số Event Loop Delay bằng `perf_hooks.monitorEventLoopDelay()`.
2. Chạy ứng dụng dưới tải giả lập kết hợp công cụ `clinic doctor` hoặc `clinic flame`.
3. Nếu phát hiện rò rỉ bộ nhớ: chụp 2 bản Heap Snapshot (Snapshot 1 lúc bắt đầu tải, Snapshot 2 sau 10,000 requests) và dùng so sánh (Comparison view) trong Chrome DevTools để tìm object rò rỉ.
4. Tối ưu hóa các đoạn code đồng bộ chặn main thread hoặc thay thế in-memory cache bằng Redis/LRU cache có giới hạn.
5. Xác minh lại bằng bài kiểm thử tải ngâm (Soak test).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```javascript
// Giám sát Event Loop Delay chuyên sâu bằng perf_hooks
const { monitorEventLoopDelay } = require('perf_hooks');

const h = monitorEventLoopDelay({ resolution: 20 });
h.enable();

setInterval(() => {
  const p99 = h.percentile(99) / 1e6; // Chuyển nanoseconds sang milliseconds
  console.log(`Node.js Event Loop P99 Delay: ${p99.toFixed(2)}ms`);
  if (p99 > 50) {
    console.warn('CẢNH BÁO: Event loop đang bị chặn bởi tác vụ đồng bộ!');
  }
  h.reset();
}, 5000);
```

### Lệnh xác minh & thực thi:
```bash
# Phân tích hiệu năng chuyên sâu Node.js bằng Clinic.js Flamegraph
npx clinic flame -- node server.js
```

## 8. Anti-Patterns & Common Traps
- Sử dụng các hàm đồng bộ chặn luồng (`fs.readFileSync`, `crypto.pbkdf2Sync`) trong request handler.
- Lạm dụng `JSON.stringify` trên các đối tượng dữ liệu khổng lồ trong luồng chính.

## 9. Quality Gates & Acceptance Criteria
- Event Loop Delay P99 phải duy trì dưới 10ms dưới điều kiện tải thiết kế.
- 0 rò rỉ bộ nhớ được ghi nhận trong bài kiểm thử ngâm tải 6 tiếng liên tục.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Cổng debug `--inspect` tuyệt đối không được mở ra ngoài mạng công cộng (chỉ bind vào `127.0.0.1` và truy cập qua SSH tunnel).
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Báo cáo phân tích Clinic.js HTML Flamegraph.
- Bản vá khắc phục triệt để lỗi rò rỉ bộ nhớ hoặc chặn Event Loop.

## 13. Related & Complementary Skills
dex-typescript-type-safety, dex-load-and-stress-testing, dex-performance-profiling

## 14. Realistic Usage Example
### Tình huống thực tế:
Một API Gateway viết bằng Express.js cứ sau 48 giờ chạy lại bị khởi động lại do hết bộ nhớ. Sử dụng Chrome DevTools so sánh Heap Snapshots, kỹ sư phát hiện mỗi request đều đăng ký một listener mới vào một EventEmitter chung mà không bao giờ gỡ bỏ. Sau khi sửa lỗi rò rỉ listener, bộ nhớ ổn định ở mức 120MB phẳng suốt nhiều tháng.
