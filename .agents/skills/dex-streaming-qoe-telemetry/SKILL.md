---
name: dex-streaming-qoe-telemetry
description: Collect, aggregate, and analyze video streaming Quality of Experience (QoE) metrics. Measure startup time, rebuffering ratios, bitrate transitions, and playback failures without violating user privacy.
---

# dex-streaming-qoe-telemetry

## 1. Purpose & Scope
Thu thập, tổng hợp và phân tích các chỉ số chất lượng trải nghiệm phát video (Quality of Experience - QoE) từ phía người dùng cuối; đo lường chính xác thời gian khởi động phát (Time to First Frame / Startup Delay), tỷ lệ giật bộ đệm (Rebuffering Ratio), tần suất nhảy tầng bitrate và các lỗi phát nghiêm trọng (Fatal Playback Errors); bảo đảm tính riêng tư tuyệt đối cho người dùng không thu thập dữ liệu định danh cá nhân (Zero-PII Telemetry).

## 2. When to Use
- Khi theo dõi chất lượng mạng phân phối CDN và hiệu năng phát video trên quy mô hàng triệu người dùng.
- Khi đánh giá tác động của việc thay đổi thuật toán bitrate thích ứng (ABR) lên trải nghiệm thực tế của người xem.
- Khi điều tra sự cố sụt giảm chất lượng video trên các nhà mạng viễn thông hoặc khu vực địa lý cụ thể.

## 3. When NOT to Use
- Khi ứng dụng chỉ phát tệp âm thanh ngắn hạn chế thời lượng (<5s) hoặc thông báo hệ thống.
- Khi hệ thống giám sát hạ tầng thuần túy ở tầng mạng (ping, packet loss máy chủ) mà không đo lường góc nhìn của trình phát video.

## 4. Prerequisites & Input Context
- **Hệ thống trình phát:** HLS.js, Shaka Player, hoặc Video.js có hook sự kiện phân tích.
- **Hạ tầng Telemetry:** Endpoint nạp dữ liệu phân tích có khả năng chịu tải cao (Kafka, ClickHouse, hoặc AWS Kinesis).

## 5. Core Concepts & Taxonomy
- **Time to First Frame (TTFF):** Thời gian tính từ khi người dùng bấm nút Play cho đến khi khung hình video đầu tiên thực sự được vẽ lên màn hình.
- **Rebuffer Ratio:** Tỷ lệ phần trăm thời gian người xem phải chờ nạp bộ đệm chia cho tổng thời gian xem video (mục tiêu tiêu chuẩn công nghiệp < 0.5%).
- **Beacon API:** API trình duyệt `navigator.sendBeacon()` gửi dữ liệu telemetry bất đồng bộ khi người dùng chuẩn bị đóng tab mà không làm chậm việc điều hướng.

## 6. Step-by-Step Execution Workflow
1. Đăng ký các bộ lắng nghe sự kiện trên video player (`waiting`, `playing`, `error`, `ratechange`).
2. Đo đạc các mốc thời gian quan trọng: Bắt đầu tải manifest -> Nhận manifest -> Tải segment 0 -> Hiển thị khung hình 1.
3. Định kỳ 30 giây gom các thông số (bitrate trung bình, số lần buffer, số frame bị rớt - dropped frames) thành một payload gọn nhẹ.
4. Gửi payload về backend qua `navigator.sendBeacon()` hoặc HTTP POST nén gzip.
5. Tổng hợp dữ liệu trên dashboard theo thời gian thực (P50, P90, P99 của TTFF và tỷ lệ rebuffer).
6. Kích hoạt cảnh báo tự động nếu tỷ lệ lỗi phát sóng vượt ngưỡng 1.0% trong 5 phút liên tiếp.

## 7. Concrete Examples
### Module thu thap telemetry QoE video nhe khong thu thap PII:
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
```

## 8. Anti-Patterns & Common Traps
- **Tracking Personal Identifiers (PII):** Gửi kèm email, IP nguyên bản hoặc tên thật của người dùng vào payload telemetry gây vi phạm GDPR/CCPA.
- **Synchronous Telemetry Calls:** Dùng AJAX đồng bộ chặn đứng sự kiện thoát tab của trình duyệt làm giảm trải nghiệm người dùng.
- **High Frequency Reporting:** Gửi ping telemetry mỗi 100ms gây quá tải hệ thống ingestion backend và tốn pin điện thoại.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Payload telemetry không chứa bất kỳ dữ liệu PII nào; IP được băm ẩn danh (anonymized/truncated).
- **QG-02**: Quá trình thu thập telemetry không chiếm quá 1% CPU của Main Thread.
- **QG-03**: Tỷ lệ gửi thành công qua `sendBeacon` đạt trên 99% khi người dùng đóng trang.

## 10. Security & Safety Boundaries
- Tuân thủ nghiêm ngặt nguyên tắc Data Minimization; mã hóa luồng dữ liệu telemetry khi truyền tải qua HTTPS.

## 11. Platform Adapters
- **Runtimes**: W3C Media Capabilities API, HLS.js telemetry, Shaka Player analytics, ClickHouse.

## 12. Deliverables & Output Artifacts
- Thư viện thu thập QoE phía client (`VideoQoETracker.js`).
- Lược đồ bảng lưu trữ phân tích dữ liệu QoE trên ClickHouse.

## 13. Related & Complementary Skills
dex-video-transcoding-ladders, dex-streaming-manifest-validation, dex-live-stream-latency-control

## 14. Realistic Usage Example
```bash
# Truy van chi so QoE P95 tu ClickHouse
clickhouse-client --query "SELECT quantile(0.95)(ttff) AS p95_ttff, avg(rebuffer_ratio) FROM qoe_events WHERE timestamp >= now() - INTERVAL 1 HOUR"
```
