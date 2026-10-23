---
name: dex-chess-opening-book-validation
description: Validate, inspect, and benchmark chess opening book formats (Polyglot .bin, CTG, PGN opening trees). Verify move legality, weight distributions, and transposition coverage.
---

# dex-chess-opening-book-validation

## 1. Purpose & Scope
Kiểm định, phân tích và đo lường chất lượng của sách khai cuộc cờ vua (Chess Opening Books); xác thực cấu trúc nhị phân của định dạng Polyglot (`.bin`), cây khai cuộc PGN và sách CTG; kiểm tra tính hợp lệ của các nước đi, phân phối trọng số nước cờ (Move Weighting & Randomization), và bảo đảm độ phủ các nhánh hoán vị khai cuộc chính tắc.

## 2. When to Use
- Khi tạo mới hoặc nhập khẩu sách khai cuộc Polyglot cho engine cờ vua thi đấu.
- Khi engine bị mắc bẫy khai cuộc đã biết hoặc chọn phải các biến yếu do trọng số trong sách bị gán nhãn sai.
- Khi cần xuất các ván đấu PGN lớn thành tệp nhị phân mở sách nhỏ gọn tối ưu hóa tốc độ nạp.

## 3. When NOT to Use
- Khi cấu hình engine thi đấu ở giải đấu không cho phép sử dụng sách khai cuộc (No-book conditions).
- Khi kiểm thử năng lực tự tìm kiếm thuần túy của thuật toán tìm kiếm và đánh giá.

## 4. Prerequisites & Input Context
- **Tệp sách nhị phân:** Tệp Polyglot `.bin` hoặc cơ sở dữ liệu PGN chứa các ván cờ kiện tướng (Master games).
- **Công cụ phân tích:** Python `chess.polyglot` hoặc công cụ dòng lệnh `polyglot` CLI.

## 5. Core Concepts & Taxonomy
- **Polyglot Zobrist Hash:** Chuẩn băm Zobrist 64-bit đặc thù của định dạng Polyglot (có bảng số ngẫu nhiên khác với Stockfish), bao gồm cả xử lý mốc bắt tốt qua đường chỉ khi có thể bắt thực tế.
- **Weight-Proportional Selection:** Thuật toán chọn nước đi ngẫu nhiên có trọng số: xác suất chọn một nước cờ tỷ lệ thuận với điểm trọng số `weight` của nó trong tệp `.bin`.
- **Book Transposition Coverage:** Khả năng nhận diện cùng một thế cờ khai cuộc đạt được thông qua các thứ tự đi quân khác nhau (ví dụ: transposition giữa Khai cuộc Anh và Gambit Hậu).

## 6. Step-by-Step Execution Workflow
1. Đọc và phân tích các bản ghi 16-byte trong tệp Polyglot `.bin`: `key` (8 byte), `move` (2 byte), `weight` (2 byte), `learn` (4 byte).
2. Kiểm tra tính sắp xếp tăng dần đơn điệu của các khóa `key` trong tệp nhị phân để hỗ trợ tìm kiếm nhị phân $O(\log N)$.
3. Giải mã mã nước đi 16-bit thành tọa độ ô cờ (from_square, to_square, promotion_piece).
4. Đối soát nước đi với bộ sinh nước đi chuẩn để khẳng định 100% nước đi trong sách đều hoàn toàn hợp lệ (Legal Move).
5. Kiểm tra tính đa dạng của các phương án: không để một nhánh khai cuộc chỉ có duy nhất 1 nước đi đơn điệu nếu thế cờ có nhiều biến hay.
6. Chạy kịch bản tra cứu thử nghiệm trên 1,000 thế cờ khai cuộc phổ biến và đo thời gian truy xuất.

## 7. Concrete Examples
### Script Python doc va kiem dinh tinh hop le cua sach Polyglot .bin:
```python
import chess
import chess.polyglot
import struct

def validate_polyglot_book(book_path):
    print(f"Auditing Polyglot Book: {book_path}")
    entry_size = 16
    total_entries = 0
    prev_key = 0

    with open(book_path, "rb") as f:
        while chunk := f.read(entry_size):
            key, move_int, weight, learn = struct.unpack(">QHHI", chunk)
            
            # 1. Kiem tra tinh sap xep tang dan de tim kiem nhi phan
            assert key >= prev_key, f"Unsorted key detected at entry {total_entries}: {key} < {prev_key}"
            prev_key = key
            
            # 2. Giai ma nuoc co: from(6), to(6), promo(3)
            to_sq = move_int & 0x3F
            from_sq = (move_int >> 6) & 0x3F
            promo = (move_int >> 12) & 0x7
            
            assert 0 <= from_sq <= 63 and 0 <= to_sq <= 63, f"Corrupted coordinates: {from_sq} -> {to_sq}"
            total_entries += 1

    print(f"Total Entries: {total_entries}. Binary sorting VERIFIED.")

    # 3. Kiem tra thu vien bang python-chess
    board = chess.Board()
    with chess.polyglot.open_reader(book_path) as reader:
        entries = list(reader.find_all(board))
        print(f"Startpos Book Moves: {len(entries)}")
        for e in entries:
            print(f"  - Move: {e.move} | Weight: {e.weight}")

validate_polyglot_book("performance.bin")
```

## 8. Anti-Patterns & Common Traps
- **Unsorted Binary Book Entries:** Lưu các bản ghi không theo thứ tự khóa tăng dần khiến thuật toán Binary Search không thể tìm thấy nước đi và coi như hết sách.
- **Including Blunder Moves:** Nhập các ván cờ nghiệp dư có nước đi sai lầm vào sách mà không lọc Elo khiến engine chọn phải nước cờ yếu.
- **Zero-Weight Default Traps:** Đặt trọng số bằng 0 cho tất cả các nước đi khiến thuật toán chọn ngẫu nhiên không thể kích hoạt.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các khóa trong tệp `.bin` được sắp xếp tăng dần nghiêm ngặt.
- **QG-02**: Mọi nước đi trong sách đều là nước cờ hợp lệ 100% theo luật cờ vua quốc tế FIDE.
- **QG-03**: Tốc độ tra cứu nhị phân đạt dưới 5 micro-giây cho một thế cờ.

## 10. Security & Safety Boundaries
- Kiểm tra kích thước tệp và giới hạn số lượng mục nhập trước khi cấp phát bộ nhớ đọc vào RAM.

## 11. Platform Adapters
- **Runtimes**: Python python-chess, C++ Polyglot Reader, Cutechess-cli.

## 12. Deliverables & Output Artifacts
- Kịch bản kiểm định và làm sạch sách khai cuộc (`validate_polyglot.py`).
- Báo cáo phân tích độ phủ và phân phối trọng số khai cuộc.

## 13. Related & Complementary Skills
dex-chess-legal-movegen-perft, dex-chess-uci-protocol-compliance, dex-chess-engine-match-statistics

## 14. Realistic Usage Example
```bash
# Trich xuat va kiem tra sach khai cuoc tu PGN bang cong cu polyglot
polyglot make-book -pgn games.pgn -bin output.bin -max-fl 20
```
