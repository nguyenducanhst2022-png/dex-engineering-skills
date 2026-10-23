---
name: dex-component-state-matrix
description: Systematically specify, render, and visually verify all interactive UI component permutations across rest, hover, active, focus-visible, disabled, loading, error, and empty states. Use when building robust design systems and preventing interactive UX regressions.
---

# dex-component-state-matrix

## 1. Purpose & Scope
Hệ thống hóa, mô phỏng và kiểm chứng trực quan toàn bộ ma trận trạng thái của UI component bao gồm idle, hover, active, focus-visible, disabled, loading, invalid, và empty; đảm bảo trải nghiệm tương tác liền mạch và khả năng tiếp cận chuẩn WCAG.

## 2. When to Use
- Khi phát triển component mới cho thư viện UI hoặc Design System trung tâm.
- Khi audit khả năng tiếp cận (a11y) của các trường nhập liệu và nút bấm tương tác.
- Khi phát hiện lỗi giao diện chỉ xuất hiện ở các trạng thái biên như loading kết hợp disabled.

## 3. When NOT to Use
- Khi dựng mockup tĩnh phục vụ mục đích phỏng vấn ý tưởng ban đầu trong thời gian ngắn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Component specification, Storybook hoặc môi trường test trực quan tương đương.
- **Quyền hạn truy cập:** Quyền ghi vào thư mục stories và test của component.

## 5. Core Concepts & Taxonomy
- **Component Permutation Matrix:** Tích Descartes của tất cả các biến thể (variants: primary, secondary) x kích thước (sm, md, lg) x trạng thái tương tác.
- **Focus-Visible Discipline:** Chỉ hiển thị viền focus nổi bật khi người dùng điều hướng bằng bàn phím (Tab), không gây khó chịu khi click chuột.
- **State Collision Handling:** Định nghĩa thứ tự ưu tiên khi nhiều trạng thái đồng thời xuất hiện (ví dụ: disabled có ưu tiên cao hơn hover và active).

## 6. Step-by-Step Execution Workflow
1. Liệt kê toàn bộ các trạng thái khả dĩ của component: Idle, Hover, Active, Focus, Focus-Visible, Disabled, Loading, Error, Empty.
2. Thiết lập bảng ma trận ưu tiên trạng thái (State Precedence Table) để xử lý xung đột.
3. Viết Storybook stories hiển thị song song toàn bộ ma trận trạng thái trên cùng một view.
4. Tích hợp kiểm thử tự động giả lập tương tác bàn phím và con trỏ chuột bằng Playwright hoặc Cypress.
5. Xác nhận tỷ lệ tương phản màu sắc (Color Contrast Ratio) ở mọi trạng thái đều đạt chuẩn WCAG 2.2 AA (>= 4.5:1 hoặc >= 3:1 cho focus ring).
6. Đóng gói component kèm tài liệu trực quan minh họa từng trạng thái.

## 7. Concrete Examples
### Định nghĩa ma trận trạng thái trong Storybook (React / TypeScript):
```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Design System/Button/StateMatrix',
  component: Button,
};
export default meta;

export const AllStatesMatrix: StoryObj = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
      <div>
        <h4>Normal / Idle</h4>
        <Button variant="primary">Submit</Button>
      </div>
      <div>
        <h4>Hover State</h4>
        <Button variant="primary" className="pseudo-hover">Submit</Button>
      </div>
      <div>
        <h4>Focus-Visible</h4>
        <Button variant="primary" className="pseudo-focus-visible">Submit</Button>
      </div>
      <div>
        <h4>Loading State</h4>
        <Button variant="primary" isLoading>Submit</Button>
      </div>
      <div>
        <h4>Disabled State</h4>
        <Button variant="primary" disabled>Submit</Button>
      </div>
    </div>
  ),
};
```

## 8. Anti-Patterns & Common Traps
- **Missing Disabled Interaction Block:** Chỉ đổi màu nút bấm sang xám nhưng không chặn sự kiện click hoặc submit trong JavaScript.
- **Outline None Without Alternative:** Ẩn viền focus mặc định (`outline: none`) mà không tạo kiểu focus ring thay thế cho người dùng bàn phím.
- **Flickering Loading Jitter:** Đổi kích thước component đột ngột khi hiển thị spinner làm dịch chuyển bố cục xung quanh (Layout Shift).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tất cả các component tương tác đều có Storybook story bao phủ 100% các trạng thái trong ma trận.
- **QG-03**: Trạng thái focus-visible luôn có viền tương phản tối thiểu 3:1 so với nền liền kề.
- **QG-07**: Component disabled không kích hoạt bất kỳ callback sự kiện nào khi click hoặc nhấn phím.

## 10. Security & Safety Boundaries
- Ngăn ngừa tấn công Clickjacking bằng cách kiểm tra các component có thể che khuất nút tương tác bằng CSS opacity.

## 11. Platform Adapters
- **Catalog & UI Testing**: Storybook, Chromatic, Playwright Component Testing, Jest-DOM.

## 12. Deliverables & Output Artifacts
- File Storybook matrix story cho component.
- Bộ quy tắc CSS trạng thái tương tác hoàn chỉnh.
- Test suite xác thực chặn sự kiện khi disabled.

## 13. Related & Complementary Skills
dex-accessibility-automation, dex-design-token-migration, dex-gesture-interaction-accessibility

## 14. Realistic Usage Example
```powershell
# Chạy Storybook để kiểm tra ma trận trạng thái
npm run storybook

# Chạy visual regression test xác thực trạng thái tương tác
npx playwright test tests/visual/button-matrix.spec.ts
```
