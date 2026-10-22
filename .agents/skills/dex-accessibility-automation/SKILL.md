---
name: dex-accessibility-automation
description: Automate accessibility audits (WCAG 2.1 AA/AAA) across web applications using axe-core, Pa11y, and Playwright, while designing manual testing protocols for screen readers (NVDA, VoiceOver). Use to guarantee digital inclusion and legal compliance.
---

# dex-accessibility-automation

## 1. Purpose & Scope
Tự động hóa kiểm toán khả năng tiếp cận kỹ thuật số (Accessibility Automation: WCAG 2.1 / 2.2 cấp độ AA/AAA) trên các ứng dụng web và mobile thông qua các công cụ tự động (axe-core, Pa11y, Playwright Accessibility Engine); kết hợp quy trình kiểm thử thủ công với trình đọc màn hình (Screen Readers: NVDA, VoiceOver) nhằm bảo đảm sản phẩm có thể sử dụng trọn vẹn bởi người khuyết tật và tuân thủ các quy định pháp lý quốc tế (ADA, Section 508, EAA).

## 2. When to Use
- Doanh nghiệp mở rộng thị trường sang Mỹ hoặc Châu Âu, nơi việc tuân thủ chuẩn WCAG 2.1 AA là bắt buộc theo luật pháp.
- Tích hợp kiểm tra tự động khả năng tiếp cận vào CI/CD pipeline để ngăn chặn hồi quy giao diện.
- Xây dựng hệ thống Design System dùng chung cho toàn bộ các sản phẩm của tổ chức.

## 3. When NOT to Use
- Không tuyên bố rằng 'Ứng dụng đã đạt chuẩn 100% WCAG' chỉ dựa vào công cụ quét tự động (các công cụ tự động như axe-core chỉ bắt được tối đa 30-40% các lỗi tiếp cận; 60% còn lại bắt buộc phải kiểm tra thủ công bằng bàn phím và screen reader).
- Không lạm dụng thuộc tính `aria-*` bừa bãi khi có thể dùng thẻ HTML ngữ nghĩa gốc (Native HTML elements).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- URL ứng dụng hoặc mã nguồn Frontend (React/Vue/Angular).
- Cấp độ tuân thủ mục tiêu (WCAG 2.1 Level AA).
- Công cụ tự động hóa CI (Playwright, Jest-axe, Lighthouse CI).
- **Điều kiện tiên quyết**:
- Ứng dụng có thể chạy và tương tác được trong môi trường kiểm thử headless browser.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- First Rule of ARIA: 'Nếu có thể sử dụng thẻ HTML ngữ nghĩa gốc (như `<button>`, `<nav>`, `<dialog>`), đừng bao giờ thay thế bằng `<div role="button">`'. Thẻ gốc đã tích hợp sẵn hỗ trợ bàn phím và screen reader.
- Bốn nguyên tắc WCAG (POUR):
  + Perceivable: Người dùng có thể cảm nhận được thông tin (độ tương phản màu sắc tối thiểu 4.5:1, có text thay thế `alt` cho ảnh).
  + Operable: Có thể điều khiển hoàn toàn bằng bàn phím (Tab, Enter, Space, Escape) mà không bị bẫy chuột (Keyboard Trap).
  + Understandable: Giao diện và thông báo lỗi rõ ràng, dễ hiểu.
  + Robust: Tương thích tốt với các công nghệ trợ giúp hiện tại và tương lai.
- **Quy tắc quyết định kỹ thuật**:
- Mọi ảnh mang tính thông tin bắt buộc phải có thuộc tính `alt` có nghĩa; ảnh thuần trang trí phải có `alt=""`.
- Bất kỳ lỗi vi phạm nghiêm trọng (Critical Violation) nào từ axe-core đều phải chặn đứng việc merge code trong CI.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Xóa bỏ viền hiển thị tiêu điểm bàn phím (`outline: none` trong CSS) mà không có kiểu thay thế, khiến người dùng khiếm thị dùng phím Tab hoàn toàn không biết mình đang đứng ở đâu trên màn hình.

## 6. Step-by-Step Execution Workflow
1. Cài đặt `@axe-core/playwright` vào bộ test E2E hiện có.
2. Viết các bài test tự động quét accessibility trên toàn bộ các trang chính và các trạng thái mở modal/menu.
3. Kiểm tra độ tương phản màu sắc của toàn bộ Design System tokens.
4. Thực hiện bài kiểm tra thủ công: rút chuột ra và chỉ dùng bàn phím duyệt toàn bộ quy trình mua hàng.
5. Bật trình đọc màn hình NVDA (Windows) hoặc VoiceOver (macOS) để kiểm tra các thông báo động (Aria-live regions).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Audits', () => {
  test('Trang thanh toán phải vượt qua kiểm tra WCAG 2.1 AA', async ({ page }) => {
    await page.goto('/checkout');
    
    // Quét toàn bộ trang với các quy tắc WCAG 2.1 AA
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();
      
    expect(accessibilityScanResults.violations).toEqual([]);
  });
});
```

### Lệnh xác minh & thực thi:
```bash
# Chạy kiểm thử tự động Accessibility trên toàn bộ trang qua Playwright
npx playwright test tests/a11y/
```

## 8. Anti-Patterns & Common Traps
- Sử dụng màu sắc làm phương tiện duy nhất để truyền tải thông tin (ví dụ: chỉ đổi chữ thành màu đỏ mà không có biểu tượng lỗi hoặc thông báo chữ đi kèm cho người mù màu).
- Tạo các nút bấm không thể focus được bằng phím Tab.

## 9. Quality Gates & Acceptance Criteria
- 0 lỗi vi phạm Critical hoặc Serious nào từ công cụ axe-core trong CI pipeline.
- 100% các luồng nghiệp vụ cốt lõi có thể hoàn thành trọn vẹn chỉ bằng bàn phím.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Đảm bảo các thuộc tính aria không làm lộ thông tin mật khẩu hoặc dữ liệu nhạy cảm của người dùng ra log trình duyệt.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Bộ kiểm thử tự động hóa Accessibility trong CI.
- Báo cáo kiểm toán Accessibility VPAT (Voluntary Product Accessibility Template) sơ bộ.

## 13. Related & Complementary Skills
dex-usability-study-design, dex-frontend-architecture, dex-design-handoff-verification

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty thương mại điện tử bị dọa kiện vì trang web vi phạm luật ADA tại Mỹ do người mù không thể mua hàng bằng screen reader. Nhóm kỹ sư đã tích hợp `@axe-core/playwright` vào CI, sửa 45 lỗi thiếu nhãn form và bổ sung `aria-live` cho giỏ hàng. Trang web đạt chuẩn WCAG 2.1 AA, vô hiệu hóa nguy cơ pháp lý và mở rộng phục vụ thêm hàng trăm ngàn khách hàng khuyết tật.
