---
name: dex-api-pagination-cursors
description: Engineer high-performance cursor-based and keyset pagination APIs, eliminating OFFSET performance degradation on millions of rows, handling opaque cursor token encoding, and ensuring stable bidirectional scrolling. Use when designing high-throughput data APIs, activity feeds, or audit log query interfaces.
---

# dex-api-pagination-cursors

## 1. Purpose & Scope
Thiết kế và hiện thực hóa các giao diện lập trình phân trang dựa trên con trỏ (Cursor-Based Pagination) và phân trang Keyset hiệu năng cao; triệt tiêu hoàn toàn sự suy giảm hiệu năng nghiêm trọng của phân trang truyền thống `OFFSET` trên bảng dữ liệu hàng chục triệu bản ghi; xử lý mã hóa mã con trỏ mờ (Opaque Cursors) và đảm bảo tính ổn định của thứ tự dữ liệu khi có bản ghi mới chèn vào.

## 2. When to Use
- Khi xây dựng API truy vấn bảng dữ liệu lớn (nhật ký giao dịch, bảng log, bảng tin tức feeds) vượt quá 100,000 dòng.
- Khi người dùng phản ánh trang thứ 1,000 tải quá chậm hoặc gây quá tải CPU của cơ sở dữ liệu.
- Khi cần hỗ trợ cuộn trang vô tận hai chiều (Bidirectional Infinite Scroll) mà không bị trùng lặp hoặc sót bản ghi.

## 3. When NOT to Use
- Khi bảng dữ liệu nhỏ dưới 500 bản ghi đơn giản.
- Khi người dùng có nhu cầu nhảy cóc trực tiếp đến một số trang bất kỳ (ví dụ: 'Nhảy đến trang 42').

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cơ sở dữ liệu quan hệ (PostgreSQL, MySQL) có chỉ mục (Index) trên các cột sắp xếp (ví dụ: `created_at, id`), kiến thức về toán tử so sánh tuple.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **OFFSET Inefficiency:** Lệnh `OFFSET 100000 LIMIT 20` buộc cơ sở dữ liệu phải đọc quét qua 100,020 bản ghi rồi mới vứt bỏ 100,000 bản ghi đầu, gây lãng phí IO.
- **Keyset Comparison:** Sử dụng trực tiếp chỉ mục để nhảy đến bản ghi tiếp theo: `WHERE (created_at, id) < (:last_created_at, :last_id) ORDER BY created_at DESC, id DESC LIMIT 20`.
- **Opaque Base64 Cursor:** Đóng gói các giá trị con trỏ thành một chuỗi mã hóa URL-safe base64 để giấu cấu trúc cơ sở dữ liệu nội bộ.

## 6. Step-by-Step Execution Workflow
1. Xác định bộ khóa sắp xếp xác định (Deterministic Tie-breaker), kết hợp cột thời gian và khóa chính `(created_at, id)`.
2. Tạo chỉ mục phức hợp (Composite Index) trên các cột sắp xếp.
3. Giải mã chuỗi con trỏ `after` nhận được từ client để lấy ra mốc giá trị cuối cùng.
4. Viết câu lệnh SQL lọc dữ liệu sử dụng toán tử so sánh tuple kết hợp với `LIMIT`.
5. Mã hóa bản ghi cuối cùng của kết quả trả về thành mã con trỏ `nextCursor` cho trang tiếp theo.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Keyset Cursor Pagination Implementation
export function encodeCursor(createdAt: Date, id: string): string {
  return Buffer.from(JSON.stringify([createdAt.toISOString(), id])).toString('base64url');
}

export function decodeCursor(cursor: string): [Date, string] {
  const [dateStr, id] = JSON.parse(Buffer.from(cursor, 'base64url').toString('utf-8'));
  return [new Date(dateStr), id];
}

// SQL Query Example:
// SELECT * FROM transactions 
// WHERE (created_at, id) < ($1, $2)
// ORDER BY created_at DESC, id DESC 
// LIMIT 21;
```

## 8. Anti-Patterns & Common Traps
- Sử dụng `LIMIT 20 OFFSET 500000` trên bảng lớn khiến database bị treo nghẽn IO đĩa trong hàng chục giây.
- Chỉ sắp xếp theo `created_at` mà không có trường khóa phụ (Tie-breaker `id`), dẫn đến việc các bản ghi có cùng mili-giây bị sót ngẫu nhiên giữa các trang.
- Để lộ ID tự tăng (Auto-increment ID) thô trong tham số URL thay vì mã hóa thành chuỗi cursor an toàn.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Thời gian thực thi truy vấn trang thứ 1,000 tương đương với trang số 1 (<10ms).
- QG-02: Không có bản ghi nào bị hiển thị lặp lại hoặc bị bỏ sót khi có dữ liệu mới chèn vào đầu bảng.
- QG-03: 100% các câu truy vấn phân trang đều tận dụng được Composite Index đã thiết lập.

## 10. Security & Safety Boundaries
- Kiểm tra và xác thực tính hợp lệ của chuỗi con trỏ đầu vào để ngăn chặn các cuộc tấn công SQL Injection hoặc làm sập tiến trình qua lỗi JSON parse.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module phân trang con trỏ `CursorPaginationHelper.ts`.
1. Tài liệu đặc tả API chuẩn REST / GraphQL với con trỏ.

## 13. Related & Complementary Skills
- [`dex-database-query-plans`](.agents/skills/dex-database-query-plans/SKILL.md)
- [`dex-virtualized-infinite-lists`](.agents/skills/dex-virtualized-infinite-lists/SKILL.md)
- [`dex-api-engineering`](.agents/skills/dex-api-engineering/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Bảng nhật ký kiểm toán hệ thống có 25 triệu dòng dữ liệu. Mỗi khi nhân viên mở trang 500 để tra cứu lịch sử, server cơ sở dữ liệu ngốn 100% CPU do lệnh OFFSET quét qua 20 triệu dòng. Kỹ sư kích hoạt `dex-api-pagination-cursors`, chuyển sang dùng Keyset Pagination dựa trên `(timestamp, id)`, giúp tốc độ tải trang từ 14 giây giảm xuống chỉ còn 8 mili-giây.
