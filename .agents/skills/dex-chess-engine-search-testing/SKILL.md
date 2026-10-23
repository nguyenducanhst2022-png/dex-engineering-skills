---
name: dex-chess-engine-search-testing
description: Design deterministic search verification suites for chess engines and tree search algorithms, verifying perft move generation correctness, alpha-beta pruning invariants, transposition table hits, and quiescence stability. Use when engineering game engines, minimax agents, or combinatorial search trees.
---

# dex-chess-engine-search-testing

## 1. Purpose & Scope
Thiết kế và xây dựng bộ kiểm thử xác minh thuật toán tìm kiếm cây trò chơi và động cơ cờ vua (Chess Engine Search Testing); kiểm chứng tính đúng đắn của hàm sinh nước đi bằng kiểm thử Perft (Performance Test), bảo toàn các bất biến của thuật toán tỉa cành Alpha-Beta (Alpha-Beta Pruning Invariants), tỷ lệ trúng bảng chuyển vị (Transposition Table Hits) và tính ổn định của tìm kiếm tĩnh (Quiescence Search).

## 2. When to Use
- Khi lập trình động cơ cờ vua, cờ vây hoặc các thuật toán tìm kiếm Minimax cho game đối kháng.
- Khi tối ưu hóa thuật toán tỉa cành Alpha-Beta và cần đảm bảo không cắt bỏ nhầm các nước đi tối ưu.
- Khi kiểm tra tính đúng đắn tuyệt đối của bộ sinh nước đi hợp lệ (Move Generator) tại các thế cờ đặc biệt (phong cấp, nhập thành, bắt tốt qua đường).

## 3. When NOT to Use
- Khi xây dựng các game casual 2D đơn giản không có logic tìm kiếm cây nước đi thông minh.
- Khi kiểm thử giao diện đồ họa bên ngoài của bàn cờ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Động cơ cờ viết bằng C++, Rust hoặc Go; bảng thế cờ tiêu chuẩn FEN; bộ dữ liệu chuẩn Perft (Perft Benchmark Suite).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Perft (Performance Test):** Thuật toán đếm tổng số lượng nút lá (Leaf Nodes) tại một độ sâu tìm kiếm nhất định để xác minh bộ sinh nước đi chuẩn xác 100%.
- **Alpha-Beta Invariant:** Đảm bảo điểm số tìm kiếm với cửa sổ hẹp $[\alpha, \beta]$ luôn đồng nhất với tìm kiếm toàn diện khi điểm số nằm trong khoảng cửa sổ.
- **Transposition Table Zobrist Hashing:** Sử dụng mã băm Zobrist 64-bit để lưu trữ và tái sử dụng kết quả đánh giá các thế cờ trùng lặp qua các nhánh đi khác nhau.

## 6. Step-by-Step Execution Workflow
1. Nạp các thế cờ FEN kinh điển (thế cờ ban đầu, thế cờ Kiwipete nhiều va chạm, thế cờ tàn cuộc phong cấp).
2. Chạy kiểm thử Perft đệ quy từ độ sâu 1 đến độ sâu 6, so sánh số lượng nước đi với bảng số liệu chuẩn quốc tế.
3. Kiểm tra tính nhất quán của bảng chuyển vị Transposition Table (tránh xung đột băm làm sai lệch nước đi).
4. Xác minh thuật toán Quiescence Search để giải quyết triệt tiêu hiệu ứng chân trời (Horizon Effect).
5. Xuất biên bản kiểm thử xác minh động cơ cờ `PERFT_VERIFICATION_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```rust
// Perft (Performance Test) Move Generation Verifier in Rust
pub fn perft(depth: u32, board: &mut Board) -> u64 {
    if depth == 0 {
        return 1;
    }

    let mut nodes: u64 = 0;
    let moves = board.generate_legal_moves();

    for m in moves {
        board.make_move(m);
        nodes += perft(depth - 1, board);
        board.undo_move(m);
    }

    nodes
}

// Verification assertion against standard Kiwipete position at depth 4
// Expected nodes: 4,085,603
#[test]
fn test_kiwipete_depth_4() {
    let mut board = Board::from_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1");
    assert_eq!(perft(4, &mut board), 4085603);
}
```

## 8. Anti-Patterns & Common Traps
- Bỏ qua kiểm thử Perft trên các thế cờ phức tạp, dẫn đến lỗi sót nước đi bắt tốt qua đường (En Passant) chỉ lộ ra sau hàng triệu ván đấu.
- Lưu điểm số vào bảng Transposition Table mà không lưu độ sâu tìm kiếm, khiến lượt tìm kiếm nông ghi đè lên kết quả tìm kiếm sâu.
- Thuật toán tỉa cành Null Move Pruning bị lỗi cắt tỉa trong tình huống Zugzwang (tình thế bắt buộc phải đi nước cờ xấu).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Vượt qua 100% các bài kiểm tra Perft chuẩn quốc tế từ độ sâu 1 đến độ sâu 5 với sai số bằng 0.
- QG-02: Tốc độ sinh nước đi và tìm kiếm đạt tối thiểu 2 triệu nút/giây trên một luồng CPU hiện đại.
- QG-03: Tỉ lệ trúng bảng chuyển vị Transposition Table duy trì trên 45% trong các lượt tìm kiếm trung cuộc.

## 10. Security & Safety Boundaries
- Xử lý an toàn chuỗi ký tự FEN đầu vào để ngăn chặn lỗi tràn bộ đệm hoặc tấn công từ chối dịch vụ thông qua chuỗi thế cờ độc hại.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bộ kịch bản kiểm thử Perft toàn diện `perft_suite.rs`.
1. Báo cáo hiệu năng và tính đúng đắn của thuật toán tìm kiếm cờ.

## 13. Related & Complementary Skills
- [`dex-simulation-determinism`](.agents/skills/dex-simulation-determinism/SKILL.md)
- [`dex-game-loop-timing`](.agents/skills/dex-game-loop-timing/SKILL.md)
- [`dex-performance-optimization`](.agents/skills/dex-performance-optimization/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát triển động cơ cờ vua tự viết bằng Rust. Động cơ thỉnh thoảng đi các nước cờ ngớ ngẩn khi gần hết giờ. Kỹ sư kích hoạt `dex-chess-engine-search-testing`, chạy bộ kiểm thử Perft trên thế cờ Kiwipete, phát hiện hàm sinh nước đi bị sót điều kiện khi vua bị chiếu đôi, sửa lỗi và đưa sức mạnh động cơ tăng thêm 150 điểm Elo.
