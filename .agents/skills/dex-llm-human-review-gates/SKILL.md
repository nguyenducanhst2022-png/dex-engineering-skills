---
name: dex-llm-human-review-gates
description: Design secure Human-in-the-Loop (HITL) review gates, authorization thresholds, risk-weighted approval policies, and non-blocking interactive approval modals for autonomous agent operations. Use when gating destructive tool execution, database mutations, or financial transactions.
---

# dex-llm-human-review-gates

## 1. Purpose & Scope
Thiết kế các cổng kiểm duyệt có con người tham gia (Human-in-the-Loop - HITL) an toàn và tiện dụng cho các tác vụ tự trị của AI Agent; thiết lập ngưỡng phân loại rủi ro (Risk-Weighted Approval Policies), cơ chế tạm dừng và khôi phục phiên không nghẽn luồng (Non-blocking Resumption) và giao diện duyệt tương tác rõ ràng; ngăn ngừa Agent tự ý thực hiện các hành động có tính phá hủy hoặc gây thiệt hại tài chính.

## 2. When to Use
- Khi AI Agent chuẩn bị thực thi các thao tác có rủi ro cao: xóa cơ sở dữ liệu, sửa đổi cấu hình production, chuyển tiền hoặc gửi email hàng loạt.
- Khi xây dựng hệ thống tự trị trong các lĩnh vực có yêu cầu tuân thủ pháp lý cao (y tế, tài chính, tư pháp).
- Khi cần cơ chế xin phê duyệt nhanh từ kỹ sư phụ trách qua Slack, Teams hoặc giao diện web.

## 3. When NOT to Use
- Khi Agent chỉ thực hiện các thao tác chỉ đọc (Read-only operations) như tìm kiếm tài liệu hoặc phân tích log.
- Khi các tác vụ có rủi ro cực thấp và hoàn toàn có thể tự động hoàn tác (revert) không để lại hậu quả.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Hệ thống hàng đợi thông báo phê duyệt (Webhook, Slack bot hoặc Web UI Modal), cơ chế lưu trạng thái phiên làm việc (Session State Persistence).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Risk-Weighted Policy Engine:** Phân loại hành động thành 3 cấp: Low (Tự động thực thi), Medium (Cần thông báo), High (Bắt buộc con người bấm Approve mới được chạy).
- **Session Suspension & Token Resumption:** Đóng băng trạng thái của Agent và trả về một token phê duyệt; Agent chỉ tiếp tục chạy khi nhận được webhook xác nhận hợp lệ.
- **Transparent Blast Radius Preview:** Hiển thị minh bạch phạm vi tác động (Diff code, số lượng bản ghi bị xóa, số tiền giao dịch) trên giao diện duyệt của con người.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa bảng chính sách rủi ro cho từng công cụ và tham số tương ứng.
2. Trước khi thực thi công cụ, interceptor kiểm tra mức độ rủi ro của hành động.
3. Nếu hành động thuộc diện High Risk, tạm dừng vòng lặp Agent, lưu trạng thái vào cơ sở dữ liệu và gửi thông báo phê duyệt kèm nút Duyệt/Từ chối.
4. Chờ tín hiệu phản hồi từ người dùng có thẩm quyền (kèm xác thực chữ ký điện tử).
5. Nếu được duyệt, nạp lại trạng thái và tiếp tục chu trình; nếu bị từ chối, chuyển thông điệp từ chối vào ngữ cảnh để Agent đổi phương án khác.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Human-in-the-Loop Approval Interceptor
export async function hitlApprovalGate(action: { tool: string; params: any }, userId: string): Promise<boolean> {
  const isDestructive = ['drop_table', 'delete_s3_bucket', 'deploy_production'].includes(action.tool);

  if (!isDestructive) {
    return true; // Auto-approved for safe read/write operations
  }

  // Generate pending review record
  const reviewTicket = await createApprovalTicket({
    requesterAgent: 'dex-devops-agent',
    action: action.tool,
    blastRadius: JSON.stringify(action.params),
    approverRole: 'DevOps-Lead'
  });

  // Notify approver via Slack / UI Modal and await response
  const decision = await waitForHumanApproval(reviewTicket.id, { timeoutMs: 3600000 });
  return decision === 'APPROVED';
}
```

## 8. Anti-Patterns & Common Traps
- Cấu hình ngưỡng duyệt quá nhạy cảm khiến việc đọc một tệp tin cũng bắt con người bấm duyệt, gây ra hiện tượng mệt mỏi duyệt (Approval Fatigue) làm người dùng bấm bừa mà không đọc.
- Tạm dừng bằng lệnh chờ đồng bộ (`while(!approved) sleep()`) làm khóa cứng toàn bộ luồng xử lý của máy chủ.
- Không hiển thị chi tiết tham số mà chỉ hỏi chung chung 'Bạn có đồng ý cho Agent chạy tiếp không?'.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các hành động phá hủy hoặc tài chính đều bắt buộc phải kích hoạt cổng duyệt HITL.
- QG-02: Giao diện phê duyệt hiển thị đầy đủ phạm vi tác động (Blast Radius) và tham số chi tiết.
- QG-03: Có nhật ký ghi nhận danh tính người duyệt (Audit Trail) và dấu thời gian phê duyệt.

## 10. Security & Safety Boundaries
- Xác thực danh tính người phê duyệt bằng cơ chế phân quyền RBAC và xác thực đa yếu tố (MFA); ngăn chặn Agent tự phê duyệt chính mình.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module cổng kiểm duyệt con người `HumanReviewGate.ts`.
1. Bảng phân loại chính sách rủi ro công cụ `tool-risk-policies.json`.

## 13. Related & Complementary Skills
- [`dex-agent-permissions`](.agents/skills/dex-agent-permissions/SKILL.md)
- [`dex-agent-engineering`](.agents/skills/dex-agent-engineering/SKILL.md)
- [`dex-agent-execution-budget-controls`](.agents/skills/dex-agent-execution-budget-controls/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
AI Agent quản trị hạ tầng phát hiện một cụm cơ sở dữ liệu thử nghiệm cũ và chuẩn bị gọi lệnh `drop_database`. Nhờ `dex-llm-human-review-gates`, hành động bị chặn lại ngay lập tức, một thông báo được gửi lên kênh Slack của đội DevOps kèm chi tiết tên database, kỹ sư trưởng kiểm tra thấy database này vẫn còn dữ liệu cần sao lưu nên bấm 'Reject', cứu hệ thống khỏi mất dữ liệu.
