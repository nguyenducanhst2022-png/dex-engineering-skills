---
name: dex-chess-nnue-evaluation-integration
description: Integrate and optimize NNUE (Efficiently Updatable Neural Network) evaluation into chess engines. Validate SIMD accumulator updates, quantized int8 inference, and benchmark against classical HCE.
---

# dex-chess-nnue-evaluation-integration

## 1. Purpose & Scope
Tích hợp và tối ưu hóa mạng nơ-ron cập nhật hiệu quả (NNUE - Efficiently Updatable Neural Network) vào engine cờ vua; cài đặt bộ tích lũy cập nhật vi sai (Incremental Accumulator Updates) trên các tập lệnh SIMD (AVX2, AVX-512, ARM Neon); lượng tử hóa trọng số về dạng số nguyên 8-bit/16-bit (`int8_t` / `int16_t`) và đo kiểm sức mạnh thi đấu so với hàm đánh giá thủ công truyền thống (Handcrafted Evaluation - HCE).

## 2. When to Use
- Khi nâng cấp hàm đánh giá tĩnh của engine cờ vua từ các tham số tĩnh (Material + Piece-Square Tables) lên độ chính xác cấp cao của NNUE.
- Khi engine bị suy giảm tốc độ duyệt nút (NPS) do tính toán lại toàn bộ mạng từ đầu ở mỗi thế cờ thay vì cập nhật vi sai.
- Khi cần nạp và kiểm tra tính toàn vẹn của tệp trọng số nhị phân (`.nnue`) đi kèm engine.

## 3. When NOT to Use
- Khi biên dịch engine cho các vi điều khiển nhúng 8-bit/16-bit không có hỗ trợ số học vector SIMD.
- Khi nghiên cứu các thuật toán tìm kiếm thuần túy mà không muốn bị ảnh hưởng bởi độ phức tạp của mạng nơ-ron.

## 4. Prerequisites & Input Context
- **Tập lệnh phần cứng:** CPU hỗ trợ SIMD (x86 AVX2/AVX-512 hoặc ARM Neon).
- **Tệp trọng số:** Tệp mạng nơ-ron nhị phân `.nnue` tương thích kiến trúc HalfKP hoặc HalfKAv2.

## 5. Core Concepts & Taxonomy
- **HalfKP / HalfKAv2 Architecture:** Kiến trúc mạng nơ-ron cờ vua kinh điển ánh xạ vị trí Vua phe mình và các quân cờ khác trên bàn cờ vào một lớp đặc trưng thưa (Sparse Feature Transformer Layer).
- **Incremental Accumulator Update:** Khi một quân cờ di chuyển từ ô A đến ô B, chỉ cần trừ đi các trọng số của ô A và cộng thêm trọng số của ô B vào Accumulator của lớp ẩn đầu tiên thay vì tính lại 40,960 trọng số.
- **Clipped ReLU (CReLU):** Hàm kích hoạt được lượng tử hóa trong khoảng `[0, 127]` hoặc `[0, 255]`, dễ dàng tính toán siêu nhanh bằng lệnh bão hòa SIMD.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa cấu trúc file nhị phân NNUE: Magic Header, Version, Feature Transformer Weights, Output Layer Weights.
2. Cài đặt cấu trúc `Accumulator` lưu trữ 2 vector (trắng và đen) kích thước 512 hoặc 1024 số nguyên 16-bit.
3. Viết hàm cập nhật vi sai trong hàm `make_move()`: sao chép Accumulator của nút cha và thêm/bớt các đặc trưng di chuyển.
4. Cài đặt các hàm nhân ma trận và kích hoạt CReLU sử dụng nội tại hàm SIMD (`_mm256_add_epi16`, `_mm256_madd_epi16`).
5. Tính toán điểm đánh giá cuối cùng từ lớp đầu ra và nhân với hệ số tỉ lệ centipawn.
6. Kiểm tra chéo điểm số sinh ra từ đường cập nhật vi sai so với đường tính toán từ đầu (Refresh Accumulator) để khẳng định không bị trôi số học.

## 7. Concrete Examples
### Cap nhat vi sai Accumulator va tinh toan CReLU SIMD AVX2 trong C++:
```cpp
#include <immintrin.h>
#include <cstdint>

constexpr int TRANSFORMER_SIZE = 512;

struct Accumulator {
    alignas(64) int16_t white[TRANSFORMER_SIZE];
    alignas(64) int16_t black[TRANSFORMER_SIZE];
};

// Cap nhat vi sai: Tru tinh nang cu (sub_feature), Cong tinh nang moi (add_feature)
void update_accumulator(Accumulator& next, const Accumulator& prev, int add_idx, int sub_idx, const int16_t* weights) {
    const int16_t* add_w = &weights[add_idx * TRANSFORMER_SIZE];
    const int16_t* sub_w = &weights[sub_idx * TRANSFORMER_SIZE];

    for (int i = 0; i < TRANSFORMER_SIZE; i += 16) {
        __m256i p = _mm256_load_si256(reinterpret_cast<const __m256i*>(&prev.white[i]));
        __m256i a = _mm256_load_si256(reinterpret_cast<const __m256i*>(&add_w[i]));
        __m256i s = _mm256_load_si256(reinterpret_cast<const __m256i*>(&sub_w[i]));
        
        __m256i result = _mm256_sub_epi16(_mm256_add_epi16(p, a), s);
        _mm256_store_si256(reinterpret_cast<__m256i*>(&next.white[i]), result);
    }
}

// Tinh toan CReLU [0, 127] bang AVX2
inline __m256i crelu_avx2(__m256i val) {
    __m256i zero = _mm256_setzero_si256();
    __m256i max_val = _mm256_set1_epi16(127);
    return _mm256_min_epi16(_mm256_max_epi16(val, zero), max_val);
}
```

## 8. Anti-Patterns & Common Traps
- **Accumulator Drift Accumulation:** Dùng phép cộng trừ dấu chấm động (floating-point) khiến sai số tích lũy dần theo các ply; bắt buộc phải sử dụng số nguyên chuẩn (`int16_t`).
- **Full Forward Pass Every Node:** Tính toán lại toàn bộ lớp biến đổi đặc trưng từ đầu ở mọi nút tìm kiếm khiến tốc độ engine bị sụt giảm hơn 90%.
- **Unaligned Memory Access:** Không sử dụng thuộc tính căn chỉnh biên địa chỉ `alignas(64)` cho các mảng vector SIMD dẫn đến việc vi phạm chỉ thị `_mm256_load_si256` và gây sập chương trình (SIGSEGV).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Điểm số sinh ra từ cập nhật vi sai (Incremental) khớp 100% với điểm tính toán từ đầu (Full Refresh) trên 10,000 thế cờ ngẫu nhiên.
- **QG-02**: Tốc độ đánh giá đạt tối thiểu 2.5 triệu lượt đánh giá/giây trên một luồng CPU x86-64 hỗ trợ AVX2.
- **QG-03**: Tệp trọng số nhị phân có cơ chế kiểm tra mã băm SHA-256 trước khi nạp vào bộ nhớ.

## 10. Security & Safety Boundaries
- Xác thực kích thước và cấu trúc tệp mạng nơ-ron trước khi phân tích; từ chối các tệp `.nnue` bị hỏng hoặc cố tình tạo buffer overflow.

## 11. Platform Adapters
- **Runtimes**: C++20 AVX2/AVX-512/Neon, Rust, PyTorch (training exporter), Stockfish nnue-probe.

## 12. Deliverables & Output Artifacts
- Lớp đánh giá nơ-ron (`nnue_eval.cpp` / `nnue.rs`).
- Kịch bản kiểm thử tính đúng đắn vi sai của Accumulator (`test_accumulator_drift.py`).

## 13. Related & Complementary Skills
dex-chess-search-pruning-evals, dex-native-simd-dispatch, dex-chess-engine-match-statistics

## 14. Realistic Usage Example
```bash
# Nạp và kiểm định tệp mạng NNUE trong engine
./chess_engine uci
setoption name EvalFile value nn-123456789abc.nnue
isready
```
