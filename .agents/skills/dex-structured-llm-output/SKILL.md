---
name: dex-structured-llm-output
description: Enforce reliable, validated JSON schema and Pydantic/Zod structured outputs from LLMs using constrained decoding, tool-calling APIs, and automatic self-correction. Use when LLM outputs drive downstream code execution.
---

# dex-structured-llm-output

## 1. Purpose & Scope
Cưỡng chế và bảo đảm tính tin cậy tuyệt đối của dữ liệu đầu ra có cấu trúc (Structured Outputs: JSON Schema, Pydantic, Zod) sinh ra từ các mô hình ngôn ngữ lớn (LLMs); khai thác tính năng Constrained Decoding (Grammar-based sampling như Outlines/Instructor), OpenAI Structured Outputs Mode, và cơ chế tự động sửa sai (Self-correction loops) khi gặp dữ liệu dị dạng.

## 2. When to Use
- Dữ liệu trả về từ LLM được sử dụng trực tiếp để ghi vào cơ sở dữ liệu hoặc kích hoạt API backend.
- LLM thỉnh thoảng sinh ra JSON lỗi cú pháp (thiếu dấu ngoặc nhọn, thừa dấu phẩy cuối trailing comma, hoặc chèn text giải thích bên ngoài JSON).
- Cần đảm bảo 100% các trường bắt buộc và kiểu dữ liệu (enum, regex) được tuân thủ nghiêm ngặt.

## 3. When NOT to Use
- Không cần cưỡng chế structured output nếu tác vụ chỉ là viết bài luận, sáng tác thơ hoặc trò chuyện tự do với người dùng.
- Không thiết kế schema JSON quá sâu (>5 tầng lồng nhau) làm suy giảm khả năng suy luận logic của LLM.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Lược đồ cấu trúc mong muốn (Pydantic Model trong Python hoặc Zod Schema trong TypeScript).
- System Prompt và User Prompt.
- Cấu hình model (OpenAI `response_format: { type: 'json_schema' }` hoặc Instructor library).
- **Điều kiện tiên quyết**:
- Model API hỗ trợ tính năng Structured Outputs hoặc Function Calling.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Constrained Decoding: Thay vì để LLM chọn token tiếp theo hoàn toàn tự do, engine can thiệp vào Logits Masking ở cấp độ sampler, chỉ cho phép các token hợp lệ theo ngữ pháp của JSON Schema được sinh ra. Tỉ lệ sinh sai cấu trúc = 0%.
- Pydantic Validation & Retry: Nếu LLM vi phạm ràng buộc logic (ví dụ `age < 0`), thư viện tự động nạp thông báo lỗi của Pydantic trở lại context và yêu cầu LLM sửa lại đúng trường đó.
- Schema Descriptions as Prompts: Mô tả (`description`) của từng trường trong schema đóng vai trò như một lời chỉ dẫn trực tiếp cho LLM về ý nghĩa của trường đó.
- **Quy tắc quyết định kỹ thuật**:
- Luôn bật cờ `strict: true` khi sử dụng OpenAI JSON Schema mode.
- Cấu hình tối đa 3 lần thử lại tự động (Auto-retries) nếu quá trình parse schema thất bại.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- LLM trả về chuỗi markdown ```json ... ``` bao quanh JSON, khiến hàm `JSON.parse` thô bị ném lỗi cú pháp (cần hàm extractor làm sạch trước).

## 6. Step-by-Step Execution Workflow
1. Định nghĩa cấu trúc dữ liệu trả về bằng Pydantic model hoặc Zod schema.
2. Cấu hình request gửi tới LLM với tham số `response_format` chuẩn.
3. Parse phản hồi qua schema validation layer.
4. Nếu gặp lỗi validation logic: tự động xây dựng phản hồi sửa sai (Correction prompt) gửi lại LLM.
5. Trả về đối tượng đã được type-safe hoàn toàn cho các tầng nghiệp vụ tiếp theo.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI
import instructor

# Khởi tạo Instructor client bọc ngoài OpenAI
client = instructor.from_openai(OpenAI())

class ExtractedInvoice(BaseModel):
    invoice_number: str = Field(description="Mã số hóa đơn, ví dụ: INV-2026-001")
    total_amount: float = Field(gt=0, description="Tổng số tiền phải lớn hơn 0")
    currency: str = Field(pattern="^[A-Z]{3}$", description="Mã tiền tệ ISO 4217 gồm 3 chữ cái, ví dụ VND, USD")

# Gọi LLM với cam kết cấu trúc 100%
invoice = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=ExtractedInvoice,
    max_retries=3,
    messages=[{"role": "user", "content": "Hóa đơn INV-99 thanh toán 500000 VND hôm qua."}]
)
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm thử độ ổn định cấu trúc trên 100 mẫu văn bản phức tạp
pytest tests/test_structured_extraction.py
```

## 8. Anti-Patterns & Common Traps
- Chỉ dặn dò LLM trong prompt: 'Hãy trả về JSON hợp lệ' mà không dùng API response_format chuyên dụng.
- Viết Regex để bóc tách các trường trong văn bản trả về của LLM thay vì sử dụng structured outputs.

## 9. Quality Gates & Acceptance Criteria
- 100% phản hồi từ LLM được parse thành công sang đối tượng Pydantic/Zod hợp lệ.
- Tỉ lệ cần retry do lỗi cấu trúc dưới 1% tổng số requests.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Kiểm tra và làm sạch các chuỗi ký tự trong output để chống tấn công XSS hoặc SQL Injection trước khi render lên UI hoặc lưu DB.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Module Schema Pydantic/Zod hoàn chỉnh.
- Hàm client wrapper tích hợp cơ chế tự động thử lại khi có lỗi.

## 13. Related & Complementary Skills
dex-mcp-server-design, dex-typescript-type-safety, dex-prompt-injection-defense

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty logistics sử dụng LLM để bóc tách thông tin từ email đặt hàng của khách hàng gửi vào hệ thống ERP. Trước đây, 8% đơn hàng bị lỗi do LLM trả về thiếu trường hoặc sai định dạng ngày tháng. Sau khi áp dụng Instructor Pydantic với OpenAI Structured Outputs, tỉ lệ bóc tách thành công đạt 100% tuyệt đối trên hơn 50,000 đơn hàng.
