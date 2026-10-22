---
name: dex-llm-integration
description: Integrate Large Language Model APIs (OpenAI, Anthropic, Gemini, local Ollama), structured JSON outputs, streaming responses, fallback model routing, and token usage optimization. Use when integrating LLM endpoints, enforcing schema outputs, or building AI-powered features.
---

# dex-llm-integration

## 1. Purpose & Scope
Thiết kế và tích hợp các mô hình ngôn ngữ lớn (Large Language Models - LLMs: OpenAI GPT, Anthropic Claude, Google Gemini, local Ollama) vào ứng dụng phần mềm sản xuất; chuẩn hóa đầu ra có cấu trúc (Structured JSON Outputs / Pydantic / Zod), truyền phát phản hồi theo luồng (Streaming Responses), điều phối mô hình dự phòng (Fallback Model Routing) và tối ưu hóa sử dụng token.

## 2. When to Use
- Khi xây dựng tính năng tóm tắt văn bản, phân loại dữ liệu, trích xuất thực thể hoặc trợ lý ảo thông minh bằng LLM.
- Khi LLM trả về văn bản tự do không đúng định dạng JSON yêu cầu làm sập ứng dụng ở bước sau.
- Khi API của OpenAI bị quá tải (mã lỗi 429 hoặc 503) và cần tự động chuyển sang mô hình Claude hoặc Gemini dự phòng trong 1 giây.

## 3. When NOT to Use
- Xử lý các phép toán logic cố định có thể giải quyết bằng biểu thức chính quy (Regex) hoặc thuật toán thông thường.
- Huấn luyện mô hình từ đầu (Pre-training / Deep Learning training from scratch).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Lựa chọn mô hình mục tiêu (Model ID: `gpt-4o`, `claude-3-5-sonnet`, `gemini-1.5-pro`).
- Cấu trúc JSON Schema mong muốn cho đầu ra.
- Danh sách mô hình dự phòng (Fallback Hierarchy).

**Điều kiện tiên quyết:**
- Có API keys hợp lệ của các nhà cung cấp mô hình AI.
- Thư viện client AI (OpenAI SDK, Vercel AI SDK, LangChain, LiteLLM) sẵn sàng trong dự án.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Structured Output Bắt Buộc Khi Tích Hợp Hệ Thống**: Tuyệt đối không bao giờ dùng prompt dặn 'hãy trả về JSON' một cách mơ hồ; luôn sử dụng tính năng Schema Enforcement chính thức của API.
- **Luôn Có Timeout Nghiêm Ngặt**: Lời gọi LLM có thể bị treo phản hồi hàng phút; luôn đặt `timeout: 15000` (15 giây) để không làm đơ tiến trình máy chủ.
- **Nhiệt Độ (Temperature) Phù Hợp**: Với các tác vụ cần độ chính xác cao, trích xuất dữ liệu hoặc sinh code, đặt `temperature: 0.0` hoặc `0.2`; chỉ tăng `temperature: 0.7+` cho các tác vụ sáng tạo văn thơ.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **LLM bị ảo giác trả về JSON thiếu trường bắt buộc**: Do mô hình nhỏ không tuân thủ schema -> Khắc phục: Sử dụng tính năng Strict JSON Schema của OpenAI hoặc bọc qua vòng lặp sửa lỗi tự động (Pydantic OutputFixingParser).
- **Gặp lỗi 429 Rate Limit làm gián đoạn người dùng**: -> Khắc phục: Áp dụng Exponential Backoff Retry và chuyển tiếp ngay sang mô hình dự phòng.

## 6. Step-by-Step Execution Workflow
1. Đóng gói việc gọi LLM qua một Interface trừu tượng (AI Provider Abstraction) để không bị phụ thuộc vào một nhà cung cấp duy nhất.
2. Ép buộc đầu ra có cấu trúc bằng cơ chế **Structured Outputs** (OpenAI `response_format: { type: 'json_schema' }` hoặc Pydantic / Zod) để đảm bảo 100% kết quả trả về là JSON hợp lệ tuân thủ schema.
3. Triển khai kỹ thuật Streaming: Sử dụng Server-Sent Events (SSE) để truyền phát từng token về frontend, mang lại trải nghiệm chữ chạy tức thì cho người dùng.
4. Thiết lập tầng điều phối dự phòng (Fallback Routing): Bọc lời gọi trong hàm kiểm soát lỗi; nếu Model A trả về lỗi Rate Limit hoặc Timeout, tự động chuyển sang Model B.
5. Bổ sung cơ chế đếm và ghi log số lượng Token (Prompt Tokens, Completion Tokens, Chi phí USD).
6. Viết unit test mock phản hồi của LLM để kiểm chứng tính bền vững của ứng dụng.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/ai/llmService.ts
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const UserSummarySchema = z.object({
  sentiment: z.enum(['POSITIVE', 'NEUTRAL', 'NEGATIVE']),
  keyPoints: z.array(z.string()),
  confidenceScore: z.number().min(0).max(1)
});

export async function analyzeFeedback(text: string) {
  const result = await generateObject({
    model: openai('gpt-4o-mini'),
    schema: UserSummarySchema,
    prompt: `Phân tích ý kiến người dùng sau: ${text}`,
  });
  return result.object; // Đảm bảo đúng 100% kiểu dữ liệu UserSummarySchema
}
```

### Lệnh xác minh & thực thi:
- Chạy unit test tích hợp LLM với mock response: `npm test -- tests/ai/llmService.spec.ts`
- Kiểm tra gọi thử API thực tế: `node scripts/test-llm-call.js`
- Đo thời gian phản hồi token đầu tiên (Time to First Token - TTFT).

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% dữ liệu LLM trả về được xác thực thành công qua Zod / Pydantic schema.
- QG-05: Kịch bản giả lập mô hình chính bị lỗi 503 được hệ thống tự động chuyển sang mô hình phụ thành công.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tuyệt đối không hardcode API key của OpenAI/Anthropic trong mã nguồn hoặc client frontend; mọi lời gọi LLM phải đi qua backend an toàn.
- Làm sạch dữ liệu đầu vào (Prompt Sanitization) để ngăn chặn tấn công Prompt Injection.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Service giao tiếp LLM trừu tượng (`src/ai/llmClient.ts`).
- File định nghĩa Zod Schema cho phản hồi (`src/ai/schemas/extractedData.schema.ts`).
- Bộ test xác minh cơ chế chuyển đổi dự phòng.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-llm-integration**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
