---
name: dex-human-ai-workflow-design
description: Architect collaborative human-AI workflows, explicit approval checkpoints, explainability artifacts, and human override intervention channels. Use when deploying autonomous AI systems in high-impact operations requiring human oversight.
---

# dex-human-ai-workflow-design

## 1. Purpose & Scope
Thiết kế kiến trúc quy trình cộng tác giữa Con người và AI (Human-AI Collaborative Workflows); thiết lập các điểm kiểm soát phê duyệt tường minh (Explicit Approval Checkpoints), sinh sinh các tài liệu giải trình quyết định (Explainability Artifacts), và cung cấp kênh can thiệp ghi đè của con người khi AI gặp bế tắc hoặc lệch hướng.

## 2. When to Use
- Khi triển khai các AI Agent có khả năng tự động thực thi các hành động rủi ro cao (chuyển tiền, xóa dữ liệu, gửi email hàng loạt cho khách hàng, thay đổi hạ tầng cloud).
- Khi các quy định pháp lý (như EU AI Act) bắt buộc phải có sự giám sát của con người đối với các hệ thống AI có rủi ro cao (High-risk AI systems).
- Khi cần nâng cao độ tin cậy và sự chấp nhận của nhân viên đối với các công cụ tự động hóa thông minh.

## 3. When NOT to Use
- Khi các tác vụ có tính chất tự động hóa vi mô lặp đi lặp lại với rủi ro bằng 0 (như tự động phân loại thư mục rác).
- Khi yêu cầu về tốc độ xử lý tính bằng mili-giây không cho phép có sự can thiệp của con người (như High-frequency trading).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bản đồ phân cấp rủi ro tác vụ (Task Risk Classification), giao diện người dùng cho việc phê duyệt (Approval UI), cơ chế tạm dừng và tiếp tục luồng xử lý (Pause/Resume State Machine).
- **Quyền hạn truy cập:** Quyền cấu hình workflow orchestrator và phân quyền tài khoản phê duyệt.

## 5. Core Concepts & Taxonomy
- **Human-in-the-Loop (HITL):** Con người đóng vai trò là một mắt xích bắt buộc trong quy trình; AI chỉ được tiếp tục bước tiếp theo sau khi nhận được sự phê duyệt của con người.
- **Decision Audit Trail:** Bản ghi chi tiết giải thích rõ lý do tại sao AI lại đề xuất hành động đó (các dữ liệu đã đọc, suy luận logic, các phương án đã loại trừ).
- **Override Intervention:** Khả năng con người có thể sửa đổi một phần kế hoạch của AI (chỉnh sửa nội dung email, thay đổi số tiền) trước khi nhấn nút phê duyệt.

## 6. Step-by-Step Execution Workflow
1. Phân loại mức độ rủi ro của từng hành động của Agent: Green (Rủi ro thấp - Tự động chạy), Yellow (Rủi ro vừa - Thông báo sau khi chạy), Red (Rủi ro cao - Bắt buộc phê duyệt trước khi chạy).
2. Khi Agent chuẩn bị thực hiện hành động thuộc nhóm Red: tạm dừng tiến trình (Pause Execution) và lưu snapshot trạng thái vào database.
3. Sinh bản tóm tắt giải trình quyết định: tóm tắt mục tiêu, hành động đề xuất, rủi ro tiềm ẩn và các bằng chứng hỗ trợ.
4. Gửi thông báo phê duyệt tới người có thẩm quyền qua Slack/Teams/Email kèm liên kết tới giao diện phê duyệt một chạm.
5. Người phê duyệt có 3 lựa chọn: Phê duyệt (Approve), Từ chối kèm lý do (Reject), hoặc Chỉnh sửa và chạy (Override & Execute).
6. Khi nhận được lệnh phê duyệt: nạp lại snapshot trạng thái và kích hoạt Agent tiếp tục thực thi bước tiếp theo.

## 7. Concrete Examples
### Ví dụ định nghĩa trạng thái tạm dừng chờ con người phê duyệt bằng TypeScript:
```typescript
interface ApprovalRequest {
  taskId: string;
  actionType: 'DELETE_RESOURCES' | 'EXECUTE_PAYMENT' | 'MODIFY_IAM';
  proposedPayload: Record<string, any>;
  justification: string;
  riskScore: number;
}

export class HumanInTheLoopOrchestrator {
  async executeWithApprovalGate(request: ApprovalRequest): Promise<boolean> {
    if (request.riskScore > 0.7) {
      console.log(`Action ${request.actionType} requires human approval. Pausing execution...`);
      
      // 1. Lưu snapshot trạng thái vào database
      await saveTaskCheckpoint(request.taskId, 'AWAITING_HUMAN_APPROVAL', request);

      // 2. Bắn thông báo phê duyệt tới Slack/Webhook
      await sendApprovalNotification(request);

      // 3. Tạm dừng tiến trình và trả về trạng thái chờ
      return false;
    }

    // Tác vụ rủi ro thấp -> Cho phép tự động thực thi
    return true;
  }
}
```

## 8. Anti-Patterns & Common Traps
- **Approval Fatigue:** Bắt con người phải phê duyệt hàng trăm thông báo vụn vặt mỗi ngày, dẫn tới việc nhân viên nhấn nút Approve bừa bãi mà không đọc.
- **Black-Box Requests:** Gửi yêu cầu phê duyệt mà không giải thích lý do tại sao AI lại làm như vậy, khiến con người không thể đánh giá được độ an toàn.
- **No Timeout Policy:** Yêu cầu phê duyệt bị treo vô thời hạn khi người chịu trách nhiệm đi nghỉ phép mà không có cơ chế chuyển cấp (Escalation Policy).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các hành động có mức độ rủi ro cao (phá hủy dữ liệu, tài chính) đều có cổng kiểm duyệt bắt buộc.
- **QG-08**: Bản tóm tắt giải trình quyết định cung cấp đầy đủ liên kết tới dữ liệu nguồn mà AI đã tham khảo.
- **QG-14**: Giao diện phê duyệt có cơ chế xác thực hai lớp (2FA) đối với các hành động đặc quyền.

## 10. Security & Safety Boundaries
- Bảo vệ kênh phê duyệt: ngăn chặn việc giả mạo chữ ký hoặc gửi lệnh phê duyệt giả mạo qua API không được chứng thực.
- Ghi log bất biến toàn bộ danh tính của người đã phê duyệt, thời điểm phê duyệt và phiên bản dữ liệu được phê duyệt.

## 11. Platform Adapters
- **Workflow Engines**: Temporal.io Signals, Camunda BPMN, AWS Step Functions with Task Tokens.
- **Notification**: Slack Block Kit Interactive Messages, Microsoft Teams Adaptive Cards.

## 12. Deliverables & Output Artifacts
- Module Human-in-the-Loop Approval Orchestrator.
- Schema tài liệu giải trình quyết định (Explainability Artifact Schema).
- Bộ kiểm thử tự động quy trình Tạm dừng, Phê duyệt và Tiếp tục thực thi.

## 13. Related & Complementary Skills
dex-llm-human-review-gates, dex-agent-task-planning-validation, dex-ai-safety-red-teaming

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử quy trình Human-in-the-loop tạm dừng và phê duyệt tác vụ
pytest tests/ai/test_human_ai_workflow.py -v
```
