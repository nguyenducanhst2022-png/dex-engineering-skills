---
name: dex-drm-compliant-playback-integration
description: Integrate and verify authorized multi-DRM playback architectures (Widevine, FairPlay, PlayReady) via Encrypted Media Extensions (EME). Audit license server exchanges, key rotation, and secure hardware pipelines.
---

# dex-drm-compliant-playback-integration

## 1. Purpose & Scope
Tích hợp và kiểm chứng kiến trúc bảo vệ bản quyền số đa nền tảng (Multi-DRM: Google Widevine, Apple FairPlay Streaming, Microsoft PlayReady); xác thực quy trình cấp phép bản quyền qua Encrypted Media Extensions (EME), kiểm tra khả năng phục hồi lỗi của License Server, mã hóa Common Encryption (CENC - cenc/cbcs) và cơ chế xoay vòng khóa (Key Rotation) an toàn.

## 2. When to Use
- Khi phát hành nội dung video cao cấp (phim điện ảnh, giải đấu thể thao có bản quyền) yêu cầu bảo vệ chuẩn Hollywood (Studio-grade DRM).
- Khi cấu hình trình phát web (Shaka Player, Video.js, Dash.js) hoặc ứng dụng mobile/TV tương tác với hệ thống Key Management Server (KMS).
- Khi chẩn đoán lỗi giải mã DRM (ví dụ lỗi EME `MEDIA_ERR_ENCRYPTED`, HDCP mismatch, hoặc chứng chỉ FairPlay hết hạn).

## 3. When NOT to Use
- Khi video là nội dung công khai, open-source hoặc chỉ cần bảo vệ cơ bản bằng chữ ký số URL (Signed URLs/Token Authentication).
- Khi mục tiêu là bẻ khóa hoặc vượt qua các biện pháp bảo vệ bản quyền (nghiêm cấm tuyệt đối theo chính sách bảo mật DEX).

## 4. Prerequisites & Input Context
- **Hạ tầng DRM:** Endpoint License Acquisition Server hợp lệ, Application Secret Key (FairPlay ASK), hoặc Widevine Provider Credentials.
- **Trình phát thử nghiệm:** Trình duyệt hỗ trợ EME (Chrome Widevine, Safari FairPlay, Edge PlayReady).

## 5. Core Concepts & Taxonomy
- **Common Encryption (CENC):** Chuẩn ISO/IEC 23001-7 cho phép mã hóa nội dung một lần nhưng giải mã được bằng nhiều hệ thống DRM khác nhau.
- **Encrypted Media Extensions (EME):** API W3C cho phép ứng dụng web giao tiếp với Content Decryption Module (CDM) chạy trong môi trường bảo vệ của OS.
- **Security Levels (Widevine L1 vs L3):** L1 xử lý giải mã và hiển thị hoàn toàn trong Trusted Execution Environment (TEE) của phần cứng; L3 chỉ giải mã bằng phần mềm.

## 6. Step-by-Step Execution Workflow
1. Kiểm tra sự sẵn sàng của CDM trên thiết bị mục tiêu bằng API `navigator.requestMediaKeySystemAccess()`.
2. Cấu hình xử lý sự kiện `encrypted` từ thẻ `<video>` để trích xuất `initData` (PSSH box).
3. Tạo phiên giải mã `MediaKeySession` và sinh chuỗi yêu cầu giấy phép (License Request Challenge).
4. Gửi Challenge tới License Server kèm JWT Token chứng thực quyền sở hữu của người dùng.
5. Nhận phản hồi License từ máy chủ và cập nhật vào CDM thông qua `session.update()`.
6. Lắng nghe các lỗi EME và thiết lập cơ chế retry có giới hạn với backoff nếu mạng gặp sự cố tạm thời.

## 7. Concrete Examples
### Tích hợp Shaka Player với cấu hình Multi-DRM (Widevine & FairPlay):
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
```

## 8. Anti-Patterns & Common Traps
- **Hardcoding DRM Credentials in Client Bundles:** Lưu khóa giải mã hoặc client secret trực tiếp trong mã nguồn frontend.
- **Missing HDCP Error Handling:** Không bắt lỗi khi người dùng kết nối màn hình ngoài không hỗ trợ HDCP 2.2, dẫn đến việc video bị đen màn hình mà không có thông báo cho người dùng.
- **Ignoring CDM Certificate Expiry:** Quên gia hạn chứng chỉ FairPlay Application Certificate khiến hàng loạt người dùng thiết bị Apple không thể mở video.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Xác thực thành công handshake EME và nhận license hợp lệ trên cả 3 hệ thống Widevine, FairPlay và PlayReady.
- **QG-02**: Mọi yêu cầu cấp phép bản quyền đều mang token xác thực danh tính người dùng có thời hạn sống ngắn (short-lived JWT).
- **QG-03**: Hệ thống có cơ chế hạ cấp chất lượng mượt mà (fallback HDCP/L3) thay vì gây sập trình duyệt.

## 10. Security & Safety Boundaries
- Tuân thủ tuyệt đối quy định bảo vệ bản quyền số; không lưu trữ khóa giải mã dưới dạng plaintext trên bất kỳ bộ nhớ đệm ứng dụng nào.

## 11. Platform Adapters
- **Runtimes**: Shaka Player, Video.js Contrib-EME, Apple AVPlayer, ExoPlayer (Android), DASH-IF Player.

## 12. Deliverables & Output Artifacts
- Module cấu hình trình phát Multi-DRM (`drm_player_config.js`).
- Bộ kịch bản kiểm thử EME handshake tự động (`test_eme_handshake.js`).

## 13. Related & Complementary Skills
dex-streaming-manifest-validation, dex-streaming-qoe-telemetry, dex-media-content-ingest-moderation

## 14. Realistic Usage Example
```bash
# Kiem tra phan hoi cua License Server bang curl co chu ky JWT
curl -X POST https://license.example.com/v1/widevine \
  -H "Authorization: Bearer $DRM_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @challenge.bin --output license.bin
```
