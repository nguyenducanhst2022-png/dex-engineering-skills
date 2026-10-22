---
name: dex-end-to-end-engineering
description: Full-lifecycle end-to-end software engineering meta-workflow integrating all 29 DEX engineering skills. Guides software creation from raw idea to production operations, monitoring, and long-term maintenance. Use when building complete applications from scratch, orchestrating complex full-lifecycle projects, or managing end-to-end software delivery.
---

# DEX End-to-End AI Software Engineering

## 1. Purpose & Scope
Tích hợp toàn bộ tinh hoa kỹ thuật từ 29 bài học và kỹ năng DEX thành một quy trình phát triển phần mềm toàn diện từ đầu đến cuối (End-to-End AI Software Engineering Lifecycle); hướng dẫn con người và AI phối hợp nhịp nhàng để biến một ý tưởng sơ khai thành một sản phẩm phần mềm hoàn chỉnh, an toàn, ổn định và có thể vận hành, bảo trì lâu dài.

Quy trình tổng thể 15 giai đoạn:
`Ý tưởng → Yêu cầu → Đặc tả → Kiến trúc → Chia nhiệm vụ → Code → Test → Debug → Review → Bảo mật → Tối ưu → Git → Release → Giám sát → Bảo trì`

Nguyên tắc cốt lõi: **AI đảm nhiệm các công việc kỹ thuật thực thi trong phạm vi được giao. Con người kiểm soát mục tiêu, chất lượng, rủi ro và giữ quyền quyết định phát hành cuối cùng.**
Ghi nhớ sống còn: **Quy trình chuẩn mực = Tạo ra sản phẩm chuyên nghiệp, có thể kiểm chứng, không phụ thuộc vào may rủi.**

## 2. When to Use
- Khi xây dựng một sản phẩm phần mềm hoàn chỉnh từ con số không (Greenfield Product).
- Khi tiếp quản một dự án lớn cần tái cấu trúc và đưa vào quy trình kỹ thuật chuyên nghiệp.
- Khi làm việc với Master Orchestrator trong chế độ STRICT MODE cho các dự án quy mô toàn diện.
- Khi cần tài liệu chuẩn mực hướng dẫn toàn bộ vòng đời phân phối phần mềm.

## 3. When NOT to Use
- Khi chỉ thực hiện một thay đổi nhỏ, sửa lỗi cục bộ (dùng `dex-root-cause-debugging` hoặc QUICK MODE).
- Khi nhiệm vụ chỉ thuần túy là viết một đoạn script nhỏ không có nhu cầu phát hành hay bảo trì dài hạn.

## 4. Prerequisites & Input Context
- Bản mô tả ý tưởng sản phẩm ban đầu hoặc yêu cầu nghiệp vụ từ khách hàng.
- Tài liệu hướng dẫn chi tiết toàn bộ vòng đời tại [full-lifecycle-playbook.md](references/full-lifecycle-playbook.md).
- Ma trận phân công và danh mục 30 kỹ năng chuyên biệt DEX.

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác kỹ thuật phải có thể kiểm chứng độc lập với số liệu rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
Quy trình End-to-End bao gồm 10 Phase chiến lược phối hợp các kỹ năng chuyên biệt:

### Phase 1: Khám Phá & Phân Tích (Discovery & Analysis)
- Đọc hiểu mục tiêu bài toán, phân tích người dùng mục tiêu và ranh giới hệ thống.
- *Kỹ năng kích hoạt*: `dex-context-engineering`.

### Phase 2: Đặc Tả Hướng Kỹ Thuật (Specification & Acceptance Criteria)
- Soạn thảo tài liệu `SPEC.md` chi tiết, định nghĩa các tiêu chí nghiệm thu (Acceptance Criteria) cụ thể theo Given - When - Then.
- *Kỹ năng kích hoạt*: `dex-specification-driven`.

### Phase 3: Thiết Kế Kiến Trúc & Dữ Liệu (Architecture & Data Design)
- Thiết kế mô hình Modular Monolith, phân tầng ranh giới, lập ADR và thiết kế Database Schema chuẩn hóa.
- *Kỹ năng kích hoạt*: `dex-software-architecture`, `dex-database-engineering`, `dex-code-organization`.

### Phase 4: Phân Rã & Giao Nhiệm Vụ (Task Delegation & Planning)
- Lập danh sách `TASKS.md`, chia nhỏ nhiệm vụ kỹ thuật thành các bước khả thi, thiết lập phạm vi và ràng buộc.
- *Kỹ năng kích hoạt*: `dex-task-delegation`, `dex-multi-agent-orchestration`.

### Phase 5: Lập Trình Tăng Dần Có Kiểm Soát (Incremental Implementation)
- Lập trình từng bước nhỏ theo nguyên lý Vibe Coding: Không nâng cấp khi phần trước chưa ổn định.
- *Kỹ năng kích hoạt*: `dex-development-workflow`, `dex-agent-engineering`, `dex-api-engineering`.

### Phase 6: Kiểm Thử Toàn Diện & Sửa Lỗi Tận Gốc (Testing & Debugging)
- Xây dựng kim tự tháp kiểm thử (Unit, Integration, E2E), tái hiện và triệt tiêu lỗi tận gốc rễ.
- *Kỹ năng kích hoạt*: `dex-testing-engineering`, `dex-code-verification`, `dex-root-cause-debugging`.

### Phase 7: Rà Soát Chất Lượng & Tối Ưu Hóa (Review & Optimization)
- Soát từng dòng Git Diff, loại bỏ nợ kỹ thuật, kiểm toán bảo mật OWASP và đo lường benchmark hiệu năng.
- *Kỹ năng kích hoạt*: `dex-code-review`, `dex-security-audit`, `dex-performance-optimization`, `dex-technical-debt-refactoring`.

### Phase 8: Nghiệm Thu Thực Tế & Trải Nghiệm (UAT & UX)
- Kiểm thử hành trình người dùng thực tế trên môi trường Staging, kiểm tra tương thích Responsive và tiêu chuẩn WCAG a11y.
- *Kỹ năng kích hoạt*: `dex-acceptance-testing`, `dex-ux-accessibility`.

### Phase 9: Đóng Gói, Phiên Bản & Phát Hành (Release & Delivery)
- Gắn nhãn Semantic Versioning, cập nhật `CHANGELOG.md`, thiết lập pipeline CI/CD và Feature Flags an toàn.
- *Kỹ năng kích hoạt*: `dex-release-engineering`, `dex-cicd-automation`, `dex-feature-flags`, `dex-git-workflow`.

### Phase 10: Vận Hành, Giám Sát & Tiến Hóa (Operations & Evolution)
- Cấu hình Structured Logging, Health Check, giám sát chỉ số RED và quản lý lộ trình bảo trì dài hạn.
- *Kỹ năng kích hoạt*: `dex-production-monitoring`, `dex-software-maintenance`, `dex-reliability-engineering`.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-end-to-end-engineering
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
Áp dụng đầy đủ **10 Quality Gates (từ QG-01 đến QG-10)** tại các mốc chuyển giai đoạn:
- Không chuyển từ Spec sang Code nếu chưa có Acceptance Criteria (QG-01, QG-02).
- Không chuyển từ Code sang Review nếu Test chưa PASS 100% (QG-03, QG-04, QG-05).
- Không chuyển từ Review sang Release nếu chưa qua Security Audit và Diff Review (QG-06, QG-07, QG-08).
- Không bàn giao nếu thiếu tài liệu và bằng chứng kiểm chứng (QG-09, QG-10).

## 10. Security & Safety Boundaries
- **Tuân Thủ Toàn Bộ 7 Universal Engineering Rules**:
  1. Scope Control.
  2. Test Before Completion.
  3. Root Cause First.
  4. Git Safety.
  5. Security (Zero secret leaks).
  6. No False Completion (Zero hallucinated tests).
  7. Simplicity (KISS & YAGNI).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Toàn bộ mã nguồn hoàn chỉnh của sản phẩm phần mềm.
2. Bộ tài liệu dự án đầy đủ (`README.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, `CHANGELOG.md`).
3. Bộ test suite hoàn chỉnh bao phủ Unit, Integration và E2E tests đạt 100% PASS.
4. Hệ thống CI/CD, kịch bản Release và cấu hình Giám sát vận hành.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-end-to-end-engineering** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
