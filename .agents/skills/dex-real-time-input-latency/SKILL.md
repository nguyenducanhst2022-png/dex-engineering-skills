---
name: dex-real-time-input-latency
description: Diagnose and minimize end-to-end user input latency, raw input device polling, OS event pump queuing, render pipeline latency, and display scanout synchronization. Use when building competitive esports games, audio DAWs, or high-responsiveness stylus drawing apps.
---

# dex-real-time-input-latency

## 1. Purpose & Scope
Đo lường, chẩn đoán và giảm thiểu độ trễ thao tác đầu vào từ đầu đến cuối (End-to-End Input Latency / Motion-to-Photon); tối ưu hóa việc lấy mẫu thiết bị đầu vào thô (Raw Input Polling), bơm xử lý sự kiện hệ điều hành (OS Event Pump), độ trễ đường ống kết xuất và đồng bộ hóa quét hình hiển thị; phục vụ các tựa game thể thao điện tử thi đấu chuyên nghiệp, phần mềm âm thanh kỹ thuật số (DAW) và ứng dụng vẽ bút cảm ứng có độ nhạy tức thì.

## 2. When to Use
- Khi người chơi game bắn súng phàn nàn việc di chuột có cảm giác bị nặng, trễ hoặc trôi (Input Lag).
- Khi xây dựng ứng dụng vẽ trên máy tính bảng và cần nét vẽ bám sát đầu bút stylus mà không bị thụt lùi lại phía sau.
- Khi cần đo lường chính xác tổng độ trễ từ lúc bấm phím vật lý đến lúc pixel trên màn hình đổi màu.

## 3. When NOT to Use
- Khi ứng dụng là các website đọc tin tức hoặc biểu mẫu văn phòng thông thường.
- Khi độ trễ vài chục mili-giây không ảnh hưởng đến trải nghiệm người dùng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Chuột/Bàn phím có tần số phản hồi cao (1000Hz+ Polling Rate), màn hình tần số quét cao, công cụ đo độ trễ phần cứng (NVIDIA Reflex Analyzer hoặc máy quay tốc độ cao).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Windows Raw Input API:** Bỏ qua hàng đợi thông điệp cửa sổ thông thường (`WM_MOUSEMOVE`), đọc trực tiếp dữ liệu thô từ cổng USB để giảm thiểu độ trễ của hệ điều hành.
- **Render Queue Latency:** Hàng đợi khung hình render của GPU là thủ phạm lớn nhất gây trễ chuột; giải pháp là kích hoạt công nghệ NVIDIA Reflex hoặc AMD Anti-Lag để GPU chỉ bắt đầu dựng hình ngay khi nhận được input mới nhất.
- **Predictive Input Modeling:** Dự đoán tọa độ tiếp theo của đầu bút vẽ dựa trên vận tốc và gia tốc tức thời để vẽ trước vài mili-giây, tạo cảm giác mực chảy tức thì.

## 6. Step-by-Step Execution Workflow
1. Đăng ký thiết bị đầu vào thô bằng hàm `RegisterRawInputDevices` trên Windows.
2. Lấy mẫu sự kiện chuột/phím ở tần số cao độc lập với tốc độ khung hình của game.
3. Kích hoạt công nghệ NVIDIA Reflex Low Latency Mode trong động cơ kết xuất đồ họa.
4. Đo lường tổng độ trễ hệ thống (System Latency) bằng bộ phân tích Reflex Analyzer.
5. Kiểm tra và xác nhận độ trễ thao tác chuột giảm xuống dưới ngưỡng 15ms.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```cpp
// Registering High-Precision Windows Raw Input for Mouse
#include <windows.h>

void registerRawMouseInput(HWND hwnd) {
    RAWINPUTDEVICE rid[1];
    rid[0].usUsagePage = 0x01; // Generic Desktop Controls
    rid[0].usUsage = 0x02;     // Mouse
    rid[0].dwFlags = RIDEV_INPUTSINK;
    rid[0].hwndTarget = hwnd;

    if (!RegisterRawInputDevices(rid, 1, sizeof(rid[0]))) {
        // Handle error
    }
}
```

## 8. Anti-Patterns & Common Traps
- Dùng tọa độ chuột lấy từ sự kiện cửa sổ thông thường kết hợp với cơ chế làm mượt chuột nội suy quá đà (Mouse Smoothing), gây cảm giác trễ và mất cảm giác rê chuột chân thực.
- Bật chế độ khử răng cưa toàn màn hình hoặc lọc đa mẫu quá nặng khiến GPU bị quá tải và đẩy độ trễ hàng đợi lên trên 60ms.
- Bỏ qua việc tắt cờ tăng tốc chuột của Windows (Mouse Acceleration / Enhance pointer precision).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Độ trễ thao tác chuột tổng thể từ lúc bấm đến lúc hiển thị giảm xuống dưới 18ms ở tốc độ 144Hz.
- QG-02: 100% dữ liệu chuột được nạp qua Raw Input API với tần số lấy mẫu 1000Hz đầy đủ.
- QG-03: Tích hợp thành công SDK giảm độ trễ NVIDIA Reflex hoặc AMD Anti-Lag.

## 10. Security & Safety Boundaries
- Chặn các phần mềm can thiệp gửi sự kiện chuột giả lập (Mouse injection scripts / Aimbot) bằng cách xác thực nguồn gốc phần cứng của Raw Input.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module thu nhận đầu vào độ trễ cực thấp `RawInputManager.cpp`.
1. Báo cáo đối chuẩn độ trễ thao tác hệ thống `INPUT_LATENCY_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-rendering-frame-pacing`](.agents/skills/dex-rendering-frame-pacing/SKILL.md)
- [`dex-game-loop-timing`](.agents/skills/dex-game-loop-timing/SKILL.md)
- [`dex-performance-optimization`](.agents/skills/dex-performance-optimization/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Tựa game bắn súng FPS trực tuyến bị các game thủ thi đấu chê vì cảm giác bắn súng không nhạy bằng đối thủ cạnh tranh. Kỹ sư kích hoạt `dex-real-time-input-latency`, chuyển đổi sang Windows Raw Input và tích hợp NVIDIA Reflex Low Latency SDK, đưa tổng độ trễ từ 42ms xuống chỉ còn 14ms, nhận được sự khen ngợi nhiệt liệt từ cộng đồng thể thao điện tử.
