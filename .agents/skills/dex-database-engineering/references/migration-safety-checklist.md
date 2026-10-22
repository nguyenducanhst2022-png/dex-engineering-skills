# Safe Database Migration Checklist & Anti-Patterns

## 1. Safe Migration Checklist
- [ ] **Khả năng đảo ngược**: File migration có đầy đủ cả hàm `UP` và hàm `DOWN` (hoặc cú pháp rollback tương đương).
- [ ] **Kiểm tra dữ liệu lớn**: Nếu bảng có trên 100,000 dòng, có kiểm tra xem lệnh DDL có gây Full Table Lock (khóa bảng hoàn toàn) hay không?
- [ ] **Thêm cột an toàn**: Khi thêm cột mới, cột đó phải cho phép `NULL` hoặc có giá trị `DEFAULT` hợp lệ. Tuyệt đối không thêm cột `NOT NULL` mà không có giá trị mặc định trên bảng đang có sẵn dữ liệu.
- [ ] **Tạo Index không khóa bảng**: Sử dụng `CREATE INDEX CONCURRENTLY` (PostgreSQL) hoặc `ALGORITHM=INPLACE, LOCK=NONE` (MySQL) để không chặn các truy vấn đọc/ghi của người dùng trong khi index đang được tạo.
- [ ] **Transaction cho DDL**: Nếu cơ sở dữ liệu hỗ trợ Transactional DDL (như PostgreSQL), hãy bọc toàn bộ migration trong một transaction để nếu lỗi ở câu lệnh thứ 2 thì câu lệnh thứ 1 sẽ được tự động rollback hoàn toàn.

---

## 2. Các Anti-Pattern Nguy Hiểm Cần Tránh
1. **Đổi tên cột trực tiếp (RENAME COLUMN)**: Ứng dụng phiên bản cũ vẫn đang truy vấn tên cột cũ sẽ bị sập ngay lập tức.
   - *Cách làm đúng*: Thêm cột mới → Đồng bộ dữ liệu từ cột cũ sang cột mới qua code/trigger → Deploy code trỏ sang cột mới → Xóa cột cũ ở release tiếp theo.
2. **Chạy script di chuyển dữ liệu nặng (Data Backfill) trong cùng migration DDL**:
   - Chạy vòng lặp cập nhật hàng triệu bản ghi trong một transaction duy nhất sẽ làm đầy WAL log và khóa bảng hàng giờ.
   - *Cách làm đúng*: Tách DDL schema ra riêng. Data backfill chạy bằng background worker theo từng batch nhỏ (ví dụ 1000 records/batch).
