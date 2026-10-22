---
name: dex-end-to-end-engineering
description: Full-lifecycle end-to-end software engineering meta-workflow integrating all 29 DEX engineering skills. Guides software creation from raw idea to production operations, monitoring, and long-term maintenance. Use when building complete applications from scratch, orchestrating complex full-lifecycle projects, or managing end-to-end software delivery.
---

# DEX End-to-End AI Software Engineering

## 1. Purpose
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

## 3. When Not to Use
- Khi chỉ thực hiện một thay đổi nhỏ, sửa lỗi cục bộ (dùng `dex-root-cause-debugging` hoặc QUICK MODE).
- Khi nhiệm vụ chỉ thuần túy là viết một đoạn script nhỏ không có nhu cầu phát hành hay bảo trì dài hạn.

## 4. Inputs
- Bản mô tả ý tưởng sản phẩm ban đầu hoặc yêu cầu nghiệp vụ từ khách hàng.
- Tài liệu hướng dẫn chi tiết toàn bộ vòng đời tại [full-lifecycle-playbook.md](references/full-lifecycle-playbook.md).
- Ma trận phân công và danh mục 30 kỹ năng chuyên biệt DEX.

## 5. Workflow

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

## 6. Quality Gates
Áp dụng đầy đủ **10 Quality Gates (từ QG-01 đến QG-10)** tại các mốc chuyển giai đoạn:
- Không chuyển từ Spec sang Code nếu chưa có Acceptance Criteria (QG-01, QG-02).
- Không chuyển từ Code sang Review nếu Test chưa PASS 100% (QG-03, QG-04, QG-05).
- Không chuyển từ Review sang Release nếu chưa qua Security Audit và Diff Review (QG-06, QG-07, QG-08).
- Không bàn giao nếu thiếu tài liệu và bằng chứng kiểm chứng (QG-09, QG-10).

## 7. Safety Rules
- **Tuân Thủ Toàn Bộ 7 Universal Engineering Rules**:
  1. Scope Control.
  2. Test Before Completion.
  3. Root Cause First.
  4. Git Safety.
  5. Security (Zero secret leaks).
  6. No False Completion (Zero hallucinated tests).
  7. Simplicity (KISS & YAGNI).

## 8. Expected Outputs
1. Toàn bộ mã nguồn hoàn chỉnh của sản phẩm phần mềm.
2. Bộ tài liệu dự án đầy đủ (`README.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, `CHANGELOG.md`).
3. Bộ test suite hoàn chỉnh bao phủ Unit, Integration và E2E tests đạt 100% PASS.
4. Hệ thống CI/CD, kịch bản Release và cấu hình Giám sát vận hành.

## 9. Failure Handling
- Khi một giai đoạn trong chuỗi bị ách tắc hoặc vi phạm Quality Gate: Hệ thống tự động chặn chuyển tiếp, kích hoạt kỹ năng tương ứng (ví dụ `dex-root-cause-debugging` hoặc `dex-change-impact-analysis`) để giải quyết dứt điểm trước khi cho phép đi tiếp.

## 10. Completion Criteria
- Sản phẩm được triển khai hoàn chỉnh, vượt qua toàn bộ 10 Quality Gates.
- Có đầy đủ bằng chứng kiểm thử thực nghiệm và báo cáo nghiệm thu sản phẩm chính thức.

---

## Real-world Example
Xây dựng nền tảng Blog cá nhân bằng AI từ con số không:
- *Giai đoạn 1-3*: Đặc tả tính năng đăng bài/bình luận, thiết kế kiến trúc Next.js + SQLite, thiết lập DB schema.
- *Giai đoạn 4-6*: Chia 8 nhiệm vụ trong `TASKS.md`, code tuần tự từng endpoint kèm 24 unit/integration tests PASS 100%.
- *Giai đoạn 7-8*: Quét bảo mật XSS bình luận, đo Lighthouse đạt 98/100, kiểm tra responsive mobile.
- *Giai đoạn 9-10*: Gắn tag `v1.0.0`, tạo GitHub Actions CI/CD tự động test, cấu hình Docker container và endpoint `/healthz`.
Kết quả: Sản phẩm sẵn sàng vận hành thực tế mà không có bất kỳ dòng code rác nào.
