---
name: dex-agent-permissions
description: Establish least-privilege security boundaries, human-in-the-loop authorization gates, tool execution sandboxes, and audit logs for autonomous AI agents. Use when restricting agent autonomy, securing tool execution, or gating destructive actions.
---

# dex-agent-permissions

## 1. Purpose & Scope
Thiết lập các ranh giới an toàn và kiểm soát quyền hạn theo nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege) cho AI Coding Agents; thiết lập các cổng phê duyệt bắt buộc có sự tham gia của con người (Human-in-the-Loop Authorization Gates), môi trường cách ly thực thi lệnh (Sandboxing) và ghi nhật ký kiểm toán hành vi (Audit Logging) ngăn chặn Agent tự ý gây ra các hậu quả không thể đảo ngược.

## 2. When to Use
- Khi trao quyền cho AI Agent chạy các lệnh Terminal, thao tác trên cơ sở dữ liệu, hoặc sửa đổi file trong hệ thống.
- Khi cần ngăn chặn Agent tự ý chạy các lệnh nguy hiểm (`git push --force`, `rm -rf`, `DROP TABLE`, `npm publish`).
- Khi hệ thống yêu cầu tuân thủ tiêu chuẩn an ninh nghiêm ngặt trước khi cho phép AI tương tác với tài nguyên sản xuất.

## 3. When NOT to Use
- AI chỉ làm nhiệm vụ đọc hiểu hoặc sinh văn bản gợi ý trong cửa sổ chat không có công cụ thực thi.
- Phân quyền người dùng thông thường trong ứng dụng web (dùng `dex-access-control-tenancy`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh mục các công cụ và lệnh mà Agent có thể yêu cầu thực thi.
- Bảng phân loại mức độ rủi ro (Risk Classification: READ_ONLY, SAFE_WRITE, DANGEROUS/DESTRUCTIVE).
- Cơ chế xác thực người dùng phê duyệt (Interactive Modal / CLI prompt / Webhook approval).

**Điều kiện tiên quyết:**
- Có lớp trung gian (Guardrails / Interceptor) đứng giữa quyết định của Agent và việc thực thi lệnh thật.
- Hệ thống có khả năng tạm dừng tiến trình (Pause Execution) để chờ tín hiệu phê duyệt từ con người.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Nguyên Tắc Mặc Định Từ Chối (Deny by Default)**: Bất kỳ công cụ hoặc lệnh nào không nằm trong danh sách cho phép (Whitelist) đều bị chặn mặc định.
- **Không Cho Phép Tự Động Duyệt Lệnh Phá Hủy**: Cấm tuyệt đối việc cấu hình cờ `--yes` hoặc tự động bypass các bước xác nhận phê duyệt đối với các thao tác Cấp độ 3.
- **Giới Hạn Thời Gian Chờ Phê Duyệt**: Lời nhắc phê duyệt có thời hạn tối đa (ví dụ: 10 phút); nếu con người không phản hồi, tiến trình tự động hủy bỏ an toàn.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Agent cố gắng đọc file SSH private key của lập trình viên**: Do câu lệnh tìm kiếm quét toàn bộ ổ cứng -> Khắc phục: Bộ lọc Path Sandboxing chặn đứng câu lệnh và ghi nhận cảnh báo vi phạm bảo mật.
- **Agent tự ý chạy migration xóa bảng**: -> Khắc phục: Lệnh DDL bị chặn tại Cổng Human-in-the-loop, yêu cầu quản trị viên xác nhận mật khẩu trước khi chạy.

## 6. Step-by-Step Execution Workflow
1. Phân loại mọi hành động của Agent vào 3 cấp độ rủi ro:
   - **Cấp độ 1 (Safe / Auto-approved)**: Đọc file, tra cứu mã nguồn, chạy linter, chạy unit test -> Cho phép tự động thực thi tức thì.
   - **Cấp độ 2 (Moderate / Bounded Write)**: Tạo file mới, chỉnh sửa file trong phạm vi được giao, tạo branch git mới -> Cho phép thực thi tự động nếu nằm trong Scope quy định.
   - **Cấp độ 3 (Dangerous / Destructive)**: Xóa file, chạy migration thay đổi schema DB, commit lên nhánh chính, chạy lệnh bash có quyền root, cài package mới -> BẮT BUỘC dừng lại và yêu cầu con người bấm nút PHÊ DUYỆT (Approve).
2. Kiểm soát ranh giới thư mục (Path Sandboxing): Khóa cứng phạm vi thao tác của Agent bên trong thư mục workspace dự án; cấm tuyệt đối việc đọc ghi ra ngoài thư mục gốc (ngăn truy cập `~/.ssh`, `~/.aws`, `/etc/passwd`).
3. Ghi nhận toàn bộ lệnh, tham số và kết quả vào file nhật ký kiểm toán không thể xóa (`agent_audit.log`).
4. Nếu người dùng từ chối (Reject): Gửi phản hồi từ chối về cho Agent kèm lý do để Agent tìm phương án khác an toàn hơn.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/ai/guardrails/permissionGuard.ts
export async function authorizeAction(action: AgentAction): Promise<boolean> {
  if (action.type === 'READ_FILE' && isInsideWorkspace(action.path)) {
    return true; // Auto-approved
  }
  if (action.isDestructive || action.type === 'DATABASE_MIGRATION') {
    // Dừng lại và kích hoạt Modal xin phê duyệt từ con người
    const approved = await requestHumanApproval({
      prompt: `Agent yêu cầu thực thi thao tác nguy hiểm: ${action.summary}`,
      command: action.command
    });
    return approved;
  }
  return false; // Deny by default
}
```

### Lệnh xác minh & thực thi:
- Chạy kiểm thử bộ lọc bảo vệ quyền hạn: `npm test -- tests/security/agentPermissions.spec.ts`
- Kiểm tra nhật ký kiểm toán của Agent: `tail -n 20 agent_audit.log`
- Giả lập hành vi chạy lệnh nguy hiểm và xác minh lệnh bị chặn thành công.

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-07: 0 lệnh nguy hiểm nào được phép thực thi mà không có chữ ký xác nhận của con người.
- QG-10: 100% các hành động của Agent được ghi lại đầy đủ trong file nhật ký kiểm toán.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Môi trường chạy lệnh của Agent phải được cách ly trong Container (Docker sandbox) hoặc tài khoản người dùng không có quyền `sudo`.
- Tuyệt đối không truyền biến môi trường chứa secrets quản trị hệ thống vào phiên làm việc của Agent.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Middleware kiểm soát quyền thực thi của Agent (`src/ai/guardrails/permissionGuard.ts`).
- File cấu hình ma trận quyền hạn (`config/agent_permissions.json`).
- File nhật ký kiểm toán (`logs/agent_audit.log`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-agent-permissions**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
