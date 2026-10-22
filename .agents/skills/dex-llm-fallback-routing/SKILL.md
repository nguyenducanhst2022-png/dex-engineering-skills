---
name: dex-llm-fallback-routing
description: Architect resilient, cost-aware multi-LLM routing, load-balancing, and fallback cascades across providers (OpenAI, Anthropic, DeepSeek, Local Ollama) managing rate limits, context windows, and cost optimization. Use to ensure 99.99% AI availability.
---

# dex-llm-fallback-routing

## 1. Purpose & Scope
Thiết kế, xây dựng và quản trị hệ thống định tuyến thông minh và dự phòng đa mô hình ngôn ngữ (Multi-LLM Fallback & Routing Cascades: OpenAI, Anthropic, Google Gemini, DeepSeek, Local vLLM/Ollama); tự động chuyển đổi nhà cung cấp khi gặp sự cố mạng hoặc lỗi vượt hạn mức (Rate Limits HTTP 429), cân bằng tải và tối ưu hóa chi phí vận hành bằng cách định tuyến tác vụ dễ về model rẻ và tác vụ khó về model mạnh.

## 2. When to Use
- Dịch vụ AI bị gián đoạn hoạt động khi OpenAI hoặc Anthropic gặp sự cố downtime toàn cầu.
- Thường xuyên bị lỗi HTTP 429 (Rate Limit Exceeded) vào giờ cao điểm do vượt quota RPM/TPM.
- Chi phí sử dụng các model cao cấp (GPT-4o, Claude 3.5 Sonnet) quá đắt đỏ cho các tác vụ phân loại văn bản đơn giản.

## 3. When NOT to Use
- Không tự động fallback sang một model quá yếu (ví dụ từ GPT-4 xuống model 7B nhỏ) cho các tác vụ tính toán logic hoặc viết code phức tạp (sẽ làm hỏng chất lượng đầu ra).
- Không triển khai định tuyến quá phức tạp nếu lưu lượng của ứng dụng chỉ có vài trăm request mỗi ngày.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các nhà cung cấp LLM khả dụng và API Keys tương ứng.
- Bảng phân loại độ phức tạp của tác vụ (Task Complexity: Simple, Medium, Complex).
- Ngưỡng ngân sách chi phí và SLA độ trễ cam kết.
- **Điều kiện tiên quyết**:
- Có proxy định tuyến trung gian (LiteLLM, Portkey, Cloudflare AI Gateway, hoặc Custom Router).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Fallback Cascade: Khi Provider A trả về mã lỗi 429 (Rate Limit) hoặc 500/503 (Server Error), hệ thống tự động thử lại ngay lập tức trên Provider B trong vòng 200ms mà người dùng không hề hay biết.
- Semantic / Cost-based Routing: Tác vụ đơn giản (phân loại cảm xúc, trích xuất thực thể) định tuyến về `gpt-4o-mini` hoặc `deepseek-chat` ($0.15/1M tokens); Tác vụ suy luận đa bước định tuyến về `claude-3-5-sonnet` ($3.00/1M tokens), tiết kiệm 80% ngân sách.
- Health Checks & Circuit Breaker: Tự động tạm ngừng gửi traffic tới một provider nếu nó liên tục bị lỗi trong 1 phút qua.
- **Quy tắc quyết định kỹ thuật**:
- Nếu gặp lỗi HTTP 429 hoặc 5xx: kích hoạt fallback sang secondary provider ngay lập tức.
- Nếu độ trễ phản hồi của Provider chính vượt quá 10 giây: kích hoạt timeout và chuyển sang provider dự phòng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Provider dự phòng sử dụng định dạng JSON format khác với provider chính, khiến code backend phía sau bị lỗi parse khi xảy ra fallback.

## 6. Step-by-Step Execution Workflow
1. Cài đặt và cấu hình LiteLLM Proxy hoặc xây dựng Router module nội bộ.
2. Định nghĩa danh sách các Model Groups (ví dụ: nhóm `production-high-reasoning`, nhóm `production-fast-cheap`).
3. Cấu hình chuỗi ưu tiên chuyển đổi dự phòng (Fallback Hierarchy).
4. Thiết lập cơ chế kiểm tra sức khỏe và tự động phục hồi (Cool-down period).
5. Giám sát tỉ lệ định tuyến, độ trễ và chi phí tiết kiệm được trên Dashboard.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
from litellm import completion
import litellm

# Định nghĩa danh sách fallback tự động khi có lỗi
fallback_models = ["claude-3-5-sonnet-20241022", "gpt-4o", "gemini/gemini-1.5-pro"]

def resilient_llm_call(prompt: str):
    try:
        # Thử model ưu tiên số 1, nếu lỗi tự động cascade sang các model sau
        response = completion(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            fallbacks=fallback_models,
            num_retries=2,
            timeout=15
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.critical(f"Toàn bộ các nhà cung cấp LLM đều thất bại: {e}")
        raise ServiceUnavailableException("Hệ thống AI đang bảo trì")
```

### Lệnh xác minh & thực thi:
```bash
# Giả lập lỗi nhà cung cấp chính để kiểm tra cơ chế fallback tự động
pytest tests/test_llm_fallback_resilience.py
```

## 8. Anti-Patterns & Common Traps
- Chỉ phụ thuộc vào một nhà cung cấp LLM duy nhất (Single Point of Failure).
- Cấu hình retry liên tục vào cùng một provider đang bị rate limit 429 khiến tài khoản bị khóa.

## 9. Quality Gates & Acceptance Criteria
- Đạt độ sẵn sàng 99.95% cho các dịch vụ AI người dùng cuối.
- Thời gian chuyển đổi fallback khi model chính lỗi phải dưới 500ms.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi provider trong danh sách fallback đều phải ký thỏa thuận bảo mật dữ liệu doanh nghiệp (Zero Data Retention / BAA).
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- File cấu hình Router LiteLLM / Custom Python Router.
- Dashboard Grafana giám sát chi phí và tỉ lệ fallback giữa các hãng AI.

## 13. Related & Complementary Skills
dex-structured-llm-output, dex-service-failover, dex-load-and-stress-testing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng y tế sử dụng AI để tóm tắt bệnh án. Trong đợt sự cố OpenAI sập toàn cầu vào tháng 11, các đối thủ cạnh tranh đều bị tê liệt dịch vụ. Nhờ kiến trúc Multi-LLM Fallback tự động chuyển hướng sang Claude 3.5 và Google Gemini trong 300ms, hệ thống của họ duy trì hoạt động 100% không một phút gián đoạn.
