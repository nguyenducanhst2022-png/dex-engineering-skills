---
name: dex-audio-loudness-normalization
description: Normalize, measure, and enforce professional audio loudness standards (ITU-R BS.1770-4, EBU R128, AES TD1004). Prevent true-peak clipping, balance dynamic range, and ensure consistent listening volume.
---

# dex-audio-loudness-normalization

## 1. Purpose & Scope
Đo lường, chuẩn hóa và xử lý tự động độ lớn âm thanh (Audio Loudness Normalization) theo các tiêu chuẩn quốc tế ITU-R BS.1770-4, EBU R128 (-23 LUFS cho phát thanh truyền hình) và AES TD1004 / streaming platforms (-14 LUFS cho Spotify, YouTube, Apple Music); ngăn chặn triệt để hiện tượng vỡ âm đỉnh thực (True-Peak Clipping), cân bằng dải động (Dynamic Range) và đảm bảo trải nghiệm nghe đồng nhất giữa các video khác nhau.

## 2. When to Use
- Khi xây dựng pipeline kiểm định âm thanh tự động cho nội dung do người dùng tải lên (UGC) hoặc podcast/vodcast.
- Khi người dùng phàn nàn âm lượng video quá nhỏ hoặc giật mình vì quảng cáo phát quá to so với nội dung chính.
- Khi xuất bản nội dung lên các nền tảng streaming có bộ lọc tự động hạ âm lượng nếu vượt ngưỡng True-Peak cho phép.

## 3. When NOT to Use
- Khi xử lý các luồng âm thanh viễn thông (VoIP 8kHz telephony) không yêu cầu tiêu chuẩn âm học chuyên nghiệp.
- Khi tín hiệu là âm thanh khoa học, telemetry siêu âm không phục vụ thính giác con người.

## 4. Prerequisites & Input Context
- **Công cụ âm thanh:** FFmpeg tích hợp bộ lọc `loudnorm`, hoặc Sox / libebur128.
- **Tệp âm thanh:** Tệp nguồn WAV, FLAC, hoặc AAC chất lượng gốc.

## 5. Core Concepts & Taxonomy
- **LUFS (Loudness Units relative to Full Scale):** Đơn vị đo độ lớn âm thanh tích hợp dựa trên thuật toán lọc trọng số K-weighting phản ánh thính giác người.
- **True Peak (dBTP):** Mức biên độ đỉnh thực tế của tín hiệu sau khi tái tạo qua bộ chuyển đổi số sang tương tự (DAC), tính cả các đỉnh giữa các mẫu (inter-sample peaks).
- **LRA (Loudness Range):** Thước đo độ biến thiên động của âm thanh giữa các đoạn thì thầm và đoạn bùng nổ trong toàn bộ tác phẩm.

## 6. Step-by-Step Execution Workflow
1. Thực hiện lượt quét phân tích đầu tiên (First Pass) bằng bộ lọc `ebur128` hoặc `loudnorm` để thu thập các chỉ số I, LRA, TP.
2. So sánh chỉ số tích hợp thu được với mục tiêu phát hành: Target I = -14 LUFS, Max True Peak = -1.0 dBTP, Target LRA = 7 LU.
3. Nếu mức chênh lệch lớn hơn 0.5 LUFS, thực hiện lượt xử lý thứ hai (Second Pass) với các tham số tuyến tính đã tính toán từ lượt 1.
4. Áp dụng bộ giới hạn đỉnh (True Peak Limiter) để triệt tiêu mọi đỉnh vượt quá -1.0 dBTP mà không tạo ra hiện tượng méo tiếng hài (harmonic distortion).
5. Xuất tệp âm thanh đã chuẩn hóa và xác nhận lại bằng bài test kiểm định độc lập.

## 7. Concrete Examples
### Kịch bản FFmpeg 2-Pass chuẩn hóa âm thanh đạt chuẩn Streaming (-14 LUFS):
```bash
# Pass 1: Do dac thong so am thanh thuc te
ffmpeg -i input_video.mp4 -af loudnorm=I=-14:TP=-1.0:LRA=7:print_format=json -f null - 2> loudness_stats.json

# Trich xuat cac gia tri: input_i, input_tp, input_lra, input_thresh tu JSON va truyen vao Pass 2
INPUT_I=$(grep "input_i" loudness_stats.json | awk -F'"' '{print $4}')
INPUT_TP=$(grep "input_tp" loudness_stats.json | awk -F'"' '{print $4}')
INPUT_LRA=$(grep "input_lra" loudness_stats.json | awk -F'"' '{print $4}')
INPUT_THRESH=$(grep "input_thresh" loudness_stats.json | awk -F'"' '{print $4}')

# Pass 2: Ap dung bo loc tuyen tinh 2-pass khong lam bien dang dải dong
ffmpeg -y -i input_video.mp4 -c:v copy \
  -af loudnorm=I=-14:TP=-1.0:LRA=7:measured_I=${INPUT_I}:measured_TP=${INPUT_TP}:measured_LRA=${INPUT_LRA}:measured_thresh=${INPUT_THRESH}:linear=true \
  -c:a aac -b:a 192k normalized_output.mp4
```

## 8. Anti-Patterns & Common Traps
- **Simple Peak Normalization:** Chỉ khuếch đại đỉnh cao nhất lên 0dB khiến đoạn hội thoại thông thường vẫn quá nhỏ trong khi tiếng súng/nổ làm chói tai.
- **Single Pass Loudnorm with Dynamic Mode:** Dùng loudnorm 1 lượt mà không truyền tham số đo lường thực tế khiến âm lượng bị phập phồng (pumping artifact).
- **Ignoring Inter-Sample Peaks:** Để True Peak đạt 0.0 dBFS khiến tín hiệu bị clipping nặng nề khi phát qua loa tai nghe Bluetooth hoặc soundbar gia đình.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Âm lượng tích hợp (Integrated Loudness) đạt chính xác mục tiêu (-14.0 LUFS ± 0.5 LUFS cho web streaming).
- **QG-02**: Mức True Peak tối đa không bao giờ vượt quá -1.0 dBTP.
- **QG-03**: Không xuất hiện hiện tượng méo tiếng (THD+N < 0.1%) sau khi chuẩn hóa.

## 10. Security & Safety Boundaries
- Giữ nguyên quyền sở hữu bản quyền audio metadata; không nhúng watermark lạ vào luồng dữ liệu thô.

## 11. Platform Adapters
- **Runtimes**: FFmpeg libebur128, Audacity CLI, iZotope RX, Python pyloudnorm.

## 12. Deliverables & Output Artifacts
- Kịch bản chuẩn hóa âm thanh 2-pass tự động (`normalize_audio.sh`).
- Báo cáo phân tích âm học JSON trước và sau chuẩn hóa.

## 13. Related & Complementary Skills
dex-video-transcoding-ladders, dex-media-content-ingest-moderation

## 14. Realistic Usage Example
```bash
# Kiem tra do lon am thanh bang script Python pyloudnorm
python -c "import soundfile as sf, pyloudnorm as pyln; data, rate = sf.read('audio.wav'); meter = pyln.Meter(rate); print(f'Integrated Loudness: {meter.integrated_loudness(data):.2f} LUFS')"
```
