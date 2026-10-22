---
name: dex-skill-semantic-deduplication
description: Identify, analyze, and consolidate functionally identical or near-duplicate Agent Skills across repositories using semantic similarity and intent clustering. Use to keep the skill catalog lean, modular, and non-redundant.
---

# dex-skill-semantic-deduplication

## 1. Purpose & Scope
Nhận diện, phân tích và hợp nhất các kỹ năng AI Agent có chức năng tương đương hoặc trùng lặp ngữ nghĩa (Skill Semantic Deduplication); sử dụng thuật toán gom cụm ý định (Intent Clustering) và đo lường khoảng cách ngữ nghĩa giữa các bộ kích hoạt (Activation Triggers) nhằm giữ cho danh mục kỹ năng luôn tinh gọn, ngăn ngừa xung đột điều phối và loại bỏ hiện tượng '10 skills khác tên nhưng cùng làm 1 việc'.

## 2. When to Use
- Khi nhập các bộ kỹ năng lớn từ cộng đồng mã nguồn mở vào hệ sinh thái hiện có.
- Master Orchestrator bị bối rối khi gặp câu hỏi của người dùng vì có 3 kỹ năng khác nhau đều tự nhận là phù hợp.
- Chuẩn hóa và tinh gọn danh mục kỹ năng để tối ưu hóa bộ nhớ và hiệu quả chọn lựa của agent.

## 3. When NOT to Use
- Không vội vã gộp hai kỹ năng có phạm vi chuyên môn khác nhau chỉ vì chúng cùng sử dụng chung một công cụ (ví dụ: `dex-unit-testing` và `dex-mutation-testing` đều dùng pytest nhưng mục đích hoàn toàn khác nhau).
- Không xóa bỏ các kỹ năng đang được tham chiếu bởi các hệ thống khác mà không có kế hoạch chuyển tiếp.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh mục toàn bộ các kỹ năng hiện có kèm mô tả và triggers.
- Mô hình tính toán độ tương đồng ngữ nghĩa (Embedding model hoặc LLM-as-a-Judge).
- Ngưỡng tương đồng phát hiện trùng lặp (Similarity Threshold: ví dụ Cosine > 0.88).
- **Điều kiện tiên quyết**:
- Đã hoàn thành bước khám phá và lập chỉ mục metadata của các skills.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Functional Overlap vs Complementarity:
  + Functional Overlap (Trùng lặp chức năng): Hai kỹ năng có cùng mục đích, cùng nhận input và sinh ra cùng output (ví dụ: `k8s-pod-scaler` và `kubernetes-scaling-expert`). Cần loại bỏ một bản hoặc sáp nhập làm một.
  + Complementarity (Bổ trợ lẫn nhau): Hai kỹ năng thuộc cùng một lĩnh vực nhưng giải quyết 2 giai đoạn khác nhau trong quy trình (ví dụ: `build-container` và `scan-container-sbom`). Cần giữ cả hai và liên kết qua `related_skills`.
- Semantic Matrix: Tính ma trận tương đồng giữa tất cả các cặp kỹ năng để phát hiện các cụm kỹ năng có nguy cơ xung đột điều phối cao nhất.
- **Quy tắc quyết định kỹ thuật**:
- Nếu độ tương đồng ngữ nghĩa giữa 2 skills > 0.88: đưa vào danh sách xem xét hợp nhất (Merge Candidates).
- Ưu tiên giữ lại kỹ năng bản địa (Native DEX Skill) và chỉ chọn lọc những phần tinh hoa của kỹ năng ngoại nhập để bổ sung.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Xóa nhầm một kỹ năng chuyên biệt sâu vì nghĩ rằng kỹ năng tổng quát đã bao hàm nó, làm mất đi các hướng dẫn kỹ thuật chi tiết của chuyên ngành.

## 6. Step-by-Step Execution Workflow
1. Trích xuất mục đích, điều kiện kích hoạt và mô tả của toàn bộ kỹ năng trong danh mục.
2. Sinh embeddings cho từng kỹ năng và tính toán ma trận tương đồng Cosine giữa các cặp.
3. Lọc ra các cặp có độ tương đồng vượt ngưỡng 0.85.
4. Chuyên gia an ninh và kiến trúc sư rà soát từng cặp để đưa ra quyết định: Giữ cả hai, Hợp nhất, hoặc Tách biệt phạm vi.
5. Cập nhật lại mô tả và phần 'When NOT to use' để phân định ranh giới rõ ràng giữa các kỹ năng gần giống nhau.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Phân tích ma trận tương đồng phát hiện kỹ năng trùng lặp ngữ nghĩa
import numpy as np

def detect_duplicate_skills(skills: list[dict], embeddings: list[np.ndarray], threshold=0.88):
    duplicates = []
    n = len(skills)
    for i in range(n):
        for j in range(i + 1, n):
            similarity = np.dot(embeddings[i], embeddings[j]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
            )
            if similarity >= threshold:
                duplicates.append({
                    "skill_a": skills[i]["id"],
                    "skill_b": skills[j]["id"],
                    "similarity_score": round(float(similarity), 3)
                })
    return duplicates
```

### Lệnh xác minh & thực thi:
```bash
# Quét và xuất báo cáo các cặp kỹ năng có nguy cơ trùng lặp
python scripts/audit_skills.py --detect-duplicates
```

## 8. Anti-Patterns & Common Traps
- Giữ nguyên 10 kỹ năng có nội dung na ná nhau chỉ để 'khoe số lượng' kỹ năng nhiều.
- Không định nghĩa rõ phần 'When NOT to use' khiến Master Orchestrator chọn sai kỹ năng khi điều phối.

## 9. Quality Gates & Acceptance Criteria
- 0 cặp kỹ năng nào trong cùng một nhóm có độ tương đồng chức năng trùng lặp 100%.
- Mọi kỹ năng có tính tương đồng cao đều có phần phân định ranh giới rõ ràng trong tài liệu.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quá trình hợp nhất kỹ năng không được làm mất các ranh giới kiểm soát an toàn đã được thiết lập ban đầu.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm toán trùng lặp kỹ năng (Deduplication Audit Report).
- Kế hoạch tinh chỉnh và hợp nhất các kỹ năng trùng lặp.

## 13. Related & Complementary Skills
dex-skill-discovery-indexer, dex-skill-activation-evaluation, dex-skill-dependency-graph

## 14. Realistic Usage Example
### Tình huống thực tế:
Khi nhập kho kỹ năng từ bên ngoài, hệ thống phát hiện có 3 kỹ năng khác nhau: `docker-optimizer`, `container-hardening` và `dex-container-image-engineering`. Thay vì để cả 3 gây rối cho Orchestrator, chuyên gia phân tích cho thấy kỹ năng DEX bản địa đã bao trùm đầy đủ. Hai kỹ năng ngoài được chuyển thành tài liệu tham khảo và catalog duy trì duy nhất một kỹ năng chuẩn mực, tối ưu hóa độ chính xác định tuyến.
