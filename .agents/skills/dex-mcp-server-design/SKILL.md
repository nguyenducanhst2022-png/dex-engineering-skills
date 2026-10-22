---
name: dex-mcp-server-design
description: Architect, implement, and secure Model Context Protocol (MCP) servers exposing tools, resources, and prompts to AI agents with strict JSON-RPC schemas and permission boundaries. Use when connecting agents to enterprise systems.
---

# dex-mcp-server-design

## 1. Purpose & Scope
Thiết kế, xây dựng và bảo mật máy chủ giao thức Model Context Protocol (MCP Servers) theo chuẩn của Anthropic/Linux Foundation; cung cấp công cụ (Tools), tài nguyên (Resources) và lời nhắc mẫu (Prompts) cho các AI Coding Agents thông qua giao thức JSON-RPC chuẩn mực; thiết lập ranh giới thẩm quyền chặt chẽ và cơ chế xác thực an toàn.

## 2. When to Use
- Cần kết nối AI Agent (Claude Desktop, Cursor, OpenAI Codex) với cơ sở dữ liệu nội bộ, hệ thống CI/CD hoặc API doanh nghiệp.
- Xây dựng MCP Server cho phép agent truy vấn dữ liệu nhạy cảm mà không để lộ connection string.
- Chuẩn hóa các công cụ mở rộng của tổ chức theo giao thức chung thay vì viết các wrapper độc quyền.

## 3. When NOT to Use
- Không mở các công cụ có quyền hủy diệt (ví dụ: `drop_database`, `delete_all_files`) mà không có sự xác nhận của người dùng (Human-in-the-loop).
- Không dùng MCP nếu tác vụ chỉ là một script CLI chạy một lần độc lập.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Đặc tả các khả năng cần mở rộng (Tools schema, Resource URIs).
- Giao thức truyền tải mục tiêu (Standard I/O `stdio` hoặc Server-Sent Events `sse`).
- Hệ thống phân quyền và token xác thực.
- **Điều kiện tiên quyết**:
- Đã cài đặt MCP SDK (@modelcontextprotocol/sdk cho TypeScript hoặc mcp cho Python).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Ba trụ cột của MCP:
  + Tools: Các hàm thực thi có side-effect (ví dụ: `run_query`, `create_ticket`) kèm JSON Schema cho tham số đầu vào.
  + Resources: Dữ liệu thụ động chỉ đọc được định danh bằng URI (ví dụ: `postgres://db/schema/tables`).
  + Prompts: Các mẫu tương tác có tham số giúp định hướng cho LLM.
- Human Confirmation: Các tool có tính rủi ro cao phải trả về yêu cầu xác nhận trước khi thực hiện hành động thực tế.
- **Quy tắc quyết định kỹ thuật**:
- Với kết nối cục bộ (Desktop Agent): ưu tiên giao thức truyền tin `stdio` để đảm bảo bảo mật và tốc độ cao.
- Mọi tham số đầu vào của tool bắt buộc phải có mô tả rõ ràng (description) và kiểu dữ liệu JSON Schema chặt chẽ.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cung cấp tool cho phép nhận câu lệnh shell tự do (`exec(cmd)`), khiến kẻ tấn công có thể điều khiển agent chạy lệnh nguy hiểm thông qua Prompt Injection.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo MCP Server sử dụng SDK chính thức của TypeScript hoặc Python.
2. Định nghĩa danh sách các tools kèm JSON Schema cho tham số đầu vào bằng Zod/Pydantic.
3. Đăng ký các hàm xử lý (Handlers) với cơ chế kiểm tra quyền truy cập và giới hạn tài nguyên.
4. Viết kịch bản kiểm thử mô phỏng client JSON-RPC bằng MCP Inspector.
5. Đóng gói và hướng dẫn cấu hình vào file `claude_desktop_config.json`.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';

const server = new Server({ name: 'jira-mcp-server', version: '5.0.0' }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'search_tickets',
    description: 'Tìm kiếm các ticket Jira theo từ khóa',
    inputSchema: {
      type: 'object',
      properties: { query: { type: 'string', description: 'Từ khóa tìm kiếm' } },
      required: ['query']
    }
  }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm thử MCP Server tương tác bằng công cụ chính thức MCP Inspector
npx @modelcontextprotocol/inspector node dist/index.js
```

## 8. Anti-Patterns & Common Traps
- Không xác thực dữ liệu đầu vào của tool và truyền thẳng vào câu truy vấn SQL thô.
- Quá tải agent bằng cách expose hàng trăm tools vụn vặt làm tràn Context Window của LLM.

## 9. Quality Gates & Acceptance Criteria
- 100% schemas của tools vượt qua kiểm tra tính hợp lệ của MCP Specification.
- Phản hồi của tool xử lý dưới 500ms cho các truy vấn dữ liệu cục bộ.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Tuyệt đối không cho phép tool thực thi các lệnh tùy tiện mà không có whitelist lệnh được phép.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Mã nguồn MCP Server hoàn chỉnh.
- File cấu hình tích hợp mẫu cho Claude Desktop / Codex.

## 13. Related & Complementary Skills
dex-structured-llm-output, dex-prompt-injection-defense, dex-agent-memory-governance

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ muốn cho phép AI coding assistant tra cứu thông tin lỗi từ hệ thống Sentry nội bộ. Họ thiết kế một MCP Server bằng TypeScript với tool `get_sentry_issue(issue_id)`. Kỹ sư chỉ cần hỏi 'Tại sao issue SENTRY-404 xảy ra?', agent tự động gọi MCP tool lấy stack trace và phân tích nguyên nhân chỉ trong vài giây.
