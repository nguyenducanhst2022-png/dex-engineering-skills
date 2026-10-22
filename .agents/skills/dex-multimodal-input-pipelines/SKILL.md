---
name: dex-multimodal-input-pipelines
description: Design, validate, and optimize multimodal input pipelines (images, audio, PDF documents) for vision and speech LLMs, managing resolution, token costs, and PII masking. Use when building vision-enabled or voice AI applications.
---

# dex-multimodal-input-pipelines

## 1. Purpose & Scope
Thiết kế, kiểm chứng và tối ưu hóa đường ống xử lý dữ liệu đầu vào đa phương thức (Multimodal Input Pipelines: Hình ảnh, Âm thanh, Video, Tài liệu PDF) cho các mô hình AI đa phương thức (GPT-4o, Claude 3.5 Sonnet, Gemini Pro); tối ưu hóa độ phân giải ảnh, kiểm soát chi phí token hình ảnh, làm sạch dữ liệu riêng tư (PII Masking trên ảnh) và chuẩn hóa định dạng trước khi gửi tới API.

## 2. When to Use
- Xây dựng ứng dụng AI đọc hóa đơn, chứng từ, sơ đồ kiến trúc hoặc phân tích ảnh y tế.
- Tích hợp tính năng nhận diện giọng nói hoặc thị giác máy tính vào AI agent.
- Chi phí API tăng vọt do gửi ảnh độ phân giải quá lớn (4K/8K) mà không qua nén tối ưu.

## 3. When NOT to Use
- Không gửi các tệp video dung lượng lớn trực tiếp tới LLM nếu chỉ cần phân tích vài khung hình chính (hãy trích xuất Keyframes trước).
- Không dùng multimodal LLM đắt tiền cho các tác vụ OCR văn bản đen trắng đơn giản (hãy dùng Tesseract hoặc paddleOCR trước).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File đa phương thức đầu vào (PNG, JPEG, WebP, MP3, WAV, PDF).
- Yêu cầu về độ trễ và ngân sách token cho mỗi request.
- Quy định về bảo mật hình ảnh (làm mờ mặt, bôi đen số tài khoản).
- **Điều kiện tiên quyết**:
- Có thư viện xử lý ảnh và âm thanh (Pillow, Sharp, FFmpeg, pdf2image).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Image Tiling & Vision Tokens: Các mô hình như GPT-4o chia nhỏ ảnh thành các ô vuông (ví dụ 512x512 pixels). Một bức ảnh 4K có thể tiêu tốn tới hơn 2,000 tokens. Thu nhỏ ảnh về độ phân giải chuẩn (ví dụ 1024px cạnh dài nhất) giữ nguyên 99% thông tin nhưng giảm 75% chi phí token.
- Audio Normalization: Chuyển đổi file âm thanh về định dạng 16kHz mono WAV/Opus giúp tăng độ chính xác của mô hình Speech-to-Text.
- Visual PII Scrubbing: Tự động nhận diện và làm mờ khuôn mặt hoặc biển số xe trên ảnh trước khi gửi ra bên ngoài.
- **Quy tắc quyết định kỹ thuật**:
- Tự động resize ảnh về kích thước tối đa 1568px và nén WebP chất lượng 85% trước khi gửi tới LLM.
- Nếu file PDF có hơn 20 trang: trích xuất mục lục và bảng biểu trước, chỉ gửi các trang liên quan thay vì toàn bộ file.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Gửi ảnh định dạng HEIC từ iPhone mà LLM API không hỗ trợ, gây ra lỗi HTTP 400 Bad Request.

## 6. Step-by-Step Execution Workflow
1. Kiểm tra định dạng và tính toàn vẹn của tệp đa phương thức đầu vào.
2. Chuyển đổi định dạng sang chuẩn tương thích (WebP/JPEG cho ảnh, Opus/MP3 cho âm thanh).
3. Tối ưu hóa kích thước và độ phân giải để giảm thiểu chi phí vision tokens.
4. Áp dụng bộ lọc bôi đen dữ liệu nhạy cảm nếu có.
5. Mã hóa Base64 hoặc tải lên S3 an toàn và tạo payload chuẩn gửi tới Multimodal API.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
from PIL import Image
import io
import base64

def prepare_optimized_image_payload(image_bytes: bytes, max_dimension: int = 1200) -> str:
    # Mở và chuẩn hóa ảnh bằng Pillow
    with Image.open(io.BytesIO(image_bytes)) as img:
        # Tự động xoay ảnh theo EXIF orientation
        img = img.convert('RGB')
        # Resize tỷ lệ giữ nguyên khung hình nếu vượt quá max_dimension
        img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        img.save(output, format='WEBP', quality=85)
        # Xuất chuỗi Base64 sẵn sàng cho payload LLM
        return base64.b64encode(output.getvalue()).decode('utf-8')
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra chất lượng và kích thước sau khi tối ưu hóa ảnh
python scripts/test_image_pipeline.py --input sample_receipt.png
```

## 8. Anti-Patterns & Common Traps
- Gửi ảnh thô nguyên bản 20MB trực tiếp từ máy ảnh điện thoại lên Cloud LLM API.
- Bỏ qua metadata EXIF chứa thông tin vị trí GPS nhạy cảm của người dùng.

## 9. Quality Gates & Acceptance Criteria
- Giảm dung lượng payload ảnh trung bình > 60% mà không làm giảm độ chính xác OCR của LLM.
- 100% metadata GPS (EXIF) được xóa sạch trước khi gửi ra API bên ngoài.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quét mã độc trong file tải lên (chống tấn công ImageTragick hoặc zip bomb) trước khi đưa vào pipeline.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Module tiền xử lý đa phương thức tối ưu hóa.
- Tài liệu hướng dẫn định dạng và bảng tính toán chi phí token theo độ phân giải.

## 13. Related & Complementary Skills
dex-structured-llm-output, dex-prompt-injection-defense, dex-supportability-engineering

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng bảo hiểm số tiếp nhận hàng chục ngàn ảnh chụp hiện trường tai nạn xe hơi mỗi ngày. Trước đây, việc gửi ảnh gốc lên GPT-4-Vision tốn $0.08 mỗi bức ảnh và mất 5 giây tải. Áp dụng Multimodal Pipeline nén thông minh sang WebP và xóa EXIF, chi phí giảm xuống còn $0.015/ảnh, thời gian xử lý giảm 65% và hoàn toàn bảo vệ thông tin vị trí của khách hàng.
