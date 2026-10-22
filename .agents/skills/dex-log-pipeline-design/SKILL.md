---
name: dex-log-pipeline-design
description: Design scalable, structured, observable log collection and processing pipelines with correlation IDs, redaction of sensitive data (PII), and tiered storage policies. Use when centralizing telemetry across large distributed clusters.
---

# dex-log-pipeline-design

## 1. Purpose & Scope
Thiết kế, xây dựng và tối ưu hóa đường ống thu thập và xử lý nhật ký (Log Pipeline: Fluentbit, Vector, Logstash, Loki, Elasticsearch/OpenSearch); cấu trúc hóa JSON logs, gắn định danh tương quan (Correlation/Trace IDs), tự động bôi đen dữ liệu nhạy cảm (PII Redaction) và thiết lập chính sách lưu trữ phân tầng tiết kiệm chi phí.

## 2. When to Use
- Nhật ký phân tán rải rác trên hàng trăm container khiến việc điều tra sự cố gặp khó khăn.
- Chi phí lưu trữ log trên Datadog/Splunk tăng phi mã vượt ngân sách.
- Rò rỉ dữ liệu thẻ tín dụng hoặc mật khẩu vào log hệ thống vi phạm tiêu chuẩn bảo mật (PCI-DSS/GDPR).

## 3. When NOT to Use
- Không sử dụng log cho các số liệu thống kê thời gian thực cần tần suất cao (hãy dùng Prometheus metrics).
- Không ghi log văn bản tự do (unstructured text) cho các hệ thống quy mô lớn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Định dạng log hiện tại của các dịch vụ (Stdout, syslog, file).
- Khối lượng log sinh ra mỗi ngày (GB/ngày).
- Yêu cầu tuân thủ về thời gian lưu trữ (Retention policy: Hot, Warm, Cold).
- **Điều kiện tiên quyết**:
- Các ứng dụng có thể ghi log ra chuẩn `stdout/stderr` dưới định dạng JSON có cấu trúc.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Structured Logging: Mọi dòng log là một đối tượng JSON hợp lệ chứa các trường chuẩn hóa: `timestamp`, `level`, `trace_id`, `service`, `message`.
- PII Redaction at the Edge: Làm sạch các trường nhạy cảm (`password`, `access_token`, `card_number`) ngay tại agent thu thập (Vector/Fluentbit) trước khi gửi qua mạng.
- Tiered Storage: Dữ liệu log 7 ngày đầu lưu ở bộ nhớ nhanh (Hot/SSD), từ ngày 8-30 lưu ở Warm, sau 30 ngày nén đưa vào S3 Glacier (Cold) để lưu trữ pháp lý.
- **Quy tắc quyết định kỹ thuật**:
- Nếu log không chứa `trace_id`: gắn định danh tự sinh tại proxy đầu vào để đảm bảo truy vết toàn trình.
- Không bao giờ lưu log DEBUG trên môi trường production trong điều kiện vận hành bình thường.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Một dịch vụ bị lỗi vòng lặp in hàng triệu dòng log mỗi giây làm tắc nghẽn log collector và làm đầy ổ đĩa toàn bộ node Kubernetes.

## 6. Step-by-Step Execution Workflow
1. Chuẩn hóa format JSON log trong thư viện framework dùng chung của công ty.
2. Cấu hình Vector hoặc Fluentbit làm DaemonSet trên từng node để thu thập stdout.
3. Viết bộ lọc regex/VRL để bôi đen dữ liệu nhạy cảm (PII scrubbing).
4. Cấu hình đệm chống tràn (Disk buffer) trong trường hợp cụm Elasticsearch/Loki bị nghẽn.
5. Thiết lập lifecycle policy tự động chuyển log cũ sang S3 và xóa sau hạn mức quy định.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Vector configuration for PII redaction and structured routing
transforms:
  redact_pii:
    type: "remap"
    inputs: ["kubernetes_logs"]
    source: |
      # Masking credit cards
      .message = replace(.message, r'[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}', "****-****-****-****")
      # Masking authorization headers
      if exists(.headers.authorization) {
        .headers.authorization = "[REDACTED]"
      }
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra cấu hình Vector và giả lập luồng log
vector validate --config /etc/vector/vector.yaml
```

## 8. Anti-Patterns & Common Traps
- Ghi log chuỗi cộng chuỗi (string concatenation) thay vì structured logging.
- Thu thập log trực tiếp từ container gửi qua HTTP đồng bộ khiến ứng dụng bị chậm theo khi log server lag.

## 9. Quality Gates & Acceptance Criteria
- 100% log được phân loại có `trace_id` hợp lệ và 0% dữ liệu thẻ tín dụng thô lọt vào log storage.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quyền truy cập vào hệ thống log tập trung phải được kiểm soát nghiêm ngặt theo vai trò (RBAC) và có audit log người xem.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- File cấu hình DaemonSet Vector/Fluentbit hoàn chỉnh.
- Tài liệu chuẩn hóa cấu trúc JSON log chung cho toàn tổ chức.

## 13. Related & Complementary Skills
dex-alert-quality-engineering, dex-metric-cardinality-control, dex-distributed-tracing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ngân hàng số phát hiện lập trình viên vô tình log toàn bộ request payload chứa OTP và số thẻ vào CloudWatch. Đội ngũ SRE đã triển khai đường ống Vector DaemonSet với bộ lọc VRL tự động bôi đen thông tin nhạy cảm ngay tại node cục bộ trong 0.2ms, ngăn chặn nguy cơ rò rỉ dữ liệu quy mô lớn.
