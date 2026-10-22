---
name: dex-physics-engine-validation
description: Validate 2D/3D rigid-body physics engines, measuring energy conservation invariants, continuous collision detection (CCD) tunneling prevention, solver constraint stability, and restitution accuracy. Use when engineering physics simulations, robotics controllers, or action game mechanics.
---

# dex-physics-engine-validation

## 1. Purpose & Scope
Kiểm chứng và thẩm định tính đúng đắn của động cơ vật lý vật rắn (Rigid-Body Physics Engine Validation); đo lường sự bảo toàn cơ năng và động lượng (Energy & Momentum Conservation), cơ chế phát hiện va chạm liên tục (Continuous Collision Detection - CCD) chống hiện tượng vật thể xuyên tường (Tunneling), độ ổn định của bộ giải ràng buộc (Solver Constraints) và hệ số phục hồi va chạm (Restitution).

## 2. When to Use
- Khi xây dựng hoặc tích hợp động cơ vật lý (Box2D, PhysX, Jolt Physics hoặc Rapier).
- Khi các vật thể di chuyển ở tốc độ cao bị xuyên thủng qua bức tường mỏng mà không phát sinh va chạm.
- Khi các chồng hộp hoặc vật thể xếp chồng lên nhau bị rung lắc dữ dội hoặc tự động nảy tung lên không rõ lý do.

## 3. When NOT to Use
- Khi làm game theo lượt hoặc game giao diện không có yếu tố tương tác vật lý.
- Khi mô phỏng vật lý hạt hoặc biến dạng chất lỏng quy mô vi mô (CFD).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Động cơ vật lý mục tiêu (Rapier, Box2D hoặc PhysX), kịch bản kiểm thử vật lý tiêu chuẩn (Stacking test, High-speed projectile test).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Tunneling Effect:** Hiện tượng viên đạn hoặc xe đua di chuyển một quãng đường quá lớn trong một bước thời gian $\Delta t$, nhảy cóc từ phía trước tường sang phía sau tường mà không có điểm giao cắt tại thời điểm rời rạc.
- **Continuous Collision Detection (CCD):** Sử dụng thuật toán quét khối (Swept Volume) hoặc kiểm tra thời gian va chạm (Time of Impact - TOI) để bắt va chạm liên tục trên đoạn đường di chuyển.
- **Constraint Solver Jitter:** Hiện tượng dao động số học trong bộ giải ràng buộc tiếp xúc (Iterative Impulse Solver) khi giải quyết các chồng vật thể nặng xếp lên nhau.

## 6. Step-by-Step Execution Workflow
1. Xây dựng kịch bản kiểm thử viên đạn siêu tốc bắn vào tấm tường mỏng 1cm ở các góc nghiêng khác nhau.
2. Kiểm tra xem cờ CCD có phát hiện chính xác thời điểm va chạm TOI hay không.
3. Tạo kịch bản kiểm thử chồng 20 hộp chữ nhật để đo lường độ ổn định của bộ giải tiếp xúc và độ lún hình học (Penetration Slop).
4. Tính toán tổng cơ năng (Động năng + Thế năng) của con lắc đơn qua 1,000 chu kỳ dao động để đo độ rò rỉ năng lượng.
5. Lập biên bản đánh giá tính ổn định của động cơ vật lý `PHYSICS_STABILITY_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```cpp
// Validating Energy Conservation in Rigid-Body Physics
#include <iostream>
#include <cmath>

struct PhysicalState {
    double kineticEnergy;
    double potentialEnergy;
    double totalEnergy() const { return kineticEnergy + potentialEnergy; }
};

bool validate_energy_conservation(const PhysicalState& initial, const PhysicalState& current, double tolerance = 0.01) {
    double initialE = initial.totalEnergy();
    double currentE = current.totalEnergy();
    double drift = std::abs(currentE - initialE) / initialE;
    return drift <= tolerance;
}
```

## 8. Anti-Patterns & Common Traps
- Tăng bước thời gian vật lý $\Delta t$ quá lớn (ví dụ 100ms) để tiết kiệm CPU khiến toàn bộ hệ thống vật lý bị phát nổ (Explosion bug).
- Bỏ qua bước cấu hình CCD cho các vật thể nhỏ di chuyển nhanh khiến người chơi bị rớt xuống dưới đáy bản đồ.
- Đặt trọng lượng giữa hai vật thể nối với nhau chênh lệch hàng triệu lần (ví dụ vật 1g nối với vật 1,000,000kg) làm sập bộ giải tiếp xúc.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Không có hiện tượng xuyên tường (Zero Tunneling) ở vận tốc vật thể lên tới 500 m/s khi bật CCD.
- QG-02: Chồng 15 hộp vật lý đứng yên ổn định không bị trôi dạt hoặc rung lắc trong 60 giây.
- QG-03: Sự suy giảm cơ năng của hệ dao động không ma sát không vượt quá 0.5% sau 1,000 bước tính toán.

## 10. Security & Safety Boundaries
- Đặt giới hạn vận tốc tối đa và số lượng va chạm tối đa cho mỗi khung hình để ngăn ngừa kẻ gian làm sập server game bằng cách tạo hàng nghìn va chạm cùng lúc.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bộ kịch bản kiểm thử độ ổn định vật lý `PhysicsVerificationSuite.cpp`.
1. Báo cáo thẩm định an toàn động cơ vật lý `PHYSICS_STABILITY_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-simulation-determinism`](.agents/skills/dex-simulation-determinism/SKILL.md)
- [`dex-game-loop-timing`](.agents/skills/dex-game-loop-timing/SKILL.md)
- [`dex-rendering-frame-pacing`](.agents/skills/dex-rendering-frame-pacing/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Game đua xe bắn súng gặp lỗi người chơi bắn tên lửa thường xuyên bay xuyên qua vỏ xe tăng của đối thủ mà không nổ. Kỹ sư kích hoạt `dex-physics-engine-validation`, phát hiện tên lửa di chuyển 12 mét mỗi frame trong khi vỏ xe chỉ dày 0.2 mét và chưa bật CCD. Kích hoạt tính năng Swept Shape CCD cho tên lửa, triệt tiêu hoàn toàn 100% hiện tượng xuyên vật thể.
