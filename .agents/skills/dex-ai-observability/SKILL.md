---
name: dex-ai-observability
description: Implement comprehensive AI observability, OpenTelemetry tracing, LLM spans, token metrics, prompt/completion logging, and Langfuse/Arize integrations. Use when debugging AI agent workflows, tracing complex chains, or monitoring production LLMs.
---

# dex-ai-observability

## 1. Purpose & Scope
Thiết lập hệ thống quan sát toàn diện cho ứng dụng AI (AI Observability & Distributed LLM Tracing); theo dõi chi tiết từng mắt xích trong chuỗi xử lý (Traces, Spans, Generation steps, Tool calls, Retrieval steps) thông qua tiêu chuẩn OpenTelemetry và các nền tảng chuyên dụng (Langfuse, Arize Phoenix, LangSmith), giúp phát hiện lập tức nguyên nhân các câu trả lời sai lệch, độ trễ cao hoặc lỗi trong chuỗi hành động của Agent.

## 2. When to Use
- Khi ứng dụng AI hoạt động qua nhiều bước phức tạp (Agent -> RAG -> Re-rank -> LLM 1 -> Tool Call -> LLM 2) và người dùng phàn nàn câu trả lời bị sai nhưng không ai biết sai ở bước nào.
- Khi thời gian phản hồi của trợ lý ảo quá lâu (> 10 giây) và cần mổ xẻ Flamegraph xem bước nào chiếm nhiều thời gian nhất.
- Khi cần thu thập phản hồi của người dùng (Thumbs up / Thumbs down) để liên kết với các vết thực thi phục vụ cải tiến sản phẩm.

## 3. When NOT to Use
- Ứng dụng chỉ gọi một hàm LLM đơn lẻ một lần duy nhất không có chuỗi xử lý nhiều bước.
- Giám sát các chỉ số hạ tầng máy chủ CPU/RAM thông thường (dùng `dex-production-monitoring`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các bước trong chuỗi AI cần bọc Tracing.
- Nền tảng đích thu thập Trace (Langfuse tự lưu trữ / Cloud, OpenTelemetry Collector, Phoenix).
- Các thẻ metadata cần gắn liền với Trace (User ID, Session ID, Feature Name, Prompt Version).

**Điều kiện tiên quyết:**
- Thư viện OpenTelemetry hoặc SDK chuyên dụng (như `@langfuse/tracer` hoặc `langfuse-python`) đã được cài đặt.
- Đã thiết lập các biến môi trường kết nối tới Observability backend (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tracing Phải Bất Đồng Bộ 100%**: Tuyệt đối không để việc gửi dữ liệu giám sát trace làm tăng độ trễ phản hồi của người dùng; luôn dùng Background Batch Exporter.
- **Làm Sạch Thông Tin Nhạy Cảm Trước Khi Ghi Trace**: Tự động lọc bỏ mật khẩu, số thẻ tín dụng hoặc dữ liệu PII trước khi gửi sang hệ thống quan sát AI tập trung.
- **Sampling Hợp Lý Ở Tải Lớn**: Nếu ứng dụng xử lý hàng triệu requests mỗi ngày, kích hoạt chế độ lấy mẫu (ví dụ: Trace 100% các request bị lỗi, và lấy mẫu 10% các request thành công) để tối ưu chi phí lưu trữ trace.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Hệ thống giám sát bị mất kết nối làm nghẽn ứng dụng chính**: Do SDK cố gắng gửi trace đồng bộ -> Khắc phục: Cấu hình `flushAt: 10`, `flushInterval: 5000` và bọc trong khối try-catch an toàn nuốt lỗi mạng của tracer.
- **Không tìm thấy trace tương ứng khi khách hàng khiếu nại**: Do thiếu `sessionId` xuyên suốt -> Khắc phục: Truyền `traceId` về header phản hồi của client để dễ dàng tra cứu.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo Tracer toàn cục ở đầu vòng đời ứng dụng.
2. Bọc mỗi phiên tương tác của người dùng trong một `Trace` lớn có gắn `sessionId` và `userId`.
3. Tạo các `Span` con đại diện cho từng bước xử lý:
   - *Retrieval Span*: Ghi nhận câu truy vấn tìm kiếm, danh sách chunk văn bản lấy được và điểm tương đồng.
   - *Generation Span*: Ghi nhận System Prompt, User Prompt, Model ID, Temperature, phản hồi thô và số lượng token tiêu thụ.
   - *Tool Call Span*: Ghi nhận tên công cụ, tham số đầu vào và kết quả thực thi của công cụ.
4. Tự động ghi nhận lỗi và ngoại lệ vào span tương ứng nếu bước đó bị thất bại.
5. Tích hợp API ghi nhận phản hồi đánh giá (User Feedback Scores: 1 = Hài lòng, 0 = Không hài lòng) liên kết trực tiếp với trace id.
6. Cấu hình cơ chế gửi trace bất đồng bộ chạy ngầm (Non-blocking background export) để không làm chậm luồng chính của ứng dụng.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/ai/observability/tracer.ts
import { Langfuse } from 'langfuse';
const langfuse = new Langfuse();

export async function runObservedAgentChain(userId: string, question: string) {
  const trace = langfuse.trace({ name: 'agent-qa-chain', userId, input: question });
  
  const retrievalSpan = trace.span({ name: 'vector-retrieval', input: question });
  const context = await retrieveDocuments(question);
  retrievalSpan.end({ output: context.length });
  
  const generation = trace.generation({
    name: 'llm-synthesis',
    model: 'gpt-4o',
    input: [{ role: 'user', content: question }],
  });
  const answer = await callLlm(question, context);
  generation.end({ output: answer.text, usage: answer.usage });
  
  trace.update({ output: answer.text });
  return { answer: answer.text, traceId: trace.id };
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra kết nối tới Langfuse: `curl http://localhost:3000/api/public/health`
- Chạy kịch bản test có tracing: `npm test -- tests/ai/observability.spec.ts`
- Xem cây dấu vết thực thi trên giao diện dashboard của Langfuse.

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các cuộc gọi LLM và Tool Execution đều có Span tương ứng trong hệ thống Tracing.
- QG-10: Cây Trace hiển thị chi tiết thời gian (Latency) và số token tiêu thụ của từng bước xử lý con.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tuân thủ quy định bảo vệ dữ liệu: Dữ liệu prompt và completion hiển thị trong công cụ giám sát phải có cơ chế cấu hình che mờ (Data Masking).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Module quản lý Tracing chuẩn hóa (`src/ai/observability/tracer.ts`).
- File middleware gắn Trace ID cho mỗi phiên làm việc (`src/ai/observability/traceMiddleware.ts`).
- File unit test xác minh các spans được phát đi đúng quy chuẩn.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-ai-observability**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
