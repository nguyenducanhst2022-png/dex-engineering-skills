---
name: dex-gpu-resource-lifetime
description: Architect robust GPU memory allocators and resource lifetime managers across Vulkan, DirectX 12, and Metal, eliminating VRAM leaks, staging buffer stalls, and handling graphics device loss. Use when building AAA rendering engines, native CAD viewports, or compute pipelines.
---

# dex-gpu-resource-lifetime

## 1. Purpose & Scope
Thiết kế kiến trúc quản lý vòng đời tài nguyên và bộ cấp phát bộ nhớ GPU (GPU Memory Allocator & Lifetime Management) trên các API đồ họa cấp thấp hiện đại: Vulkan, DirectX 12 và Metal; triệt tiêu hoàn toàn rò rỉ bộ nhớ đồ họa VRAM, tối ưu hóa các bộ đệm trung gian (Staging Buffers) và xử lý khôi phục sự cố mất thiết bị đồ họa (Device Loss Recovery).

## 2. When to Use
- Khi phát triển động cơ kết xuất đồ họa hiệu năng cao sử dụng Vulkan (`vkAllocateMemory`) hoặc DirectX 12 (`ID3D12Resource`).
- Khi trò chơi bị sập với lỗi `VK_ERROR_OUT_OF_DEVICE_MEMORY` hoặc `DXGI_ERROR_DEVICE_REMOVED` sau một thời gian chơi dài.
- Khi cần tối ưu hóa tốc độ tải và giải phóng hàng nghìn texture mô hình 3D mà không làm khựng game.

## 3. When NOT to Use
- Khi làm việc với các API đồ họa cấp cao tự động dọn rác như Three.js hoặc Babylon.js.
- Khi lập trình ứng dụng văn phòng thông thường.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kiến thức về các loại bộ nhớ GPU (Device Local, Host Visible, Host Coherent), thư viện Vulkan Memory Allocator (VMA) hoặc D3D12MA.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Sub-allocation from Large Heaps:** Trình điều khiển GPU giới hạn số lần gọi cấp phát bộ nhớ trực tiếp (thường tối đa 4,096 lần); giải pháp chuẩn là cấp phát các khối VRAM lớn (256MB) và tự chia nhỏ (Sub-allocate) cho từng tài nguyên.
- **Staging Buffer Ring:** Bộ đệm trung gian nằm trên RAM CPU cho phép ghi dữ liệu nhanh và sử dụng lệnh DMA chuyển sang bộ nhớ siêu tốc của GPU trong nền.
- **Device Loss Recovery Flow:** Khi card màn hình bị tháo rời hoặc driver bị khởi động lại, phải giải phóng sạch toàn bộ tài nguyên cũ và tái tạo lại Swapchain và Pipeline.

## 6. Step-by-Step Execution Workflow
1. Tích hợp thư viện Vulkan Memory Allocator (VMA) vào dự án.
2. Phân loại các tài nguyên theo mục đích sử dụng (Static Meshes, Dynamic Uniforms, Render Targets).
3. Cấp phát các tài nguyên tĩnh vào vùng nhớ `VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT`.
4. Sử dụng Staging Buffer dạng vòng tròn (Ring Buffer) để tải dữ liệu bất đồng bộ.
5. Thiết lập cơ chế bắt mã lỗi `VK_ERROR_DEVICE_LOST` để thực hiện quy trình tái tạo tài nguyên an toàn.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```cpp
// Safe GPU Memory Allocation using Vulkan Memory Allocator (VMA)
#include "vk_mem_alloc.h"

VkBuffer createGpuBuffer(VmaAllocator allocator, VkDeviceSize size, VkBufferUsageFlags usage) {
    VkBufferCreateInfo bufferInfo = { VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO };
    bufferInfo.size = size;
    bufferInfo.usage = usage;
    bufferInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;

    VmaAllocationCreateInfo allocInfo = {};
    allocInfo.usage = VMA_MEMORY_USAGE_AUTO_PREFER_DEVICE; // Prefer fast VRAM

    VkBuffer buffer;
    VmaAllocation allocation;
    vmaCreateBuffer(allocator, &bufferInfo, &allocInfo, &buffer, &allocation, nullptr);
    return buffer;
}
```

## 8. Anti-Patterns & Common Traps
- Gọi lệnh `vkAllocateMemory` trực tiếp cho từng tấm ảnh texture nhỏ vài KB làm cạn kiệt giới hạn cấp phát của driver và làm sập game.
- Quên giải phóng tài nguyên đồ họa khi chuyển đổi giữa các màn chơi, dẫn đến việc VRAM tăng lũy tiến đến khi đầy đĩa.
- Ghi dữ liệu từ CPU thẳng vào bộ nhớ Device Local của GPU mà không qua Staging Buffer khiến băng thông bị bóp nghẹt nghiêm trọng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Không có hiện tượng rò rỉ bộ nhớ VRAM (0 bytes leaked) sau khi chuyển đổi qua lại 10 màn chơi khác nhau.
- QG-02: 100% các tài nguyên tĩnh được nạp vào bộ nhớ Device Local thông qua Staging Buffer.
- QG-03: Khôi phục ứng dụng thành công sau khi giả lập sự kiện reset driver đồ họa.

## 10. Security & Safety Boundaries
- Xóa sạch dữ liệu trong các bộ đệm VRAM nhạy cảm trước khi tái sử dụng để ngăn ngừa rò rỉ hình ảnh giữa các tiến trình đồ họa khác nhau.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Lớp quản lý bộ nhớ GPU `GpuMemoryManager.cpp`.
1. Quy trình xử lý sự cố mất thiết bị đồ họa `DeviceLossRecovery.hpp`.

## 13. Related & Complementary Skills
- [`dex-gpu-shader-profiling`](.agents/skills/dex-gpu-shader-profiling/SKILL.md)
- [`dex-webgpu-rendering-fundamentals`](.agents/skills/dex-webgpu-rendering-fundamentals/SKILL.md)
- [`dex-asset-pipeline-optimization`](.agents/skills/dex-asset-pipeline-optimization/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phần mềm mô phỏng bản vẽ kiến trúc 3D bị crash sau 30 phút sử dụng do ngốn hết 12GB VRAM card màn hình. Kỹ sư kích hoạt `dex-gpu-resource-lifetime`, tích hợp Vulkan Memory Allocator với cơ chế gộp khối và tự động dọn rác các mô hình khuất tầm nhìn, giảm mức tiêu thụ VRAM xuống ổn định ở 3.2GB và chấm dứt hoàn toàn hiện tượng sập phần mềm.
