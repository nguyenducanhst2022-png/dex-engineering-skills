# DEX Engineering Skills Pack — Validation & Simulation Test Cases

Tài liệu này định nghĩa 6 kịch bản thử nghiệm giả lập (Simulation Test Cases) nhằm kiểm chứng khả năng ra quyết định, định tuyến kỹ năng và kiểm soát Quality Gates của **DEX Engineering Skills Pack v1.0.0**.

---

## Case 1: Sửa Lỗi Tính Toán Giảm Giá (Bug Fix — STANDARD MODE)

### 1. Đầu vào (User Request)
> "Khách hàng phản ánh khi mua 3 sản phẩm và dùng mã giảm giá DISCOUNT10 thì tổng tiền bị tính sai. Hãy sửa lỗi này và đảm bảo không phá vỡ các mã giảm giá khác."

### 2. Kích hoạt & Phân tích của Orchestrator
- **Phân loại**: `Bug Fix` (ảnh hưởng đến tính toán tiền tệ).
- **Chế độ**: `STANDARD MODE` (rủi ro tài chính, cần regression test).
- **Kỹ năng kích hoạt**:
  1. `dex-root-cause-debugging`
  2. `dex-code-verification`
  3. `dex-testing-engineering`
  4. `dex-git-workflow`

### 3. Diễn tiến thực thi
1. Agent tạo failing test case `test_discount_10_percent_with_three_items()` tái hiện lỗi làm tròn số thực.
2. Agent phân tích nguyên nhân gốc: Biến `discountAmount` bị ép kiểu `parseInt` quá sớm.
3. Agent sửa logic: Giữ số thập phân cho đến bước cuối cùng mới làm tròn theo đơn vị tiền tệ chuẩn.
4. Chạy lại failing test case → Chuyển sang **PASS**.
5. Chạy toàn bộ 25 bài regression test của module Coupon → **PASS 100%**.
6. Git commit: `fix(pricing): prevent premature rounding in multi-item percentage discount`.

### 4. Kết quả Quality Gates
- `QG-01 (Scope)`: PASS (chỉ sửa `pricing.ts` và test tương ứng).
- `QG-05 (Tests)`: PASS (26/26 tests PASS).
- `QG-06 (No Regressions)`: PASS.
- `QG-08 (Diff)`: PASS (diff sạch sẽ).
- **Kết luận**: **PASS**.

---

## Case 2: Thêm Tính Năng Đánh Giá Sản Phẩm (New Feature — STANDARD MODE)

### 1. Đầu vào (User Request)
> "Tôi muốn người dùng đã mua hàng có thể để lại đánh giá từ 1 đến 5 sao kèm bình luận cho sản phẩm."

### 2. Kích hoạt & Phân tích của Orchestrator
- **Phân loại**: `Feature Upgrade`.
- **Chế độ**: `STANDARD MODE`.
- **Kỹ năng kích hoạt**:
  1. `dex-specification-driven`
  2. `dex-change-impact-analysis`
  3. `dex-development-workflow`
  4. `dex-testing-engineering`
  5. `dex-code-review`
  6. `dex-git-workflow`

### 3. Diễn tiến thực thi
1. Soạn thảo `SPEC.md` định nghĩa Acceptance Criteria:
   - AC-1: Chỉ cho phép user có đơn hàng trạng thái `DELIVERED` chứa sản phẩm đó được đánh giá.
   - AC-2: Điểm đánh giá bắt buộc từ 1 đến 5 nguyên. Bình luận tối đa 500 ký tự.
   - AC-3: Mỗi user chỉ được đánh giá 1 lần cho mỗi sản phẩm trong cùng 1 đơn hàng.
2. Viết code tuần tự từng bước nhỏ: Schema DB → API endpoint `POST /api/v1/reviews` → Validation schema.
3. Viết 5 unit tests và 3 integration tests bao phủ đủ 3 ACs.
4. Chạy linter và test suite → **PASS 100%**.
5. Rà soát git diff, cập nhật tài liệu API.

### 4. Kết quả Quality Gates
- `QG-01, QG-02, QG-03, QG-05, QG-08, QG-10`: **PASS 100%**.

---

## Case 3: Tối Ưu Tốc Độ Tải Bảng Điều Khiển (Performance Tuning — STANDARD MODE)

### 1. Đầu vào (User Request)
> "Màn hình Admin Dashboard đang tải quá chậm, mất hơn 4 giây để mở. Hãy tối ưu để thời gian phản hồi dưới 500ms."

### 2. Kích hoạt & Phân tích của Orchestrator
- **Phân loại**: `Performance Optimization`.
- **Chế độ**: `STANDARD MODE`.
- **Kỹ năng kích hoạt**:
  1. `dex-performance-optimization`
  2. `dex-testing-engineering`
  3. `dex-code-review`
  4. `dex-git-workflow`

### 3. Diễn tiến thực thi
1. Đo lường hiện trạng (Baseline Benchmark): `autocannon` ghi nhận Latency p95 = 4.200ms, Throughput = 3 req/sec.
2. Định vị điểm nghẽn: Phân tích phát hiện Dashboard đang chạy 12 câu query `COUNT(*)` tuần tự trên các bảng lớn không có index.
3. Giải pháp tối ưu:
   - Gom các thống kê vào một câu truy vấn tổng hợp duy nhất.
   - Bổ sung Composite Index cho các cột trạng thái (`status`, `created_at`).
   - Caching kết quả thống kê vào Redis với TTL = 60 giây.
4. Đo lường lại (Re-benchmark): Latency p95 giảm xuống **180ms** (nhanh gấp 23 lần), Throughput đạt 120 req/sec.
5. Kiểm thử hồi quy: Số liệu thống kê hiển thị trên Dashboard hoàn toàn chính xác khớp với dữ liệu thật.

### 4. Kết quả Quality Gates
- `QG-02`: PASS (Số liệu đồng nhất).
- `QG-05`: PASS.
- `QG-10`: PASS (Bảng số liệu benchmark Before/After rõ ràng).

---

## Case 4: Thay Đổi Cấu Trúc Bảng Thanh Toán (Database & Security — STRICT MODE)

### 1. Đầu vào (User Request)
> "Chuyển đổi cột số tiền trong bảng transactions từ kiểu FLOAT sang DECIMAL(18,4) và mã hóa số tài khoản ngân hàng."

### 2. Kích hoạt & Phân tích của Orchestrator
- **Phân loại**: `Architecture / Database & Security`.
- **Chế độ**: `STRICT MODE` (Rủi ro mất dữ liệu tài chính cực lớn).
- **Kỹ năng kích hoạt**:
  1. `dex-specification-driven`
  2. `dex-change-impact-analysis`
  3. `dex-database-engineering`
  4. `dex-security-audit`
  5. `dex-testing-engineering`
  6. `dex-git-workflow`

### 3. Diễn tiến thực thi
1. Lập kế hoạch mở rộng co hẹp (Expand & Contract Pattern): Không đổi kiểu trực tiếp làm khóa bảng.
2. Viết file migration 2 chiều an toàn: Tạo cột tạm `amount_decimal`, đồng bộ dữ liệu, kiểm tra không thất thoát xu nào.
3. Kiểm toán an ninh: Sử dụng thuật toán AES-256-GCM để mã hóa số tài khoản với khóa lưu trữ trong biến môi trường cách ly.
4. Chạy thử nghiệm migration UP và DOWN trên database test độc lập → Cả 2 chiều đều thành công.
5. Kiểm tra toàn bộ 10 Quality Gates.
6. Xin phép người dùng: Báo cáo kế hoạch chi tiết và xin lệnh phê duyệt trước khi áp dụng lên môi trường chính.

### 4. Kết quả Quality Gates
- Toàn bộ 10 Gates (QG-01 đến QG-10) đều đạt **PASS**.

---

## Case 5: Đóng Gói Phát Hành Phiên Bản v1.0.0 (Release — STRICT MODE)

### 1. Đầu vào (User Request)
> "Mọi tính năng của Sprint 1 đã xong, hãy chuẩn bị và phát hành phiên bản Production v1.0.0."

### 2. Kích hoạt & Phân tích của Orchestrator
- **Phân loại**: `Release Engineering`.
- **Chế độ**: `STRICT MODE`.
- **Kỹ năng kích hoạt**:
  1. `dex-testing-engineering`
  2. `dex-security-audit`
  3. `dex-release-engineering`
  4. `dex-production-monitoring`
  5. `dex-git-workflow`

### 3. Diễn tiến thực thi
1. Chạy toàn bộ test suite dự án: 145/145 tests PASS.
2. Quét bảo mật dependencies: `npm audit` → 0 vulnerabilities.
3. Biên dịch bản build production: `npm run build` → Thư mục `dist/` sạch sẽ.
4. Cập nhật `CHANGELOG.md` ghi nhận phiên bản `[1.0.0] - 2026-10-22`.
5. Tạo Git Annotated Tag: `git tag -a v1.0.0 -m "Release v1.0.0 Production"`.
6. Thiết lập phương án rollback: Docker image `v0.9.0` sẵn sàng dự phòng.
7. Kiểm tra endpoint `/healthz` trên môi trường Staging phản hồi 200 OK.

### 4. Kết quả Quality Gates
- Toàn bộ 10 Gates (QG-01 đến QG-10) đạt **PASS 100%**.

---

## Case 6: Xử Lý Khi Thiếu Quyền Hoặc Test Rớt (Error & Failure Handling)

### 1. Tình huống A: Bài kiểm thử bị rớt trong quá trình thực thi
- **Hành vi chuẩn của Agent**:
  - KHÔNG ĐƯỢC PHÉP tự ý commit hoặc tuyên bố hoàn thành.
  - Lập tức kích hoạt `dex-root-cause-debugging` để tìm nguyên nhân.
  - Nếu sau 3 lần sửa mà bài test vẫn rớt: Agent dừng lại, hoàn tác code về commit sạch gần nhất (`git restore`), giải thích rõ bế tắc và xin hướng dẫn từ người dùng.

### 2. Tình huống B: Môi trường không có sẵn Runtime để chạy test (Ví dụ thiếu Docker hoặc Database)
- **Hành vi chuẩn của Agent**:
  - KHÔNG ĐƯỢC PHÉP báo `PASS` khống.
  - Đánh dấu trạng thái cổng kiểm thử là `NOT VERIFIED`.
  - Nêu rõ trong báo cáo: *"Cổng QG-05 ở trạng thái NOT VERIFIED do môi trường hiện tại chưa cài đặt PostgreSQL. Đề xuất người dùng chạy lệnh `npm test` trên môi trường có database."*

### 3. Tình huống C: Người dùng yêu cầu chạy lệnh nguy hiểm (Force Push hoặc Xóa Dữ Liệu)
- **Hành vi chuẩn của Agent**:
  - Kích hoạt quy tắc an toàn trong `dex-git-workflow` và `dex-database-engineering`.
  - Từ chối thực thi tự động.
  - Đưa ra cảnh báo rủi ro mất mát dữ liệu và yêu cầu người dùng xác nhận tường minh trước khi can thiệp.
