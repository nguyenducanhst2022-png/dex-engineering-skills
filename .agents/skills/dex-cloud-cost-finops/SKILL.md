---
name: dex-cloud-cost-finops
description: Analyze, attribute, and optimize cloud infrastructure costs using FinOps principles, resource right-sizing, idle asset reclamation, spot/savings plan strategies, and unit economics. Use when managing, reducing, or forecasting cloud spend.
---

# dex-cloud-cost-finops

## 1. Purpose & Scope
Phân tích, phân bổ và tối ưu hóa chi phí sử dụng hạ tầng đám mây theo nguyên lý FinOps (Cloud Financial Operations); gắn thẻ chi phí (Cost Allocation Tagging), phát hiện và thu hồi tài nguyên lãng phí/nhàn rỗi (Unattached EBS, Idle Load Balancers, Abandoned Snapshots), tối ưu hóa cấu hình tài nguyên (Right-Sizing CPU/RAM), áp dụng chiến lược Cam kết sử dụng (Savings Plans, Reserved Instances) và xây dựng mô hình chỉ số kinh tế đơn vị (Unit Economics: Chi phí trên mỗi giao dịch).

## 2. When to Use
- Khi hóa đơn đám mây (AWS, GCP, Azure) tăng đột biến mà không rõ nguyên nhân từ tính năng nào.
- Khi ban giám đốc yêu cầu cắt giảm 20-30% chi phí hạ tầng mà không làm suy giảm hiệu năng và độ ổn định.
- Khi cần phân bổ chi phí cloud chính xác cho từng đội ngũ kỹ thuật (Showback / Chargeback).

## 3. When NOT to Use
- Xử lý lỗi crash ứng dụng hoặc bug code (dùng `dex-root-cause-debugging`).
- Thiết lập cấu hình auto-scaling cơ bản của Kubernetes (dùng `dex-kubernetes-deployment`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Dữ liệu hóa đơn chi tiết (AWS Cost and Usage Report - CUR, GCP Cloud Billing Export).
- Chỉ số sử dụng tài nguyên thực tế trong 30 ngày (CloudWatch CPU/Memory metrics, Kube-cost).
- Danh sách tài nguyên nhàn rỗi và chính sách tag chi phí của doanh nghiệp.
- **Điều kiện tiên quyết**:
- Quyền truy cập báo cáo chi phí (AWS Cost Explorer, Billing Console) hoặc công cụ OpenCost / Kubecost.
- Chính sách Cost Allocation Tags (`Environment`, `Team`, `Service`, `CostCenter`) đã được kích hoạt.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **FinOps Lifecycle (Inform -> Optimize -> Operate)**: Minh bạch chi phí (ai tiêu tiền gì) -> Tối ưu hóa (tắt đồ thừa, mua cam kết giảm giá) -> Vận hành (đưa chỉ số chi phí vào KPI kỹ thuật).
- **Unit Economics**: Đo lường chi phí đám mây trên một đơn vị giá trị kinh doanh (ví dụ: `Chi phí hạ tầng / Số đơn hàng thành công`), giúp phân biệt tăng chi phí do tăng trưởng lành mạnh hay do lãng phí.
- **Right-Sizing Strategy**: Đưa dung lượng CPU/RAM được cấp phát tiệm cận với mức sử dụng thực tế (P95 usage + 20% headroom).
- **Quy tắc quyết định kỹ thuật**:
- **Tất Cả Tài Nguyên Phải Được Gắn Tag**: Mọi tài nguyên không có tag `Owner` và `Environment` hợp lệ sẽ bị cảnh báo và tự động đánh dấu để rà soát xóa bỏ.
- **Thu Hồi Tài Nguyên Mồ Côi Ngay Lập Tức**: Xóa bỏ các volume ổ cứng không gắn vào máy chủ (`available` EBS) hoặc Elastic IP không sử dụng sau 7 ngày.
- **Ưu Tiên Mua Savings Plans Cho Tải Ổn Định (Baseline Load)**: Chỉ mua Savings Plans / Reserved Instances cho phần tải nền chạy 24/7; phần tải co giãn dùng On-Demand hoặc Spot Instances.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Cắt giảm quá đà làm crash hệ thống vào giờ cao điểm**: Hạ cấu hình server xuống quá thấp mà không tính đến peak traffic -> Khắc phục: Phân tích chỉ số P99 trong 30 ngày và kiểm thử tải trước khi hạ cấu hình.
- **Mua cam kết dài hạn cho hệ thống sắp bị khai tử**: Mua RI 3 năm cho dịch vụ sắp migrate sang serverless -> Khắc phục: Đối chiếu lộ trình kiến trúc trước khi ký cam kết tài chính.

## 6. Step-by-Step Execution Workflow
1. Thu thập dữ liệu báo cáo chi phí từ AWS Cost Explorer / Kubecost và phân nhóm theo dịch vụ/đội ngũ.
2. Thực hiện rà soát tài nguyên mồ côi (Unattached EBS, Old Snapshots, Idle ALBs, Idle NAT Gateways) và dọn dẹp an toàn.
3. Phân tích chỉ số CPU/Memory Utilization của cụm máy chủ/container để đề xuất Right-Sizing.
4. Đánh giá tính khả thi của việc chuyển đổi sang CPU kiến trúc ARM64 (AWS Graviton) để tiết kiệm 20-40% chi phí.
5. Đánh giá tỷ lệ tải nền ổn định và đề xuất gói Compute Savings Plans 1 năm không trả trước (No Upfront).
6. Thiết lập cảnh báo chi phí tăng đột biến (Cost Anomaly Detection Alert) qua Slack.
7. Xây dựng báo cáo Unit Economics hàng tháng và trình bày cho ban lãnh đạo.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Script quét và báo cáo các ổ đĩa EBS không sử dụng (Unattached EBS Volumes)
import boto3

def scan_unattached_ebs(region="ap-southeast-1"):
    ec2 = boto3.client("ec2", region_name=region)
    volumes = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"]
    
    total_wasted_gb = 0
    wasted_volumes = []
    for v in volumes:
        size = v["Size"]
        vol_id = v["VolumeId"]
        total_wasted_gb += size
        wasted_volumes.append({"id": vol_id, "size_gb": size, "type": v["VolumeType"]})
        
    print(f"Tìm thấy {len(volumes)} ổ EBS nhàn rỗi. Tổng dung lượng lãng phí: {total_wasted_gb} GB")
    return wasted_volumes

if __name__ == "__main__":
    scan_unattached_ebs()
```

### Lệnh xác minh & thực thi:
- Quét cảnh báo chi phí bất thường: `aws ce get-anomalies --date-interval Start=2026-10-01,End=2026-10-22`
- Kiểm tra danh sách ổ đĩa mồ côi: `aws ec2 describe-volumes --filters Name=status,Values=available --query 'Volumes[*].[VolumeId,Size]' --output table`
- Xem tỷ lệ bao phủ của Savings Plans: `aws ce get-savings-plans-coverage --time-period Start=2026-09-01,End=2026-10-01`

## 8. Anti-Patterns & Common Traps
- **Bật máy chủ Dev/Staging chạy xuyên suốt cuối tuần**: Gây lãng phí 30-40% chi phí môi trường thử nghiệm (cần tự động tắt ngoài giờ làm việc).
- **Bỏ quên NAT Gateway trong mỗi AZ**: NAT Gateway tốn phí cố định $32/tháng/cổng cộng phí băng thông ngay cả khi không có traffic.
- **Lưu trữ dữ liệu vĩnh viễn trên S3 Standard**: Không thiết lập Lifecycle policy chuyển dữ liệu cũ sang Glacier sau 90 ngày.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tỷ lệ tài nguyên có tag chi phí đạt tối thiểu 95%.
- QG-08: Thu hồi 100% các tài nguyên nhàn rỗi đã được xác nhận không sử dụng.
- QG-11: Tiết kiệm tối thiểu 15% tổng chi phí hàng tháng sau đợt tối ưu hóa.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Luôn tạo Snapshot sao lưu trước khi xóa bỏ bất kỳ ổ đĩa hoặc cơ sở dữ liệu nhàn rỗi nào.
- Chỉ cấp quyền đọc (ReadOnlyAccess) cho các công cụ phân tích chi phí của bên thứ ba.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm toán chi phí đám mây (Cloud Cost Audit Report).
- Kế hoạch thu hồi tài nguyên nhàn rỗi và lộ trình Right-sizing.
- Bảng theo dõi chỉ số Unit Economics hàng tháng.

## 13. Related & Complementary Skills
- `dex-infrastructure-as-code`: Cập nhật cấu hình kích thước máy chủ vào code Terraform.
- `dex-capacity-planning`: Dự phóng nhu cầu tài nguyên trong tương lai.
- `dex-storage-lifecycle`: Tự động chuyển đổi tầng lưu trữ dữ liệu rẻ hơn.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một startup tăng trưởng nhanh nhận thấy chi phí AWS tăng từ $10,000 lên $28,000/tháng. Áp dụng `dex-cloud-cost-finops`, kỹ sư phát hiện $4,000 lãng phí từ các EBS volume cũ và snapshot không dùng, chuyển đổi 80% máy chủ EC2 sang chip Graviton3 (tiết kiệm 20%), cấu hình tắt môi trường Dev vào ban đêm và mua Compute Savings Plan cho tải nền. Kết quả giảm hóa đơn xuống $16,500/tháng mà không làm giảm tốc độ phát triển.
