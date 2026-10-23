---
name: dex-chess-search-pruning-evals
description: Implement, evaluate, and tune alpha-beta search pruning heuristics in chess engines. Benchmark LMR, Null Move Pruning, Futility Pruning, and SEE while avoiding tactical regressions.
---

# dex-chess-search-pruning-evals

## 1. Purpose & Scope
Thiết kế, tinh chỉnh và kiểm chứng các thuật toán cắt tỉa nhánh tìm kiếm trong engine cờ vua (Search Pruning Heuristics); tối ưu hóa thuật toán Alpha-Beta / Principal Variation Search (PVS); tích hợp Null Move Pruning (NMP), Late Move Reductions (LMR), Reverse Futility Pruning (RFP) và Static Exchange Evaluation (SEE); đo lường chính xác tương quan giữa độ sâu tìm kiếm (Search Depth) và điểm số mù chiến thuật (Tactical Blindspots).

## 2. When to Use
- Khi engine cờ vua bị tụt độ sâu tìm kiếm so với đối thủ cùng thời gian (time control).
- Khi muốn cải thiện hệ số phân nhánh hữu hiệu (Effective Branching Factor - EBF) từ 5.0 xuống 2.0 hoặc thấp hơn.
- Khi cần tinh chỉnh các công thức giảm độ sâu nước đi muộn (LMR formula) dựa trên số lượng nước đi và độ sâu hiện tại.

## 3. When NOT to Use
- Khi bộ sinh nước đi hoặc hàm đánh giá tĩnh (Static Evaluation) chưa ổn định và còn tồn tại lỗi logic cơ bản.
- Khi giải bài toán cờ tàn giải quyết triệt để bằng bảng dữ liệu Endgame Tablebase (sử dụng `dex-chess-endgame-tablebase-integration`).

## 4. Prerequisites & Input Context
- **Bộ sinh nước đi:** Bộ sinh nước đi hợp lệ đã vượt qua kiểm thử perft.
- **Hàm đánh giá tĩnh:** Hàm đánh giá tĩnh cơ bản (HCE hoặc NNUE) trả về điểm số centipawn ổn định.

## 5. Core Concepts & Taxonomy
- **Null Move Pruning (NMP):** Kỹ thuật cho phép đối phương đi thêm một nước; nếu đối phương vẫn không thể tạo ra ưu thế vượt trội, vị trí hiện tại quá mạnh và có thể cắt tỉa nhánh ngay lập tức (tránh hiện tượng Zugzwang).
- **Late Move Reductions (LMR):** Giảm độ sâu tìm kiếm đối với các nước đi nằm ở cuối danh sách nước cờ đã được sắp xếp, vì xác suất một nước cờ muộn trở thành nước cờ tối ưu là rất thấp.
- **Static Exchange Evaluation (SEE):** Thuật toán mô phỏng chuỗi ăn quân tại một ô cờ duy nhất để xác định xem việc đổi quân có đem lại lợi thế vật chất hay không mà không cần tìm kiếm toàn diện.

## 6. Step-by-Step Execution Workflow
1. Thiết lập khung tìm kiếm chuẩn PVS (Principal Variation Search) với cửa sổ hẹp (Zero-Window Search).
2. Cài đặt Quiescence Search (tìm kiếm tĩnh) chỉ duyệt các nước ăn quân và phong cấp để tránh hiệu ứng chân trời (Horizon Effect).
3. Tích hợp Reverse Futility Pruning tại các nút tiền-lá (depth <= 2) nếu `eval - margin >= beta`.
4. Cài đặt Null Move Pruning có kiểm tra điều kiện không tồn tại Zugzwang (không áp dụng khi chỉ còn Tốt và Vua).
5. Thiết lập bảng giảm LMR dạng mảng 2 chiều tính trước `LMR_Table[depth][move_count]`.
6. Chạy bộ kiểm thử chiến thuật WAC (Win At Chess) và STS (Strategic Test Suite) để đo lường tỷ lệ giải bài tập.

## 7. Concrete Examples
### Cai dat thuat toan Alpha-Beta ket hop NMP va LMR bang C++:
```cpp
int search(int alpha, int beta, int depth, bool cut_node, Board& board) {
    if (depth <= 0) return quiescence_search(alpha, beta, board);
    
    int static_eval = evaluate(board);
    
    // 1. Reverse Futility Pruning (RFP)
    if (depth <= 2 && !board.is_in_check() && static_eval - 80 * depth >= beta) {
        return static_eval;
    }

    // 2. Null Move Pruning (NMP)
    if (depth >= 3 && !board.is_in_check() && board.has_non_pawn_material() && static_eval >= beta) {
        int R = 3 + depth / 6;
        board.make_null_move();
        int score = -search(-beta, -beta + 1, depth - 1 - R, !cut_node, board);
        board.unmake_null_move();
        if (score >= beta) return beta;
    }

    std::vector<Move> moves;
    generate_moves(board, moves);
    order_moves(moves, board);

    int moves_searched = 0;
    for (const auto& move : moves) {
        board.make_move(move);
        int score;
        
        // 3. Late Move Reductions (LMR)
        if (moves_searched >= 4 && depth >= 3 && !board.is_in_check() && !is_tactical(move)) {
            int reduction = lmr_table[depth][moves_searched];
            score = -search(-alpha - 1, -alpha, depth - 1 - reduction, true, board);
            if (score > alpha) {
                // Re-search voi do sau day du neu nuoc co bat ngo tot
                score = -search(-beta, -alpha, depth - 1, false, board);
            }
        } else {
            score = -search(-beta, -alpha, depth - 1, false, board);
        }
        
        board.unmake_move(move);
        moves_searched++;

        if (score >= beta) return beta; // Beta cutoff
        if (score > alpha) alpha = score;
    }
    return alpha;
}
```

## 8. Anti-Patterns & Common Traps
- **Blind Null Move in Zugzwang Endgames:** Cho phép Null Move Pruning ở tàn cuộc Vua Tốt dẫn đến việc engine bỏ qua các đòn zugzwang hiểm hóc và tự thua.
- **Over-reducing Tactical Checks:** Áp dụng LMR cho các nước đi chiếu Vua hoặc nước đi ăn lại quân khiến engine bị mù các đòn chiến thuật đơn giản.
- **Skipping Quiescence Search:** Dừng tìm kiếm ngay ở `depth = 0` mà không chạy Quiescence Search gây ra hiện tượng Horizon Effect nghiêm trọng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tỷ lệ giải đúng bài tập trong bộ WAC (Win At Chess - 300 vị trí) đạt tối thiểu 285/300 bài ở 1 giây/nút.
- **QG-02**: Tốc độ tìm kiếm sâu trung bình (Search Depth) tăng ít nhất 30% so với phiên bản Alpha-Beta không có pruning.
- **QG-03**: Không bị dính lỗi lặp lại nước đi vô tận hoặc tìm kiếm vượt quá thời gian phân bổ.

## 10. Security & Safety Boundaries
- Kiểm tra điều kiện ngắt tìm kiếm định kỳ (Time Check mỗi 2048 nút) để tránh treo vô tận khi nhận lệnh `stop` từ GUI.

## 11. Platform Adapters
- **Runtimes**: C++20, Rust, Cutechess CLI, OpenBench / FastGM test harness.

## 12. Deliverables & Output Artifacts
- Mô-đun tìm kiếm engine cờ vua (`search.cpp` / `search.rs`).
- Báo cáo kết quả giải các bài tập chiến thuật STS và WAC.

## 13. Related & Complementary Skills
dex-chess-legal-movegen-perft, dex-chess-transposition-table-correctness, dex-chess-engine-match-statistics

## 14. Realistic Usage Example
```bash
# Kiem thu engine tren bo bai tap chien thuat WAC bang script Python
python scripts/chess/bench_tactics.py --engine ./my_engine --epd test/wac.epd --movetime 1000
```
