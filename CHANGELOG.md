# Changelog — DEX Engineering Skills Pack

Tất cả các thay đổi đáng chú ý của dự án này sẽ được ghi nhận trong tệp này theo chuẩn [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) và tuân thủ [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-22

### Added
- **Master Orchestrator (`dex-master-orchestrator`)**:
  - Hỗ trợ 3 chế độ thực thi thông minh: `QUICK MODE`, `STANDARD MODE`, `STRICT MODE`.
  - Bộ tài liệu điều phối chuyên sâu: `orchestration-protocol.md`, `routing-rules.md`, `mode-selection.md`.
  - Kiểm soát nghiêm ngặt 10 Quality Gates (từ QG-01 đến QG-10).
- **Foundation Skills (01 - 06)**:
  - `dex-development-workflow`: Quy trình Vibe Coding chuẩn mực.
  - `dex-task-delegation`: Giao việc chuẩn cho AI theo 6 trường mục tiêu.
  - `dex-code-verification`: Kiểm chứng chất lượng code bằng terminal thật.
  - `dex-git-workflow`: Quy trình Git an toàn và Conventional Commits.
  - `dex-code-organization`: Thiết kế cấu trúc thư mục sạch và phân tách module.
  - `dex-root-cause-debugging`: Sửa lỗi tận gốc bằng failing test case.
- **Quality Engineering Skills (07 - 12)**:
  - `dex-performance-optimization`: Tối ưu hiệu năng có số liệu benchmark định lượng.
  - `dex-security-audit`: Quét bảo mật OWASP Top 10 kèm `security-checklist.md`.
  - `dex-cicd-automation`: Tự động hóa kiểm thử bằng GitHub Actions pipeline.
  - `dex-release-engineering`: Đóng gói phát hành SemVer và rollback plan.
  - `dex-production-monitoring`: Structured logging JSON và health check `/healthz`.
  - `dex-technical-debt-refactoring`: Tái cấu trúc an toàn bảo vệ hành vi cũ.
- **System Engineering Skills (13 - 16)**:
  - `dex-software-architecture`: Thiết kế Modular Monolith tối giản kèm `architecture-decision-record.md`.
  - `dex-database-engineering`: Thiết kế schema 3NF, migration 2 chiều kèm `migration-safety-checklist.md`.
  - `dex-api-engineering`: Thiết kế API RESTful/GraphQL chuẩn hóa và tương thích ngược.
  - `dex-testing-engineering`: Kim tự tháp kiểm thử tự động Unit, Integration, E2E.
- **AI Agent Engineering Skills (17 - 20)**:
  - `dex-agent-engineering`: 4 nguyên tắc điều khiển AI Agent tự lập kế hoạch.
  - `dex-multi-agent-orchestration`: Phối hợp đa Agent song song và review chéo.
  - `dex-context-engineering`: Quản lý ngữ cảnh và bộ nhớ dài hạn của dự án.
  - `dex-specification-driven`: Phương pháp SDD kèm `spec-template.md`.
- **Production Engineering Skills (21 - 30)**:
  - `dex-change-impact-analysis`: Phân tích bán kính ảnh hưởng trước khi sửa code.
  - `dex-dependency-management`: Quản lý dependencies tái lập 100% qua lockfile.
  - `dex-reliability-engineering`: Timeout, Retry Exponential Backoff, Circuit Breaker.
  - `dex-concurrency-state`: Kiểm soát tác vụ đồng thời, triệt tiêu race conditions.
  - `dex-ux-accessibility`: Trải nghiệm người dùng 5 trạng thái, WCAG 2.1 AA.
  - `dex-feature-flags`: Feature Flags, staged canary rollout, instant kill-switch.
  - `dex-code-review`: Rà soát từng dòng Git Diff trước khi merge PR.
  - `dex-acceptance-testing`: Kiểm thử nghiệm thu thực tế (UAT) hành trình người dùng.
  - `dex-software-maintenance`: Lộ trình bảo trì dài hạn và quản lý vòng đời phần mềm.
  - `dex-end-to-end-engineering`: Quy trình tổng thể 15 giai đoạn kèm `full-lifecycle-playbook.md`.
- **Tài Liệu Hướng Dẫn & Bộ Kiểm Tra**:
  - `README.md`: Hướng dẫn tổng thể bằng tiếng Việt rõ ràng, minh bạch.
  - `INSTALL.md`: Hướng dẫn cài đặt chi tiết trên Windows 11 PowerShell và Linux/macOS.
  - `SKILLS_INDEX.md`: Bảng tra cứu danh mục nhanh 31 kỹ năng.
  - `ROUTING_MATRIX.md`: Ma trận điều phối kỹ năng và Quality Gates.
  - `AGENTS.example.md`: File mẫu ngữ cảnh cho các dự án tích hợp.
  - `scripts/validate_pack.py`: Công cụ Python kiểm thử tự động toàn diện.
  - `tests/skill-validation-cases.md`: Bộ 6 ca kiểm thử giả lập đa tình huống.
