---
name: dex-live-stream-latency-control
description: Analyze, tune, and measure ultra-low and low-latency live streaming architectures (LL-HLS, LL-DASH, WebRTC/WHIP). Balance buffer drift, catch-up playback rates, and network stability.
---

# dex-live-stream-latency-control

## 1. Purpose & Scope
Tối ưu hóa và kiểm soát độ trễ trong các hệ thống truyền phát trực tiếp (Live Streaming Latency Control); cấu hình chuẩn truyền tải phân đoạn nhỏ (LL-HLS Partial Segments và LL-DASH Chunked Transfer); thiết lập thuật toán bám đuổi độ trễ (Catch-up playback rate adjustment) giúp thu hẹp khoảng cách thời gian giữa nguồn phát và người xem xuống dưới 2-3 giây mà không làm giật bộ đệm.

## 2. When to Use
- Khi phát sóng các sự kiện thể thao trực tiếp, đấu giá online, cá cược thể thao điện tử (Esports) hoặc phòng họp tương tác.
- Khi chuyển đổi kiến trúc từ HLS truyền thống (độ trễ 15–30s) sang Low-Latency HLS (độ trễ 2–4s).
- Khi cần tinh chỉnh thuật toán đồng bộ buffer và tốc độ phát bù (playback speed catching up) trên client.

## 3. When NOT to Use
- Khi hệ thống chỉ phân phối video VOD ghi hình sẵn không có yếu tố tương tác thời gian thực.
- Khi mạng truyền dẫn của khách hàng là vệ tinh có RTT tự nhiên cao (>1000ms) không thể áp dụng low-latency.

## 4. Prerequisites & Input Context
- **Hạ tầng đóng gói:** Máy chủ đóng gói hỗ trợ HTTP/2 Push và Chunked Transfer Encoding (CMAF).
- **Trình phát hỗ trợ:** HLS.js 1.0+ hoặc Shaka Player hỗ trợ chế độ Low Latency.

## 5. Core Concepts & Taxonomy
- **CMAF Partial Segments:** Chia phân đoạn 2 giây thành các mảnh con 200–500ms giúp trình phát bắt đầu giải mã ngay khi mảnh đầu tiên được nạp qua mạng.
- **Catch-up Rate (1.05x - 1.1x):** Tăng nhẹ tốc độ phát khi trình phát bị tụt lại phía sau live edge và tự động hạ về 1.0x khi đã vào vùng mục tiêu an toàn.
- **Live Edge Distance:** Khoảng cách thời gian từ khung hình đang hiển thị tới thời điểm máy quay ghi hình thực tế.

## 6. Step-by-Step Execution Workflow
1. Khảo sát hạ tầng mạng và đo đạc RTT trung bình giữa CDN edge và client.
2. Cấu hình máy chủ media đóng gói CMAF chunked chunks (độ dài partial segment 333ms, full segment 2s).
3. Bật hỗ trợ HTTP/2 hoặc HTTP/3 trên máy chủ CDN để phục vụ các yêu cầu tải partial song song hiệu quả.
4. Cấu hình tham số trình phát: `targetLatency: 2.5s`, `maxLatency: 4.0s`, `minPlaybackRate: 0.95`, `maxPlaybackRate: 1.1`.
5. Thực hiện đo đạc độ trễ đầu cuối (Glass-to-Glass Latency) bằng đồng hồ tham chiếu độ chính xác mili-giây.
6. Theo dõi tỷ lệ rebuffering khi người dùng mạng chập chờn để điều chỉnh ngưỡng rơi về fallback buffer.

## 7. Concrete Examples
### Cấu hình thuật toán Low-Latency Catch-up trong HLS.js:
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
```

## 8. Anti-Patterns & Common Traps
- **Aggressive Catch-up Rate (>1.2x):** Tăng tốc độ phát quá mức làm méo tiếng (pitch shifting) gây khó chịu nghiêm trọng cho người nghe.
- **Deploying LL-HLS over HTTP/1.1:** Không bật HTTP/2 khiến trình duyệt bị cạn kiệt kết nối mạng TCP socket khi liên tục kéo các partial segment nhỏ.
- **Zero Buffer Target:** Cố ép độ trễ xuống dưới 1s trên mạng công cộng khiến trình phát lập tức bị xoay vòng đệm ngay khi mạng suy giảm nhẹ.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Độ trễ trung bình End-to-End ổn định trong khoảng 2.0s – 3.5s trên mạng cáp quang/4G ổn định.
- **QG-02**: Tỷ lệ Rebuffer Ratio dưới 0.5% trong suốt phiên phát sóng 30 phút.
- **QG-03**: Tốc độ phát bù (catch-up playback) không bao giờ vượt quá 1.1x và giữ nguyên cao độ âm thanh (pitch preservation).

## 10. Security & Safety Boundaries
- Bảo vệ endpoint ingest (SRT/RTMP/WHIP) bằng cơ chế stream key luân phiên và kiểm soát dải IP được phép truyền phát.

## 11. Platform Adapters
- **Runtimes**: HLS.js, Shaka Player, NGINX RTMP, SRS (Simple Realtime Server), Wowza Streaming Engine.

## 12. Deliverables & Output Artifacts
- Kịch bản tinh chỉnh tham số trình phát LL-HLS (`latency_tuner.js`).
- Biểu đồ theo dõi phân bố độ trễ Glass-to-Glass (`latency_telemetry.png`).

## 13. Related & Complementary Skills
dex-streaming-manifest-validation, dex-streaming-qoe-telemetry, dex-video-transcoding-ladders

## 14. Realistic Usage Example
```bash
# Do do tre tu may chu ingest den CDN edge bang script do timestamp
python -m scripts.media.measure_glass_latency --stream-url "https://live.example.com/llhls/index.m3u8"
```
