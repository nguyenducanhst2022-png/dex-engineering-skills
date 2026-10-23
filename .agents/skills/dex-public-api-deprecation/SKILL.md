---
name: dex-public-api-deprecation
description: Manage public API deprecation lifecycles according to RFC 8594 standards, consumer migration communication, sunset telemetry, and backward-compatible evolution. Use when retiring legacy API versions or breaking interface contracts.
---

# dex-public-api-deprecation

## 1. Purpose & Scope
Quản trị quy trình khai tử API công khai (Public API Deprecation Lifecycle) tuân thủ tiêu chuẩn RFC 8594 (Sunset & Deprecation HTTP headers); đo lường mức độ sử dụng của các đối tác tích hợp, cung cấp tài liệu di chuyển và bảo đảm chuyển đổi mượt mà không làm sập ứng dụng client.

## 2. When to Use
- Khi cần loại bỏ các API endpoint cũ không còn an toàn hoặc không phù hợp với kiến trúc mới.
- Khi thực hiện thay đổi phá vỡ tương thích (breaking changes) trên các API công khai cho bên thứ ba.
- Khi xây dựng lộ trình chấm dứt hỗ trợ phiên bản API v1 để chuyển sang v2 theo hợp đồng dịch vụ (SLA).

## 3. When NOT to Use
- Khi chỉ sửa đổi logic nội bộ không thay đổi cấu trúc request/response của API.
- Khi thêm trường mới có tính tương thích ngược hoàn toàn (non-breaking additions).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách endpoint cần khai tử, thời hạn sunset chính thức, hệ thống phân tích API access logs nhận diện client theo API Key / Client ID.
- **Quyền hạn truy cập:** Quyền sửa đổi mã nguồn API gateway hoặc middleware response headers.

## 5. Core Concepts & Taxonomy
- **RFC 8594 Sunset Header:** Header chuẩn hóa thông báo thời điểm chính xác endpoint sẽ ngừng hoạt động vĩnh viễn (ví dụ: `Sunset: Wed, 11 Nov 2026 00:00:00 GMT`).
- **Deprecation HTTP Header:** Báo hiệu endpoint đã bị phản đối và cung cấp link dẫn tới tài liệu di chuyển (ví dụ: `Deprecation: @1762819200; link="<https://api.dex.dev/migrations/v1-to-v2>"`).
- **Brownout Testing:** Tạm thời tắt API cũ trong khoảng thời gian ngắn (ví dụ: 15 phút) trước ngày sunset để phát hiện các client còn dùng mà chưa liên hệ.

## 6. Step-by-Step Execution Workflow
1. Công bố thông báo deprecation chính thức kèm theo Migration Guide tối thiểu 6-12 tháng trước ngày sunset.
2. Cài đặt middleware tự động trả về các HTTP header `Deprecation` và `Sunset` trên tất cả endpoint thuộc diện khai tử.
3. Thiết lập dashboard đo lường số lượng request hàng ngày theo từng API Key / Client ID còn gọi vào endpoint cũ.
4. Gửi email cảnh báo tự động tới các khách hàng vẫn còn lưu lượng truy cập cao khi thời hạn sunset đến gần.
5. Tiến hành Brownout testing định kỳ (tắt tạm thời trong giờ thấp điểm) để cảnh tỉnh các lập trình viên client.
6. Đến ngày Sunset: chuyển đổi response vĩnh viễn sang mã lỗi `HTTP 410 Gone` kèm theo link hướng dẫn nâng cấp.

## 7. Concrete Examples
### Ví dụ middleware thêm header Deprecation & Sunset trong Node.js Express:
```typescript
import { Request, Response, NextFunction } from 'express';

export function deprecationMiddleware(sunsetDate: string, docUrl: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    // 1. Thêm chuẩn header theo RFC 8594
    res.setHeader('Deprecation', 'true');
    res.setHeader('Sunset', sunsetDate); // e.g., "Wed, 11 Nov 2026 00:00:00 GMT"
    res.setHeader('Link', `<${docUrl}>; rel="deprecation"; type="text/html"`);

    // 2. Ghi nhận telemetry client ID đang gọi endpoint cũ
    const clientId = req.headers['x-api-key'] || 'anonymous';
    console.warn(`[API-DEPRECATION] Client ${clientId} called deprecated endpoint: ${req.originalUrl}`);

    next();
  };
}
```

## 8. Anti-Patterns & Common Traps
- **Silent Breaking Changes:** Đột ngột xóa hoặc sửa kiểu dữ liệu endpoint mà không báo trước cho khách hàng bên thứ ba.
- **Indefinite Deprecation:** Đánh dấu deprecated nhưng để tồn tại 10 năm không bao giờ sunset khiến hệ thống gánh nợ kỹ thuật nặng nề.
- **Generic Error Codes:** Trả về `500 Internal Server Error` thay vì mã chuẩn `410 Gone` khi endpoint chính thức bị tắt.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Tất cả response từ deprecated endpoint phải chứa đầy đủ header `Sunset` và `Link`.
- **QG-08**: Đường dẫn migration guide trong header `Link` phải hoạt động và trả về HTTP 200.
- **QG-14**: Tỷ lệ lưu lượng gọi vào endpoint cũ dưới 0.1% tổng lưu lượng trước khi tiến hành tắt hẳn.

## 10. Security & Safety Boundaries
- Đảm bảo các API endpoint cũ sắp bị khai tử vẫn nhận được các bản vá bảo mật khẩn cấp trong suốt thời gian bảo trì.
- Thu hồi quyền truy cập của các client không chịu nâng cấp sau khi thời hạn sunset đã kết thúc.

## 11. Platform Adapters
- **API Gateways**: Kong Deprecation Plugin, AWS API Gateway custom response parameters.
- **Frameworks**: Express.js, FastAPI, Spring Boot Interceptors.

## 12. Deliverables & Output Artifacts
- Middleware gắn header RFC 8594 Deprecation & Sunset.
- Tài liệu Migration Guide chuyển đổi phiên bản API.
- Dashboard theo dõi lưu lượng client còn sót lại trước ngày sunset.

## 13. Related & Complementary Skills
dex-api-engineering, dex-semantic-version-automation, dex-contract-first-development

## 14. Realistic Usage Example
```powershell
# Kiểm tra sự hiện diện của các header Deprecation chuẩn mực trên endpoint
curl -I https://api.dex.dev/v1/legacy-resource
```
