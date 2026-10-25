# -*- coding: utf-8 -*-
"""
DEX ENGINEERING SKILLS FRAMEWORK v9.0 — GENERATOR
Builds Group AQ (Skills 421–430: Streaming & Digital Media Systems)
and Group AR (Skills 431–440: Advanced Chess Engine & Native Performance).
All skills strictly implement the 14 mandatory sections standard.
"""

import os
import sys

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

SKILLS_AQ_AR = [
    # =========================================================================
    # GROUP AQ: Streaming & Digital Media Systems (Skills 421–430)
    # =========================================================================
    {
        "id": "dex-video-transcoding-ladders",
        "name": "dex-video-transcoding-ladders",
        "desc": "Design, benchmark, and validate adaptive video transcoding ladders across H.264, HEVC, and AV1. Optimize bitrate-resolution trade-offs using VMAF and PSNR thresholds while ensuring multi-device playback compatibility.",
        "purpose": "Thiết kế, đo kiểm và tối ưu hóa bậc thang mã hóa video đa độ phân giải (Adaptive Bitrate Transcoding Ladders) cho các định dạng H.264/AVC, H.265/HEVC và AV1; tính toán điểm cân bằng giữa chất lượng thị giác (VMAF >= 93, PSNR >= 42dB) và băng thông truyền tải mạng; bảo đảm tính tương thích phần cứng với các thiết bị di động, Smart TV và trình duyệt web.",
        "when_use": "- Khi xây dựng hoặc cấu hình pipeline mã hóa video VOD (Video-on-Demand) hoặc Live Streaming quy mô lớn.\n- Khi tối ưu hóa chi phí CDN và băng thông phát video cho người dùng mạng yếu hoặc dữ liệu di động 4G/5G.\n- Khi thiết lập tiêu chuẩn kiểm định chất lượng video tự động (VMAF scoring) trước khi đóng gói HLS/DASH.",
        "when_not_use": "- Khi ứng dụng chỉ xử lý hình ảnh tĩnh hoặc âm thanh đơn thuần không chứa luồng video.\n- Khi hệ thống truyền phát thời gian thực sử dụng WebRTC P2P không thông qua máy chủ transcoding đa tầng.",
        "prereqs": "- **Công cụ mã hóa:** FFmpeg 6.0+ tích hợp libx264, libx265, libsvtav1 và libvmaf.\n- **Dữ liệu đầu vào:** Tệp video gốc chất lượng cao (ProRes, DNxHD hoặc raw mezzanine video).",
        "concepts": "- **Convex Hull Optimization:** Phương pháp dựng đường cong Pareto giữa bitrate và VMAF để chọn đúng độ phân giải tối ưu cho từng mức bitrate mà không lãng phí tài nguyên.\n- **GOP (Group of Pictures) Alignment:** Đồng bộ hóa kích thước khung hình GOP (thường là 2 giây hoặc 48-60 khung hình) trên tất cả các biến thể bitrate để chuyển đổi tầng thích ứng mượt mà.\n- **VMAF (Video Multi-Method Assessment Fusion):** Thước đo cảm nhận thị giác do Netflix phát triển, kết hợp các mô hình SVM để đánh giá chất lượng video gần nhất với mắt người.",
        "workflow": "1. Khảo sát tệp video gốc (độ phân giải gốc, tốc độ khung hình, dải màu dynamic range) bằng `ffprobe`.\n2. Phân tích độ phức tạp không gian và thời gian (Spatial/Temporal Information) của nội dung (thể thao chuyển động nhanh vs bài giảng tĩnh).\n3. Lựa chọn ma trận độ phân giải và bitrate mục tiêu: 1080p (4500k), 720p (2400k), 540p (1200k), 360p (600k).\n4. Chạy kịch bản mã hóa đa luồng với GOP đồng bộ (Closed GOP, `keyint=48:min-keyint=48:no-scenecut`).\n5. Tính toán chỉ số VMAF tham chiếu chéo giữa luồng mã hóa và tệp mezzanine gốc.\n6. Kiểm định tính tương thích của tệp đầu ra (h.264 level, profile high/main, pixel format yuv420p).",
        "examples": """### Kịch bản FFmpeg mã hóa thang bitrate tối ưu 3 tầng với GOP cố định:
```bash
# Ma hoa da tang song song voi Closed GOP 2s (48 frames o 24fps)
ffmpeg -y -i raw_mezzanine.mov \\
  -filter_complex "[0:v]split=3[v1],[v2],[v3]; \\
    [v1]scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v1out]; \\
    [v2]scale=w=1280:h=720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2[v2out]; \\
    [v3]scale=w=854:h=480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2[v3out]" \\
  -map "[v1out]" -c:v:0 libx264 -b:v:0 4500k -maxrate:v:0 4800k -bufsize:v:0 9000k -x264-params "keyint=48:min-keyint=48:no-scenecut=1" \\
  -map "[v2out]" -c:v:1 libx264 -b:v:1 2400k -maxrate:v:1 2600k -bufsize:v:1 4800k -x264-params "keyint=48:min-keyint=48:no-scenecut=1" \\
  -map "[v3out]" -c:v:2 libx264 -b:v:2 1200k -maxrate:v:2 1300k -bufsize:v:2 2400k -x264-params "keyint=48:min-keyint=48:no-scenecut=1" \\
  -preset slow -profile:v high -pix_fmt yuv420p \\
  -f hls -hls_time 2 -hls_playlist_type vod -master_pl_name master.m3u8 \\
  -var_stream_map "v:0 v:1 v:2" output_%v/manifest.m3u8
```""",
        "antipatterns": "- **Mismatched Keyframe Intervals:** Không cố định keyframe giữa các tầng phân giải khiến trình phát bị giật hình hoặc vỡ khung khi chuyển bitrate mạng.\n- **Overbitrate on Static Scenes:** Đặt bitrate cố định (CBR) quá cao cho các cảnh tĩnh gây lãng phí dung lượng CDN và tiền lưu trữ.\n- **Ignoring Mobile Color Spaces:** Xuất video ở định dạng 10-bit HDR (yuv420p10le) cho tầng fallback 360p khiến các điện thoại Android đời cũ không thể giải mã phần cứng.",
        "gates": "- **QG-01**: Điểm VMAF của tầng 1080p đạt tối thiểu 93.0 điểm so với video gốc.\n- **QG-02**: Khoảng cách keyframe (GOP) đồng nhất 100% trên tất cả các luồng phân giải.\n- **QG-03**: Định dạng pixel format bắt buộc là `yuv420p` cho profile phổ thông tương thích trình duyệt.",
        "security": "- Phân lập môi trường transcoding trong container hạn chế quyền; ngăn ngừa lỗ hổng buffer overflow từ các parser codec bên thứ ba.",
        "adapters": "- **Runtimes**: FFmpeg, AWS Elemental MediaConvert, Bitmovin, HandBrake CLI, Shaka Packager.",
        "deliverables": "- Ma trận cấu hình thang bitrate transcoding (`transcoding_ladder.json`).\n- Báo cáo kiểm định điểm VMAF và PSNR tự động (`vmaf_report.csv`).\n- Bộ tệp manifest HLS/DASH sẵn sàng phân phối.",
        "related": "dex-streaming-manifest-validation, dex-streaming-qoe-telemetry, dex-media-content-ingest-moderation",
        "usage": "```bash\n# Do diem VMAF giua ban encode va mezzanine goc\nffmpeg -i output_1080p.mp4 -i raw_mezzanine.mov -filter_complex libvmaf=\"model_path=vmaf_v0.6.1.json:log_fmt=json:log_path=vmaf.json\" -f null -\ncat vmaf.json | jq '.pooled_metrics.vmaf.mean'\n```"
    },
    {
        "id": "dex-streaming-manifest-validation",
        "name": "dex-streaming-manifest-validation",
        "desc": "Validate, audit, and debug HLS (m3u8) and MPEG-DASH (mpd) streaming manifests. Verify segment sequencing, discontinuity tags, audio/video synchronization, and multi-codec adaptation sets.",
        "purpose": "Kiểm tra cú pháp và logic nghiệp vụ của các tệp kê khai phát trực tuyến HLS (`.m3u8`) và MPEG-DASH (`.mpd`); phát hiện các sai lệch về timestamp trình diễn (PTS/DTS), mất đồng bộ âm thanh/hình ảnh, nhảy vọt chuỗi phân đoạn (`EXT-X-MEDIA-SEQUENCE`), thiếu thẻ `EXT-X-DISCONTINUITY` khi chèn quảng cáo, và bảo đảm tính hợp lệ của các AdaptationSet.",
        "when_use": "- Khi triển khai hoặc nâng cấp máy chủ đóng gói streaming (Shaka Packager, Bento4, NGINX RTMP/HLS).\n- Khi người dùng phản hồi video bị dừng đứng (stall), mất tiếng hoặc lặp lại một phân đoạn khi chuyển đổi chất lượng mạng.\n- Khi tích hợp cơ chế chèn quảng cáo động (SSAI/CSAI) vào luồng phát trực tiếp.",
        "when_not_use": "- Khi phát video qua giao thức progressive download tệp tĩnh MP4 thông thường.\n- Khi kiểm thử logic giải mã DRM chuyên sâu tại tầng phần cứng Secure Media Path (sử dụng `dex-drm-compliant-playback-integration`).",
        "prereqs": "- **Tệp manifest:** URL hoặc tệp cục bộ `.m3u8` hoặc `.mpd`.\n- **Công cụ kiểm tra:** Python `m3u8`, `mpd-parser`, hoặc `mediastreamvalidator` của Apple.",
        "concepts": "- **EXT-X-DISCONTINUITY:** Thẻ báo hiệu sự thay đổi về định dạng tệp, cấu hình mã hóa, hoặc sự ngắt quãng trong trục thời gian (PTS), thường gặp khi chèn quảng cáo.\n- **Media Presentation Timeline:** Trục thời gian tuyến tính trong DASH biểu diễn mối quan hệ giữa Period, AdaptationSet và Representation.\n- **Segment Drift:** Hiện tượng độ dài thực tế của phân đoạn media bị trôi lệch so với thời lượng khai báo trong thuộc tính `#EXTINF`.",
        "workflow": "1. Tải và phân tích cú pháp manifest phân cấp (Master Playlist và Media Playlist).\n2. Kiểm tra tính liên tục của `EXT-X-MEDIA-SEQUENCE` giữa các lần refresh trong live stream.\n3. Kiểm tra tính sẵn sàng của tất cả URI phân đoạn media (`.ts`, `.m4s`, `.mp4`).\n4. Xác minh sự khớp nối về thời lượng giữa luồng âm thanh (audio rendition) và luồng hình ảnh (video stream).\n5. Kiểm tra tính hợp lệ của các thông số CODECS trong thẻ `#EXT-X-STREAM-INF` (ví dụ `avc1.640028,mp4a.40.2`).\n6. Xuất báo cáo cảnh báo nếu độ trôi lệch tích lũy (accumulated drift) vượt quá 100ms.",
        "examples": """### Script Python kiểm thử tính hợp lệ của HLS Manifest và đồng bộ phân đoạn:
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
```""",
        "antipatterns": "- **Missing Target Duration Ceiling:** Khai báo `#EXT-X-TARGETDURATION: 2` nhưng thực tế tạo phân đoạn 2.8s khiến trình phát iOS Safari từ chối phát luồng.\n- **Unannounced Ad Discontinuities:** Nối luồng quảng cáo khác bitrate mà không chèn thẻ `EXT-X-DISCONTINUITY` gây sập bộ giải mã phần cứng trên TV.\n- **Relative URI Resolution Failure:** Viết đường dẫn phân đoạn tương đối nhưng thiếu cấu hình base-path chuẩn khiến CDN trả lỗi HTTP 404.",
        "gates": "- **QG-01**: Cú pháp manifest tuân thủ 100% RFC 8216 (HLS) hoặc ISO/IEC 23009-1 (DASH).\n- **QG-02**: Không có phân đoạn nào trả về mã lỗi HTTP 4xx hoặc 5xx.\n- **QG-03**: Sai lệch PTS/DTS giữa luồng audio và video không vượt quá 50ms.",
        "security": "- Chặn các đường dẫn phân đoạn chứa ký tự traversal (`../`) hoặc URL trỏ tới tài nguyên nội bộ trái phép (SSRF protection).",
        "adapters": "- **Runtimes**: Apple Mediastreamvalidator, HLS.js, Shaka Player, FFmpeg, Python m3u8 library.",
        "deliverables": "- Báo cáo kiểm định manifest (`manifest_audit.json`).\n- Danh sách cảnh báo sai lệch timestamp và độ trôi thời gian phân đoạn.",
        "related": "dex-video-transcoding-ladders, dex-live-stream-latency-control, dex-streaming-qoe-telemetry",
        "usage": "```bash\n# Kiem thu HLS manifest bang cong cu mediastreamvalidator tren macOS/Linux\nmediastreamvalidator https://cdn.example.com/hls/master.m3u8 --output report.plist\n```"
    },
    {
        "id": "dex-drm-compliant-playback-integration",
        "name": "dex-drm-compliant-playback-integration",
        "desc": "Integrate and verify authorized multi-DRM playback architectures (Widevine, FairPlay, PlayReady) via Encrypted Media Extensions (EME). Audit license server exchanges, key rotation, and secure hardware pipelines.",
        "purpose": "Tích hợp và kiểm chứng kiến trúc bảo vệ bản quyền số đa nền tảng (Multi-DRM: Google Widevine, Apple FairPlay Streaming, Microsoft PlayReady); xác thực quy trình cấp phép bản quyền qua Encrypted Media Extensions (EME), kiểm tra khả năng phục hồi lỗi của License Server, mã hóa Common Encryption (CENC - cenc/cbcs) và cơ chế xoay vòng khóa (Key Rotation) an toàn.",
        "when_use": "- Khi phát hành nội dung video cao cấp (phim điện ảnh, giải đấu thể thao có bản quyền) yêu cầu bảo vệ chuẩn Hollywood (Studio-grade DRM).\n- Khi cấu hình trình phát web (Shaka Player, Video.js, Dash.js) hoặc ứng dụng mobile/TV tương tác với hệ thống Key Management Server (KMS).\n- Khi chẩn đoán lỗi giải mã DRM (ví dụ lỗi EME `MEDIA_ERR_ENCRYPTED`, HDCP mismatch, hoặc chứng chỉ FairPlay hết hạn).",
        "when_not_use": "- Khi video là nội dung công khai, open-source hoặc chỉ cần bảo vệ cơ bản bằng chữ ký số URL (Signed URLs/Token Authentication).\n- Khi mục tiêu là bẻ khóa hoặc vượt qua các biện pháp bảo vệ bản quyền (nghiêm cấm tuyệt đối theo chính sách bảo mật DEX).",
        "prereqs": "- **Hạ tầng DRM:** Endpoint License Acquisition Server hợp lệ, Application Secret Key (FairPlay ASK), hoặc Widevine Provider Credentials.\n- **Trình phát thử nghiệm:** Trình duyệt hỗ trợ EME (Chrome Widevine, Safari FairPlay, Edge PlayReady).",
        "concepts": "- **Common Encryption (CENC):** Chuẩn ISO/IEC 23001-7 cho phép mã hóa nội dung một lần nhưng giải mã được bằng nhiều hệ thống DRM khác nhau.\n- **Encrypted Media Extensions (EME):** API W3C cho phép ứng dụng web giao tiếp với Content Decryption Module (CDM) chạy trong môi trường bảo vệ của OS.\n- **Security Levels (Widevine L1 vs L3):** L1 xử lý giải mã và hiển thị hoàn toàn trong Trusted Execution Environment (TEE) của phần cứng; L3 chỉ giải mã bằng phần mềm.",
        "workflow": "1. Kiểm tra sự sẵn sàng của CDM trên thiết bị mục tiêu bằng API `navigator.requestMediaKeySystemAccess()`.\n2. Cấu hình xử lý sự kiện `encrypted` từ thẻ `<video>` để trích xuất `initData` (PSSH box).\n3. Tạo phiên giải mã `MediaKeySession` và sinh chuỗi yêu cầu giấy phép (License Request Challenge).\n4. Gửi Challenge tới License Server kèm JWT Token chứng thực quyền sở hữu của người dùng.\n5. Nhận phản hồi License từ máy chủ và cập nhật vào CDM thông qua `session.update()`.\n6. Lắng nghe các lỗi EME và thiết lập cơ chế retry có giới hạn với backoff nếu mạng gặp sự cố tạm thời.",
        "examples": """### Tích hợp Shaka Player với cấu hình Multi-DRM (Widevine & FairPlay):
```javascript
const player = new shaka.Player(document.getElementById('video'));

player.configure({
  drm: {
    servers: {
      'com.widevine.alpha': 'https://license.example.com/v1/widevine',
      'com.apple.fps': 'https://license.example.com/v1/fairplay'
    },
    advanced: {
      'com.apple.fps': {
        serverCertificateUri: 'https://license.example.com/certs/fairplay.cer'
      }
    }
  }
});

player.getNetworkingEngine().registerRequestFilter((type, request) => {
  if (type === shaka.net.NetworkingEngine.RequestType.LICENSE) {
    request.headers['Authorization'] = 'Bearer ' + getUserAuthToken();
  }
});

player.load('https://cdn.example.com/cenc_stream/manifest.mpd')
  .then(() => console.log('DRM playback initialized successfully.'))
  .catch((err) => console.error('DRM Error Code:', err.code, err.data));
```""",
        "antipatterns": "- **Hardcoding DRM Credentials in Client Bundles:** Lưu khóa giải mã hoặc client secret trực tiếp trong mã nguồn frontend.\n- **Missing HDCP Error Handling:** Không bắt lỗi khi người dùng kết nối màn hình ngoài không hỗ trợ HDCP 2.2, dẫn đến việc video bị đen màn hình mà không có thông báo cho người dùng.\n- **Ignoring CDM Certificate Expiry:** Quên gia hạn chứng chỉ FairPlay Application Certificate khiến hàng loạt người dùng thiết bị Apple không thể mở video.",
        "gates": "- **QG-01**: Xác thực thành công handshake EME và nhận license hợp lệ trên cả 3 hệ thống Widevine, FairPlay và PlayReady.\n- **QG-02**: Mọi yêu cầu cấp phép bản quyền đều mang token xác thực danh tính người dùng có thời hạn sống ngắn (short-lived JWT).\n- **QG-03**: Hệ thống có cơ chế hạ cấp chất lượng mượt mà (fallback HDCP/L3) thay vì gây sập trình duyệt.",
        "security": "- Tuân thủ tuyệt đối quy định bảo vệ bản quyền số; không lưu trữ khóa giải mã dưới dạng plaintext trên bất kỳ bộ nhớ đệm ứng dụng nào.",
        "adapters": "- **Runtimes**: Shaka Player, Video.js Contrib-EME, Apple AVPlayer, ExoPlayer (Android), DASH-IF Player.",
        "deliverables": "- Module cấu hình trình phát Multi-DRM (`drm_player_config.js`).\n- Bộ kịch bản kiểm thử EME handshake tự động (`test_eme_handshake.js`).",
        "related": "dex-streaming-manifest-validation, dex-streaming-qoe-telemetry, dex-media-content-ingest-moderation",
        "usage": "```bash\n# Kiem tra phan hoi cua License Server bang curl co chu ky JWT\ncurl -X POST https://license.example.com/v1/widevine \\\n  -H \"Authorization: Bearer $DRM_TOKEN\" \\\n  -H \"Content-Type: application/octet-stream\" \\\n  --data-binary @challenge.bin --output license.bin\n```"
    },
    {
        "id": "dex-live-stream-latency-control",
        "name": "dex-live-stream-latency-control",
        "desc": "Analyze, tune, and measure ultra-low and low-latency live streaming architectures (LL-HLS, LL-DASH, WebRTC/WHIP). Balance buffer drift, catch-up playback rates, and network stability.",
        "purpose": "Tối ưu hóa và kiểm soát độ trễ trong các hệ thống truyền phát trực tiếp (Live Streaming Latency Control); cấu hình chuẩn truyền tải phân đoạn nhỏ (LL-HLS Partial Segments và LL-DASH Chunked Transfer); thiết lập thuật toán bám đuổi độ trễ (Catch-up playback rate adjustment) giúp thu hẹp khoảng cách thời gian giữa nguồn phát và người xem xuống dưới 2-3 giây mà không làm giật bộ đệm.",
        "when_use": "- Khi phát sóng các sự kiện thể thao trực tiếp, đấu giá online, cá cược thể thao điện tử (Esports) hoặc phòng họp tương tác.\n- Khi chuyển đổi kiến trúc từ HLS truyền thống (độ trễ 15–30s) sang Low-Latency HLS (độ trễ 2–4s).\n- Khi cần tinh chỉnh thuật toán đồng bộ buffer và tốc độ phát bù (playback speed catching up) trên client.",
        "when_not_use": "- Khi hệ thống chỉ phân phối video VOD ghi hình sẵn không có yếu tố tương tác thời gian thực.\n- Khi mạng truyền dẫn của khách hàng là vệ tinh có RTT tự nhiên cao (>1000ms) không thể áp dụng low-latency.",
        "prereqs": "- **Hạ tầng đóng gói:** Máy chủ đóng gói hỗ trợ HTTP/2 Push và Chunked Transfer Encoding (CMAF).\n- **Trình phát hỗ trợ:** HLS.js 1.0+ hoặc Shaka Player hỗ trợ chế độ Low Latency.",
        "concepts": "- **CMAF Partial Segments:** Chia phân đoạn 2 giây thành các mảnh con 200–500ms giúp trình phát bắt đầu giải mã ngay khi mảnh đầu tiên được nạp qua mạng.\n- **Catch-up Rate (1.05x - 1.1x):** Tăng nhẹ tốc độ phát khi trình phát bị tụt lại phía sau live edge và tự động hạ về 1.0x khi đã vào vùng mục tiêu an toàn.\n- **Live Edge Distance:** Khoảng cách thời gian từ khung hình đang hiển thị tới thời điểm máy quay ghi hình thực tế.",
        "workflow": "1. Khảo sát hạ tầng mạng và đo đạc RTT trung bình giữa CDN edge và client.\n2. Cấu hình máy chủ media đóng gói CMAF chunked chunks (độ dài partial segment 333ms, full segment 2s).\n3. Bật hỗ trợ HTTP/2 hoặc HTTP/3 trên máy chủ CDN để phục vụ các yêu cầu tải partial song song hiệu quả.\n4. Cấu hình tham số trình phát: `targetLatency: 2.5s`, `maxLatency: 4.0s`, `minPlaybackRate: 0.95`, `maxPlaybackRate: 1.1`.\n5. Thực hiện đo đạc độ trễ đầu cuối (Glass-to-Glass Latency) bằng đồng hồ tham chiếu độ chính xác mili-giây.\n6. Theo dõi tỷ lệ rebuffering khi người dùng mạng chập chờn để điều chỉnh ngưỡng rơi về fallback buffer.",
        "examples": """### Cấu hình thuật toán Low-Latency Catch-up trong HLS.js:
```javascript
const hls = new Hls({
  lowLatencyMode: true,
  backBufferLength: 30,
  liveSyncDurationCount: 3,
  liveMaxLatencyDurationCount: 6,
  liveDurationInfinity: true,
  highBufferWatchdogPeriod: 2,
  // Thuat toan tang toc nhe nhang de bam sat diem phat live
  enableWorker: true
});

hls.on(Hls.Events.MANIFEST_PARSED, () => {
  video.play();
});

// Quan sat do tre thuc te so voi Live Edge
setInterval(() => {
  if (hls.liveSyncPosition) {
    const latency = hls.liveSyncPosition - video.currentTime;
    console.log(`Current Live Latency: ${latency.toFixed(2)}s`);
    if (latency > 4.0) {
      video.playbackRate = 1.08; // Bat che do duoi kip
    } else if (latency < 2.2) {
      video.playbackRate = 1.0;  // Ve toc do binh thuong
    }
  }
}, 1000);
```""",
        "antipatterns": "- **Aggressive Catch-up Rate (>1.2x):** Tăng tốc độ phát quá mức làm méo tiếng (pitch shifting) gây khó chịu nghiêm trọng cho người nghe.\n- **Deploying LL-HLS over HTTP/1.1:** Không bật HTTP/2 khiến trình duyệt bị cạn kiệt kết nối mạng TCP socket khi liên tục kéo các partial segment nhỏ.\n- **Zero Buffer Target:** Cố ép độ trễ xuống dưới 1s trên mạng công cộng khiến trình phát lập tức bị xoay vòng đệm ngay khi mạng suy giảm nhẹ.",
        "gates": "- **QG-01**: Độ trễ trung bình End-to-End ổn định trong khoảng 2.0s – 3.5s trên mạng cáp quang/4G ổn định.\n- **QG-02**: Tỷ lệ Rebuffer Ratio dưới 0.5% trong suốt phiên phát sóng 30 phút.\n- **QG-03**: Tốc độ phát bù (catch-up playback) không bao giờ vượt quá 1.1x và giữ nguyên cao độ âm thanh (pitch preservation).",
        "security": "- Bảo vệ endpoint ingest (SRT/RTMP/WHIP) bằng cơ chế stream key luân phiên và kiểm soát dải IP được phép truyền phát.",
        "adapters": "- **Runtimes**: HLS.js, Shaka Player, NGINX RTMP, SRS (Simple Realtime Server), Wowza Streaming Engine.",
        "deliverables": "- Kịch bản tinh chỉnh tham số trình phát LL-HLS (`latency_tuner.js`).\n- Biểu đồ theo dõi phân bố độ trễ Glass-to-Glass (`latency_telemetry.png`).",
        "related": "dex-streaming-manifest-validation, dex-streaming-qoe-telemetry, dex-video-transcoding-ladders",
        "usage": "```bash\n# Do do tre tu may chu ingest den CDN edge bang script do timestamp\npython -m scripts.media.measure_glass_latency --stream-url \"https://live.example.com/llhls/index.m3u8\"\n```"
    },
    {
        "id": "dex-audio-loudness-normalization",
        "name": "dex-audio-loudness-normalization",
        "desc": "Normalize, measure, and enforce professional audio loudness standards (ITU-R BS.1770-4, EBU R128, AES TD1004). Prevent true-peak clipping, balance dynamic range, and ensure consistent listening volume.",
        "purpose": "Đo lường, chuẩn hóa và xử lý tự động độ lớn âm thanh (Audio Loudness Normalization) theo các tiêu chuẩn quốc tế ITU-R BS.1770-4, EBU R128 (-23 LUFS cho phát thanh truyền hình) và AES TD1004 / streaming platforms (-14 LUFS cho Spotify, YouTube, Apple Music); ngăn chặn triệt để hiện tượng vỡ âm đỉnh thực (True-Peak Clipping), cân bằng dải động (Dynamic Range) và đảm bảo trải nghiệm nghe đồng nhất giữa các video khác nhau.",
        "when_use": "- Khi xây dựng pipeline kiểm định âm thanh tự động cho nội dung do người dùng tải lên (UGC) hoặc podcast/vodcast.\n- Khi người dùng phàn nàn âm lượng video quá nhỏ hoặc giật mình vì quảng cáo phát quá to so với nội dung chính.\n- Khi xuất bản nội dung lên các nền tảng streaming có bộ lọc tự động hạ âm lượng nếu vượt ngưỡng True-Peak cho phép.",
        "when_not_use": "- Khi xử lý các luồng âm thanh viễn thông (VoIP 8kHz telephony) không yêu cầu tiêu chuẩn âm học chuyên nghiệp.\n- Khi tín hiệu là âm thanh khoa học, telemetry siêu âm không phục vụ thính giác con người.",
        "prereqs": "- **Công cụ âm thanh:** FFmpeg tích hợp bộ lọc `loudnorm`, hoặc Sox / libebur128.\n- **Tệp âm thanh:** Tệp nguồn WAV, FLAC, hoặc AAC chất lượng gốc.",
        "concepts": "- **LUFS (Loudness Units relative to Full Scale):** Đơn vị đo độ lớn âm thanh tích hợp dựa trên thuật toán lọc trọng số K-weighting phản ánh thính giác người.\n- **True Peak (dBTP):** Mức biên độ đỉnh thực tế của tín hiệu sau khi tái tạo qua bộ chuyển đổi số sang tương tự (DAC), tính cả các đỉnh giữa các mẫu (inter-sample peaks).\n- **LRA (Loudness Range):** Thước đo độ biến thiên động của âm thanh giữa các đoạn thì thầm và đoạn bùng nổ trong toàn bộ tác phẩm.",
        "workflow": "1. Thực hiện lượt quét phân tích đầu tiên (First Pass) bằng bộ lọc `ebur128` hoặc `loudnorm` để thu thập các chỉ số I, LRA, TP.\n2. So sánh chỉ số tích hợp thu được với mục tiêu phát hành: Target I = -14 LUFS, Max True Peak = -1.0 dBTP, Target LRA = 7 LU.\n3. Nếu mức chênh lệch lớn hơn 0.5 LUFS, thực hiện lượt xử lý thứ hai (Second Pass) với các tham số tuyến tính đã tính toán từ lượt 1.\n4. Áp dụng bộ giới hạn đỉnh (True Peak Limiter) để triệt tiêu mọi đỉnh vượt quá -1.0 dBTP mà không tạo ra hiện tượng méo tiếng hài (harmonic distortion).\n5. Xuất tệp âm thanh đã chuẩn hóa và xác nhận lại bằng bài test kiểm định độc lập.",
        "examples": """### Kịch bản FFmpeg 2-Pass chuẩn hóa âm thanh đạt chuẩn Streaming (-14 LUFS):
```bash
# Pass 1: Do dac thong so am thanh thuc te
ffmpeg -i input_video.mp4 -af loudnorm=I=-14:TP=-1.0:LRA=7:print_format=json -f null - 2> loudness_stats.json

# Trich xuat cac gia tri: input_i, input_tp, input_lra, input_thresh tu JSON va truyen vao Pass 2
INPUT_I=$(grep "input_i" loudness_stats.json | awk -F'"' '{print $4}')
INPUT_TP=$(grep "input_tp" loudness_stats.json | awk -F'"' '{print $4}')
INPUT_LRA=$(grep "input_lra" loudness_stats.json | awk -F'"' '{print $4}')
INPUT_THRESH=$(grep "input_thresh" loudness_stats.json | awk -F'"' '{print $4}')

# Pass 2: Ap dung bo loc tuyen tinh 2-pass khong lam bien dang dải dong
ffmpeg -y -i input_video.mp4 -c:v copy \\
  -af loudnorm=I=-14:TP=-1.0:LRA=7:measured_I=${INPUT_I}:measured_TP=${INPUT_TP}:measured_LRA=${INPUT_LRA}:measured_thresh=${INPUT_THRESH}:linear=true \\
  -c:a aac -b:a 192k normalized_output.mp4
```""",
        "antipatterns": "- **Simple Peak Normalization:** Chỉ khuếch đại đỉnh cao nhất lên 0dB khiến đoạn hội thoại thông thường vẫn quá nhỏ trong khi tiếng súng/nổ làm chói tai.\n- **Single Pass Loudnorm with Dynamic Mode:** Dùng loudnorm 1 lượt mà không truyền tham số đo lường thực tế khiến âm lượng bị phập phồng (pumping artifact).\n- **Ignoring Inter-Sample Peaks:** Để True Peak đạt 0.0 dBFS khiến tín hiệu bị clipping nặng nề khi phát qua loa tai nghe Bluetooth hoặc soundbar gia đình.",
        "gates": "- **QG-01**: Âm lượng tích hợp (Integrated Loudness) đạt chính xác mục tiêu (-14.0 LUFS ± 0.5 LUFS cho web streaming).\n- **QG-02**: Mức True Peak tối đa không bao giờ vượt quá -1.0 dBTP.\n- **QG-03**: Không xuất hiện hiện tượng méo tiếng (THD+N < 0.1%) sau khi chuẩn hóa.",
        "security": "- Giữ nguyên quyền sở hữu bản quyền audio metadata; không nhúng watermark lạ vào luồng dữ liệu thô.",
        "adapters": "- **Runtimes**: FFmpeg libebur128, Audacity CLI, iZotope RX, Python pyloudnorm.",
        "deliverables": "- Kịch bản chuẩn hóa âm thanh 2-pass tự động (`normalize_audio.sh`).\n- Báo cáo phân tích âm học JSON trước và sau chuẩn hóa.",
        "related": "dex-video-transcoding-ladders, dex-media-content-ingest-moderation",
        "usage": "```bash\n# Kiem tra do lon am thanh bang script Python pyloudnorm\npython -c \"import soundfile as sf, pyloudnorm as pyln; data, rate = sf.read('audio.wav'); meter = pyln.Meter(rate); print(f'Integrated Loudness: {meter.integrated_loudness(data):.2f} LUFS')\"\n```"
    },
    {
        "id": "dex-media-caption-timedtext",
        "name": "dex-media-caption-timedtext",
        "desc": "Process, convert, validate, and synchronize timed-text caption formats (WebVTT, TTML, SRT). Detect cue collision overlaps, enforce WCAG accessibility standards, and support multi-language tracks.",
        "purpose": "Xử lý, chuyển đổi, xác thực cú pháp và đồng bộ hóa các định dạng phụ đề và văn bản theo thời gian (Timed Text: WebVTT, TTML, SubRip SRT); phát hiện và tự động sửa các lỗi va chạm mốc thời gian (overlapping cues), bảo đảm tuân thủ tiêu chuẩn tiếp cận tiếp cận người khuyết tật (WCAG 2.1 AA / FCC closed captioning rules), và quản lý đa ngôn ngữ trong luồng phát trực tuyến HLS/DASH.",
        "when_use": "- Khi nhập kho và phân phối phụ đề đa ngôn ngữ cho phim, khóa học trực tuyến hoặc chương trình truyền hình.\n- Khi chuyển đổi kho phụ đề định dạng cũ (.srt, .scc) sang chuẩn web hiện đại (.vtt) tương thích HTML5 `<track>`.\n- Khi phụ đề hiển thị sai lệch mốc thời gian (lệch khẩu hình) hoặc 2 câu thoại đè chồng lên nhau trên màn hình.",
        "when_not_use": "- Khi xử lý văn bản tài liệu tĩnh (PDF, DOCX) không gắn liền với trục thời gian của media.\n- Khi tạo phụ đề tự động bằng mô hình AI Speech-to-Text (sử dụng các skill về Speech Recognition).",
        "prereqs": "- **Tệp phụ đề:** Tệp văn bản định dạng `.vtt`, `.srt`, hoặc `.ttml`.\n- **Công cụ kiểm tra:** Python `webvtt-py`, `pycaption`, hoặc bộ validator W3C Timed Text.",
        "concepts": "- **Cue Payload Formatting:** Cú pháp đánh dấu trong WebVTT bao gồm mốc bắt đầu `-->` mốc kết thúc, cùng các chỉ thị căn vị trí (line, position, align, size).\n- **Drift Synchronization:** Hiện tượng phụ đề bị trôi dần về cuối phim do sự không khớp giữa tốc độ khung hình (23.976 fps drop-frame vs 24 fps true).\n- **WCAG Captioning Standards:** Quy tắc hiển thị tối đa 2 dòng văn bản trên màn hình cùng một lúc, không vượt quá 37 ký tự mỗi dòng và tốc độ đọc tối ưu 160–180 từ/phút.",
        "workflow": "1. Phân tích cú pháp tệp phụ đề và kiểm tra dòng tiêu đề bắt buộc (`WEBVTT` header ở dòng đầu tiên).\n2. Kiểm tra tính tăng dần đơn điệu của trục thời gian: `start_time < end_time` và `start_time[n] >= start_time[n-1]`.\n3. Phát hiện các đoạn cue bị chồng lấn thời gian vô lý và tách biệt thành các dòng riêng biệt.\n4. Làm sạch các thẻ HTML không an toàn hoặc ký tự mã hóa Unicode lỗi thời.\n5. Đóng gói phụ đề vào HLS Master Playlist dưới dạng thẻ `#EXT-X-MEDIA:TYPE=SUBTITLES` với mã ngôn ngữ chuẩn ISO 639-1/2.\n6. Kiểm thử việc hiển thị trên trình phát HTML5 và khẳng định không có lỗi lệch khung.",
        "examples": """### Script Python xác thực và làm sạch tệp phụ đề WebVTT:
```python
import webvtt

def validate_and_clean_vtt(input_path, output_path):
    vtt = webvtt.read(input_path)
    cleaned_cues = []
    
    prev_end = "00:00:00.000"
    for idx, cue in enumerate(vtt):
        # 1. Kiem tra thoi gian bat dau phai nho hon thoi gian ket thuc
        assert cue.start < cue.end, f"Invalid duration at cue {idx}: {cue.start} -> {cue.end}"
        
        # 2. Canh bao va sua neu co va cham chong lan
        if cue.start < prev_end:
            print(f"[WARN] Overlapping cue detected at {cue.start}, adjusting...")
            cue.start = prev_end
            
        # 3. Kiem tra so dong khong vuot qua 2 dong
        lines = [line.strip() for line in cue.text.split('\\n') if line.strip()]
        if len(lines) > 2:
            print(f"[WARN] Cue {idx} has {len(lines)} lines, collapsing to 2 lines.")
            cue.text = " ".join(lines[:-1]) + "\\n" + lines[-1]
            
        prev_end = cue.end
        cleaned_cues.append(cue)
        
    vtt.save(output_path)
    print(f"Validated {len(cleaned_cues)} cues successfully.")

validate_and_clean_vtt("subs_raw.vtt", "subs_clean.vtt")
```""",
        "antipatterns": "- **Missing WEBVTT Header:** Lưu tệp chỉ có các mốc giờ mà thiếu chữ `WEBVTT` ở đầu tệp khiến trình duyệt Safari từ chối tải phụ đề hoàn toàn.\n- **Comma vs Period Millisecond Delimiters:** Dùng dấu phẩy `,` (kiểu SRT `00:01:20,500`) thay vì dấu chấm `.` (kiểu WebVTT `00:01:20.500`) trong tệp VTT.\n- **Excessive Text Density:** Nhét cả đoạn văn bản 4 dòng dài dằng dặc che kín màn hình video gây cản trở tầm nhìn của người xem.",
        "gates": "- **QG-01**: Tệp phụ đề vượt qua kiểm tra cú pháp WebVTT/TTML với 0 lỗi biên dịch.\n- **QG-02**: Không có mốc thời gian âm hoặc va chạm thời gian giữa các câu thoại đơn âm.\n- **QG-03**: Định danh ngôn ngữ tuân thủ chính xác mã chuẩn quốc tế (ví dụ: `en`, `vi`, `ja`).",
        "security": "- Lọc sạch các thẻ script nguy hiểm (`<script>`, `onerror=`) chèn trong nội dung phụ đề trước khi render vào DOM (XSS prevention).",
        "adapters": "- **Runtimes**: WebVTT, pycaption, Subtitle Edit CLI, FFmpeg subtitles filter.",
        "deliverables": "- Tệp phụ đề WebVTT chuẩn hóa (`captions_standard.vtt`).\n- Báo cáo lỗi va chạm và cảnh báo khả năng tiếp cận WCAG.",
        "related": "dex-video-transcoding-ladders, dex-streaming-manifest-validation",
        "usage": "```bash\n# Chuyen doi tu phu de SRT sang WebVTT chuan bang ffmpeg\nffmpeg -y -i subtitles.srt -c:s webvtt subtitles.vtt\n```"
    },
    {
        "id": "dex-manga-reader-performance",
        "name": "dex-manga-reader-performance",
        "desc": "Optimize high-performance long-strip (webtoon) and paginated manga reader engines. Implement virtualized canvas/DOM windowing, preemptive image prefetching, decode memory pooling, and scroll position restoration.",
        "purpose": "Thiết kế và tối ưu hóa hiệu năng cho trình đọc truyện tranh trực tuyến (Manga/Webtoon Reader Engine); áp dụng kỹ thuật ảo hóa danh sách trang (Virtualized Viewport Windowing), tiền tải thông minh hình ảnh tiếp theo (Preemptive Prefetching), quản lý vùng nhớ đệm giải mã ảnh (Bitmap Decode Memory Pooling) nhằm triệt tiêu hiện tượng lag giật và chống tràn RAM trên các thiết bị di động khi đọc các bộ truyện hàng trăm trang.",
        "when_use": "- Khi xây dựng hoặc tái cấu trúc ứng dụng đọc truyện tranh kỹ thuật số dạng cuộn dọc liên tục (Webtoon / Long-strip) hoặc lật trang đôi (Double-page spread).\n- Khi ứng dụng bị sập tab (Out of Memory - OOM crash) do tải quá nhiều hình ảnh chất lượng cao vào DOM cùng một lúc.\n- Khi cần duy trì chính xác vị trí cuộn trang (scroll position restoration) sau khi xoay màn hình hoặc tải lại trang.",
        "when_not_use": "- Khi ứng dụng chỉ hiển thị bài viết văn bản thuần túy với 1-2 hình ảnh minh họa nhỏ.\n- Khi đọc tài liệu PDF văn bản thông thường (nên dùng PDF.js chuyên dụng).",
        "prereqs": "- **Công nghệ frontend:** React, Vue, Svelte hoặc Vanilla JS với HTML5 Canvas và IntersectionObserver.\n- **Hạ tầng hình ảnh:** Máy chủ CDN hỗ trợ ảnh định dạng WebP/AVIF hiện đại.",
        "concepts": "- **DOM Virtualization:** Chỉ render vào cây DOM những trang truyện nằm trong viewport cộng thêm vùng đệm (buffer window 2 trang trước và sau); các trang còn lại được thay thế bằng placeholder có chiều cao tương ứng.\n- **createImageBitmap Decoupling:** Giải mã dữ liệu nén của ảnh trên Background Web Worker bằng `createImageBitmap` thay vì giải mã trên Main UI Thread gây nghẽn giao diện.\n- **Memory Ceiling Budget:** Giới hạn tổng dung lượng ảnh giải mã trong bộ nhớ RAM không vượt quá 150MB trên thiết bị di động.",
        "workflow": "1. Khởi tạo IntersectionObserver để theo dõi các phần tử giữ chỗ (placeholder element) của từng trang truyện.\n2. Khi trang đi vào vùng đệm (buffer margin 1000px), kích hoạt pipeline tải ảnh bất đồng bộ.\n3. Chuyển đổi Blob tải về thành Bitmap thông qua Web Worker hoặc `img.decode()` bất đồng bộ.\n4. Đưa hình ảnh đã giải mã vào thẻ `<canvas>` hoặc `<img>` và giải phóng URL tạm bằng `URL.revokeObjectURL()`.\n5. Khi trang cuộn ra xa khỏi viewport (cách hơn 3 màn hình), chủ động xóa thuộc tính `src` hoặc context của canvas để bộ thu gom rác (Garbage Collector) dọn dẹp RAM.\n6. Lưu mốc phần trăm trang đã đọc vào `localStorage` kèm debounce 300ms.",
        "examples": """### Module ao hoa va giai ma anh bat dong bo cho Webtoon Reader:
```javascript
class MangaVirtualScroller {
  constructor(container, pages) {
    this.container = container;
    this.pages = pages; // Danh sach URL cac trang
    this.renderedPages = new Map();
    this.initObserver();
  }

  initObserver() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const pageIdx = parseInt(entry.target.dataset.pageIndex, 10);
        if (entry.isIntersecting) {
          this.loadPageImage(pageIdx, entry.target);
        } else {
          this.unloadPageImage(pageIdx, entry.target);
        }
      });
    }, { rootMargin: '800px 0px 800px 0px' });
  }

  async loadPageImage(idx, element) {
    if (this.renderedPages.has(idx)) return;
    const imgUrl = this.pages[idx];
    
    const img = new Image();
    img.src = imgUrl;
    img.loading = 'eager';
    try {
      await img.decode(); // Giai ma truoc ngoai main-thread
      element.innerHTML = '';
      element.appendChild(img);
      this.renderedPages.set(idx, img);
    } catch (err) {
      console.error(`Failed to decode page ${idx}:`, err);
    }
  }

  unloadPageImage(idx, element) {
    if (this.renderedPages.has(idx)) {
      const img = this.renderedPages.get(idx);
      img.src = ''; // Huy lien ket bo nho bitmap
      element.innerHTML = `<div class="page-placeholder" style="height:${element.clientHeight}px"></div>`;
      this.renderedPages.delete(idx);
    }
  }
}
```""",
        "antipatterns": "- **Appending 100 Image Tags Directly:** Nối thẳng 100 thẻ `<img src=\"large_page.jpg\">` vào DOM cùng lúc làm cạn kiệt RAM thiết bị và đóng băng luồng UI.\n- **Layout Thrashing on Scroll:** Đọc liên tục các thuộc tính `offsetTop` và `clientHeight` trong sự kiện cuộn `window.onscroll` mà không bọc trong `requestAnimationFrame`.\n- **Ignoring Network Tier:** Vẫn tải ảnh gốc 4K cho người dùng đang bật chế độ tiết kiệm dữ liệu (Data Saver mode).",
        "gates": "- **QG-01**: Tốc độ khung hình khi cuộn dọc duy trì ổn định 60fps (hoặc 120fps trên màn hình ProMotion) không rớt khung hình nghiêm trọng.\n- **QG-02**: Mức tiêu thụ bộ nhớ RAM của tab trình duyệt giữ dưới 150MB trong suốt 50 trang cuộn liên tục.\n- **QG-03**: Khôi phục chính xác 100% vị trí trang đang đọc sau khi người dùng reload trang.",
        "security": "- Ngăn chặn tấn công Pixel Flood / Decompression Bomb bằng cách giới hạn kích thước tối đa của hình ảnh được phép giải mã (chiều rộng tối đa 4096px).",
        "adapters": "- **Runtimes**: Modern Browsers (Chrome, Safari, Firefox), React Native WebView, Tauri Desktop Manga Readers.",
        "deliverables": "- Thư viện điều phối ảo hóa trình đọc truyện (`MangaVirtualScroller.js`).\n- Bộ benchmark đo lường bộ nhớ RAM và tỷ lệ FPS khi cuộn trang.",
        "related": "dex-frontend-performance, dex-streaming-qoe-telemetry",
        "usage": "```bash\n# Kiem thu hieu nang cuon trang bang Lighthouse CLI\nlighthouse https://example.com/reader/chapter-1 --only-categories=performance --view\n```"
    },
    {
        "id": "dex-media-metadata-normalization",
        "name": "dex-media-metadata-normalization",
        "desc": "Normalize, resolve, and deduplicate multimedia metadata across movies, series, anime, and manga. Handle multilingual titles, romanized naming schemes, and synchronize canonical external IDs.",
        "purpose": "Chuẩn hóa, phân giải và hợp nhất dữ liệu siêu dữ liệu đa phương tiện (Media Metadata Normalization); xử lý các biến thể tiêu đề đa ngôn ngữ (chữ Hán/Kanji, Romaji phiên âm, tên tiếng Anh, tên phát hành tiếng Việt), loại bỏ dữ liệu trùng lặp (Deduplication) và liên kết đồng bộ các mã định danh chuẩn từ các kho dữ liệu quốc tế (TMDB, IMDb, AniList, MyAnimeList, MusicBrainz, Wikidata).",
        "when_use": "- Khi xây dựng kho danh mục nội dung đa phương tiện tổng hợp (VOD streaming catalog, manga aggregator, digital library).\n- Khi nhập khẩu dữ liệu từ nhiều nhà cung cấp khác nhau với các quy ước đặt tên và phân chia mùa/tập (Season/Episode) mâu thuẫn nhau.\n- Khi cần ánh xạ thông minh các từ khóa tìm kiếm của người dùng sang thực thể chính tắc (Canonical Media Entity).",
        "when_not_use": "- Khi ứng dụng chỉ xử lý các tập tin nhị phân nội bộ mà không cần phân loại hoặc hiển thị thông tin tác phẩm ra người dùng.\n- Khi dữ liệu đã được gán nhãn cứng bởi một cơ quan đăng ký duy nhất mà không có nguồn đối sánh bên ngoài.",
        "prereqs": "- **Cơ sở dữ liệu:** PostgreSQL hỗ trợ extension `pg_trgm` (trigram matching) và `unaccent`.\n- **Nguồn dữ liệu tham chiếu:** API Keys cho TMDB, AniList GraphQL, hoặc Wikidata SPARQL endpoint.",
        "concepts": "- **Fuzzy String Matching (Trigram Similarity):** Thuật toán so khớp chuỗi xấp xỉ giúp nhận diện các tiêu đề có sự sai lệch nhỏ về chính tả, dấu cách hoặc ký tự đặc biệt.\n- **External ID Graph:** Bảng quan hệ liên kết một bản ghi nội bộ với nhiều mã khóa định danh bên ngoài (`tmdb_id`, `imdb_id`, `mal_id`, `anilist_id`).\n- **Canonical Title Hierarchy:** Thứ tự ưu tiên xác định tên chính: Tên bản địa gốc (Native) -> Tên phiên âm quốc tế (Romaji) -> Tên tiếng Anh chính thức -> Danh sách bí danh (Aliases).",
        "workflow": "1. Thu thập chuỗi siêu dữ liệu thô (tên phim, số mùa, số tập, năm phát hành, tên studio/tác giả).\n2. Làm sạch chuỗi: loại bỏ thông tin tag kỹ thuật (ví dụ `[1080p]`, `[x265]`, `[Vietsub]`, `Dual Audio`).\n3. Truy vấn tìm kiếm trên cơ sở dữ liệu tham chiếu (TMDB/AniList) bằng tiêu đề đã làm sạch và năm phát hành.\n4. Đánh giá độ tin cậy của kết quả (Confidence Score): nếu Similarity >= 0.85, tự động gán mã liên kết; nếu từ 0.65 đến 0.84, đưa vào danh sách chờ nhân sự đối soát.\n5. Chuẩn hóa cấu trúc đánh số tập và mùa theo định dạng SxxExx tiêu chuẩn.\n6. Cập nhật thực thể canonical vào database kèm mốc thời gian kiểm chứng.",
        "examples": """### Pipeline Python chuan hoa tieu de truyen/phim va trich xuat mua/tap:
```python
import re
from difflib import SequenceMatcher

def clean_media_title(raw_title):
    # Loai bo cac the nguon [1080p], (Batch), [Vietsub]
    cleaned = re.sub(r'\[.*?\]|\(.*?\)', '', raw_title)
    
    # Trich xuat mua va tap (VD: S02E15 hoac Season 2 Episode 15)
    season_match = re.search(r'(?:S|Season\s*)(\d+)', cleaned, re.IGNORECASE)
    episode_match = re.search(r'(?:E|Episode|Ep\s*)(\d+)', cleaned, re.IGNORECASE)
    
    season = int(season_match.group(1)) if season_match else 1
    episode = int(episode_match.group(1)) if episode_match else 1
    
    # Loai bo phan tap khoi ten chinh
    core_title = re.sub(r'(?:S\d+)?(?:E\d+)|(?:Season\s*\d+)?(?:Episode\s*\d+)', '', cleaned, flags=re.IGNORECASE)
    core_title = " ".join(core_title.split()).strip()
    
    return {"canonical_title": core_title, "season": season, "episode": episode}

def calculate_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

raw = "[SubsPlease] Frieren Beyond Journey's End - S01E28 [1080p] [Vietsub].mkv"
print(clean_media_title(raw))
# Output: {'canonical_title': "Frieren Beyond Journey's End -", 'season': 1, 'episode': 28}
```""",
        "antipatterns": "- **Destructive Stripping of Roman Numerals:** Xóa nhầm các ký tự số La Mã (như `II`, `III`) trong tên tác phẩm làm mất phân biệt giữa các phần tiếp theo.\n- **Single Source Lock-in:** Chỉ phụ thuộc vào 1 API bên thứ ba (như TMDB); khi API đó đổi policy hoặc sập mạng, toàn bộ pipeline nhập liệu bị đình trệ.\n- **Ignoring Unicode Normalization Form:** Không chuẩn hóa chuỗi về dạng NFC trước khi so sánh khiến các ký tự có dấu tổ hợp bị lệch mã hash.",
        "gates": "- **QG-01**: Tỷ lệ phân giải chính xác tiêu đề chuẩn (Disambiguation Precision) đạt trên 98% trên tập mẫu kiểm thử.\n- **QG-02**: Không có bản ghi trùng lặp nào cùng chia sẻ chung một `tmdb_id` hoặc `imdb_id` trong danh mục chính tắc.\n- **QG-03**: Tất cả các chuỗi văn bản lưu trữ đều được chuẩn hóa Unicode NFC.",
        "security": "- Giới hạn tần suất gọi API bên ngoài (Rate Limiting) và bảo vệ an toàn các API Key của bên cung cấp dịch vụ.",
        "adapters": "- **Runtimes**: Python, PostgreSQL pg_trgm, AniList GraphQL, TMDB v3 API, MusicBrainz API.",
        "deliverables": "- Module chuẩn hóa chuỗi siêu dữ liệu (`metadata_normalizer.py`).\n- Lược đồ CSDL quản lý bảng ánh xạ bí danh (`aliases_mapping_schema.sql`).",
        "related": "dex-database-engineering, dex-media-content-ingest-moderation",
        "usage": "```bash\n# Chay test chuan hoa metadata tren bo test case mau\npytest tests/test_metadata_normalization.py -v\n```"
    },
    {
        "id": "dex-streaming-qoe-telemetry",
        "name": "dex-streaming-qoe-telemetry",
        "desc": "Collect, aggregate, and analyze video streaming Quality of Experience (QoE) metrics. Measure startup time, rebuffering ratios, bitrate transitions, and playback failures without violating user privacy.",
        "purpose": "Thu thập, tổng hợp và phân tích các chỉ số chất lượng trải nghiệm phát video (Quality of Experience - QoE) từ phía người dùng cuối; đo lường chính xác thời gian khởi động phát (Time to First Frame / Startup Delay), tỷ lệ giật bộ đệm (Rebuffering Ratio), tần suất nhảy tầng bitrate và các lỗi phát nghiêm trọng (Fatal Playback Errors); bảo đảm tính riêng tư tuyệt đối cho người dùng không thu thập dữ liệu định danh cá nhân (Zero-PII Telemetry).",
        "when_use": "- Khi theo dõi chất lượng mạng phân phối CDN và hiệu năng phát video trên quy mô hàng triệu người dùng.\n- Khi đánh giá tác động của việc thay đổi thuật toán bitrate thích ứng (ABR) lên trải nghiệm thực tế của người xem.\n- Khi điều tra sự cố sụt giảm chất lượng video trên các nhà mạng viễn thông hoặc khu vực địa lý cụ thể.",
        "when_not_use": "- Khi ứng dụng chỉ phát tệp âm thanh ngắn hạn chế thời lượng (<5s) hoặc thông báo hệ thống.\n- Khi hệ thống giám sát hạ tầng thuần túy ở tầng mạng (ping, packet loss máy chủ) mà không đo lường góc nhìn của trình phát video.",
        "prereqs": "- **Hệ thống trình phát:** HLS.js, Shaka Player, hoặc Video.js có hook sự kiện phân tích.\n- **Hạ tầng Telemetry:** Endpoint nạp dữ liệu phân tích có khả năng chịu tải cao (Kafka, ClickHouse, hoặc AWS Kinesis).",
        "concepts": "- **Time to First Frame (TTFF):** Thời gian tính từ khi người dùng bấm nút Play cho đến khi khung hình video đầu tiên thực sự được vẽ lên màn hình.\n- **Rebuffer Ratio:** Tỷ lệ phần trăm thời gian người xem phải chờ nạp bộ đệm chia cho tổng thời gian xem video (mục tiêu tiêu chuẩn công nghiệp < 0.5%).\n- **Beacon API:** API trình duyệt `navigator.sendBeacon()` gửi dữ liệu telemetry bất đồng bộ khi người dùng chuẩn bị đóng tab mà không làm chậm việc điều hướng.",
        "workflow": "1. Đăng ký các bộ lắng nghe sự kiện trên video player (`waiting`, `playing`, `error`, `ratechange`).\n2. Đo đạc các mốc thời gian quan trọng: Bắt đầu tải manifest -> Nhận manifest -> Tải segment 0 -> Hiển thị khung hình 1.\n3. Định kỳ 30 giây gom các thông số (bitrate trung bình, số lần buffer, số frame bị rớt - dropped frames) thành một payload gọn nhẹ.\n4. Gửi payload về backend qua `navigator.sendBeacon()` hoặc HTTP POST nén gzip.\n5. Tổng hợp dữ liệu trên dashboard theo thời gian thực (P50, P90, P99 của TTFF và tỷ lệ rebuffer).\n6. Kích hoạt cảnh báo tự động nếu tỷ lệ lỗi phát sóng vượt ngưỡng 1.0% trong 5 phút liên tiếp.",
        "examples": """### Module thu thap telemetry QoE video nhe khong thu thap PII:
```javascript
class VideoQoETracker {
  constructor(videoElement, streamId) {
    this.video = videoElement;
    this.streamId = streamId;
    this.metrics = {
      startTime: Date.now(),
      ttffMs: 0,
      rebufferDurationMs: 0,
      rebufferCount: 0,
      totalPlayDurationMs: 0
    };
    this.bindEvents();
  }

  bindEvents() {
    let rebufferStart = 0;
    
    // Do TTFF
    const onFirstFrame = () => {
      this.metrics.ttffMs = Date.now() - this.metrics.startTime;
      this.video.removeEventListener('playing', onFirstFrame);
    };
    this.video.addEventListener('playing', onFirstFrame);

    // Theo doi Rebuffering
    this.video.addEventListener('waiting', () => {
      rebufferStart = Date.now();
      this.metrics.rebufferCount++;
    });

    this.video.addEventListener('playing', () => {
      if (rebufferStart > 0) {
        this.metrics.rebufferDurationMs += (Date.now() - rebufferStart);
        rebufferStart = 0;
      }
    });

    // Gui beacon khi dong trang
    window.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') {
        this.flush();
      }
    });
  }

  flush() {
    const payload = JSON.stringify({
      streamId: this.streamId,
      ttff: this.metrics.ttffMs,
      rebufferRatio: this.metrics.rebufferDurationMs / Math.max(1, this.video.currentTime * 1000),
      rebuffers: this.metrics.rebufferCount
    });
    navigator.sendBeacon('/api/v1/telemetry/qoe', payload);
  }
}
```""",
        "antipatterns": "- **Tracking Personal Identifiers (PII):** Gửi kèm email, IP nguyên bản hoặc tên thật của người dùng vào payload telemetry gây vi phạm GDPR/CCPA.\n- **Synchronous Telemetry Calls:** Dùng AJAX đồng bộ chặn đứng sự kiện thoát tab của trình duyệt làm giảm trải nghiệm người dùng.\n- **High Frequency Reporting:** Gửi ping telemetry mỗi 100ms gây quá tải hệ thống ingestion backend và tốn pin điện thoại.",
        "gates": "- **QG-01**: Payload telemetry không chứa bất kỳ dữ liệu PII nào; IP được băm ẩn danh (anonymized/truncated).\n- **QG-02**: Quá trình thu thập telemetry không chiếm quá 1% CPU của Main Thread.\n- **QG-03**: Tỷ lệ gửi thành công qua `sendBeacon` đạt trên 99% khi người dùng đóng trang.",
        "security": "- Tuân thủ nghiêm ngặt nguyên tắc Data Minimization; mã hóa luồng dữ liệu telemetry khi truyền tải qua HTTPS.",
        "adapters": "- **Runtimes**: W3C Media Capabilities API, HLS.js telemetry, Shaka Player analytics, ClickHouse.",
        "deliverables": "- Thư viện thu thập QoE phía client (`VideoQoETracker.js`).\n- Lược đồ bảng lưu trữ phân tích dữ liệu QoE trên ClickHouse.",
        "related": "dex-video-transcoding-ladders, dex-streaming-manifest-validation, dex-live-stream-latency-control",
        "usage": "```bash\n# Truy van chi so QoE P95 tu ClickHouse\nclickhouse-client --query \"SELECT quantile(0.95)(ttff) AS p95_ttff, avg(rebuffer_ratio) FROM qoe_events WHERE timestamp >= now() - INTERVAL 1 HOUR\"\n```"
    },
    {
        "id": "dex-media-content-ingest-moderation",
        "name": "dex-media-content-ingest-moderation",
        "desc": "Validate, inspect, and quarantine incoming media assets during ingest. Detect container-level malformations, verify audio/video codec integrity, and isolate malicious payloads.",
        "purpose": "Kiểm định, rà soát và cách ly tự động các tệp đa phương tiện đầu vào trong pipeline nạp nội dung (Media Ingest Moderation Pipeline); phát hiện các dị tật ở tầng container (MP4 atom corruption, MKV header malformation), xác minh tính toàn vẹn của luồng âm thanh/hình ảnh, ngăn chặn các kỹ thuật chèn mã độc vào metadata (ID3/EXIF exploits) và cách ly an toàn các tệp nguy hiểm.",
        "when_use": "- Khi tiếp nhận tệp video/âm thanh từ người dùng tải lên (UGC platforms, cloud storage).\n- Khi xây dựng rào chắn an ninh trước khi đưa tệp vào cụm máy chủ giải mã và transcoding tập trung.\n- Khi cần xác minh nhanh một tệp media có đúng là định dạng thực tế hay chỉ là tệp thực thi độc hại ngụy trang đổi đuôi mở rộng.",
        "when_not_use": "- Khi tệp media được sinh ra từ chính các máy chủ nội bộ đã được chứng thực chữ ký số an toàn.\n- Khi kiểm duyệt nội dung hình ảnh nhạy cảm về mặt thị giác (sử dụng các mô hình Computer Vision Moderation chuyên dụng).",
        "prereqs": "- **Công cụ kiểm tra:** MediaInfo CLI, FFprobe, hoặc thư viện `mutagen` / `exiftool` chạy trong sandbox cô lập.\n- **Môi trường:** Container không có quyền root (unprivileged container) với giới hạn RAM và CPU chặt chẽ.",
        "concepts": "- **Magic Byte Validation:** Kiểm tra các byte nhận diện đầu tệp (ví dụ `ftypisom` trong MP4, `\x1a\x45\xdf\xa3` trong MKV/WebM) thay vì tin tưởng phần mở rộng của tệp.\n- **Container Bomb Protection:** Ngăn ngừa các tệp chứa cấu trúc đệ quy hoặc thông số kích thước ảo (như atom MP4 có kích thước 1000 Terabyte) gây sập parser.\n- **Quarantine Isolation:** Di chuyển các tệp lỗi hoặc nghi ngờ vào vùng lưu trữ cách ly biệt lập, ngăn chặn việc kích hoạt tự động các worker tiếp theo.",
        "workflow": "1. Tiếp nhận tệp và kiểm tra Magic Bytes ở 64 byte đầu tiên của tệp.\n2. Chạy `ffprobe` với các cờ hạn chế quyền (`-v error -show_entries stream=codec_type,codec_name -of json`).\n3. Quét sạch các trường siêu dữ liệu (metadata tags) để phát hiện ký tự điều khiển lạ hoặc chuỗi nghi ngờ SQL Injection / Command Injection.\n4. Xác nhận sự tồn tại của ít nhất một luồng video hoặc audio hợp lệ có thời lượng lớn hơn 0.\n5. Nếu phát hiện tệp hỏng hoặc có cấu trúc bất thường, đánh dấu trạng thái QUARANTINED và gửi thông báo kiểm toán.\n6. Nếu tệp vượt qua toàn bộ các bài kiểm tra, chuyển tệp sang bucket chính để tiến hành transcoding.",
        "examples": """### Script Python kiem tra va cach ly tep media doc hai / bi hong:
```python
import subprocess
import json
import os
import shutil

QUARANTINE_DIR = "/var/media/quarantine"
SAFE_DIR = "/var/media/processing"

def inspect_and_quarantine(file_path):
    # 1. Kiem tra dung luong co ban
    if os.path.getsize(file_path) == 0:
        return quarantine(file_path, "Empty file")
        
    # 2. Chay ffprobe trong sandbox bounded timeout 5s
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,format_name:stream=codec_type,codec_name,width,height",
        "-of", "json", file_path
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if proc.returncode != 0:
            return quarantine(file_path, f"Probe error: {proc.stderr[:100]}")
            
        data = json.loads(proc.stdout)
        streams = data.get("streams", [])
        if not streams:
            return quarantine(file_path, "No valid audio/video streams found")
            
        # Kiem tra kich thuoc hop le
        for s in streams:
            if s.get("codec_type") == "video":
                w, h = s.get("width", 0), s.get("height", 0)
                if w > 8192 or h > 8192:
                    return quarantine(file_path, f"Extreme dimensions: {w}x{h}")
                    
        # File an toan
        shutil.move(file_path, os.path.join(SAFE_DIR, os.path.basename(file_path)))
        print(f"File {file_path} PASSED inspection.")
        return True
    except subprocess.TimeoutExpired:
        return quarantine(file_path, "Parser timeout - potential zip/container bomb")

def quarantine(file_path, reason):
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    dest = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
    shutil.move(file_path, dest)
    print(f"[QUARANTINE] {file_path} isolated. Reason: {reason}")
    return False
```""",
        "antipatterns": "- **Trusting User-Supplied File Extensions:** Cho phép tệp `.mp4` đi thẳng vào pipeline transcoding mà không kiểm tra magic bytes khiến tệp script độc hại được thực thi.\n- **Running Transcoders as Root:** Chạy FFmpeg bằng quyền root khiến kẻ tấn công có thể chiếm toàn quyền điều khiển máy chủ nếu khai thác được lỗ hổng parser.\n- **Unbounded Processing Timeout:** Không đặt timeout khi phân tích cú pháp tệp khiến worker bị treo vĩnh viễn khi gặp các tệp lặp cấu trúc vô tận.",
        "gates": "- **QG-01**: 100% tệp nạp vào phải vượt qua kiểm tra magic bytes và cấu trúc container hợp lệ.\n- **QG-02**: Mọi tiến trình kiểm tra (probe) đều bị giới hạn thời gian thực thi tối đa 5 giây và RAM tối đa 512MB.\n- **QG-03**: Các tệp bị lỗi hoặc vi phạm chính sách được cách ly tự động 100% không để lọt vào pipeline chính.",
        "security": "- Thực thi cơ chế phòng thủ chiều sâu (Defense-in-Depth); cô lập parser trong sandbox cgroups/seccomp không có kết nối mạng internet.",
        "adapters": "- **Runtimes**: FFprobe, MediaInfo, Python mutagen, Linux seccomp sandbox.",
        "deliverables": "- Kịch bản điều phối kiểm duyệt nạp tệp (`ingest_moderator.py`).\n- Báo cáo nhật ký cách ly tệp độc hại (`quarantine_audit.log`).",
        "related": "dex-video-transcoding-ladders, dex-media-metadata-normalization",
        "usage": "```bash\n# Kiem tra nhanh container media bang mediainfo\nmediainfo --Output=JSON suspicious_upload.bin\n```"
    },

    # =========================================================================
    # GROUP AR: Advanced Chess Engine & Native Performance (Skills 431–440)
    # =========================================================================
    {
        "id": "dex-chess-legal-movegen-perft",
        "name": "dex-chess-legal-movegen-perft",
        "desc": "Design, benchmark, and validate move generation engines for chess. Build comprehensive perft testing suites, verify magic bitboards, and eliminate subtle castling and en-passant bugs.",
        "purpose": "Thiết kế, kiểm thử và chứng minh tính đúng đắn tuyệt đối của bộ sinh nước đi cờ vua (Chess Move Generation Engine); xây dựng bộ kiểm thử perft (Performance Test) toàn diện từ các vị trí tiêu chuẩn đến các thế cờ biên phức tạp; kiểm chứng thuật toán Magic Bitboards cho quân Xe và Tượng, giải quyết triệt để các lỗi tinh vi về phong cấp, bắt tốt qua đường (En Passant), quyền nhập thành và thoát chiếu.",
        "when_use": "- Khi phát triển hoặc tối ưu hóa engine cờ vua viết bằng C++, Rust, Zig, hoặc C#.\n- Khi chuyển đổi từ bộ sinh nước đi pseudo-legal sang legal move generator hoặc tối ưu hóa cấu trúc dữ liệu Bitboard 64-bit.\n- Khi phát hiện engine bị treo, tính toán số nút sai lệch so with cơ sở dữ liệu chuẩn Stockfish perft.",
        "when_not_use": "- Khi ứng dụng chỉ là bàn cờ hiển thị giao diện người dùng đơn giản (UI chessboard) đã có thư viện chuẩn như `chess.js` đảm nhiệm.\n- Khi giải quyết các bài toán tìm kiếm nước đi AI mà chưa hoàn thiện tầng sinh nước đi cơ sở.",
        "prereqs": "- **Kiến trúc dữ liệu:** Biểu diễn bàn cờ bằng Bitboard 64-bit (`uint64_t`), Magic Bitboards hoặc PEXT Bitboards.\n- **Bộ dữ liệu chuẩn:** Tệp danh sách vị trí FEN kèm số nút perft chuẩn (Stockfish/Chess Programming Wiki perft test suites).",
        "concepts": "- **Perft (Performance Test):** Hàm duyệt cây đệ quy đếm tổng số lượng nút lá (leaf nodes) tại một độ sâu nhất định để xác minh bộ sinh nước đi không thừa và không thiếu bất kỳ nước cờ hợp lệ nào.\n- **Magic Bitboards:** Kỹ thuật băm hoàn hảo sử dụng phép nhân số nguyên 64-bit và phép dịch bit để tra cứu bảng nước đi của quân trượt (Rook/Bishop) trong thời gian $O(1)$.\n- **Make/Unmake vs Copy-Make:** Kỹ thuật áp dụng nước đi lên trạng thái bàn cờ hiện tại và phục hồi lại (Make/Unmake) so với sao chép toàn bộ struct bàn cờ (Copy-Make).",
        "workflow": "1. Thiết lập biểu diễn bàn cờ 64 ô sử dụng kiểu dữ liệu số nguyên không dấu 64-bit (`U64 bitboards`).\n2. Cài đặt bộ sinh nước đi pseudo-legal cho từng loại quân cờ (Tốt, Mã, Tượng, Xe, Hậu, Vua).\n3. Lọc bỏ các nước đi không hợp lệ (nước đi khiến Vua phe mình bị chiếu) bằng hàm `is_in_check()`.\n4. Xử lý các điều kiện đặc biệt: Quyền nhập thành bị mất khi Xe/Vua di chuyển hoặc các ô bị kiểm soát, mốc bắt tốt qua đường (ep square).\n5. Viết hàm đệ quy `perft(depth)` và in chi tiết chia nhánh (perft divide) cho từng nước đi đầu tiên.\n6. Chạy kiểm thử tự động trên bộ 10 vị trí FEN thử thách nổi tiếng (Kiwipete, Position 3, Position 4, Position 5).",
        "examples": """### Ham duyet cay perft va divide kiem thu move generator bang C++20:
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

    std::cout << "--- PERFT DIVIDE (Depth " << depth << ") ---\\n";
    for (const auto& move : move_list) {
        board.make_move(move);
        uint64_t nodes = perft(depth - 1, board);
        board.unmake_move(move);
        std::cout << move_to_uci(move) << ": " << nodes << "\\n";
        total_nodes += nodes;
    }
    std::cout << "Total Nodes: " << total_nodes << "\\n";
}
```""",
        "antipatterns": "- **Allowing Castling Through Check:** Cho phép nhập thành khi ô trung gian giữa Vua và Xe đang bị quân đối phương tấn công (vi phạm luật cờ vua quốc tế).\n- **En Passant Pin Disregard:** Quên kiểm tra việc bắt tốt qua đường có thể mở ra đường chiếu ngang của Xe đối phương lên Vua của mình.\n- **Slow Board Copying:** Lạm dụng việc sao chép toàn bộ đối tượng Board lớn trên mỗi nút đệ quy khiến tốc độ perft bị giảm từ 50 triệu nút/giây xuống dưới 1 triệu nút/giây.",
        "gates": "- **QG-01**: Vị trí xuất phát đạt chính xác `4,865,609` nút ở độ sâu `depth = 5` và `119,060,324` nút ở `depth = 6`.\n- **QG-02**: Vị trí Kiwipete (`r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -`) đạt chính xác `4,085,603` nút ở độ sâu 4.\n- **QG-03**: Tốc độ sinh nước đi đạt tối thiểu 25 triệu nút/giây (25 MNPS) trên một luồng CPU hiện đại.",
        "security": "- Ngăn ngừa lỗi tràn mảng danh sách nước đi (MoveList buffer overflow) bằng cách cấp phát kích thước tối đa 256 phần tử cho một vị trí cờ.",
        "adapters": "- **Runtimes**: C++20/C++23 (GCC, Clang, MSVC), Rust 2021, Cutechess-cli, Stockfish perft.",
        "deliverables": "- Mô-đun sinh nước đi cờ vua chuẩn (`movegen.cpp` / `movegen.rs`).\n- Bộ kiểm thử tự động Perft Suite 100 vị trí (`perft_suite_runner.py`).",
        "related": "dex-chess-search-pruning-evals, dex-chess-transposition-table-correctness, dex-chess-uci-protocol-compliance",
        "usage": "```bash\n# Chay test perft divide cho vi tri Kiwipete do sau 4\n./chess_engine perft \"r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -\" 4\n```"
    },
    {
        "id": "dex-chess-search-pruning-evals",
        "name": "dex-chess-search-pruning-evals",
        "desc": "Implement, evaluate, and tune alpha-beta search pruning heuristics in chess engines. Benchmark LMR, Null Move Pruning, Futility Pruning, and SEE while avoiding tactical regressions.",
        "purpose": "Thiết kế, tinh chỉnh và kiểm chứng các thuật toán cắt tỉa nhánh tìm kiếm trong engine cờ vua (Search Pruning Heuristics); tối ưu hóa thuật toán Alpha-Beta / Principal Variation Search (PVS); tích hợp Null Move Pruning (NMP), Late Move Reductions (LMR), Reverse Futility Pruning (RFP) và Static Exchange Evaluation (SEE); đo lường chính xác tương quan giữa độ sâu tìm kiếm (Search Depth) và điểm số mù chiến thuật (Tactical Blindspots).",
        "when_use": "- Khi engine cờ vua bị tụt độ sâu tìm kiếm so với đối thủ cùng thời gian (time control).\n- Khi muốn cải thiện hệ số phân nhánh hữu hiệu (Effective Branching Factor - EBF) từ 5.0 xuống 2.0 hoặc thấp hơn.\n- Khi cần tinh chỉnh các công thức giảm độ sâu nước đi muộn (LMR formula) dựa trên số lượng nước đi và độ sâu hiện tại.",
        "when_not_use": "- Khi bộ sinh nước đi hoặc hàm đánh giá tĩnh (Static Evaluation) chưa ổn định và còn tồn tại lỗi logic cơ bản.\n- Khi giải bài toán cờ tàn giải quyết triệt để bằng bảng dữ liệu Endgame Tablebase (sử dụng `dex-chess-endgame-tablebase-integration`).",
        "prereqs": "- **Bộ sinh nước đi:** Bộ sinh nước đi hợp lệ đã vượt qua kiểm thử perft.\n- **Hàm đánh giá tĩnh:** Hàm đánh giá tĩnh cơ bản (HCE hoặc NNUE) trả về điểm số centipawn ổn định.",
        "concepts": "- **Null Move Pruning (NMP):** Kỹ thuật cho phép đối phương đi thêm một nước; nếu đối phương vẫn không thể tạo ra ưu thế vượt trội, vị trí hiện tại quá mạnh và có thể cắt tỉa nhánh ngay lập tức (tránh hiện tượng Zugzwang).\n- **Late Move Reductions (LMR):** Giảm độ sâu tìm kiếm đối với các nước đi nằm ở cuối danh sách nước cờ đã được sắp xếp, vì xác suất một nước cờ muộn trở thành nước cờ tối ưu là rất thấp.\n- **Static Exchange Evaluation (SEE):** Thuật toán mô phỏng chuỗi ăn quân tại một ô cờ duy nhất để xác định xem việc đổi quân có đem lại lợi thế vật chất hay không mà không cần tìm kiếm toàn diện.",
        "workflow": "1. Thiết lập khung tìm kiếm chuẩn PVS (Principal Variation Search) với cửa sổ hẹp (Zero-Window Search).\n2. Cài đặt Quiescence Search (tìm kiếm tĩnh) chỉ duyệt các nước ăn quân và phong cấp để tránh hiệu ứng chân trời (Horizon Effect).\n3. Tích hợp Reverse Futility Pruning tại các nút tiền-lá (depth <= 2) nếu `eval - margin >= beta`.\n4. Cài đặt Null Move Pruning có kiểm tra điều kiện không tồn tại Zugzwang (không áp dụng khi chỉ còn Tốt và Vua).\n5. Thiết lập bảng giảm LMR dạng mảng 2 chiều tính trước `LMR_Table[depth][move_count]`.\n6. Chạy bộ kiểm thử chiến thuật WAC (Win At Chess) và STS (Strategic Test Suite) để đo lường tỷ lệ giải bài tập.",
        "examples": """### Cai dat thuat toan Alpha-Beta ket hop NMP va LMR bang C++:
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
```""",
        "antipatterns": "- **Blind Null Move in Zugzwang Endgames:** Cho phép Null Move Pruning ở tàn cuộc Vua Tốt dẫn đến việc engine bỏ qua các đòn zugzwang hiểm hóc và tự thua.\n- **Over-reducing Tactical Checks:** Áp dụng LMR cho các nước đi chiếu Vua hoặc nước đi ăn lại quân khiến engine bị mù các đòn chiến thuật đơn giản.\n- **Skipping Quiescence Search:** Dừng tìm kiếm ngay ở `depth = 0` mà không chạy Quiescence Search gây ra hiện tượng Horizon Effect nghiêm trọng.",
        "gates": "- **QG-01**: Tỷ lệ giải đúng bài tập trong bộ WAC (Win At Chess - 300 vị trí) đạt tối thiểu 285/300 bài ở 1 giây/nút.\n- **QG-02**: Tốc độ tìm kiếm sâu trung bình (Search Depth) tăng ít nhất 30% so với phiên bản Alpha-Beta không có pruning.\n- **QG-03**: Không bị dính lỗi lặp lại nước đi vô tận hoặc tìm kiếm vượt quá thời gian phân bổ.",
        "security": "- Kiểm tra điều kiện ngắt tìm kiếm định kỳ (Time Check mỗi 2048 nút) để tránh treo vô tận khi nhận lệnh `stop` từ GUI.",
        "adapters": "- **Runtimes**: C++20, Rust, Cutechess CLI, OpenBench / FastGM test harness.",
        "deliverables": "- Mô-đun tìm kiếm engine cờ vua (`search.cpp` / `search.rs`).\n- Báo cáo kết quả giải các bài tập chiến thuật STS và WAC.",
        "related": "dex-chess-legal-movegen-perft, dex-chess-transposition-table-correctness, dex-chess-engine-match-statistics",
        "usage": "```bash\n# Kiem thu engine tren bo bai tap chien thuat WAC bang script Python\npython scripts/chess/bench_tactics.py --engine ./my_engine --epd test/wac.epd --movetime 1000\n```"
    },
    {
        "id": "dex-chess-transposition-table-correctness",
        "name": "dex-chess-transposition-table-correctness",
        "desc": "Implement, verify, and tune Transposition Tables (TT) in chess engines. Ensure hash collision safety with Zobrist hashing, replacement strategies, lockless SMP probing, and bound semantics.",
        "purpose": "Thiết kế, kiểm chứng và tối ưu hóa bảng chuyển vị (Transposition Table - TT) trong engine cờ vua; bảo đảm an toàn trước va chạm hàm băm bằng Zobrist Hashing 64-bit; thiết lập chính sách thay thế ô nhớ (Replacement Schemes: Depth-preferred, Age-based, 2-tier bucket); xử lý đa luồng phi khóa (Lockless SMP TT Probing) an toàn trên CPU đa nhân và bảo đảm tính toàn vẹn của các cờ cận biên (EXACT, LOWERBOUND, UPPERBOUND).",
        "when_use": "- Khi engine gặp hiện tượng lặp lại tính toán các thế cờ hoán vị (Transposition) qua các thứ tự nước đi khác nhau.\n- Khi mở rộng engine chạy trên hệ thống đa luồng (SMP / Multithreading) sử dụng thuật toán Lazy SMP.\n- Khi muốn lưu giữ nước đi tốt nhất (Best Move) để hỗ trợ sắp xếp nước đi (Move Ordering Heuristics) cho các lượt lặp sâu hơn.",
        "when_not_use": "- Khi bộ nhớ hệ thống bị giới hạn nghiêm trọng (<16MB RAM) không đủ để cấp phát bảng băm hiệu quả.\n- Khi kiểm thử hàm perft đơn thuần (perft chỉ kiểm tra cây di chuyển, không dùng bảng TT trừ khi đo perft có TT).",
        "prereqs": "- **Cơ chế băm:** Bảng số ngẫu nhiên Zobrist 64-bit đã được khởi tạo hoàn tất.\n- **Bộ nhớ hệ thống:** Dung lượng RAM tối thiểu 64MB - 512MB để cấp phát bảng băm.",
        "concepts": "- **Zobrist Hashing:** Kỹ thuật băm bàn cờ bằng phép XOR các số ngẫu nhiên 64-bit được khởi tạo trước cho từng quân cờ tại từng ô cờ, lượt đi và quyền nhập thành.\n- **Bound Semantics:** Cờ đánh dấu giá trị lưu trong TT: `EXACT` (giá trị thực tế trong khoảng alpha-beta), `LOWERBOUND` (giá trị fail-high >= beta), `UPPERBOUND` (giá trị fail-low <= alpha).\n- **Lockless SMP (Shared TT with XOR Keys):** Kỹ thuật lưu trữ `key_xor_data = key ^ data` giúp các luồng đọc ghi đồng thời mà không cần mutex khóa, tự phát hiện dữ liệu rác nếu khóa không khớp.",
        "workflow": "1. Khởi tạo mảng số ngẫu nhiên Zobrist 64-bit cho 12 loại quân cờ x 64 ô, 16 trạng thái nhập thành, và 8 cột bắt tốt qua đường.\n2. Thiết kế cấu trúc ô nhớ `TTEntry` nhỏ gọn (16 byte hoặc 8 byte) để tối ưu hóa bộ nhớ đệm CPU Cache Line (64 byte).\n3. Cài đặt hàm `probe_tt()` trước khi bắt đầu duyệt cây tìm kiếm; cắt tỉa nhánh nếu độ sâu lưu trong TT đủ lớn và thỏa mãn cờ cận biên.\n4. Cài đặt hàm `store_tt()` cập nhật ô nhớ sau khi tìm kiếm hoàn tất, áp dụng chiến lược ưu tiên độ sâu lớn hơn hoặc thời gian cũ hơn (aging).\n5. Thiết lập cơ chế xóa và tăng chu kỳ tuổi (`age`) của bảng băm khi bắt đầu một ván cờ mới (`ucinewgame`).\n6. Đo kiểm tỷ lệ đánh trúng bảng băm (TT Hit Rate) và khẳng định không có xung đột dữ liệu trên môi trường 8-16 luồng.",
        "examples": """### Cau truc TTEntry 16-byte va thuat toan Lockless SMP trong C++20:
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
```""",
        "antipatterns": "- **Unbounded Mate Score Storage:** Lưu trực tiếp điểm số chiếu hết (Checkmate Score) mà không điều chỉnh khoảng cách ply từ nút gốc, khiến engine nhầm lẫn khoảng cách chiếu hết khi lấy từ TT.\n- **Entry Size Misalignment:** Cấu trúc Entry có kích thước lẻ (như 19 byte hoặc 23 byte) làm vỡ biên căn chỉnh cache line, gây suy giảm nghiêm trọng băng thông truy cập RAM.\n- **Missing Age Mechanism:** Không làm mới chu kỳ tuổi khiến các thế cờ từ ván đấu trước hoặc từ lượt tìm kiếm sâu trước đó chiếm dụng vĩnh viễn các ô nhớ giá trị.",
        "gates": "- **QG-01**: Tỷ lệ va chạm sai lệch khóa băm (False Hash Collision) bằng 0 tuyệt đối trên 100 triệu lượt truy xuất.\n- **QG-02**: Điểm số chiếu hết được điều chỉnh chính xác theo ply: `score += ply` khi lưu và `score -= ply` khi đọc.\n- **QG-03**: Kích thước mỗi phần tử `sizeof(TTEntry)` là bội số của 8 byte và vừa vặn chia hết cho 64-byte Cache Line.",
        "security": "- Cấp phát bộ nhớ an toàn cho bảng băm; kiểm tra giới hạn kích thước tối đa (ví dụ tối đa 32GB) tránh làm cạn kiệt RAM hệ điều hành.",
        "adapters": "- **Runtimes**: C++20/C++23, Rust (std::sync::atomic), Stockfish TT benchmarks.",
        "deliverables": "- Lớp triển khai bảng chuyển vị (`transposition_table.hpp` / `tt.rs`).\n- Bộ kiểm thử tính đúng đắn của Bound Semantics và độ tuổi băm.",
        "related": "dex-chess-search-pruning-evals, dex-chess-legal-movegen-perft, dex-chess-uci-protocol-compliance",
        "usage": "```bash\n# Kiem tra toc do truy xuat TT va hit rate bang che do benchmark\n./chess_engine bench 16 1 14 default depth\n```"
    },
    {
        "id": "dex-chess-nnue-evaluation-integration",
        "name": "dex-chess-nnue-evaluation-integration",
        "desc": "Integrate and optimize NNUE (Efficiently Updatable Neural Network) evaluation into chess engines. Validate SIMD accumulator updates, quantized int8 inference, and benchmark against classical HCE.",
        "purpose": "Tích hợp và tối ưu hóa mạng nơ-ron cập nhật hiệu quả (NNUE - Efficiently Updatable Neural Network) vào engine cờ vua; cài đặt bộ tích lũy cập nhật vi sai (Incremental Accumulator Updates) trên các tập lệnh SIMD (AVX2, AVX-512, ARM Neon); lượng tử hóa trọng số về dạng số nguyên 8-bit/16-bit (`int8_t` / `int16_t`) và đo kiểm sức mạnh thi đấu so với hàm đánh giá thủ công truyền thống (Handcrafted Evaluation - HCE).",
        "when_use": "- Khi nâng cấp hàm đánh giá tĩnh của engine cờ vua từ các tham số tĩnh (Material + Piece-Square Tables) lên độ chính xác cấp cao của NNUE.\n- Khi engine bị suy giảm tốc độ duyệt nút (NPS) do tính toán lại toàn bộ mạng từ đầu ở mỗi thế cờ thay vì cập nhật vi sai.\n- Khi cần nạp và kiểm tra tính toàn vẹn của tệp trọng số nhị phân (`.nnue`) đi kèm engine.",
        "when_not_use": "- Khi biên dịch engine cho các vi điều khiển nhúng 8-bit/16-bit không có hỗ trợ số học vector SIMD.\n- Khi nghiên cứu các thuật toán tìm kiếm thuần túy mà không muốn bị ảnh hưởng bởi độ phức tạp của mạng nơ-ron.",
        "prereqs": "- **Tập lệnh phần cứng:** CPU hỗ trợ SIMD (x86 AVX2/AVX-512 hoặc ARM Neon).\n- **Tệp trọng số:** Tệp mạng nơ-ron nhị phân `.nnue` tương thích kiến trúc HalfKP hoặc HalfKAv2.",
        "concepts": "- **HalfKP / HalfKAv2 Architecture:** Kiến trúc mạng nơ-ron cờ vua kinh điển ánh xạ vị trí Vua phe mình và các quân cờ khác trên bàn cờ vào một lớp đặc trưng thưa (Sparse Feature Transformer Layer).\n- **Incremental Accumulator Update:** Khi một quân cờ di chuyển từ ô A đến ô B, chỉ cần trừ đi các trọng số của ô A và cộng thêm trọng số của ô B vào Accumulator của lớp ẩn đầu tiên thay vì tính lại 40,960 trọng số.\n- **Clipped ReLU (CReLU):** Hàm kích hoạt được lượng tử hóa trong khoảng `[0, 127]` hoặc `[0, 255]`, dễ dàng tính toán siêu nhanh bằng lệnh bão hòa SIMD.",
        "workflow": "1. Định nghĩa cấu trúc file nhị phân NNUE: Magic Header, Version, Feature Transformer Weights, Output Layer Weights.\n2. Cài đặt cấu trúc `Accumulator` lưu trữ 2 vector (trắng và đen) kích thước 512 hoặc 1024 số nguyên 16-bit.\n3. Viết hàm cập nhật vi sai trong hàm `make_move()`: sao chép Accumulator của nút cha và thêm/bớt các đặc trưng di chuyển.\n4. Cài đặt các hàm nhân ma trận và kích hoạt CReLU sử dụng nội tại hàm SIMD (`_mm256_add_epi16`, `_mm256_madd_epi16`).\n5. Tính toán điểm đánh giá cuối cùng từ lớp đầu ra và nhân với hệ số tỉ lệ centipawn.\n6. Kiểm tra chéo điểm số sinh ra từ đường cập nhật vi sai so với đường tính toán từ đầu (Refresh Accumulator) để khẳng định không bị trôi số học.",
        "examples": """### Cap nhat vi sai Accumulator va tinh toan CReLU SIMD AVX2 trong C++:
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
```""",
        "antipatterns": "- **Accumulator Drift Accumulation:** Dùng phép cộng trừ dấu chấm động (floating-point) khiến sai số tích lũy dần theo các ply; bắt buộc phải sử dụng số nguyên chuẩn (`int16_t`).\n- **Full Forward Pass Every Node:** Tính toán lại toàn bộ lớp biến đổi đặc trưng từ đầu ở mọi nút tìm kiếm khiến tốc độ engine bị sụt giảm hơn 90%.\n- **Unaligned Memory Access:** Không sử dụng thuộc tính căn chỉnh biên địa chỉ `alignas(64)` cho các mảng vector SIMD dẫn đến việc vi phạm chỉ thị `_mm256_load_si256` và gây sập chương trình (SIGSEGV).",
        "gates": "- **QG-01**: Điểm số sinh ra từ cập nhật vi sai (Incremental) khớp 100% với điểm tính toán từ đầu (Full Refresh) trên 10,000 thế cờ ngẫu nhiên.\n- **QG-02**: Tốc độ đánh giá đạt tối thiểu 2.5 triệu lượt đánh giá/giây trên một luồng CPU x86-64 hỗ trợ AVX2.\n- **QG-03**: Tệp trọng số nhị phân có cơ chế kiểm tra mã băm SHA-256 trước khi nạp vào bộ nhớ.",
        "security": "- Xác thực kích thước và cấu trúc tệp mạng nơ-ron trước khi phân tích; từ chối các tệp `.nnue` bị hỏng hoặc cố tình tạo buffer overflow.",
        "adapters": "- **Runtimes**: C++20 AVX2/AVX-512/Neon, Rust, PyTorch (training exporter), Stockfish nnue-probe.",
        "deliverables": "- Lớp đánh giá nơ-ron (`nnue_eval.cpp` / `nnue.rs`).\n- Kịch bản kiểm thử tính đúng đắn vi sai của Accumulator (`test_accumulator_drift.py`).",
        "related": "dex-chess-search-pruning-evals, dex-native-simd-dispatch, dex-chess-engine-match-statistics",
        "usage": "```bash\n# Nạp và kiểm định tệp mạng NNUE trong engine\n./chess_engine uci\nsetoption name EvalFile value nn-123456789abc.nnue\nisready\n```"
    },
    {
        "id": "dex-chess-uci-protocol-compliance",
        "name": "dex-chess-uci-protocol-compliance",
        "desc": "Implement, test, and verify complete Universal Chess Interface (UCI) protocol compliance. Handle asynchronous commands, stop/ponder mechanics, option schemas, and engine state machines.",
        "purpose": "Thiết kế, kiểm thử và chứng minh tính tuân thủ tuyệt đối chuẩn giao thức quốc tế Universal Chess Interface (UCI); điều phối máy trạng thái bất đồng bộ của engine cờ vua (Asynchronous Engine State Machine); xử lý mượt mà các luồng lệnh `uci`, `isready`, `ucinewgame`, `position`, `go`, `stop`, `ponderhit` và `quit`; bảo đảm engine tương thích hoàn hảo với các phần mềm giao diện thi đấu hàng đầu (Cutechess, Fritz, Arena, Lichess Bots).",
        "when_use": "- Khi xuất bản engine cờ vua ra cộng đồng hoặc kết nối vào các hệ thống giải đấu tự động (TCEC, CCC, Lichess Bot).\n- Khi engine bị treo (deadlock), bỏ qua lệnh `stop` từ GUI, hoặc xuất ra các chuỗi thông tin tìm kiếm (PV lines) sai cú pháp.\n- Khi thiết lập hệ thống tùy chỉnh tham số engine (`setoption name ... value ...`) cho Hash, Threads, MultiPV.",
        "when_not_use": "- Khi phát triển engine sử dụng giao thức cũ WinBoard/XBoard (trừ khi xây dựng adapter chuyển đổi giao thức).\n- Khi kiểm thử nội bộ các hàm thuật toán không liên quan đến tầng giao tiếp vào/ra (I/O).",
        "prereqs": "- **Luồng giao tiếp:** Tiêu chuẩn Standard I/O (stdin/stdout) hoạt động trên tiến trình độc lập không có buffer trễ.\n- **Harness kiểm thử:** Công cụ `cutechess-cli` hoặc script Python giả lập GUI kiểm thử giao thức.",
        "concepts": "- **UCI Asynchronous Command Loop:** Luồng I/O độc lập đọc các lệnh từ stdin trong khi luồng tìm kiếm (Search Worker Thread) đang duyệt cây tính toán.\n- **Pondering:** Trạng thái engine suy nghĩ tính toán trước nước đi trong thời gian đối phương đang suy nghĩ (`go ponder`).\n- **UCI Info String Format:** Cú pháp chuẩn xuất thông tin đánh giá: `info depth 14 seldepth 20 score cp 45 nodes 125000 nps 1500000 time 83 pv e2e4 e7e5 g1f3`.",
        "workflow": "1. Khởi tạo luồng lắng nghe `stdin` không chặn (Non-blocking I/O hoặc Background Reader Thread).\n2. Khi nhận lệnh `uci`, xuất ra thông tin tác giả, các tùy chọn `option name ... type ...` và kết thúc bằng `uciok`.\n3. Khi nhận lệnh `isready`, đồng bộ hóa bộ nhớ và xuất ra `readyok`.\n4. Phân tích lệnh `position [fen <fenstring> | startpos] moves <move1> ... <moveN>` và cập nhật trạng thái bàn cờ.\n5. Xử lý lệnh `go`: phân bổ thời gian tính toán dựa trên `wtime`, `btime`, `winc`, `binc` hoặc `movetime`.\n6. Khi nhận lệnh `stop`, gửi tín hiệu hủy (`std::atomic<bool> stop_flag = true`), chờ luồng tìm kiếm kết thúc và in ra `bestmove <move>`.",
        "examples": """### Vong lap xu ly lenh UCI bat dong bo trong C++20:
```cpp
#include <iostream>
#include <string>
#include <sstream>
#include <thread>
#include <atomic>

std::atomic<bool> is_searching{false};
std::atomic<bool> stop_search{false};
std::thread search_thread;

void handle_uci() {
    std::cout << "id name DEX-ChessEngine 9.0\\n";
    std::cout << "id author Principal DEX Agent\\n";
    std::cout << "option name Hash type spin default 64 min 1 max 32768\\n";
    std::cout << "option name Threads type spin default 1 min 1 max 256\\n";
    std::cout << "uciok" << std::endl;
}

void uci_loop() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);
        std::string token;
        iss >> token;

        if (token == "uci") {
            handle_uci();
        } else if (token == "isready") {
            std::cout << "readyok" << std::endl;
        } else if (token == "ucinewgame") {
            // Reset Transposition Table va lich su
        } else if (token == "position") {
            // Parse FEN va moves
        } else if (token == "go") {
            stop_search = false;
            is_searching = true;
            if (search_thread.joinable()) search_thread.join();
            search_thread = std::thread([]() {
                // Thuc hien tim kiem tren worker thread
                std::cout << "bestmove e2e4" << std::endl;
                is_searching = false;
            });
        } else if (token == "stop") {
            stop_search = true;
            if (search_thread.joinable()) search_thread.join();
        } else if (token == "quit") {
            stop_search = true;
            if (search_thread.joinable()) search_thread.join();
            break;
        }
    }
}
```""",
        "antipatterns": "- **Blocking Stdin on Search:** Đọc stdin trên cùng luồng tìm kiếm khiến engine không thể nhận được lệnh `stop` khi đang tính toán độ sâu lớn.\n- **Missing Flushing of Stdout:** Quên gọi `std::endl` hoặc `fflush(stdout)` khiến các thông điệp `readyok` hoặc `bestmove` bị nghẽn trong bộ đệm hệ thống.\n- **Printing Unformatted Debug Output:** Xuất các dòng text debug linh tinh không theo cú pháp `info string ...` làm sập trình phân tích cú pháp của GUI.",
        "gates": "- **QG-01**: Vượt qua 100% các bài kiểm tra giao thức của bộ test `cutechess-cli` mà không có lỗi timeout.\n- **QG-02**: Engine phản hồi lệnh `stop` và in ra `bestmove` trong vòng tối đa 20ms.\n- **QG-03**: Toàn bộ chuỗi xuất thông tin đều tuân thủ chính xác đặc tả UCI Specification.",
        "security": "- Giới hạn độ dài tối đa của dòng lệnh đầu vào từ stdin (tối đa 4096 ký tự) ngăn ngừa lỗi tràn bộ đệm chuỗi.",
        "adapters": "- **Runtimes**: C++20, Rust, Cutechess-cli, Python python-chess library, Arena Chess GUI.",
        "deliverables": "- Mô-đun phân tích giao thức UCI (`uci.cpp` / `uci.rs`).\n- Kịch bản kiểm thử bắt tay giao thức UCI tự động (`test_uci_handshake.py`).",
        "related": "dex-chess-search-pruning-evals, dex-chess-transposition-table-correctness, dex-chess-engine-match-statistics",
        "usage": "```bash\n# Kiem thu tinh tuong thich UCI bang cutechess-cli\ncutechess-cli -engine cmd=./my_engine name=MyEngine -each tc=10+0.1 -rounds 2\n```"
    },
    {
        "id": "dex-chess-opening-book-validation",
        "name": "dex-chess-opening-book-validation",
        "desc": "Validate, inspect, and benchmark chess opening book formats (Polyglot .bin, CTG, PGN opening trees). Verify move legality, weight distributions, and transposition coverage.",
        "purpose": "Kiểm định, phân tích và đo lường chất lượng của sách khai cuộc cờ vua (Chess Opening Books); xác thực cấu trúc nhị phân của định dạng Polyglot (`.bin`), cây khai cuộc PGN và sách CTG; kiểm tra tính hợp lệ của các nước đi, phân phối trọng số nước cờ (Move Weighting & Randomization), và bảo đảm độ phủ các nhánh hoán vị khai cuộc chính tắc.",
        "when_use": "- Khi tạo mới hoặc nhập khẩu sách khai cuộc Polyglot cho engine cờ vua thi đấu.\n- Khi engine bị mắc bẫy khai cuộc đã biết hoặc chọn phải các biến yếu do trọng số trong sách bị gán nhãn sai.\n- Khi cần xuất các ván đấu PGN lớn thành tệp nhị phân mở sách nhỏ gọn tối ưu hóa tốc độ nạp.",
        "when_not_use": "- Khi cấu hình engine thi đấu ở giải đấu không cho phép sử dụng sách khai cuộc (No-book conditions).\n- Khi kiểm thử năng lực tự tìm kiếm thuần túy của thuật toán tìm kiếm và đánh giá.",
        "prereqs": "- **Tệp sách nhị phân:** Tệp Polyglot `.bin` hoặc cơ sở dữ liệu PGN chứa các ván cờ kiện tướng (Master games).\n- **Công cụ phân tích:** Python `chess.polyglot` hoặc công cụ dòng lệnh `polyglot` CLI.",
        "concepts": "- **Polyglot Zobrist Hash:** Chuẩn băm Zobrist 64-bit đặc thù của định dạng Polyglot (có bảng số ngẫu nhiên khác với Stockfish), bao gồm cả xử lý mốc bắt tốt qua đường chỉ khi có thể bắt thực tế.\n- **Weight-Proportional Selection:** Thuật toán chọn nước đi ngẫu nhiên có trọng số: xác suất chọn một nước cờ tỷ lệ thuận với điểm trọng số `weight` của nó trong tệp `.bin`.\n- **Book Transposition Coverage:** Khả năng nhận diện cùng một thế cờ khai cuộc đạt được thông qua các thứ tự đi quân khác nhau (ví dụ: transposition giữa Khai cuộc Anh và Gambit Hậu).",
        "workflow": "1. Đọc và phân tích các bản ghi 16-byte trong tệp Polyglot `.bin`: `key` (8 byte), `move` (2 byte), `weight` (2 byte), `learn` (4 byte).\n2. Kiểm tra tính sắp xếp tăng dần đơn điệu của các khóa `key` trong tệp nhị phân để hỗ trợ tìm kiếm nhị phân $O(\log N)$.\n3. Giải mã mã nước đi 16-bit thành tọa độ ô cờ (from_square, to_square, promotion_piece).\n4. Đối soát nước đi với bộ sinh nước đi chuẩn để khẳng định 100% nước đi trong sách đều hoàn toàn hợp lệ (Legal Move).\n5. Kiểm tra tính đa dạng của các phương án: không để một nhánh khai cuộc chỉ có duy nhất 1 nước đi đơn điệu nếu thế cờ có nhiều biến hay.\n6. Chạy kịch bản tra cứu thử nghiệm trên 1,000 thế cờ khai cuộc phổ biến và đo thời gian truy xuất.",
        "examples": """### Script Python doc va kiem dinh tinh hop le cua sach Polyglot .bin:
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
```""",
        "antipatterns": "- **Unsorted Binary Book Entries:** Lưu các bản ghi không theo thứ tự khóa tăng dần khiến thuật toán Binary Search không thể tìm thấy nước đi và coi như hết sách.\n- **Including Blunder Moves:** Nhập các ván cờ nghiệp dư có nước đi sai lầm vào sách mà không lọc Elo khiến engine chọn phải nước cờ yếu.\n- **Zero-Weight Default Traps:** Đặt trọng số bằng 0 cho tất cả các nước đi khiến thuật toán chọn ngẫu nhiên không thể kích hoạt.",
        "gates": "- **QG-01**: 100% các khóa trong tệp `.bin` được sắp xếp tăng dần nghiêm ngặt.\n- **QG-02**: Mọi nước đi trong sách đều là nước cờ hợp lệ 100% theo luật cờ vua quốc tế FIDE.\n- **QG-03**: Tốc độ tra cứu nhị phân đạt dưới 5 micro-giây cho một thế cờ.",
        "security": "- Kiểm tra kích thước tệp và giới hạn số lượng mục nhập trước khi cấp phát bộ nhớ đọc vào RAM.",
        "adapters": "- **Runtimes**: Python python-chess, C++ Polyglot Reader, Cutechess-cli.",
        "deliverables": "- Kịch bản kiểm định và làm sạch sách khai cuộc (`validate_polyglot.py`).\n- Báo cáo phân tích độ phủ và phân phối trọng số khai cuộc.",
        "related": "dex-chess-legal-movegen-perft, dex-chess-uci-protocol-compliance, dex-chess-engine-match-statistics",
        "usage": "```bash\n# Trich xuat va kiem tra sach khai cuoc tu PGN bang cong cu polyglot\npolyglot make-book -pgn games.pgn -bin output.bin -max-fl 20\n```"
    },
    {
        "id": "dex-chess-endgame-tablebase-integration",
        "name": "dex-chess-endgame-tablebase-integration",
        "desc": "Integrate and verify Syzygy and Nalimov endgame tablebase probing in chess engines. Validate WDL and DTZ semantics, root probing, and safe missing-file fallback.",
        "purpose": "Tích hợp và kiểm chứng cơ chế tra cứu cơ sở dữ liệu cờ tàn hoàn hảo (Endgame Tablebases: Syzygy WDL và DTZ); xác thực ngữ nghĩa của kết quả Thắng/Hòa/Thua (Win/Draw/Loss - WDL) và khoảng cách tới nước đi hoàn lại 50 nước (Distance to Zeroing - DTZ); tối ưu hóa tra cứu tại nút gốc (Root Probing) và trong cây tìm kiếm (Search Probing); bảo đảm khả năng phục hồi an toàn khi thiếu tệp dữ liệu mà không làm sập engine.",
        "when_use": "- Khi thế cờ rút gọn về số lượng quân cờ nhỏ (3-4-5-6 hoặc 7 quân trên bàn cờ).\n- Khi engine cần tìm ra nước đi duy nhất để thủ hòa hoặc dứt điểm chiến thắng tuyệt đối trong tàn cuộc phức tạp.\n- Khi cấu hình đường dẫn `SyzygyPath` trong giao thức UCI kết nối tới thư mục chứa các tệp `.rtbw` và `.rtbz`.",
        "when_not_use": "- Khi bàn cờ còn nhiều quân (>7 quân) vượt quá phạm vi dữ liệu của các bộ Tablebase hiện có.\n- Khi bộ nhớ lưu trữ ổ cứng không cho phép cài đặt các bộ tệp kích thước lớn (Syzygy 6-piece chiếm ~150GB, 7-piece chiếm ~17TB).",
        "prereqs": "- **Dữ liệu cờ tàn:** Thư mục chứa các tệp Syzygy Tablebase 3-4-5 quân (`.rtbw` và `.rtbz`).\n- **Thư viện tích hợp:** Thư viện C/C++ Fathom hoặc module tra cứu nhị phân tích hợp trong engine.",
        "concepts": "- **Syzygy WDL (.rtbw):** Bảng dữ liệu tra cứu nhanh kết quả thế cờ (Thắng, Hòa, Thua, Thắng nhưng bị chặn bởi luật 50 nước, Hòa do luật 50 nước), dùng chủ yếu trong quá trình duyệt cây tìm kiếm.\n- **Syzygy DTZ (.rtbz):** Bảng dữ liệu xác định số nước đi chính xác cho đến khi có một quân tốt di chuyển hoặc một quân cờ bị bắt (zeroing move), dùng tại nút gốc để bảo đảm không bị xử hòa 50 nước.\n- **50-Move Rule Compliance:** Nguy cơ thế cờ thắng về lý thuyết nhưng bị xử hòa thực tế do không thể ăn quân hoặc đi tốt trong vòng 50 nước đi liên tiếp.",
        "workflow": "1. Khởi tạo đường dẫn thư mục Tablebase thông qua tùy chọn UCI `setoption name SyzygyPath value /path/to/syzygy`.\n2. Nạp các bảng băm nhận diện tệp Syzygy WDL (`.rtbw`) và DTZ (`.rtbz`) có sẵn trên ổ cứng.\n3. Tại nút gốc (Root Node): nếu số lượng quân cờ <= giới hạn Tablebase, thực hiện `probe_root()` để chọn ngay nước cờ DTZ tối ưu.\n4. Trong cây tìm kiếm (Search Tree): tại các nút có số lượng quân phù hợp, gọi `probe_wdl()`; nếu kết quả trả về là Thua, trả về giá trị fail-low; nếu Thắng, trả về giá trị fail-high để cắt tỉa toàn bộ cây con phía dưới.\n5. Bọc các cuộc gọi I/O đọc tệp trong cơ chế phòng vệ ngoại lệ, tự động chuyển về hàm tìm kiếm thông thường nếu tệp bị lỗi hoặc không tìm thấy.\n6. Chạy bộ kiểm thử 50 vị trí tàn cuộc kinh điển (KPK, KBNK, KQKR) để khẳng định tính chính xác tuyệt đối.",
        "examples": """### Tich hop tra cuu Syzygy WDL trong ham tim kiem C++ bang Fathom library:
```cpp
#include "fathom/tbprobe.h"

// Khoi tao duong dan Syzygy khi nhan lenh UCI
void init_tablebases(const std::string& path) {
    tb_init(path.c_str());
    std::cout << "info string Syzygy Tablebases initialized. Max pieces: " << TB_LARGEST << std::endl;
}

int probe_tablebase_wdl(const Board& board, int depth, int alpha, int beta) {
    if (board.piece_count() > TB_LARGEST || board.has_castling_rights()) {
        return -1; // Khong the probe
    }

    // Tra cuu Fathom WDL: 0=Loss, 1=Blessed Loss, 2=Draw, 3=Cursed Win, 4=Win
    unsigned res = tb_probe_wdl(
        board.white_pieces(), board.black_pieces(),
        board.kings(), board.queens(), board.rooks(),
        board.bishops(), board.knights(), board.pawns(),
        board.halfmove_clock(), 0, board.ep_square(),
        board.turn() == WHITE
    );

    if (res == TB_RESULT_FAILED) return -1;

    int score = 0;
    if (res == TB_WIN) score = 20000;
    else if (res == TB_LOSS) score = -20000;
    else score = 0; // Draw, Blessed Loss, Cursed Win

    return score;
}
```""",
        "antipatterns": "- **Crashing on Missing Syzygy Files:** Cố tình truy cập mảng con mà không kiểm tra cờ tồn tại của tệp, khiến engine bị crash khi gặp vị trí 6 quân mà chỉ có bộ tệp 5 quân.\n- **Ignoring 50-Move Counter in Tablebase:** Bỏ qua bộ đếm `halfmove_clock` khi đọc WDL khiến engine chọn phương án dẫn đến hòa cờ 50 nước trong thế cờ thắng.\n- **Probing DTZ at Every Tree Node:** Gọi hàm DTZ đắt đỏ ở sâu trong cây tìm kiếm thay vì chỉ dùng WDL gọn nhẹ làm sụt giảm tốc độ duyệt nút nghiêm trọng.",
        "gates": "- **QG-01**: Nhận diện chính xác 100% kết quả WDL trên tất cả các vị trí tàn cuộc 3, 4, 5 quân có trong thư mục.\n- **QG-02**: Không bao giờ gây ra hiện tượng sập engine (crash-safe) khi truy cập các vị trí chưa có tệp tablebase tương ứng.\n- **QG-03**: Nước đi tại nút gốc luôn tuân thủ luật 50 nước (Zeroing move trước khi vượt quá 100 ply).",
        "security": "- Sử dụng cơ chế ánh xạ bộ nhớ tệp an toàn (Memory-mapped file / mmap) có giới hạn bảo vệ đọc (read-only) để tránh làm hỏng dữ liệu trên đĩa.",
        "adapters": "- **Runtimes**: C++20, Rust, Fathom Syzygy Prober, Stockfish syzygy module.",
        "deliverables": "- Mô-đun tích hợp Tablebase (`syzygy_adapter.cpp` / `syzygy.rs`).\n- Bộ kiểm thử tự động 50 bài toán tàn cuộc chuẩn (`test_endgame_tablebases.py`).",
        "related": "dex-chess-search-pruning-evals, dex-chess-uci-protocol-compliance, dex-chess-engine-match-statistics",
        "usage": "```bash\n# Kiem tra tra cuu Syzygy trong vi tri KBNK bang lenh UCI\n./chess_engine uci\nsetoption name SyzygyPath value /data/syzygy\nposition fen 8/8/8/8/8/5k2/4N3/4K2B w - - 0 1\ngo depth 1\n```"
    },
    {
        "id": "dex-cpp-rust-ffi-validation",
        "name": "dex-cpp-rust-ffi-validation",
        "desc": "Verify, test, and audit Foreign Function Interface (FFI) contracts between C++ and Rust. Validate memory layout alignment, ownership transfers, exception/panic firewalls, and sanitize with ASan/Miri.",
        "purpose": "Kiểm chứng, kiểm toán an toàn và tối ưu hóa ranh giới tương tác liên ngôn ngữ (FFI - Foreign Function Interface) giữa C++ (C++20/C++23) và Rust; xác thực tính tương thích của bố cục bộ nhớ (`#[repr(C)]` vs `struct layout`), quyền sở hữu và chuyển giao con trỏ (Ownership & Lifetimes), cơ chế bắt ngoại lệ ngăn chặn Panic tràn qua ranh giới C-ABI (Panic Firewall), và kiểm thử tự động với AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan) và Miri.",
        "when_use": "- Khi tích hợp các thư viện hiệu năng cao bằng C++ (như engine cờ vua, codec media, SIMD math) vào ứng dụng quản lý an toàn bằng Rust.\n- Khi phát hiện các lỗi rò rỉ bộ nhớ bí ẩn (Memory Leaks), vi phạm vùng nhớ (Segfault) hoặc hỏng dữ liệu heap (Heap Corruption) tại tầng FFI.\n- Khi định nghĩa các hàm trao đổi chuỗi ký tự UTF-8, mảng cắt lát (slices), hoặc đối tượng gọi ngược (callbacks) giữa hai ngôn ngữ.",
        "when_not_use": "- Khi hai dịch vụ giao tiếp với nhau qua mạng thông qua gRPC, REST hoặc Message Queue (IPC/RPC).\n- Khi chương trình chỉ được viết hoàn toàn bằng một ngôn ngữ duy nhất mà không có thành phần native đa ngôn ngữ.",
        "prereqs": "- **Trình biên dịch:** Rust 1.75+ (Cargo), Clang/GCC hỗ trợ C++20.\n- **Công cụ hỗ trợ:** `cxx`, `bindgen`, AddressSanitizer (`-fsanitize=address`), và Miri.",
        "concepts": "- **#[repr(C)] Layout Alignment:** Thuộc tính bắt buộc trên các cấu trúc dữ liệu Rust để bảo đảm các trường dữ liệu được sắp xếp và đệm kích thước theo chuẩn ABI của C/C++.\n- **Panic Firewall (catch_unwind):** Vùng đệm bắt toàn bộ panic trong Rust trước khi trả về C++, vì việc để một Rust panic lan truyền sang ngăn xếp C++ là hành vi Undefined Behavior (UB).\n- **Opaque Pointers & Box Leak/From_raw:** Kỹ thuật chuyển giao quyền sở hữu con trỏ an toàn qua ranh giới FFI bằng cách cấp phát `Box::into_raw` và thu hồi bằng `Box::from_raw`.",
        "workflow": "1. Khai báo các kiểu dữ liệu dùng chung với thuộc tính `#[repr(C)]` trong Rust và `struct` tương ứng trong C++.\n2. Sử dụng thư viện `cxx` hoặc `bindgen` để sinh ra các hàm bao an toàn (Safe Wrapper Bridges).\n3. Thiết lập Panic Firewall cho tất cả các hàm `extern \"C\"` phía Rust bằng `std::panic::catch_unwind`.\n4. Định nghĩa rõ ràng quy ước giải phóng bộ nhớ: bên nào cấp phát (allocate) thì bên đó chịu trách nhiệm giải phóng (deallocate).\n5. Biên dịch toàn bộ dự án với cờ AddressSanitizer (`-fsanitize=address`) trên Clang và `RUSTFLAGS=\"-Zsanitizer=address\"`.\n6. Chạy bộ kiểm thử FFI tự động kiểm tra ranh giới dữ liệu và khẳng định 0 lỗi bộ nhớ rò rỉ.",
        "examples": """### Cau truc FFI an toan giua Rust va C++ co Panic Firewall va Repr(C):
```rust
// Rust implementation (lib.rs)
use std::ffi::{c_char, c_int, CStr};
use std::panic::catch_unwind;

#[repr(C)]
pub struct EngineMetrics {
    pub nodes_searched: u64,
    pub nps: u32,
    pub depth: u8,
}

#[no_mangle]
pub extern "C" fn rust_compute_eval(fen: *const c_char, out_metrics: *mut EngineMetrics) -> c_int {
    // Panic Firewall: Ngan khong cho panic thoat ra C ABI
    let result = catch_unwind(|| {
        if fen.is_null() || out_metrics.is_null() {
            return -1; // Loi con tro null
        }
        let c_str = unsafe { CStr::from_ptr(fen) };
        let fen_str = match c_str.to_str() {
            Ok(s) => s,
            Err(_) => return -2, // Loi ma hoa UTF-8
        };

        // Gia lap tinh toan an toan
        unsafe {
            (*out_metrics).nodes_searched = 1_500_000;
            (*out_metrics).nps = 2_500_000;
            (*out_metrics).depth = 18;
        }
        0 // Thanh cong
    });

    result.unwrap_or(-99) // Tra ma loi neu xay ra panic
}
```

```cpp
// C++ consumer (main.cpp)
#include <iostream>
#include <cstdint>

extern "C" {
    struct EngineMetrics {
        uint64_t nodes_searched;
        uint32_t nps;
        uint8_t depth;
    };

    int rust_compute_eval(const char* fen, EngineMetrics* out_metrics);
}

int main() {
    EngineMetrics metrics{};
    int status = rust_compute_eval("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", &metrics);
    if (status == 0) {
        std::cout << "Success! Depth: " << (int)metrics.depth << ", NPS: " << metrics.nps << "\\n";
    }
    return status;
}
```""",
        "antipatterns": "- **Uncaught Panic over FFI Boundary:** Để xảy ra `panic!` bên trong hàm `extern \"C\"` làm sập toàn bộ tiến trình hoặc làm rách nát stack frame của C++.\n- **Mismatched Allocator Deallocation:** Cấp phát bộ nhớ bằng `malloc` trong C++ nhưng lại giải phóng bằng `Box::from_raw` trong Rust (hoặc ngược lại) gây sập Heap Manager.\n- **Passing Raw Non-repr(C) Structs:** Truyền các cấu trúc dữ liệu Rust mặc định (không có `#[repr(C)]`) sang C++ dẫn đến việc đọc sai lệch offset dữ liệu do trình biên dịch tự ý sắp xếp lại thứ tự trường.",
        "gates": "- **QG-01**: 100% các hàm FFI đều có `catch_unwind` hoặc `noexcept` bảo đảm không phát tán ngoại lệ xuyên biên giới.\n- **QG-02**: Vượt qua bộ kiểm thử kiểm tra bộ nhớ AddressSanitizer (ASan) với 0 byte memory leak.\n- **QG-03**: Kích thước và căn chỉnh byte (`sizeof` và `alignof`) của các struct dùng chung khớp nhau 100% giữa C++ và Rust.",
        "security": "- Luôn kiểm tra con trỏ `null` và tính hợp lệ của chuỗi ký tự UTF-8 trước khi thực hiện các thao tác trong khối `unsafe`.",
        "adapters": "- **Runtimes**: C++20 (Clang/GCC), Rust 2021 (Cargo), cxx crate, bindgen, LLVM ASan/UBSan.",
        "deliverables": "- Tệp tiêu đề C-ABI dùng chung (`engine_bridge.h` / `bridge.rs`).\n- Bộ kiểm thử tự động kiểm tra tính an toàn bộ nhớ FFI (`test_ffi_sanitizers.sh`).",
        "related": "dex-chess-legal-movegen-perft, dex-native-simd-dispatch, dex-chess-nnue-evaluation-integration",
        "usage": "```bash\n# Chay kiem thu FFI co bat AddressSanitizer\nclang++ -fsanitize=address -std=c++20 main.cpp -L./target/debug -lengine_rust -o ffi_test && ./ffi_test\n```"
    },
    {
        "id": "dex-native-simd-dispatch",
        "name": "dex-native-simd-dispatch",
        "desc": "Detect, benchmark, and implement portable runtime SIMD CPU dispatch (AVX2, AVX-512, ARM Neon). Ensure robust scalar fallbacks, vector alignment, and multiversioned execution paths.",
        "purpose": "Thiết kế và triển khai cơ chế điều phối lệnh vector hóa thời gian thực (Portable Runtime SIMD Dispatch); tự động nhận diện tập lệnh phần cứng của CPU (x86-64 AVX2, AVX-512, SSE4.2 và ARM64 Neon); xây dựng cơ chế phân nhánh đa phiên bản (Function Multiversioning / Dynamic Function Pointer Dispatch) và duy trì đường dự phòng vô hướng (Scalar Fallback) đảm bảo tính tương thích phần mềm 100% trên mọi kiến trúc CPU.",
        "when_use": "- Khi viết các thuật toán tính toán ma trận, xử lý tín hiệu âm thanh/hình ảnh hoặc hàm đánh giá NNUE đòi hỏi băng thông tính toán cực đại.\n- Khi phần mềm được phân phối dưới dạng tệp nhị phân duy nhất (Universal Binary) nhưng phải chạy tối ưu trên cả máy tính đời mới lẫn máy tính đời cũ.\n- Khi gặp lỗi sập chương trình với mã `SIGILL` (Illegal Instruction) trên các máy tính người dùng không có tập lệnh AVX2.",
        "when_not_use": "- Khi khối lượng tính toán là các tác vụ I/O mạng hoặc truy vấn cơ sở dữ liệu bị nghẽn bởi tốc độ đọc ghi đĩa.\n- Khi trình biên dịch tự động vector hóa (Auto-vectorization) đã đạt hiệu quả tối ưu mà không cần can thiệp mã lắp ráp nội tại (Intrinsics).",
        "prereqs": "- **Trình biên dịch:** Hỗ trợ C++20/Rust và các hàm nội tại SIMD (`<immintrin.h>` hoặc `core::arch`).\n- **Môi trường đo kiểm:** CPU hỗ trợ tối thiểu tập lệnh cơ sở SSE4.2 kèm các tập lệnh mở rộng AVX2.",
        "concepts": "- **CPUID Instruction:** Lệnh phần cứng x86 cho phép truy vấn trực tiếp các tính năng được hỗ trợ bởi bộ vi xử lý tại thời điểm khởi động ứng dụng.\n- **Dynamic Function Pointer Dispatch:** Kỹ thuật gán con trỏ hàm toàn cục một lần duy nhất khi khởi động chương trình trỏ tới phiên bản SIMD tối ưu nhất mà CPU hỗ trợ.\n- **Vector Register Alignment:** Yêu cầu địa chỉ bộ nhớ phải là bội số của 16, 32 hoặc 64 byte để nạp dữ liệu bằng các lệnh vector không căn chỉnh (unaligned) hoặc căn chỉnh (aligned) với hiệu năng tối đa.",
        "workflow": "1. Viết hàm kiểm tra CPUID phát hiện cờ hỗ trợ phần cứng: AVX2, FMA, AVX-512F, AVX-512BW, Neon.\n2. Cài đặt thuật toán theo 3 phiên bản độc lập: Phiên bản chuẩn vô hướng (Scalar), phiên bản AVX2 (256-bit), và phiên bản AVX-512 (512-bit).\n3. Định nghĩa con trỏ hàm: `typedef void (*compute_fn)(const float* in, float* out, size_t n);`.\n4. Viết hàm khởi tạo hàm điều phối (Dispatch Resolver) thiết lập con trỏ hàm chính xác trước khi ứng dụng thực thi vòng lặp chính.\n5. Thực hiện đo kiểm hiệu năng (Micro-benchmarking) so sánh tốc độ tăng tốc giữa các phiên bản.\n6. Kiểm chứng đường fallback vô hướng bằng cách giả lập tắt cờ CPUID trong môi trường ảo hóa.",
        "examples": """### Thuat toan Runtime CPU Dispatch cho phep tinh toan Vector tren C++20:
```cpp
#include <iostream>
#include <vector>
#include <immintrin.h>

#if defined(_MSC_VER)
#include <intrin.h>
#else
#include <cpuid.h>
#endif

// 1. Kiem tra CPUID thoi diem runtime
bool cpu_supports_avx2() {
#if defined(_MSC_VER)
    int info[4];
    __cpuidex(info, 7, 0);
    return (info[1] & (1 << 5)) != 0;
#else
    unsigned int eax, ebx, ecx, edx;
    if (__get_cpuid_max(0, nullptr) < 7) return false;
    __cpuid_count(7, 0, eax, ebx, ecx, edx);
    return (ebx & (1 << 5)) != 0;
#endif
}

// 2. Phien ban Scalar Fallback
void dot_product_scalar(const float* a, const float* b, float* result, size_t n) {
    float sum = 0.0f;
    for (size_t i = 0; i < n; ++i) sum += a[i] * b[i];
    *result = sum;
}

// 3. Phien ban AVX2 (256-bit)
void dot_product_avx2(const float* a, const float* b, float* result, size_t n) {
    __m256 sum_vec = _mm256_setzero_ps();
    size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        sum_vec = _mm256_fmadd_ps(va, vb, sum_vec);
    }
    // Horizontal add
    alignas(32) float buffer[8];
    _mm256_store_ps(buffer, sum_vec);
    float total = 0.0f;
    for (int k = 0; k < 8; ++k) total += buffer[k];
    
    // Xu ly phan du con lai
    for (; i < n; ++i) total += a[i] * b[i];
    *result = total;
}

// 4. Function Pointer Dispatch
using DotProductFn = void (*)(const float*, const float*, float*, size_t);

DotProductFn resolve_dot_product() {
    if (cpu_supports_avx2()) {
        std::cout << "[SIMD] Selected AVX2 hardware acceleration.\\n";
        return dot_product_avx2;
    }
    std::cout << "[SIMD] Fallback to Portable Scalar implementation.\\n";
    return dot_product_scalar;
}

DotProductFn dot_product = resolve_dot_product();
```""",
        "antipatterns": "- **Compiling with Global -mavx2 Flag:** Biên dịch toàn bộ dự án với cờ `-mavx2` khiến ngay cả mã khởi động hoặc hàm `main` cũng chứa lệnh AVX2, gây crash lập tức trên CPU cũ trước khi kịp chạy hàm kiểm tra CPUID.\n- **Ignoring Remainder Elements:** Quên xử lý các phần tử thừa ở cuối mảng khi kích thước mảng không chia hết cho kích thước vector (8 đối với AVX, 16 đối với AVX-512).\n- **Misaligned Store Crashes:** Dùng lệnh nạp yêu cầu căn chỉnh `_mm256_load_ps` trên con trỏ bộ nhớ ngẫu nhiên chưa được kiểm tra địa chỉ chia hết cho 32 byte.",
        "gates": "- **QG-01**: Kết quả tính toán giữa phiên bản SIMD và phiên bản Scalar fallback trùng khớp với sai số epsilon < 1e-5.\n- **QG-02**: Ứng dụng khởi động an toàn và chuyển về đường fallback trên môi trường giả lập không có AVX2 (0 lỗi `SIGILL`).\n- **QG-03**: Phiên bản AVX2 đạt tốc độ tăng tốc tối thiểu 3.5x so với phiên bản Scalar trên các tập dữ liệu lớn.",
        "security": "- Ngăn ngừa lỗi đọc vượt biên (Buffer Over-read) ở các phần tử cuối mảng trong các phép toán vector.",
        "adapters": "- **Runtimes**: C++20 (GCC, Clang, MSVC), Rust (std::arch, is_x86_feature_detected!), ARM Neon.",
        "deliverables": "- Thư viện điều phối SIMD đa nền tảng (`simd_dispatch.hpp` / `simd.rs`).\n- Bộ benchmark đo lường thông lượng tính toán giữa các tập lệnh.",
        "related": "dex-chess-nnue-evaluation-integration, dex-cpp-rust-ffi-validation",
        "usage": "```bash\n# Chay benchmark so sanh toc do cac tap lenh SIMD\n./simd_benchmark --iterations 1000000 --size 65536\n```"
    },
    {
        "id": "dex-chess-engine-match-statistics",
        "name": "dex-chess-engine-match-statistics",
        "desc": "Design, orchestrate, and statistically evaluate chess engine matches. Calculate Elo ratings, confidence intervals, SPRT hypothesis tests, and prevent opening book or hardware bias.",
        "purpose": "Thiết kế, điều phối và phân tích thống kê các giải đấu kiểm thử tự động giữa các engine cờ vua (Chess Engine Match Statistics); cài đặt thuật toán kiểm định tỉ số xác suất tuần tự (SPRT - Sequential Probability Ratio Test) để xác nhận các cải tiến mã nguồn; tính toán điểm xếp hạng Elo, khoảng tin cậy 95% (Confidence Intervals), hệ số hòa (Draw Rate) và triệt tiêu các sai lệch do sách khai cuộc hoặc tài nguyên phần cứng bất đối xứng.",
        "when_use": "- Khi quyết định chấp thuận (merge) một cải tiến thuật toán tìm kiếm hoặc hàm đánh giá mới vào nhánh chính của engine.\n- Khi cần chứng minh một thay đổi mã nguồn đem lại mức tăng ít nhất +5 Elo với mức ý nghĩa thống kê cao mà không cần đấu hàng chục nghìn ván không cần thiết.\n- Khi đo lường sức mạnh thi đấu của engine so với các đối thủ trong danh sách xếp hạng tiêu chuẩn (CCRL, CEGT, Lichess).",
        "when_not_use": "- Khi kiểm tra tính đúng đắn chức năng (như test perft sinh nước đi hoặc bắt lỗi cú pháp FEN).\n- Khi số lượng ván đấu quá nhỏ (<50 ván), kết quả hoàn toàn bị chi phối bởi yếu tố ngẫu nhiên và không có giá trị thống kê.",
        "prereqs": "- **Hạ tầng thi đấu:** Cutechess-cli hoặc fastchess chạy trên máy chủ có CPU pinning cố định.\n- **Công cụ thống kê:** Python `scipy`, `ordo`, hoặc thư viện `bayeselo`.",
        "concepts": "- **SPRT (Sequential Probability Ratio Test):** Phương pháp kiểm định giả thuyết của Abraham Wald cho phép dừng trận đấu ngay khi có đủ bằng chứng thống kê chứng minh giả thuyết $H_1$ (Elo gain >= bounds) hoặc $H_0$ (không tăng Elo).\n- **BayesElo / Ordo:** Mô hình thống kê Bayes ước lượng trình độ Elo của nhiều đấu thủ từ kết quả ma trận đối đầu, xử lý tốt các ván hòa.\n- **Opening Book Pairings:** Mỗi cặp khai cuộc được thi đấu 2 ván đảo màu quân (White/Black) giữa hai engine để triệt tiêu lợi thế cầm quân trắng.",
        "workflow": "1. Chuẩn bị tập sách khai cuộc mở rộng gồm các vị trí cân bằng (ví dụ UHO_2022 8-move opening book).\n2. Cấu hình kịch bản thi đấu `cutechess-cli` với kiểm soát thời gian chặt chẽ (ví dụ: 10s + 0.1s increment) và pinning CPU core.\n3. Thiết lập thông số SPRT: `elo0 = 0.0`, `elo1 = 5.0`, `alpha = 0.05`, `beta = 0.05`.\n4. Chạy các ván đấu theo từng cặp đảo màu quân (Gauntlet hoặc Round-Robin).\n5. Cập nhật Log-Likelihood Ratio (LLR) sau mỗi ván đấu hoàn tất; dừng ngay trận đấu khi LLR chạm ngưỡng trên (Pass) hoặc ngưỡng dưới (Fail).\n6. Xuất báo cáo thống kê: Điểm số, Thắng/Hòa/Thua, Elo chênh lệch, Lỗi sai số ±Error, và phân tích các ván thua để tìm bug chiến thuật.",
        "examples": """### Kich ban thi dau tu dong SPRT giua ban thu nghiem va ban goc bang Cutechess-cli:
```bash
# Dieu phoi tran dau SPRT 2 engine voi cuon sach UHO, dao mau quan moi round
cutechess-cli \\
  -engine cmd=./engine_dev name=DEX_Dev \\
  -engine cmd=./engine_base name=DEX_Base \\
  -each proto=uci tc=10+0.1 timemargin=50 hash=64 \\
  -openings file=openings/uho_2024.epd format=epd order=random plies=16 \\
  -repeat \\
  -sprt elo0=0 elo1=5 alpha=0.05 beta=0.05 \\
  -concurrency 4 \\
  -draw movenumber=40 movecount=8 score=10 \\
  -resign movecount=3 score=600 \\
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
```""",
        "antipatterns": "- **Ignoring Color Inversion:** Chỉ cho engine thử nghiệm cầm quân Trắng dẫn đến ảo giác tăng Elo do lợi thế đi trước tự nhiên của cờ vua.\n- **Uncontrolled CPU Throttling:** Chạy giải đấu trên máy tính cá nhân đang chạy các tác vụ nặng khác khiến một bên bị rớt thời gian (Time forfeit) do nghẽn CPU.\n- **Early Stop Bias:** Dừng trận đấu thủ công khi thấy kết quả tạm thời đang có lợi mà không tuân thủ các ngưỡng toán học của SPRT.",
        "gates": "- **QG-01**: Mọi trận đấu đối kháng bắt buộc phải sử dụng chế độ thi đấu đảo màu quân theo cặp (Round-paired play).\n- **QG-02**: Thử nghiệm SPRT chỉ được chấp thuận (Pass) khi LLR chạm ngưỡng trên với độ tin cậy thống kê >= 95%.\n- **QG-03**: Tỷ lệ thua do hết thời gian (Time loss) của engine dưới 0.1% tổng số ván thi đấu.",
        "security": "- Giới hạn số lượng luồng và dung lượng RAM của các tiến trình engine thi đấu; cô lập môi trường sandbox không cho engine ghi đè file hệ thống.",
        "adapters": "- **Runtimes**: Cutechess-cli, fastchess, Ordo, BayesElo, Python scipy.",
        "deliverables": "- Kịch bản điều phối giải đấu SPRT tự động (`run_sprt_match.sh`).\n- Báo cáo phân tích thống kê Elo và tệp biên bản thi đấu PGN (`tournament_summary.md`).",
        "related": "dex-chess-search-pruning-evals, dex-chess-uci-protocol-compliance, dex-chess-nnue-evaluation-integration",
        "usage": "```bash\n# Tinh toan bang xep hang Elo bang cong cu ordo\nordo -p matches_output.pgn -a 0 -A \"DEX_Base\" -W -D -c -j ordo_report.txt\n```"
    }
]

def generate_skills():
    total = len(SKILLS_AQ_AR)
    created = 0
    print("=== GENERATING GROUP AQ & AR (Skills 421–440) ===")

    for idx, skill in enumerate(SKILLS_AQ_AR, 1):
        skill_id = skill["id"]
        skill_dir = os.path.join(SKILLS_DIR, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        file_path = os.path.join(skill_dir, "SKILL.md")

        content = f"""---
name: {skill["name"]}
description: {skill["desc"]}
---

# {skill["id"]}

## 1. Purpose & Scope
{skill["purpose"]}

## 2. When to Use
{skill["when_use"]}

## 3. When NOT to Use
{skill["when_not_use"]}

## 4. Prerequisites & Input Context
{skill["prereqs"]}

## 5. Core Concepts & Taxonomy
{skill["concepts"]}

## 6. Step-by-Step Execution Workflow
{skill["workflow"]}

## 7. Concrete Examples
{skill["examples"]}

## 8. Anti-Patterns & Common Traps
{skill["antipatterns"]}

## 9. Quality Gates & Acceptance Criteria
{skill["gates"]}

## 10. Security & Safety Boundaries
{skill["security"]}

## 11. Platform Adapters
{skill["adapters"]}

## 12. Deliverables & Output Artifacts
{skill["deliverables"]}

## 13. Related & Complementary Skills
{skill["related"]}

## 14. Realistic Usage Example
{skill["usage"]}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"[{idx:02d}/{total:02d}] Created: {skill_id}")

    print(f"\nSuccessfully generated {created}/{total} skills for Groups AQ & AR.")

if __name__ == "__main__":
    generate_skills()
