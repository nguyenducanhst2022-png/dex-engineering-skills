---
name: dex-reproducible-benchmarking
description: Design, isolate, measure, and statistically analyze software benchmarks with controlled noise, CPU pinning, warmups, and variance tracking. Use when making performance-critical claims, optimizing algorithms, or preventing regressions.
---

# dex-reproducible-benchmarking

## 1. Purpose & Scope
Thiết kế, cô lập môi trường và đo lường benchmark hiệu năng có tính tái lập cao (reproducible); kiểm soát nhiễu hệ thống, thực hiện warmup chu kỳ, cố định CPU core và tính toán phương sai thống kê để bảo đảm các kết luận tối ưu hóa là xác thực.

## 2. When to Use
- Tuyên bố một thuật toán hoặc thư viện mới nhanh hơn giải pháp hiện tại.
- Điều tra xem một bản refactor có gây suy giảm hiệu năng (performance regression) hay không.
- Thiết lập benchmark đường cơ sở (baseline) cho hệ thống trước khi mở rộng quy mô.

## 3. When NOT to Use
- Không đo benchmark trên máy laptop đang cắm sạc/pin chập chờn hoặc đang mở nhiều tab trình duyệt.
- Không benchmark các hàm có network I/O mà không giả lập độ trễ mạng ổn định.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Đoạn mã nguồn hoặc API cần đo lường.
- Bộ dữ liệu mẫu có kích thước chuẩn hóa.
- Công cụ đo chuyên dụng (Criterion.rs, Google Benchmark, pytest-benchmark, Hyperfine).
- **Điều kiện tiên quyết**:
- Môi trường đo lường phải tắt các tác vụ nền không cần thiết (CPU governor đặt ở chế độ performance).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Tái lập (Reproducibility): Chạy 5 lần độc lập vào 5 thời điểm khác nhau phải cho kết quả lệch không quá 3%.
- JIT Compilation & Warmup: Trong Java/Node.js/V8, code cần chạy hàng ngàn lần trước khi đo để engine JIT tối ưu hóa xong.
- Độ lệch chuẩn (Standard Deviation) và P99: Giá trị trung bình (Mean) thường che giấu các đột biến nghiêm trọng.
- **Quy tắc quyết định kỹ thuật**:
- Nếu độ lệch chuẩn giữa các lần đo > 5%: loại bỏ kết quả vì môi trường quá nhiễu, chạy lại sau khi khóa tải nền.
- Đánh giá tối ưu hóa thành công khi hiệu năng tăng tối thiểu 10% với độ tin cậy thống kê 95% (p < 0.05).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Trình biên dịch (Compiler) tối ưu hóa loại bỏ toàn bộ đoạn code đo lường (Dead Code Elimination) do kết quả không được sử dụng.

## 6. Step-by-Step Execution Workflow
1. Chuẩn bị môi trường đo: cố định tần số CPU hoặc sử dụng dedicated CI runner.
2. Viết benchmark harness sử dụng framework chuẩn, tiêu thụ kết quả (black box) để tránh Dead Code Elimination.
3. Thực hiện giai đoạn Warmup đầy đủ.
4. Thu thập hàng trăm iterations và ghi nhận phân phối thời gian (P50, P90, P99).
5. So sánh trực tiếp với baseline bằng công cụ phân tích thống kê.
6. Lưu trữ kết quả có thể so sánh trong kho dữ liệu benchmark.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
def test_json_parse_speed(benchmark):
    payload = generate_standard_json_payload(1000)
    # Đo thời gian hàm chạy lặp lại nhiều lần kèm warmup tự động
    result = benchmark(parse_json_fast, payload)
    assert result is not None
```

### Lệnh xác minh & thực thi:
```bash
pytest tests/benchmarks/ --benchmark-only --benchmark-compare --benchmark-autosave
```

## 8. Anti-Patterns & Common Traps
- Đo thời gian chỉ bằng `console.time()` hoặc `time.time()` cho một lần chạy duy nhất.
- So sánh benchmark chạy trên máy tính cá nhân với máy chủ sản xuất.

## 9. Quality Gates & Acceptance Criteria
- Mọi tối ưu hóa phải có biểu đồ phân phối trước/sau chứng minh giảm latency P99.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Không tải dữ liệu nhạy cảm của khách hàng làm tập mẫu cho public benchmarks.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- File báo cáo benchmark (JSON, biểu đồ SVG/HTML).
- Cam kết hiệu năng với số liệu sai số thống kê rõ ràng.

## 13. Related & Complementary Skills
dex-performance-optimization, dex-differential-testing, dex-jvm-performance-diagnostics

## 14. Realistic Usage Example
### Tình huống thực tế:
Một kỹ sư khẳng định viết lại parser bằng WebAssembly giúp tăng tốc độ 3 lần. Sau khi chạy benchmark chuẩn với Criterion và loại bỏ chi phí FFI overhead, kết quả thực tế cho thấy với payload nhỏ (<1KB) bản WASM thực chất chậm hơn JS gốc 20%.
