---
name: dex-backfill-reconciliation
description: Orchestrate safe, idempotent historical data backfills across partitioned analytical tables, verifying pre/post row counts, metric parity reconciliations, and preventing downstream cascade corruptions. Use when recalculating metrics, fixing historic ETL bugs, or migrating database schemas.
---

# dex-backfill-reconciliation

## 1. Purpose & Scope
Điều phối quy trình nạp bù dữ liệu lịch sử (Historical Data Backfill) an toàn và có tính bất biến; chia nhỏ tác vụ theo phân vùng thời gian có kiểm soát, đối soát số lượng bản ghi (Pre/Post Row Counts), kiểm tra tính tương đương của chỉ số (Metric Parity Reconciliation) và ngăn chặn sự cố làm ô nhiễm dữ liệu của các đường ống xuôi dòng (Downstream Pipelines).

## 2. When to Use
- Khi phát hiện lỗi công thức tính toán trong mã ETL cũ và cần chạy lại toàn bộ dữ liệu của 6 tháng trước.
- Khi bổ sung thêm một cột thông tin mới vào bảng lịch sử và cần nạp bù giá trị cho các năm cũ.
- Khi di chuyển dữ liệu từ hệ thống cũ sang nền tảng kho dữ liệu mới mà cần đảm bảo không thất thoát dữ liệu.

## 3. When NOT to Use
- Khi chỉ sửa một bản ghi đơn lẻ trực tiếp bằng tay trong môi trường phát triển.
- Khi dữ liệu luồng thời gian thực đang chạy bình thường không có nhu cầu tính toán lại quá khứ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Công cụ điều phối luồng công việc (Airflow, Dagster hoặc script Python), bản sao lưu dự phòng của bảng dữ liệu mục tiêu, chỉ số đối soát chuẩn.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Partition-by-Partition Execution:** Chia nhỏ việc nạp bù dữ liệu thành từng khoảng thời gian nhỏ (ví dụ từng ngày hoặc từng tuần) thay vì chạy một mẻ lớn làm sập hệ thống.
- **Idempotent Overwrite:** Sử dụng cơ chế ghi đè nguyên tử từng phân vùng (`INSERT OVERWRITE PARTITION`) để nếu có chạy lại nhiều lần thì kết quả vẫn không bị trùng lặp bản ghi.
- **Metric Parity Check:** So sánh tổng số tiền hoặc số lượng người dùng giữa bảng cũ và bảng vừa nạp bù; nếu sai lệch vượt quá ngưỡng cho phép (0.001%), lập tức hoàn tác.

## 6. Step-by-Step Execution Workflow
1. Tạo bản sao lưu ảnh chụp (Snapshot Backup) của bảng dữ liệu mục tiêu trước khi can thiệp.
2. Viết kịch bản nạp bù dữ liệu có tham số hóa ngày bắt đầu `start_date` và ngày kết thúc `end_date`.
3. Chạy thử nghiệm trên một phân vùng duy nhất và thực hiện đối soát số liệu pre/post.
4. Kích hoạt chạy tuần tự cho toàn bộ các phân vùng lịch sử với cơ chế kiểm soát tốc độ (Throttling) để không làm nghẽn tài nguyên chung.
5. Lập biên bản nghiệm thu đối soát dữ liệu nạp bù `BACKFILL_RECONCILIATION_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Controlled Partitioned Backfill Runner with Parity Check
import datetime

def run_backfill_partition(date_str: str, db_conn):
    print(f"Starting atomic backfill for date: {date_str}")
    # 1. Snapshot baseline metric before update
    baseline_sum = db_conn.query(f"SELECT SUM(revenue) FROM fct_sales WHERE sale_date = '{date_str}'")

    # 2. Atomic overwrite partition
    db_conn.execute(f"""
        INSERT OVERWRITE TABLE fct_sales PARTITION (sale_date = '{date_str}')
        SELECT id, amount - discount AS revenue, customer_id, '{date_str}' 
        FROM staging_sales WHERE sale_date = '{date_str}';
    """)

    # 3. Reconcile parity
    new_sum = db_conn.query(f"SELECT SUM(revenue) FROM fct_sales WHERE sale_date = '{date_str}'")
    diff_pct = abs(new_sum - baseline_sum) / (baseline_sum + 1e-6)
    print(f"Partition {date_str} completed. Parity variance: {diff_pct:.4f}")
    assert diff_pct < 0.05, f"Parity check failed on {date_str}!" 
```

## 8. Anti-Patterns & Common Traps
- Chạy một câu lệnh `UPDATE` khổng lồ trên toàn bộ bảng 500 triệu dòng mà không có phân vùng, làm khóa bảng cơ sở dữ liệu suốt 8 tiếng.
- Dùng lệnh `INSERT INTO` thông thường mà không có khóa bất biến, khiến việc chạy lại khi gặp lỗi mạng làm nhân đôi toàn bộ dữ liệu doanh thu.
- Không thông báo cho các đội ngũ phân tích hạ nguồn khiến họ tưởng số liệu bị đột biến và gửi báo cáo sai cho ban giám đốc.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các tác vụ nạp bù dữ liệu được thực thi dưới dạng ghi đè nguyên tử từng phân vùng (Idempotent Overwrite).
- QG-02: Số lượng bản ghi và tổng chỉ số kiểm soát sau khi nạp bù khớp chính xác với tiêu chí nghiệm thu đề ra.
- QG-03: Có sẵn kế hoạch hoàn tác (Rollback Plan) đã được kiểm chứng trước khi chạy trên dữ liệu sản xuất.

## 10. Security & Safety Boundaries
- Giới hạn quyền chạy backfill chỉ cho các tài khoản quản trị chuyên dụng; lưu nhật ký kiểm toán người kích hoạt và lý do thực hiện.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Script điều phối nạp bù dữ liệu có kiểm soát `backfill_orchestrator.py`.
1. Biên bản đối soát số liệu nạp bù `BACKFILL_RECONCILIATION_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-schema-evolution`](.agents/skills/dex-schema-evolution/SKILL.md)
- [`dex-data-quality-audits`](.agents/skills/dex-data-quality-audits/SKILL.md)
- [`dex-disaster-recovery`](.agents/skills/dex-disaster-recovery/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát hiện mã tính thuế VAT trong bảng báo cáo tài chính của năm 2025 bị áp sai tỷ lệ 8% thay vì 10%. Kỹ sư kích hoạt `dex-backfill-reconciliation`, lập kịch bản nạp bù từng ngày cho 365 ngày của năm 2025, chạy đối soát tự động sau mỗi ngày nạp và hoàn thành tính lại toàn bộ số liệu chuẩn xác mà không làm gián đoạn các báo cáo đang chạy của công ty.
