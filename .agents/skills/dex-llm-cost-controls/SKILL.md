---
name: dex-llm-cost-controls
description: Implement LLM token budgeting, semantic caching (GPTCache), cost tracking, rate limiting, and model fallback cascades to optimize API spend. Use when preventing unexpected LLM bills, monitoring token consumption, or enforcing tenant quotas.
---

# dex-llm-cost-controls

## 1. Purpose & Scope
Thiết lập hệ thống kiểm soát và tối ưu hóa chi phí sử dụng API mô hình ngôn ngữ lớn (LLM Cost Controls & Token Budgeting); triển khai bộ nhớ đệm ngữ nghĩa (Semantic Caching), giám sát hạn ngạch sử dụng theo từng người dùng/tenant, cắt giảm token dư thừa và tự động kích hoạt ngắt mạch (Circuit Breaker) khi chi phí chạm ngưỡng cảnh báo, ngăn chặn các hóa đơn tiền điện toán đám mây tăng đột biến ngoài tầm kiểm soát.

## 2. When to Use
- Khi chi phí API OpenAI / Anthropic tăng vọt bất thường do người dùng lạm dụng hoặc do vòng lặp prompt vô tận.
- Khi cần áp đặt hạn mức chi tiêu tối đa (ví dụ: mỗi người dùng miễn phí chỉ được dùng tối đa $0.50 tiền token mỗi ngày).
- Khi các câu hỏi giống hệt nhau liên tục được gửi lên LLM làm tiêu tốn chi phí lặp lại vô ích.

## 3. When NOT to Use
- Ứng dụng chạy các mô hình mã nguồn mở cục bộ tự lưu trữ (Self-hosted Ollama) không tính phí theo token.
- Quản lý ngân sách máy chủ hạ tầng thông thường (dùng `dex-capacity-planning`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bảng giá token cập nhật của từng mô hình (Input Price, Output Price per 1M tokens).
- Ngân sách trần tối đa theo ngày / tháng (Daily / Monthly Cost Cap, ví dụ: $50/ngày).
- Hạn ngạch cấp phát cho từng người dùng hoặc tổ chức (Tenant Quotas).

**Điều kiện tiên quyết:**
- Hệ thống có cơ chế đếm chính xác số lượng Prompt Tokens và Completion Tokens của từng lượt gọi (sử dụng `tiktoken` hoặc dữ liệu `usage` từ API response).
- Có kho lưu trữ phân tán (Redis) để lưu trữ bộ nhớ đệm ngữ nghĩa và theo dõi hạn ngạch thời gian thực.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Luôn Bật Cắt Giảm Lịch Sử Chat**: Trong các ứng dụng Chatbot, không bao giờ gửi lại toàn bộ 50 tin nhắn cũ của lịch sử hội thoại; chỉ gửi tối đa 6-10 tin nhắn gần nhất kèm một đoạn tóm tắt ngắn.
- **Không Gọi Mô Hình Đắt Cho Các Tác Vụ Đơn Giản**: Cấm dùng GPT-4o cho các tác vụ phân loại nhị phân đơn giản (Yes/No classification); các tác vụ này bắt buộc phải dùng mô hình nhỏ nhất.
- **Hard Cap Là Luật Bất Di Bất Dịch**: Tuyệt đối không bao giờ cho phép hệ thống tự động vượt quá ngân sách trần mà không có sự can thiệp phê duyệt nâng hạn mức của con người.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Vòng lặp Agent bị kẹt làm tiêu tốn $500 trong 1 tiếng**: Do Agent liên tục gọi LLM để sửa một lỗi không thể giải quyết -> Khắc phục: Giới hạn tối đa số lượt gọi trong một phiên làm việc (ví dụ: tối đa 20 calls/session) và ngắt mạch ngân sách cấp phiên.
- **Bộ nhớ đệm ngữ nghĩa trả về câu trả lời sai ngữ cảnh**: Do đặt ngưỡng tương đồng quá thấp (80%) -> Khắc phục: Nâng ngưỡng tương đồng lên >= 95% và kiểm tra metadata phạm vi.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo bộ đếm chi phí: Ánh xạ số token tiêu thụ với bảng giá của từng model để tính ra số tiền USD chính xác cho mỗi request.
2. Triển khai **Bộ Nhớ Đệm Ngữ Nghĩa (Semantic Caching)**: Lưu lại các cặp Câu hỏi - Câu trả lời trong Redis; khi có câu hỏi mới có độ tương đồng ngữ nghĩa >= 95% (tính qua vector cosine similarity), lập tức trả về kết quả từ cache với chi phí $0 và độ trễ 5ms.
3. Thiết lập Hạn ngạch người dùng (User Quotas): Sử dụng thuật toán Token Bucket trong Redis; nếu user vượt quá hạn mức được cấp trong ngày, trả về mã lỗi HTTP `429 Too Many Requests - Daily AI Quota Exceeded`.
4. Kỹ thuật nén Prompt (Prompt Compression): Tự động loại bỏ các từ đệm, khoảng trắng thừa và lịch sử chat quá cũ trước khi gửi lên API.
5. Áp dụng Mô hình Phân tầng (Model Cascading): Thử xử lý bằng mô hình siêu rẻ (như GPT-4o-mini hoặc Claude 3.5 Haiku) trước; chỉ khi độ tin cậy thấp mới gọi sang mô hình cao cấp (GPT-4o).
6. Thiết lập Ngắt Mạch Ngân Sách (Hard Spending Limit): Nếu tổng chi phí trong ngày của toàn hệ thống chạm mốc 90% ngân sách trần, tự động phát cảnh báo Slack; nếu chạm 100%, tự động chuyển toàn bộ hệ thống sang chế độ bảo trì hoặc dùng cache.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/ai/cost/costTracker.ts
export async function trackLlmCost(userId: string, model: string, usage: { promptTokens: number; completionTokens: number }) {
  const cost = calculateCostUsd(model, usage.promptTokens, usage.completionTokens);
  const currentDailySpend = await redis.incrbyfloat(`ai:spend:${new Date().toISOString().slice(0, 10)}`, cost);
  
  if (currentDailySpend > GLOBAL_DAILY_HARD_CAP_USD) {
    await triggerEmergencyShutdown('Vượt quá ngân sách AI trần hàng ngày!');
    throw new ServiceUnavailableError('Hệ thống AI tạm thời đạt giới hạn ngân sách hàng ngày.');
  }
  await redis.incrbyfloat(`user:spend:${userId}`, cost);
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra chi phí tiêu thụ hôm nay: `npm run ai:cost-report`
- Kiểm tra tỷ lệ Semantic Cache Hit: `redis-cli get ai:metrics:cache_hit_count`
- Chạy unit test kiểm tra cơ chế ngắt hạn ngạch: `npm test -- tests/ai/costControls.spec.ts`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Tỷ lệ câu hỏi lặp lại được phục vụ qua Semantic Cache đạt tối thiểu >= 25%.
- QG-07: Hệ thống tự động từ chối request và bảo vệ ngân sách khi chạm mốc 100% hạn ngạch.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Semantic Cache phải được cô lập theo `tenant_id` để tránh việc người dùng của công ty A nhận được câu trả lời chứa dữ liệu bí mật từ cache của công ty B.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Module theo dõi chi phí và hạn ngạch (`src/ai/cost/costTracker.ts`).
- Lớp Semantic Cache tích hợp Redis (`src/ai/cost/semanticCache.ts`).
- Dashboard cảnh báo chi phí token hàng ngày.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-llm-cost-controls**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
