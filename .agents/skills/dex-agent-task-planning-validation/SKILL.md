---
name: dex-agent-task-planning-validation
description: Validate AI agent task decomposition plans before execution, detecting dependency cycles, unachievable prerequisites, missing tool capabilities, and excessive scope creep. Use when engineering autonomous coding agents, multi-step orchestration workflows, or agentic CI pipelines.
---

# dex-agent-task-planning-validation

## 1. Purpose & Scope
Thẩm định và xác thực tính khả thi của kế hoạch phân rã nhiệm vụ (Task Planning Validation) do AI Agent lập ra trước khi cho phép thực thi; phát hiện các chu trình phụ thuộc vòng tròn (Circular Dependencies), các điều kiện tiên quyết không thể đáp ứng, sự thiếu hụt công cụ thực thi và hiện tượng mở rộng phạm vi mất kiểm soát (Scope Creep); đảm bảo Agent hoạt động có kiểm soát và an toàn.

## 2. When to Use
- Khi AI Agent tạo ra một kế hoạch thực hiện gồm nhiều bước phức tạp cần can thiệp vào mã nguồn hoặc hệ thống.
- Trước khi Agent gọi các công cụ tốn kém chi phí hoặc có tính chất ghi/xóa dữ liệu.
- Khi cần kiểm tra xem kế hoạch của Agent có thực sự bám sát mục tiêu của người dùng hay tự ý vẽ ra các việc không liên quan.

## 3. When NOT to Use
- Khi Agent chỉ thực hiện các câu hỏi - đáp đơn giản một bước không cần lập kế hoạch.
- Khi thực hiện các tác vụ tự động hóa tĩnh (Deterministic Scripts) đã được lập trình sẵn thứ tự các bước.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bản kế hoạch dạng cấu trúc JSON do Agent đề xuất, danh sách các công cụ (Tools/Capabilities) khả dụng, các quy tắc an toàn hệ thống.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Directed Acyclic Graph (DAG) Validation:** Đảm bảo đồ thị các bước thực thi là một đồ thị có hướng không có chu trình (không có bước nào tự phụ thuộc vào chính nó).
- **Tool Capability Matching:** Kiểm tra xem mọi thao tác trong từng bước đều có công cụ tương ứng được cấp phép trong danh sách cho phép (Allowlist).
- **Prerequisite Preflight Check:** Xác minh các tài nguyên đầu vào (tệp tin, biến môi trường, quyền hạn) đã sẵn sàng trước khi bước đầu tiên bắt đầu chạy.

## 6. Step-by-Step Execution Workflow
1. Phân tích kế hoạch của Agent thành đồ thị các nhiệm vụ con kèm các quan hệ phụ thuộc (`dependsOn`).
2. Chạy thuật toán sắp xếp tô-pô (Topological Sort) để phát hiện chu trình phụ thuộc lặp vô tận.
3. Đối chiếu từng hành động trong kế hoạch với danh mục quyền hạn của Agent.
4. Tính toán chi phí và thời gian ước tính; nếu vượt ngưỡng cho phép, yêu cầu Agent phân rã lại kế hoạch.
5. Xuất biên bản phê duyệt kế hoạch `PLAN_VALIDATION_REPORT.json` trước khi cấp quyền chạy.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Task Planning DAG & Capability Validator
export interface AgentTaskPlan {
  planId: string;
  tasks: Array<{
    id: string;
    description: string;
    requiredTool: string;
    dependsOn: string[];
  }>;
}

export function validateAgentPlan(plan: AgentTaskPlan, availableTools: Set<string>): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  const taskIds = new Set(plan.tasks.map(t => t.id));

  for (const task of plan.tasks) {
    // 1. Tool availability check
    if (!availableTools.has(task.requiredTool)) {
      errors.push(`Task ${task.id} requires unavailable tool: ${task.requiredTool}`);
    }
    // 2. Dependency existence check
    for (const dep of task.dependsOn) {
      if (!taskIds.has(dep)) {
        errors.push(`Task ${task.id} depends on non-existent task: ${dep}`);
      }
    }
  }

  // 3. Circular dependency detection via cycle detection in DAG
  if (hasCycle(plan.tasks)) {
    errors.push('Circular dependency detected in agent task plan.');
  }

  return { valid: errors.length === 0, errors };
}
```

## 8. Anti-Patterns & Common Traps
- Cho phép AI Agent tự động thực thi một chuỗi 20 bước phức tạp mà không có bước thẩm định tính khả thi của kế hoạch ban đầu.
- Agent lập kế hoạch sử dụng các công cụ tưởng tượng không hề có trong hệ thống (Tool Hallucination).
- Kế hoạch chứa chu trình lặp kín (Bước 2 đợi Bước 3, nhưng Bước 3 lại đợi Bước 2) khiến Agent bị treo vĩnh viễn.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Kế hoạch phân rã nhiệm vụ là một đồ thị DAG hợp lệ 100%, không có chu trình phụ thuộc.
- QG-02: 100% các công cụ được yêu cầu trong kế hoạch đều có sẵn và nằm trong danh sách quyền hạn cho phép.
- QG-03: Mọi điều kiện tiên quyết đều được kiểm tra đạt trước khi kích hoạt bước đầu tiên.

## 10. Security & Safety Boundaries
- Chặn đứng các kế hoạch chứa các bước can thiệp vào tệp cấu hình hệ thống nhạy cảm, xóa cơ sở dữ liệu hoặc kết nối tới các domain lạ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module thẩm định kế hoạch AI Agent `AgentPlanValidator.ts`.
1. Bản đánh giá tính khả thi của kế hoạch `PLAN_VALIDATION_REPORT.json`.

## 13. Related & Complementary Skills
- [`dex-agent-engineering`](.agents/skills/dex-agent-engineering/SKILL.md)
- [`dex-multi-agent-orchestration`](.agents/skills/dex-multi-agent-orchestration/SKILL.md)
- [`dex-agent-loop-safety-cutoffs`](.agents/skills/dex-agent-loop-safety-cutoffs/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
AI Agent lập trình nhận yêu cầu 'Tối ưu hóa hiệu năng website'. Kế hoạch do Agent tự sinh ra có một bước tự ý xóa bỏ toàn bộ thư mục ảnh cũ và một bước phụ thuộc vòng tròn giữa build và test. Nhờ `dex-agent-task-planning-validation`, hệ thống phát hiện lỗi chu trình và công cụ xóa tệp nguy hiểm, từ chối kế hoạch và yêu cầu Agent lập lại phương án an toàn.
