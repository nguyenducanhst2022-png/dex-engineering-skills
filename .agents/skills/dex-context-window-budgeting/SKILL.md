---
name: dex-context-window-budgeting
description: Allocate, prioritize, and compress prompt context window token budgets with lost-in-the-middle positioning defense and hard truncation guardrails. Use when orchestrating complex prompts containing large retrieved contexts or multi-turn agent histories.
---

# dex-context-window-budgeting

## 1. Purpose & Scope
Quản lý và phân bổ ngân sách token trong cửa sổ ngữ cảnh của LLM (Context Window Budgeting); áp dụng chiến lược sắp xếp vị trí phòng chống hiện tượng mất thông tin ở giữa (Lost-in-the-Middle Defense), nén ngữ cảnh có ưu tiên, và thực thi các ranh giới cắt cụt cứng (Hard Truncation Guardrails) tránh tràn token.

## 2. When to Use
- Khi xây dựng ứng dụng LLM có nhiều thành phần ngữ cảnh cạnh tranh token (System instructions, Chat history, RAG documents, Few-shot examples, Tool outputs).
- Khi gặp lỗi `context_length_exceeded` từ API nhà cung cấp LLM làm sập ứng dụng người dùng.
- Khi chi phí gọi API LLM tăng vọt do gửi kèm quá nhiều ngữ cảnh không liên quan.

## 3. When NOT to Use
- Khi câu hỏi và câu trả lời rất ngắn, không sử dụng RAG hoặc tài liệu đính kèm.
- Khi sử dụng các mô hình có cửa sổ ngữ cảnh cực lớn (1-2 triệu tokens) và không bị ràng buộc về chi phí lẫn độ trễ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Giới hạn token tối đa của model (`max_context_tokens`), ngân sách dành riêng cho câu trả lời đầu ra (`max_output_tokens`), tokenizer tương ứng.
- **Quyền hạn truy cập:** Quyền điều chỉnh prompt assembly pipeline.

## 5. Core Concepts & Taxonomy
- **Token Budget Partitioning:** Phân chia cửa sổ thành các hạn ngạch cố định: System Prompt (10%), Chat History (20%), Retrieved Context (50%), Buffer & Output (20%).
- **Lost-in-the-Middle Defense:** LLM ghi nhớ thông tin tốt nhất ở phần đầu và phần cuối của prompt; các tài liệu có độ liên quan cao nhất bắt buộc phải được đặt ở đầu hoặc cuối danh sách context.
- **Hierarchical Context Compaction:** Khi vượt ngân sách: trước hết tóm tắt lịch sử trò chuyện cũ, sau đó loại bỏ các tài liệu có điểm liên quan thấp nhất, tuyệt đối không cắt cụt System Prompt.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo Token Budget Manager với giới hạn trần của model (ví dụ: 8,192 tokens cho GPT-4o-mini).
2. Khấu trừ trước ngân sách cho câu trả lời đầu ra (ví dụ: 2,048 tokens) và System Prompt cốt lõi (500 tokens).
3. Đếm số lượng token của các tài liệu RAG truy hồi được bằng tokenizer chính xác (`tiktoken`).
4. Lựa chọn các tài liệu có điểm tương đồng cao nhất cho tới khi lấp đầy ngân sách RAG (ví dụ: tối đa 4,000 tokens).
5. Sắp xếp lại thứ tự tài liệu theo quy tắc: tài liệu quan trọng nhất đặt ở vị trí #1 (đầu), tài liệu quan trọng thứ hai đặt ở vị trí cuối cùng, tài liệu kém quan trọng hơn nằm ở giữa.
6. Áp dụng cơ chế cắt cụt lịch sử chat cũ (chỉ giữ lại $N$ turns gần nhất) để bảo đảm tổng số token của toàn bộ prompt không vượt ngưỡng trần.

## 7. Concrete Examples
### Ví dụ thuật toán sắp xếp tài liệu chống Lost-in-the-Middle trong Python:
```python
def arrange_context_lost_in_the_middle(documents: list[dict]) -> list[dict]:
    # Giả định documents đã được sắp xếp theo độ liên quan giảm dần (Doc 0 là tốt nhất)
    # Thuật toán phân bổ: Xen kẽ đưa tài liệu tốt nhất vào đầu và cuối
    reordered = []
    left = True
    for doc in documents:
        if left:
            reordered.insert(0, doc) # Đưa vào đầu
        else:
            reordered.append(doc)    # Đưa vào cuối
        left = not left
    return reordered

# Kết quả: [Doc 2, Doc 0 (tốt nhất), ..., Doc 1 (tốt nhì)]
# Đảm bảo các tài liệu tốt nhất nằm sát hai biên của Context Window
```

## 8. Anti-Patterns & Common Traps
- **Greedy Unbounded Injection:** Nhồi nhét toàn bộ kết quả tìm kiếm vào prompt mà không đếm token, dẫn tới API trả về mã lỗi 400 Bad Request.
- **Linear Context Stacking:** Đặt tài liệu quan trọng nhất ở giữa 50 trang tài liệu khiến LLM hoàn toàn bỏ sót thông tin quan trọng.
- **Character-Based Budgeting:** Giả định 1 từ = 4 ký tự và dùng hàm `len(text)` để đo độ dài, gây sai số nghiêm trọng khi gặp mã nguồn hoặc văn bản tiếng Việt.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: 100% prompt gửi tới LLM được kiểm tra số lượng token bằng tokenizer chính xác trước khi gọi API mạng.
- **QG-07**: Tỷ lệ prompt bị lỗi `context_length_exceeded` trên môi trường sản xuất bằng chính xác 0%.
- **QG-13**: Các tài liệu truy hồi có điểm tương quan cao nhất luôn được xếp tại vị trí ưu tiên chú ý trong prompt.

## 10. Security & Safety Boundaries
- Giới hạn ngân sách tối đa cho phần nhập liệu của người dùng (User Input) để ngăn chặn các đòn tấn công Denial-of-Service tiêu tốn token.
- Bảo vệ System Prompt không bao giờ bị cắt ngắn hoặc biến dạng khi ngữ cảnh bị đầy.

## 11. Platform Adapters
- **Tokenizers**: `tiktoken` (OpenAI), HuggingFace `AutoTokenizer`, Google `sentencepiece`.
- **Frameworks**: LangChain ContextCompressor, LlamaIndex TokenBudget.

## 12. Deliverables & Output Artifacts
- Module Token Budget Manager với cơ chế phân bổ ngân sách đa thành phần.
- Thuật toán sắp xếp tài liệu Lost-in-the-Middle Defense.
- Bộ unit test kiểm tra cơ chế tự động cắt tỉa lịch sử chat khi vượt trần token.

## 13. Related & Complementary Skills
dex-llm-cost-controls, dex-rag-pipelines, dex-embedding-data-preparation

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử phân bổ ngân sách token và chống tràn context
pytest tests/ai/test_context_window_budgeting.py -v
```
