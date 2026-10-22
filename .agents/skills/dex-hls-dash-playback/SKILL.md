---
name: dex-hls-dash-playback
description: Architect resilient HTTP Live Streaming (HLS) and MPEG-DASH adaptive bitrate playback engines with automated buffer stall recovery, multi-track audio, and WebVTT captions. Use when implementing custom video players, live streaming feeds, or multimedia learning platforms.
---

# dex-hls-dash-playback

## 1. Purpose & Scope
Thiết kế kiến trúc trình phát đa phương tiện phát sóng thích ứng (Adaptive Bitrate Streaming) chuẩn HLS và MPEG-DASH; tích hợp cơ chế tự động phục hồi khi nghẽn đệm dữ liệu (Buffer Stall Recovery), chuyển đổi luồng âm thanh đa ngôn ngữ và đồng bộ phụ đề WebVTT mượt mà.

## 2. When to Use
- Khi xây dựng trình phát video trực tiếp (Live Stream) hoặc video theo yêu cầu (VOD) chất lượng cao.
- Khi người dùng gặp hiện tượng video dừng hình liên tục do tốc độ mạng không ổn định.
- Khi triển khai nền tảng học trực tuyến có yêu cầu phụ đề đa ngôn ngữ và chuyển đổi chất lượng động.

## 3. When NOT to Use
- Khi chỉ phát một đoạn video nền (background video) ngắn 3 giây dạng MP4 lặp đi lặp lại.
- Khi truyền nhận âm thanh thoại thời gian thực hai chiều có độ trễ cực thấp (<200ms) - nên dùng WebRTC.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp manifest HLS (.m3u8) hoặc DASH (.mpd), thư viện player (Hls.js hoặc Shaka Player), phần cứng giải mã Media Source Extensions (MSE).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Adaptive Bitrate (ABR):** Tự động đo lường băng thông mạng tức thời và điều chỉnh độ phân giải phân đoạn video (segment) tiếp theo.
- **Buffer Management:** Duy trì khoảng đệm an toàn (Buffer Ahead 30s) và dọn dẹp bộ đệm đã xem để chống tràn bộ nhớ RAM.
- **Live Edge Synchronization:** Điều chỉnh tốc độ phát nhẹ (1.05x hoặc 0.95x) để giữ khoảng cách với luồng trực tiếp mà không gây giật tiếng.

## 6. Step-by-Step Execution Workflow
1. Kiểm tra hỗ trợ Media Source Extensions (MSE) hoặc trình phát HLS gốc của trình duyệt.
2. Khởi tạo thực thể Hls.js với cấu hình giới hạn kích thước buffer tối đa.
3. Lắng nghe sự kiện lỗi mạng và lỗi giải mã để thực thi chiến lược hồi phục tự động (Stall Recovery Algorithm).
4. Đăng ký danh sách phụ đề WebVTT và thiết lập giao diện tùy chỉnh cho phép người dùng chuyển track.
5. Kiểm tra chuyển đổi độ phân giải mượt mà khi giả lập thay đổi tốc độ mạng từ 10Mbps xuống 1Mbps.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import Hls from 'hls.js';

export function initializePlayer(videoElement: HTMLVideoElement, streamUrl: string) {
  if (Hls.isSupported()) {
    const hls = new Hls({
      maxBufferLength: 30,
      maxMaxBufferLength: 60,
      enableWorker: true,
      lowLatencyMode: true
    });
    
    hls.loadSource(streamUrl);
    hls.attachMedia(videoElement);
    
    hls.on(Hls.Events.ERROR, (event, data) => {
      if (data.fatal) {
        switch (data.type) {
          case Hls.ErrorTypes.NETWORK_ERROR:
            hls.startLoad();
            break;
          case Hls.ErrorTypes.MEDIA_ERROR:
            hls.recoverMediaError();
            break;
          default:
            hls.destroy();
            break;
        }
      }
    });
    return hls;
  }
}
```

## 8. Anti-Patterns & Common Traps
- Để kích thước buffer video quá lớn khiến trình duyệt di động bị crash do tràn bộ nhớ (Out of Memory).
- Không xử lý các lỗi nghiêm trọng (`fatal errors`) làm video bị đứng hình vĩnh viễn khi mạng rớt gói tin.
- Tự động ép phát ở chất lượng cao nhất 4K ngay từ giây đầu tiên mà không đợi đo lường băng thông thực tế.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tỷ lệ dừng hình (Stall Rate) dưới 0.5% tổng thời gian phát trong điều kiện mạng biến động.
- QG-02: Thời gian bắt đầu phát video (Time-to-First-Frame) dưới 1.2 giây.
- QG-03: Tự động phục hồi thành công sau khi ngắt kết nối mạng giả lập 3 giây.

## 10. Security & Safety Boundaries
- Bảo vệ bản quyền nội dung bằng cách xác thực token chữ ký trên từng phân đoạn video (Encrypted HLS / DRM Integration).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module trình phát video đa thích ứng `AdaptiveVideoPlayer.ts`.
1. Chiến lược xử lý lỗi buffer và phục hồi luồng dữ liệu tự động.

## 13. Related & Complementary Skills
- [`dex-media-delivery-pipelines`](.agents/skills/dex-media-delivery-pipelines/SKILL.md)
- [`dex-frontend-error-recovery`](.agents/skills/dex-frontend-error-recovery/SKILL.md)
- [`dex-realtime-protocols`](.agents/skills/dex-realtime-protocols/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Xây dựng cổng truyền hình trực tiếp cho sự kiện thể thao. Sử dụng `dex-hls-dash-playback` để tích hợp trình phát HLS có cơ chế tự động hạ chất lượng xuống 480p khi người dùng vào vùng sóng yếu và tăng lại 1080p khi mạng ổn định, không để xảy ra hiện tượng đứng hình giữa trận đấu.
