---
name: dex-multimodal-evaluation
description: Design evaluation harnesses for vision, audio, and document layout multimodal models, quantifying OCR extraction precision, chart interpretation accuracy, visual grounding, and hallucination rates. Use when validating multimodal document agents, UI automation agents, or visual inspection pipelines.
---

# dex-multimodal-evaluation

## 1. Purpose & Scope
Thiết kế và hiện thực hóa bộ công cụ đánh giá năng lực của các mô hình đa phương thức (Multimodal Evaluation Harness); đo lường định lượng độ chính xác trích xuất văn bản từ hình ảnh (OCR Precision), khả năng thông hiểu biểu đồ số liệu, độ chuẩn xác định vị tọa độ phần tử giao diện (Visual Grounding / Bounding Boxes) và tỷ lệ ảo giác thị giác; phục vụ kiểm định các AI Agent xử lý tài liệu và tự động hóa giao diện.

## 2. When to Use
- Khi xây dựng Agent tự động đọc hóa đơn, chứng từ kế toán hoặc biểu đồ tài chính từ ảnh chụp và tệp PDF.
- Khi đánh giá năng lực điều khiển giao diện người dùng (UI Automation Agent) bằng cách nhận diện các nút bấm trên ảnh màn hình.
- Trước khi phát hành mô hình Vision-Language Model (VLM) cho các tác vụ kiểm tra chất lượng sản phẩm.

## 3. When NOT to Use
- Khi chỉ đánh giá các tác vụ xử lý văn bản thuần túy không có hình ảnh hay âm thanh.
- Khi kiểm tra hiệu năng nén hình ảnh trên mạng CDN (dùng `dex-media-delivery-pipelines`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tập dữ liệu hình ảnh mẫu kèm nhãn chuẩn (Bounding Boxes, Bảng dữ liệu ground truth), thư viện đo lường (Intersection over Union - IoU, Word Error Rate - WER).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Visual Grounding IoU:** Đo lường độ trùng khớp giữa tọa độ hộp bao (Bounding Box) do AI dự đoán với nhãn thật bằng chỉ số IoU (Intersection over Union >= 0.5).
- **Chart Comprehension Precision:** Khả năng đọc đúng số liệu từ trục tung, trục hoành và các thanh biểu đồ mà không bị ảo giác bịa số.
- **Visual Hallucination Rate:** Tỷ lệ mô hình tự miêu tả các vật thể hoặc dòng chữ hoàn toàn không hề có trong bức ảnh.

## 6. Step-by-Step Execution Workflow
1. Thu thập 100 hình ảnh mẫu đa dạng (hóa đơn scan mờ, ảnh chụp màn hình UI phức tạp, biểu đồ nhiều màu sắc).
2. Gắn nhãn chuẩn vị trí các trường dữ liệu và giá trị văn bản tương ứng.
3. Chạy mô hình VLM để trích xuất thông tin có cấu trúc dạng JSON.
4. Tính toán các chỉ số kỹ thuật: Độ chính xác trường dữ liệu (Field-level Accuracy), chỉ số IoU vị trí và tỷ lệ lỗi từ (WER).
5. Lập bảng báo cáo năng lực thị giác của mô hình `MULTIMODAL_EVAL_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Evaluating Bounding Box Visual Grounding IoU
def calculate_iou(boxA: list[int], boxB: list[int]) -> float:
    # box format: [x1, y1, x2, y2]
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return iou
```

## 8. Anti-Patterns & Common Traps
- Chỉ kiểm tra mô hình trên các bức ảnh scan có chất lượng hoàn hảo độ phân giải cao, bỏ qua các ảnh chụp thực tế bị nghiêng, mờ hoặc thiếu sáng.
- Bỏ qua bước đo lường tọa độ phần tử khiến Agent bấm nhầm vào khoảng trống thay vì bấm trúng nút trên màn hình.
- Tin tưởng tuyệt đối vào số liệu đọc được từ biểu đồ mà không có bước kiểm tra đối chiếu tính hợp lý.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Độ chính xác trích xuất số tiền trên hóa đơn đạt tối thiểu 99.5%.
- QG-02: Chỉ số định vị phần tử giao diện IoU trung bình đạt >= 0.75 trên tập dữ liệu UI benchmark.
- QG-03: Tỷ lệ ảo giác thị giác (Visual Hallucinations) duy trì dưới 2% tổng số mẫu thử nghiệm.

## 10. Security & Safety Boundaries
- Đảm bảo hình ảnh thử nghiệm không chứa thông tin thẻ ngân hàng thật hoặc hình ảnh khuôn mặt nhạy cảm khi chưa được làm mờ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo đánh giá năng lực thị giác `MULTIMODAL_EVAL_REPORT.md`.
1. Script tự động tính toán chỉ số IoU và độ chính xác OCR.

## 13. Related & Complementary Skills
- [`dex-multimodal-input-pipelines`](.agents/skills/dex-multimodal-input-pipelines/SKILL.md)
- [`dex-model-evaluation`](.agents/skills/dex-model-evaluation/SKILL.md)
- [`dex-llm-evaluation-dataset-design`](.agents/skills/dex-llm-evaluation-dataset-design/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát triển AI Agent tự động xử lý hóa đơn hoàn tiền. Kỹ sư kích hoạt `dex-multimodal-evaluation` để chạy benchmark trên 200 hóa đơn thực tế, phát hiện mô hình VLM đọc nhầm dấu phẩy và dấu chấm trong số tiền ở 8% các hóa đơn bị mờ, từ đó bổ sung khâu tiền xử lý tăng độ tương phản hình ảnh giúp đưa độ chính xác lên 99.8%.
