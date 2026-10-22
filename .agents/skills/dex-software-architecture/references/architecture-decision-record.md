# Architecture Decision Record (ADR) Template & Guidelines

## 1. Mục đích của ADR
Ghi lại các quyết định kỹ thuật quan trọng trong dự án, giải thích bối cảnh, các giải pháp đã được cân nhắc, lý do đưa ra lựa chọn và các đánh đổi (trade-offs) kèm theo. Giúp các kỹ sư và AI Agent về sau không tự ý đảo ngược hoặc thắc mắc tại sao hệ thống lại được thiết kế như vậy.

---

## 2. ADR Standard Template

```markdown
# ADR-[NUMBER]: [TIÊU ĐỀ NGẮN GỌN VỀ QUYẾT ĐỊNH]

- **Trạng thái**: [PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED]
- **Ngày quyết định**: YYYY-MM-DD
- **Người đề xuất**: [Tên Kỹ sư / AI Agent]
- **Phạm vi tác động**: [Toàn hệ thống | Module cụ thể | Database layer]

---

### 1. Bối cảnh & Vấn đề (Context)
Mô tả tình huống thực tế dẫn đến quyết định này. Đâu là thách thức kỹ thuật hoặc ràng buộc kinh doanh đang gặp phải?

### 2. Các Lựa chọn Đã Cân Nhắc (Options Considered)
- **Lựa chọn A**: [Mô tả tóm tắt, ưu điểm và nhược điểm]
- **Lựa chọn B**: [Mô tả tóm tắt, ưu điểm và nhược điểm]
- **Lựa chọn C**: [Mô tả tóm tắt, ưu điểm và nhược điểm]

### 3. Quyết Định Được Chọn (Decision)
Chúng tôi quyết định chọn [Lựa chọn X] vì những lý do then chốt sau:
1. ...
2. ...

### 4. Hệ quả & Đánh đổi (Consequences)
- **Mặt tích cực (Positive)**: Những lợi ích rõ rệt đạt được (hiệu năng, độ đơn giản, thời gian ra mắt).
- **Mặt tiêu cực / Rủi ro (Negative/Trade-offs)**: Những điểm cần lưu ý hoặc chi phí phải trả.
- **Biện pháp giảm thiểu rủi ro (Mitigation)**: Cách kiểm soát các hạn chế đó.

### 5. Tiêu chí Kiểm chứng (Verification)
Cách thức kiểm tra để xác nhận quyết định này phát huy tác dụng trong thực tế (Benchmark, Unit test, Linting rule).
```
