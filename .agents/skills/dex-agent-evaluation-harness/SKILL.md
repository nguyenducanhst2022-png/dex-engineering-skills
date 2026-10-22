---
name: dex-agent-evaluation-harness
description: Design, automate, and score end-to-end AI agent trajectory evaluations measuring tool-call accuracy, task success rate, step efficiency, and regression resilience. Use when shipping autonomous agent systems to production.
---

# dex-agent-evaluation-harness

## 1. Purpose & Scope
Thiết kế, tự động hóa và chấm điểm khung đánh giá đường đi hành động của AI Agent (Agent Trajectory Evaluation Harness); đo lường chính xác tỉ lệ hoàn thành nhiệm vụ (Task Success Rate), độ chính xác khi gọi công cụ (Tool Call Precision/Recall), hiệu quả số bước thực thi (Step Efficiency) và khả năng chống suy thoái chất lượng (Regression Resilience) trước khi triển khai agent vào môi trường sản xuất.

## 2. When to Use
- Thay đổi System Prompt, cập nhật danh sách Tools hoặc đổi model nền tảng (ví dụ chuyển từ GPT-4o sang Claude 3.5 Sonnet) và cần biết agent có thông minh hơn hay kém đi.
- Agent bị rơi vào vòng lặp vô hạn (Infinite Loop) hoặc gọi sai thứ tự các công cụ cần thiết.
- Cần thiết lập bộ bài thi chuẩn mực (Benchmark suite) để đo lường độ tin cậy của AI Agent.

## 3. When NOT to Use
- Không đánh giá agent chỉ bằng một vài câu chat thủ công cảm tính trên giao diện web.
- Không chấm điểm thành công chỉ dựa trên việc 'agent không báo lỗi' (cần kiểm tra kết quả thực tế trên môi trường sandbox).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Tập hợp các bài kiểm thử kịch bản thực tế (Evaluation Dataset: Tasks, Expected Outcomes, Allowed Tools).
- Môi trường Sandbox cô lập (Docker container, Mock APIs, Database test).
- Thước đo đánh giá (Metrics: Pass@1, Tool Precision, Token Cost, Execution Steps).
- **Điều kiện tiên quyết**:
- AI Agent có khả năng xuất log chi tiết toàn bộ chuỗi hành động (Trajectory: Thought -> Action -> Observation).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Trajectory Evaluation: Đánh giá không chỉ kết quả cuối cùng mà đánh giá từng bước đi của agent: Agent có chọn đúng tool không? Tham số truyền vào có chuẩn không? Có tự sửa lỗi khi tool trả về error không?
- Deterministic Evaluation Sandbox: Mọi bài test phải bắt đầu từ cùng một trạng thái hệ thống xác định (Clean snapshot) và kết thúc bằng việc kiểm tra trạng thái thực tế (ví dụ: file có được tạo đúng không, DB có được cập nhật đúng bản ghi không).
- Step Efficiency: Agent nào giải quyết được bài toán trong 3 bước sẽ tốt hơn agent mất 12 bước dù cả hai đều hoàn thành.
- **Quy tắc quyết định kỹ thuật**:
- Nếu một bản cập nhật prompt làm giảm Task Success Rate dù chỉ 2%: chặn đứng việc deploy bản cập nhật đó vào production.
- Giới hạn số bước tối đa (Max Steps = 15) để ngắt các agent bị rơi vào vòng lặp vô tận.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Agent tự sinh ra câu trả lời 'Tôi đã hoàn thành xong việc xóa file' nhưng thực tế không hề gọi tool xóa file, khiến việc đánh giá chỉ nhìn vào text bị đánh lừa.

## 6. Step-by-Step Execution Workflow
1. Xây dựng bộ dữ liệu benchmark gồm tối thiểu 30 kịch bản từ dễ đến khó.
2. Thiết lập môi trường chạy thử nghiệm sandbox tự động khôi phục trạng thái sau mỗi bài test.
3. Chạy AI Agent qua toàn bộ bộ đề thi, thu thập toàn bộ nhật ký trajectory.
4. Tự động chấm điểm theo các tiêu chí: Kết quả thực tế, Độ chính xác tool call, Số bước thực hiện.
5. Xuất báo cáo so sánh chi tiết và biểu đồ radar đánh giá năng lực agent.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Harness chấm điểm hành động của AI Agent trên môi trường thực tế
def evaluate_agent_task(task_spec, agent_runner, sandbox_env):
    sandbox_env.reset_to_snapshot(task_spec.initial_state)
    
    trajectory = agent_runner.run(task_spec.prompt, max_steps=10)
    
    # Kiểm tra trạng thái thực tế sau khi agent chạy xong
    actual_state = sandbox_env.get_current_state()
    is_success = task_spec.verify_success(actual_state)
    
    tool_accuracy = calculate_tool_call_precision(trajectory, task_spec.expected_tools)
    
    return {
        "task_id": task_spec.id,
        "success": is_success,
        "steps_taken": len(trajectory.steps),
        "tool_accuracy": tool_accuracy,
        "tokens_used": trajectory.total_tokens
    }
```

### Lệnh xác minh & thực thi:
```bash
# Chạy toàn bộ bộ test suite đánh giá năng lực Agent
python -m evals.run_agent_benchmark --suite=enterprise_devops
```

## 8. Anti-Patterns & Common Traps
- Đánh giá agent bằng cách hỏi chính nó: 'Bạn đã làm xong việc chưa?'.
- Không có timeout hoặc max steps khiến agent chạy hao tốn hàng trăm USD tiền API trong một vòng lặp lỗi.

## 9. Quality Gates & Acceptance Criteria
- Task Success Rate tổng thể phải đạt tối thiểu 85% trên bộ benchmark chuẩn.
- Tỉ lệ gọi sai tool hoặc truyền sai tham số (Invalid Tool Call Rate) dưới 5%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi bài kiểm thử trajectory bắt buộc phải chạy trong môi trường sandbox cô lập không có internet thật.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Khung đánh giá tự động (Evaluation Harness Code).
- Báo cáo kết quả kiểm thử năng lực Agent kèm file ghi vết trajectory.

## 13. Related & Complementary Skills
dex-mcp-server-design, dex-agent-memory-governance, dex-llm-fallback-routing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty xây dựng AI DevOps Agent để tự động sửa lỗi CI/CD. Trước khi release, đội ngũ chạy bộ 50 bài test giả lập lỗi repo trong Docker. Họ phát hiện phiên bản prompt mới khiến agent cố gắng force push Git bừa bãi khi gặp xung đột. Nhờ Evaluation Harness bắt được lỗi này, họ kịp thời bổ sung quy tắc an toàn trước khi đưa vào sử dụng thực tế.
