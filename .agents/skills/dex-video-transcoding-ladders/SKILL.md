---
name: dex-video-transcoding-ladders
description: Design, benchmark, and validate adaptive video transcoding ladders across H.264, HEVC, and AV1. Optimize bitrate-resolution trade-offs using VMAF and PSNR thresholds while ensuring multi-device playback compatibility.
---

# dex-video-transcoding-ladders

## 1. Purpose & Scope
Thiết kế, đo kiểm và tối ưu hóa bậc thang mã hóa video đa độ phân giải (Adaptive Bitrate Transcoding Ladders) cho các định dạng H.264/AVC, H.265/HEVC và AV1; tính toán điểm cân bằng giữa chất lượng thị giác (VMAF >= 93, PSNR >= 42dB) và băng thông truyền tải mạng; bảo đảm tính tương thích phần cứng với các thiết bị di động, Smart TV và trình duyệt web.

## 2. When to Use
- Khi xây dựng hoặc cấu hình pipeline mã hóa video VOD (Video-on-Demand) hoặc Live Streaming quy mô lớn.
- Khi tối ưu hóa chi phí CDN và băng thông phát video cho người dùng mạng yếu hoặc dữ liệu di động 4G/5G.
- Khi thiết lập tiêu chuẩn kiểm định chất lượng video tự động (VMAF scoring) trước khi đóng gói HLS/DASH.

## 3. When NOT to Use
- Khi ứng dụng chỉ xử lý hình ảnh tĩnh hoặc âm thanh đơn thuần không chứa luồng video.
- Khi hệ thống truyền phát thời gian thực sử dụng WebRTC P2P không thông qua máy chủ transcoding đa tầng.

## 4. Prerequisites & Input Context
- **Công cụ mã hóa:** FFmpeg 6.0+ tích hợp libx264, libx265, libsvtav1 và libvmaf.
- **Dữ liệu đầu vào:** Tệp video gốc chất lượng cao (ProRes, DNxHD hoặc raw mezzanine video).

## 5. Core Concepts & Taxonomy
- **Convex Hull Optimization:** Phương pháp dựng đường cong Pareto giữa bitrate và VMAF để chọn đúng độ phân giải tối ưu cho từng mức bitrate mà không lãng phí tài nguyên.
- **GOP (Group of Pictures) Alignment:** Đồng bộ hóa kích thước khung hình GOP (thường là 2 giây hoặc 48-60 khung hình) trên tất cả các biến thể bitrate để chuyển đổi tầng thích ứng mượt mà.
- **VMAF (Video Multi-Method Assessment Fusion):** Thước đo cảm nhận thị giác do Netflix phát triển, kết hợp các mô hình SVM để đánh giá chất lượng video gần nhất với mắt người.

## 6. Step-by-Step Execution Workflow
1. Khảo sát tệp video gốc (độ phân giải gốc, tốc độ khung hình, dải màu dynamic range) bằng `ffprobe`.
2. Phân tích độ phức tạp không gian và thời gian (Spatial/Temporal Information) của nội dung (thể thao chuyển động nhanh vs bài giảng tĩnh).
3. Lựa chọn ma trận độ phân giải và bitrate mục tiêu: 1080p (4500k), 720p (2400k), 540p (1200k), 360p (600k).
4. Chạy kịch bản mã hóa đa luồng với GOP đồng bộ (Closed GOP, `keyint=48:min-keyint=48:no-scenecut`).
5. Tính toán chỉ số VMAF tham chiếu chéo giữa luồng mã hóa và tệp mezzanine gốc.
6. Kiểm định tính tương thích của tệp đầu ra (h.264 level, profile high/main, pixel format yuv420p).

## 7. Concrete Examples
### Kịch bản FFmpeg mã hóa thang bitrate tối ưu 3 tầng với GOP cố định:
```bash
# Ma hoa da tang song song voi Closed GOP 2s (48 frames o 24fps)
ffmpeg -y -i raw_mezzanine.mov \
  -filter_complex "[0:v]split=3[v1],[v2],[v3]; \
    [v1]scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v1out]; \
    [v2]scale=w=1280:h=720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2[v2out]; \
    [v3]scale=w=854:h=480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2[v3out]" \
  -map "[v1out]" -c:v:0 libx264 -b:v:0 4500k -maxrate:v:0 4800k -bufsize:v:0 9000k -x264-params "keyint=48:min-keyint=48:no-scenecut=1" \
  -map "[v2out]" -c:v:1 libx264 -b:v:1 2400k -maxrate:v:1 2600k -bufsize:v:1 4800k -x264-params "keyint=48:min-keyint=48:no-scenecut=1" \
  -map "[v3out]" -c:v:2 libx264 -b:v:2 1200k -maxrate:v:2 1300k -bufsize:v:2 2400k -x264-params "keyint=48:min-keyint=48:no-scenecut=1" \
  -preset slow -profile:v high -pix_fmt yuv420p \
  -f hls -hls_time 2 -hls_playlist_type vod -master_pl_name master.m3u8 \
  -var_stream_map "v:0 v:1 v:2" output_%v/manifest.m3u8
```

## 8. Anti-Patterns & Common Traps
- **Mismatched Keyframe Intervals:** Không cố định keyframe giữa các tầng phân giải khiến trình phát bị giật hình hoặc vỡ khung khi chuyển bitrate mạng.
- **Overbitrate on Static Scenes:** Đặt bitrate cố định (CBR) quá cao cho các cảnh tĩnh gây lãng phí dung lượng CDN và tiền lưu trữ.
- **Ignoring Mobile Color Spaces:** Xuất video ở định dạng 10-bit HDR (yuv420p10le) cho tầng fallback 360p khiến các điện thoại Android đời cũ không thể giải mã phần cứng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Điểm VMAF của tầng 1080p đạt tối thiểu 93.0 điểm so với video gốc.
- **QG-02**: Khoảng cách keyframe (GOP) đồng nhất 100% trên tất cả các luồng phân giải.
- **QG-03**: Định dạng pixel format bắt buộc là `yuv420p` cho profile phổ thông tương thích trình duyệt.

## 10. Security & Safety Boundaries
- Phân lập môi trường transcoding trong container hạn chế quyền; ngăn ngừa lỗ hổng buffer overflow từ các parser codec bên thứ ba.

## 11. Platform Adapters
- **Runtimes**: FFmpeg, AWS Elemental MediaConvert, Bitmovin, HandBrake CLI, Shaka Packager.

## 12. Deliverables & Output Artifacts
- Ma trận cấu hình thang bitrate transcoding (`transcoding_ladder.json`).
- Báo cáo kiểm định điểm VMAF và PSNR tự động (`vmaf_report.csv`).
- Bộ tệp manifest HLS/DASH sẵn sàng phân phối.

## 13. Related & Complementary Skills
dex-streaming-manifest-validation, dex-streaming-qoe-telemetry, dex-media-content-ingest-moderation

## 14. Realistic Usage Example
```bash
# Do diem VMAF giua ban encode va mezzanine goc
ffmpeg -i output_1080p.mp4 -i raw_mezzanine.mov -filter_complex libvmaf="model_path=vmaf_v0.6.1.json:log_fmt=json:log_path=vmaf.json" -f null -
cat vmaf.json | jq '.pooled_metrics.vmaf.mean'
```
