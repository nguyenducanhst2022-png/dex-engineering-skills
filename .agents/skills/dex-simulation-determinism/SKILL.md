---
name: dex-simulation-determinism
description: Engineer bit-level deterministic simulation loops using fixed-point arithmetic, isolated PRNG streams, and zero-float divergence across heterogeneous OS architectures (Windows/Linux/macOS). Use when developing lockstep multiplayer games, physics replays, or scientific simulations.
---

# dex-simulation-determinism

## 1. Purpose & Scope
Thiết kế và hiện thực hóa các vòng lặp mô phỏng có tính xác định tuyệt đối đến từng bit (Bit-Level Deterministic Simulation Loops); ứng dụng số học dấu phẩy tĩnh (Fixed-Point Arithmetic) triệt tiêu sai số dấu phẩy động (Float Divergence), luồng sinh số ngẫu nhiên cô lập (Seeded PRNG) và độc lập hoàn toàn với kiến trúc hệ điều hành (Windows, Linux, macOS); phục vụ các game nhiều người chơi đồng bộ khóa bước (Lockstep Multiplayer) và hệ thống phát lại mô phỏng vật lý.

## 2. When to Use
- Khi xây dựng game chiến thuật thời gian thực (RTS) hoặc game đối kháng sử dụng mô hình mạng Lockstep hoặc Rollback Netcode (GGPO).
- Khi phát lại một trận đấu từ tệp ghi nhật ký thao tác (Input Replay) mà kết quả giữa hai máy tính khác nhau bị phân kỳ (Desync).
- Khi chạy các mô phỏng vật lý khoa học đòi hỏi kết quả lặp lại hoàn toàn trùng khớp 100% trên mọi nền tảng.

## 3. When NOT to Use
- Khi game chơi đơn thông thường không có tính năng phát lại và không cần đồng bộ qua mạng.
- Khi các ứng dụng web kinh doanh thông thường không liên quan đến mô phỏng vật lý.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư viện toán học số thực dấu phẩy tĩnh (Fixed-point math như `Fixed64` hoặc `fpm`), bộ sinh số ngẫu nhiên xác định (Xoshiro256** hoặc PCG).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Floating-Point Non-Determinism:** Phép tính số thực dấu phẩy động `float/double` (IEEE 754) cho ra các kết quả khác nhau ở các bit cuối trên các CPU Intel, AMD, ARM và các mức cờ tối ưu của trình biên dịch.
- **Lockstep State Synchronization:** Chỉ truyền các nút bấm của người chơi qua mạng thay vì truyền tọa độ; tất cả các máy khách tự tính toán và ra kết quả giống hệt nhau.
- **Desync Detection Checksum:** Tính toán mã băm trạng thái thế giới (State Hash) ở mỗi khung hình để phát hiện sự phân kỳ ngay từ khung hình đầu tiên.

## 6. Step-by-Step Execution Workflow
1. Thay thế toàn bộ kiểu dữ liệu `float` và `double` trong logic mô phỏng bằng kiểu số thực dấu phẩy tĩnh `fp64` (Q32.32 hoặc Q48.16).
2. Khởi tạo bộ sinh số ngẫu nhiên PRNG có hạt giống (Seed) được lưu trong trạng thái thế giới.
3. Thực thi cập nhật trạng thái theo bước thời gian cố định (Fixed Delta Time).
4. Tính toán mã băm trạng thái toàn cục `state_hash` sau mỗi 60 khung hình mô phỏng.
5. Chạy mô phỏng 10,000 khung hình trên cả Windows x86-64 và Linux ARM64 để đối chiếu mã băm trạng thái.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```cpp
// Fixed-Point 32.32 Deterministic Vector Implementation
#include <cstdint>

struct Fixed64 {
    int64_t raw;
    static constexpr int64_t SCALE = 1LL << 32;

    static Fixed64 from_int(int32_t val) { return { static_cast<int64_t>(val) * SCALE }; }
    Fixed64 operator+(const Fixed64& o) const { return { raw + o.raw }; }
    Fixed64 operator*(const Fixed64& o) const { return { (raw * o.raw) / SCALE }; }
};

struct DeterministicEntity {
    Fixed64 posX;
    Fixed64 posY;
    Fixed64 velX;
    Fixed64 velY;

    void tick() {
        posX = posX + velX;
        posY = posY + velY;
    }
};
```

## 8. Anti-Patterns & Common Traps
- Dùng `Math.random()` hoặc hàm ngẫu nhiên của hệ điều hành `rand()` bên trong logic gameplay đồng bộ lockstep.
- Sử dụng kiểu dữ liệu `float` cho vị trí và vận tốc trong game đồng bộ mạng lockstep.
- Duyệt qua các phần tử của bảng băm `std::unordered_map` mà không sắp xếp (thứ tự duyệt phần tử không xác định giữa các nền tảng).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Mã băm trạng thái (State Checksum) trùng khớp 100% từng bit sau 50,000 khung hình mô phỏng giữa Windows và Linux.
- QG-02: 100% các phép tính toán học trong logic trò chơi sử dụng Fixed-Point Math.
- QG-03: Tệp ghi lại thao tác người dùng (Replay file) phát lại ra kết quả trận đấu giống hệt nhau 100 lần liên tiếp.

## 10. Security & Safety Boundaries
- Ngăn chặn các phần mềm gian lận (Speedhack) can thiệp vào bộ đếm thời gian hệ thống bằng cách xác thực tính nhất quán của chuỗi tick từ client.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Thư viện toán học số học xác định `FixedPointMath.hpp`.
1. Bộ test tự động kiểm tra hiện tượng phân kỳ trạng thái `desync_detector.py`.

## 13. Related & Complementary Skills
- [`dex-chess-engine-search-testing`](.agents/skills/dex-chess-engine-search-testing/SKILL.md)
- [`dex-physics-engine-validation`](.agents/skills/dex-physics-engine-validation/SKILL.md)
- [`dex-game-loop-timing`](.agents/skills/dex-game-loop-timing/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Game chiến thuật nhiều người chơi bị lỗi mất đồng bộ (Desync) ngẫu nhiên mỗi khi người chơi trên PC thi đấu với người chơi trên iPhone. Kỹ sư kích hoạt `dex-simulation-determinism`, phát hiện việc tính toán góc quay dùng `std::sin(float)` cho ra kết quả lệch 1 bit ở số thập phân thứ 7 giữa chip Intel và Apple Silicon. Thay thế bằng bảng sin tra cứu Fixed-Point, triệt tiêu hoàn toàn lỗi desync.
