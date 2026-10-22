---
name: dex-cloud-resource-tagging
description: Design, enforce, and automate cloud resource tagging taxonomies (FinOps, Cost Allocation, Ownership, Lifecycle) using policy-as-code and automated remediations. Use to gain financial visibility and clean untagged cloud sprawl.
---

# dex-cloud-resource-tagging

## 1. Purpose & Scope
Thiết kế, cưỡng chế và tự động hóa khung định danh thẻ tài nguyên đám mây (Cloud Resource Tagging Taxonomy: FinOps, Phân bổ chi phí, Đội ngũ sở hữu, Vòng đời môi trường); áp dụng Policy-as-Code để chặn việc tạo tài nguyên 'mồ côi' không có thẻ, mang lại sự minh bạch tài chính và tự động dọn dẹp lãng phí tài nguyên đám mây.

## 2. When to Use
- Hóa đơn Cloud hàng tháng tăng vọt nhưng không rõ đội ngũ hoặc dịch vụ nào đang tiêu tốn nhiều tiền nhất.
- Hàng trăm máy ảo EC2, ổ đĩa EBS và snapshot vô chủ không ai dám xóa vì không biết của ai.
- Chuẩn bị triển khai thực hành quản lý tài chính đám mây (FinOps).

## 3. When NOT to Use
- Không gắn các thông tin nhạy cảm (mật khẩu, email cá nhân) vào Tag của tài nguyên.
- Không thiết kế quá nhiều thẻ bắt buộc (>10 tags) gây khó khăn cho việc triển khai nhanh của các kỹ sư.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh mục các thẻ bắt buộc (Required Tags: `Environment`, `Owner`, `Project`, `CostCenter`).
- Công cụ cưỡng chế (AWS Organizations Tag Policies, Azure Policy, Terraform tflint).
- Công cụ phân tích chi phí (AWS Cost Explorer, Kubecost).
- **Điều kiện tiên quyết**:
- Có quyền quản trị AWS Organizations hoặc Cloud Governance để áp dụng chính sách toàn tài khoản.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Core Tagging Taxonomy: Bốn nhóm thẻ cốt lõi:
  + Business: `Owner` (email đội ngũ), `Project`, `CostCenter`.
  + Technical: `Environment` (prod, staging, dev), `Application`, `Role`.
  + Security: `DataClassification` (public, confidential, restricted).
  + Automation: `AutoStop` (opt-in cho dev tắt máy ngoài giờ làm việc), `Retention`.
- Preventive Enforcement: Dùng SCP (Service Control Policy) hoặc Terraform chặn tạo tài nguyên nếu thiếu các thẻ bắt buộc.
- **Quy tắc quyết định kỹ thuật**:
- Nếu một tài nguyên thiếu thẻ `Owner`: gửi cảnh báo sau 24h và tự động dừng (Stop) sau 7 ngày nếu không cập nhật.
- 100% tài nguyên môi trường Development phải có thẻ `AutoStop: true` để tắt máy vào 20:00 tối các ngày trong tuần.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Sử dụng quy ước viết hoa/thường không nhất quán (ví dụ: `env`, `Env`, `Environment`), khiến hệ thống phân tích chi phí coi đó là 3 thẻ khác nhau và báo cáo sai lệch.

## 6. Step-by-Step Execution Workflow
1. Soạn thảo tài liệu Tiêu chuẩn Gắn thẻ Tài nguyên Cloud chuẩn cho toàn công ty.
2. Cấu hình Terraform `default_tags` ở cấp độ AWS Provider để tự động gắn thẻ cho mọi tài nguyên.
3. Thiết lập AWS Tag Policy ở cấp độ Organization để phát hiện các thẻ sai chính tả.
4. Viết script tự động quét tìm các tài nguyên 'mồ côi' (Untagged Resources) hàng tuần.
5. Tích hợp báo cáo phân bổ chi phí lên Dashboard FinOps của công ty.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```hcl
# Terraform: Tự động gắn thẻ chuẩn hóa cho toàn bộ tài nguyên trong AWS Provider
provider "aws" {
  region = "ap-southeast-1"
  default_tags {
    tags = {
      Environment = "Production"
      Owner       = "team-data-platform"
      Project     = "DataLake-v2"
      CostCenter  = "CC-8421"
      ManagedBy   = "Terraform"
    }
  }
}
```

### Lệnh xác minh & thực thi:
```bash
# Quét tìm các tài nguyên không có thẻ Owner trong tài khoản AWS
aws resourcegroupstaggingapi get-resources --tag-filters Key=Owner,Values=[]
```

## 8. Anti-Patterns & Common Traps
- Cho phép lập trình viên tạo tài nguyên tùy tiện trên console web mà không có thẻ.
- Đặt giá trị thẻ là tên một cá nhân cụ thể (người đó nghỉ việc thì tài nguyên vô chủ; phải dùng tên Team hoặc Mail Group).

## 9. Quality Gates & Acceptance Criteria
- 98% tài nguyên trên toàn bộ các tài khoản Cloud có đầy đủ 4 thẻ bắt buộc.
- 0 tài nguyên mới nào được tạo qua CI/CD nếu thiếu thẻ bắt buộc.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Giá trị của các tag không được chứa thông tin bí mật hay dữ liệu PII.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Tài liệu quy chuẩn Tagging Taxonomy chính thức.
- File cấu hình AWS Tag Policy và dashboard phân tích chi phí FinOps.

## 13. Related & Complementary Skills
dex-cloud-iam-policy-review, dex-cloud-network-design, dex-platform-service-catalog

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ có hóa đơn AWS đạt $150,000/tháng nhưng ban giám đốc không thể bóc tách chi phí của từng sản phẩm. Sau khi áp dụng chuẩn Tagging tự động qua Terraform default_tags kết hợp AWS Cost Categories, họ bóc tách chính xác chi phí từng team đến từng cent và phát hiện 15 cụm test bị bỏ quên tốn $22,000/tháng, dọn dẹp tiết kiệm ngay lập tức.
