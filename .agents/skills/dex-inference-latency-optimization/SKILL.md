---
name: dex-inference-latency-optimization
description: Profile and optimize end-to-end LLM inference latency, tuning Time-to-First-Token (TTFT), tokens-per-second throughput, KV-cache utilization, prompt prefix caching, and speculative decoding. Use when reducing latency in interactive chat agents or real-time voice bots.
---

# dex-inference-latency-optimization

## 1. Purpose & Scope
Đo lường, lập hồ sơ và tối ưu hóa độ trễ suy luận mô hình ngôn ngữ lớn (LLM Inference Latency Optimization); tinh chỉnh thời gian tạo mã đầu tiên (Time-to-First-Token - TTFT), tốc độ xuất chuỗi ký tự (Tokens-per-Second), tối ưu hóa bộ nhớ đệm KV (KV-Cache), tận dụng bộ nhớ đệm tiền tố prompt (Prompt Prefix Caching) và giải thuật giải mã phỏng đoán (Speculative Decoding); phục vụ các ứng dụng trò chuyện thời gian thực và trợ lý giọng nói có độ trễ cực thấp.

## 2. When to Use
- Khi người dùng phàn nàn AI phản hồi quá chậm (>3 giây mới bắt đầu hiện chữ đầu tiên).
- Khi xây dựng trợ lý giọng nói thời gian thực (Voice Agent) yêu cầu độ trễ phản hồi dưới 800ms.
- Khi cần tối ưu hóa chi phí và tài nguyên phần cứng máy chủ GPU phục vụ suy luận mô hình cục bộ (vLLM, Ollama, TensorRT-LLM).

## 3. When NOT to Use
- Khi chạy các tác vụ xử lý hàng loạt ngoại tuyến qua đêm (Batch Processing) không quan tâm đến độ trễ tức thời.
- Khi tối ưu hóa hiệu năng câu lệnh truy vấn cơ sở dữ liệu quan hệ truyền thống.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Hạ tầng phục vụ suy luận LLM (vLLM, TGI hoặc API OpenAI/Anthropic), công cụ đo lường độ trễ mạng và token stream.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Time-to-First-Token (TTFT):** Thời gian từ lúc gửi prompt đến khi nhận được token đầu tiên (phụ thuộc vào giai đoạn Pre-fill của GPU và chiều dài prompt).
- **Prompt Prefix Caching:** Thiết kế cấu trúc prompt sao cho phần cố định dài (System instructions, tài liệu chuẩn) nằm ở đầu để GPU tái sử dụng KV-cache, giảm 80% thời gian TTFT.
- **Speculative Decoding:** Dùng một mô hình nhỏ siêu nhanh (Draft Model) dự đoán trước chuỗi token và dùng mô hình lớn để xác thực song song trong một lượt chạy GPU.

## 6. Step-by-Step Execution Workflow
1. Đo lường phân rã độ trễ: Network Latency, TTFT và Inter-Token Latency (ITL).
2. Cấu trúc lại cấu trúc Prompt: Đặt toàn bộ hướng dẫn cố định và schema ở đầu, chỉ đưa nội dung biến động của người dùng xuống cuối cùng để kích hoạt Prompt Caching.
3. Kích hoạt cơ chế truyền luồng dữ liệu tức thì (Streaming Response qua SSE) để người dùng đọc được chữ ngay khi có token đầu tiên.
4. Cấu hình máy chủ vLLM với cờ tối ưu hóa bộ nhớ đệm `enable-chunked-prefill` và PagedAttention.
5. Kiểm tra và xác nhận chỉ số TTFT giảm xuống dưới ngưỡng mục tiêu (<600ms).

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Profiling TTFT & Streaming Latency in Python
import time
import httpx

async def measure_inference_latency(api_url: str, prompt: str):
    start_time = time.perf_counter()
    ttft = None
    token_count = 0

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", api_url, json={"prompt": prompt, "stream": True}) as response:
            async for chunk in response.aiter_text():
                if ttft is None:
                    ttft = time.perf_counter() - start_time
                token_count += 1
            
            total_time = time.perf_counter() - start_time
            tps = token_count / (total_time - ttft) if total_time > ttft else 0

    print(f"Time to First Token (TTFT): {ttft*1000:.2f}ms")
    print(f"Tokens Per Second (TPS): {tps:.2f} tok/s")
    print(f"Total Latency: {total_time*1000:.2f}ms")
```

## 8. Anti-Patterns & Common Traps
- Chèn các giá trị động thay đổi liên tục (như dấu thời gian hiện tại `Date.now()`) vào ngay dòng đầu tiên của System Prompt làm hỏng hoàn toàn cơ chế Prompt Caching của GPU.
- Chờ đợi mô hình sinh xong toàn bộ câu trả lời 500 từ rồi mới gửi về client cùng lúc thay vì truyền luồng stream.
- Nhồi nhét tài liệu dài 50,000 từ vào prompt mà không cần thiết, làm tăng thời gian Pre-fill lên nhiều giây.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Chỉ số TTFT trên các yêu cầu phổ biến duy trì dưới 600ms nhờ cơ chế Prompt Caching.
- QG-02: 100% các endpoint tương tác trực tiếp với người dùng đều kích hoạt truyền luồng Streaming.
- QG-03: Tốc độ sinh chữ duy trì ổn định tối thiểu 35 tokens/giây.

## 10. Security & Safety Boundaries
- Không tắt bỏ các cơ chế kiểm tra an toàn (Safety Guardrails) chỉ nhằm mục đích giảm độ trễ một vài mili-giây.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module đo lường và tối ưu hóa độ trễ suy luận `InferenceLatencyProfiler.py`.
1. Bản hướng dẫn tái cấu trúc prompt tận dụng tối đa Prompt Prefix Caching.

## 13. Related & Complementary Skills
- [`dex-llm-integration`](.agents/skills/dex-llm-integration/SKILL.md)
- [`dex-ai-observability`](.agents/skills/dex-ai-observability/SKILL.md)
- [`dex-performance-optimization`](.agents/skills/dex-performance-optimization/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trợ lý lập trình viên trong IDE bị phàn nàn vì mỗi lần gõ phím phải đợi 3.5 giây mới hiện gợi ý mã nguồn. Kỹ sư kích hoạt `dex-inference-latency-optimization`, tái cấu trúc prompt đưa tài liệu API cố định lên đầu để kích hoạt Prompt Caching của Anthropic/vLLM, đưa thời gian phản hồi TTFT từ 3,500ms xuống còn 420ms, đem lại trải nghiệm gõ code tức thì mượt mà.
