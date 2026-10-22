---
name: dex-game-loop-timing
description: Implement rock-solid game loop architectures with fixed timestep physics updates, accumulator buffer smoothing, variable frame rendering interpolation, and spiral-of-death panics. Use when engineering deterministic game runtimes, interactive simulations, or VR render loops.
---

# dex-game-loop-timing

## 1. Purpose & Scope
Thiết kế và hiện thực hóa kiến trúc vòng lặp trò chơi (Game Loop Architecture) vững chắc như bàn thạch; tách bạch hoàn toàn giữa bước cập nhật vật lý theo thời gian cố định (Fixed Timestep Update) và bước kết xuất đồ họa theo thời gian biến thiên (Variable Frame Rendering); ứng dụng bộ đệm tích lũy thời gian (Time Accumulator) kèm nội suy trạng thái (State Interpolation) và cơ chế phòng chống vòng xoáy tử thần (Spiral-of-Death Panic).

## 2. When to Use
- Khi xây dựng game engine hoặc ứng dụng đồ họa tương tác thời gian thực từ đầu.
- Khi chuyển động của nhân vật game bị giật cục hoặc chạy nhanh gấp đôi trên màn hình tần số quét cao (144Hz/240Hz).
- Khi máy tính cấu hình yếu bị sập hoàn toàn do rơi vào vòng lặp cập nhật vật lý không hồi kết (Spiral of Death).

## 3. When NOT to Use
- Khi phát triển các ứng dụng form doanh nghiệp truyền thống cập nhật theo sự kiện bấm chuột.
- Khi xây dựng các dịch vụ backend xử lý theo lô.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Đồng hồ đo thời gian độ chính xác cao (`std::chrono::high_resolution_clock` hoặc `performance.now()`), kiến thức về bài toán 'Fix Your Timestep!'.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Fixed Timestep for Physics:** Cập nhật vật lý và logic gameplay luôn ở một khoảng thời gian cố định chính xác (ví dụ $\Delta t = 1/60s = 16.66ms$) để bảo toàn tính xác định.
- **Time Accumulator & Interpolation:** Tích lũy thời gian thực tế đã trôi qua và chạy số lượng bước cố định tương ứng; nội suy hình ảnh giữa trạng thái cũ và mới bằng tỷ lệ dư thừa $\alpha = accumulator / dt$.
- **Spiral of Death Prevention:** Giới hạn số lượng bước cập nhật tối đa trong một khung hình (ví dụ `maxSubSteps = 5`) để ngăn CPU bị quá tải khi frame render bị trễ.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo đồng hồ đo thời gian có độ chính xác micro-giây.
2. Đo lường thời gian trôi qua thực tế kể từ khung hình trước (`frameTime`).
3. Cộng dồn `frameTime` vào biến tích lũy `accumulator`.
4. Chạy vòng lặp cập nhật logic cố định `while (accumulator >= dt)` và trừ dần `accumulator`.
5. Tính toán hệ số nội suy $\alpha$ và gọi hàm kết xuất đồ họa `render(alpha)`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```cpp
// Canonical 'Fix Your Timestep' Game Loop Implementation
#include <chrono>

void run_game_loop() {
    using clock = std::chrono::high_resolution_clock;
    auto previousTime = clock::now();
    double accumulator = 0.0;
    const double dt = 1.0 / 60.0; // 60Hz fixed physics update
    const double maxFrameTime = 0.25; // Clamp to prevent Spiral of Death

    while (isRunning) {
        auto currentTime = clock::now();
        std::chrono::duration<double> elapsed = currentTime - previousTime;
        previousTime = currentTime;

        double frameTime = std::min(elapsed.count(), maxFrameTime);
        accumulator += frameTime;

        while (accumulator >= dt) {
            update_physics(dt);
            accumulator -= dt;
        }

        const double alpha = accumulator / dt;
        render_interpolated(alpha);
    }
}
```

## 8. Anti-Patterns & Common Traps
- Nhân trực tiếp biến thời gian `delta_time` vào vị trí nhân vật trong hàm render (`x += speed * dt`) khiến vật lý bị lỗi nhảy cóc khi máy tính bị lag.
- Không giới hạn thời gian khung hình tối đa, dẫn đến việc khi máy tính bị lag 1 giây, vòng lặp cố chạy 60 bước vật lý làm máy tính càng lag hơn và sập luôn ứng dụng (Spiral of Death).
- Không nội suy trạng thái khi render trên màn hình 144Hz, khiến hình ảnh nhìn bị giật rung dù FPS đo được rất cao.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Logic vật lý chạy ở tốc độ cập nhật cố định tuyệt đối bất kể màn hình hiển thị ở 30Hz, 60Hz hay 144Hz.
- QG-02: Không bao giờ rơi vào vòng xoáy tử thần khi tạm dừng cửa sổ ứng dụng 5 giây.
- QG-03: Chuyển động hiển thị mượt mà không có hiện tượng rung giật vi mô (Micro-stuttering) nhờ hệ số nội suy $\alpha$.

## 10. Security & Safety Boundaries
- Chống việc người dùng can thiệp vào đồng hồ hệ điều hành để tăng tốc độ nhân vật trong game (Speed-hacking) bằng cách kiểm tra bước thời gian từ máy chủ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Kiến trúc vòng lặp game hoàn chỉnh `GameLoopEngine.cpp`.
1. Bộ quy chuẩn nội suy trạng thái đồ họa theo hệ số alpha.

## 13. Related & Complementary Skills
- [`dex-simulation-determinism`](.agents/skills/dex-simulation-determinism/SKILL.md)
- [`dex-rendering-frame-pacing`](.agents/skills/dex-rendering-frame-pacing/SKILL.md)
- [`dex-real-time-input-latency`](.agents/skills/dex-real-time-input-latency/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Một tựa game hành động khi chạy trên màn hình MacBook Pro 120Hz thì nhân vật di chuyển nhanh gấp đôi so với trên máy tính văn phòng 60Hz. Kỹ sư kích hoạt `dex-game-loop-timing`, triển khai vòng lặp Fixed Timestep 60Hz kết hợp nội suy Alpha cho bước render, giúp nhân vật di chuyển đúng tốc độ thiết kế trên mọi loại màn hình với độ mượt mà tuyệt đối.
