# DEX Engineering Skills Pack v1.0.0

> **Bộ kỹ năng kỹ thuật phần mềm thực chiến toàn diện dành cho AI Coding Agents, chuyển đổi từ chương trình 30 bài học Vibe Coding kinh điển.**

Tuân thủ nghiêm ngặt chuẩn mở **Agent Skills Specification** ([agentskills.io](https://agentskills.io/specification)), tương thích trực tiếp với **OpenAI Codex**, **Google Antigravity**, **Claude Code**, **Cursor**, **Windsurf** và các hệ thống AI Agent hỗ trợ chuẩn Agent Skills.

---

## 1. Giới Thiệu & Triết Lý Cốt Lõi

**DEX Engineering Skills Pack** không phải là một tập hợp các prompt rời rạc hay tài liệu lý thuyết suông. Đây là một khung kỹ năng phần mềm (Engineering Skill Framework) hoàn chỉnh, có khả năng thực thi thực tế trong môi trường phát triển dự án.

Mỗi kỹ năng được thiết kế như một quy trình kỹ thuật độc lập, có quy định đầu vào, các bước thực thi, ranh giới an toàn, điều kiện kiểm chứng (Quality Gates) và bằng chứng đầu ra có thể kiểm tra định lượng.

### Triết lý Vận hành Bất Biến:
```
Analyze → Specify → Plan → Implement → Verify → Debug → Stabilize → Review → Commit → Release → Maintain
```

**Nguyên tắc vàng**:
1. Không nâng cấp hoặc thêm tính năng khi hệ thống hiện tại chưa chạy ổn định.
2. AI đảm nhiệm các công việc kỹ thuật trong phạm vi được giao; bạn kiểm soát mục tiêu, chất lượng, rủi ro và quyết định phát hành.
3. Không tin AI báo "hoàn thành" khi chưa có bằng chứng kiểm thử thực nghiệm từ terminal.

---

## 2. Master Orchestrator (`dex-master-orchestrator`)

Đóng vai trò là "Nhạc trưởng điều phối", Master Orchestrator là điểm tiếp nhận đầu tiên của mọi tác vụ.

### Nhiệm Vụ Của Orchestrator:
- **Triage**: Phân tích yêu cầu của người dùng và xác định bản chất tác vụ (Bugfix, Feature, Performance, Security, Refactor, Release, Greenfield).
- **Mode Selection**: Tự động đề xuất 1 trong 3 chế độ thực thi thông minh:
  - **QUICK MODE**: Dành cho sửa lỗi nhỏ, chỉnh sửa UI nhẹ, cập nhật cấu hình đơn giản.
  - **STANDARD MODE**: Dành cho phát triển tính năng mới, refactor module vừa.
  - **STRICT MODE**: Dành cho thay đổi kiến trúc, DB migration, xác thực/bảo mật, phát hành Production.
- **Minimal Routing**: Chỉ chọn đúng tập kỹ năng tối thiểu cần thiết; không kích hoạt các kỹ năng thừa thãi.
- **Quality Gates Enforcement**: Kiểm soát 10 cổng chất lượng (QG-01 đến QG-10); chặn không cho chuyển giai đoạn nếu bài kiểm tra chưa đạt PASS.
- **Reporting**: Tổng hợp báo cáo kiểm chứng minh bạch kèm terminal output và mã commit an toàn.

---

## 3. Danh Mục 30 Kỹ Năng Chuyên Biệt (Specialized Skills Catalog)

### Nhóm 1: Foundation (Nền tảng Kỹ thuật — Bài 1 đến 6)
- [`dex-development-workflow`](.agents/skills/dex-development-workflow/SKILL.md): Quy trình Vibe Coding chuẩn mực: Chia nhỏ → Code → Test → Sửa → Ổn định → Git → Nâng cấp.
- [`dex-task-delegation`](.agents/skills/dex-task-delegation/SKILL.md): Giao việc chuẩn cho AI: Mục tiêu → Phạm vi → Ràng buộc → Viết code → Kiểm tra → Báo cáo.
- [`dex-code-verification`](.agents/skills/dex-code-verification/SKILL.md): Xác minh chất lượng mã nguồn thực tế, triệt tiêu việc báo hoàn thành ảo.
- [`dex-git-workflow`](.agents/skills/dex-git-workflow/SKILL.md): Quản lý Git an toàn: Commit là điểm lưu an toàn, Branch là khu vực thử nghiệm.
- [`dex-code-organization`](.agents/skills/dex-code-organization/SKILL.md): Tổ chức cấu trúc thư mục sạch, phân tách module, loại bỏ god-files.
- [`dex-root-cause-debugging`](.agents/skills/dex-root-cause-debugging/SKILL.md): Tái hiện lỗi bằng failing test, sửa tận gốc rễ, ngăn chặn lỗi hồi quy.

### Nhóm 2: Quality Engineering (Kỹ thuật Chất lượng — Bài 7 đến 12)
- [`dex-performance-optimization`](.agents/skills/dex-performance-optimization/SKILL.md): Tối ưu hiệu năng dựa trên số liệu benchmark định lượng trước và sau.
- [`dex-security-audit`](.agents/skills/dex-security-audit/SKILL.md): Quét bảo mật, rà soát lỗ hổng OWASP Top 10, ngăn lộ secret và kiểm toán bản vá.
- [`dex-cicd-automation`](.agents/skills/dex-cicd-automation/SKILL.md): Xây dựng pipeline CI/CD tự động hóa linting, build, test và scan bảo mật.
- [`dex-release-engineering`](.agents/skills/dex-release-engineering/SKILL.md): Đóng gói, nâng version SemVer, cập nhật changelog và lập kế hoạch rollback.
- [`dex-production-monitoring`](.agents/skills/dex-production-monitoring/SKILL.md): Cấu hình Structured JSON Logging, Health checks (/healthz) và giám sát chỉ số RED.
- [`dex-technical-debt-refactoring`](.agents/skills/dex-technical-debt-refactoring/SKILL.md): Tái cấu trúc code an toàn, xóa bỏ code smells mà không làm đổi hành vi.

### Nhóm 3: System Engineering (Kỹ thuật Hệ thống — Bài 13 đến 16)
- [`dex-software-architecture`](.agents/skills/dex-software-architecture/SKILL.md): Thiết kế kiến trúc Modular Monolith đơn giản, luồng dữ liệu một chiều, lập ADR.
- [`dex-database-engineering`](.agents/skills/dex-database-engineering/SKILL.md): Thiết kế Schema, migration 2 chiều an toàn, tối ưu index và transaction ACID.
- [`dex-api-engineering`](.agents/skills/dex-api-engineering/SKILL.md): Thiết kế RESTful/GraphQL API chuẩn mực, validate schema chặt chẽ, duy trì tương thích ngược.
- [`dex-testing-engineering`](.agents/skills/dex-testing-engineering/SKILL.md): Kim tự tháp kiểm thử tự động chuyên sâu: Unit, Integration, E2E và Regression tests.

### Nhóm 4: AI Agent Engineering (Điều khiển AI Agent — Bài 17 đến 20)
- [`dex-agent-engineering`](.agents/skills/dex-agent-engineering/SKILL.md): Điều khiển AI tự lập kế hoạch và thực thi với 4 nguyên tắc điều khiển Agent.
- [`dex-multi-agent-orchestration`](.agents/skills/dex-multi-agent-orchestration/SKILL.md): Phối hợp nhiều Agent song song, phân lập vùng code và review chéo.
- [`dex-context-engineering`](.agents/skills/dex-context-engineering/SKILL.md): Quản lý ngữ cảnh và bộ nhớ dài hạn với Single Source of Truth (`AGENTS.md`, `SPEC.md`).
- [`dex-specification-driven`](.agents/skills/dex-specification-driven/SKILL.md): Phát triển hướng đặc tả (SDD), xác lập Acceptance Criteria rõ ràng trước khi code.

### Nhóm 5: Production Engineering (Kỹ thuật Vận hành & Sản phẩm — Bài 21 đến 30)
- [`dex-change-impact-analysis`](.agents/skills/dex-change-impact-analysis/SKILL.md): Phân tích bán kính ảnh hưởng và rủi ro của thay đổi trước khi sửa code.
- [`dex-dependency-management`](.agents/skills/dex-dependency-management/SKILL.md): Quản lý dependencies có thể tái lập 100% qua lockfile, ngăn ngừa supply-chain attacks.
- [`dex-reliability-engineering`](.agents/skills/dex-reliability-engineering/SKILL.md): Tăng cường độ tin cậy với Timeout, Exponential Backoff, Retry và Circuit Breaker.
- [`dex-concurrency-state`](.agents/skills/dex-concurrency-state/SKILL.md): Kiểm soát tác vụ đồng thời, triệt tiêu race condition và ngăn ngừa deadlock.
- [`dex-ux-accessibility`](.agents/skills/dex-ux-accessibility/SKILL.md): Hoàn thiện trải nghiệm người dùng, responsive mobile và chuẩn tiếp cận WCAG 2.1 AA.
- [`dex-feature-flags`](.agents/skills/dex-feature-flags/SKILL.md): Tách biệt deploy và release với Feature Flags, staged canary rollout và instant kill-switch.
- [`dex-code-review`](.agents/skills/dex-code-review/SKILL.md): Rà soát từng dòng Git Diff trước khi merge PR, phân loại nhận xét xây dựng.
- [`dex-acceptance-testing`](.agents/skills/dex-acceptance-testing/SKILL.md): Kiểm thử nghiệm thu thực tế (UAT) theo kịch bản hành trình người dùng.
- [`dex-software-maintenance`](.agents/skills/dex-software-maintenance/SKILL.md): Lập roadmap bảo trì dài hạn, xử lý nợ kỹ thuật và quản lý vòng đời ứng dụng.
- [`dex-end-to-end-engineering`](.agents/skills/dex-end-to-end-engineering/SKILL.md): Quy trình tổng thể tích hợp trọn vẹn 29 kỹ năng từ Ý tưởng đến Vận hành.

---

## 4. Hướng Dẫn Kích Hoạt & Sử Dụng

### Cách 1: Sử dụng Master Orchestrator (Khuyến nghị cho mọi tác vụ)
Chỉ cần gửi yêu cầu cho Agent kèm lệnh kích hoạt Orchestrator:
> "Sử dụng `dex-master-orchestrator`: Hãy phân tích và sửa lỗi không nhận mã giảm giá khi thanh toán giỏ hàng."

Orchestrator sẽ tự động phân loại, chọn chế độ (`STANDARD MODE`), lập lộ trình kỹ năng (`dex-root-cause-debugging` → `dex-code-verification` → `dex-testing-engineering` → `dex-git-workflow`) và báo cáo kết quả.

### Cách 2: Kích hoạt Kỹ năng Chuyên biệt Trực tiếp
Khi bạn đã biết chính xác mình cần gì:
> "Sử dụng `dex-security-audit`: Hãy quét bảo mật toàn bộ các router trong thư mục `src/routes/` và báo cáo các nguy cơ OWASP."

---

## 5. 10 Quality Gates (Tiêu Chuẩn Kiểm Chứng)

| Cổng | Tên Cổng | Tiêu Chuẩn Đạt PASS |
|:---|:---|:---|
| **QG-01** | Scope Defined | Phạm vi file được phép sửa được xác định rõ ràng, không sửa lan man. |
| **QG-02** | Spec Compliant | Mã nguồn đáp ứng 100% Acceptance Criteria đã thỏa thuận. |
| **QG-03** | Lint & Typecheck | 0 lỗi cú pháp, 0 cảnh báo linter hoặc type check nghiêm trọng. |
| **QG-04** | Build Succeeded | Dự án build ra production artifact thành công không lỗi. |
| **QG-05** | Automated Tests | 100% các bài test liên quan vượt qua thành công (PASS). |
| **QG-06** | No Regressions | Không làm hỏng bất kỳ bài test hoặc chức năng cũ nào. |
| **QG-07** | Security Audit | 0 secret bị lộ trong code, 0 lỗ hổng CRITICAL hoặc HIGH. |
| **QG-08** | Diff Reviewed | Git diff sạch sẽ, không có mã debug thừa hay file rác. |
| **QG-09** | Docs Updated | `README.md`, `SPEC.md`, `TASKS.md` hoặc `CHANGELOG.md` được cập nhật đồng bộ. |
| **QG-10** | Verified Evidence | Kết quả có log terminal thực tế chứng minh, không bịa đặt báo cáo ảo. |

---

## 6. Ví Dụ Vận Hành Theo 3 Chế Độ

### Ví dụ 1: QUICK MODE (Sửa lỗi nhỏ)
- **Yêu cầu**: "Đổi tiêu đề trang chủ từ 'My Shop' thành 'Cửa Hàng DEX'."
- **Quy trình**:
  1. *Analyze*: Xác định file `src/pages/index.html`.
  2. *Implement*: Sửa thẻ `<title>Cửa Hàng DEX</title>`.
  3. *Verify*: Chạy `npm run test:e2e` kiểm tra title → PASS.
  4. *Report*: Báo cáo kết quả và commit.

### Ví dụ 2: STANDARD MODE (Thêm chức năng)
- **Yêu cầu**: "Thêm API lấy lịch sử đơn hàng của người dùng kèm phân trang."
- **Quy trình**:
  1. *SDD*: Soạn `SPEC.md` với endpoint `GET /api/v1/orders?page=1&limit=10`.
  2. *Impact*: Quét caller phụ thuộc → Thêm hàm mới, không ảnh hưởng code cũ.
  3. *Implement*: Viết controller, service và DTO validation.
  4. *Test*: Viết 4 unit tests và 2 integration tests → 100% PASS.
  5. *Review*: Soát diff, xóa debug log.
  6. *Git*: Commit chuẩn `feat(order): add get order history with pagination`.

### Ví dụ 3: STRICT MODE (Database Migration & Security)
- **Yêu cầu**: "Thêm trường `balance_cents` cho bảng `wallets` và triển khai API chuyển tiền."
- **Quy trình**:
  1. *Spec & Risk*: Xác định rủi ro tài chính cao, chọn STRICT MODE.
  2. *Database*: Viết file migration 2 chiều UP/DOWN an toàn, dùng `BIGINT`.
  3. *Reliability & Concurrency*: Áp dụng Atomic DB decrement và Distributed lock chống double spending.
  4. *Security*: Kiểm toán bảo mật xác thực JWT và phân quyền ví.
  5. *Quality Gates*: Kiểm tra toàn bộ 10 Gates đạt PASS.
  6. *Approval*: Xin phép người dùng trước khi áp dụng migration lên database thật.

---

## 7. Kiểm Tra & Xác Thực Tính Toàn Vẹn Của Bộ Kỹ Năng

Bộ kỹ năng đi kèm công cụ kiểm chứng tự động bằng Python:
```powershell
python scripts\validate_pack.py
```
Công cụ sẽ kiểm tra cú pháp YAML Frontmatter, giới hạn độ dài ký tự, tính duy nhất của tên skill, sự hiện diện của đủ 10 mục nội dung bắt buộc và tính toàn vẹn của tất cả các liên kết tài liệu.

Xem hướng dẫn cài đặt và tích hợp chi tiết tại [`INSTALL.md`](INSTALL.md).
Xem bảng tra cứu toàn bộ kỹ năng tại [`SKILLS_INDEX.md`](SKILLS_INDEX.md).
Xem ma trận định tuyến công việc tại [`ROUTING_MATRIX.md`](ROUTING_MATRIX.md).
