---
name: dex-property-based-testing
description: Implement property-based testing, generative fuzzing, system invariant verification with Hypothesis / fast-check / QuickCheck, edge-case discovery, and test case shrinking. Use when verifying complex algorithms, data serializers, or domain invariants.
---

# dex-property-based-testing

## 1. Purpose & Scope
Hiện thực hóa phương pháp Kiểm thử Dựa trên Thuộc tính (Property-Based Testing - PBT) và Kiểm thử Sinh ngẫu nhiên (Generative Fuzzing); sử dụng các framework chuyên dụng (Hypothesis cho Python, fast-check cho TypeScript, proptest cho Rust) để tạo ra hàng nghìn trường hợp kiểm thử tự động, kiểm chứng các bất biến toán học và nghiệp vụ của hệ thống (System Invariants), đồng thời tự động thu nhỏ ca kiểm thử lỗi về dạng tối giản nhất (Test Case Shrinking).

## 2. When to Use
- Khi các bài kiểm thử đơn vị thông thường (Unit tests với dữ liệu cố định do lập trình viên nghĩ ra) không thể bao quát hết các ca biên kỳ quặc (Unicode, số âm, chuỗi cực dài, ký tự null).
- Khi kiểm chứng tính đúng đắn của các thuật toán phức tạp (Thuật toán sắp xếp, mã hóa dữ liệu, nén file, parser).
- Khi kiểm thử tính toàn vẹn của quá trình tuần tự hóa và giải mã (Roundtrip Invariant: `decode(encode(data)) === data`).

## 3. When NOT to Use
- Kiểm thử giao diện hiển thị HTML/CSS tĩnh (dùng `dex-visual-regression`).
- Các hàm CRUD cơ bản không chứa logic tính toán phức tạp.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Thuật toán hoặc hàm nghiệp vụ cần kiểm chứng.
- Các bất biến cần bảo toàn (Invariants: Ví dụ: Số dư không âm, tổng tiền không đổi, tính đối xứng).
- Bộ sinh dữ liệu mẫu (Arbitrary Generators: Chuỗi ký tự, số thực, đối tượng phức tạp).

**Điều kiện tiên quyết:**
- Hàm cần kiểm thử phải là hàm thuần khiết (Pure function) hoặc có thể cô lập trạng thái không gây tác dụng phụ khó kiểm soát.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tập Trung Vào Bất Biến Thay Vì Kết Quả Cố Định**: Thay vì kiểm tra `add(2, 3) === 5`, kiểm tra thuộc tính giao hoán: `add(a, b) === add(b, a)` với mọi `a, b`.
- **Luôn Kiểm Tra Roundtrip Cho Các Parser/Serializer**: Bất kỳ hàm nào biến đổi định dạng (JSON, Tokenizer, Encryption) đều phải đảm bảo `decode(encode(x)) === x`.
- **Cố Định Hạt Giống (Seed Reproducibility)**: Khi một bài kiểm thử thuộc tính thất bại, công cụ phải in ra giá trị hạt giống (Seed value) để có thể tái hiện chính xác lỗi đó trong lần chạy tiếp theo.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Ứng dụng sập khi nhận chuỗi emoji kết hợp (Zero-Width Joiner) hoặc Unicode RTL**: Unit test thông thường bỏ sót -> Property test tự động sinh chuỗi ký tự Unicode ngẫu nhiên và phát hiện lỗi tràn mảng ký tự.
- **Hàm chia cho 0 gây crash tiến trình**: Property test sinh số nguyên `min=0` làm lộ lỗi thiếu validation đầu vào.

## 6. Step-by-Step Execution Workflow
1. Xác định bất biến cốt lõi của bài toán (Properties): Tính đối xứng đảo ngược (Roundtrip), Tính giao hoán, Tính kết hợp, hoặc Bất biến về giá trị biên.
2. Xây dựng bộ sinh dữ liệu ngẫu nhiên (Smart Generators/Arbitraries) mô phỏng miền dữ liệu thực tế.
3. Viết kịch bản kiểm thử thuộc tính: Cho phép framework chạy 100 đến 1,000 lần với các đầu vào ngẫu nhiên khác nhau trên mỗi lần chạy.
4. Khi phát hiện một ca kiểm thử bị lỗi, quan sát cơ chế Shrinking của công cụ tự động cắt gọt dữ liệu về giá trị tối giản nhất làm sập hệ thống (ví dụ: chuỗi rỗng `""`, số 0, hoặc ký tự `\0`).
5. Phân tích nguyên nhân gốc, sửa chữa mã nguồn nghiệp vụ để xử lý ca biên đó.
6. Tái kiểm tra và cố định ca lỗi vừa tìm được thành một unit test hồi quy vĩnh viễn.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// test/money-roundtrip.test.ts using fast-check
import { describe, it } from 'vitest';
import * as fc from 'fast-check';
import { serializeMoney, deserializeMoney } from '../src/money';

describe('Money Serialization Invariants', () => {
  it('satisfies roundtrip invariant: deserialize(serialize(x)) == x', () => {
    fc.assert(
      fc.property(
        fc.record({
          amountInCents: fc.bigInt({ min: 0n, max: 1_000_000_000_000n }),
          currency: fc.constantFrom('USD', 'EUR', 'VND', 'JPY')
        }),
        (money) => {
          const serialized = serializeMoney(money);
          const restored = deserializeMoney(serialized);
          return restored.amountInCents === money.amountInCents && restored.currency === money.currency;
        }
      ),
      { numRuns: 500 }
    );
  });
});
```

### Lệnh xác minh & thực thi:
- Chạy kiểm thử thuộc tính bằng fast-check (Node): `npx vitest run tests/properties/`
- Chạy kiểm thử thuộc tính bằng Hypothesis (Python): `pytest tests/test_properties.py`
- Chạy kiểm thử proptest (Rust): `cargo test --test proptest`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Mỗi thuộc tính được kiểm chứng qua tối thiểu 100 lần sinh ngẫu nhiên thành công.
- QG-05: 100% các bất biến hệ thống được bảo toàn, không có exception chưa được xử lý.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Giới hạn kích thước tối đa của bộ sinh ngẫu nhiên để tránh hiện tượng kiểm thử gây cạn kiệt bộ nhớ RAM (OOM) trên máy CI.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Bộ kiểm thử thuộc tính (`tests/properties/*.test.ts`).
- Danh sách các bất biến hệ thống được tài liệu hóa rõ ràng.
- Báo cáo thu nhỏ ca lỗi (Shrunk failing examples) nếu phát hiện khiếm khuyết.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-property-based-testing**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
