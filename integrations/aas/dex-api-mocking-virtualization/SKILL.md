---
name: dex-api-mocking-virtualization
description: Architect hermetic API mocking, WireMock integration, Mock Service Worker (MSW) client interception, synthetic contract fixtures, and fault simulation. Use when isolating external dependencies or building resilient integration tests.
---

# dex-api-mocking-virtualization

> Provenance correction: the attribution/commit below is a historical, unverified import claim. The current verified upstream reference baseline is `8bda5fa7264cafe8259fc8212550d13bf690bfb0`; it does not authenticate the origin of this DEX adapter. See the root `manifests/upstream-sources.json` and `docs/audits/DEX_V9_PIN_CANDIDATES.json`.

> **Source Attribution:** Adapted from [Agentic Awesome Skills](https://github.com/sickn33/agentic-awesome-skills) under MIT License.  
> **Original Author:** sickn33 and contributors  
> **Upstream Path:** `skills/testing/api-mocking-virtualization` (Commit: `a1b2c3d4e5f60718293a4b5c6d7e8f9012345678`)

## 1. Purpose & Scope
Thiết lập môi trường giả lập API (API Mocking & Service Virtualization) mang tính kín (Hermetic) và kiểm soát hoàn toàn; áp dụng Mock Service Worker (MSW) ở tầng network client và WireMock ở tầng backend; cho phép chạy toàn bộ bộ kiểm thử tích hợp mà không cần gọi ra các dịch vụ bên thứ ba.

## 2. When to Use
- Khi các bài kiểm thử tích hợp (Integration tests) thường xuyên rớt chập chờn (Flaky tests) do API đối tác bên ngoài bị chậm hoặc giới hạn lượt gọi (Rate limited).
- Khi cần mô phỏng các lỗi mạng hiếm gặp (504 Gateway Timeout, 429 Too Many Requests, Payload rác) mà môi trường thật không dễ tái tạo.
- Khi phát triển song song Frontend và Backend trước khi Backend hoàn thành xong API thật.

## 3. When NOT to Use
- Kiểm thử End-to-End toàn diện trên môi trường Staging với các service thật (dùng `dex-end-to-end-engineering`).
- Thiết kế hợp đồng API chính thức (dùng `dex-api-engineering`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bản đặc tả API OpenAPI / Swagger hoặc JSON contracts.
- Danh sách các kịch bản phản hồi cần giả lập (Thành công 200, Lỗi 400, Timeout 504).
- Môi trường chạy (Node.js Vitest/Jest, Python Pytest, Browser MSW).

**Điều kiện tiên quyết:**
- Đã xác định rõ các endpoint cần cô lập và cấu trúc dữ liệu phản hồi mẫu.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Tuân thủ chuẩn Agent Skills Specification và ranh giới an toàn của DEX Engineering Framework.
- **Quy tắc quyết định kỹ thuật**:
- **Hermetic Isolation**: Toàn bộ mock phải chạy in-memory hoặc local container; cấm gọi request ra internet trong khi chạy test suite cục bộ.
- **Contract Drift Detection**: Mock data phải được tự động đối chiếu với OpenAPI schema chính thức để tránh hiện tượng mock bị lệch so với API thật.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Mock trả về cấu trúc cũ nhưng test vẫn pass**: Khắc phục bằng cách tự động validate mock response với Zod schema trích xuất từ OpenAPI spec.

## 6. Step-by-Step Execution Workflow
1. Khảo sát danh sách endpoint và third-party APIs cần giả lập.
2. Thiết lập trình đánh chặn mạng (MSW handlers hoặc WireMock server).
3. Định nghĩa các kịch bản phản hồi (Scenarios) bao gồm ca thành công và ca lỗi biên.
4. Tích hợp mock server vào test harness.
5. Chạy bộ kiểm thử tự động trong trạng thái ngắt mạng hoàn toàn.
6. Kiểm tra tính đồng bộ giữa mock data và API contract chính thức.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
export const handlers = [
  http.get('https://api.partner.com/v1/charge', () => {
    return HttpResponse.json({ status: 'succeeded', transactionId: 'tx_12345' });
  })
];
export const mockServer = setupServer(...handlers);
```

### Lệnh xác minh & thực thi:
- Chạy kiểm thử với MSW: `npx vitest run tests/integration/mocked-api.test.ts`
- Kiểm tra tính hợp lệ của schema mock: `npm run test:mock-schema`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống bên thứ ba luôn hoạt động lý tưởng.
- **Anti-Pattern 2**: Thực hiện phân tích trên các tệp hoặc mục tiêu chưa được cấp thẩm quyền kiểm tra rõ ràng.
- **Trap**: Tự động giả lập kết quả phân tích hoặc đưa ra kết luận thiếu bằng chứng kỹ thuật khách quan.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Định nghĩa đầy đủ schema giả lập cho cả ca thành công và thất bại.
- QG-04: Bộ kiểm thử chạy thành công 100% trong chế độ offline hoàn toàn.
- Mọi kết quả phải có lệnh thực thi kiểm chứng và bằng chứng rõ ràng trước khi báo cáo hoàn thành.

## 10. Security & Safety Boundaries
- Tuyệt đối không dùng API keys thật trong tệp cấu hình mock test.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế kiểm soát rủi ro.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **MCP & Tooling**: Hỗ trợ tích hợp Model Context Protocol và CLI tương ứng trên Windows 11, Linux, macOS.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình handler mock (`tests/mocks/handlers.ts`).
- Bộ test tích hợp chạy cô lập.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-security-audit`: Kiểm toán an ninh toàn diện cho ứng dụng.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-api-mocking-virtualization** trong dự án:
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Chạy các lệnh kiểm chứng tại Mục 7 và đối chiếu với Quality Gates tại Mục 9.
4. Đóng gói deliverables theo danh sách tại Mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
