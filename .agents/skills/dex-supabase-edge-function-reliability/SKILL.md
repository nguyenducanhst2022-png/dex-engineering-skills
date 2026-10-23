---
name: dex-supabase-edge-function-reliability
description: Architect, harden, and monitor Supabase Edge Functions in the Deno runtime. Implement idempotent webhooks, timeout mitigation, connection pooler integration, and structured observability. Use when building production serverless backend services.
---

# dex-supabase-edge-function-reliability

## 1. Purpose & Scope
Thiết kế, bảo mật và duy trì độ tin cậy cao của các hàm Supabase Edge Functions chạy trên môi trường Deno Serverless; xử lý bài toán Webhook Idempotency chống xử lý trùng lặp sự kiện; tối ưu hóa quản lý kết nối cơ sở dữ liệu qua Supavisor Transaction Pooler; kiểm soát thời gian chạy chống timeout đột ngột; và thiết lập hệ thống ghi log có cấu trúc.

## 2. When to Use
- Khi triển khai các webhook xử lý thanh toán (Stripe, LemonSqueezy) đòi hỏi tính bất biến và không được xử lý lặp.
- Khi Edge Function cần kết nối tới cơ sở dữ liệu PostgreSQL dưới tải cao mà không làm cạn kiệt connection slots.
- Khi cần chạy logic backend gần người dùng (Edge) với độ trễ thấp và khả năng scale tự động.

## 3. When NOT to Use
- Khi tác vụ là xử lý dữ liệu nặng kéo dài hàng chục phút (như render video, training model AI) vượt quá giới hạn thời gian chạy của Edge Function (nên dùng Background Job Queues).
- Khi dịch vụ yêu cầu hệ thống socket trạng thái liên tục kéo dài nhiều giờ (nên dùng Dedicated Server hoặc Realtime Channels).

## 4. Prerequisites & Input Context
- **Môi trường phát triển:** Deno CLI và Supabase CLI cài đặt cục bộ.
- **Thông tin cấu hình:** Khóa API, Database Connection String (Transaction Pooler port 6543), và Webhook Signing Secrets.

## 5. Core Concepts & Taxonomy
- **Supavisor Transaction Pooling:** Bắt buộc sử dụng cổng `6543` với tham số `?pgbouncer=true` khi Edge Function kết nối trực tiếp vào Postgres để tránh cạn kiệt pool kết nối vật lý.
- **Idempotency Key:** Khóa định danh duy nhất của mỗi sự kiện webhook (như Stripe Event ID) được lưu vào bảng atomic trước khi xử lý, ngăn chặn việc trừ tiền hoặc tạo đơn hàng lặp lại khi nhà cung cấp retry webhook.
- **CPU vs Wall-Clock Timeout:** Deno Edge Functions có giới hạn thời gian tính toán CPU (thường 2s) và thời gian thực tế (Wall-Clock, thường 60-150s); cần tách các tác vụ I/O bất đồng bộ đúng cách.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo Edge Function mới bằng Supabase CLI: `supabase functions new payment-webhook`.
2. Thiết lập cơ chế kiểm tra chữ ký điện tử HMAC (Signature Verification) ngay tại đầu hàm để từ chối các request giả mạo.
3. Kiểm tra Idempotency: Ghi `event_id` vào bảng `processed_events` bằng câu lệnh `INSERT ... ON CONFLICT DO NOTHING;`.
4. Kết nối tới database qua transaction pooler và thực thi logic nghiệp vụ trong một transaction duy nhất.
5. Bọc toàn bộ logic trong khối `try/catch` có cấu trúc; ghi log JSON chứa request ID và execution duration.
6. Trả về mã phản hồi `200 OK` kịp thời để nhà cung cấp webhook không gửi lại yêu cầu.

## 7. Concrete Examples
### Edge Function xử lý Webhook Idempotent an toàn với Deno và PostgreSQL:
```typescript
// supabase/functions/stripe-webhook/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req: Request) => {
  const signature = req.headers.get("stripe-signature");
  if (!signature) {
    return new Response("Missing signature", { status: 400 });
  }

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  try {
    const payload = await req.json();
    const eventId = payload.id;

    // Kiem tra Idempotency: Neu event da xu ly thi bo qua ngay lap tuc
    const { data, error } = await supabase
      .from("processed_webhooks")
      .insert({ event_id: eventId, event_type: payload.type })
      .select();

    if (error && error.code === "23505") { // 23505: Unique violation trong Postgres
      return new Response(JSON.stringify({ status: "already_processed" }), { status: 200 });
    }

    // Xu ly nghiep vu (vi du: cap nhat trang thai don hang)
    if (payload.type === "checkout.session.completed") {
      await supabase
        .from("orders")
        .update({ status: "PAID" })
        .eq("stripe_session_id", payload.data.object.id);
    }

    return new Response(JSON.stringify({ received: true }), { status: 200 });
  } catch (err: any) {
    console.error(JSON.stringify({ error: err.message, stack: err.stack }));
    return new Response("Internal Server Error", { status: 500 });
  }
});
```

## 8. Anti-Patterns & Common Traps
- **Direct DB Connection without Pooler:** Kết nối thẳng vào cổng `5432` từ hàng nghìn Edge Function đồng thời, làm cạn kiệt slots kết nối của Postgres và làm sập cơ sở dữ liệu.
- **Skipping HMAC Verification:** Tin tưởng mù quáng vào body request mà không kiểm tra chữ ký số của nhà cung cấp, cho phép tin tặc giả lập sự kiện thanh toán thành công.
- **Uncaught Promise Rejections:** Quên xử lý lỗi bất đồng bộ khiến Edge Function crash và trả về lỗi 502 Bad Gateway không có thông tin chẩn đoán.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các webhook Edge Functions đều có bước kiểm tra chữ ký mật mã (HMAC/Ed25519) trước khi phân tích payload.
- **QG-02**: Mọi sự kiện có tính thay đổi trạng thái tài chính đều được bảo vệ bằng bảng Idempotency.
- **QG-03**: Các hàm kết nối database đều sử dụng chuỗi kết nối cổng `6543` (Supavisor Transaction Mode).

## 10. Security & Safety Boundaries
- Bảo vệ tuyệt đối tính toàn vẹn của các giao dịch kinh doanh và bảo mật các khóa `SERVICE_ROLE_KEY` trong biến môi trường Deno Secrets.

## 11. Platform Adapters
- **Runtimes**: Deno Deploy, Supabase CLI, Stripe CLI, Cloudflare Workers.

## 12. Deliverables & Output Artifacts
- Mã nguồn Edge Function chuẩn tắc (`supabase/functions/*/index.ts`).
- Lược đồ bảng lưu trữ sự kiện Idempotency (`processed_webhooks.sql`).
- Bộ kiểm thử unit test cho Edge Function chạy bằng Deno Test Runner.

## 13. Related & Complementary Skills
dex-supabase-adapter, dex-idempotent-operations, dex-webhook-signature-validation

## 14. Realistic Usage Example
```bash
# Chay thu nghiem Edge Function cuc bo bang Supabase CLI
supabase functions serve --env-file .env.local

# Trien khai Edge Function len Supabase Cloud
supabase functions deploy stripe-webhook --no-verify-jwt
```
