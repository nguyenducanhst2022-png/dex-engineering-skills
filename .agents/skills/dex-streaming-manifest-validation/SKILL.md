---
name: dex-streaming-manifest-validation
description: Validate, audit, and debug HLS (m3u8) and MPEG-DASH (mpd) streaming manifests. Verify segment sequencing, discontinuity tags, audio/video synchronization, and multi-codec adaptation sets.
---

# dex-streaming-manifest-validation

## 1. Purpose & Scope
Kiểm tra cú pháp và logic nghiệp vụ của các tệp kê khai phát trực tuyến HLS (`.m3u8`) và MPEG-DASH (`.mpd`); phát hiện các sai lệch về timestamp trình diễn (PTS/DTS), mất đồng bộ âm thanh/hình ảnh, nhảy vọt chuỗi phân đoạn (`EXT-X-MEDIA-SEQUENCE`), thiếu thẻ `EXT-X-DISCONTINUITY` khi chèn quảng cáo, và bảo đảm tính hợp lệ của các AdaptationSet.

## 2. When to Use
- Khi triển khai hoặc nâng cấp máy chủ đóng gói streaming (Shaka Packager, Bento4, NGINX RTMP/HLS).
- Khi người dùng phản hồi video bị dừng đứng (stall), mất tiếng hoặc lặp lại một phân đoạn khi chuyển đổi chất lượng mạng.
- Khi tích hợp cơ chế chèn quảng cáo động (SSAI/CSAI) vào luồng phát trực tiếp.

## 3. When NOT to Use
- Khi phát video qua giao thức progressive download tệp tĩnh MP4 thông thường.
- Khi kiểm thử logic giải mã DRM chuyên sâu tại tầng phần cứng Secure Media Path (sử dụng `dex-drm-compliant-playback-integration`).

## 4. Prerequisites & Input Context
- **Tệp manifest:** URL hoặc tệp cục bộ `.m3u8` hoặc `.mpd`.
- **Công cụ kiểm tra:** Python `m3u8`, `mpd-parser`, hoặc `mediastreamvalidator` của Apple.

## 5. Core Concepts & Taxonomy
- **EXT-X-DISCONTINUITY:** Thẻ báo hiệu sự thay đổi về định dạng tệp, cấu hình mã hóa, hoặc sự ngắt quãng trong trục thời gian (PTS), thường gặp khi chèn quảng cáo.
- **Media Presentation Timeline:** Trục thời gian tuyến tính trong DASH biểu diễn mối quan hệ giữa Period, AdaptationSet và Representation.
- **Segment Drift:** Hiện tượng độ dài thực tế của phân đoạn media bị trôi lệch so với thời lượng khai báo trong thuộc tính `#EXTINF`.

## 6. Step-by-Step Execution Workflow
1. Tải và phân tích cú pháp manifest phân cấp (Master Playlist và Media Playlist).
2. Kiểm tra tính liên tục của `EXT-X-MEDIA-SEQUENCE` giữa các lần refresh trong live stream.
3. Kiểm tra tính sẵn sàng của tất cả URI phân đoạn media (`.ts`, `.m4s`, `.mp4`).
4. Xác minh sự khớp nối về thời lượng giữa luồng âm thanh (audio rendition) và luồng hình ảnh (video stream).
5. Kiểm tra tính hợp lệ của các thông số CODECS trong thẻ `#EXT-X-STREAM-INF` (ví dụ `avc1.640028,mp4a.40.2`).
6. Xuất báo cáo cảnh báo nếu độ trôi lệch tích lũy (accumulated drift) vượt quá 100ms.

## 7. Concrete Examples
### Script Python kiểm thử tính hợp lệ của HLS Manifest và đồng bộ phân đoạn:
```python
import m3u8
import requests

def validate_hls_stream(master_url):
    res = requests.get(master_url, timeout=5)
    playlist = m3u8.loads(res.text)
    
    print(f"Master Playlist Valid: {playlist.is_variant}")
    for stream in playlist.playlists:
        sub_url = stream.uri if stream.uri.startswith('http') else master_url.rsplit('/', 1)[0] + '/' + stream.uri
        sub_pl = m3u8.loads(requests.get(sub_url).text)
        
        total_duration = sum(seg.duration for seg in sub_pl.segments)
        target_duration = sub_pl.target_duration
        print(f"Stream {stream.stream_info.resolution}: {len(sub_pl.segments)} segments, total={total_duration:.2f}s, target={target_duration}s")
        
        # Kiem tra khong phan doan nao vuot target_duration
        for seg in sub_pl.segments:
            assert seg.duration <= target_duration + 0.5, f"Segment exceeds target duration: {seg.uri} ({seg.duration}s > {target_duration}s)"

validate_hls_stream("https://streaming.example.com/live/master.m3u8")
```

## 8. Anti-Patterns & Common Traps
- **Missing Target Duration Ceiling:** Khai báo `#EXT-X-TARGETDURATION: 2` nhưng thực tế tạo phân đoạn 2.8s khiến trình phát iOS Safari từ chối phát luồng.
- **Unannounced Ad Discontinuities:** Nối luồng quảng cáo khác bitrate mà không chèn thẻ `EXT-X-DISCONTINUITY` gây sập bộ giải mã phần cứng trên TV.
- **Relative URI Resolution Failure:** Viết đường dẫn phân đoạn tương đối nhưng thiếu cấu hình base-path chuẩn khiến CDN trả lỗi HTTP 404.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Cú pháp manifest tuân thủ 100% RFC 8216 (HLS) hoặc ISO/IEC 23009-1 (DASH).
- **QG-02**: Không có phân đoạn nào trả về mã lỗi HTTP 4xx hoặc 5xx.
- **QG-03**: Sai lệch PTS/DTS giữa luồng audio và video không vượt quá 50ms.

## 10. Security & Safety Boundaries
- Chặn các đường dẫn phân đoạn chứa ký tự traversal (`../`) hoặc URL trỏ tới tài nguyên nội bộ trái phép (SSRF protection).

## 11. Platform Adapters
- **Runtimes**: Apple Mediastreamvalidator, HLS.js, Shaka Player, FFmpeg, Python m3u8 library.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm định manifest (`manifest_audit.json`).
- Danh sách cảnh báo sai lệch timestamp và độ trôi thời gian phân đoạn.

## 13. Related & Complementary Skills
dex-video-transcoding-ladders, dex-live-stream-latency-control, dex-streaming-qoe-telemetry

## 14. Realistic Usage Example
```bash
# Kiem thu HLS manifest bang cong cu mediastreamvalidator tren macOS/Linux
mediastreamvalidator https://cdn.example.com/hls/master.m3u8 --output report.plist
```
