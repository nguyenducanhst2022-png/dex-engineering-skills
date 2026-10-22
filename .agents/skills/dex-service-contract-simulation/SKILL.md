---
name: dex-service-contract-simulation
description: Construct hermetic wire-level mock virtualization and fault injection environments for external HTTP/gRPC APIs using WireMock, MSW, or Prism. Use when isolating test suites from unstable third-party sandboxes, testing edge timeouts, or developing frontend features against unreleased APIs.
---

# dex-service-contract-simulation

## 1. Purpose & Scope
Xây dựng môi trường ảo hóa hợp đồng dịch vụ cấp độ dây truyền (Wire-Level Mock Virtualization) và tiêm lỗi có kiểm soát (Fault Injection) cho các API HTTP/REST và gRPC bên ngoài bằng WireMock, Mock Service Worker (MSW) hoặc Prism; giúp cô lập hoàn toàn môi trường kiểm thử khỏi sự bất ổn của sandbox bên thứ ba, mô phỏng lỗi gián đoạn mạng và hỗ trợ lập trình song song.

## 2. When to Use
- Khi viết bài kiểm thử tích hợp nhưng sandbox của đối tác ngân hàng bên thứ ba thường xuyên bị bảo trì hoặc giới hạn rate limit.
- Khi cần kiểm tra phản ứng của hệ thống khi API bên ngoài bị timeout (chậm 10s) hoặc trả về mã lỗi 503 Service Unavailable.
- Khi đội frontend cần phát triển tính năng trước khi đội backend hoàn thành việc triển khai API thật.

## 3. When NOT to Use
- Khi chạy bài kiểm thử nghiệm thu cuối cùng (End-to-End Acceptance Test) trên môi trường Staging tích hợp thật.
- Khi chỉ cần mock một hàm nội bộ đơn giản bằng Jest/Vitest trong cùng tiến trình.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp đặc tả OpenAPI (Swagger) hoặc Protobuf, thư viện MSW (Mock Service Worker) hoặc công cụ WireMock standalone.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Hermetic Wire-Level Interception:** Đánh chặn request ở tầng mạng trình duyệt hoặc tầng network socket của Node.js, giúp mã nguồn ứng dụng chạy y hệt như đang gọi API thật.
- **Chaos & Fault Injection:** Chủ động mô phỏng các tình huống xấu: độ trễ cao (Jitter), rớt kết nối giữa chừng (TCP reset) và phản hồi HTTP 5xx.
- **Contract-Driven Verification:** Tự động kiểm tra xem dữ liệu mock có tuân thủ 100% theo bản đặc tả OpenAPI chuẩn hay không.

## 6. Step-by-Step Execution Workflow
1. Nạp bản đặc tả OpenAPI chuẩn vào công cụ ảo hóa Prism hoặc MSW.
2. Xây dựng các kịch bản phản hồi thành công (Happy Path) và thất bại (Edge Cases).
3. Cấu hình các kịch bản tiêm lỗi mạng (Network Faults: 5000ms delay, socket hang up).
4. Chạy toàn bộ bộ kiểm thử tự động trong môi trường ảo hóa hoàn toàn khép kín (Hermetic Sandbox).
5. Xác nhận hệ thống có cơ chế xử lý lỗi và hiển thị thông báo phù hợp cho người dùng.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { http, HttpResponse, delay } from 'msw';
import { setupServer } from 'msw/node';

// Wire-level Mock Virtualization with Fault Injection
export const handlers = [
  http.post('https://api.partner-bank.com/v1/charge', async ({ request }) => {
    const body = await request.json() as any;
    
    // Simulate Chaos Fault: Timeout when amount exceeds 10,000
    if (body.amount > 10000) {
      await delay(6000); // Trigger client timeout
      return new HttpResponse(null, { status: 504 });
    }

    return HttpResponse.json({
      transactionId: 'TX-SIMULATED-999',
      status: 'SUCCESS',
      chargedAt: new Date().toISOString()
    });
  })
];

export const server = setupServer(...handlers);
```

## 8. Anti-Patterns & Common Traps
- Viết mã mock bằng cách viết đè trực tiếp các hàm nội bộ (Monkey Patching `axios.post`) khiến việc kiểm thử không đo lường được hành vi mạng thực tế.
- Để dữ liệu mock bị trôi lệch cấu trúc so với API thật của đối tác mà không có công cụ đối chiếu tự động.
- Chạy bài test tự động trên CI mà gọi thẳng ra dịch vụ bên ngoài, khiến test bị fail ngẫu nhiên mỗi khi mất kết nối Internet.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Bộ kiểm thử tự động chạy hermetic 100% thành công không cần kết nối Internet ra ngoài.
- QG-02: Dữ liệu mock tuân thủ 100% theo cấu trúc hợp đồng OpenAPI schema.
- QG-03: Kiểm thử thành công khả năng xử lý của ứng dụng đối với kịch bản timeout và lỗi 5xx.

## 10. Security & Safety Boundaries
- Không sử dụng dữ liệu thẻ tín dụng hoặc thông tin khách hàng thật trong các tệp kịch bản mock dữ liệu.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bộ kịch bản ảo hóa dịch vụ mạng `service-mock-handlers.ts`.
1. Báo cáo kiểm thử tiêm lỗi và khả năng chịu tải `FAULT_INJECTION_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-api-mocking-virtualization`](.agents/skills/dex-api-mocking-virtualization/SKILL.md)
- [`dex-testing-engineering`](.agents/skills/dex-testing-engineering/SKILL.md)
- [`dex-reliability-engineering`](.agents/skills/dex-reliability-engineering/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Đội ngũ phát triển bị tắc nghẽn công việc vì đối tác cổng thanh toán đang bảo trì môi trường test trong 3 ngày. Kỹ sư kích hoạt `dex-service-contract-simulation`, dựng môi trường mock wire-level với MSW dựa trên OpenAPI của đối tác, tích hợp thêm kịch bản giả lập lỗi ngân hàng từ chối thẻ, giúp đội ngũ tiếp tục lập trình và hoàn thành tính năng đúng hạn.
