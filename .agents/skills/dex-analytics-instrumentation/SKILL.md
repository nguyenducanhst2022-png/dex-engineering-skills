---
name: dex-analytics-instrumentation
description: Instrument product and business analytics with strict tracking plans, event taxonomy (object_action), schema validation, PII scrubbing, and dual client/server verification. Use when adding or maintaining behavioral event tracking.
---

# dex-analytics-instrumentation

## 1. Purpose & Scope
Thiết kế, tích hợp và kiểm thử hệ thống thu thập dữ liệu hành vi người dùng và phân tích sản phẩm (Product & Business Analytics Instrumentation); thiết lập kế hoạch theo dõi chặt chẽ (Tracking Plan / Event Dictionary), chuẩn hóa cấu trúc định danh sự kiện (Event Taxonomy: `object_action`), kiểm tra hợp đồng dữ liệu payload tại thời điểm phát sinh (Event Schema Validation), tự động thanh lọc thông tin định danh cá nhân nhạy cảm (Automated PII Scrubbing) và kiểm chứng luồng truyền tin kép (Dual Client-Side & Server-Side Tracking).

## 2. When to Use
- Khi ra mắt tính năng mới cần đo lường tỷ lệ chuyển đổi (Conversion Rate), hành vi tương tác hoặc hiệu quả thử nghiệm A/B.
- Khi hệ thống phân tích hiện tại bị hỗn loạn (Spaghetti Events) với hàng trăm tên sự kiện đặt tự do, sai chính tả hoặc thiếu thuộc tính quan trọng.
- Khi phát hiện mã theo dõi đang vô tình gửi email hoặc mật khẩu người dùng sang các dịch vụ phân tích thứ ba (Mixpanel, Amplitude, PostHog, Segment).

## 3. When NOT to Use
- Thu thập metrics hệ thống CPU, RAM, Network (dùng `dex-production-monitoring`).
- Truy vết phân tán latency giữa các microservices (dùng `dex-distributed-tracing`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các sự kiện cần đo lường theo hành trình người dùng (User Funnel).
- Danh mục thuộc tính chung (Global Context: `user_id`, `app_version`, `platform`, `locale`) và thuộc tính riêng của từng sự kiện.
- Nền tảng đích (PostHog, Amplitude, Mixpanel, Segment, Snowplow).
- **Điều kiện tiên quyết**:
- Analytics SDK hoặc Tracking Client được cài đặt.
- Thư viện kiểm tra schema (Zod, JSON Schema).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Standardized Event Taxonomy (`object_action`)**: Tên sự kiện phải tuân thủ nghiêm ngặt quy ước danh từ + động từ ở dạng quá khứ: `order_completed`, `button_clicked`, `form_submitted`; cấm dùng tên mơ hồ như `track1`, `click_here`.
- **Strict Tracking Plan as Code**: Kế hoạch đo lường được định nghĩa bằng mã nguồn (TypeScript / JSON Schema); mọi sự kiện vi phạm schema sẽ bị từ chối hoặc cảnh báo ngay trong môi trường staging.
- **Client vs Server-Side Dispatch Balance**: Các sự kiện nhạy cảm về doanh thu (Thanh toán thành công, Đổi mật khẩu) bắt buộc phải emit từ Server-side để chống gian lận và chặn ad-blocker; các sự kiện tương tác giao diện (Scroll, Hover) emit từ Client-side.
- **Quy tắc quyết định kỹ thuật**:
- **Tuyệt Đối Không Gửi PII Vào Analytics Payload**: Tự động chặn và lọc bỏ các key nhạy cảm: `password`, `token`, `email`, `phone`, `ssn`, `credit_card`.
- **Snake_case Cho Tên Sự Kiện và Thuộc Tính**: Toàn bộ tên sự kiện và keys thuộc tính phải dùng chữ thường phân cách bằng dấu gạch dưới (`snake_case`).
- **Đảm Bảo Tính Nhất Quán Giữa Các Nền Tảng**: Sự kiện `sign_up_completed` trên iOS, Android và Web phải có cùng một tên gọi và cùng cấu trúc thuộc tính.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Dữ liệu phân tích doanh thu bị lệch 30% so với Database thực tế**: Do chỉ bắt sự kiện `payment_completed` ở giao diện trình duyệt, người dùng thanh toán xong tắt tab trước khi script kịp chạy hoặc bị tiện ích chặn quảng cáo (AdBlock) chặn -> Khắc phục: Chuyển toàn bộ sự kiện thanh toán sang Server-Side Webhook.
- **Bảng phân tích ngập rác vì lập trình viên gửi dữ liệu bẩn**: Một sự kiện gửi thuộc tính `price: "100k"` thay vì số nguyên `price: 100000` -> Khắc phục: Áp dụng schema validation chặt chẽ bằng Zod trước khi gọi SDK `track()`.

## 6. Step-by-Step Execution Workflow
1. Xây dựng tài liệu Tracking Plan quy định danh mục sự kiện và các trường bắt buộc.
2. Viết định nghĩa Schema bằng Zod hoặc TypeScript cho từng sự kiện: `OrderCompletedSchema`.
3. Tạo lớp bọc (Analytics Wrapper / Facade) tích hợp cơ chế tự động validate và PII scrubbing.
4. Tích hợp lệnh gọi `analytics.track()` tại các điểm kích hoạt nghiệp vụ tương ứng.
5. Kiểm tra tính hợp lệ trong môi trường test bằng công cụ Debugger / Proxy (Charles, Proxyman, PostHog Toolbar).
6. Xác nhận dữ liệu hiển thị chính xác trên dashboard phân tích (Live Stream Events).
7. Khóa schema trong CI: Chạy unit test kiểm tra toàn bộ lệnh gọi analytics tuân thủ tracking plan.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
import { z } from 'zod';

// 1. Định nghĩa Event Schema chặt chẽ
export const OrderCompletedEventSchema = z.object({
  order_id: z.string().uuid(),
  total_amount: z.number().positive(),
  currency: z.enum(['VND', 'USD', 'EUR']),
  item_count: z.number().int().positive(),
  payment_method: z.enum(['credit_card', 'bank_transfer', 'e_wallet']),
});
export type OrderCompletedEvent = z.infer<typeof OrderCompletedEventSchema>;

// 2. Analytics Client có PII Scrubbing và Schema Validation
export class SafeAnalyticsClient {
  private scrubPII(data: Record<string, any>): Record<string, any> {
    const piiKeys = ['email', 'password', 'phone', 'token', 'card_number'];
    const cleanData = { ...data };
    for (const key of Object.keys(cleanData)) {
      if (piiKeys.some((pii) => key.toLowerCase().includes(pii))) {
        delete cleanData[key]; // Loại bỏ trường nhạy cảm
      }
    }
    return cleanData;
  }

  trackOrderCompleted(payload: OrderCompletedEvent) {
    // Validate schema trước khi gửi
    const parsed = OrderCompletedEventSchema.safeParse(payload);
    if (!parsed.success) {
      console.error('ANALYTICS_SCHEMA_ERROR:', parsed.error.format());
      return;
    }
    const sanitized = this.scrubPII(parsed.data);
    // Gửi dữ liệu an toàn tới Analytics Provider
    posthog.capture('order_completed', sanitized);
  }
}
```

### Lệnh xác minh & thực thi:
- Chạy unit test kiểm tra schema validation của analytics: `npm run test -- test/analytics-schema.test.ts`
- Bắt gói tin kiểm tra không có PII trong request: `proxyman --filter 'analytics.example.com'`
- Kiểm tra tính đầy đủ của thuộc tính sự kiện: Sử dụng PostHog CLI hoặc Amplitude Data validator

## 8. Anti-Patterns & Common Traps
- **Bắt sự kiện tự do trực tiếp trong UI Component**: `onClick={() => mixpanel.track('btn1')}` gây rác dữ liệu và cực khó bảo trì.
- **Gửi sự kiện thanh toán chỉ từ Client-side**: Dễ bị hack số tiền giả mạo hoặc mất dữ liệu do mạng.
- **Thay đổi kiểu dữ liệu của thuộc tính cũ**: Đang dùng kiểu số `user_age: 25` đổi thành chuỗi `user_age: "25-30"` làm hỏng toàn bộ biểu đồ lịch sử.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các sự kiện mới đều có định nghĩa trong Tracking Plan và có schema validation.
- QG-07: 0 trường thông tin PII nhạy cảm bị rò rỉ sang analytics payload.
- QG-11: Tỷ lệ khớp dữ liệu (Data Reconciliation) giữa Server-side Analytics và Database đạt >= 99%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Tôn trọng tùy chọn không theo dõi của người dùng (Respect Do-Not-Track / Global Privacy Control headers).
- Bật tính năng ẩn danh địa chỉ IP (IP Anonymization) trên các công cụ phân tích lưu trữ ngoài lãnh thổ.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Tệp tài liệu Tracking Plan (Event Dictionary).
- Module Type-safe Analytics Client có chức năng PII scrubber.
- Bộ kiểm thử unit tests xác thực hợp đồng sự kiện.

## 13. Related & Complementary Skills
- `dex-privacy-impact-assessment`: Rà soát việc thu thập dữ liệu hành vi dưới góc độ pháp lý.
- `dex-feature-prioritization`: Sử dụng dữ liệu analytics để tính toán điểm Reach và Impact.
- `dex-experimentation-metrics`: Kết nối sự kiện analytics vào các bài kiểm thử A/B testing.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng ngân hàng số muốn tối ưu luồng mở thẻ tín dụng. Kỹ sư sử dụng `dex-analytics-instrumentation`, thiết kế tracking plan với các sự kiện chuẩn: `card_flow_started`, `id_step_completed`, `card_application_submitted`. Nhờ có module PII scrubbing, số CMND và mã OTP của khách hàng được tự động lọc bỏ không bị gửi lên PostHog, trong khi tỷ lệ rớt ở bước chụp ảnh giấy tờ được ghi nhận chính xác 99.8%, giúp đội ngũ UX phát hiện và sửa ngay điểm nghẽn giao diện.
