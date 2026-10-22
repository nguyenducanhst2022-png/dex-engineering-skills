---
name: dex-agent-memory-governance
description: Architect, maintain, and govern short-term, working, and long-term memory for AI agents, implementing summarization, eviction, privacy boundaries, and stale context pruning. Use when agents engage in extended multi-turn or multi-day tasks.
---

# dex-agent-memory-governance

## 1. Purpose & Scope
Thiết kế, xây dựng và quản trị hệ thống bộ nhớ cho AI Agents (Short-term Conversation History, Working Memory, Long-term Persistent Memory); áp dụng các chiến lược tóm tắt ngữ cảnh (Context Summarization), đào thải dữ liệu cũ (Stale Context Pruning / Eviction), quản lý ranh giới quyền riêng tư và ngăn ngừa tràn Context Window trong các tác vụ dài hạn.

## 2. When to Use
- Cuộc hội thoại hoặc tác vụ của agent kéo dài nhiều lượt, làm đầy Context Window của LLM (8k/32k/128k tokens) và làm tăng chi phí API theo cấp số nhân.
- Agent bị 'quên' các chỉ dẫn ban đầu do context quá dài hoặc bị nhiễu bởi các thông tin rác từ các bước trước.
- Cần lưu trữ các sở thích và tri thức học được của người dùng qua nhiều phiên làm việc độc lập mà vẫn tuân thủ luật bảo vệ dữ liệu riêng tư (GDPR Right to be Forgotten).

## 3. When NOT to Use
- Không lưu trữ toàn bộ lịch sử thô (Raw Chat Logs) vĩnh viễn vào bộ nhớ của agent mà không có chính sách nén hoặc đào thải.
- Không lưu trữ mật khẩu, khóa bí mật hoặc thông tin thẻ tín dụng vào bộ nhớ dài hạn của agent.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Lịch sử hội thoại hiện tại (Current session messages).
- Giới hạn Context Window của model (ví dụ 128k tokens) và ngân sách chi phí token.
- Cơ sở dữ liệu lưu trữ bộ nhớ dài hạn (PostgreSQL, Redis, Vector DB).
- **Điều kiện tiên quyết**:
- Có hệ thống phân loại mức độ quan trọng của thông tin (Episodic vs Semantic Memory).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Phân loại bộ nhớ AI Agent:
  + Short-term (Scratchpad): Các tin nhắn gần nhất và kết quả thực thi tool tức thì.
  + Working Memory: Kế hoạch hiện tại, trạng thái nhiệm vụ và các biến cần theo dõi.
  + Long-term Memory: Tri thức tổng hợp, thói quen và quy tắc của người dùng được lưu trữ bền vững.
- Context Compression & Summarization: Định kỳ gộp 10 tin nhắn cũ thành 1 đoạn tóm tắt súc tích, giải phóng 80% dung lượng token.
- Memory Pruning & Privacy: Tự động xóa sạch các thông tin tạm thời sau khi nhiệm vụ kết thúc và hỗ trợ lệnh xóa dữ liệu khi người dùng yêu cầu.
- **Quy tắc quyết định kỹ thuật**:
- Nếu Context Window đã sử dụng > 70% dung lượng tối đa: kích hoạt tiến trình tóm tắt và nén bộ nhớ ngắn hạn ngay lập tức.
- Mọi thông tin lưu vào Long-term Memory phải được người dùng đồng thuận hoặc có giá trị sử dụng lại rõ ràng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Lưu giữ các thông tin đã lỗi thời (ví dụ: biến cấu hình cũ đã đổi) trong bộ nhớ dài hạn, khiến agent liên tục đưa ra quyết định sai dựa trên dữ liệu cũ.

## 6. Step-by-Step Execution Workflow
1. Thiết lập cấu trúc lưu trữ 3 tầng cho bộ nhớ agent.
2. Đo lường số lượng tokens của context trước mỗi lượt gọi LLM.
3. Khi vượt ngưỡng 70%: chạy hàm tóm tắt bất đồng bộ (Background summarization) để nén các vòng hội thoại cũ.
4. Trích xuất các sự kiện quan trọng (Key facts) lưu vào Long-term Semantic Store kèm nhãn thời gian (Timestamp).
5. Cung cấp API cho phép người dùng xem, chỉnh sửa hoặc xóa sạch bộ nhớ của agent.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Mô hình quản trị bộ nhớ Agent tự động tóm tắt khi vượt ngưỡng token
class GovernedAgentMemory:
    def __init__(self, max_tokens: int = 8000):
        self.short_term_messages = []
        self.summary_context = ""
        self.max_tokens = max_tokens

    def add_message(self, role: str, content: str):
        self.short_term_messages.append({"role": role, "content": content})
        if self.estimate_tokens() > self.max_tokens:
            self.compress_memory()

    def compress_memory(self):
        # Giữ lại 4 tin nhắn gần nhất, tóm tắt toàn bộ tin nhắn phía trước
        older_msgs = self.short_term_messages[:-4]
        self.summary_context = summarize_dialogue(self.summary_context, older_msgs)
        self.short_term_messages = self.short_term_messages[-4:]
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm thử hành vi ghi nhớ và đào thải ngữ cảnh qua 50 lượt tương tác
pytest tests/test_agent_memory_lifecycle.py
```

## 8. Anti-Patterns & Common Traps
- Gửi toàn bộ lịch sử 100 tin nhắn thô vào mỗi request gây lãng phí hàng ngàn USD tiền token.
- Không gắn timestamp vào các sự kiện trong bộ nhớ dài hạn dẫn đến xung đột thông tin cũ/mới.

## 9. Quality Gates & Acceptance Criteria
- Giữ mức tiêu thụ Context Window luôn ổn định dưới 60% bất kể cuộc hội thoại kéo dài bao lâu.
- 100% dữ liệu PII được loại bỏ trước khi ghi vào kho lưu trữ bộ nhớ dài hạn.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Tuân thủ quy định quyền được lãng quên: cung cấp lệnh xóa hoàn toàn bộ nhớ của user khi có yêu cầu (`/clear-memory`).
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Module quản trị bộ nhớ Agent tích hợp cơ chế nén tự động.
- Bảng điều khiển quản lý và kiểm toán dữ liệu bộ nhớ dài hạn.

## 13. Related & Complementary Skills
dex-agent-evaluation-harness, dex-mcp-server-design, dex-prompt-injection-defense

## 14. Realistic Usage Example
### Tình huống thực tế:
Một AI coding agent hỗ trợ lập trình viên trong dự án kéo dài 3 tháng. Nhờ cơ chế Memory Governance, agent tự động tóm tắt các cuộc thảo luận kỹ thuật hàng ngày thành tài liệu kiến trúc súc tích lưu trong Long-term memory, trong khi xóa sạch các đoạn code tạm thời. Chi phí token duy trì ở mức $0.05/ngày thay vì tăng vọt lên $5.00/ngày.
