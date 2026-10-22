---
name: dex-cloud-network-design
description: Architect secure, isolated, and scalable cloud network topologies including VPCs, private subnets, transit gateways, VPC peering, and egress filtering. Use when establishing enterprise cloud network foundations.
---

# dex-cloud-network-design

## 1. Purpose & Scope
Thiết kế, xây dựng và quản trị cấu trúc liên kết mạng đám mây (Cloud Network Topology: VPCs, Private/Public Subnets, NAT Gateways, Transit Gateways, VPC Peering, PrivateLink); thiết lập các ranh giới cô lập mạng nghiêm ngặt, kiểm soát lưu lượng ra vào (Egress/Ingress Filtering) và tối ưu hóa chi phí truyền tải dữ liệu.

## 2. When to Use
- Khởi tạo hạ tầng môi trường Cloud mới cho doanh nghiệp.
- Kết nối các microservices ở các VPC hoặc các tài khoản Cloud khác nhau mà không đi qua Internet công cộng.
- Yêu cầu bảo mật cách ly hoàn toàn cơ sở dữ liệu không có Public IP.

## 3. When NOT to Use
- Không thiết kế hệ thống mạng đa tầng quá phức tạp nếu dự án chỉ là ứng dụng nhỏ chạy trên 1-2 container.
- Không lạm dụng VPC Peering toàn phần (Full-mesh peering) khi số lượng VPC > 10 (hãy dùng Transit Gateway).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Dải địa chỉ IP mạng (CIDR blocks: ví dụ `10.0.0.0/16`).
- Danh sách các dịch vụ cần truy cập Internet (Egress) và dịch vụ chỉ chạy nội bộ (Private).
- Yêu cầu về băng thông và dự phòng thảm họa đa vùng (Multi-AZ).
- **Điều kiện tiên quyết**:
- Có quyền quy hoạch kiến trúc mạng và tạo Network Resources qua Terraform/CloudFormation.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Subnet Segmentation: Chia mạng thành 3 tầng: Public (chỉ đặt ALB), Private (đặt ứng dụng/EKS), Isolated/Database (đặt RDS/Redis, không có đường ra Internet).
- AWS PrivateLink / VPC Endpoints: Kết nối tới các dịch vụ AWS (S3, DynamoDB, SQS) qua mạng cáp quang nội bộ của AWS, vừa tăng tốc độ vừa loại bỏ chi phí truyền tải qua NAT Gateway.
- Network Security Groups vs NACLs: Security Groups là stateful filter tại tầng instance; NACLs là stateless filter tại tầng subnet.
- **Quy tắc quyết định kỹ thuật**:
- Tuyệt đối không cấp Public IP cho các Database instances, Cache cluster hay backend pods.
- Sử dụng tối thiểu 3 Availability Zones (AZs) cho VPC để đảm bảo tính sẵn sàng cao.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Xung đột dải địa chỉ IP (CIDR Overlap) giữa các VPC khiến việc kết nối Peering hoặc VPN về trụ sở công ty bị thất bại.

## 6. Step-by-Step Execution Workflow
1. Lập bảng phân bổ dải mạng CIDR không trùng lặp cho các môi trường (Dev, Staging, Prod).
2. Viết mã Terraform khởi tạo VPC, Subnets theo từng Availability Zone.
3. Cấu hình bảng định tuyến (Route Tables), Internet Gateway và NAT Gateways.
4. Thiết lập VPC Endpoints cho S3 và ECR để tiết kiệm chi phí data transfer.
5. Áp dụng Flow Logs để giám sát và ghi vết toàn bộ lưu lượng mạng.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```hcl
# Terraform: Thiết kế Subnet Database hoàn toàn cô lập
resource "aws_subnet" "database" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet("10.0.0.0/16", 4, count.index + 8)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "prod-subnet-db-az${count.index + 1}"
    Tier = "Isolated"
  }
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra định tuyến và bảng phân bổ mạng trong Terraform
terraform plan -target=module.vpc
```

## 8. Anti-Patterns & Common Traps
- Đặt cơ sở dữ liệu trong Public Subnet và chỉ dựa vào mật khẩu để bảo vệ.
- Sử dụng dải CIDR quá nhỏ (`/24`) khiến VPC bị hết địa chỉ IP khi hệ thống Kubernetes scale pod.

## 9. Quality Gates & Acceptance Criteria
- 100% cơ sở dữ liệu và cache nằm trong Isolated Subnet không có route ra Internet Gateway.
- Bật VPC Flow Logs trên 100% các VPC môi trường production.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi luồng truy cập quản trị (SSH/RDP) bắt buộc phải đi qua Bastion Host/AWS Systems Manager Session Manager có MFA.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Module Terraform kiến trúc VPC chuẩn hóa.
- Sơ đồ kiến trúc mạng Cloud (Network Topology Diagram).

## 13. Related & Complementary Skills
dex-cloud-iam-policy-review, dex-gitops-workflows, dex-kubernetes-policy-enforcement

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty thanh toán phát hiện hóa đơn AWS NAT Gateway lên tới $8,000/tháng do các container kéo ảnh từ ECR và đọc file từ S3 qua Internet. Bằng cách thiết lập S3 Gateway Endpoint và ECR Interface Endpoint qua PrivateLink, chi phí NAT Gateway giảm về dưới $400/tháng và loại bỏ hoàn toàn nguy cơ tấn công từ mạng công cộng.
