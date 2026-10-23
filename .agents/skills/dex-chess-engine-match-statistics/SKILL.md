---
name: dex-chess-engine-match-statistics
description: Design, orchestrate, and statistically evaluate chess engine matches. Calculate Elo ratings, confidence intervals, SPRT hypothesis tests, and prevent opening book or hardware bias.
---

# dex-chess-engine-match-statistics

## 1. Purpose & Scope
Thiết kế, điều phối và phân tích thống kê các giải đấu kiểm thử tự động giữa các engine cờ vua (Chess Engine Match Statistics); cài đặt thuật toán kiểm định tỉ số xác suất tuần tự (SPRT - Sequential Probability Ratio Test) để xác nhận các cải tiến mã nguồn; tính toán điểm xếp hạng Elo, khoảng tin cậy 95% (Confidence Intervals), hệ số hòa (Draw Rate) và triệt tiêu các sai lệch do sách khai cuộc hoặc tài nguyên phần cứng bất đối xứng.

## 2. When to Use
- Khi quyết định chấp thuận (merge) một cải tiến thuật toán tìm kiếm hoặc hàm đánh giá mới vào nhánh chính của engine.
- Khi cần chứng minh một thay đổi mã nguồn đem lại mức tăng ít nhất +5 Elo với mức ý nghĩa thống kê cao mà không cần đấu hàng chục nghìn ván không cần thiết.
- Khi đo lường sức mạnh thi đấu của engine so với các đối thủ trong danh sách xếp hạng tiêu chuẩn (CCRL, CEGT, Lichess).

## 3. When NOT to Use
- Khi kiểm tra tính đúng đắn chức năng (như test perft sinh nước đi hoặc bắt lỗi cú pháp FEN).
- Khi số lượng ván đấu quá nhỏ (<50 ván), kết quả hoàn toàn bị chi phối bởi yếu tố ngẫu nhiên và không có giá trị thống kê.

## 4. Prerequisites & Input Context
- **Hạ tầng thi đấu:** Cutechess-cli hoặc fastchess chạy trên máy chủ có CPU pinning cố định.
- **Công cụ thống kê:** Python `scipy`, `ordo`, hoặc thư viện `bayeselo`.

## 5. Core Concepts & Taxonomy
- **SPRT (Sequential Probability Ratio Test):** Phương pháp kiểm định giả thuyết của Abraham Wald cho phép dừng trận đấu ngay khi có đủ bằng chứng thống kê chứng minh giả thuyết $H_1$ (Elo gain >= bounds) hoặc $H_0$ (không tăng Elo).
- **BayesElo / Ordo:** Mô hình thống kê Bayes ước lượng trình độ Elo của nhiều đấu thủ từ kết quả ma trận đối đầu, xử lý tốt các ván hòa.
- **Opening Book Pairings:** Mỗi cặp khai cuộc được thi đấu 2 ván đảo màu quân (White/Black) giữa hai engine để triệt tiêu lợi thế cầm quân trắng.

## 6. Step-by-Step Execution Workflow
1. Chuẩn bị tập sách khai cuộc mở rộng gồm các vị trí cân bằng (ví dụ UHO_2022 8-move opening book).
2. Cấu hình kịch bản thi đấu `cutechess-cli` với kiểm soát thời gian chặt chẽ (ví dụ: 10s + 0.1s increment) và pinning CPU core.
3. Thiết lập thông số SPRT: `elo0 = 0.0`, `elo1 = 5.0`, `alpha = 0.05`, `beta = 0.05`.
4. Chạy các ván đấu theo từng cặp đảo màu quân (Gauntlet hoặc Round-Robin).
5. Cập nhật Log-Likelihood Ratio (LLR) sau mỗi ván đấu hoàn tất; dừng ngay trận đấu khi LLR chạm ngưỡng trên (Pass) hoặc ngưỡng dưới (Fail).
6. Xuất báo cáo thống kê: Điểm số, Thắng/Hòa/Thua, Elo chênh lệch, Lỗi sai số ±Error, và phân tích các ván thua để tìm bug chiến thuật.

## 7. Concrete Examples
### Kich ban thi dau tu dong SPRT giua ban thu nghiem va ban goc bang Cutechess-cli:
```bash
# Dieu phoi tran dau SPRT 2 engine voi cuon sach UHO, dao mau quan moi round
cutechess-cli \
  -engine cmd=./engine_dev name=DEX_Dev \
  -engine cmd=./engine_base name=DEX_Base \
  -each proto=uci tc=10+0.1 timemargin=50 hash=64 \
  -openings file=openings/uho_2024.epd format=epd order=random plies=16 \
  -repeat \
  -sprt elo0=0 elo1=5 alpha=0.05 beta=0.05 \
  -concurrency 4 \
  -draw movenumber=40 movecount=8 score=10 \
  -resign movecount=3 score=600 \
  -pgnout matches_output.pgn
```

### Script Python tinh toan diem Elo va khoang tin cay 95% tu ket qua W/D/L:
```python
import math

def calculate_elo_stats(wins, draws, losses):
    total = wins + draws + losses
    score = (wins + 0.5 * draws) / total
    
    # Uoc tinh Elo chenh lech
    elo_diff = -400 * math.log10(1 / score - 1)
    
    # Sai so chuan (Standard Error)
    variance = (wins * (1 - score)**2 + draws * (0.5 - score)**2 + losses * (0 - score)**2) / total
    se = math.sqrt(variance / total)
    
    # Khoang tin cay 95% (z = 1.96)
    elo_margin = 1.96 * (se * 400 / (score * (1 - score) * math.log(10)))
    
    print(f"Games: {total} (Wins: {wins}, Draws: {draws}, Losses: {losses})")
    print(f"Score: {score*100:.2f}% | Elo Diff: {elo_diff:+.2f} ± {elo_margin:.2f}")

calculate_elo_stats(320, 540, 240)
# Output: Games: 1100 (Wins: 320, Draws: 540, Losses: 240)
# Score: 53.64% | Elo Diff: +25.32 ± 16.84
```

## 8. Anti-Patterns & Common Traps
- **Ignoring Color Inversion:** Chỉ cho engine thử nghiệm cầm quân Trắng dẫn đến ảo giác tăng Elo do lợi thế đi trước tự nhiên của cờ vua.
- **Uncontrolled CPU Throttling:** Chạy giải đấu trên máy tính cá nhân đang chạy các tác vụ nặng khác khiến một bên bị rớt thời gian (Time forfeit) do nghẽn CPU.
- **Early Stop Bias:** Dừng trận đấu thủ công khi thấy kết quả tạm thời đang có lợi mà không tuân thủ các ngưỡng toán học của SPRT.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Mọi trận đấu đối kháng bắt buộc phải sử dụng chế độ thi đấu đảo màu quân theo cặp (Round-paired play).
- **QG-02**: Thử nghiệm SPRT chỉ được chấp thuận (Pass) khi LLR chạm ngưỡng trên với độ tin cậy thống kê >= 95%.
- **QG-03**: Tỷ lệ thua do hết thời gian (Time loss) của engine dưới 0.1% tổng số ván thi đấu.

## 10. Security & Safety Boundaries
- Giới hạn số lượng luồng và dung lượng RAM của các tiến trình engine thi đấu; cô lập môi trường sandbox không cho engine ghi đè file hệ thống.

## 11. Platform Adapters
- **Runtimes**: Cutechess-cli, fastchess, Ordo, BayesElo, Python scipy.

## 12. Deliverables & Output Artifacts
- Kịch bản điều phối giải đấu SPRT tự động (`run_sprt_match.sh`).
- Báo cáo phân tích thống kê Elo và tệp biên bản thi đấu PGN (`tournament_summary.md`).

## 13. Related & Complementary Skills
dex-chess-search-pruning-evals, dex-chess-uci-protocol-compliance, dex-chess-nnue-evaluation-integration

## 14. Realistic Usage Example
```bash
# Tinh toan bang xep hang Elo bang cong cu ordo
ordo -p matches_output.pgn -a 0 -A "DEX_Base" -W -D -c -j ordo_report.txt
```
