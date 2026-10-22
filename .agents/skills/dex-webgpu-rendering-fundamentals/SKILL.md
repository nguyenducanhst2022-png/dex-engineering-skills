---
name: dex-webgpu-rendering-fundamentals
description: Design safe, high-performance WebGPU rendering pipelines, WGSL shader compilations, memory buffer lifecycle management, and device-loss recovery with WebGL2 fallback. Use when implementing compute shaders in the browser, 3D product visualizers, or high-throughput visualization.
---

# dex-webgpu-rendering-fundamentals

## 1. Purpose & Scope
Thiết kế và triển khai đường ống kết xuất đồ họa và tính toán song song thế hệ mới trên WebGPU; lập trình shader ngôn ngữ WGSL, quản trị vòng đời bộ nhớ đệm (GPU Buffers), cơ chế tự phục hồi khi mất thiết bị (Device Loss Recovery) và phương án dự phòng WebGL2 tương thích ngược.

## 2. When to Use
- Khi xây dựng các ứng dụng đồ họa 3D phức tạp, mô phỏng vật lý hạt hoặc tính toán AI/Machine Learning trực tiếp trên trình duyệt.
- Khi ứng dụng gặp giới hạn nghẽn cổ chai của WebGL do chi phí gọi lệnh vẽ (Draw Call Overhead) quá lớn.
- Khi cần tận dụng Compute Shaders để xử lý song song khối lượng dữ liệu khổng lồ trên GPU.

## 3. When NOT to Use
- Khi ứng dụng chỉ hiển thị các bảng dữ liệu HTML hoặc biểu đồ kinh doanh thông thường.
- Khi trình duyệt của đối tượng khách hàng mục tiêu là các trình duyệt đời cũ chưa bật WebGPU.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Trình duyệt hỗ trợ WebGPU (`navigator.gpu`), card đồ họa hỗ trợ DirectX 12 / Metal / Vulkan, kiến thức về ngôn ngữ shader WGSL.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Pipeline State Object (PSO):** Đóng gói toàn bộ cấu hình shader, định dạng đỉnh và trạng thái blend thành đối tượng bất biến để tối ưu tốc độ thực thi trên GPU.
- **Command Buffer Recording:** Ghi lại danh sách các lệnh vẽ độc lập ngoài luồng trước khi gửi hàng loạt xuống hàng đợi `gpuQueue`.
- **Device Loss Handling:** Bắt sự kiện thiết bị GPU bị ngắt (do sleep, chuyển card màn hình) để khởi tạo lại tài nguyên mà không làm sập ứng dụng.

## 6. Step-by-Step Execution Workflow
1. Kiểm tra hỗ trợ `navigator.gpu` và yêu cầu `GPUAdapter` cùng `GPUDevice`.
2. Viết và biên dịch mã nguồn Shader ngôn ngữ WGSL cho Vertex, Fragment hoặc Compute stage.
3. Khởi tạo các bộ đệm `GPUBuffer` chứa tọa độ đỉnh và ma trận đồng nhất (Uniforms).
4. Tạo Render Pipeline và cấu hình Bind Group liên kết bộ nhớ đệm với shader.
5. Thiết lập cơ chế bắt lỗi `device.lost` để tái tạo tài nguyên và kích hoạt WebGL2 fallback nếu không thể khôi phục.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Basic WebGPU Initialization & Pipeline
export async function initWebGPU(canvas: HTMLCanvasElement) {
  if (!navigator.gpu) throw new Error('WebGPU is not supported');
  
  const adapter = await navigator.gpu.requestAdapter();
  if (!adapter) throw new Error('No appropriate GPUAdapter found');
  
  const device = await adapter.requestDevice();
  const context = canvas.getContext('webgpu') as GPUCanvasContext;
  const presentationFormat = navigator.gpu.getPreferredCanvasFormat();
  
  context.configure({
    device,
    format: presentationFormat,
    alphaMode: 'premultiplied',
  });
  
  // Listen for device loss
  device.lost.then(info => {
    console.warn(`GPU Device lost: ${info.reason}`, info.message);
  });
  
  return { device, context, presentationFormat };
}
```

## 8. Anti-Patterns & Common Traps
- Tạo mới `GPURenderPipeline` hoặc nạp lại shader trong mỗi khung hình khiến GPU bị giật nghiêm trọng.
- Không giải phóng bộ nhớ `buffer.destroy()` khi hủy bỏ đối tượng đồ họa dẫn đến tràn bộ nhớ VRAM card màn hình.
- Giả định mọi máy khách đều có WebGPU mà không chuẩn bị giải pháp dự phòng WebGL2.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Khởi tạo WebGPU pipeline thành công không có lỗi biên dịch WGSL shader trong console.
- QG-02: Ứng dụng tự động phục hồi hoặc thông báo nhẹ nhàng khi GPU bị mất thiết bị (Device Lost event).
- QG-03: Có sẵn module fallback sang WebGL2 khi `navigator.gpu` trả về null.

## 10. Security & Safety Boundaries
- Ngăn chặn việc khai thác lỗi tràn bộ đệm GPU hoặc tấn công kênh kề (Side-channel timing attacks) thông qua việc kiểm tra kỹ giới hạn kích thước buffer truyền vào compute shader.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Mẫu khởi tạo WebGPU chuẩn `WebGPURuntime.ts`.
1. Bộ shader WGSL mẫu cho kết xuất 3D và tính toán song song.

## 13. Related & Complementary Skills
- [`dex-web-canvas-rendering`](.agents/skills/dex-web-canvas-rendering/SKILL.md)
- [`dex-gpu-shader-profiling`](.agents/skills/dex-gpu-shader-profiling/SKILL.md)
- [`dex-gpu-resource-lifetime`](.agents/skills/dex-gpu-resource-lifetime/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát triển công cụ xem trước mô hình 3D cho sản phẩm nội thất kiến trúc. Áp dụng `dex-webgpu-rendering-fundamentals` để tận dụng Compute Shaders tính toán phản chiếu ánh sáng chân thực với tốc độ 60fps trên trình duyệt Chrome và Safari hiện đại.
