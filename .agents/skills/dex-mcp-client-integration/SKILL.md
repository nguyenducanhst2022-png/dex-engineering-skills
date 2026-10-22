---
name: dex-mcp-client-integration
description: Architect type-safe Model Context Protocol (MCP) client connections across Stdio and SSE transports, managing protocol handshakes, dynamic tool discovery, resource subscriptions, and strict schema validation. Use when integrating coding agents with external MCP tool servers.
---

# dex-mcp-client-integration

## 1. Purpose & Scope
Thiết kế kiến trúc máy khách giao thức ngữ cảnh mô hình (Model Context Protocol - MCP Client) an toàn về kiểu dữ liệu (Type-Safe); hỗ trợ cả hai phương thức truyền tải chuẩn Stdio và HTTP Server-Sent Events (SSE), quản lý bắt tay giao thức, khám phá công cụ động (Dynamic Tool Discovery), đăng ký tài nguyên thời gian thực và xác thực lược đồ tham số nghiêm ngặt.

## 2. When to Use
- Khi kết nối AI Agent với các MCP Server chuyên biệt (như SQLite MCP, Git MCP, GitHub MCP, REA MCP).
- Khi xây dựng IDE hoặc ứng dụng máy khách cho phép mở rộng khả năng của AI thông qua hệ sinh thái công cụ MCP.
- Khi cần chuẩn hóa giao tiếp giữa Agent và các công cụ ngoại vi theo tiêu chuẩn công nghiệp mở của Anthropic.

## 3. When NOT to Use
- Khi chỉ gọi các hàm lập trình cục bộ đơn giản trong cùng một tệp mã nguồn.
- Khi giao tiếp máy tính truyền thống không liên quan đến AI hay Model Context Protocol.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư viện SDK chính thức `@modelcontextprotocol/sdk` (TypeScript hoặc Python), máy chủ MCP Server mục tiêu đang chạy.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **MCP Protocol Lifecycle:** Bắt tay khởi tạo (`initialize`) -> Đàm phán năng lực (Capabilities Negotiation) -> Khám phá công cụ (`tools/list`) -> Gọi lệnh (`tools/call`).
- **Transport Flexibility:** Phương thức `StdioClientTransport` cho các tiến trình chạy cục bộ trên máy và `SSEClientTransport` cho các máy chủ từ xa.
- **Dynamic Tool Schema Mapping:** Tự động chuyển đổi các công cụ MCP thành định dạng Tool Calling của OpenAI/Codex hoặc Claude.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo đối tượng Transport phù hợp (Stdio hoặc SSE) với địa chỉ máy chủ mục tiêu.
2. Thực hiện bắt tay giao thức `client.connect(transport)` và xác nhận phiên bản giao thức tương thích.
3. Gọi phương thức `client.listTools()` để lấy danh sách các công cụ được máy chủ hỗ trợ.
4. Ánh xạ schema JSON của từng công cụ MCP sang giao diện gọi hàm của mô hình AI.
5. Khi Agent quyết định gọi công cụ, chuyển tiếp lệnh qua `client.callTool()` và trả kết quả về cho LLM.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

export async function createMcpClient() {
  const transport = new StdioClientTransport({
    command: 'npx',
    args: ['-y', '@modelcontextprotocol/server-filesystem', '/workspace']
  });

  const client = new Client({ name: 'dex-mcp-client', version: '6.0.0' }, { capabilities: {} });
  await client.connect(transport);

  // Discover available tools dynamically
  const tools = await client.listTools();
  console.log('Connected to MCP Server, discovered tools:', tools.tools.map(t => t.name));

  return client;
}
```

## 8. Anti-Patterns & Common Traps
- Gọi công cụ của MCP Server mà không kiểm tra tính hợp lệ của tham số đầu vào bằng JSON Schema, dẫn đến việc máy chủ server bị crash do lỗi dữ liệu.
- Không xử lý việc ngắt kết nối đột ngột của tiến trình Stdio, khiến client bị treo vĩnh viễn khi tiến trình con bị chết.
- Để lộ toàn bộ hệ thống tệp gốc của máy chủ vào quyền điều khiển của MCP Filesystem Server mà không giới hạn thư mục làm việc.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Bắt tay giao thức MCP hoàn tất thành công và liệt kê đầy đủ danh mục công cụ khả dụng.
- QG-02: 100% các cuộc gọi `callTool` đều được kiểm tra kiểu dữ liệu tham số đúng theo schema trước khi truyền tải.
- QG-03: Tự động đóng và giải phóng tiến trình con Stdio sạch sẽ khi ứng dụng kết thúc.

## 10. Security & Safety Boundaries
- Giới hạn nghiêm ngặt quyền hạn của MCP Server thông qua tham số khởi chạy; cấm truy cập ra ngoài thư mục làm việc quy định.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Lớp điều phối máy khách MCP chuẩn `McpClientManager.ts`.
1. Bộ chuyển đổi schema công cụ MCP sang chuẩn OpenAI/Codex Function Calling.

## 13. Related & Complementary Skills
- [`dex-mcp-server-design`](.agents/skills/dex-mcp-server-design/SKILL.md)
- [`dex-tool-calling-contracts`](.agents/skills/dex-tool-calling-contracts/SKILL.md)
- [`dex-rea-adapter`](.agents/skills/dex-rea-adapter/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Xây dựng môi trường làm việc thông minh cho kỹ sư. Kỹ sư kích hoạt `dex-mcp-client-integration` để kết nối AI Agent với GitHub MCP Server và PostgreSQL MCP Server, cho phép Agent tự động đọc cấu trúc bảng dữ liệu và tạo Pull Request giải quyết vấn đề mà không cần viết mã kết nối thủ công.
