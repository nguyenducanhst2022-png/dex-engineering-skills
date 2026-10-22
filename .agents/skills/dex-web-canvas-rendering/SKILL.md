---
name: dex-web-canvas-rendering
description: Engineer interactive, high-DPI HTML5 2D Canvas interfaces with dirty-rectangle redraw optimizations, spatial indexing (quadtrees), pan-zoom transformations, and pointer hit detection. Use when building interactive whiteboards, flowchart editors, or custom data visualizations.
---

# dex-web-canvas-rendering

## 1. Purpose & Scope
Thiết kế và xây dựng giao diện đồ họa tương tác trên nền tảng HTML5 2D Canvas; hỗ trợ tối ưu độ phân giải cao (Retina / High-DPI screens), cơ chế vẽ lại vùng thay đổi (Dirty-Rectangle Redraw), cấu trúc dữ liệu không gian Quadtree để phát hiện va chạm con trỏ và ma trận biến đổi tọa độ pan-zoom mượt mà.

## 2. When to Use
- Khi xây dựng bảng vẽ tương tác (Online Whiteboard), công cụ vẽ sơ đồ hoặc game 2D trên web.
- Khi số lượng phần tử đồ họa vượt quá khả năng xử lý của thẻ SVG hoặc DOM thông thường (>3,000 objects).
- Khi cần điều khiển từng pixel màu sắc và hiệu ứng ánh sáng đồ họa tùy biến.

## 3. When NOT to Use
- Khi giao diện chỉ bao gồm các form nhập liệu, danh sách và văn bản thông thường.
- Khi cần hỗ trợ đầy đủ các tính năng trợ năng màn hình (Screen Reader) một cách tự nhiên mà không muốn giả lập ARIA.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Ngữ cảnh đồ họa `HTMLCanvasElement.getContext('2d')`, toán học vector và ma trận biến đổi không gian 2D.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Device Pixel Ratio (DPR) Scaling:** Nhân đôi kích thước bộ đệm canvas theo `window.devicePixelRatio` và co lại bằng CSS để triệt tiêu hiện tượng mờ chữ trên màn hình Retina.
- **Quadtree Spatial Partitioning:** Phân hoạch không gian thành cây 4 góc để tra cứu phần tử được bấm trúng (Hit Testing) với độ phức tạp $O(\log N)$.
- **Dirty Rectangle Redraw:** Chỉ xóa và vẽ lại khu vực có phần tử di chuyển thay vì vẽ lại toàn bộ khung tranh (`clearRect` toàn màn hình).

## 6. Step-by-Step Execution Workflow
1. Khởi tạo canvas và hiệu chuẩn kích thước theo tỷ lệ DPR của màn hình thiết bị.
2. Thiết lập vòng lặp kết xuất đồ họa (Render Loop) sử dụng `requestAnimationFrame`.
3. Xây dựng ma trận biến đổi tọa độ (View Matrix) hỗ trợ thao tác kéo (Pan) và thu phóng (Zoom).
4. Đưa các thực thể hình học vào cây không gian Quadtree.
5. Lắng nghe sự kiện chuột/cảm ứng, chuyển đổi tọa độ màn hình sang tọa độ thế giới canvas để kiểm tra va chạm.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// High-DPI Canvas Scaling Pattern
export function setupHighDpiCanvas(canvas: HTMLCanvasElement, width: number, height: number) {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;

  const ctx = canvas.getContext('2d');
  if (ctx) {
    ctx.scale(dpr, dpr);
  }
  return ctx;
}
```

## 8. Anti-Patterns & Common Traps
- Không hiệu chuẩn theo `devicePixelRatio` khiến nét vẽ trên màn hình điện thoại và MacBook bị nhòe mờ như ảnh nén chất lượng thấp.
- Dùng vòng lặp kiểm tra va chạm tuần tự $O(N)$ trên 10,000 vật thể khi di chuyển chuột khiến FPS sụt giảm thê thảm.
- Tạo mới đối tượng hoặc mảng trong mỗi khung hình render loop gây kích hoạt dọn rác (Garbage Collection) liên tục làm giật hình.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Hình ảnh và văn bản trên Canvas hiển thị sắc nét trên cả màn hình chuẩn 1x và Retina 2x/3x.
- QG-02: Duy trì tốc độ khung hình 60fps khi tương tác kéo thả với tối thiểu 5,000 vật thể độc lập.
- QG-03: Độ chính xác phát hiện bấm trúng điểm ảnh (Hit-test accuracy) đạt tuyệt đối.

## 10. Security & Safety Boundaries
- Xử lý cẩn thận phương thức `toDataURL()` hoặc `getImageData()` khi vẽ ảnh từ domain khác để tránh lỗi ô nhiễm Canvas (Tainted Canvas CORS error).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Lớp quản lý tương tác Canvas `CanvasEngine2D.ts`.
1. Module cấu trúc dữ liệu không gian `QuadtreeSpatialIndex.ts`.

## 13. Related & Complementary Skills
- [`dex-webgpu-rendering-fundamentals`](.agents/skills/dex-webgpu-rendering-fundamentals/SKILL.md)
- [`dex-simulation-determinism`](.agents/skills/dex-simulation-determinism/SKILL.md)
- [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát triển công cụ chỉnh sửa sơ đồ mạng lưới hạ tầng đám mây. Kỹ sư kích hoạt `dex-web-canvas-rendering` để vẽ hơn 8,000 node máy chủ, sử dụng Quadtree để hỗ trợ chọn và nối dây giữa các node với tốc độ 60fps mượt mà, không gặp hiện tượng trễ chuột.
