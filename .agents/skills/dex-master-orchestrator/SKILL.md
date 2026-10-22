---
name: dex-master-orchestrator
description: Master skill to analyze user requests, determine task complexity, select intelligent execution modes (QUICK, STANDARD, STRICT), coordinate specialized DEX skills, enforce Quality Gates, and generate final verification reports. Use whenever starting a software engineering task or orchestrating multi-skill workflows.
---

# DEX Master Orchestrator

## 1. Purpose & Scope
Điều phối toàn bộ vòng đời phát triển phần mềm bằng AI theo chuẩn DEX Engineering Framework. Master Orchestrator chịu trách nhiệm phân tích yêu cầu, đánh giá rủi ro, lựa chọn đúng chế độ thực thi, kích hoạt các kỹ năng chuyên biệt tối thiểu cần thiết, kiểm soát nghiêm ngặt 10 Quality Gates và tổng hợp báo cáo kiểm chứng minh bạch.

Triết lý cốt lõi:
`Analyze → Specify → Plan → Implement → Verify → Debug → Stabilize → Review → Commit → Release → Maintain`

## 2. When to Use
- Bắt đầu bất kỳ tác vụ kỹ thuật phần mềm mới nào từ người dùng.
- Khi cần xác định quy trình kỹ thuật phù hợp cho một yêu cầu chưa rõ ràng.
- Khi tác vụ yêu cầu phối hợp nhiều kỹ năng kỹ thuật (ví dụ: sửa bug, nâng cấp tính năng, refactor, release, audit).
- Khi cần kiểm soát rủi ro và ngăn chặn việc AI tự ý bỏ qua các bước kiểm tra quan trọng.

## 3. When NOT to Use
- Trả lời các câu hỏi lý thuyết hoặc tra cứu thông tin đơn giản không làm thay đổi mã nguồn.
- Khi người dùng đã chỉ định tường minh kích hoạt một skill độc lập duy nhất (ví dụ: chỉ chạy `dex-security-audit` trên một file cụ thể).
- Khi đang ở giữa một quy trình con do skill khác trực tiếp xử lý (tránh can thiệp lặp vòng).

## 4. Prerequisites & Input Context
- **Yêu cầu của người dùng**: Mục tiêu, tính năng cần làm, mô tả bug hoặc lệnh phát hành.
- **Ngữ cảnh dự án**: `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `TASKS.md`, `CHANGELOG.md`.
- **Trạng thái kho mã nguồn**: Trạng thái Git (`git status`, nhánh hiện tại, commit hash gần nhất).
- **Môi trường kỹ thuật**: Ngôn ngữ lập trình, framework, package manager, bộ test hiện có.

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Phân tích Ý định & Phân loại Nhiệm vụ (Triage & Classification)
1. Đọc và phân tích yêu cầu của người dùng:
   - Mục tiêu chính là gì?
   - Phạm vi thay đổi (Scope) dự kiến: một dòng, một hàm, một module hay toàn bộ hệ thống?
   - Mức độ ảnh hưởng đến dữ liệu, bảo mật, người dùng cuối.
2. Phân loại tác vụ vào một trong các nhóm:
   - **Bug Fix**: Sửa lỗi phát sinh, crash, hành vi sai.
   - **Feature Upgrade**: Thêm chức năng mới, mở rộng logic hiện có.
   - **Performance Tuning**: Tối ưu tốc độ, bộ nhớ, tài nguyên.
   - **Security Audit / Patch**: Quét bảo mật, vá lỗ hổng.
   - **Refactoring / Debt Reduction**: Cải tiến cấu trúc không đổi hành vi.
   - **Architecture / Database Change**: Thiết kế hệ thống, thay đổi schema dữ liệu.
   - **Release & Deployment**: Đóng gói, nâng version, phát hành.
   - **Greenfield Project**: Xây dựng dự án mới từ con số không.

### Bước 2: Lựa chọn Chế độ Thực thi Thông minh (Execution Mode Selection)
Căn cứ vào ma trận rủi ro ([mode-selection.md](references/mode-selection.md)):
- **QUICK MODE** (Rủi ro thấp):
  - *Áp dụng*: Sửa lỗi nhỏ, sửa chính tả/UI text, chỉnh sửa cấu hình đơn giản.
  - *Chu trình*: Analyze → Implement → Verify → Report.
- **STANDARD MODE** (Rủi ro trung bình):
  - *Áp dụng*: Phát triển tính năng mới tiêu chuẩn, refactor module vừa, nâng cấp thư viện không breaking.
  - *Chu trình*: Analyze → Plan → Implement → Test → Review → Report.
- **STRICT MODE** (Rủi ro cao / Bắt buộc kiểm soát gắt gao):
  - *Áp dụng*: Thay đổi kiến trúc, Database migration, Authentication/Security, tính năng lõi thanh toán/tài chính, Release Production.
  - *Chu trình*: Specification → Impact Analysis → Risk Assessment → Plan → Implement → Tests → Security Review → Quality Gates → Approval → Release.

### Bước 3: Định tuyến Kỹ năng Tối thiểu (Skill Routing)
Chỉ kích hoạt tập kỹ năng thực sự cần thiết theo [routing-rules.md](references/routing-rules.md):
- **Bug Fix**: `dex-root-cause-debugging` → `dex-code-verification` → `dex-testing-engineering` → `dex-git-workflow`.
- **Feature Upgrade**: `dex-specification-driven` → `dex-change-impact-analysis` → `dex-development-workflow` → `dex-testing-engineering` → `dex-code-review` → `dex-git-workflow`.
- **Performance**: `dex-performance-optimization` → `dex-testing-engineering` → `dex-code-review`.
- **Security**: `dex-security-audit` → `dex-code-verification` → `dex-testing-engineering`.
- **Release**: `dex-testing-engineering` → `dex-security-audit` (nếu cần) → `dex-release-engineering` → `dex-git-workflow`.
- **Greenfield**: `dex-specification-driven` → `dex-software-architecture` → `dex-task-delegation` → `dex-development-workflow` → `dex-testing-engineering` → `dex-git-workflow`.

### Bước 4: Kiểm soát Chuyển Giai đoạn & Quality Gates
Tại mỗi mốc chuyển giao giữa các skill, Master Orchestrator kiểm tra các Quality Gates tương ứng (từ QG-01 đến QG-10).
- Nếu bất kỳ Gate bắt buộc nào chưa đạt: **CHẶN** chuyển giai đoạn, yêu cầu Agent/Skill hiện tại sửa chữa hoặc bổ sung bằng chứng.
- Không được phép chuyển sang commit hoặc release khi test còn FAIL hoặc NOT VERIFIED.

### Bước 5: Tổng hợp & Báo cáo Kiểm chứng (Final Report Synthesis)
Sau khi hoàn tất toàn bộ chuỗi kỹ năng, tổng hợp kết quả theo định dạng chuẩn hóa:
- **Tóm tắt hành động**: Những thay đổi đã thực hiện.
- **Trạng thái Quality Gates**: Liệt kê rõ từng Gate (PASS / FAIL / SKIP kèm lý do).
- **Bằng chứng kiểm chứng**: Log test thực tế, kết quả benchmark hoặc diff review.
- **Khuyến nghị tiếp theo**: Hướng dẫn người dùng nghiệm thu hoặc các bước tiếp theo.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-master-orchestrator
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
Master Orchestrator kiểm soát 10 cổng chất lượng:
- **QG-01 (Scope Control)**: Xác định rõ danh sách file được phép chỉnh sửa; không sửa file ngoài phạm vi.
- **QG-02 (Spec Compliance)**: Đáp ứng đầy đủ tiêu chí nghiệm thu (Acceptance Criteria) đã thỏa thuận.
- **QG-03 (Lint & Typecheck)**: Không có lỗi cú pháp hoặc cảnh báo linter/type-check nghiêm trọng.
- **QG-04 (Build Verification)**: Dự án build thành công ở môi trường target (nếu có quy trình build).
- **QG-05 (Automated Tests)**: Toàn bộ Unit/Integration tests liên quan đạt PASS 100%.
- **QG-06 (Regression Free)**: Các chức năng cũ không bị ảnh hưởng tiêu cực.
- **QG-07 (Security Audit)**: Không có secrets hardcoded, không phát sinh lỗ hổng bảo mật mới.
- **QG-08 (Diff Review)**: Git diff được rà soát từng dòng, không có mã thừa, debug console hay file tạm.
- **QG-09 (Documentation Update)**: Tài liệu kỹ thuật, README hoặc CHANGELOG được cập nhật tương ứng.
- **QG-10 (Verified Evidence)**: Toàn bộ kết quả phải có log/terminal output thực tế chứng minh, không tự tạo kết quả giả.

## 10. Security & Safety Boundaries
- **Không tự ý chuyển chế độ hạ cấp**: Không được hạ từ STRICT xuống QUICK chỉ để bỏ qua bước kiểm thử.
- **Git Safety First**: Không bao giờ thực hiện `git push --force`, `git reset --hard` hoặc xóa nhánh khi chưa có sự đồng ý tường minh từ người dùng.
- **Bảo mật tuyệt đối**: Không bao giờ đọc, in ra màn hình hoặc commit API key, token, mật khẩu hoặc secrets vào file/log.
- **Chặn ảo tưởng (No Hallucinated Passes)**: Cấm tuyệt đối việc tự báo PASS khi chưa thực sự chạy lệnh kiểm tra trong shell.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Bản đánh giá phân loại nhiệm vụ và chế độ thực thi đề xuất (`QUICK`, `STANDARD` hoặc `STRICT`).
2. Kế hoạch định tuyến chuỗi skills cụ thể.
3. Bảng theo dõi tiến độ các Quality Gates trong quá trình thực thi.
4. Báo cáo tổng kết hoàn thành dự án kèm bằng chứng thực nghiệm (Terminal Output / Git Hash / Test Log).

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-master-orchestrator** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
