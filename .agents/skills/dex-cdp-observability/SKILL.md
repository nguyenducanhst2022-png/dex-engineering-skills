---
name: dex-cdp-observability
description: Harness the Chrome DevTools Protocol (CDP) for low-level performance trace capture, memory heap snapshot analysis, network throttle simulation, and console telemetry auditing. Use when diagnosing elusive browser memory leaks, profiling main thread blocking tasks, or automating deep performance audits.
---

# dex-cdp-observability

## 1. Purpose & Scope
Khai thác giao thức Chrome DevTools Protocol (CDP) để chẩn đoán chuyên sâu hiệu năng trình duyệt ở tầng thấp; tự động thu thập dấu vết thực thi (Performance Traces), chụp và so sánh ảnh chụp bộ nhớ heap (Heap Snapshots), mô phỏng bóp nghẹt mạng/CPU và kiểm toán nhật ký console của trình duyệt mà không làm rò rỉ phiên làm việc.

## 2. When to Use
- Khi cần điều tra các lỗi rò rỉ bộ nhớ (Memory Leaks) phức tạp khiến ứng dụng bị đơ sau một thời gian dài sử dụng.
- Khi xây dựng các công cụ đo lường hiệu năng và chất lượng web tự động trong đường ống CI/CD.
- Khi cần mô phỏng chính xác các điều kiện mạng yếu, mất gói tin hoặc ngắt kết nối đột ngột ở tầng socket.

## 3. When NOT to Use
- Khi chỉ cần kiểm tra các tính năng tương tác UI thông thường (dùng Playwright cấp cao là đủ).
- Khi chạy kiểm thử trên các trình duyệt không thuộc họ Chromium (như Safari/WebKit).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kết nối CDP WebSocket (`chrome-remote-interface` hoặc `CDPSession` của Playwright), kiến thức về các domain CDP: `Page`, `Network`, `Performance`, `HeapProfiler`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **CDP Domain Architecture:** Kiến trúc chia thành các miền chức năng độc lập (Domains) điều khiển qua các lệnh JSON-RPC.
- **Heap Allocation Timeline:** Ghi lại từng lần cấp phát đối tượng trên bộ nhớ JavaScript để tìm ra các đối tượng bị giữ lại không được thu gom rác (Retained Objects).
- **Network Throttling Profiles:** Giả lập chính xác độ trễ mạng (Latency), băng thông tải xuống (Download throughput) và tải lên (Upload throughput).

## 6. Step-by-Step Execution Workflow
1. Mở phiên kết nối `CDPSession` từ Playwright hoặc Puppeteer.
2. Kích hoạt các domain cần thiết: `await client.send('Performance.enable')` và `Network.enable`.
3. Thiết lập điều kiện mạng mô phỏng (ví dụ mạng 3G Chậm: 400ms latency, 400kbps download).
4. Chụp ảnh phân bổ bộ nhớ trước và sau khi thực hiện thao tác nghiệp vụ lặp lại 10 lần.
5. So sánh hai file heap snapshot để tìm các đối tượng bị rò rỉ và lập báo cáo phân tích.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { chromium } from '@playwright/test';

export async function profileMemoryWithCDP(url: string) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const cdp = await page.context().newCDPSession(page);

  await cdp.send('HeapProfiler.enable');
  await page.goto(url);

  // Collect initial garbage and take baseline snapshot
  await cdp.send('HeapProfiler.collectGarbage');
  
  // Track allocation metrics
  const metrics = await cdp.send('Performance.getMetrics');
  console.log('JS Heap Used Size:', metrics.metrics.find(m => m.name === 'JSHeapUsedSize')?.value);

  await browser.close();
}
```

## 8. Anti-Patterns & Common Traps
- Để mở phiên kết nối CDP mà không đóng lại gây rò rỉ tiến trình Chromium chạy ngầm làm nghẽn RAM server CI.
- Chụp heap snapshot quá thường xuyên trên ứng dụng đang tải dữ liệu lớn làm sập tiến trình trình duyệt.
- Bỏ qua bước cưỡng bức dọn rác (`collectGarbage`) trước khi đo lường bộ nhớ dẫn đến số liệu đo bị sai lệch.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Bộ nhớ heap JavaScript không tăng tuyến tính sau 20 chu kỳ lặp lại hành động người dùng.
- QG-02: Dấu vết thực thi CDP thu thập đầy đủ thông tin về các tác vụ chặn luồng chính (Long Tasks > 50ms).
- QG-03: Mọi phiên CDP được dọn dẹp và giải phóng tài nguyên hoàn toàn sau khi hoàn thành đo lường.

## 10. Security & Safety Boundaries
- Không để cổng điều khiển từ xa CDP (`--remote-debugging-port`) lắng nghe trên giao diện mạng công cộng không có mật khẩu.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Script tự động đo lường hiệu năng sâu qua CDP `cdp-performance-audit.ts`.
1. Báo cáo phân tích rò rỉ bộ nhớ kèm đồ thị heap memory.

## 13. Related & Complementary Skills
- [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md)
- [`dex-browser-automation-testing`](.agents/skills/dex-browser-automation-testing/SKILL.md)
- [`dex-web-animation-performance`](.agents/skills/dex-web-animation-performance/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trang web dashboard theo dõi camera an ninh bị sập tab sau khi chạy liên tục 4 tiếng. Kỹ sư kích hoạt `dex-cdp-observability` để kết nối CDP, tự động chụp heap snapshot mỗi 30 phút, phát hiện một mảng mảng lưu trữ frame ảnh cũ không được xóa bỏ, sửa lỗi và giúp trang chạy ổn định suốt 7 ngày.
