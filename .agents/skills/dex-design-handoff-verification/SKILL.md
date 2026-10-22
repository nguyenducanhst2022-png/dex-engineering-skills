---
name: dex-design-handoff-verification
description: Verify and enforce pixel, typography, spacing, and state consistency between Figma design tokens and production frontend code using Storybook and visual regression tools. Use when bridging the gap between designers and developers.
---

# dex-design-handoff-verification

## 1. Purpose & Scope
Kiểm chứng và cưỡng chế tính nhất quán về kích thước (Pixel-perfect), kiểu chữ (Typography), khoảng cách (Spacing Tokens), màu sắc và các trạng thái tương tác (Hover, Active, Focus, Disabled, Loading) giữa bản thiết kế Figma với mã nguồn Frontend thực tế; sử dụng công cụ Visual Regression Testing (Storybook, Chromatic, Playwright Visual Comparison) để xóa bỏ hoàn toàn khoảng cách hiểu nhầm giữa Designer và Developer.

## 2. When to Use
- Giao diện web/mobile sau khi lập trình khác biệt đáng kể so với bản vẽ Figma khiến Designer phải review lại nhiều lần.
- Cập nhật một CSS component ở một nơi nhưng vô tình làm vỡ giao diện ở hàng chục màn hình khác (Visual Regression).
- Xây dựng và duy trì hệ thống Design System cấp doanh nghiệp.

## 3. When NOT to Use
- Không yêu cầu trùng khớp pixel 100% trên các thiết bị có kích thước màn hình dị biệt không nằm trong bản thiết kế (cần tư duy Responsive linh hoạt).
- Không chặn merge code chỉ vì lệch 1 pixel ở các thành phần phụ không ảnh hưởng tới trải nghiệm.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File thiết kế Figma (Figma Tokens / Variables, Component Specs).
- Mã nguồn Component Frontend (React, Vue, Tailwind CSS).
- Ảnh chụp mẫu cơ sở (Visual Baseline Screenshots).
- **Điều kiện tiên quyết**:
- Dự án có thiết lập thư viện Storybook hoặc có trang cô lập để chụp ảnh component.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Design Tokens as Code: Màu sắc, khoảng cách, font chữ được đồng bộ trực tiếp từ Figma Variables sang mã nguồn (CSS Variables / Tailwind Config) thông qua công cụ tự động hóa (như Tokens Studio hoặc Figma API), loại bỏ việc gõ giá trị màu cứng (`#1A73E8`) bằng tay.
- Visual Regression Testing: Chụp ảnh component ở từng trạng thái và so sánh từng pixel (Pixel-by-pixel diff) với ảnh chụp chuẩn trước đó. Nếu sai lệch vượt ngưỡng quy định (ví dụ > 0.2%), test sẽ fail và hiển thị ảnh highlight vùng bị lệch.
- Component States Coverage: Một component hoàn chỉnh không chỉ có giao diện bình thường (Default) mà bắt buộc phải có đầy đủ các trạng thái: Hover, Focus-visible, Loading/Skeleton, Error, Empty, Disabled.
- **Quy tắc quyết định kỹ thuật**:
- Mọi giá trị màu sắc và spacing trong CSS bắt buộc phải sử dụng biến Design Token; cấm gõ mã màu hex cứng trong component files.
- Nếu Visual Diff vượt quá ngưỡng 0.5%: bắt buộc phải có sự phê duyệt (Approve) từ Lead Designer trước khi merge PR.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Lập trình viên quên xử lý trạng thái chữ quá dài (Text Overflow) hoặc màn hình nhỏ, khiến giao diện bị vỡ layout khi dữ liệu thực tế dài hơn dữ liệu mẫu trong Figma.

## 6. Step-by-Step Execution Workflow
1. Xuất Design Tokens từ Figma sang file `tokens.json` và đồng bộ vào Tailwind config.
2. Viết Storybook stories bao quát toàn bộ các trạng thái khả dĩ của component.
3. Cấu hình Playwright Visual Comparison hoặc Chromatic trong CI pipeline.
4. Khi có PR thay đổi giao diện: CI tự động chụp ảnh và xuất báo cáo so sánh Diff trực quan.
5. Designer kiểm tra trực tiếp ảnh diff trên PR và bấm phê duyệt trực tuyến.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// Playwright Visual Regression Test cho Component Button
import { test, expect } from '@playwright/test';

test('Button Component phải khớp hoàn toàn với thiết kế Figma', async ({ page }) => {
  await page.goto('/iframe.html?id=components-button--primary');
  
  // Chụp ảnh component ở trạng thái mặc định và so sánh với baseline
  await expect(page.locator('button')).toHaveScreenshot('button-primary-default.png', {
    maxDiffPixelRatio: 0.01 // Cho phép sai lệch tối đa 1% do khử răng cưa font
  });
  
  // Kiểm tra trạng thái Hover
  await page.locator('button').hover();
  await expect(page.locator('button')).toHaveScreenshot('button-primary-hover.png');
});
```

### Lệnh xác minh & thực thi:
```bash
# Cập nhật baseline ảnh chụp visual regression sau khi được phê duyệt
npx playwright test --update-snapshots
```

## 8. Anti-Patterns & Common Traps
- Đánh giá giao diện chỉ bằng mắt thường trên máy cá nhân của developer.
- Bỏ qua trạng thái Loading Skeleton và Error State khi hiện thực component từ Figma.

## 9. Quality Gates & Acceptance Criteria
- 100% component trong Design System có Storybook stories và bài kiểm tra Visual Regression.
- Sai lệch trực quan giữa code và thiết kế không vượt quá ngưỡng sai số quy định.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Đảm bảo các ảnh chụp màn hình trong test không chứa thông tin dữ liệu khách hàng thực tế.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Bộ Storybook Stories đầy đủ các trạng thái.
- Báo cáo Visual Regression Diff tự động trong Pull Request.

## 13. Related & Complementary Skills
dex-frontend-architecture, dex-accessibility-automation, dex-usability-study-design

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ thường xuyên xảy ra tranh cãi giữa Designer và Developer vì nút bấm trên web bị lệch lề 4px và màu hover sai sắc độ. Nhờ triển khai Design Tokens tự động đồng bộ từ Figma sang Tailwind và áp dụng Playwright Visual Testing, 100% sai lệch giao diện đều được phát hiện tự động ngay tại CI, rút ngắn thời gian bàn giao thiết kế từ 5 ngày xuống còn 2 giờ.
