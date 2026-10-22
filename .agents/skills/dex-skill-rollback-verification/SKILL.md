---
name: dex-skill-rollback-verification
description: Design deterministic rollback procedures, state restoration drills, and backup verification for skill deployments, guaranteeing zero-downtime recovery from flawed skill updates. Use when deploying critical skill updates or establishing disaster recovery plans.
---

# dex-skill-rollback-verification

## 1. Purpose & Scope
Thiết kế và kiểm chứng quy trình hoàn tác xác định (Deterministic Rollback Procedures); thực hiện diễn tập khôi phục trạng thái (State Restoration Drills) và xác minh tính toàn vẹn của bản sao lưu; đảm bảo khả năng quay trở lại phiên bản kỹ năng an toàn trước đó trong vòng dưới 60 giây khi một bản cập nhật kỹ năng phát sinh lỗi; bảo toàn tính liên tục của hệ thống Agent.

## 2. When to Use
- Trước khi triển khai một bản cập nhật kỹ năng lớn có tác động sâu rộng lên toàn bộ hệ thống.
- Khi một kỹ năng vừa cập nhật bị phát hiện có lỗi làm gián đoạn quá trình điều phối của Master Orchestrator.
- Khi thực hiện các bài diễn tập khôi phục sau thảm họa (Disaster Recovery Drills) định kỳ.

## 3. When NOT to Use
- Khi bản cập nhật chỉ sửa một lỗi chính tả nhỏ không gây rủi ro vận hành.
- Khi hệ thống đang trong giai đoạn phát triển ban đầu chưa có người sử dụng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Hệ thống kiểm soát phiên bản Git có gắn thẻ phát hành (Release Tags), bản sao lưu trạng thái trước khi triển khai, kịch bản hoàn tác tự động.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Atomic Rollback via Git Revert / Tag Checkout:** Khôi phục trạng thái kho kỹ năng về đúng mã commit hash của phiên bản ổn định gần nhất một cách nguyên tử.
- **Zero-Data-Loss State Cache:** Đảm bảo các phiên làm việc đang chạy dở dang của Agent không bị mất dữ liệu khi hệ thống thực hiện hoàn tác kỹ năng.
- **Post-Rollback Smoke Test:** Tự động chạy ngay một bộ kiểm thử nhanh (Smoke Test) sau khi hoàn tác để xác nhận hệ thống đã hồi phục hoàn toàn.

## 6. Step-by-Step Execution Workflow
1. Trước khi deploy bản cập nhật, tạo một điểm đánh dấu an toàn (Safety Tag hoặc Snapshot).
2. Mô phỏng tình huống sự cố: bản cập nhật mới làm hỏng khả năng phân tích của Master Orchestrator.
3. Kích hoạt lệnh hoàn tác tự động đưa kho kỹ năng về điểm an toàn gần nhất.
4. Chạy bài kiểm thử khói tự động `pytest tests/test_skill_structure.py` để xác nhận trạng thái.
5. Lập biên bản diễn tập hoàn tác `ROLLBACK_VERIFICATION_REPORT.md` ghi nhận thời gian phục hồi.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Automated Atomic Skill Rollback Script
#!/usr/bin/env bash
set -e

LATEST_STABLE_TAG="v5.0.0"

echo "CRITICAL: Initiating automated rollback to ${LATEST_STABLE_TAG}..."
git checkout "${LATEST_STABLE_TAG}"

# Re-index manifest immediately
python scripts/discover_skills.py --output manifests/dex-skills.json

# Run immediate smoke test verification
python scripts/validate_skills.py

echo "SUCCESS: Rollback to ${LATEST_STABLE_TAG} completed and verified!" 
```

## 8. Anti-Patterns & Common Traps
- Triển khai cập nhật kỹ năng mà không tạo điểm sao lưu hoặc không có phương án hoàn tác khẩn cấp.
- Cố gắng sửa lỗi trực tiếp trên môi trường đang gặp sự cố (Hot-patching under panic) thay vì lập tức hoàn tác về bản ổn định.
- Hoàn tác mã nguồn kỹ năng nhưng quên cập nhật lại tệp manifest `dex-skills.json`, khiến hệ thống bị lệch trạng thái.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Thời gian hoàn tác toàn bộ kho kỹ năng về trạng thái ổn định dưới 60 giây.
- QG-02: Bộ kiểm thử xác thực tự động chạy thành công 100% ngay sau khi hoàn tác.
- QG-03: Bản sao lưu dự phòng được kiểm tra tính toàn vẹn định kỳ hàng tháng.

## 10. Security & Safety Boundaries
- Bảo vệ các thẻ phát hành Git an toàn (Protected Tags) để ngăn ngừa việc xóa nhầm các điểm khôi phục ổn định.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Kịch bản hoàn tác tự động khẩn cấp `scripts/emergency_rollback.sh`.
1. Biên bản diễn tập hoàn tác và khôi phục trạng thái `ROLLBACK_VERIFICATION_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-skill-upgrade-migrations`](.agents/skills/dex-skill-upgrade-migrations/SKILL.md)
- [`dex-disaster-recovery`](.agents/skills/dex-disaster-recovery/SKILL.md)
- [`dex-skill-retirement-governance`](.agents/skills/dex-skill-retirement-governance/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Một bản cập nhật kỹ năng vô tình làm thay đổi cấu trúc bảng phân loại khiến Master Orchestrator bị lỗi định tuyến. Kỹ sư kích hoạt `dex-skill-rollback-verification`, thực thi kịch bản hoàn tác khẩn cấp đưa hệ thống về tag `v5.0.0` trong 22 giây, chạy smoke test xác nhận hệ thống hoạt động ổn định trở lại, bảo vệ uy tín dịch vụ.
