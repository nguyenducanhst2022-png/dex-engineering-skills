---
name: dex-sast-finding-triage
description: Triage, validate, and remediate Static Application Security Testing (SAST) findings, eliminating false positives and tracing true-positive source-to-sink taint flows. Use when processing automated security scan reports.
---

# dex-sast-finding-triage

## 1. Purpose & Scope
Sàng lọc, thẩm định và xử lý các cảnh báo an ninh ứng dụng từ công cụ phân tích tĩnh (SAST Finding Triage: SonarQube, Semgrep, CodeQL, Checkmarx); phân tích luồng dữ liệu ô nhiễm từ nguồn tới đích (Taint Flow: Source to Sink), phân biệt chính xác giữa lỗi thực tế (True Positives) và cảnh báo giả (False Positives), và lập kế hoạch vá lỗi hiệu quả cho đội ngũ phát triển.

## 2. When to Use
- Báo cáo SAST định kỳ trả về hàng trăm cảnh báo bảo mật khiến lập trình viên bị quá tải và bỏ qua.
- Chuẩn bị nghiệm thu bảo mật cho đợt phát hành phần mềm lớn.
- Tích hợp SAST gate vào CI/CD pipeline và cần thiết lập ngưỡng chặn (Quality Gate Thresholds) hợp lý.

## 3. When NOT to Use
- Không tự ý đóng cảnh báo với lý do 'False Positive' mà không có bằng chứng phân tích luồng dữ liệu xác thực hoặc chú thích kỹ thuật rõ ràng.
- Không dùng SAST để phát hiện các lỗ hổng mang tính logic nghiệp vụ phức tạp khi runtime (cần DAST hoặc PenTest).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Báo cáo kết quả quét bảo mật (File SARIF / JSON / Sonar report).
- Mã nguồn dự án tại commit tương ứng.
- Bối cảnh kiến trúc của ứng dụng (Public facing vs Internal microservice).
- **Điều kiện tiên quyết**:
- Có quyền truy cập vào mã nguồn và công cụ quản lý cảnh báo bảo mật (DefectDojo, GitHub Security).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Taint Analysis Model:
  + Source: Điểm đầu vào của dữ liệu từ người dùng không tin cậy (Request params, Headers, Cookies, File upload).
  + Sanitizer / Validator: Hàm kiểm tra hoặc làm sạch dữ liệu (Regex check, HTML escape, Parameterized query).
  + Sink: Điểm thực thi nguy hiểm nếu dữ liệu ô nhiễm chạm tới (Database execution, Shell command, HTML render, Eval).
- True Positive vs False Positive: Cảnh báo chỉ là True Positive khi tồn tại một đường đi trực tiếp từ Source tới Sink mà không có bất kỳ Sanitizer hữu hiệu nào ở giữa.
- **Quy tắc quyết định kỹ thuật**:
- Nếu cảnh báo có độ nghiêm trọng Critical/High và có đường đi Taint Flow xác thực: tạo ticket P0 sửa lỗi ngay lập tức.
- Nếu đóng cảnh báo là False Positive: bắt buộc ghi rõ mã lý do (Reason Code) và người thẩm định chịu trách nhiệm.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Thẩm định sai, đóng cảnh báo SQL Injection vì nghĩ rằng 'endpoint này chỉ dùng nội bộ', sau đó bị kẻ tấn công khai thác qua mạng nội bộ.

## 6. Step-by-Step Execution Workflow
1. Nhập file SARIF từ công cụ quét vào dashboard thẩm định.
2. Lọc bỏ các cảnh báo trùng lặp và các cảnh báo nằm trong thư mục test/fixtures.
3. Đối với từng cảnh báo High/Critical: vẽ đường đi Taint Analysis từ Source tới Sink.
4. Xác minh xem dữ liệu đã được làm sạch bởi framework hay chưa.
5. Nếu là True Positive: viết đoạn code vá mẫu (Fix recommendation) và tạo issue cho dev.
6. Nếu là False Positive: gắn nhãn suppress kèm comment giải thích lý do vào file cấu hình SAST.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Semgrep Rule Suppression kèm lý giải thẩm định an ninh
# file: src/api/export.py
def export_data(user_id):
    # nosemgrep: python.lang.security.audit.sqli.hardcoded-sql-expression
    # AUDIT-REASON: user_id đã được validate bằng UUID v4 regex tại API gateway layer,
    # giá trị an toàn tuyệt đối và câu lệnh chỉ đọc read-only.
    cursor.execute(f"SELECT * FROM exports WHERE user_id = '{user_id}'")
```

### Lệnh xác minh & thực thi:
```bash
# Quét lại mã nguồn để xác nhận các cảnh báo đã được triage hoặc sửa xong
semgrep scan --config auto --sarif --output report.sarif
```

## 8. Anti-Patterns & Common Traps
- Tắt toàn bộ rule của scanner vì nó báo quá nhiều lỗi (thay vì tinh chỉnh rule cho phù hợp).
- Đánh dấu 'Wont Fix' hàng loạt mà không có sự đồng thuận của bộ phận Security.

## 9. Quality Gates & Acceptance Criteria
- 0 cảnh báo Critical True-Positive nào còn tồn đọng trước khi phát hành release.
- 100% cảnh báo được đánh dấu False Positive có ghi chú giải trình rõ ràng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Bản báo cáo SARIF chứa chi tiết lỗ hổng phải được lưu trữ trong kho lưu trữ bảo mật có phân quyền nghiêm ngặt.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Bảng đối soát phân loại cảnh báo (SAST Triage Matrix).
- File SARIF đã làm sạch và các bản vá lỗi bảo mật cụ thể.

## 13. Related & Complementary Skills
dex-static-analysis-rule-authoring, dex-vulnerability-remediation, dex-dast-scoping

## 14. Realistic Usage Example
### Tình huống thực tế:
Một dự án ngân hàng nhận báo cáo Checkmarx với 420 cảnh báo bảo mật, khiến toàn bộ tiến độ release bị đình trệ. Nhóm chuyên gia SAST Triage đã rà soát và phát hiện 380 cảnh báo là False Positives do công cụ không nhận diện được hàm mã hóa chuẩn của framework nội bộ. 40 lỗ hổng thực tế còn lại (gồm 3 lỗi SQLi và 5 lỗi Path Traversal) đã được phân loại ưu tiên và vá xong trong 3 ngày, đưa dự án về đích an toàn.
