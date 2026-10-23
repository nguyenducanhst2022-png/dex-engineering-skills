---
name: dex-chess-legal-movegen-perft
description: Design, benchmark, and validate move generation engines for chess. Build comprehensive perft testing suites, verify magic bitboards, and eliminate subtle castling and en-passant bugs.
---

# dex-chess-legal-movegen-perft

## 1. Purpose & Scope
Thiết kế, kiểm thử và chứng minh tính đúng đắn tuyệt đối của bộ sinh nước đi cờ vua (Chess Move Generation Engine); xây dựng bộ kiểm thử perft (Performance Test) toàn diện từ các vị trí tiêu chuẩn đến các thế cờ biên phức tạp; kiểm chứng thuật toán Magic Bitboards cho quân Xe và Tượng, giải quyết triệt để các lỗi tinh vi về phong cấp, bắt tốt qua đường (En Passant), quyền nhập thành và thoát chiếu.

## 2. When to Use
- Khi phát triển hoặc tối ưu hóa engine cờ vua viết bằng C++, Rust, Zig, hoặc C#.
- Khi chuyển đổi từ bộ sinh nước đi pseudo-legal sang legal move generator hoặc tối ưu hóa cấu trúc dữ liệu Bitboard 64-bit.
- Khi phát hiện engine bị treo, tính toán số nút sai lệch so with cơ sở dữ liệu chuẩn Stockfish perft.

## 3. When NOT to Use
- Khi ứng dụng chỉ là bàn cờ hiển thị giao diện người dùng đơn giản (UI chessboard) đã có thư viện chuẩn như `chess.js` đảm nhiệm.
- Khi giải quyết các bài toán tìm kiếm nước đi AI mà chưa hoàn thiện tầng sinh nước đi cơ sở.

## 4. Prerequisites & Input Context
- **Kiến trúc dữ liệu:** Biểu diễn bàn cờ bằng Bitboard 64-bit (`uint64_t`), Magic Bitboards hoặc PEXT Bitboards.
- **Bộ dữ liệu chuẩn:** Tệp danh sách vị trí FEN kèm số nút perft chuẩn (Stockfish/Chess Programming Wiki perft test suites).

## 5. Core Concepts & Taxonomy
- **Perft (Performance Test):** Hàm duyệt cây đệ quy đếm tổng số lượng nút lá (leaf nodes) tại một độ sâu nhất định để xác minh bộ sinh nước đi không thừa và không thiếu bất kỳ nước cờ hợp lệ nào.
- **Magic Bitboards:** Kỹ thuật băm hoàn hảo sử dụng phép nhân số nguyên 64-bit và phép dịch bit để tra cứu bảng nước đi của quân trượt (Rook/Bishop) trong thời gian $O(1)$.
- **Make/Unmake vs Copy-Make:** Kỹ thuật áp dụng nước đi lên trạng thái bàn cờ hiện tại và phục hồi lại (Make/Unmake) so với sao chép toàn bộ struct bàn cờ (Copy-Make).

## 6. Step-by-Step Execution Workflow
1. Thiết lập biểu diễn bàn cờ 64 ô sử dụng kiểu dữ liệu số nguyên không dấu 64-bit (`U64 bitboards`).
2. Cài đặt bộ sinh nước đi pseudo-legal cho từng loại quân cờ (Tốt, Mã, Tượng, Xe, Hậu, Vua).
3. Lọc bỏ các nước đi không hợp lệ (nước đi khiến Vua phe mình bị chiếu) bằng hàm `is_in_check()`.
4. Xử lý các điều kiện đặc biệt: Quyền nhập thành bị mất khi Xe/Vua di chuyển hoặc các ô bị kiểm soát, mốc bắt tốt qua đường (ep square).
5. Viết hàm đệ quy `perft(depth)` và in chi tiết chia nhánh (perft divide) cho từng nước đi đầu tiên.
6. Chạy kiểm thử tự động trên bộ 10 vị trí FEN thử thách nổi tiếng (Kiwipete, Position 3, Position 4, Position 5).

## 7. Concrete Examples
### Ham duyet cay perft va divide kiem thu move generator bang C++20:
```cpp
#include <cstdint>
#include <iostream>
#include <vector>

using U64 = uint64_t;

struct Move {
    uint16_t data; // from(6), to(6), flags(4)
};

uint64_t perft(int depth, Board& board) {
    if (depth == 0) return 1ULL;

    std::vector<Move> move_list;
    generate_legal_moves(board, move_list);
    
    if (depth == 1) return move_list.size();

    uint64_t nodes = 0;
    for (const auto& move : move_list) {
        board.make_move(move);
        nodes += perft(depth - 1, board);
        board.unmake_move(move);
    }
    return nodes;
}

void perft_divide(int depth, Board& board) {
    std::vector<Move> move_list;
    generate_legal_moves(board, move_list);
    uint64_t total_nodes = 0;

    std::cout << "--- PERFT DIVIDE (Depth " << depth << ") ---\n";
    for (const auto& move : move_list) {
        board.make_move(move);
        uint64_t nodes = perft(depth - 1, board);
        board.unmake_move(move);
        std::cout << move_to_uci(move) << ": " << nodes << "\n";
        total_nodes += nodes;
    }
    std::cout << "Total Nodes: " << total_nodes << "\n";
}
```

## 8. Anti-Patterns & Common Traps
- **Allowing Castling Through Check:** Cho phép nhập thành khi ô trung gian giữa Vua và Xe đang bị quân đối phương tấn công (vi phạm luật cờ vua quốc tế).
- **En Passant Pin Disregard:** Quên kiểm tra việc bắt tốt qua đường có thể mở ra đường chiếu ngang của Xe đối phương lên Vua của mình.
- **Slow Board Copying:** Lạm dụng việc sao chép toàn bộ đối tượng Board lớn trên mỗi nút đệ quy khiến tốc độ perft bị giảm từ 50 triệu nút/giây xuống dưới 1 triệu nút/giây.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Vị trí xuất phát đạt chính xác `4,865,609` nút ở độ sâu `depth = 5` và `119,060,324` nút ở `depth = 6`.
- **QG-02**: Vị trí Kiwipete (`r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -`) đạt chính xác `4,085,603` nút ở độ sâu 4.
- **QG-03**: Tốc độ sinh nước đi đạt tối thiểu 25 triệu nút/giây (25 MNPS) trên một luồng CPU hiện đại.

## 10. Security & Safety Boundaries
- Ngăn ngừa lỗi tràn mảng danh sách nước đi (MoveList buffer overflow) bằng cách cấp phát kích thước tối đa 256 phần tử cho một vị trí cờ.

## 11. Platform Adapters
- **Runtimes**: C++20/C++23 (GCC, Clang, MSVC), Rust 2021, Cutechess-cli, Stockfish perft.

## 12. Deliverables & Output Artifacts
- Mô-đun sinh nước đi cờ vua chuẩn (`movegen.cpp` / `movegen.rs`).
- Bộ kiểm thử tự động Perft Suite 100 vị trí (`perft_suite_runner.py`).

## 13. Related & Complementary Skills
dex-chess-search-pruning-evals, dex-chess-transposition-table-correctness, dex-chess-uci-protocol-compliance

## 14. Realistic Usage Example
```bash
# Chay test perft divide cho vi tri Kiwipete do sau 4
./chess_engine perft "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -" 4
```
