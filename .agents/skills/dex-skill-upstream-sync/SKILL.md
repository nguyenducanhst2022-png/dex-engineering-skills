---
name: dex-skill-upstream-sync
description: Track, diff, and synchronize pinned upstream repositories, detecting remote updates and breaking changes without overwriting local modifications. Use to maintain long-term alignment with upstream skill ecosystems.
---

# dex-skill-upstream-sync

## 1. Purpose & Scope
Theo dõi, so sánh khác biệt (Diff Tracking) và đồng bộ hóa có kiểm soát các kho lưu trữ thượng nguồn đã được khóa phiên bản (Upstream Synchronization: AAS, Reverse Skill, REA); phát hiện các bản cập nhật mới, các bản vá bảo mật hoặc các thay đổi phá vỡ tương thích (Breaking Changes) từ tác giả gốc mà không bao giờ ghi đè làm mất các tùy chỉnh cục bộ (Local Customizations) của dự án.

## 2. When to Use
- Định kỳ hàng tháng kiểm tra xem các repo thượng nguồn có bản phát hành hoặc bản vá lỗi mới hay không.
- Khi tác giả của một upstream repo thông báo có bản vá bảo mật quan trọng.
- Cần xem trước các thay đổi khác biệt (Reviewable Diffs) trước khi quyết định cập nhật.

## 3. When NOT to Use
- Tuyệt đối không tự động chạy lệnh `git pull` hoặc đồng bộ ngầm mà không có sự kiểm tra và phê duyệt của kỹ sư.
- Không đồng bộ nếu nhánh hiện tại đang có các thay đổi chưa được commit sạch sẽ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các upstream sources được quản lý trong `manifests/upstream-sources.json`.
- Commit SHA đã khóa phiên bản hiện tại (Current Pinned Commit).
- Kết nối mạng tới remote GitHub repositories.
- **Điều kiện tiên quyết**:
- Có cài đặt Git CLI và script đồng bộ `scripts/sync_upstream.py`.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Pinned Versioning: Mọi nguồn ngoại nhập đều được cố định tại một Git Commit SHA cụ thể (ví dụ `7b4e28f...`), bảo đảm bản build luôn luôn tái lập được 100% ở bất kỳ thời điểm nào.
- Non-destructive Syncing: Quá trình đồng bộ chỉ tải về thư mục tạm, tạo file đối chiếu diff trực quan giữa phiên bản đang dùng và phiên bản mới nhất trên remote, chờ kỹ sư review từng dòng code.
- Three-Way Merge for Custom Skills: Nếu một kỹ năng đã được tùy chỉnh nội địa, hệ thống áp dụng cơ chế hợp nhất 3 chiều (Base, Local, Remote) để bảo tồn toàn bộ các cải tiến của dự án.
- **Quy tắc quyết định kỹ thuật**:
- Nếu phát hiện upstream có commit mới: xuất báo cáo Diff chi tiết và tạo Pull Request đề xuất cập nhật thay vì cập nhật trực tiếp.
- Luôn chạy toàn bộ test suite và validator sau mỗi đợt đồng bộ thử nghiệm.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Chạy lệnh đồng bộ tự động ghi đè mất toàn bộ các chỉnh sửa tiếng Việt và các ví dụ thực tế mà đội ngũ DEX đã tối ưu hóa cho kỹ năng.

## 6. Step-by-Step Execution Workflow
1. Đọc danh sách upstream repositories và commit SHA hiện tại từ `manifests/upstream-sources.json`.
2. Kiểm tra commit HEAD mới nhất trên remote repository thông qua Git API hoặc `git ls-remote`.
3. Nếu có commit mới: tải về bản sao tạm thời và tạo file so sánh diff (`upstream-sync.diff`).
4. Phân tích các thay đổi: kiểm tra xem có thay đổi nào mang tính phá vỡ cấu trúc hoặc vi phạm an ninh không.
5. Xuất báo cáo tóm tắt các thay đổi cho kỹ sư xem xét.
6. Nếu được phê duyệt: cập nhật file trong `integrations/` và cập nhật Commit SHA mới vào manifest.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Kiểm tra cập nhật từ repo thượng nguồn an toàn không ghi đè
import subprocess, json

def check_upstream_updates(manifest_path: str):
    with open(manifest_path, "r", encoding="utf-8") as f:
        sources = json.load(f)
        
    for src in sources.get("sources", []):
        repo_url = src["repository_url"]
        pinned_sha = src["pinned_commit"]
        
        # Lấy commit SHA mới nhất từ remote
        output = subprocess.check_output(["git", "ls-remote", repo_url, "HEAD"]).decode("utf-8")
        remote_sha = output.split()[0]
        
        if remote_sha != pinned_sha:
            print(f"[SYNC-ALERT] Nguồn {src['upstream_id']} có phiên bản mới!")
            print(f"  - Đang dùng: {pinned_sha[:8]}")
            print(f"  - Mới nhất : {remote_sha[:8]}")
        else:
            print(f"[SYNC-OK] Nguồn {src['upstream_id']} đã ở phiên bản mới nhất.")
```

### Lệnh xác minh & thực thi:
```bash
# Chạy kiểm tra đồng bộ thượng nguồn ở chế độ xem trước an toàn
python scripts/sync_upstream.py --dry-run
```

## 8. Anti-Patterns & Common Traps
- Cấu hình cron job tự động pull code từ internet thẳng vào production repository mà không có review.
- Xóa bỏ commit SHA đã pin và chuyển sang dùng nhánh `main` trôi nổi.

## 9. Quality Gates & Acceptance Criteria
- 0 dòng code tùy chỉnh cục bộ nào bị mất mát sau quá trình đồng bộ.
- File diff được xuất ra rõ ràng và có thể review từng dòng trên Pull Request.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi bản cập nhật từ upstream đều phải trải qua lại quy trình rà soát an ninh (Security Screening) trước khi chấp nhận commit mới.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Báo cáo trạng thái đồng bộ thượng nguồn (Upstream Sync Report).
- File diff so sánh chi tiết giữa phiên bản hiện tại và phiên bản mới.

## 13. Related & Complementary Skills
dex-skill-import-packaging, dex-skill-license-provenance, dex-skill-security-screening

## 14. Realistic Usage Example
### Tình huống thực tế:
Tác giả của repository Agentic Awesome Skills phát hành phiên bản mới sửa lỗi một số script CI/CD. Chạy công cụ `sync_upstream.py --dry-run`, hệ thống phát hiện có 3 files được sửa đổi và xuất ra file diff súc tích. Kỹ sư kiểm tra nhanh thấy bản sửa lỗi rất hữu ích và không ảnh hưởng tới bản dịch tiếng Việt, lập tức phê duyệt cập nhật commit SHA mới trong vòng 5 phút.
