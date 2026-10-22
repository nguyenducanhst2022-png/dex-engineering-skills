---
name: dex-concurrency-state
description: Concurrency control, distributed locks, race condition elimination, atomic state transitions, and deadlock prevention. Guarantees consistency under concurrent operations and high traffic. Use when managing shared mutable state, handling inventory deductions, or preventing double-spending.
---

# DEX Concurrency & State Management

## 1. Purpose
Kiểm soát tác vụ đồng thời (Concurrency Control) và quản lý trạng thái dùng chung (Shared State) an toàn trong các hệ thống phân tán hoặc đa luồng; loại bỏ hoàn toàn các lỗi điều kiện tranh định (Race Conditions), chống hiện tượng mất mát dữ liệu (Lost Updates) và ngăn ngừa bế tắc (Deadlocks).

Quy trình quản lý đồng thời chuẩn:
`Phân tích luồng xử lý → Xác định trạng thái dùng chung → Phát hiện Race Condition → Thiết kế đồng bộ → Triển khai giải pháp → Kiểm thử tải đồng thời → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Khi nhiều người dùng hoặc tác vụ cùng truy cập và cập nhật một vùng dữ liệu chung tại cùng một thời điểm, dữ liệu phải luôn đảm bảo tính chính xác, nhất quán và tuyệt đối không xảy ra xung đột.**
Ghi nhớ sống còn: **Không kiểm soát đồng thời = Dữ liệu bị ghi đè + Bán lố hàng tồn kho + Trừ tiền sai lệch.**

## 2. When to Use
- Khi xử lý trừ số lượng hàng tồn kho (Inventory decrement) trong các đợt flash sale.
- Khi xử lý giao dịch tài chính, số dư ví điện tử (Double spending prevention).
- Khi tạo số thứ tự tự tăng duy nhất (Counter/Sequence generation) không dùng auto-increment của database.
- Khi chia sẻ tài nguyên giữa nhiều tiến trình worker thông qua Redis hoặc cơ chế khóa phân tán (Distributed Locks).

## 3. When Not to Use
- Ứng dụng xử lý dữ liệu bất biến (Immutable data) hoặc chỉ đọc (Read-only operations).
- Các tác vụ cục bộ trong một luồng riêng biệt không chia sẻ biến hoặc bộ nhớ với bất kỳ ai.

## 4. Inputs
- Vùng dữ liệu chia sẻ (Shared State: bản ghi database, khóa redis, biến toàn cục).
- Số lượng tác vụ đồng thời dự kiến (Concurrent requests / Workers).
- Mức độ cô lập giao dịch mong muốn (Isolation Level: Read Committed, Repeatable Read, Serializable).

## 5. Workflow

### Bước 1: Nhận Diện Trạng Thái Dùng Chung (Identify Shared Mutable State)
- Rà soát các luồng nghiệp vụ:
  - Nơi nào thực hiện chuỗi: `ĐỌC DỮ LIỆU (Read) → TÍNH TOÁN (Compute) → GHI ĐÈ DỮ LIỆU (Write)`?
  - Ví dụ: `const stock = await getStock(); if (stock > 0) await setStock(stock - 1);` ← **ĐÂY LÀ ĐIỂM CHẾT VÌ RACE CONDITION!**

### Bước 2: Lựa Chọn Cơ Chế Đồng Bộ Hóa Phù Hợp (Concurrency Strategy)
- Tùy thuộc vào bản chất bài toán:
  - **Phương án 1: Atomic Database Updates (Khuyến nghị ưu tiên cao nhất)**:
    - Thay vì đọc rồi ghi, thực thi câu lệnh nguyên tử ngay tại DB:
      `UPDATE products SET stock = stock - 1 WHERE id = $1 AND stock > 0;`
  - **Phương án 2: Optimistic Locking (Khóa lạc quan)**:
    - Sử dụng cột phiên bản: `UPDATE products SET stock = $new_stock, version = version + 1 WHERE id = $1 AND version = $old_version;`
    - Nếu số dòng ảnh hưởng = 0 (có người khác đã sửa trước) → Tự động thử lại hoặc báo xung đột.
  - **Phương án 3: Pessimistic Locking (Khóa bi quan)**:
    - Khóa bản ghi trong transaction: `SELECT * FROM products WHERE id = $1 FOR UPDATE;`
  - **Phương án 4: Distributed Lock (Khóa phân tán dùng Redis Redlock)**:
    - Áp dụng khi logic nghiệp vụ phức tạp kéo dài qua nhiều hệ thống khác nhau.

### Bước 3: Phòng Ngừa Bế Tắc (Deadlock Prevention)
- Khi một giao dịch cần khóa nhiều tài nguyên khác nhau: Luôn khóa các tài nguyên theo một **thứ tự cố định thống nhất** (ví dụ sắp xếp theo `ID` tăng dần).
- Luôn đặt thời gian chờ khóa (Lock timeout / TTL) để tránh treo vĩnh viễn nếu tiến trình giữ khóa bị sập.

### Bước 4: Kiểm Thử Tải Đồng Thời (Concurrent Stress Testing)
- Viết bài kiểm thử tự động bắn hàng chục/hàng trăm requests đồng thời (dùng `Promise.all` hoặc công cụ load test):
  - Ví dụ: Sản phẩm có 10 sản phẩm trong kho. Bắn đồng thời 50 requests mua hàng.
  - Kết quả mong đợi: Đúng chính xác 10 đơn mua thành công, 40 đơn báo hết hàng, tồn kho cuối cùng bằng đúng 0 (không bao giờ được âm).

### Bước 5: Ổn Định & Lưu Git (Stabilize & Commit)
- Ghi nhận commit: `fix(inventory): eliminate race condition using atomic decrement with conditional where clause`.

## 6. Quality Gates
- **QG-02 (AC Compliant Under Load)**: Kết quả tính toán chính xác tuyệt đối ngay cả khi chịu tải đồng thời.
- **QG-05 (Concurrency Test PASS)**: Kịch bản stress test đồng thời đạt 100% PASS, không có hiện tượng over-selling.
- **QG-06 (No Deadlocks)**: Không phát sinh lỗi Deadlock hoặc timeout lock trong quá trình chạy.

## 7. Safety Rules
- **Cấm Tuyệt Đối Check-Then-Act Ngoài Database**: Tuyệt đối không bao giờ kiểm tra điều kiện ở code Node.js/Python rồi mới cập nhật DB trên hai câu lệnh rời rạc mà không có Lock hoặc Atomic condition.
- **Luôn Có TTL Cho Distributed Lock**: Bất kỳ khóa Redis nào cũng bắt buộc phải có thời gian sống (TTL / Expire time) để tự giải phóng nếu server bị mất điện.
- **Giữ Giao Dịch Ngắn Nhất Có Thể**: Không bao giờ thực hiện các lời gọi mạng HTTP bên thứ ba bên trong một Database Transaction đang giữ khóa bảng/dòng.

## 8. Expected Outputs
1. Mã nguồn xử lý đồng thời an toàn (Atomic updates / Distributed locks).
2. Kịch bản kiểm thử tải đồng thời (Concurrent test suite).
3. Bằng chứng kiểm thử chứng minh dữ liệu nhất quán 100%.

## 9. Failure Handling
- Nếu phát hiện deadlock xuất hiện trong log database: Lập tức rà soát thứ tự truy cập bảng của các câu truy vấn và chuẩn hóa lại thứ tự khóa thống nhất.

## 10. Completion Criteria
- Trạng thái dùng chung không bị sai lệch dưới tải đồng thời.
- Test case kiểm tra race condition chạy thành công và được lưu vào Git.

---

## Real-world Example
Trừ tồn kho sản phẩm an toàn chống race condition trong PostgreSQL:
```typescript
async function purchaseItem(productId: string, quantity: number): Promise<boolean> {
  const result = await db.query(
    `UPDATE products 
     SET stock = stock - $1 
     WHERE id = $2 AND stock >= $1 
     RETURNING stock`,
    [quantity, productId]
  );
  // Nếu không dòng nào được cập nhật nghĩa là không đủ hàng tồn kho
  return (result.rowCount ?? 0) > 0;
}
```
Kiểm thử bắn 100 request đồng thời tranh mua 5 sản phẩm: Đúng 5 request trả về `true`, 95 request trả về `false`, tồn kho còn đúng 0.
