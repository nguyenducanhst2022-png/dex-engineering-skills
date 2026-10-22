---
name: dex-rendering-frame-pacing
description: Diagnose frame time variance, 1% low FPS, pipeline presentation latencies, and display VSync synchronization glitches. Use when eliminating micro-stutters, tuning Android/Vulkan frame pacers, or optimizing VR motion-to-photon latency.
---

# dex-rendering-frame-pacing

## 1. Purpose & Scope
Đo lường, chẩn đoán và đồng nhất hóa nhịp độ hiển thị khung hình (Rendering Frame Pacing); triệt tiêu phương sai thời gian khung hình (Frame Time Variance), tối ưu hóa chỉ số FPS thấp 1% (1% Low FPS), độ trễ đường ống hiển thị (Presentation Latency) và các lỗi không đồng bộ làm rách hình (VSync Tearing / Jitter); phục vụ mang lại trải nghiệm thị giác mượt mà không bị giật vi mô trên Android, Vulkan, DirectX và kính thực tế ảo VR.

## 2. When to Use
- Khi game đo được chỉ số FPS trung bình là 60 nhưng người chơi vẫn cảm thấy hình ảnh bị giật khựng từng đợt (Micro-stutters).
- Khi tối ưu hóa game trên thiết bị di động Android sử dụng thư viện Android Frame Pacing Library (Swappy).
- Khi xây dựng ứng dụng thực tế ảo (VR) cần đảm bảo độ trễ từ chuyển động đến điểm ảnh (Motion-to-Photon Latency) dưới 20ms để chống say xe.

## 3. When NOT to Use
- Khi ứng dụng không có hoạt cảnh chuyển động liên tục.
- Khi kiểm tra hiệu năng tính toán thuật toán không hiển thị đồ họa.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Công cụ đo lường thời gian hiển thị khung hình (PresentMon, CapFrameX hoặc Android GPU Inspector), card đồ họa hỗ trợ VSync/G-Sync/FreeSync.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **1% Low FPS Metric:** Chỉ số trung bình của 1% các khung hình chạy chậm nhất trong phiên chơi; phản ánh chân thực độ mượt mà của game hơn nhiều so với chỉ số FPS trung bình.
- **Buffer Queuing Latency:** Số lượng khung hình nằm chờ trong hàng đợi hiển thị (Triple Buffering làm tăng FPS nhưng tăng độ trễ điều khiển con trỏ).
- **Tearing vs Stuttering:** Rách hình xảy ra khi GPU nạp khung hình mới giữa lúc màn hình đang quét tia; giật khựng xảy ra khi GPU bị lỡ nhịp quét VSync của màn hình.

## 6. Step-by-Step Execution Workflow
1. Thu thập biểu đồ phân bố thời gian từng khung hình (Frame Time Graph) bằng PresentMon.
2. Nhận diện các đỉnh gai thời gian khung hình vượt quá 16.6ms (cho màn 60Hz) hoặc 8.3ms (cho màn 120Hz).
3. Cấu hình cơ chế đồng bộ khung hình mượt mà (chế độ Mailbox hoặc FIFO trong Vulkan / DirectX).
4. Tích hợp thư viện điều phối nhịp độ khung hình (Frame Pacer) để đồng bộ nhịp đẩy frame khớp với nhịp quét của màn hình.
5. Xác nhận chỉ số 1% Low FPS được nâng lên sát với chỉ số FPS trung bình.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```cpp
// Vulkan Frame Pacing Present Mode Selection
#include <vulkan/vulkan.h>
#include <vector>

VkPresentModeKHR selectOptimalPresentMode(const std::vector<VkPresentModeKHR>& availableModes) {
    // Prefer Mailbox (Triple Buffering without tearing & low latency)
    for (const auto& mode : availableModes) {
        if (mode == VK_PRESENT_MODE_MAILBOX_KHR) {
            return mode;
        }
    }
    // Fallback to FIFO (Standard VSync, guaranteed support)
    return VK_PRESENT_MODE_FIFO_KHR;
}
```

## 8. Anti-Patterns & Common Traps
- Chỉ tự hào khoe chỉ số FPS trung bình đạt 120 trong khi đồ thị frame time liên tục nhảy nhót từ 8ms lên 45ms khiến game thủ cảm thấy giật lag nặng.
- Để hàng đợi khung hình GPU (Max Pre-rendered Frames) lên tới 4 hoặc 5 khung hình làm tăng độ trễ điều khiển chuột gây cảm giác lướt trên băng.
- Bỏ qua việc khóa tốc độ khung hình (Frame Rate Limiting) dẫn đến việc GPU chạy hết 100% công suất gây quá nhiệt và bóp nghẹt xung nhịp (Thermal Throttling).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Phương sai thời gian khung hình duy trì dưới 1.5ms trong suốt 99% thời gian chơi.
- QG-02: Chỉ số 1% Low FPS đạt tối thiểu 85% giá trị của FPS trung bình.
- QG-03: Không có hiện tượng rách hình (Tearing) hoặc lỡ nhịp quét VSync trên màn hình thử nghiệm.

## 10. Security & Safety Boundaries
- Không sử dụng các tiện ích can thiệp hook vào API đồ họa không rõ nguồn gốc để đo đạc có thể bị hệ thống chống hack (Anti-cheat) cấm tài khoản.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bản phân tích thời gian khung hình `FRAME_PACING_AUDIT.md`.
1. Module cấu hình đồng bộ hiển thị màn hình chuẩn `FramePacerConfig.cpp`.

## 13. Related & Complementary Skills
- [`dex-game-loop-timing`](.agents/skills/dex-game-loop-timing/SKILL.md)
- [`dex-gpu-shader-profiling`](.agents/skills/dex-gpu-shader-profiling/SKILL.md)
- [`dex-real-time-input-latency`](.agents/skills/dex-real-time-input-latency/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Game đối kháng 3D trên Android có FPS trung bình 60 nhưng người chơi liên tục than phiền bị khựng hình khi ra đòn. Kỹ sư kích hoạt `dex-rendering-frame-pacing`, dùng Android GPU Inspector phát hiện bộ đệm hiển thị bị trễ nhịp so với tần số quét của màn hình điện thoại, tích hợp thư viện Swappy Frame Pacing, đưa chỉ số 1% Low từ 28 FPS lên thẳng 58 FPS mượt mà.
