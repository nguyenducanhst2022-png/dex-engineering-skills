---
name: dex-chess-transposition-table-correctness
description: Implement, verify, and tune Transposition Tables (TT) in chess engines. Ensure hash collision safety with Zobrist hashing, replacement strategies, lockless SMP probing, and bound semantics.
---

# dex-chess-transposition-table-correctness

## 1. Purpose & Scope
Thiết kế, kiểm chứng và tối ưu hóa bảng chuyển vị (Transposition Table - TT) trong engine cờ vua; bảo đảm an toàn trước va chạm hàm băm bằng Zobrist Hashing 64-bit; thiết lập chính sách thay thế ô nhớ (Replacement Schemes: Depth-preferred, Age-based, 2-tier bucket); xử lý đa luồng phi khóa (Lockless SMP TT Probing) an toàn trên CPU đa nhân và bảo đảm tính toàn vẹn của các cờ cận biên (EXACT, LOWERBOUND, UPPERBOUND).

## 2. When to Use
- Khi engine gặp hiện tượng lặp lại tính toán các thế cờ hoán vị (Transposition) qua các thứ tự nước đi khác nhau.
- Khi mở rộng engine chạy trên hệ thống đa luồng (SMP / Multithreading) sử dụng thuật toán Lazy SMP.
- Khi muốn lưu giữ nước đi tốt nhất (Best Move) để hỗ trợ sắp xếp nước đi (Move Ordering Heuristics) cho các lượt lặp sâu hơn.

## 3. When NOT to Use
- Khi bộ nhớ hệ thống bị giới hạn nghiêm trọng (<16MB RAM) không đủ để cấp phát bảng băm hiệu quả.
- Khi kiểm thử hàm perft đơn thuần (perft chỉ kiểm tra cây di chuyển, không dùng bảng TT trừ khi đo perft có TT).

## 4. Prerequisites & Input Context
- **Cơ chế băm:** Bảng số ngẫu nhiên Zobrist 64-bit đã được khởi tạo hoàn tất.
- **Bộ nhớ hệ thống:** Dung lượng RAM tối thiểu 64MB - 512MB để cấp phát bảng băm.

## 5. Core Concepts & Taxonomy
- **Zobrist Hashing:** Kỹ thuật băm bàn cờ bằng phép XOR các số ngẫu nhiên 64-bit được khởi tạo trước cho từng quân cờ tại từng ô cờ, lượt đi và quyền nhập thành.
- **Bound Semantics:** Cờ đánh dấu giá trị lưu trong TT: `EXACT` (giá trị thực tế trong khoảng alpha-beta), `LOWERBOUND` (giá trị fail-high >= beta), `UPPERBOUND` (giá trị fail-low <= alpha).
- **Lockless SMP (Shared TT with XOR Keys):** Kỹ thuật lưu trữ `key_xor_data = key ^ data` giúp các luồng đọc ghi đồng thời mà không cần mutex khóa, tự phát hiện dữ liệu rác nếu khóa không khớp.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo mảng số ngẫu nhiên Zobrist 64-bit cho 12 loại quân cờ x 64 ô, 16 trạng thái nhập thành, và 8 cột bắt tốt qua đường.
2. Thiết kế cấu trúc ô nhớ `TTEntry` nhỏ gọn (16 byte hoặc 8 byte) để tối ưu hóa bộ nhớ đệm CPU Cache Line (64 byte).
3. Cài đặt hàm `probe_tt()` trước khi bắt đầu duyệt cây tìm kiếm; cắt tỉa nhánh nếu độ sâu lưu trong TT đủ lớn và thỏa mãn cờ cận biên.
4. Cài đặt hàm `store_tt()` cập nhật ô nhớ sau khi tìm kiếm hoàn tất, áp dụng chiến lược ưu tiên độ sâu lớn hơn hoặc thời gian cũ hơn (aging).
5. Thiết lập cơ chế xóa và tăng chu kỳ tuổi (`age`) của bảng băm khi bắt đầu một ván cờ mới (`ucinewgame`).
6. Đo kiểm tỷ lệ đánh trúng bảng băm (TT Hit Rate) và khẳng định không có xung đột dữ liệu trên môi trường 8-16 luồng.

## 7. Concrete Examples
### Cau truc TTEntry 16-byte va thuat toan Lockless SMP trong C++20:
```cpp
#include <cstdint>
#include <atomic>

enum TT_Flag : uint8_t { NONE = 0, EXACT = 1, LOWER_BOUND = 2, UPPER_BOUND = 3 };

struct TTEntry {
    uint64_t key;       // 8 byte Zobrist key
    uint16_t move;      // 2 byte best move
    int16_t score;      // 2 byte evaluation
    uint8_t depth;      // 1 byte depth searched
    uint8_t flag;       // 1 byte bound flag
    uint8_t age;        // 1 byte entry age
    uint8_t padding;    // 1 byte pad to 16 bytes
};

class TranspositionTable {
private:
    std::vector<TTEntry> table;
    size_t num_entries;
    uint8_t current_age = 0;

public:
    void resize_mb(size_t mb) {
        num_entries = (mb * 1024 * 1024) / sizeof(TTEntry);
        table.assign(num_entries, TTEntry{});
    }

    bool probe(uint64_t key, int depth, int alpha, int beta, int& out_score, uint16_t& out_move) {
        TTEntry& entry = table[key % num_entries];
        if (entry.key == key) {
            out_move = entry.move;
            if (entry.depth >= depth) {
                if (entry.flag == EXACT) { out_score = entry.score; return true; }
                if (entry.flag == LOWER_BOUND && entry.score >= beta) { out_score = entry.score; return true; }
                if (entry.flag == UPPER_BOUND && entry.score <= alpha) { out_score = entry.score; return true; }
            }
        }
        return false;
    }

    void store(uint64_t key, uint16_t move, int score, int depth, TT_Flag flag) {
        TTEntry& entry = table[key % num_entries];
        // Chien luoc thay the: Ghi de neu do sau lon hon hoac la the co o chu ky cu
        if (entry.key == 0 || depth >= entry.depth || entry.age != current_age) {
            entry.key = key;
            entry.move = move;
            entry.score = score;
            entry.depth = static_cast<uint8_t>(depth);
            entry.flag = flag;
            entry.age = current_age;
        }
    }
    
    void new_search() { current_age++; }
};
```

## 8. Anti-Patterns & Common Traps
- **Unbounded Mate Score Storage:** Lưu trực tiếp điểm số chiếu hết (Checkmate Score) mà không điều chỉnh khoảng cách ply từ nút gốc, khiến engine nhầm lẫn khoảng cách chiếu hết khi lấy từ TT.
- **Entry Size Misalignment:** Cấu trúc Entry có kích thước lẻ (như 19 byte hoặc 23 byte) làm vỡ biên căn chỉnh cache line, gây suy giảm nghiêm trọng băng thông truy cập RAM.
- **Missing Age Mechanism:** Không làm mới chu kỳ tuổi khiến các thế cờ từ ván đấu trước hoặc từ lượt tìm kiếm sâu trước đó chiếm dụng vĩnh viễn các ô nhớ giá trị.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tỷ lệ va chạm sai lệch khóa băm (False Hash Collision) bằng 0 tuyệt đối trên 100 triệu lượt truy xuất.
- **QG-02**: Điểm số chiếu hết được điều chỉnh chính xác theo ply: `score += ply` khi lưu và `score -= ply` khi đọc.
- **QG-03**: Kích thước mỗi phần tử `sizeof(TTEntry)` là bội số của 8 byte và vừa vặn chia hết cho 64-byte Cache Line.

## 10. Security & Safety Boundaries
- Cấp phát bộ nhớ an toàn cho bảng băm; kiểm tra giới hạn kích thước tối đa (ví dụ tối đa 32GB) tránh làm cạn kiệt RAM hệ điều hành.

## 11. Platform Adapters
- **Runtimes**: C++20/C++23, Rust (std::sync::atomic), Stockfish TT benchmarks.

## 12. Deliverables & Output Artifacts
- Lớp triển khai bảng chuyển vị (`transposition_table.hpp` / `tt.rs`).
- Bộ kiểm thử tính đúng đắn của Bound Semantics và độ tuổi băm.

## 13. Related & Complementary Skills
dex-chess-search-pruning-evals, dex-chess-legal-movegen-perft, dex-chess-uci-protocol-compliance

## 14. Realistic Usage Example
```bash
# Kiem tra toc do truy xuat TT va hit rate bang che do benchmark
./chess_engine bench 16 1 14 default depth
```
