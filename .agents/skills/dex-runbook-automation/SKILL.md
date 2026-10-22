---
name: dex-runbook-automation
description: Author, validate, and execute operational runbooks (SOPs) with pre-flight checks, interactive approval gates, guarded commands, and rollback procedures. Use when standardizing and automating operational maintenance tasks.
---

# dex-runbook-automation

## 1. Purpose & Scope
Thiết kế, chuẩn hóa và tự động hóa các quy trình vận hành tiêu chuẩn (Standard Operating Procedures - SOPs / Executable Runbooks); chuyển hóa tài liệu hướng dẫn bằng lời văn mơ hồ thành các kịch bản thực thi an toàn (Runbook as Code); tích hợp các bước kiểm tra điều kiện tiên quyết (Pre-flight Checks), cổng phê duyệt tương tác (Interactive Approval Gates), câu lệnh thực thi có rào chắn bảo vệ (Guarded Commands), cơ chế khôi phục khẩn cấp (Rollback Procedures) và ghi vết kiểm toán minh bạch nhằm giảm thiểu thời gian phục hồi sự cố (MTTR) và loại bỏ lỗi do con người (Human Error).

## 2. When to Use
- Khi các tác vụ vận hành định kỳ hoặc khẩn cấp (Xoay vòng chứng chỉ, Dọn dẹp dung lượng đĩa, Khởi động lại cụm Redis, Failover Database) đang phải gõ lệnh thủ công bằng tay.
- Khi kỹ sư trực on-call lúc 3h sáng gõ nhầm lệnh xóa nhầm dữ liệu production do căng thẳng và thiếu ngủ.
- Khi quy trình khắc phục sự cố chỉ nằm trong đầu một vài kỹ sư kỳ cựu mà không được tài liệu hóa cho toàn đội ngũ.

## 3. When NOT to Use
- Triển khai code ứng dụng định kỳ qua pipeline CI/CD (dùng `dex-cicd-automation`).
- Thiết kế kiến trúc phần mềm cốt lõi (dùng `dex-software-architecture`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mục tiêu của quy trình vận hành và hệ thống đích (Database, Kubernetes, Message Queue).
- Danh sách các câu lệnh thực thi và tham số bắt buộc.
- Điều kiện kiểm tra an toàn trước khi chạy (Pre-checks) và sau khi chạy (Post-verification).
- Kịch bản hoàn nguyên (Rollback Steps) khi gặp sự cố giữa chừng.
- **Điều kiện tiên quyết**:
- Môi trường thực thi kịch bản (Python, Bash, Ansible, Runme, Rundeck).
- Quyền truy cập hạ tầng được giới hạn theo nguyên tắc đặc quyền tối thiểu (Least Privilege).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Executable Runbooks as Code**: Tài liệu hướng dẫn vận hành phải là tệp mã nguồn có thể thực thi được trực tiếp (ví dụ: Markdown tương tác với Runme hoặc Script tự động hóa), không phải file Word tĩnh bám bụi trên Wiki.
- **Guarded Execution Pattern**: Mỗi câu lệnh tác động nguy hiểm phải được bao bọc bởi 3 lớp: Kiểm tra điều kiện (Pre-flight) -> Hỏi xác nhận tường minh (Approval Prompt hiển thị rõ môi trường `PRODUCTION`) -> Thực thi có timeout và ghi log.
- **Idempotent Operational Steps**: Mỗi bước trong runbook phải có tính chất idempotent; nếu chạy lại lần 2 khi bước đó đã hoàn thành thì không gây ra lỗi hay làm hỏng dữ liệu.
- **Quy tắc quyết định kỹ thuật**:
- **Luôn Có Kịch Bản Rollback Tương Ứng Cho Từng Bước**: Không bao giờ phê duyệt một Runbook nếu thiếu phần hướng dẫn chi tiết cách đảo ngược hành động khi xảy ra lỗi.
- **Hiển Thị Cảnh Báo Đỏ Cho Môi Trường Production**: Mọi kịch bản chạy trên Production bắt buộc phải yêu cầu kỹ sư gõ đúng tên môi trường (`CONFIRM_PRODUCTION`) mới cho phép chạy tiếp.
- **Tự Động Lưu Toàn Bộ Output Vào Log Kiểm Toán**: Mọi lệnh thực thi, thời gian chạy và người bấm nút phải được tự động ghi nhận vào audit log trung tâm.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Chạy nhầm lệnh xóa trên Production thay vì Staging**: Do kỹ sư mở nhầm tab terminal đang trỏ context vào cụm Prod -> Khắc phục: Runbook tự động kiểm tra `kubectl config current-context` hoặc `AWS_PROFILE`; nếu phát hiện context không khớp tham số đầu vào, lập tức dừng chương trình ngay.
- **Runbook bị treo vô tận khi gọi lệnh khởi động lại service**: Do service bị deadlock không thoát được -> Khắc phục: Bắt buộc cấu hình timeout tường minh (ví dụ: `timeout 60s systemctl restart ...`) cho mọi lệnh trong runbook.

## 6. Step-by-Step Execution Workflow
1. Khảo sát quy trình vận hành thủ công hiện tại và phân tích các điểm rủi ro tiềm ẩn.
2. Viết tài liệu Runbook theo cấu trúc chuẩn: Mục tiêu, Phạm vi, Rủi ro, Thời gian dự kiến, Pre-flight checks, Execution, Rollback, Post-checks.
3. Chuyển hóa các bước dòng lệnh thành kịch bản tự động hóa có kiểm soát (Guarded Script).
4. Thử nghiệm toàn bộ Runbook trên môi trường Staging/Sandbox, giả lập tình huống lỗi giữa chừng để kiểm tra luồng Rollback.
5. Đưa Runbook vào quy trình diễn tập định kỳ (Game Day / Chaos Testing) cho đội ngũ on-call.
6. Lưu trữ Runbook trong repository Git tập trung (`ops/runbooks/`) có quy trình review nghiêm ngặt.
7. Cập nhật và tinh chỉnh Runbook sau mỗi sự cố thực tế (Postmortem Action Items).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
#!/usr/bin/env python3
# ops/runbooks/db_failover_runbook.py
# Runbook tự động hóa chuyển đổi dự phòng cơ sở dữ liệu (Database Failover)

import sys, os, time, subprocess

def run_guarded_command(cmd, description):
    print(f"\n[EXEC] {description}...")
    print(f"Command: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    if res.returncode != 0:
        print(f"[ERROR] Thất bại tại bước: {description}")
        print(f"STDERR: {res.stderr}")
        trigger_rollback()
        sys.exit(1)
    print(f"[SUCCESS] Hoàn tất: {description}")
    return res.stdout

def trigger_rollback():
    print("\n=================== KÍCH HOẠT QUY TRÌNH ROLLBACK ===================")
    print("Đang trả lại trạng thái kết nối cho Database cũ...")
    subprocess.run("kubectl rollout undo deployment/api-gateway -n core", shell=True)
    print("Rollback hoàn tất. Vui lòng kiểm tra lại trạng thái hệ thống.")

def main():
    target_env = os.getenv("TARGET_ENV", "staging")
    print(f"=== BẮT ĐẦU RUNBOOK: DATABASE FAILOVER [{target_env.upper()}] ===")
    
    # 1. Pre-flight Check: Xác minh Replication Lag
    lag = run_guarded_command("aws rds describe-db-instances --db-instance-identifier prod-replica --query 'DBInstances[0].StatusInfos[0].Normal'", "Kiểm tra trạng thái Read Replica")
    
    # 2. Interactive Approval Gate
    confirm = input(f"XÁC NHẬN: Bạn có chắc chắn muốn chuyển đổi Master DB trên [{target_env}]? (Gõ 'YES' để tiếp tục): ")
    if confirm.strip() != "YES":
        print("Đã hủy bỏ thực thi Runbook.")
        sys.exit(0)
        
    # 3. Execution: Promote Replica thành Master
    run_guarded_command("aws rds promote-read-replica --db-instance-identifier prod-replica", "Promote Read Replica thành Standalone Master")
    
    # 4. Post-flight Verification: Kiểm tra kết nối từ ứng dụng
    print("Chờ 30s để DNS cập nhật...")
    time.sleep(30)
    run_guarded_command("curl -f -s https://api.internal/healthz/db || exit 1", "Kiểm tra sức khỏe kết nối DB mới")
    
    print(f"\n[COMPLETED] Runbook Database Failover trên [{target_env}] THÀNH CÔNG RỰC RỠ!")

if __name__ == "__main__":
    main()
```

### Lệnh xác minh & thực thi:
- Kiểm tra cú pháp script runbook: `python3 -m py_compile ops/runbooks/*.py`
- Chạy thử nghiệm chế độ Dry-Run không tác động: `python3 ops/runbooks/db_failover_runbook.py --dry-run`
- Kiểm tra tài liệu markdown hiển thị đúng trên Runme / CLI: `npx runme list --all`

## 8. Anti-Patterns & Common Traps
- **Lưu runbook trong tệp tài liệu Word cá nhân trên máy laptop**: Không ai tìm thấy khi sự cố xảy ra lúc người đó đi nghỉ mát.
- **Runbook chứa các lệnh nguy hiểm kiểu `rm -rf /data/*` không có điều kiện bảo vệ**: Chỉ cần gõ sai biến thư mục là xóa sạch server.
- **Không bao giờ diễn tập Runbook trước khi có sự cố**: Đến khi production sập mới đem ra chạy lần đầu và phát hiện script bị lỗi cú pháp.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các thao tác vận hành production đều có Runbook dạng mã nguồn có thể kiểm chứng.
- QG-09: Toàn bộ Runbook đều có kịch bản Rollback tự động hoặc bán tự động rõ ràng.
- QG-11: Runbook đã được diễn tập thành công trên môi trường Staging/GameDay ít nhất 1 lần.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Mọi thông tin xác thực (Passwords, Tokens) phải được inject động từ Vault, không hardcode trong Runbook.
- Ghi vết kiểm toán (Audit Trail) bất biến cho toàn bộ phiên chạy Runbook.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Tệp Runbook tiêu chuẩn (`ops/runbooks/<procedure>.md` hoặc `.py`).
- Kịch bản Rollback tương ứng.
- Biên bản diễn tập vận hành (GameDay Runbook Verification Report).

## 13. Related & Complementary Skills
- `dex-incident-postmortems`: Cập nhật Runbook sau khi hoàn tất điều tra nguyên nhân sự cố.
- `dex-operational-readiness-review`: Kiểm tra sự tồn tại của Runbook trước khi cho phép release sản phẩm.
- `dex-root-cause-debugging`: Sử dụng Runbook để chẩn đoán và cô lập vùng lỗi nhanh chóng.

## 14. Realistic Usage Example
### Tình huống thực tế:
Hệ thống cơ sở dữ liệu PostgreSQL chính bị nghẽn I/O và cần thực hiện chuyển đổi dự phòng (Failover) sang cụm Replica lúc 2h sáng. Kỹ sư on-call mở Runbook `db_failover_runbook.py`, chạy một lệnh duy nhất. Script tự động kiểm tra độ trễ đồng bộ (Replication Lag < 1s), yêu cầu xác nhận 'YES', tự động promote replica mới, cập nhật Route53 DNS và kiểm tra lại health check của API Gateway. Toàn bộ quá trình hoàn tất trong 85 giây mà không xảy ra sai sót nào do thao tác tay.
