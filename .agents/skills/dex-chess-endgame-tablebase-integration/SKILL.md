---
name: dex-chess-endgame-tablebase-integration
description: Integrate and verify Syzygy and Nalimov endgame tablebase probing in chess engines. Validate WDL and DTZ semantics, root probing, and safe missing-file fallback.
---

# dex-chess-endgame-tablebase-integration

## 1. Purpose & Scope
Tích hợp và kiểm chứng cơ chế tra cứu cơ sở dữ liệu cờ tàn hoàn hảo (Endgame Tablebases: Syzygy WDL và DTZ); xác thực ngữ nghĩa của kết quả Thắng/Hòa/Thua (Win/Draw/Loss - WDL) và khoảng cách tới nước đi hoàn lại 50 nước (Distance to Zeroing - DTZ); tối ưu hóa tra cứu tại nút gốc (Root Probing) và trong cây tìm kiếm (Search Probing); bảo đảm khả năng phục hồi an toàn khi thiếu tệp dữ liệu mà không làm sập engine.

## 2. When to Use
- Khi thế cờ rút gọn về số lượng quân cờ nhỏ (3-4-5-6 hoặc 7 quân trên bàn cờ).
- Khi engine cần tìm ra nước đi duy nhất để thủ hòa hoặc dứt điểm chiến thắng tuyệt đối trong tàn cuộc phức tạp.
- Khi cấu hình đường dẫn `SyzygyPath` trong giao thức UCI kết nối tới thư mục chứa các tệp `.rtbw` và `.rtbz`.

## 3. When NOT to Use
- Khi bàn cờ còn nhiều quân (>7 quân) vượt quá phạm vi dữ liệu của các bộ Tablebase hiện có.
- Khi bộ nhớ lưu trữ ổ cứng không cho phép cài đặt các bộ tệp kích thước lớn (Syzygy 6-piece chiếm ~150GB, 7-piece chiếm ~17TB).

## 4. Prerequisites & Input Context
- **Dữ liệu cờ tàn:** Thư mục chứa các tệp Syzygy Tablebase 3-4-5 quân (`.rtbw` và `.rtbz`).
- **Thư viện tích hợp:** Thư viện C/C++ Fathom hoặc module tra cứu nhị phân tích hợp trong engine.

## 5. Core Concepts & Taxonomy
- **Syzygy WDL (.rtbw):** Bảng dữ liệu tra cứu nhanh kết quả thế cờ (Thắng, Hòa, Thua, Thắng nhưng bị chặn bởi luật 50 nước, Hòa do luật 50 nước), dùng chủ yếu trong quá trình duyệt cây tìm kiếm.
- **Syzygy DTZ (.rtbz):** Bảng dữ liệu xác định số nước đi chính xác cho đến khi có một quân tốt di chuyển hoặc một quân cờ bị bắt (zeroing move), dùng tại nút gốc để bảo đảm không bị xử hòa 50 nước.
- **50-Move Rule Compliance:** Nguy cơ thế cờ thắng về lý thuyết nhưng bị xử hòa thực tế do không thể ăn quân hoặc đi tốt trong vòng 50 nước đi liên tiếp.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo đường dẫn thư mục Tablebase thông qua tùy chọn UCI `setoption name SyzygyPath value /path/to/syzygy`.
2. Nạp các bảng băm nhận diện tệp Syzygy WDL (`.rtbw`) và DTZ (`.rtbz`) có sẵn trên ổ cứng.
3. Tại nút gốc (Root Node): nếu số lượng quân cờ <= giới hạn Tablebase, thực hiện `probe_root()` để chọn ngay nước cờ DTZ tối ưu.
4. Trong cây tìm kiếm (Search Tree): tại các nút có số lượng quân phù hợp, gọi `probe_wdl()`; nếu kết quả trả về là Thua, trả về giá trị fail-low; nếu Thắng, trả về giá trị fail-high để cắt tỉa toàn bộ cây con phía dưới.
5. Bọc các cuộc gọi I/O đọc tệp trong cơ chế phòng vệ ngoại lệ, tự động chuyển về hàm tìm kiếm thông thường nếu tệp bị lỗi hoặc không tìm thấy.
6. Chạy bộ kiểm thử 50 vị trí tàn cuộc kinh điển (KPK, KBNK, KQKR) để khẳng định tính chính xác tuyệt đối.

## 7. Concrete Examples
### Tich hop tra cuu Syzygy WDL trong ham tim kiem C++ bang Fathom library:
```cpp
#include "fathom/tbprobe.h"

// Khoi tao duong dan Syzygy khi nhan lenh UCI
void init_tablebases(const std::string& path) {
    tb_init(path.c_str());
    std::cout << "info string Syzygy Tablebases initialized. Max pieces: " << TB_LARGEST << std::endl;
}

int probe_tablebase_wdl(const Board& board, int depth, int alpha, int beta) {
    if (board.piece_count() > TB_LARGEST || board.has_castling_rights()) {
        return -1; // Khong the probe
    }

    // Tra cuu Fathom WDL: 0=Loss, 1=Blessed Loss, 2=Draw, 3=Cursed Win, 4=Win
    unsigned res = tb_probe_wdl(
        board.white_pieces(), board.black_pieces(),
        board.kings(), board.queens(), board.rooks(),
        board.bishops(), board.knights(), board.pawns(),
        board.halfmove_clock(), 0, board.ep_square(),
        board.turn() == WHITE
    );

    if (res == TB_RESULT_FAILED) return -1;

    int score = 0;
    if (res == TB_WIN) score = 20000;
    else if (res == TB_LOSS) score = -20000;
    else score = 0; // Draw, Blessed Loss, Cursed Win

    return score;
}
```

## 8. Anti-Patterns & Common Traps
- **Crashing on Missing Syzygy Files:** Cố tình truy cập mảng con mà không kiểm tra cờ tồn tại của tệp, khiến engine bị crash khi gặp vị trí 6 quân mà chỉ có bộ tệp 5 quân.
- **Ignoring 50-Move Counter in Tablebase:** Bỏ qua bộ đếm `halfmove_clock` khi đọc WDL khiến engine chọn phương án dẫn đến hòa cờ 50 nước trong thế cờ thắng.
- **Probing DTZ at Every Tree Node:** Gọi hàm DTZ đắt đỏ ở sâu trong cây tìm kiếm thay vì chỉ dùng WDL gọn nhẹ làm sụt giảm tốc độ duyệt nút nghiêm trọng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Nhận diện chính xác 100% kết quả WDL trên tất cả các vị trí tàn cuộc 3, 4, 5 quân có trong thư mục.
- **QG-02**: Không bao giờ gây ra hiện tượng sập engine (crash-safe) khi truy cập các vị trí chưa có tệp tablebase tương ứng.
- **QG-03**: Nước đi tại nút gốc luôn tuân thủ luật 50 nước (Zeroing move trước khi vượt quá 100 ply).

## 10. Security & Safety Boundaries
- Sử dụng cơ chế ánh xạ bộ nhớ tệp an toàn (Memory-mapped file / mmap) có giới hạn bảo vệ đọc (read-only) để tránh làm hỏng dữ liệu trên đĩa.

## 11. Platform Adapters
- **Runtimes**: C++20, Rust, Fathom Syzygy Prober, Stockfish syzygy module.

## 12. Deliverables & Output Artifacts
- Mô-đun tích hợp Tablebase (`syzygy_adapter.cpp` / `syzygy.rs`).
- Bộ kiểm thử tự động 50 bài toán tàn cuộc chuẩn (`test_endgame_tablebases.py`).

## 13. Related & Complementary Skills
dex-chess-search-pruning-evals, dex-chess-uci-protocol-compliance, dex-chess-engine-match-statistics

## 14. Realistic Usage Example
```bash
# Kiem tra tra cuu Syzygy trong vi tri KBNK bang lenh UCI
./chess_engine uci
setoption name SyzygyPath value /data/syzygy
position fen 8/8/8/8/8/5k2/4N3/4K2B w - - 0 1
go depth 1
```
