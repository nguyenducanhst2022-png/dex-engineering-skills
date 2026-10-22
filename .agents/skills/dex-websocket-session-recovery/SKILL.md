---
name: dex-websocket-session-recovery
description: Engineer self-healing WebSocket connection managers with bi-directional heartbeats, sequence-numbered message acknowledgement, backoff reconnection, and state synchronization. Use when building real-time collaboration tools, trading dashboards, or live messaging agents.
---

# dex-websocket-session-recovery

## 1. Purpose & Scope
Thiết kế và xây dựng trình quản lý kết nối WebSocket có khả năng tự phục hồi (Self-Healing WebSocket Manager); tích hợp cơ chế nhịp tim hai chiều (Ping/Pong Heartbeats), xác nhận tin nhắn theo số thứ tự tuần tự (Sequence-Numbered ACK), tự động kết nối lại với độ trễ tăng dần và đồng bộ hóa lại khoảng trống dữ liệu bị mất (Gap Recovery).

## 2. When to Use
- Khi xây dựng bảng điều khiển giao dịch chứng khoán/tiền mã hóa cập nhật giá theo mili-giây.
- Khi phát triển ứng dụng chỉnh sửa cộng tác thời gian thực hoặc phòng chat trực tuyến.
- Khi người dùng thường xuyên bị mất kết nối ngầm (Silent Disconnect) do tường lửa hoặc router cắt socket nhàn rỗi.

## 3. When NOT to Use
- Khi chỉ cần tải dữ liệu một chiều đơn giản từ máy chủ xuống máy khách (nên dùng SSE - Server-Sent Events).
- Khi giao tiếp dạng request-response thông thường có thể giải quyết bằng HTTP REST API.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Máy chủ WebSocket (Node.js `ws`, Socket.io hoặc backend gRPC/Go), kiến thức về giao thức RFC 6455.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Application-Level Heartbeat:** Gửi bản tin định kỳ `{ type: 'ping' }` mỗi 15 giây và hủy kết nối nếu không nhận được `{ type: 'pong' }` trong 5 giây.
- **Message Sequence Offset:** Đánh số tuần tự cho từng thông điệp (`seq: 101, 102, 103`) để máy khách nhận biết khoảng trống khi kết nối lại.
- **Reconnection State Replay:** Gửi yêu cầu `{ type: 'RESYNC', lastSeq: 100 }` để máy chủ phát lại các thông điệp đã bỏ lỡ trong thời gian mất mạng.

## 6. Step-by-Step Execution Workflow
1. Bọc đối tượng `WebSocket` tiêu chuẩn trong lớp quản lý `ResilientWebSocket`.
2. Khởi chạy bộ hẹn giờ gửi tin nhắn nhịp tim Ping định kỳ.
3. Lắng nghe sự kiện `close` và `error` để kích hoạt chu trình thử kết nối lại.
4. Khi kết nối mở lại thành công, tự động gửi thông điệp bắt tay chứa `lastReceivedSequenceId`.
5. Kiểm thử khả năng bù đắp dữ liệu khi ngắt kết nối nhân tạo 10 giây trong lúc máy chủ vẫn liên tục phát sinh dữ liệu.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Resilient WebSocket Client with Heartbeat & Sequence Recovery
export class ResilientWebSocket {
  private ws: WebSocket | null = null;
  private lastSeq = 0;
  private pingTimer?: NodeJS.Timeout;

  constructor(private url: string) {
    this.connect();
  }

  private connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => {
      this.startHeartbeat();
      // Request missed messages since last sequence
      this.ws?.send(JSON.stringify({ type: 'SYNC', lastSeq: this.lastSeq }));
    };
    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'PONG') return;
      if (msg.seq > this.lastSeq) {
        this.lastSeq = msg.seq;
        this.handleMessage(msg.payload);
      }
    };
    this.ws.onclose = () => this.scheduleReconnect();
  }

  private startHeartbeat() {
    this.pingTimer = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'PING' }));
      }
    }, 15000);
  }
}
```

## 8. Anti-Patterns & Common Traps
- Không cài đặt cơ chế Ping/Pong dẫn đến tình trạng kết nối bị đứt ngầm nhưng trình duyệt vẫn tưởng là đang kết nối (Ghost Connection).
- Tự động kết nối lại ngay lập tức theo chu kỳ cứng (`setTimeout(reconnect, 1000)`) mà không có độ trễ lùi, làm sập máy chủ khi vừa khởi động lại.
- Bỏ qua số thứ tự tuần tự khiến người dùng nhận thiếu dữ liệu hoặc bị đảo lộn thứ tự tin nhắn khi mạng bị trễ.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Phát hiện và ngắt kết nối chết (Dead socket) trong vòng tối đa 20 giây nhờ nhịp tim.
- QG-02: 100% các tin nhắn phát sinh trong thời gian ngắt mạng 15 giây được đồng bộ bù đắp lại đầy đủ và đúng thứ tự.
- QG-03: Bộ test tự động kiểm tra rớt mạng ngẫu nhiên đạt tỷ lệ hồi phục hoàn hảo.

## 10. Security & Safety Boundaries
- Luôn sử dụng giao thức bảo mật `wss://`; xác thực phiên làm việc bằng token một lần (Short-lived ticket) truyền trong header hoặc bắt tay đầu tiên.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Lớp máy khách WebSocket kiên cường `ResilientWebSocket.ts`.
1. Giao thức bù đắp dữ liệu thiếu `gap-recovery-protocol.md`.

## 13. Related & Complementary Skills
- [`dex-realtime-protocols`](.agents/skills/dex-realtime-protocols/SKILL.md)
- [`dex-service-contract-simulation`](.agents/skills/dex-service-contract-simulation/SKILL.md)
- [`dex-offline-message-delivery`](.agents/skills/dex-offline-message-delivery/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Ứng dụng đặt lệnh giao dịch chứng khoán bị khách hàng phàn nàn thỉnh thoảng giá cổ phiếu bị dừng không nhảy số mà không báo lỗi. Kỹ sư kích hoạt `dex-websocket-session-recovery`, cài đặt Ping/Pong 15 giây và cơ chế đồng bộ theo số sequence, giúp tự phát hiện kết nối chết, kết nối lại sau 2 giây và kéo toàn bộ biến động giá bị lỡ về màn hình.
