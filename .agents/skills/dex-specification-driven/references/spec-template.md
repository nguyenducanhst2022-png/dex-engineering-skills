# Technical Specification (SPEC) Standard Template

## 1. Giới thiệu
Mẫu đặc tả kỹ thuật chuẩn hóa cho các tính năng phần mềm trong dự án áp dụng DEX Engineering Skills Pack.

---

```markdown
# SPEC-[NUMBER]: [TÊN TÍNH NĂNG / FEATURE NAME]

- **Trạng thái**: [DRAFT | REVIEWED | APPROVED | IMPLEMENTED]
- **Tác giả**: [Kỹ sư / AI Agent]
- **Ngày tạo**: YYYY-MM-DD
- **Phiên bản mục tiêu**: vX.Y.Z

---

## 1. Mục Tiêu & Giá Trị Kinh Doanh (Goal & Objective)
- Giải quyết bài toán gì cho người dùng hoặc hệ thống?
- Tại sao cần làm tính năng này vào thời điểm hiện tại?

## 2. Phạm Vi Thực Hiện (Scope)
- **Trong phạm vi (In-scope)**: Những gì CHẮC CHẮN sẽ làm trong phiên bản này.
- **Ngoài phạm vi (Out-of-scope)**: Những gì TẠM THỜI CHƯA LÀM để tránh phình to quy mô (YAGNI).

## 3. Kiến Trúc & Hợp Đồng Kỹ Thuật (Architecture & Contracts)
### 3.1. API Endpoints
- `METHOD /path/to/resource`
- **Request Body / Params Schema**: [JSON Schema / Type definition]
- **Response Format**: [JSON Success / Error responses]

### 3.2. Cấu Trúc Dữ Liệu (Database Schema)
- Bảng mới hoặc cột mới cần thêm.
- Ràng buộc và kiểu dữ liệu chi tiết.

## 4. Tiêu Chí Nghiệm Thu (Acceptance Criteria)
Mỗi tiêu chí phải rõ ràng, có thể kiểm chứng độc lập (Given - When - Then):

- [ ] **AC-01**: [Mô tả kịch bản thành công chính]
  - *Given*: ...
  - *When*: ...
  - *Then*: ...
- [ ] **AC-02**: [Mô tả kịch bản xử lý dữ liệu không hợp lệ]
  - *Given*: ...
  - *When*: ...
  - *Then*: ...
- [ ] **AC-03**: [Mô tả kịch bản xử lý lỗi ngoại lệ / biên]
  - *Given*: ...
  - *When*: ...
  - *Then*: ...

## 5. Rủi Ro & Kế Hoạch Kiểm Thử (Risks & Test Plan)
- Các module có nguy cơ bị ảnh hưởng tiêu cực.
- Danh sách Unit Tests, Integration Tests và E2E Tests cần viết.
```
