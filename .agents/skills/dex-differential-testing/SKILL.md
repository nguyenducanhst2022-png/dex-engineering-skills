---
name: dex-differential-testing
description: Compare behavior, output equivalence, and performance between two software implementations (legacy vs rewritten, compiler versions, or competing algorithms) across randomized inputs. Use during major refactorings, system migrations, and re-implementations.
---

# dex-differential-testing

## 1. Purpose & Scope
So sánh hành vi, kết quả đầu ra và hiệu năng giữa hai phiên bản triển khai phần mềm (hệ thống cũ vs hệ thống viết lại, thuật toán mới vs thuật toán tham chiếu) trên cùng một tập dữ liệu đầu vào ngẫu nhiên hoặc thực tế nhằm phát hiện sai lệch nhỏ nhất về ngữ nghĩa.

## 2. When to Use
- Thay thế engine tính toán cũ bằng thuật toán mới tối ưu hơn.
- Di chuyển từ cơ sở dữ liệu SQL sang NoSQL hoặc từ ORM này sang ORM khác.
- Nâng cấp phiên bản compiler/runtime lớn (ví dụ Node.js 18 lên 22, Python 3.9 lên 3.12).

## 3. When NOT to Use
- Không dùng khi phiên bản mới cố ý thay đổi hoàn toàn API schema và business logic.
- Không dùng cho các thao tác có side-effect ghi dữ liệu mà không có cơ chế shadow-run/dry-run an toàn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Triển khai nguồn A (Reference/Legacy implementation).
- Triển khai nguồn B (Candidate/New implementation).
- Bộ dữ liệu test cases hoặc generator sinh input ngẫu nhiên.
- **Điều kiện tiên quyết**:
- Cả hai phiên bản đều có thể chạy song song và nhận cùng định dạng input.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Equivalence Oracle: Nếu hai hệ thống có cùng input hợp lệ thì output nghiệp vụ phải tương đương tuyệt đối.
- Dual-run / Shadowing: Gửi đồng thời request đến cả 2 hệ thống và so sánh kết quả diff ngầm mà không ảnh hưởng tới người dùng.
- **Quy tắc quyết định kỹ thuật**:
- Nếu phát hiện bất kỳ sai khác nào về giá trị logic: ghi nhận minimal reproducer và hoãn release.
- Nếu sai khác chỉ là thứ tự các key trong JSON: áp dụng canonical JSON normalizer trước khi so sánh.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Các trường chứa giá trị không tiền định (non-deterministic: timestamps, UUID ngẫu nhiên) gây false diff.

## 6. Step-by-Step Execution Workflow
1. Xác định hàm hoặc endpoint cần so sánh và các trường cần loại trừ (timestamp, trace-id).
2. Xây dựng harness gọi song song cả Implementation A và B.
3. Sinh hàng ngàn inputs ngẫu nhiên (Property-based inputs).
4. Thu thập và so sánh output diff.
5. Thu nhỏ input gây lỗi thành minimal reproduction test case.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
def test_differential_tax_calculation(random_order):
    legacy_result = legacy_tax_engine.calculate(random_order)
    new_result = rust_tax_engine.calculate(random_order)
    assert round(legacy_result.amount, 2) == round(new_result.amount, 2), \
        f'Diff detected for input {random_order}: legacy={legacy_result.amount}, new={new_result.amount}'
```

### Lệnh xác minh & thực thi:
```bash
pytest tests/differential/test_tax_engine.py --count=5000
```

## 8. Anti-Patterns & Common Traps
- Không chuẩn hóa dữ liệu trước khi so sánh (so sánh chuỗi thô thay vì semantic objects).
- Chạy differential test trên database thật mà không rollback transaction.

## 9. Quality Gates & Acceptance Criteria
- 100% kết quả khớp nhau trên 100,000 mẫu dữ liệu kiểm thử.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Khi chạy shadow-traffic với dữ liệu thật, phải mask toàn bộ PII và thẻ tín dụng.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Harness code kiểm thử so sánh.
- Báo cáo phân tích sai lệch và test case hồi quy.

## 13. Related & Complementary Skills
dex-refactoring-mastery, dex-reproducible-benchmarking, dex-unit-testing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty logistics viết lại thuật toán tìm đường đi ngắn nhất từ Python sang C++ để giảm độ trễ. Nhờ differential testing trên 50,000 hành trình giả lập, họ phát hiện trường hợp đường một chiều bị thuật toán C++ xử lý sai lệch so với bản mẫu Python.
