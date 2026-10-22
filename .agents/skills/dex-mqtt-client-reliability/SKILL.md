---
name: dex-mqtt-client-reliability
description: Architect resilient MQTT 3.1.1/5.0 client connections with exponential backoff reconnection, in-flight message queue persistence, QoS 0/1/2 flow control, and clean session lifecycle management. Use when engineering IoT telemetry pipelines, vehicle tracking agents, or edge device gateways.
---

# dex-mqtt-client-reliability

## 1. Purpose & Scope
Thiết kế kiến trúc máy khách MQTT (phiên bản 3.1.1 và 5.0) có độ tin cậy cao; quản lý luồng kết nối kiên cường với thuật toán lùi lũy thừa (Exponential Backoff), duy trì hàng đợi tin nhắn in-flight khi đứt kết nối, điều phối các mức chất lượng dịch vụ QoS 0/1/2 và vòng đời phiên làm việc sạch (Clean Session / Clean Start); phục vụ truyền thông IoT và thiết bị biên.

## 2. When to Use
- Khi xây dựng ứng dụng thu thập dữ liệu cảm biến IoT qua giao thức MQTT.
- Khi máy khách hoạt động trong môi trường mạng di động 3G/4G chập chờn thường xuyên rớt kết nối.
- Khi cần đảm bảo tính toàn vẹn của tin nhắn điều khiển thiết bị không bị mất mát (At-least-once hoặc Exactly-once delivery).

## 3. When NOT to Use
- Khi truyền tải các tệp tin nhị phân dung lượng lớn (>10MB) - nên dùng HTTP/S3.
- Khi cần giao tiếp kiểu yêu cầu-đáp ứng đồng bộ thời gian thực (RPC kiểu REST hoặc gRPC).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** MQTT Broker (EMQX, Mosquitto hoặc HiveMQ), thư viện client (MQTT.js hoặc Paho Python), chứng chỉ số mTLS nếu kết nối bảo mật.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **QoS Levels:** QoS 0 (At most once), QoS 1 (At least once - có gói PUBACK), QoS 2 (Exactly once - 4 bước bắt tay).
- **Keep Alive & Pingreq:** Chu kỳ gửi gói tin nhịp tim giữ kết nối để phát hiện đường truyền chết (Half-open TCP connection).
- **Offline Message Queuing:** Lưu trữ các tin nhắn phát đi khi mất mạng vào bộ nhớ tạm và tự động xả hàng đợi khi kết nối lại.

## 6. Step-by-Step Execution Workflow
1. Cấu hình máy khách MQTT với cờ `clean: false` và `clientId` cố định để giữ phiên đăng ký topic trên Broker.
2. Thiết lập thuật toán tự động kết nối lại với độ trễ ngẫu nhiên (Jittered Exponential Backoff).
3. Triển khai hàng đợi lưu trữ tin nhắn ngoại tuyến trong bộ nhớ hoặc IndexedDB/SQLite.
4. Đăng ký thông điệp di chúc (Last Will and Testament - LWT) để Broker tự động thông báo khi client ngắt kết nối đột ngột.
5. Kiểm thử khả năng phục hồi dữ liệu khi ngắt cáp mạng giả lập 30 giây.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import mqtt, { MqttClient } from 'mqtt';

export function createResilientMqttClient(brokerUrl: string, clientId: string): MqttClient {
  const client = mqtt.connect(brokerUrl, {
    clientId,
    clean: false, // Persistent session
    reconnectPeriod: 1000,
    connectTimeout: 30 * 1000,
    will: {
      topic: `telemetry/${clientId}/status`,
      payload: Buffer.from(JSON.stringify({ status: 'offline', timestamp: Date.now() })),
      qos: 1,
      retain: true
    }
  });

  client.on('offline', () => console.warn('MQTT Client went offline, buffering messages...'));
  client.on('reconnect', () => console.log('Reconnecting to MQTT broker with backoff...'));

  return client;
}
```

## 8. Anti-Patterns & Common Traps
- Sử dụng `clean: true` ngẫu nhiên cho client ID khiến mỗi lần kết nối lại client bị mất toàn bộ danh sách topic đã đăng ký.
- Gửi hàng nghìn tin nhắn QoS 2 cùng lúc làm cạn kiệt số lượng Packet ID khả dụng (tối đa 65,535 IDs).
- Không cấu hình Last Will Testament dẫn đến việc thiết bị mất nguồn nhưng trên dashboard vẫn hiển thị trạng thái online giả tạo.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Không thất thoát bất kỳ tin nhắn QoS 1/2 nào trong kịch bản mất mạng 60 giây.
- QG-02: Tự động kết nối lại thành công trong vòng 5 giây sau khi mạng hồi phục.
- QG-03: Đăng ký thông điệp LWT hợp lệ trên 100% các kết nối thiết bị.

## 10. Security & Safety Boundaries
- Luôn bật mã hóa đường truyền TLS (MQTTS cổng 8883) và sử dụng chứng chỉ thiết bị x509 để xác thực hai chiều mTLS.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module kết nối MQTT kiên cường `ResilientMqttClient.ts`.
1. Hàng đợi tin nhắn ngoại tuyến có lưu trữ `OfflineMessageQueue.ts`.

## 13. Related & Complementary Skills
- [`dex-realtime-protocols`](.agents/skills/dex-realtime-protocols/SKILL.md)
- [`dex-service-contract-simulation`](.agents/skills/dex-service-contract-simulation/SKILL.md)
- [`dex-offline-message-delivery`](.agents/skills/dex-offline-message-delivery/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Hệ thống giám sát đoàn xe vận tải gặp lỗi mất dữ liệu tọa độ GPS mỗi khi xe đi qua đường hầm mất sóng 4G. Kỹ sư kích hoạt `dex-mqtt-client-reliability`, cấu hình hàng đợi lưu đệm trong bộ nhớ flash của thiết bị và thiết lập QoS 1 với LWT, giúp dữ liệu tự động đồng bộ đầy đủ lên máy chủ ngay khi xe ra khỏi hầm.
