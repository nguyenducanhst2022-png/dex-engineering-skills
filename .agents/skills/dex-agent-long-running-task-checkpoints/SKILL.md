---
name: dex-agent-long-running-task-checkpoints
description: Implement fault-tolerant checkpointing and resumption tokens for long-running AI agent workflows, persisting scratchpad states, tool execution graphs, and recovery idempotency. Use when orchestrating autonomous tasks spanning hours, overnight migrations, or batch refactoring.
---

# dex-agent-long-running-task-checkpoints

## 1. Purpose & Scope
Hiện thực hóa cơ chế lưu điểm kiểm tra chịu lỗi (Fault-Tolerant Checkpointing) và mã phục hồi phiên (Resumption Tokens) cho các tác vụ AI Agent chạy kéo dài nhiều giờ; lưu trữ bền vững trạng thái nháp (Scratchpad States), đồ thị thực thi công cụ và tính bất biến khi khôi phục; đảm bảo Agent có thể tiếp tục công việc ngay tại bước dở dang sau khi máy chủ bị khởi động lại hoặc gặp sự cố gián đoạn.

## 2. When to Use
- Khi AI Agent thực hiện các tác vụ quy mô lớn kéo dài nhiều tiếng (ví dụ: quét và nâng cấp 500 repository mã nguồn qua đêm).
- Khi tiến trình chạy trên hạ tầng đám mây có thể bị ngắt đột ngột (Spot Instances hoặc Kubernetes Pod Eviction).
- Khi cần hỗ trợ người dùng có thể tạm dừng (Pause) và tiếp tục (Resume) tác vụ bất cứ lúc nào.

## 3. When NOT to Use
- Khi tác vụ của Agent hoàn thành nhanh chóng trong vài giây.
- Khi việc chạy lại toàn bộ từ đầu không tốn chi phí và không để lại tác dụng phụ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cơ sở dữ liệu lưu trạng thái bền bỉ (PostgreSQL hoặc Redis), cơ chế định danh duy nhất cho từng bước thực thi (Task Step Hash).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **State Snapshot Serialization:** Đóng gói toàn bộ lịch sử hội thoại, danh sách công việc còn lại và các biến tạm thời thành một chuỗi JSON bất biến.
- **Idempotent Resume Token:** Mỗi điểm checkpoint sinh ra một token mã hóa; khi kích hoạt lại, Agent đọc token để khôi phục đúng ngữ cảnh mà không làm lại các bước đã xong.
- **Transactional Step Commits:** Chỉ đánh dấu bước đã hoàn thành sau khi kết quả đã được ghi nhận bền vững vào đĩa lưu trữ.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo bảng quản lý checkpoint trong cơ sở dữ liệu với các trường `task_id`, `step_index`, `state_blob`, `status`.
2. Sau mỗi bước gọi công cụ thành công, tuần tự hóa trạng thái và lưu một checkpoint mới.
3. Khi tiến trình bị dừng đột ngột và khởi động lại, truy vấn checkpoint mới nhất có trạng thái `SUCCESS`.
4. Tái tạo lại bộ nhớ ngữ cảnh của Agent từ snapshot dữ liệu.
5. Tiếp tục thực thi bước tiếp theo mà không làm lặp lại các bước đã hoàn thành trước đó.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Resilient Agent Checkpoint Manager
export class AgentCheckpointManager {
  async saveCheckpoint(taskId: string, stepIndex: number, scratchpadState: any) {
    const checkpointToken = crypto.randomUUID();
    await db('agent_checkpoints').insert({
      task_id: taskId,
      step_index: stepIndex,
      token: checkpointToken,
      state_payload: JSON.stringify(scratchpadState),
      saved_at: new Date()
    });
    return checkpointToken;
  }

  async resumeFromLatest(taskId: string): Promise<{ stepIndex: number; state: any } | null> {
    const latest = await db('agent_checkpoints')
      .where({ task_id: taskId })
      .orderBy('step_index', 'desc')
      .first();

    if (!latest) return null;
    return {
      stepIndex: latest.step_index,
      state: JSON.parse(latest.state_payload)
    };
  }
}
```

## 8. Anti-Patterns & Common Traps
- Lưu trạng thái trên bộ nhớ RAM của tiến trình, khiến mọi tiến độ bị mất sạch khi server tự động scale hoặc deploy bản vá.
- Khôi phục và chạy lại từ đầu toàn bộ các bước đã làm, dẫn đến việc commit mã nguồn hoặc gọi API bị lặp lại nhiều lần gây lỗi.
- Lưu snapshot quá cồng kềnh chứa toàn bộ dữ liệu nhị phân không cần thiết làm chậm tốc độ ghi checkpoint.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Agent tự động khôi phục và tiếp tục chạy đúng bước tiếp theo sau khi tiến trình bị cưỡng bức dừng (`kill -9`).
- QG-02: Không có bất kỳ bước nào đã hoàn thành bị thực thi lặp lại hai lần gây tác dụng phụ.
- QG-03: Thời gian ghi lưu checkpoint vào đĩa dưới 50ms cho mỗi bước thực thi.

## 10. Security & Safety Boundaries
- Mã hóa các payload trạng thái checkpoint nếu chứa thông tin nhạy cảm của dự án trước khi lưu trữ vào cơ sở dữ liệu.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Hệ thống lưu và khôi phục điểm kiểm tra `AgentCheckpointManager.ts`.
1. Kịch bản kiểm thử phục hồi sau sự cố sập nguồn `crash-recovery-test.ts`.

## 13. Related & Complementary Skills
- [`dex-agent-engineering`](.agents/skills/dex-agent-engineering/SKILL.md)
- [`dex-scheduled-workflows`](.agents/skills/dex-scheduled-workflows/SKILL.md)
- [`dex-reliability-engineering`](.agents/skills/dex-reliability-engineering/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
AI Agent thực hiện nhiệm vụ di chuyển 2,000 tệp tin tài liệu sang cấu trúc mới qua đêm. Chạy đến tệp thứ 1,420 thì máy chủ Kubernetes bị tái khởi động để cập nhật bảo mật. Nhờ `dex-agent-long-running-task-checkpoints`, khi pod mới khởi động lại, Agent đọc checkpoint gần nhất và tiếp tục xử lý mượt mà từ tệp 1,421 đến hết mà không phải chạy lại từ đầu.
