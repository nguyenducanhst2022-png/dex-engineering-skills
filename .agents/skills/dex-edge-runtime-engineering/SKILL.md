---
name: dex-edge-runtime-engineering
description: Build ultra-low latency globally distributed applications on Edge runtimes (Cloudflare Workers, V8 isolates, Fastly Compute) managing memory constraints and edge caching. Use for global personalization, auth gating, and A/B routing.
---

# dex-edge-runtime-engineering

## 1. Purpose & Scope
Thiết kế, lập trình và tối ưu hóa các ứng dụng phân tán toàn cầu chạy trên Edge Runtimes (Cloudflare Workers, Vercel Edge, Deno Deploy, Fastly Compute) dựa trên công nghệ V8 Isolates; xử lý giới hạn bộ nhớ chặt chẽ, tối ưu hóa Edge Caching và giảm thiểu độ trễ mạng xuống mức cận 0 (sub-10ms) cho người dùng toàn cầu.

## 2. When to Use
- Cần thực hiện xác thực (Auth Gating), A/B testing routing hoặc Geo-redirection ngay tại CDN Edge trước khi request chạm vào máy chủ gốc (Origin).
- Xây dựng API toàn cầu yêu cầu độ trễ phản hồi dưới 20ms trên toàn thế giới.
- Tối ưu hóa việc biến đổi nội dung (HTML rewrite, Image optimization) tức thì tại biên.

## 3. When NOT to Use
- Không dùng Edge Runtimes cho các ứng dụng phụ thuộc vào các thư viện C++ native hoặc thư viện Node.js cần filesystem access (`fs`).
- Không dùng cho các tác vụ cần thời gian tính toán CPU vượt quá 50ms trên mỗi request.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- V8 Isolate runtime environment specs (Node.js API compatibility layer).
- Cơ chế lưu trữ tại biên (Cloudflare KV, D1 SQL, Durable Objects, Fastly KV).
- Quy tắc bộ nhớ cache (Cache-Control, Stale-While-Revalidate).
- **Điều kiện tiên quyết**:
- Mã nguồn tuân thủ tiêu chuẩn Web Standards API (Fetch, Request, Response, Streams, SubtleCrypto).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- V8 Isolates vs Containers: V8 Isolates khởi động trong chưa đầy 5ms và tiêu thụ vài KB bộ nhớ, nhanh hơn hàng ngàn lần so với khởi động một container Linux.
- Edge Storage Tradeoffs: Bộ nhớ KV tại Edge có tính nhất quán cuối cùng (Eventual Consistency toàn cầu), phù hợp cho việc đọc thường xuyên và ít ghi.
- Stale-While-Revalidate: Trả về nội dung cache cũ ngay lập tức cho người dùng trong khi âm thầm tải nội dung mới từ máy chủ gốc dưới nền.
- **Quy tắc quyết định kỹ thuật**:
- Nếu kích thước mã nguồn vượt quá 1MB: thực hiện code-splitting hoặc chuyển bớt logic nặng về backend origin.
- Nếu cần chia sẻ trạng thái đồng bộ có tính nhất quán cao: sử dụng Durable Objects thay vì KV.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Lỗi sử dụng các API đặc thù của Node.js như `process.version` hoặc `child_process` khiến Worker bị sập khi khởi chạy trên Edge.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo dự án Worker tuân thủ Web Standards API bằng Wrangler.
2. Cấu hình các route biên và quy tắc cache tại điểm hiện diện (PoP).
3. Tích hợp Edge KV hoặc Durable Objects để lưu cấu hình tính năng (Feature flags).
4. Kiểm thử cục bộ bằng môi trường mô phỏng `miniflare` hoặc `workerd`.
5. Triển khai phân phối tự động tới hơn 300 trung tâm dữ liệu toàn cầu.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
export default {
  async fetch(request: Request, env: any): Promise<Response> {
    const url = new URL(request.url);
    const country = request.headers.get('cf-ipcountry') || 'US';
    
    // Tự động route người dùng tới máy chủ gốc gần nhất
    if (url.pathname.startsWith('/api/v1/feed')) {
      const cache = caches.default;
      let response = await cache.match(request);
      if (!response) {
        response = await fetch(`https://${country}.origin.example.com${url.pathname}`);
        // Cache tại Edge trong 60 giây
        response = new Response(response.body, response);
        response.headers.set('Cache-Control', 'public, max-age=60');
        await cache.put(request, response.clone());
      }
      return response;
    }
    return fetch(request);
  }
};
```

### Lệnh xác minh & thực thi:
```bash
npx wrangler dev --local
# Triển khai thử nghiệm lên edge network
npx wrangler deploy --dry-run
```

## 8. Anti-Patterns & Common Traps
- Cố gắng mở TCP socket kết nối trực tiếp tới cơ sở dữ liệu truyền thống mà không qua connection pooling proxy tại Edge.
- Bỏ qua giới hạn CPU time (10ms-50ms) dẫn đến lỗi Worker Exceeded CPU Limit.

## 9. Quality Gates & Acceptance Criteria
- Thời gian phản hồi P95 tại Edge đạt dưới 15ms cho các request hit cache.
- Bundle size sau khi nén phải nhỏ hơn 500KB.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Không lưu trữ Master Secret Key dài hạn trong biến môi trường của Worker; sử dụng Edge Secrets được mã hóa.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Mã nguồn Edge Worker chuẩn hóa TypeScript.
- File cấu hình triển khai `wrangler.toml` kèm bộ kiểm thử cục bộ.

## 13. Related & Complementary Skills
dex-serverless-architecture, dex-web-security-headers, dex-frontend-data-flow

## 14. Realistic Usage Example
### Tình huống thực tế:
Một trang tin tức toàn cầu bị nghẽn server khi có sự kiện bầu cử. Họ chuyển toàn bộ tầng xác thực paywall và định tuyến quốc gia lên Cloudflare Workers tại biên. 85% lưu lượng được xử lý ngay tại Edge với độ trễ 8ms, giảm 90% tải cho cụm máy chủ trung tâm.
