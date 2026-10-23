---
name: dex-gesture-interaction-accessibility
description: Design and validate touch, swipe, pinch, and multi-finger gesture interactions with accessible single-pointer and keyboard alternatives compliant with WCAG 2.5 Input Modalities. Use when engineering modern mobile-first web and native touch interfaces.
---

# dex-gesture-interaction-accessibility

## 1. Purpose & Scope
Thiết kế, chuẩn hóa và kiểm chứng các tương tác cử chỉ chạm vuốt (gestures) trên thiết bị di động và màn hình cảm ứng; bảo đảm luôn cung cấp giải pháp thay thế bằng con trỏ đơn (single-pointer) và bàn phím theo tiêu chí WCAG 2.5 Input Modalities.

## 2. When to Use
- Khi xây dựng các tính năng tương tác cử chỉ như vuốt để xóa (swipe to delete), kéo thả (drag and drop), hoặc chụm mở để thu phóng (pinch to zoom).
- Khi ứng dụng di động cần đáp ứng tiêu chuẩn tiếp cận tiếp cận cho người dùng có khiếm khuyết vận động.
- Khi kiểm toán tuân thủ WCAG 2.2 cho các ứng dụng Hybrid hoặc Progressive Web Apps.

## 3. When NOT to Use
- Khi ứng dụng chỉ hoạt động trên môi trường dòng lệnh CLI hoặc máy chủ không có giao diện đồ họa cảm ứng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Đặc tả cử chỉ tương tác (gesture spec), thiết bị thử nghiệm cảm ứng hoặc trình giả lập touch events.
- **Quyền hạn truy cập:** Quyền sửa đổi logic xử lý sự kiện tương tác người dùng.

## 5. Core Concepts & Taxonomy
- **WCAG 2.5.1 Pointer Gestures:** Bất kỳ thao tác nào yêu cầu cử chỉ đa điểm (multipoint) hoặc cử chỉ dựa trên đường dẫn (path-based) đều phải có phương thức tương tác đơn giản chỉ bằng một lần nhấp (single-pointer alternative).
- **WCAG 2.5.2 Pointer Cancellation:** Cho phép người dùng hủy thao tác bằng cách di chuyển ngón tay ra khỏi vùng kích hoạt trước khi nhấc lên (Up-Event Triggering).
- **Minimum Target Size:** Kích thước vùng bấm tối thiểu đạt 24x24 CSS pixels (WCAG 2.2 Level AA) hoặc khuyến nghị 44x44 / 48x48 pixels.

## 6. Step-by-Step Execution Workflow
1. Khảo sát danh mục tất cả các cử chỉ tương tác trong ứng dụng: Swipe, Drag, Pinch, Double-tap, Long-press.
2. Thiết kế nút bấm hoặc menu tùy chọn tương đương cho mỗi cử chỉ (ví dụ: cung cấp nút 'Xóa' trong menu tùy chọn bên cạnh cử chỉ vuốt ngang).
3. Gắn bộ lắng nghe sự kiện `pointerup` thay vì `pointerdown` để cho phép hủy bỏ hành động vô ý.
4. Cung cấp cơ chế xác nhận trước các hành động phá hủy dữ liệu được kích hoạt từ cử chỉ cảm ứng.
5. Đảm bảo toàn bộ các mục tiêu tương tác có kích thước vùng chạm tối thiểu đạt chuẩn.
6. Kiểm thử tương tác song song với bàn phím (phím Enter, Space, mũi tên) và phần mềm đọc màn hình (TalkBack, VoiceOver).

## 7. Concrete Examples
### Xử lý cử chỉ vuốt kèm cơ chế Single-Pointer và Phím tắt dự phòng:
```typescript
interface DismissibleItemProps {
  id: string;
  onDismiss: (id: string) => void;
  title: string;
}

export const DismissibleItem: React.FC<DismissibleItemProps> = ({ id, onDismiss, title }) => {
  return (
    <div className="item-row" role="listitem">
      <span>{title}</span>
      {/* Nút hành động đơn lẻ dự phòng cho người dùng không thể thực hiện thao tác vuốt */}
      <button 
        type="button" 
        className="btn-action-fallback"
        aria-label={`Xóa mục ${title}`}
        onClick={() => onDismiss(id)}
      >
        Xóa
      </button>
    </div>
  );
};
```

## 8. Anti-Patterns & Common Traps
- **Gesture-Only Actions:** Cung cấp tính năng quan trọng (như xóa thư hoặc lưu trữ) độc quyền qua thao tác vuốt mà không có nút bấm tương đương.
- **Trigger on PointerDown:** Kích hoạt giao dịch hoặc xóa dữ liệu ngay khi vừa chạm màn hình, không cho phép người dùng kéo ra ngoài để hủy.
- **Tiny Touch Target:** Đặt các nút icon có kích thước 16x16px nằm sát nhau trên màn hình cảm ứng khiến người dùng liên tục bấm nhầm.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các cử chỉ vuốt hoặc kéo thả đều có nút bấm đơn giản thay thế trên giao diện.
- **QG-03**: Vùng tương tác cảm ứng đạt kích thước tối thiểu 24x24 CSS pixels (đạt chuẩn WCAG 2.2 AA).
- **QG-07**: Không có hành động không thể hoàn tác nào được kích hoạt từ sự kiện pointerdown.

## 10. Security & Safety Boundaries
- Ngăn chặn hiện tượng 'Tapjacking' hoặc 'Pointer Spoofing' bằng cách kiểm tra thuộc tính `isTrusted` trên PointerEvents.

## 11. Platform Adapters
- **Libraries**: Hammer.js, interact.js, Framer Motion, React-Use-Gesture.
- **Testing**: Playwright Touch Emulation, axe-core.

## 12. Deliverables & Output Artifacts
- Component cử chỉ chạm vuốt kèm cơ chế fallback bàn phím.
- Bộ kiểm thử tự động xác minh kích thước vùng chạm.
- Tài liệu hướng dẫn thao tác tương tác đa phương thức.

## 13. Related & Complementary Skills
dex-accessibility-automation, dex-component-state-matrix, dex-mobile-safe-area-layout

## 14. Realistic Usage Example
```powershell
# Chạy kiểm thử tự động kiểm tra kích thước vùng bấm (Target Size)
npx playwright test tests/a11y/target-size.spec.ts

# Giả lập sự kiện chạm vuốt trên môi trường mobile
npx cypress run --spec "cypress/e2e/gestures.cy.ts" --config viewportWidth=375,viewportHeight=667
```
