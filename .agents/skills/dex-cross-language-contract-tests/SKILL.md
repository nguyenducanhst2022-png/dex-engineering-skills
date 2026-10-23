---
name: dex-cross-language-contract-tests
description: Design and verify cross-language API contracts, Protocol Buffers schemas, OpenAPI specifications, and consumer-driven contracts between polyglot microservices. Use when eliminating integration drift across diverse programming stacks.
---

# dex-cross-language-contract-tests

## 1. Purpose & Scope
Thiết kế, kiểm thử và xác minh các giao ước API đa ngôn ngữ (Cross-Language Contract Tests), lược đồ Protocol Buffers, đặc tả OpenAPI và hợp đồng hướng người tiêu dùng (Consumer-Driven Contracts) giữa các microservices viết bằng các ngôn ngữ khác nhau.

## 2. When to Use
- Khi dịch vụ backend viết bằng Go/Java cung cấp API cho client viết bằng TypeScript/Swift và thường xuyên bị lỗi không khớp kiểu dữ liệu.
- Khi cập nhật một trường dữ liệu trong API và cần bảo đảm không làm gãy các dịch vụ tiêu thụ khác.
- Khi muốn kiểm thử khả năng tương thích dịch vụ mà không cần khởi động toàn bộ cụm microservices phức tạp.

## 3. When NOT to Use
- Khi tất cả các dịch vụ đều nằm trong cùng một ứng dụng nguyên khối (Monolith) và chia sẻ chung các struct nội bộ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File định nghĩa giao ước (OpenAPI YAML, `.proto` files, Pact contracts), mã nguồn client và server.
- **Quyền hạn truy cập:** Quyền chạy test suite kiểm thử hợp đồng và truy cập Pact Broker.

## 5. Core Concepts & Taxonomy
- **Consumer-Driven Contracts (Pact):** Phía tiêu thụ (Consumer) định nghĩa chính xác những dữ liệu mà họ kỳ vọng nhận được; phía cung cấp (Provider) chạy kiểm thử để chứng minh họ đáp ứng đầy đủ kỳ vọng đó.
- **Schema Compatibility Rules:** Các quy tắc tương thích xuôi và ngược (Backward / Forward Compatibility) khi thêm, bớt hoặc đổi tên trường trong protobuf.
- **Pact Broker:** Máy chủ trung tâm lưu trữ và xác nhận trạng thái tương thích giữa các phiên bản dịch vụ trước khi cho phép deploy (`can-i-deploy`).

## 6. Step-by-Step Execution Workflow
1. Phía Consumer viết kiểm thử hợp đồng mô tả yêu cầu request và response mong đợi.
2. Chạy test Consumer để tự động sinh file hợp đồng chuẩn hóa (Pact JSON).
3. Đẩy file hợp đồng lên Pact Broker trung tâm kèm số phiên bản commit Git.
4. Phía Provider chạy kiểm thử xác thực hợp đồng (Provider Verification Test) đối chiếu mã nguồn của họ với Pact file.
5. Tích hợp lệnh kiểm tra `can-i-deploy` vào pipeline CI/CD trước khi triển khai dịch vụ.
6. Chặn đứng việc phát hành nếu phát hiện thay đổi phá vỡ giao dịch giữa hai ngôn ngữ.

## 7. Concrete Examples
### Kiểm thử xác thực Provider bằng Pact trong Python / TypeScript:
```typescript
// consumer.test.ts (TypeScript)
import { PactV3, MatchersV3 } from '@pact-foundation/pact';

const provider = new PactV3({
  consumer: 'WebFrontend-TS',
  provider: 'OrderService-Go',
});

it('nhan ve thong tin don hang hop le tu Go Service', async () => {
  provider
    .given('don hang ton tai voi ID 100')
    .uponReceiving('yeu cau lay chi tiet don hang')
    .withRequest({ method: 'GET', path: '/orders/100' })
    .willRespondWith({
      status: 200,
      body: {
        id: MatchersV3.integer(100),
        amount: MatchersV3.decimal(150.50),
        status: MatchersV3.like('COMPLETED'),
      },
    });

  await provider.executeTest(async (mockServer) => {
    const res = await fetch(`${mockServer.url}/orders/100`);
    const data = await res.json();
    expect(data.status).toBe('COMPLETED');
  });
});
```

## 8. Anti-Patterns & Common Traps
- **End-to-End Test Reliance:** Chỉ dựa vào các bài test E2E cồng kềnh, chạy chậm và hay gặp lỗi chập chờn (flaky) để phát hiện sai lệch API.
- **Unversioned Breaking Changes:** Xóa hoặc sửa kiểu của một trường dữ liệu trong protobuf mà không tạo phiên bản mới (v1 -> v2).
- **Manual Mock Verification:** Viết các mock dữ liệu giả lập thủ công ở phía client mà không bao giờ đối soát lại với API thực tế của server.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các endpoint liên dịch vụ có hợp đồng Pact hoặc protobuf schema được kiểm thử tự động.
- **QG-04**: Lệnh `pact-broker can-i-deploy` trả về kết quả thành công trước khi bước deploy bắt đầu.
- **QG-07**: Không có thay đổi phá vỡ tương thích ngược (Breaking Change) nào được chấp thuận vào main branch.

## 10. Security & Safety Boundaries
- Không đưa dữ liệu thật hoặc thông tin bí mật vào các fixture mẫu của hợp đồng API.

## 11. Platform Adapters
- **Contract Testing**: Pact (TypeScript, Go, Python, Java, Rust), Buf (Protobuf), OpenAPI Tools, Spectral.

## 12. Deliverables & Output Artifacts
- File hợp đồng Pact JSON hoặc Protocol Buffers schemas.
- Test suite kiểm thử giao ước hai đầu Consumer và Provider.
- Cấu hình kiểm tra `can-i-deploy` trong pipeline CI.

## 13. Related & Complementary Skills
dex-contract-first-development, dex-configuration-schema-design, dex-polyglot-build-orchestration

## 14. Realistic Usage Example
```powershell
# Chạy kiểm tra tính tương thích trước khi triển khai dịch vụ
npx pact-broker can-i-deploy --pacticipant WebFrontend-TS --version 1.2.0 --to-environment production

# Kiểm tra tính tương thích của Protobuf bằng Buf
buf breaking --against ".git#branch=main"
```
