---
name: dex-search-interface-experience
description: Architect accessible, instant search interfaces with debounced typeahead suggestions, faceted multi-attribute filters, keyboard navigation (combobox pattern), and empty search recovery. Use when building e-commerce catalogs, knowledge bases, or document search portals.
---

# dex-search-interface-experience

## 1. Purpose & Scope
Thiết kế kiến trúc giao diện tìm kiếm tức thì (Instant Search) có độ tiếp cận cao theo chuẩn WAI-ARIA Combobox Pattern; tích hợp cơ chế chống rung phím (Debounced Typeahead), bộ lọc đa thuộc tính (Faceted Filtering), điều hướng hoàn toàn bằng bàn phím và khả năng phục hồi gợi ý khi không tìm thấy kết quả.

## 2. When to Use
- Khi xây dựng thanh tìm kiếm trung tâm cho ứng dụng tài liệu kỹ thuật hoặc kho sản phẩm thương mại điện tử.
- Khi người dùng gặp khó khăn trong việc tìm kiếm thông tin do giao diện không có gợi ý từ khóa.
- Khi cần tối ưu hóa trải nghiệm điều hướng bằng bàn phím (`ArrowUp`, `ArrowDown`, `Enter`, `Escape`).

## 3. When NOT to Use
- Khi chỉ lọc danh sách dữ liệu nhỏ dưới 10 phần tử đã có sẵn trên RAM.
- Khi xây dựng các câu lệnh truy vấn nội bộ của database dưới backend.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Endpoint API tìm kiếm hỗ trợ phân trang và từ khóa, danh mục các trường dữ liệu cần lọc (facets).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Debounced Input:** Trì hoãn việc gửi request API tìm kiếm từ 250ms đến 300ms sau khi người dùng ngừng gõ phím.
- **WAI-ARIA Combobox Pattern:** Quản lý thuộc tính `aria-expanded`, `aria-activedescendant` và `aria-controls` đúng tiêu chuẩn trợ năng.
- **Zero-Result Recovery:** Khi không có kết quả, cung cấp từ khóa gợi ý gần đúng (Did you mean?), các tìm kiếm phổ biến hoặc gợi ý xóa bớt bộ lọc.

## 6. Step-by-Step Execution Workflow
1. Xây dựng ô nhập liệu tìm kiếm với icon xóa nhanh và trạng thái loading trực quan.
2. Bọc logic nhập liệu bằng hàm debounce để giảm tải 80% số lượng request lên máy chủ.
3. Hiện thực hóa danh sách dropdown gợi ý với các phần tử có thể highlight từ khóa tìm kiếm.
4. Lắng nghe sự kiện bàn phím để di chuyển vệt chọn lên xuống và phím Escape để đóng nhanh menu.
5. Xây dựng trạng thái Empty State thông minh khi kết quả trả về bằng 0.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Debounced Search Hook Pattern
import { useState, useEffect } from 'react';

export function useDebouncedSearch(query: string, delayMs = 300) {
  const [debouncedValue, setDebouncedValue] = useState(query);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(query.trim());
    }, delayMs);

    return () => clearTimeout(handler);
  }, [query, delayMs]);

  return debouncedValue;
}
```

## 8. Anti-Patterns & Common Traps
- Gửi request tìm kiếm sau từng ký tự được gõ mà không có debounce làm nghẽn server và xung đột thứ tự kết quả trả về.
- Bẫy tiêu điểm (Focus Trap) khiến người dùng bàn phím không thể nhấn Tab để thoát ra khỏi thanh tìm kiếm.
- Chỉ hiển thị dòng chữ cụt lủn 'Không tìm thấy kết quả' mà không đưa ra bất kỳ hướng dẫn hay gợi ý thay thế nào.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tuân thủ 100% tiêu chuẩn WAI-ARIA 1.2 cho Combobox Pattern.
- QG-02: Độ trễ phản hồi gợi ý giao diện dưới 150ms sau khi nhận được dữ liệu từ API.
- QG-03: Người dùng có thể hoàn thành toàn bộ chu trình tìm kiếm và chọn kết quả mà không cần chạm vào chuột máy tính.

## 10. Security & Safety Boundaries
- Khử nhiễm (Sanitize) toàn bộ chuỗi tìm kiếm trước khi render vào DOM để triệt tiêu lỗ hổng Cross-Site Scripting (XSS).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Component tìm kiếm thông minh `InstantSearchCombobox.tsx`.
1. Bộ test tự động kiểm tra điều hướng bằng bàn phím với Playwright.

## 13. Related & Complementary Skills
- [`dex-search-engineering`](.agents/skills/dex-search-engineering/SKILL.md)
- [`dex-ux-accessibility`](.agents/skills/dex-ux-accessibility/SKILL.md)
- [`dex-ui-component-contracts`](.agents/skills/dex-ui-component-contracts/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Xây dựng cổng tài liệu nội bộ với 5,000 bài viết. Kỹ sư kích hoạt `dex-search-interface-experience` để thiết kế hộp tìm kiếm dạng Spotlight (tương tự macOS Cmd+K), hỗ trợ lọc theo danh mục, điều hướng phím mũi tên mượt mà và gợi ý từ khóa liên quan khi gõ sai chính tả.
