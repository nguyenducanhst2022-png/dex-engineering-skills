---
name: dex-browser-automation-testing
description: Design deterministic, flake-free browser automation suites using Playwright/Puppeteer with locator best practices, explicit network idle waits, and isolated browser contexts. Use when testing complex user checkout journeys, cross-browser interactions, or end-to-end web flows.
---

# dex-browser-automation-testing

## 1. Purpose & Scope
Thiết kế và xây dựng bộ kiểm thử tự động hóa trình duyệt (Browser Automation Testing) có tính xác định cao, triệt tiêu lỗi chập chờn (Flaky Tests); ứng dụng công nghệ Playwright/Puppeteer với chiến lược định vị phần tử theo ngữ nghĩa (Semantic Locators), quản lý ngữ cảnh trình duyệt cô lập (Isolated Browser Contexts) và cơ chế chờ mạng thông minh.

## 2. When to Use
- Khi xây dựng bộ kiểm thử đầu-cuối (End-to-End E2E Testing) cho các luồng nghiệp vụ quan trọng.
- Khi bộ test hiện tại thường xuyên bị lỗi ngẫu nhiên (flaky) do phụ thuộc vào thời gian chờ cứng (`sleep`).
- Khi cần kiểm tra tính tương thích của ứng dụng trên cả 3 engine trình duyệt: Chromium, WebKit và Firefox.

## 3. When NOT to Use
- Khi kiểm thử các hàm tính toán logic nội bộ không có tương tác giao diện (nên dùng Unit Test).
- Khi chỉ kiểm tra tính hợp lệ của cú pháp mã nguồn hoặc kiểm tra kiểu TypeScript.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Môi trường Node.js, framework Playwright hoặc Puppeteer, máy chủ kiểm thử ứng dụng có sẵn.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **User-Facing Locators:** Định vị phần tử theo cách người dùng tương tác (`getByRole`, `getByText`, `getByLabel`) thay vì dùng XPath hoặc class CSS dễ vỡ.
- **Auto-Waiting & Web-First Assertions:** Tận dụng cơ chế tự động chờ phần tử hiển thị và có thể thao tác được của Playwright (`await expect(locator).toBeVisible()`).
- **Browser Context Isolation:** Mỗi ca kiểm thử chạy trong một Browser Context sạch hoàn toàn cookie và local storage để ngăn ngừa ảnh hưởng chéo.

## 6. Step-by-Step Execution Workflow
1. Cấu hình Playwright test runner với các thiết bị mục tiêu (Desktop Chrome, Mobile Safari).
2. Viết kịch bản kiểm thử áp dụng mô hình Page Object Model (POM) để tái sử dụng mã nguồn.
3. Sử dụng các bộ định vị ngữ nghĩa hướng người dùng như `page.getByRole('button', { name: 'Submit' })`.
4. Chờ đợi các phản hồi API hoặc trạng thái mạng ổn định bằng `page.waitForResponse` thay vì `page.waitForTimeout`.
5. Thu thập ảnh chụp màn hình, video và trace file khi có ca kiểm thử thất bại để phục vụ điều tra nguyên nhân.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { test, expect } from '@playwright/test';

test('User completes multi-step checkout journey', async ({ page }) => {
  await page.goto('/catalog');

  // Semantic user-facing locator
  await page.getByRole('button', { name: 'Add to Cart' }).first().click();
  await page.getByRole('link', { name: 'View Cart' }).click();

  // Web-first assertion with auto-waiting
  await expect(page.getByTestId('cart-total')).toHaveText('$99.00');

  // Fill shipping form
  await page.getByLabel('Full Name').fill('Alex Rivera');
  await page.getByRole('button', { name: 'Confirm Purchase' }).click();

  // Await success screen
  await expect(page.getByRole('heading', { name: 'Order Confirmed' })).toBeVisible();
});
```

## 8. Anti-Patterns & Common Traps
- Sử dụng lệnh dừng chờ cứng như `page.waitForTimeout(5000)` khiến test chạy chậm và vẫn có thể fail nếu mạng bị lag.
- Dùng bộ định vị dựa vào cấu trúc DOM sâu như `div > div:nth-child(3) > span` (sẽ hỏng ngay khi sửa giao diện).
- Chia sẻ chung trạng thái đăng nhập hoặc dữ liệu giữa các ca kiểm thử khác nhau.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tỷ lệ thất bại do chập chờn (Flakiness Rate) dưới 0.1% qua 100 lần chạy kiểm thử liên tiếp.
- QG-02: 100% các bước tương tác sử dụng Semantic Locators hoặc `data-testid` chuẩn.
- QG-03: Mỗi ca kiểm thử thất bại đều tự động xuất file Playwright Trace để xem lại từng thao tác.

## 10. Security & Safety Boundaries
- Không đưa mật khẩu hoặc tài khoản quản trị thật vào kịch bản kiểm thử; sử dụng tài khoản thử nghiệm chuyên dụng trên môi trường staging.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bộ kịch bản kiểm thử tự động Playwright hoàn chỉnh `e2e-suite.spec.ts`.
1. Báo cáo kết quả kiểm thử kèm video và trace artifacts.

## 13. Related & Complementary Skills
- [`dex-end-to-end-engineering`](.agents/skills/dex-end-to-end-engineering/SKILL.md)
- [`dex-flaky-test-remediation`](.agents/skills/dex-flaky-test-remediation/SKILL.md)
- [`dex-headless-ui-verification`](.agents/skills/dex-headless-ui-verification/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Đội ngũ phát triển gặp khủng hoảng vì bộ test E2E 200 kịch bản chạy mất 45 phút và 20% ca test bị fail ngẫu nhiên mỗi lần chạy CI. Áp dụng `dex-browser-automation-testing` để refactor sang Playwright với semantic locators và isolated contexts, giảm thời gian chạy xuống 8 phút và tỷ lệ flaky về đúng 0%.
