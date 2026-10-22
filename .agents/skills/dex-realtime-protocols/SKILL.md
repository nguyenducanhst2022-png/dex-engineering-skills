---
name: dex-realtime-protocols
description: Architect realtime communication protocols (WebSockets, Server-Sent Events, WebRTC, Long Polling), connection lifecycles, heartbeat pings, and reconnection backoffs. Use when implementing live chats, real-time dashboards, or collaborative tools.
---

# dex-realtime-protocols

## 1. Purpose & Scope
Thiết kế, triển khai và mở rộng hệ thống giao tiếp thời gian thực (Realtime Communication); lựa chọn giao thức tối ưu giữa WebSockets (hai chiều) và Server-Sent Events (SSE - một chiều từ máy chủ); quản lý vòng đời kết nối bền vững, cơ chế nhịp tim giữ kết nối (Heartbeat / Ping-Pong), tự động kết nối lại (Auto-reconnection) và phân tán thông điệp qua Redis Pub/Sub.

## 2. When to Use
- Khi xây dựng các tính năng tương tác trực tiếp: Chat thời gian thực, bảng tin thông báo nổi, theo dõi vị trí shipper trên bản đồ, sàn đấu giá trực tuyến.
- Khi hệ thống đang dùng kỹ thuật HTTP Polling liên tục (cứ 2 giây gọi API 1 lần) gây lãng phí tài nguyên máy chủ.
- Khi kết nối socket bị đứt ngẫu nhiên sau vài chục giây do router mạng hoặc proxy tự ngắt.

## 3. When NOT to Use
- Các tác vụ chỉ cần truyền nhận dữ liệu thông thường một lần qua HTTP RESTful API.
- Xử lý các batch job chạy ngầm không có nhu cầu tương tác với người dùng theo thời gian thực.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Loại hình tương tác (Một chiều hay Hai chiều).
- Số lượng kết nối đồng thời dự kiến (Concurrent connections: 1,000 hay 100,000).
- Nền tảng công nghệ (Socket.io, WS, uWebSockets.js, EventSource SSE).

**Điều kiện tiên quyết:**
- Máy chủ reverse proxy (Nginx, Traefik, AWS ALB) đã được cấu hình bật `Upgrade: websocket` và tắt proxy buffering cho SSE.
- Đã thiết lập Redis adapter nếu cần chạy mở rộng nhiều node máy chủ realtime song song.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Ưu Tiên SSE Cho AI Streaming**: Nếu xây dựng tính năng hiển thị chữ chạy từng từ của LLM, luôn ưu tiên dùng Server-Sent Events (SSE) vì nó chạy trên HTTP chuẩn, tự động kết nối lại và tương thích hoàn hảo với HTTP/2.
- **Không Tin Tưởng Client Socket**: Mọi tin nhắn gửi lên qua WebSocket đều phải validate dữ liệu và kiểm tra quyền hạn chặt chẽ như một HTTP request bình thường.
- **Dọn Dẹp Khi Ngắt Kết Nối**: Luôn xóa sạch tham chiếu socket khỏi bộ nhớ và hủy lắng nghe sự kiện khi client disconnect để tránh rò rỉ bộ nhớ (Memory Leak).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Bão kết nối lại làm sập máy chủ (Reconnection Storm)**: Khi máy chủ khởi động lại, 50,000 người dùng đồng loạt bấm kết nối lại trong cùng 1 giây -> Khắc phục: Phía client bắt buộc phải có độ trễ ngẫu nhiên (Jitter) từ 1 đến 10 giây.
- **Mất thông điệp khi mạng chập chờn**: Người dùng đi qua hầm mất mạng 5 giây làm lỡ mất tin nhắn -> Khắc phục: Client gửi kèm `last_message_id` khi kết nối lại để máy chủ gửi bù các tin nhắn chưa nhận.

## 6. Step-by-Step Execution Workflow
1. Lựa chọn giao thức: Dùng **SSE** nếu chỉ cần máy chủ đẩy dữ liệu xuống client (thông báo, kết quả AI stream, dashboard); dùng **WebSockets** nếu cần giao tiếp 2 chiều độ trễ thấp (chat, game, collaborative editor).
2. Triển khai cơ chế xác thực (Authentication Handshake): Kiểm tra JWT token ngay tại thời điểm bắt tay kết nối (Connection Handshake); từ chối lập tức nếu token hết hạn.
3. Thiết lập cơ chế Ping-Pong nhịp tim (ví dụ cứ 25 giây gửi Ping) để phát hiện kết nối chết (Ghost connections) và duy trì kết nối qua NAT router.
4. Phân chia kênh giao tiếp theo Phòng (Rooms / Channels) để gửi thông điệp trúng đích thay vì broadcast cho toàn bộ mọi người.
5. Tích hợp Redis Pub/Sub để phát thông điệp xuyên suốt giữa các node máy chủ realtime khác nhau.
6. Phía Client: Triển khai thuật toán Exponential Backoff kèm Jitter khi tự động kết nối lại để không làm tê liệt server khi server vừa khởi động lại.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/realtime/sseController.ts (SSE Streaming chuẩn)
export function streamEvents(req: Request, res: Response) {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache, no-transform');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  const sendEvent = (event: string, data: any) => {
    res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
  };

  const intervalId = setInterval(() => res.write(': keepalive\n\n'), 20000);
  req.on('close', () => clearInterval(intervalId));
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra kết nối WebSocket từ terminal: `wscat -c ws://localhost:3000/ws?token=xxx`
- Kiểm tra luồng Server-Sent Events: `curl -N http://localhost:3000/api/sse-stream`
- Chạy bài kiểm thử giao tiếp thời gian thực: `npm test -- tests/realtime/chatSocket.spec.ts`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Thời gian trễ truyền thông điệp (End-to-End Latency) dưới 50ms trong điều kiện mạng bình thường.
- QG-07: 100% kết nối mới bắt buộc phải vượt qua bước xác thực chữ ký token.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Kiểm tra chặt chẽ `Origin` header trong handshake để ngăn chặn tấn công Cross-Site WebSocket Hijacking (CSWSH).
- Áp dụng Rate Limiting trên số lượng thông điệp mà một client có thể gửi lên trong một giây.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Gateway điều phối kết nối Realtime (`src/realtime/socketGateway.ts`).
- File xử lý xác thực handshake (`src/realtime/authMiddleware.ts`).
- File test tích hợp đa kết nối.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-realtime-protocols**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
