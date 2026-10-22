---
name: dex-internationalization
description: Implement robust internationalization (i18n), localized number/currency formatting (L10n), pluralization rules, RTL layout support, and translation key management. Use when translating web applications, adapting currency formats, or implementing multi-language routing.
---

# dex-internationalization

## 1. Purpose & Scope
Thiết kế và triển khai giải pháp quốc tế hóa (i18n) và địa phương hóa (L10n) chuyên nghiệp; quản lý từ điển bản dịch theo cấu trúc phân cấp, tự động định dạng ngày tháng, tiền tệ, số liệu theo locale người dùng, xử lý các quy tắc số nhiều (Pluralization) phức tạp và hỗ trợ giao diện đọc từ phải sang trái (RTL) khi cần.

## 2. When to Use
- Khi ứng dụng mở rộng phục vụ người dùng đa quốc gia (Tiếng Việt, Tiếng Anh, Tiếng Nhật...). 
- Khi các chuỗi văn bản giao diện đang bị hardcode trực tiếp trong JSX/HTML.
- Khi hiển thị sai định dạng tiền tệ hoặc ngày tháng (ví dụ: hiển thị $1,000 thay vì 1.000 ₫ cho người dùng Việt Nam).

## 3. When NOT to Use
- Ứng dụng nội bộ chỉ phục vụ duy nhất một ngôn ngữ địa phương cố định.
- Xử lý dịch thuật nội dung bài viết động bằng AI (khi đó dùng LLM RAG pipelines).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các ngôn ngữ cần hỗ trợ (ví dụ: `vi`, `en`, `ja`).
- File từ điển bản dịch gốc (JSON / YAML / PO).
- Framework i18n mục tiêu (react-i18next, next-intl, vue-i18n, formatjs).

**Điều kiện tiên quyết:**
- Đã lựa chọn chiến lược phát hiện ngôn ngữ (URL path `/en/about`, Cookie, hoặc `Accept-Language` header).
- Có bộ font chữ hỗ trợ đầy đủ bộ ký tự Unicode của các ngôn ngữ mục tiêu.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Không Nối Chuỗi Thủ Công**: Tuyệt đối không ghép chuỗi dạng `t('you_have') + count + t('items')` vì ngữ pháp các ngôn ngữ khác nhau có cấu trúc đảo ngược; luôn dùng biến nội suy `t('items_count', { count })`.
- **Fallback Luôn Có Sẵn**: Nếu một key chưa được dịch sang tiếng Nhật, hệ thống phải tự động hiển thị bản dịch tiếng Anh thay vì in ra key thô `auth.login.title`.
- **Tách Namespace Theo Tính Năng**: Không dồn toàn bộ 5000 từ của cả dự án vào 1 file `translation.json` khổng lồ gây chậm tốc độ nạp trang.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Thiếu key bản dịch hiển thị mã thô cho khách**: Khách thấy nút bấm hiện `checkout.btn_pay` -> Khắc phục: Chạy script kiểm tra missing keys trong CI/CD trước khi build.
- **Layout vỡ khi đổi sang ngôn ngữ dài**: Tiếng Đức dài gấp 1.5 lần tiếng Anh làm tràn nút bấm -> Khắc phục: Thiết kế component responsive, dùng `min-width` co giãn tự nhiên.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo cấu hình i18n với ngôn ngữ mặc định (fallback locale) an toàn.
2. Tổ chức tệp từ điển bản dịch theo từng namespace (ví dụ: `common.json`, `auth.json`, `checkout.json`).
3. Trích xuất toàn bộ chuỗi hardcode sang translation keys có ý nghĩa ngữ cảnh (`auth.login.submit_button`).
4. Áp dụng API chuẩn `Intl.NumberFormat` và `Intl.DateTimeFormat` cho tiền tệ và ngày tháng.
5. Xử lý quy tắc số nhiều (Pluralization) và biến nhúng (Interpolation) an toàn chống injection.
6. Thiết lập thuộc tính `dir='rtl'` và kiểm tra layout khi người dùng chọn ngôn ngữ Ả Rập/Hebrew.
7. Viết script kiểm tra các translation key bị thiếu (Missing Translation Keys).

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```json
// locales/vi/cart.json
{
  "items_count_one": "Bạn có {{count}} sản phẩm trong giỏ",
  "items_count_other": "Bạn có {{count}} sản phẩm trong giỏ",
  "total_price": "Tổng tiền: {{amount, currency(currency: 'VND')}}"
}
```

### Lệnh xác minh & thực thi:
- Quét tìm key chưa dịch: `npx i18next-parser` hoặc script so sánh keys
- Chạy unit test i18n: `npm test -- src/i18n/i18n.spec.ts`
- Kiểm tra type-safe translations: `npm run type-check`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các translation keys của ngôn ngữ chính có bản dịch tương ứng ở các ngôn ngữ phụ.
- QG-03: 0 chuỗi văn bản UI hardcode bằng tiếng Anh/Việt thô trong component.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Dữ liệu truyền vào biến nội suy của translation key phải được escape chống XSS; cấm dùng interpolation đưa HTML độc hại vào DOM.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Cấu hình khởi tạo i18n (`src/i18n/config.ts`).
- Các tệp từ điển JSON (`locales/vi/common.json`, `locales/en/common.json`).
- Bộ test xác minh tính toàn vẹn bản dịch.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-internationalization**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
