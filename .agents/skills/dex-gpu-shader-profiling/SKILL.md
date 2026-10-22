---
name: dex-gpu-shader-profiling
description: Profile and optimize vertex, fragment, and compute shaders, minimizing register pressure, arithmetic intensity bottlenecks, texture bandwidth stalls, and branch divergence. Use when optimizing GPU performance across desktop GPUs, mobile chips, and WebGL/WebGPU pipelines.
---

# dex-gpu-shader-profiling

## 1. Purpose & Scope
Lập hồ sơ hiệu năng (Profiling) và tối ưu hóa mã lệnh đổ bóng đồ họa GPU (Vertex, Fragment và Compute Shaders); giảm thiểu áp lực thanh ghi (Register Pressure), triệt tiêu các nút thắt cường độ số học (Arithmetic Bottlenecks), độ trễ băng thông nạp vân bề mặt (Texture Bandwidth Stalls) và hiện tượng phân kỳ rẽ nhánh luồng (Branch Divergence); phục vụ tối ưu hóa đồ họa trên chip di động và máy tính.

## 2. When to Use
- Khi GPU liên tục chạy ở mức 100% công suất làm tụt tốc độ khung hình của trò chơi.
- Khi mã shader phức tạp chứa quá nhiều nhánh rẽ điều kiện khiến các lõi GPU bị nhàn rỗi chờ đợi.
- Khi tối ưu hóa game 3D cho các dòng điện thoại di động chip đồ họa yếu (Mali, Adreno).

## 3. When NOT to Use
- Khi ứng dụng bị nghẽn ở luồng CPU chính (CPU-bound) chứ không phải do GPU.
- Khi tinh chỉnh các đoạn mã CSS animation đơn giản trên giao diện web.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Công cụ phân tích GPU chuyên dụng (RenderDoc, NVIDIA Nsight Graphics hoặc AMD Radeon Developer Tool Suite), mã nguồn Shader (GLSL, HLSL, WGSL hoặc SPIR-V).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Warp / Wavefront Branch Divergence:** Khi các luồng trong cùng một Warp (32 luồng) rẽ sang hai nhánh `if / else` khác nhau, GPU buộc phải thực thi cả hai nhánh tuần tự, làm giảm một nửa hiệu năng.
- **Register Pressure & Occupancy:** Shader sử dụng quá nhiều biến cục bộ làm tăng số thanh ghi cần dùng trên mỗi luồng, khiến GPU không thể chạy song song số lượng luồng tối đa.
- **Texture Fetch Latency Hiding:** Tận dụng các phép tính số học ALUs để che giấu độ trễ hàng trăm chu kỳ khi nạp dữ liệu ảnh từ bộ nhớ VRAM.

## 6. Step-by-Step Execution Workflow
1. Chụp lại khung hình đồ họa (Capture Frame) bằng công cụ RenderDoc.
2. Xác định các lệnh vẽ (Draw Calls) tốn nhiều thời gian GPU nhất trên đường ống.
3. Phân tích mã hợp ngữ shader (SPIR-V hoặc ISA) để kiểm tra số lượng thanh ghi sử dụng (VGPRs / SGPRs).
4. Loại bỏ các nhánh rẽ điều kiện động, chuyển sang dùng hàm toán học nội suy (`mix`, `step`, `clamp`).
5. Đo lường lại thời gian thực thi của shader trên GPU để xác nhận mức cải thiện.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```glsl
// Shader Optimization: Eliminating Dynamic Branch Divergence
// SLOW: Dynamic branch divergence inside fragment shader
// if (lightIntensity > 0.5) { color = vec3(1.0); } else { color = vec3(0.0); }

// FAST: Branchless math using step()
vec3 calculateOptimizedLighting(float lightIntensity, vec3 baseColor) {
    float factor = step(0.5, lightIntensity);
    return mix(vec3(0.0), baseColor, factor);
}
```

## 8. Anti-Patterns & Common Traps
- Sử dụng các vòng lặp `for` có số bước lặp động thay đổi theo từng pixel khiến các luồng trong GPU bị lệch nhịp nghiêm trọng.
- Thực hiện các phép tính toán ma trận giống hệt nhau trong Fragment Shader (chạy hàng triệu lần cho mỗi pixel) thay vì tính trước một lần ở Vertex Shader.
- Nạp các texture độ phân giải khổng lồ 4K mà không có Mipmaps làm nghẽn băng thông bộ nhớ VRAM.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Thời gian thực thi của shader chính giảm tối thiểu 30% sau khi tối ưu hóa.
- QG-02: Không còn nhánh rẽ phân kỳ động bên trong các vòng lặp tính toán nặng của Fragment Shader.
- QG-03: Mức chiếm dụng GPU (GPU Occupancy) đạt tối thiểu 75% trên kiến trúc mục tiêu.

## 10. Security & Safety Boundaries
- Kiểm tra giới hạn chỉ số mảng (Array Bounds Check) trong Compute Shader để ngăn ngừa việc đọc/ghi tràn bộ nhớ VRAM làm sập trình điều khiển card đồ họa.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Mã nguồn shader đã được tối ưu hóa `optimized_shading.frag`.
1. Báo cáo phân tích hiệu năng shader từ RenderDoc/Nsight.

## 13. Related & Complementary Skills
- [`dex-rendering-frame-pacing`](.agents/skills/dex-rendering-frame-pacing/SKILL.md)
- [`dex-gpu-resource-lifetime`](.agents/skills/dex-gpu-resource-lifetime/SKILL.md)
- [`dex-webgpu-rendering-fundamentals`](.agents/skills/dex-webgpu-rendering-fundamentals/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trò chơi 3D bị tụt khung hình xuống 24 FPS mỗi khi bước vào khu vực có hiệu ứng sương mù ánh sáng. Kỹ sư kích hoạt `dex-gpu-shader-profiling`, dùng RenderDoc phân tích shader sương mù, phát hiện một nhánh rẽ `if` phức tạp chạy trên từng pixel, chuyển đổi sang phép tính toán không nhánh `step()` và giảm số thanh ghi từ 48 xuống 24, đưa FPS trở lại mức 60 mượt mà.
