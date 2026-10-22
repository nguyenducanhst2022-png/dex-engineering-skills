---
name: dex-agent-trace-replay
description: Capture, serialize, and deterministically replay multi-turn AI agent execution traces, step-by-step tool invocations, and environmental observations for debugging and auditing. Use when investigating agent failures, auditing decision provenance, or establishing golden trace regression suites.
---

# dex-agent-trace-replay

## 1. Purpose & Scope
Thu thập, tuần tự hóa và tái hiện có tính xác định (Deterministic Replay) toàn bộ dấu vết thực thi nhiều lượt (Multi-turn Traces) của AI Agent; lưu trữ chi tiết từng lượt suy nghĩ, các lệnh gọi công cụ (Tool Invocations) kèm tham số và phản hồi của môi trường; phục vụ điều tra nguyên nhân sự cố, kiểm toán xuất xứ quyết định và xây dựng bộ kiểm thử hồi quy dấu vết vàng (Golden Traces).

## 2. When to Use
- Khi một AI Agent thực hiện sai một tác vụ trên môi trường sản xuất và cần điều tra chính xác Agent đã 'nghĩ' gì và gọi những công cụ nào.
- Khi cần tái hiện lại từng bước hành động của Agent trong môi trường cục bộ để sửa lỗi mã nguồn mà không tốn chi phí gọi lại LLM.
- Khi xây dựng hồ sơ kiểm toán tuân thủ cho các quyết định tự động của AI.

## 3. When NOT to Use
- Khi chỉ xem nhật ký log văn bản đơn giản của một ứng dụng backend truyền thống.
- Khi cuộc hội thoại chỉ là hỏi đáp một lượt không có bước gọi công cụ (Tool Calling).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Định dạng nhật ký dấu vết chuẩn (OpenTelemetry hoặc file JSONL lưu vết), môi trường giả lập phản hồi công cụ (Tool Mocking).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Deterministic Replay Harness:** Phát lại toàn bộ quá trình chạy của Agent bằng cách nạp lại các phản hồi môi trường đã ghi nhận trước đó mà không cần gọi ra thế giới thực.
- **Step-by-Step Step Through:** Cho phép kỹ sư bấm 'Next Step' để xem trạng thái bộ nhớ ngữ cảnh của Agent biến đổi sau từng lượt gọi công cụ.
- **Divergence Detection:** Tự động so sánh phiên chạy mới với phiên chạy cũ để phát hiện thời điểm và nguyên nhân Agent bắt đầu đi chệch hướng.

## 6. Step-by-Step Execution Workflow
1. Cài đặt middleware ghi vết (Tracing Interceptor) bọc quanh vòng lặp thực thi của Agent.
2. Ghi nhận chi tiết từng bước: `thought`, `tool_name`, `tool_args`, `tool_result`, `tokens_used`, `latency`.
3. Lưu vết thành tệp cấu trúc `trace.jsonl` có gắn mã định danh phiên làm việc và dấu thời gian.
4. Xây dựng kịch bản chạy phát lại (Replay Runner) nạp dữ liệu từ tệp trace để mô phỏng lại toàn bộ phiên.
5. So sánh kết quả đầu ra của lần chạy phát lại với kết quả gốc để lập báo cáo sai khác.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```json
{
  "traceId": "trace-agent-9921",
  "stepIndex": 3,
  "timestamp": "2026-10-22T15:00:02.120Z",
  "agentState": {
    "goal": "Refactor database connection pool",
    "completedSteps": ["Read config.ts", "Run unit tests"]
  },
  "action": {
    "tool": "edit_file",
    "params": {
      "path": "src/db.ts",
      "target": "maxConnections: 10",
      "replacement": "maxConnections: 100"
    }
  },
  "observation": {
    "status": "SUCCESS",
    "bytesModified": 32
  }
}
```

## 8. Anti-Patterns & Common Traps
- Chỉ ghi lại câu trả lời cuối cùng của Agent mà không lưu lại chuỗi suy nghĩ và kết quả gọi công cụ trung gian.
- Lưu tệp trace ở dạng văn bản tự do không có cấu trúc khiến máy tính không thể phân tích hoặc chạy phát lại tự động.
- Không lưu phiên bản của mã nguồn tại thời điểm Agent chạy, khiến việc phát lại trên mã nguồn mới bị lỗi cú pháp.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các lượt gọi công cụ và quan sát môi trường được ghi nhận đầy đủ vào tệp trace.
- QG-02: Bộ công cụ Replay có thể phát lại hoàn hảo phiên làm việc mà không cần kết nối mạng hay gọi LLM API.
- QG-03: Tệp trace tuân thủ đầy đủ định dạng chuẩn hóa JSONL máy đọc được.

## 10. Security & Safety Boundaries
- Tự động làm sạch hoặc che giấu các khóa bí mật (API Keys, Token) trước khi ghi vào tệp trace lưu trữ dài hạn.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Khung ghi nhận và phát lại dấu vết Agent `AgentTraceReplayHarness.ts`.
1. Bản phân tích điều tra sự cố từ trace `AGENT_INCIDENT_INVESTIGATION.md`.

## 13. Related & Complementary Skills
- [`dex-agent-engineering`](.agents/skills/dex-agent-engineering/SKILL.md)
- [`dex-ai-observability`](.agents/skills/dex-ai-observability/SKILL.md)
- [`dex-agent-evaluation-harness`](.agents/skills/dex-agent-evaluation-harness/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Một Agent tự động tạo PR gây lỗi sập bản dựng trên staging nhưng không rõ lý do. Kỹ sư kích hoạt `dex-agent-trace-replay`, nạp tệp `trace-884.jsonl` vào công cụ replay, xem lại từng bước và phát hiện ở bước 4 Agent nhận được lỗi 'File not found' nhưng lại tự động đoán bừa đường dẫn thay vì dừng lại hỏi người dùng.
