---
name: dex-chess-uci-protocol-compliance
description: Implement, test, and verify complete Universal Chess Interface (UCI) protocol compliance. Handle asynchronous commands, stop/ponder mechanics, option schemas, and engine state machines.
---

# dex-chess-uci-protocol-compliance

## 1. Purpose & Scope
Thiết kế, kiểm thử và chứng minh tính tuân thủ tuyệt đối chuẩn giao thức quốc tế Universal Chess Interface (UCI); điều phối máy trạng thái bất đồng bộ của engine cờ vua (Asynchronous Engine State Machine); xử lý mượt mà các luồng lệnh `uci`, `isready`, `ucinewgame`, `position`, `go`, `stop`, `ponderhit` và `quit`; bảo đảm engine tương thích hoàn hảo với các phần mềm giao diện thi đấu hàng đầu (Cutechess, Fritz, Arena, Lichess Bots).

## 2. When to Use
- Khi xuất bản engine cờ vua ra cộng đồng hoặc kết nối vào các hệ thống giải đấu tự động (TCEC, CCC, Lichess Bot).
- Khi engine bị treo (deadlock), bỏ qua lệnh `stop` từ GUI, hoặc xuất ra các chuỗi thông tin tìm kiếm (PV lines) sai cú pháp.
- Khi thiết lập hệ thống tùy chỉnh tham số engine (`setoption name ... value ...`) cho Hash, Threads, MultiPV.

## 3. When NOT to Use
- Khi phát triển engine sử dụng giao thức cũ WinBoard/XBoard (trừ khi xây dựng adapter chuyển đổi giao thức).
- Khi kiểm thử nội bộ các hàm thuật toán không liên quan đến tầng giao tiếp vào/ra (I/O).

## 4. Prerequisites & Input Context
- **Luồng giao tiếp:** Tiêu chuẩn Standard I/O (stdin/stdout) hoạt động trên tiến trình độc lập không có buffer trễ.
- **Harness kiểm thử:** Công cụ `cutechess-cli` hoặc script Python giả lập GUI kiểm thử giao thức.

## 5. Core Concepts & Taxonomy
- **UCI Asynchronous Command Loop:** Luồng I/O độc lập đọc các lệnh từ stdin trong khi luồng tìm kiếm (Search Worker Thread) đang duyệt cây tính toán.
- **Pondering:** Trạng thái engine suy nghĩ tính toán trước nước đi trong thời gian đối phương đang suy nghĩ (`go ponder`).
- **UCI Info String Format:** Cú pháp chuẩn xuất thông tin đánh giá: `info depth 14 seldepth 20 score cp 45 nodes 125000 nps 1500000 time 83 pv e2e4 e7e5 g1f3`.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo luồng lắng nghe `stdin` không chặn (Non-blocking I/O hoặc Background Reader Thread).
2. Khi nhận lệnh `uci`, xuất ra thông tin tác giả, các tùy chọn `option name ... type ...` và kết thúc bằng `uciok`.
3. Khi nhận lệnh `isready`, đồng bộ hóa bộ nhớ và xuất ra `readyok`.
4. Phân tích lệnh `position [fen <fenstring> | startpos] moves <move1> ... <moveN>` và cập nhật trạng thái bàn cờ.
5. Xử lý lệnh `go`: phân bổ thời gian tính toán dựa trên `wtime`, `btime`, `winc`, `binc` hoặc `movetime`.
6. Khi nhận lệnh `stop`, gửi tín hiệu hủy (`std::atomic<bool> stop_flag = true`), chờ luồng tìm kiếm kết thúc và in ra `bestmove <move>`.

## 7. Concrete Examples
### Vong lap xu ly lenh UCI bat dong bo trong C++20:
```cpp
#include <iostream>
#include <string>
#include <sstream>
#include <thread>
#include <atomic>

std::atomic<bool> is_searching{false};
std::atomic<bool> stop_search{false};
std::thread search_thread;

void handle_uci() {
    std::cout << "id name DEX-ChessEngine 9.0\n";
    std::cout << "id author Principal DEX Agent\n";
    std::cout << "option name Hash type spin default 64 min 1 max 32768\n";
    std::cout << "option name Threads type spin default 1 min 1 max 256\n";
    std::cout << "uciok" << std::endl;
}

void uci_loop() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);
        std::string token;
        iss >> token;

        if (token == "uci") {
            handle_uci();
        } else if (token == "isready") {
            std::cout << "readyok" << std::endl;
        } else if (token == "ucinewgame") {
            // Reset Transposition Table va lich su
        } else if (token == "position") {
            // Parse FEN va moves
        } else if (token == "go") {
            stop_search = false;
            is_searching = true;
            if (search_thread.joinable()) search_thread.join();
            search_thread = std::thread([]() {
                // Thuc hien tim kiem tren worker thread
                std::cout << "bestmove e2e4" << std::endl;
                is_searching = false;
            });
        } else if (token == "stop") {
            stop_search = true;
            if (search_thread.joinable()) search_thread.join();
        } else if (token == "quit") {
            stop_search = true;
            if (search_thread.joinable()) search_thread.join();
            break;
        }
    }
}
```

## 8. Anti-Patterns & Common Traps
- **Blocking Stdin on Search:** Đọc stdin trên cùng luồng tìm kiếm khiến engine không thể nhận được lệnh `stop` khi đang tính toán độ sâu lớn.
- **Missing Flushing of Stdout:** Quên gọi `std::endl` hoặc `fflush(stdout)` khiến các thông điệp `readyok` hoặc `bestmove` bị nghẽn trong bộ đệm hệ thống.
- **Printing Unformatted Debug Output:** Xuất các dòng text debug linh tinh không theo cú pháp `info string ...` làm sập trình phân tích cú pháp của GUI.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Vượt qua 100% các bài kiểm tra giao thức của bộ test `cutechess-cli` mà không có lỗi timeout.
- **QG-02**: Engine phản hồi lệnh `stop` và in ra `bestmove` trong vòng tối đa 20ms.
- **QG-03**: Toàn bộ chuỗi xuất thông tin đều tuân thủ chính xác đặc tả UCI Specification.

## 10. Security & Safety Boundaries
- Giới hạn độ dài tối đa của dòng lệnh đầu vào từ stdin (tối đa 4096 ký tự) ngăn ngừa lỗi tràn bộ đệm chuỗi.

## 11. Platform Adapters
- **Runtimes**: C++20, Rust, Cutechess-cli, Python python-chess library, Arena Chess GUI.

## 12. Deliverables & Output Artifacts
- Mô-đun phân tích giao thức UCI (`uci.cpp` / `uci.rs`).
- Kịch bản kiểm thử bắt tay giao thức UCI tự động (`test_uci_handshake.py`).

## 13. Related & Complementary Skills
dex-chess-search-pruning-evals, dex-chess-transposition-table-correctness, dex-chess-engine-match-statistics

## 14. Realistic Usage Example
```bash
# Kiem thu tinh tuong thich UCI bang cutechess-cli
cutechess-cli -engine cmd=./my_engine name=MyEngine -each tc=10+0.1 -rounds 2
```
