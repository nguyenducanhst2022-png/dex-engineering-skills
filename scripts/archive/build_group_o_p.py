# -*- coding: utf-8 -*-
"""
Generator for Group O (141-150: Advanced Cloud Platform) and Group P (151-160: Language & Runtime Engineering).
Adheres strictly to the Agent Skills Specification with 14 mandatory sections.
"""

import os
import sys

SKILL_TEMPLATE = """---
name: {skill_id}
description: {desc}
---

# {skill_id}

## 1. Purpose & Scope
{purpose}

## 2. When to Use
{activation}

## 3. When NOT to Use
{when_not_to_use}

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
{inputs}
- **Điều kiện tiên quyết**:
{preconditions}

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
{core_concepts}
- **Quy tắc quyết định kỹ thuật**:
{decision_rules}
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
{failure_scenarios}

## 6. Step-by-Step Execution Workflow
{workflow}

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
{example}

### Lệnh xác minh & thực thi:
{verification_commands}

## 8. Anti-Patterns & Common Traps
{anti_patterns}

## 9. Quality Gates & Acceptance Criteria
{quality_gates}
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
{security_constraints}
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
{expected_outputs}

## 13. Related & Complementary Skills
{related_skills}

## 14. Realistic Usage Example
### Tình huống thực tế:
{realistic_usage}
"""

SKILLS_O_P = {
    # 141. dex-serverless-architecture
    "dex-serverless-architecture": {
        "desc": "Architect, optimize, and secure event-driven serverless architectures (AWS Lambda, Google Cloud Run) mitigating cold starts, managing concurrency limits, and ensuring idempotency. Use when building autoscaling, pay-per-use backend systems.",
        "purpose": "Thiết kế, xây dựng và tối ưu hóa kiến trúc không máy chủ (Serverless Architecture: AWS Lambda, GCP Cloud Run, Azure Functions); quản lý và triệt tiêu độ trễ khởi động nguội (Cold Start), kiểm soát giới hạn đồng thời (Concurrency Limits), bảo đảm tính bình thản (Idempotency) của các sự kiện và tối ưu hóa chi phí vận hành.",
        "activation": "- Xây dựng hệ thống backend xử lý sự kiện không đồng bộ (Event-driven) có lưu lượng biến thiên mạnh.\n- Cần tối ưu chi phí hạ tầng máy chủ cho các ứng dụng có khoảng thời gian rảnh rỗi kéo dài.\n- Chuyển đổi các tác vụ xử lý ảnh, video, dữ liệu hàng loạt (batch) sang kiến trúc phi tập trung.",
        "when_not_to_use": "- Không dùng Serverless cho các tác vụ tính toán kéo dài liên tục nhiều giờ (vượt quá giới hạn timeout 15 phút của Lambda).\n- Không dùng khi cần duy trì kết nối WebSocket thường trực cho hàng triệu người dùng mà không có managed gateway.",
        "inputs": "- Nguồn phát sự kiện (Event sources: S3, SQS, Kinesis, EventBridge, API Gateway).\n- Ngân sách tài nguyên (Memory: 128MB - 10GB, Timeout limit).\n- Yêu cầu về độ trễ phản hồi (P95 latency requirement).",
        "preconditions": "- Có tài khoản AWS/GCP với quyền tạo IAM Role và triển khai Lambda/Cloud Run.",
        "core_concepts": "- Cold Start: Thời gian cloud provider khởi tạo container mới và nạp runtime. Giảm thiểu bằng cách tối ưu kích thước bundle, dùng ngôn ngữ biên dịch sẵn (Rust, Go) hoặc Provisioned Concurrency.\n- Database Connection Exhaustion: Hàng ngàn Lambda instances sinh ra đồng thời có thể đánh sập PostgreSQL/MySQL truyền thống (phải dùng RDS Proxy hoặc Serverless DB như DynamoDB/Aurora Serverless).\n- Event Deduplication: Sự kiện từ SQS/Kafka có thể bị gửi lặp lại (at-least-once delivery), bắt buộc xử lý idempotent.",
        "decision_rules": "- Nếu tác vụ yêu cầu độ trễ P99 < 50ms: sử dụng Provisioned Concurrency hoặc chuyển sang Go/Rust thay vì Java/Node.\n- Khởi tạo SDK clients (AWS SDK, DB pool) bên ngoài hàm handler để tái sử dụng giữa các lần thực thi ấm (Warm execution).",
        "failure_scenarios": "- Cấu hình timeout của Lambda ngắn hơn timeout của downstream API khiến Lambda bị ngắt giữa chừng trong khi downstream vẫn đang thực thi.",
        "workflow": "1. Thiết kế sơ đồ luồng sự kiện phân tán từ nguồn tới đích.\n2. Cấu hình cấp phát RAM và CPU tương ứng (AWS Lambda tự động scale CPU theo RAM).\n3. Tích hợp RDS Proxy để quản lý connection pooling.\n4. Triển khai cơ chế lưu vết khóa Idempotency Key trên DynamoDB với TTL tự động.\n5. Đóng gói mã nguồn tối giản (Tree-shaking, loại bỏ devDependencies) và triển khai qua Serverless Framework/SAM.",
        "example": "```typescript\nimport { SQSHandler } from 'aws-lambda';\nimport { DynamoDBClient } from '@aws-sdk/client-dynamodb';\n\n// Khởi tạo client bên ngoài handler để tái sử dụng context\nconst ddb = new DynamoDBClient({});\n\nexport const handler: SQSHandler = async (event) => {\n  for (const record of event.Records) {\n    const messageId = record.messageId;\n    // Kiểm tra idempotency key trước khi xử lý\n    if (await isAlreadyProcessed(messageId)) continue;\n    await processOrder(JSON.parse(record.body));\n    await markProcessed(messageId);\n  }\n};\n```",
        "verification_commands": "```bash\n# Kiểm tra độ trễ cold start bằng plugin serverless\nsls invoke -f processOrder --log\n```",
        "anti_patterns": "- Mở kết nối Database mới bên trong thân hàm handler cho mỗi request.\n- Lưu trữ trạng thái tạm (in-memory state) và kỳ vọng nó tồn tại ở lần gọi tiếp theo.",
        "quality_gates": "- Giảm dung lượng gói deploy zip < 15MB để giữ Cold Start dưới 250ms.\n- 100% các event handler xử lý an toàn trước các tin nhắn trùng lặp.",
        "security_constraints": "- Nguyên tắc đặc quyền tối thiểu (Least Privilege IAM): mỗi hàm chỉ có quyền đọc/ghi đúng resource cần thiết.",
        "expected_outputs": "- File cấu hình kiến trúc Serverless (`serverless.yml` hoặc `template.yaml`).\n- Mã nguồn handler tối ưu hóa kèm cơ chế chống trùng lặp sự kiện.",
        "related_skills": "dex-edge-runtime-engineering, dex-cloud-iam-policy-review, dex-distributed-consistency",
        "realistic_usage": "Một công ty bảo hiểm sử dụng Lambda để bóc tách hồ sơ PDF gửi lên S3. Khi có bão lũ, lượng hồ sơ tăng đột biến gấp 50 lần. Nhờ kiến trúc Serverless kết hợp SQS Dead-Letter Queue và RDS Proxy, hệ thống tự động scale lên 1,500 worker đồng thời và xử lý xong 100,000 hồ sơ trong 20 phút mà không tốn một đồng chi phí máy chủ nhàn rỗi trước đó."
    },

    # 142. dex-edge-runtime-engineering
    "dex-edge-runtime-engineering": {
        "desc": "Build ultra-low latency globally distributed applications on Edge runtimes (Cloudflare Workers, V8 isolates, Fastly Compute) managing memory constraints and edge caching. Use for global personalization, auth gating, and A/B routing.",
        "purpose": "Thiết kế, lập trình và tối ưu hóa các ứng dụng phân tán toàn cầu chạy trên Edge Runtimes (Cloudflare Workers, Vercel Edge, Deno Deploy, Fastly Compute) dựa trên công nghệ V8 Isolates; xử lý giới hạn bộ nhớ chặt chẽ, tối ưu hóa Edge Caching và giảm thiểu độ trễ mạng xuống mức cận 0 (sub-10ms) cho người dùng toàn cầu.",
        "activation": "- Cần thực hiện xác thực (Auth Gating), A/B testing routing hoặc Geo-redirection ngay tại CDN Edge trước khi request chạm vào máy chủ gốc (Origin).\n- Xây dựng API toàn cầu yêu cầu độ trễ phản hồi dưới 20ms trên toàn thế giới.\n- Tối ưu hóa việc biến đổi nội dung (HTML rewrite, Image optimization) tức thì tại biên.",
        "when_not_to_use": "- Không dùng Edge Runtimes cho các ứng dụng phụ thuộc vào các thư viện C++ native hoặc thư viện Node.js cần filesystem access (`fs`).\n- Không dùng cho các tác vụ cần thời gian tính toán CPU vượt quá 50ms trên mỗi request.",
        "inputs": "- V8 Isolate runtime environment specs (Node.js API compatibility layer).\n- Cơ chế lưu trữ tại biên (Cloudflare KV, D1 SQL, Durable Objects, Fastly KV).\n- Quy tắc bộ nhớ cache (Cache-Control, Stale-While-Revalidate).",
        "preconditions": "- Mã nguồn tuân thủ tiêu chuẩn Web Standards API (Fetch, Request, Response, Streams, SubtleCrypto).",
        "core_concepts": "- V8 Isolates vs Containers: V8 Isolates khởi động trong chưa đầy 5ms và tiêu thụ vài KB bộ nhớ, nhanh hơn hàng ngàn lần so với khởi động một container Linux.\n- Edge Storage Tradeoffs: Bộ nhớ KV tại Edge có tính nhất quán cuối cùng (Eventual Consistency toàn cầu), phù hợp cho việc đọc thường xuyên và ít ghi.\n- Stale-While-Revalidate: Trả về nội dung cache cũ ngay lập tức cho người dùng trong khi âm thầm tải nội dung mới từ máy chủ gốc dưới nền.",
        "decision_rules": "- Nếu kích thước mã nguồn vượt quá 1MB: thực hiện code-splitting hoặc chuyển bớt logic nặng về backend origin.\n- Nếu cần chia sẻ trạng thái đồng bộ có tính nhất quán cao: sử dụng Durable Objects thay vì KV.",
        "failure_scenarios": "- Lỗi sử dụng các API đặc thù của Node.js như `process.version` hoặc `child_process` khiến Worker bị sập khi khởi chạy trên Edge.",
        "workflow": "1. Khởi tạo dự án Worker tuân thủ Web Standards API bằng Wrangler.\n2. Cấu hình các route biên và quy tắc cache tại điểm hiện diện (PoP).\n3. Tích hợp Edge KV hoặc Durable Objects để lưu cấu hình tính năng (Feature flags).\n4. Kiểm thử cục bộ bằng môi trường mô phỏng `miniflare` hoặc `workerd`.\n5. Triển khai phân phối tự động tới hơn 300 trung tâm dữ liệu toàn cầu.",
        "example": "```typescript\nexport default {\n  async fetch(request: Request, env: any): Promise<Response> {\n    const url = new URL(request.url);\n    const country = request.headers.get('cf-ipcountry') || 'US';\n    \n    // Tự động route người dùng tới máy chủ gốc gần nhất\n    if (url.pathname.startsWith('/api/v1/feed')) {\n      const cache = caches.default;\n      let response = await cache.match(request);\n      if (!response) {\n        response = await fetch(`https://${country}.origin.example.com${url.pathname}`);\n        // Cache tại Edge trong 60 giây\n        response = new Response(response.body, response);\n        response.headers.set('Cache-Control', 'public, max-age=60');\n        await cache.put(request, response.clone());\n      }\n      return response;\n    }\n    return fetch(request);\n  }\n};\n```",
        "verification_commands": "```bash\nnpx wrangler dev --local\n# Triển khai thử nghiệm lên edge network\nnpx wrangler deploy --dry-run\n```",
        "anti_patterns": "- Cố gắng mở TCP socket kết nối trực tiếp tới cơ sở dữ liệu truyền thống mà không qua connection pooling proxy tại Edge.\n- Bỏ qua giới hạn CPU time (10ms-50ms) dẫn đến lỗi Worker Exceeded CPU Limit.",
        "quality_gates": "- Thời gian phản hồi P95 tại Edge đạt dưới 15ms cho các request hit cache.\n- Bundle size sau khi nén phải nhỏ hơn 500KB.",
        "security_constraints": "- Không lưu trữ Master Secret Key dài hạn trong biến môi trường của Worker; sử dụng Edge Secrets được mã hóa.",
        "expected_outputs": "- Mã nguồn Edge Worker chuẩn hóa TypeScript.\n- File cấu hình triển khai `wrangler.toml` kèm bộ kiểm thử cục bộ.",
        "related_skills": "dex-serverless-architecture, dex-web-security-headers, dex-frontend-architecture",
        "realistic_usage": "Một trang tin tức toàn cầu bị nghẽn server khi có sự kiện bầu cử. Họ chuyển toàn bộ tầng xác thực paywall và định tuyến quốc gia lên Cloudflare Workers tại biên. 85% lưu lượng được xử lý ngay tại Edge với độ trễ 8ms, giảm 90% tải cho cụm máy chủ trung tâm."
    },

    # 143. dex-cloud-iam-policy-review
    "dex-cloud-iam-policy-review": {
        "desc": "Audit, sanitize, and enforce Least-Privilege IAM policies, role boundaries, and access conditions across AWS, GCP, and Azure. Use to eliminate privilege escalation paths and over-permissioned service accounts.",
        "purpose": "Kiểm toán, rà soát và cưỡng chế nguyên tắc đặc quyền tối thiểu (Least Privilege) cho chính sách IAM (Identity & Access Management) trên AWS, GCP, Azure; phát hiện và loại bỏ các quyền nguy hiểm (`*`), các đường dẫn leo thang đặc quyền (Privilege Escalation), và bảo vệ các Service Accounts trong hệ thống Cloud.",
        "activation": "- Chuẩn bị cho kỳ đánh giá kiểm toán an ninh thông tin (SOC2, ISO 27001, PCI-DSS).\n- Phát hiện các IAM Roles được cấp quyền Admin (`AdministratorAccess` hoặc `*.*`) vô tội vạ.\n- Sau khi một nhân sự kỹ thuật rời khỏi dự án hoặc thay đổi nhà thầu phát triển.",
        "when_not_to_use": "- Không tự tiện thu hồi hàng loạt quyền trên production khi chưa phân tích CloudTrail/Access Analyzer để biết quyền đó có đang được ứng dụng sử dụng hay không.\n- Không dùng để quản lý phân quyền trong ứng dụng người dùng cuối (dùng RBAC/ABAC nội bộ).",
        "inputs": "- File chính sách IAM (JSON/Terraform IAM definitions).\n- Nhật ký sử dụng quyền thực tế (AWS CloudTrail, IAM Access Advisor, GCP Policy Analyzer).\n- Danh sách các tài nguyên nhạy cảm (S3 buckets, KMS keys, Secret Manager).",
        "preconditions": "- Có quyền truy cập chỉ đọc vào IAM và các công cụ phân tích truy cập trên Cloud Console.",
        "core_concepts": "- Least Privilege: Chỉ cấp đúng các action (như `s3:GetObject`) trên đúng ARN tài nguyên cụ thể (chứ không phải `s3:*` trên `*`).\n- Permission Boundaries: Ranh giới tối đa mà một Role có thể cấp cho các Role khác, ngăn chặn việc dev tự tạo role mới để leo thang lên Admin.\n- Unused Access Removal: Thu hồi các quyền không được sử dụng trong vòng 90 ngày qua.",
        "decision_rules": "- Bất kỳ policy nào chứa `Action: \"*\"` hoặc `Resource: \"*\"` phải bị gắn cờ nghiêm trọng (Critical Finding).\n- Mọi IAM Role dùng cho ứng dụng bắt buộc phải có điều kiện `Condition` ràng buộc theo VPC, IP nội bộ hoặc tag hợp lệ.",
        "failure_scenarios": "- Xóa nhầm quyền `kms:Decrypt` của một service đang chạy khiến dịch vụ không thể giải mã cơ sở dữ liệu và bị ngưng trệ.",
        "workflow": "1. Quét toàn bộ IAM policies bằng công cụ tự động (Policy Sentry, Prowler, Checkov).\n2. Xuất báo cáo Access Advisor để xác định các action không được gọi trong 90 ngày qua.\n3. Viết lại chính sách IAM thu hẹp phạm vi vào các ARN cụ thể.\n4. Áp dụng Permission Boundary để khóa chặt quyền tự cấp phép.\n5. Kiểm tra lại bằng AWS IAM Policy Simulator trước khi apply chính thức.",
        "example": "```json\n// Chính sách IAM chuẩn Least-Privilege cho microservice đơn hàng\n{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Sid\": \"AllowSpecificS3BucketReadWrite\",\n      \"Effect\": \"Allow\",\n      \"Action\": [\n        \"s3:GetObject\",\n        \"s3:PutObject\"\n      ],\n      \"Resource\": \"arn:aws:s3:::company-order-invoices-prod/*\"\n    },\n    {\n      \"Sid\": \"DenyUnencryptedTraffic\",\n      \"Effect\": \"Deny\",\n      \"Action\": \"s3:*\",\n      \"Resource\": \"arn:aws:s3:::company-order-invoices-prod/*\",\n      \"Condition\": {\n        \"Bool\": { \"aws:SecureTransport\": \"false\" }\n      }\n    }\n  ]\n}\n```",
        "verification_commands": "```bash\n# Phân tích cú pháp và tìm lỗi wildcard trong IAM Policy bằng Parliament\nparliament --file policies/app-iam-policy.json\n```",
        "anti_patterns": "- Đính kèm policy `AdministratorAccess` cho các EC2 Instance hoặc ECS Tasks để 'chạy cho tiện'.\n- Chia sẻ chung một IAM Role cho nhiều microservices khác nhau.",
        "quality_gates": "- 0 quyền `Action: *` tồn tại trong mã nguồn Terraform triển khai production.\n- 100% IAM Roles đều có Resource ARN chỉ định rõ ràng.",
        "security_constraints": "- Mọi thao tác thay đổi IAM policy phải được thực hiện qua Pull Request có review và lưu audit log.",
        "expected_outputs": "- Báo cáo kiểm toán IAM (Audit Report).\n- Bộ file Terraform IAM policies đã được tinh chỉnh đạt chuẩn Least-Privilege.",
        "related_skills": "dex-cloud-network-design, dex-kubernetes-policy-enforcement, dex-security-logging-detection",
        "realistic_usage": "Một startup fintech chuẩn bị thẩm định SOC2. Chuyên gia IAM rà soát và phát hiện Lambda xử lý thanh toán có quyền `iam:CreatePolicy` và `s3:*` toàn bộ tài khoản. Bằng cách tái cấu trúc policy về đúng 4 actions trên đúng 1 S3 bucket và 1 DynamoDB table, startup đã vượt qua bài kiểm toán bảo mật xuất sắc."
    },

    # 144. dex-cloud-network-design
    "dex-cloud-network-design": {
        "desc": "Architect secure, isolated, and scalable cloud network topologies including VPCs, private subnets, transit gateways, VPC peering, and egress filtering. Use when establishing enterprise cloud network foundations.",
        "purpose": "Thiết kế, xây dựng và quản trị cấu trúc liên kết mạng đám mây (Cloud Network Topology: VPCs, Private/Public Subnets, NAT Gateways, Transit Gateways, VPC Peering, PrivateLink); thiết lập các ranh giới cô lập mạng nghiêm ngặt, kiểm soát lưu lượng ra vào (Egress/Ingress Filtering) và tối ưu hóa chi phí truyền tải dữ liệu.",
        "activation": "- Khởi tạo hạ tầng môi trường Cloud mới cho doanh nghiệp.\n- Kết nối các microservices ở các VPC hoặc các tài khoản Cloud khác nhau mà không đi qua Internet công cộng.\n- Yêu cầu bảo mật cách ly hoàn toàn cơ sở dữ liệu không có Public IP.",
        "when_not_to_use": "- Không thiết kế hệ thống mạng đa tầng quá phức tạp nếu dự án chỉ là ứng dụng nhỏ chạy trên 1-2 container.\n- Không lạm dụng VPC Peering toàn phần (Full-mesh peering) khi số lượng VPC > 10 (hãy dùng Transit Gateway).",
        "inputs": "- Dải địa chỉ IP mạng (CIDR blocks: ví dụ `10.0.0.0/16`).\n- Danh sách các dịch vụ cần truy cập Internet (Egress) và dịch vụ chỉ chạy nội bộ (Private).\n- Yêu cầu về băng thông và dự phòng thảm họa đa vùng (Multi-AZ).",
        "preconditions": "- Có quyền quy hoạch kiến trúc mạng và tạo Network Resources qua Terraform/CloudFormation.",
        "core_concepts": "- Subnet Segmentation: Chia mạng thành 3 tầng: Public (chỉ đặt ALB), Private (đặt ứng dụng/EKS), Isolated/Database (đặt RDS/Redis, không có đường ra Internet).\n- AWS PrivateLink / VPC Endpoints: Kết nối tới các dịch vụ AWS (S3, DynamoDB, SQS) qua mạng cáp quang nội bộ của AWS, vừa tăng tốc độ vừa loại bỏ chi phí truyền tải qua NAT Gateway.\n- Network Security Groups vs NACLs: Security Groups là stateful filter tại tầng instance; NACLs là stateless filter tại tầng subnet.",
        "decision_rules": "- Tuyệt đối không cấp Public IP cho các Database instances, Cache cluster hay backend pods.\n- Sử dụng tối thiểu 3 Availability Zones (AZs) cho VPC để đảm bảo tính sẵn sàng cao.",
        "failure_scenarios": "- Xung đột dải địa chỉ IP (CIDR Overlap) giữa các VPC khiến việc kết nối Peering hoặc VPN về trụ sở công ty bị thất bại.",
        "workflow": "1. Lập bảng phân bổ dải mạng CIDR không trùng lặp cho các môi trường (Dev, Staging, Prod).\n2. Viết mã Terraform khởi tạo VPC, Subnets theo từng Availability Zone.\n3. Cấu hình bảng định tuyến (Route Tables), Internet Gateway và NAT Gateways.\n4. Thiết lập VPC Endpoints cho S3 và ECR để tiết kiệm chi phí data transfer.\n5. Áp dụng Flow Logs để giám sát và ghi vết toàn bộ lưu lượng mạng.",
        "example": "```hcl\n# Terraform: Thiết kế Subnet Database hoàn toàn cô lập\nresource \"aws_subnet\" \"database\" {\n  count             = 3\n  vpc_id            = aws_vpc.main.id\n  cidr_block        = cidrsubnet(\"10.0.0.0/16\", 4, count.index + 8)\n  availability_zone = data.aws_availability_zones.available.names[count.index]\n\n  tags = {\n    Name = \"prod-subnet-db-az${count.index + 1}\"\n    Tier = \"Isolated\"\n  }\n}\n```",
        "verification_commands": "```bash\n# Kiểm tra định tuyến và bảng phân bổ mạng trong Terraform\nterraform plan -target=module.vpc\n```",
        "anti_patterns": "- Đặt cơ sở dữ liệu trong Public Subnet và chỉ dựa vào mật khẩu để bảo vệ.\n- Sử dụng dải CIDR quá nhỏ (`/24`) khiến VPC bị hết địa chỉ IP khi hệ thống Kubernetes scale pod.",
        "quality_gates": "- 100% cơ sở dữ liệu và cache nằm trong Isolated Subnet không có route ra Internet Gateway.\n- Bật VPC Flow Logs trên 100% các VPC môi trường production.",
        "security_constraints": "- Mọi luồng truy cập quản trị (SSH/RDP) bắt buộc phải đi qua Bastion Host/AWS Systems Manager Session Manager có MFA.",
        "expected_outputs": "- Module Terraform kiến trúc VPC chuẩn hóa.\n- Sơ đồ kiến trúc mạng Cloud (Network Topology Diagram).",
        "related_skills": "dex-cloud-iam-policy-review, dex-gitops-workflows, dex-kubernetes-policy-enforcement",
        "realistic_usage": "Một công ty thanh toán phát hiện hóa đơn AWS NAT Gateway lên tới $8,000/tháng do các container kéo ảnh từ ECR và đọc file từ S3 qua Internet. Bằng cách thiết lập S3 Gateway Endpoint và ECR Interface Endpoint qua PrivateLink, chi phí NAT Gateway giảm về dưới $400/tháng và loại bỏ hoàn toàn nguy cơ tấn công từ mạng công cộng."
    },

    # 145. dex-gitops-workflows
    "dex-gitops-workflows": {
        "desc": "Implement declarative continuous deployment and reconciliation using GitOps engines (ArgoCD, FluxCD), managing environment drift, secrets, and rollbacks. Use to standardize Kubernetes application delivery.",
        "purpose": "Thiết kế, xây dựng và quản trị quy trình triển khai ứng dụng khai báo liên tục (GitOps Workflows: ArgoCD, FluxCD) trên cụm Kubernetes; đồng bộ tự động trạng thái mong muốn từ Git Repository, phát hiện và tự sửa chữa sai lệch cấu hình (Drift Detection & Self-healing), tích hợp quản lý secrets an toàn và hỗ trợ rollback tức thì.",
        "activation": "- Triển khai nhiều ứng dụng microservices trên các cụm Kubernetes (EKS, GKE, On-prem).\n- Quá trình deploy thủ công bằng lệnh `kubectl apply` từ máy dev gây ra sai lệch cấu hình giữa các môi trường.\n- Cần lịch sử kiểm toán (Audit Trail) minh bạch cho mọi thay đổi hạ tầng và ứng dụng thông qua Git commits.",
        "when_not_to_use": "- Không áp dụng GitOps cho các ứng dụng monolith đơn giản chỉ chạy trên một máy chủ ảo EC2 đơn lẻ.\n- Không lưu trữ plaintext credentials hoặc passwords trực tiếp vào Git repository.",
        "inputs": "- Git Repository chứa cấu hình khai báo (Kustomize overlays hoặc Helm charts).\n- Cụm Kubernetes mục tiêu và quyền truy cập cluster.\n- Giải pháp mã hóa bí mật (SealedSecrets, SOPS, External Secrets Operator).",
        "preconditions": "- ArgoCD hoặc FluxCD controller đã được cài đặt và vận hành trên cụm Kubernetes.",
        "core_concepts": "- Git as the Single Source of Truth: Trạng thái của cụm Kubernetes phải phản chiếu chính xác 100% nội dung khai báo trong Git repo.\n- Reconciliation Loop: Controller liên tục so sánh trạng thái thực tế (Live state) với trạng thái mong muốn trong Git (Target state); nếu có ai sửa tay bằng `kubectl`, controller sẽ tự động ghi đè về trạng thái của Git (Self-healing).\n- External Secrets Operator: Lấy secret từ AWS Secrets Manager/Vault và tạo Kubernetes Secret động.",
        "decision_rules": "- Cấu hình `autoSync` kèm `prune: true` để tự động dọn dẹp các tài nguyên bị xóa trong Git.\n- Bắt buộc kích hoạt `selfHeal: true` để ngăn chặn các kỹ sư sửa đổi trực tiếp vào cụm cluster.",
        "failure_scenarios": "- Cấu hình Git sai cú pháp YAML khiến ArgoCD liên tục sync lỗi làm nghẽn CPU của API Server.",
        "workflow": "1. Cấu trúc GitOps repository tách biệt giữa Code Repo và Config/Manifests Repo.\n2. Tổ chức manifests theo mô hình Kustomize (base và các overlays cho dev, staging, prod).\n3. Định nghĩa đối tượng `Application` hoặc `ApplicationSet` trong ArgoCD.\n4. Tích hợp External Secrets Operator để quản lý secret an toàn.\n5. Thiết lập thông báo trạng thái đồng bộ hóa qua Slack/Teams.",
        "example": "```yaml\n# ArgoCD Application Definition\napiVersion: argoproj.io/v1alpha1\nkind: Application\nmetadata:\n  name: payment-service-prod\n  namespace: argocd\nspec:\n  project: default\n  source:\n    repoURL: 'https://github.com/company/gitops-manifests.git'\n    targetRevision: main\n    path: apps/payment-service/overlays/prod\n  destination:\n    server: 'https://kubernetes.default.svc'\n    namespace: payment\n  syncPolicy:\n    automated:\n      prune: true\n      selfHeal: true\n    syncOptions:\n      - CreateNamespace=true\n```",
        "verification_commands": "```bash\n# Kiểm tra trạng thái đồng bộ của ứng dụng qua ArgoCD CLI\nargocd app get payment-service-prod\n```",
        "anti_patterns": "- Chạy lệnh `kubectl edit` hoặc `kubectl apply` trực tiếp trên cụm production được quản lý bởi GitOps.\n- Lưu trữ file `.env` chứa mật khẩu thật vào Git mà không mã hóa.",
        "quality_gates": "- 100% tài nguyên trên Kubernetes được đồng bộ ở trạng thái `Synced` và `Healthy`.\n- Mọi commit vào nhánh chính của GitOps repo phải có chữ ký GPG hoặc qua PR có phê duyệt.",
        "security_constraints": "- Quyền truy cập vào giao diện web của ArgoCD phải tích hợp SSO (OAuth2/OIDC) kèm RBAC theo nhóm.",
        "expected_outputs": "- Cấu trúc thư mục GitOps Kustomize chuẩn mực.\n- File manifest ArgoCD Application / Flux Kustomization hoàn chỉnh.",
        "related_skills": "dex-kubernetes-policy-enforcement, dex-environment-promotion, dex-platform-service-catalog",
        "realistic_usage": "Một kỹ sư mới vô tình chạy lệnh xóa nhầm Namespace trên cụm Kubernetes Staging. Nhờ cơ chế Self-healing của ArgoCD, toàn bộ 25 microservices, ingress và configs đã được tự động dựng lại nguyên vẹn sau 45 giây từ Git repository mà không mất công sức phục hồi thủ công."
    },

    # 146. dex-kubernetes-policy-enforcement
    "dex-kubernetes-policy-enforcement": {
        "desc": "Author, validate, and enforce cluster governance policies using admission controllers (OPA Gatekeeper, Kyverno) to prevent privilege escalations and unconstrained resource usage. Use when securing multi-tenant Kubernetes clusters.",
        "purpose": "Thiết kế, kiểm thử và cưỡng chế các chính sách quản trị cụm Kubernetes (Cluster Governance Policies) thông qua Admission Controllers (Kyverno, OPA Gatekeeper); ngăn chặn việc chạy container dưới quyền root, chặn gắn cờ privileged, bắt buộc khai báo resource limits/requests, và bảo đảm an toàn cho các cụm máy chủ đa người dùng (Multi-tenant Clusters).",
        "activation": "- Cần tuân thủ các tiêu chuẩn bảo mật container (CIS Kubernetes Benchmark, NSA/CISA Hardening Guide).\n- Ngăn chặn các lập trình viên quên khai báo giới hạn RAM/CPU làm ảnh hưởng đến các pod khác (Noisy Neighbors).\n- Chặn việc pull image từ các public registry không tin cậy (chỉ cho phép pull từ private ECR/Artifact Registry).",
        "when_not_to_use": "- Không áp dụng chính sách ở chế độ `Enforce` (chặn đứng) ngay lập tức khi chưa qua giai đoạn `Audit` (chỉ cảnh báo) để tránh làm gián đoạn các dịch vụ đang chạy.\n- Không dùng để thay thế Network Policies hoặc IAM Roles.",
        "inputs": "- Tiêu chuẩn bảo mật cần cưỡng chế (Pod Security Standards: Baseline, Restricted).\n- Công cụ Admission Controller (Kyverno hoặc OPA Gatekeeper).\n- Danh sách các namespaces được miễn trừ (ví dụ `kube-system`).",
        "preconditions": "- Cụm Kubernetes đã cài đặt Kyverno hoặc OPA Gatekeeper controller.",
        "core_concepts": "- Validating Webhooks: Chặn đứng các tài nguyên không hợp lệ ngay tại cổng API Server trước khi ghi vào etcd.\n- Mutating Webhooks: Tự động sửa đổi hoặc chèn thêm các trường mặc định (ví dụ: tự động chèn securityContext non-root nếu người dùng quên khai báo).\n- Pod Security Standards (PSS): Ba cấp độ bảo mật chuẩn của Kubernetes: Privileged, Baseline, Restricted.",
        "decision_rules": "- Ban đầu triển khai policy ở chế độ `validationFailureAction: Audit` trong 7 ngày để thu thập danh sách vi phạm.\n- Chuyển sang chế độ `Enforce` sau khi toàn bộ mã nguồn manifest đã được cập nhật tuân thủ.",
        "failure_scenarios": "- Viết webhook chặn nhầm các Pods của hệ thống giám sát hoặc mạng (`kube-proxy`, `calico`), khiến cụm cluster bị tê liệt.",
        "workflow": "1. Lập danh sách các quy tắc bắt buộc: cấm root, cấm hostNetwork, yêu cầu readOnlyRootFilesystem, giới hạn CPU/RAM.\n2. Viết Kyverno ClusterPolicy hoặc Gatekeeper ConstraintTemplates.\n3. Kiểm thử chính sách trên tệp manifests bằng Kyverno CLI cục bộ.\n4. Triển khai chính sách lên cụm ở chế độ Audit.\n5. Xem xét các báo cáo vi phạm và chuyển sang Enforce.",
        "example": "```yaml\n# Kyverno Policy: Bắt buộc chạy container dưới non-root user\napiVersion: kyverno.io/v1\nkind: ClusterPolicy\nmetadata:\n  name: require-run-as-non-root\nspec:\n  validationFailureAction: Enforce\n  background: true\n  rules:\n    - name: check-runAsNonRoot\n      match:\n        any:\n        - resources:\n            kinds: [Pod]\n      exclude:\n        any:\n        - resources:\n            namespaces: [kube-system]\n      validate:\n        message: \"Container bắt buộc phải chạy dưới user non-root!\"\n        pattern:\n          spec:\n            securityContext:\n              runAsNonRoot: true\n```",
        "verification_commands": "```bash\n# Kiểm tra chính sách cục bộ trước khi apply bằng Kyverno CLI\nkyverno test ./policies/\n```",
        "anti_patterns": "- Cho phép pod mount thư mục nhạy cảm của host (`/var/run/docker.sock`, `/etc`).\n- Không loại trừ namespace hệ thống (`kube-system`) khỏi các chính sách ngặt nghèo.",
        "quality_gates": "- 0 pod nào trong namespace ứng dụng vi phạm tiêu chuẩn Pod Security Standard Restricted.\n- 100% manifest deployment đều có khai báo `resources.limits` và `resources.requests`.",
        "security_constraints": "- Webhook của admission controller phải có cơ chế `failurePolicy: Ignore` hoặc timeout an toàn để tránh khóa toàn bộ API server khi controller bị lag.",
        "expected_outputs": "- Tập hợp các file YAML chính sách Kyverno / Gatekeeper.\n- Báo cáo kiểm toán vi phạm chính sách trên cụm (Policy Report).",
        "related_skills": "dex-container-image-engineering, dex-gitops-workflows, dex-cloud-iam-policy-review",
        "realistic_usage": "Một công ty công nghệ bị một tài khoản dev bị lộ token và kẻ tấn công cố tình deploy một pod đào tiền ảo chạy dưới quyền root kèm mount ổ đĩa host. Nhờ Kyverno Policy chặn đứng ngay lập tức tại API Server với thông báo 'Containers must not run as root', cuộc tấn công đã bị vô hiệu hóa hoàn toàn trước khi pod kịp khởi động."
    },

    # 147. dex-platform-service-catalog
    "dex-platform-service-catalog": {
        "desc": "Design and curate Internal Developer Platform (IDP) service catalogs (Backstage, Port) providing golden paths, service ownership, API documentation, and self-service scaffolding. Use to scale developer autonomy.",
        "purpose": "Thiết kế, xây dựng và quản trị Cổng danh mục dịch vụ nội bộ (Internal Developer Platform Service Catalog: Spotify Backstage, Port); thiết lập các 'con đường hoàng kim' (Golden Paths), định rõ quyền sở hữu dịch vụ (Service Ownership), tập trung hóa tài liệu API và cung cấp khả năng tự phục vụ (Self-service Scaffolding) cho các kỹ sư phần mềm.",
        "activation": "- Số lượng microservices trong công ty vượt quá 50 dịch vụ, không ai nắm rõ dịch vụ nào do ai quản lý.\n- Lập trình viên mới mất hàng tuần chỉ để xin quyền và dựng môi trường tạo mới một service.\n- Tài liệu API bị phân mảnh và lạc hậu trên nhiều trang wiki khác nhau.",
        "when_not_to_use": "- Không dựng hệ thống IDP cồng kềnh cho các công ty chỉ có dưới 15 kỹ sư phần mềm (chỉ cần file README và tài liệu chung).\n- Không biến Service Catalog thành một công cụ quan liêu gây cản trở tốc độ phát triển.",
        "inputs": "- Danh sách các microservices hiện có trong công ty.\n- Thông tin đội ngũ sở hữu (Teams, Slack channels, On-call rotation).\n- Bản mẫu scaffolding chuẩn (Software Templates cho Node, Python, Go).",
        "preconditions": "- Có hệ thống Git tập trung và định danh người dùng SSO (GitHub Org, Okta, Google Workspace).",
        "core_concepts": "- Golden Path: Một lộ trình mẫu được hỗ trợ đầy đủ bởi đội Platform (bao gồm template repo, CI/CD có sẵn, monitoring mặc định), giúp kỹ sư đi nhanh nhất mà không phải phát minh lại cái bánh xe.\n- `catalog-info.yaml`: File siêu dữ liệu nằm ngay trong mã nguồn của mỗi service khai báo tên, mô tả, team sở hữu, tài liệu API và dependencies.\n- Service Scorecard: Bảng đánh giá mức độ hoàn thiện của service (ví dụ: đã có CI chưa, coverage > 70% chưa, có runbook chưa).",
        "decision_rules": "- Mọi repository mới tạo ra bắt buộc phải có file `catalog-info.yaml` tại thư mục gốc.\n- Template scaffolding phải sinh ra một ứng dụng hoàn chỉnh có thể deploy ngay lập tức lên môi trường Dev.",
        "failure_scenarios": "- Triển khai Backstage nhưng không ai cập nhật thông tin khiến catalog trở thành 'nghĩa địa thông tin cũ'.",
        "workflow": "1. Chuẩn hóa schema của file `catalog-info.yaml` cho toàn công ty.\n2. Cài đặt và cấu hình Backstage hoặc Port kết nối với GitHub/GitLab.\n3. Xây dựng các Software Templates mẫu (ví dụ: Fastify Microservice, Go Gin API) kèm đầy đủ Dockerfile và CI.\n4. Tích hợp Scorecard để tự động chấm điểm độ sẵn sàng sản xuất của từng service.\n5. Đào tạo và hướng dẫn các đội ngũ áp dụng Golden Path cho dự án mới.",
        "example": "```yaml\n# catalog-info.yaml\napiVersion: backstage.io/v1alpha1\nkind: Component\nmetadata:\n  name: order-processing-service\n  description: 'Xử lý và thanh toán các đơn hàng trực tuyến'\n  tags: ['ecommerce', 'golang', 'p0']\nspec:\n  type: service\n  lifecycle: production\n  owner: team-checkout\n  system: core-banking\n  providesApis: ['order-api-v1']\n```",
        "verification_commands": "```bash\n# Xác minh tính hợp lệ của catalog-info.yaml bằng CLI\nnpx @backstage/cli catalog check\n```",
        "anti_patterns": "- Xây dựng Golden Path nhưng ép buộc cứng nhắc, không cho phép ngoại lệ khi có yêu cầu kỹ thuật đặc biệt.\n- Để tình trạng các dịch vụ 'mồ côi' (Orphan services) không có đội ngũ nào chịu trách nhiệm.",
        "quality_gates": "- 100% microservices trên production đều có team sở hữu và link PagerDuty rõ ràng.\n- Thời gian từ khi kỹ sư chọn template đến khi ứng dụng chạy trên dev dưới 10 phút.",
        "security_constraints": "- Quyền tạo mới tài nguyên hạ tầng qua self-service portal phải tuân thủ hạn mức ngân sách và có ranh giới bảo mật định sẵn.",
        "expected_outputs": "- Cổng thông tin Backstage/Port hoạt động ổn định.\n- Bộ Golden Path Templates chuẩn cho các ngôn ngữ chính của công ty.",
        "related_skills": "dex-environment-promotion, dex-gitops-workflows, dex-oncall-handover",
        "realistic_usage": "Một tập đoàn mở rộng từ 40 lên 120 kỹ sư, việc tạo một service mới thường mất 2 tuần để xin quyền hạ tầng và cấu hình CI. Đội Platform ra mắt Backstage Golden Path: kỹ sư chỉ cần nhập tên service trên giao diện web, hệ thống tự động sinh Git repo, cấu hình CI/CD, đăng ký DNS, tạo cụm test và xuất sẵn template Grafana trong đúng 8 phút."
    },

    # 148. dex-environment-promotion
    "dex-environment-promotion": {
        "desc": "Design deterministic, automated promotion pipelines moving identical immutable release artifacts across Dev, Staging, and Production with rigorous gate checks. Use to eliminate environment drift and release surprises.",
        "purpose": "Thiết kế và quản trị quy trình thăng cấp môi trường (Environment Promotion Pipelines) chuyển dịch các gói phát hành bất biến (Immutable Artifacts) qua chuỗi môi trường Dev -> Staging -> Production; áp dụng các cổng kiểm soát nghiêm ngặt (Release Gates), loại bỏ hiện tượng 'chạy được trên dev nhưng lỗi trên staging', và đảm bảo tính nhất quán tuyệt đối của mã nhị phân.",
        "activation": "- Xuất hiện tình trạng mã nguồn được build lại độc lập ở từng môi trường dẫn đến sai lệch phiên bản thư viện hoặc binary.\n- Quy trình release lên production thủ công, dễ nhầm lẫn và phụ thuộc vào một vài cá nhân.\n- Cần tự động hóa việc thăng cấp phiên bản sau khi các bài kiểm thử tự động trên Staging vượt qua thành công.",
        "when_not_to_use": "- Không build lại Docker image từ source code khi thăng cấp lên môi trường tiếp theo (phải thăng cấp chính digest SHA của image đã test ở Dev/Staging).\n- Không áp dụng cho các môi trường thử nghiệm tạm thời (Ephemeral Preview Environments).",
        "inputs": "- Digest SHA của container image hoặc build artifact bất biến.\n- Danh sách các biến môi trường và file cấu hình theo từng môi trường.\n- Tiêu chí thăng cấp (Pass 100% smoke test, approval từ QA/Lead).",
        "preconditions": "- Hệ thống CI/CD có hỗ trợ pipeline gates (GitHub Actions Environments, GitLab Environments).",
        "core_concepts": "- Build Once, Deploy Everywhere: Một container image duy nhất được build tại nhánh main và được test qua tất cả môi trường; cấu hình được bơm qua environment variables, tuyệt đối không thay đổi mã máy bên trong image.\n- GitOps Branch/Directory Promotion: Thăng cấp bằng cách cập nhật image tag trong file manifest của từng thư mục môi trường (`overlays/staging` -> `overlays/prod`) qua Pull Request.\n- Automated Smoke Testing: Sau khi deploy lên Staging, pipeline tự động chạy kiểm thử hồi quy trước khi cho phép kích hoạt nút thăng cấp Prod.",
        "decision_rules": "- Nếu bất kỳ bài smoke test nào trên Staging thất bại: khóa tự động tiến trình thăng cấp lên Production.\n- Triển khai lên Production bắt buộc phải có tối thiểu 1 phê duyệt từ người có thẩm quyền (Required Approvers).",
        "failure_scenarios": "- Deploy thẳng lên Production một image tag trôi nổi như `latest` thay vì immutable semantic version hoặc git commit SHA.",
        "workflow": "1. Build container image tại CI, gắn tag bằng Git commit SHA và digest (`sha256:...`).\n2. Tự động deploy lên môi trường Dev và chạy unit/integration tests.\n3. Thăng cấp lên Staging: cập nhật manifest Staging và kích hoạt E2E/Load tests.\n4. Khi Staging đạt 100% tiêu chí xanh: mở cổng yêu cầu phê duyệt Production.\n5. Thăng cấp lên Production kèm chiến lược Canary hoặc Blue/Green.",
        "example": "```yaml\n# GitHub Actions Environment Promotion Workflow\njobs:\n  deploy-prod:\n    needs: deploy-staging\n    runs-on: ubuntu-latest\n    environment:\n      name: production\n      url: https://app.example.com\n    steps:\n      - name: Promote Immutable Image to Production Manifest\n        run: |\n          IMAGE_SHA=\"${{ needs.deploy-staging.outputs.image_sha }}\"\n          # Cập nhật GitOps manifest của production với đúng SHA đã test tại Staging\n          yq eval \".images[0].digest = \\\"$IMAGE_SHA\\\"\" -i kustomize/overlays/prod/kustomization.yaml\n```",
        "verification_commands": "```bash\n# So sánh image digest giữa môi trường Staging và Production\nkustomize build kustomize/overlays/staging | grep 'image:'\nkustomize build kustomize/overlays/prod | grep 'image:'\n```",
        "anti_patterns": "- Biên dịch lại mã nguồn từ nhánh `staging` rồi lại biên dịch từ nhánh `production` (nguy cơ sai lệch commit).\n- Sửa trực tiếp biến môi trường của Production bằng tay trên console mà không lưu vào cấu hình quản lý.",
        "quality_gates": "- 100% artifact được deploy lên Production phải trùng khớp hoàn toàn Digest SHA với artifact đã chạy thành công trên Staging.\n- Phải có biên bản phê duyệt điện tử trước khi release Production.",
        "security_constraints": "- Quyền thăng cấp lên Production chỉ được cấp cho những người được ủy quyền thông qua quy trình phê duyệt MFA.",
        "expected_outputs": "- Pipeline CI/CD đa môi trường với Approval Gates.\n- Lịch sử audit log của từng đợt thăng cấp môi trường.",
        "related_skills": "dex-gitops-workflows, dex-platform-service-catalog, dex-container-image-engineering",
        "realistic_usage": "Một công ty SaaS trước đây build lại Dockerfile ở mỗi môi trường, dẫn đến sự cố một thư viện npm bị tác giả cập nhật âm thầm khiến Production bị sập trong khi Staging vẫn chạy tốt. Sau khi áp dụng nguyên lý Build Once với immutable digest promotion, họ đã chấm dứt hoàn toàn các lỗi bất ngờ khi đưa code lên môi trường thật."
    },

    # 149. dex-service-discovery
    "dex-service-discovery": {
        "desc": "Architect, tune, and debug resilient service discovery mechanisms using DNS-based, client-side, and control-plane registries (CoreDNS, Envoy, Consul). Use when microservices fail to resolve or route dynamically.",
        "purpose": "Thiết kế, tinh chỉnh và xử lý sự cố cơ chế khám phá dịch vụ (Service Discovery: CoreDNS, Consul, Envoy Control Plane, AWS Cloud Map); bảo đảm các dịch vụ tìm thấy nhau một cách động, xử lý cân bằng tải phía client hoặc qua Service Mesh, và chống sụp đổ do ngộ độc bộ nhớ đệm DNS (DNS Cache Poisoning / TTL Misconfigurations).",
        "activation": "- Microservices gặp lỗi `Name or service not known` hoặc kết nối tới các IP của pod đã bị xóa (Stale IPs).\n- Cụm CoreDNS trong Kubernetes bị quá tải CPU do các ứng dụng liên tục gửi truy vấn DNS mỗi khi gọi API.\n- Cần kết nối linh hoạt giữa các dịch vụ chạy trên Kubernetes với các dịch vụ legacy chạy trên máy chủ ảo.",
        "when_not_to_use": "- Không cần thiết lập Consul cluster phức tạp nếu ứng dụng chỉ chạy thuần túy trên một cụm Kubernetes duy nhất (CoreDNS nội bộ là đủ).\n- Không dùng hardcoded IP tĩnh cho các dịch vụ đám mây có tính co giãn động.",
        "inputs": "- Kiến trúc kết nối mạng giữa các dịch vụ.\n- Cấu hình DNS client (ndots, search domains, resolv.conf).\n- Cơ chế đăng ký dịch vụ (Service Registry: Kubernetes Service, Consul, Eureka).",
        "preconditions": "- Có quyền kiểm tra cấu hình CoreDNS hoặc Service Mesh trong cụm cluster.",
        "core_concepts": "- CoreDNS `ndots:5` Problem: Mặc định trong Linux/Kubernetes, nếu tên miền có ít hơn 5 dấu chấm, client sẽ thử tìm kiếm lần lượt qua các search domains (`.default.svc.cluster.local`, `.svc.cluster.local`), sinh ra tới 4 truy vấn DNS lỗi trước khi hỏi ra ngoài Internet, làm nghẽn CoreDNS.\n- Client-side vs Server-side Discovery: Server-side đi qua Load Balancer trung gian; Client-side (như gRPC/Envoy) tự hỏi Registry và kết nối trực tiếp tới IP đích, giảm một hop mạng.\n- DNS Negative Caching: Khi một pod đang khởi động chưa kịp sẵn sàng, DNS có thể cache trạng thái NXDOMAIN làm ứng dụng không gọi được trong suốt thời gian TTL.",
        "decision_rules": "- Với các ứng dụng có tần suất gọi API lớn: bật NodeLocal DNSCache trong Kubernetes để giảm 80% tải cho CoreDNS.\n- Đặt DNS TTL trong ứng dụng ở mức 5-30 giây để cân bằng giữa tốc độ cập nhật IP mới và giảm tải truy vấn.",
        "failure_scenarios": "- Ứng dụng Java (JVM) mặc định cache kết quả DNS thành công mãi mãi (TTL = infinity), khi pod đích đổi IP mới thì app Java vẫn kết nối vào IP cũ và ném lỗi Connection Refused.",
        "workflow": "1. Rà soát cấu hình `/etc/resolv.conf` của ứng dụng và tinh chỉnh `ndots:2` nếu gọi domain ngoài.\n2. Cài đặt và cấu hình NodeLocal DNSCache trên từng Kubernetes node.\n3. Thiết lập thông số JVM `-Dnetworkaddress.cache.ttl=10` cho các dịch vụ Java.\n4. Cấu hình Health-based Service Registration trong Consul hoặc Envoy.\n5. Kiểm tra thời gian cập nhật danh sách endpoint khi một pod bị kill.",
        "example": "```yaml\n# Tối ưu hóa cấu hình DNS trong Kubernetes Pod Spec\nspec:\n  dnsConfig:\n    options:\n      - name: ndots\n        value: \"2\"\n      - name: single-request-reopen\n  containers:\n    - name: app\n      image: app:v1\n```",
        "verification_commands": "```bash\n# Kiểm tra độ trễ và đường đi phân giải DNS từ bên trong pod\nkubectl exec -it app-pod -- nslookup payment-service.default.svc.cluster.local\n```",
        "anti_patterns": "- Giữ nguyên thiết lập mặc định của JVM cache DNS vĩnh viễn trong môi trường Cloud động.\n- Hardcode IP của máy chủ vào file cấu hình ứng dụng.",
        "quality_gates": "- Thời gian phân giải DNS trung bình trong cụm phải dưới 1ms qua NodeLocal DNSCache.\n- Cập nhật và định tuyến sang IP mới trong vòng 3 giây sau khi pod cũ bị hủy.",
        "security_constraints": "- Bảo vệ Service Registry chống lại việc đăng ký giả mạo dịch vụ bằng cách áp dụng mTLS và Token Authentication.",
        "expected_outputs": "- File cấu hình tối ưu CoreDNS và NodeLocal DNSCache.\n- Báo cáo phân tích hiệu năng truy vấn DNS của cụm.",
        "related_skills": "dex-cloud-network-design, dex-service-failover, dex-kubernetes-policy-enforcement",
        "realistic_usage": "Một hệ thống thanh toán bị chậm vào giờ cao điểm, các kỹ sư phát hiện CoreDNS bị quá tải với 50,000 queries/giây. Sau khi phân tích lỗi `ndots:5` và triển khai NodeLocal DNSCache, số lượng truy vấn tới CoreDNS trung tâm giảm 85%, độ trễ phân giải DNS giảm từ 30ms xuống 0.2ms, chấm dứt hoàn toàn hiện tượng timeout."
    },

    # 150. dex-cloud-resource-tagging
    "dex-cloud-resource-tagging": {
        "desc": "Design, enforce, and automate cloud resource tagging taxonomies (FinOps, Cost Allocation, Ownership, Lifecycle) using policy-as-code and automated remediations. Use to gain financial visibility and clean untagged cloud sprawl.",
        "purpose": "Thiết kế, cưỡng chế và tự động hóa khung định danh thẻ tài nguyên đám mây (Cloud Resource Tagging Taxonomy: FinOps, Phân bổ chi phí, Đội ngũ sở hữu, Vòng đời môi trường); áp dụng Policy-as-Code để chặn việc tạo tài nguyên 'mồ côi' không có thẻ, mang lại sự minh bạch tài chính và tự động dọn dẹp lãng phí tài nguyên đám mây.",
        "activation": "- Hóa đơn Cloud hàng tháng tăng vọt nhưng không rõ đội ngũ hoặc dịch vụ nào đang tiêu tốn nhiều tiền nhất.\n- Hàng trăm máy ảo EC2, ổ đĩa EBS và snapshot vô chủ không ai dám xóa vì không biết của ai.\n- Chuẩn bị triển khai thực hành quản lý tài chính đám mây (FinOps).",
        "when_not_to_use": "- Không gắn các thông tin nhạy cảm (mật khẩu, email cá nhân) vào Tag của tài nguyên.\n- Không thiết kế quá nhiều thẻ bắt buộc (>10 tags) gây khó khăn cho việc triển khai nhanh của các kỹ sư.",
        "inputs": "- Danh mục các thẻ bắt buộc (Required Tags: `Environment`, `Owner`, `Project`, `CostCenter`).\n- Công cụ cưỡng chế (AWS Organizations Tag Policies, Azure Policy, Terraform tflint).\n- Công cụ phân tích chi phí (AWS Cost Explorer, Kubecost).",
        "preconditions": "- Có quyền quản trị AWS Organizations hoặc Cloud Governance để áp dụng chính sách toàn tài khoản.",
        "core_concepts": "- Core Tagging Taxonomy: Bốn nhóm thẻ cốt lõi:\n  + Business: `Owner` (email đội ngũ), `Project`, `CostCenter`.\n  + Technical: `Environment` (prod, staging, dev), `Application`, `Role`.\n  + Security: `DataClassification` (public, confidential, restricted).\n  + Automation: `AutoStop` (opt-in cho dev tắt máy ngoài giờ làm việc), `Retention`.\n- Preventive Enforcement: Dùng SCP (Service Control Policy) hoặc Terraform chặn tạo tài nguyên nếu thiếu các thẻ bắt buộc.",
        "decision_rules": "- Nếu một tài nguyên thiếu thẻ `Owner`: gửi cảnh báo sau 24h và tự động dừng (Stop) sau 7 ngày nếu không cập nhật.\n- 100% tài nguyên môi trường Development phải có thẻ `AutoStop: true` để tắt máy vào 20:00 tối các ngày trong tuần.",
        "failure_scenarios": "- Sử dụng quy ước viết hoa/thường không nhất quán (ví dụ: `env`, `Env`, `Environment`), khiến hệ thống phân tích chi phí coi đó là 3 thẻ khác nhau và báo cáo sai lệch.",
        "workflow": "1. Soạn thảo tài liệu Tiêu chuẩn Gắn thẻ Tài nguyên Cloud chuẩn cho toàn công ty.\n2. Cấu hình Terraform `default_tags` ở cấp độ AWS Provider để tự động gắn thẻ cho mọi tài nguyên.\n3. Thiết lập AWS Tag Policy ở cấp độ Organization để phát hiện các thẻ sai chính tả.\n4. Viết script tự động quét tìm các tài nguyên 'mồ côi' (Untagged Resources) hàng tuần.\n5. Tích hợp báo cáo phân bổ chi phí lên Dashboard FinOps của công ty.",
        "example": "```hcl\n# Terraform: Tự động gắn thẻ chuẩn hóa cho toàn bộ tài nguyên trong AWS Provider\nprovider \"aws\" {\n  region = \"ap-southeast-1\"\n  default_tags {\n    tags = {\n      Environment = \"Production\"\n      Owner       = \"team-data-platform\"\n      Project     = \"DataLake-v2\"\n      CostCenter  = \"CC-8421\"\n      ManagedBy   = \"Terraform\"\n    }\n  }\n}\n```",
        "verification_commands": "```bash\n# Quét tìm các tài nguyên không có thẻ Owner trong tài khoản AWS\naws resourcegroupstaggingapi get-resources --tag-filters Key=Owner,Values=[]\n```",
        "anti_patterns": "- Cho phép lập trình viên tạo tài nguyên tùy tiện trên console web mà không có thẻ.\n- Đặt giá trị thẻ là tên một cá nhân cụ thể (người đó nghỉ việc thì tài nguyên vô chủ; phải dùng tên Team hoặc Mail Group).",
        "quality_gates": "- 98% tài nguyên trên toàn bộ các tài khoản Cloud có đầy đủ 4 thẻ bắt buộc.\n- 0 tài nguyên mới nào được tạo qua CI/CD nếu thiếu thẻ bắt buộc.",
        "security_constraints": "- Giá trị của các tag không được chứa thông tin bí mật hay dữ liệu PII.",
        "expected_outputs": "- Tài liệu quy chuẩn Tagging Taxonomy chính thức.\n- File cấu hình AWS Tag Policy và dashboard phân tích chi phí FinOps.",
        "related_skills": "dex-cloud-iam-policy-review, dex-cloud-network-design, dex-platform-service-catalog",
        "realistic_usage": "Một công ty công nghệ có hóa đơn AWS đạt $150,000/tháng nhưng ban giám đốc không thể bóc tách chi phí của từng sản phẩm. Sau khi áp dụng chuẩn Tagging tự động qua Terraform default_tags kết hợp AWS Cost Categories, họ bóc tách chính xác chi phí từng team đến từng cent và phát hiện 15 cụm test bị bỏ quên tốn $22,000/tháng, dọn dẹp tiết kiệm ngay lập tức."
    },

    # 151. dex-typescript-type-safety
    "dex-typescript-type-safety": {
        "desc": "Architect strict, bulletproof TypeScript systems leveraging branded types, template literals, conditional types, and runtime schema boundaries (Zod) without resorting to 'any'. Use when building high-integrity TypeScript codebases.",
        "purpose": "Thiết kế, xây dựng và nâng cao tính an toàn kiểu dữ liệu trong TypeScript (Type Safety); khai thác triệt để các tính năng nâng cao (Branded/Nominal Types, Template Literal Types, Conditional Types, Discriminated Unions) kết hợp với các bộ kiểm tra ranh giới runtime (Zod/Valibot), loại bỏ hoàn toàn việc lạm dụng kiểu `any` và ép kiểu không an toàn (`as`).",
        "activation": "- Codebase TypeScript tràn ngập kiểu `any`, `unknown` hoặc ép kiểu bừa bãi `as unknown as Type`.\n- Xảy ra lỗi runtime `TypeError: Cannot read property of undefined` dù code đã compile thành công.\n- Cần bảo đảm tính toàn vẹn của dữ liệu nhận được từ bên ngoài (API, Database, User Input).",
        "when_not_to_use": "- Không thiết kế hệ thống kiểu quá phức tạp đến mức làm tê liệt trình biên dịch TypeScript (Type instantiation is excessively deep).\n- Không dùng TypeScript type checker để thay thế cho việc xác thực dữ liệu khi runtime.",
        "inputs": "- File cấu hình `tsconfig.json` của dự án.\n- Lược đồ dữ liệu nghiệp vụ và các interface hiện có.\n- Thư viện xác thực runtime (Zod, Valibot, Typia).",
        "preconditions": "- `tsconfig.json` đã bật cờ `\"strict\": true` và `\"noImplicitAny\": true`.",
        "core_concepts": "- Branded Types (Nominal Typing): Phân biệt hai chuỗi ký tự có kiểu dữ liệu khác nhau về mặt ngữ nghĩa (ví dụ: `UserId` không thể vô tình gán nhầm cho `OrderId`).\n- Parse, Don't Validate: Thay vì kiểm tra xem dữ liệu có đúng không, hãy parse dữ liệu từ nguồn không tin cậy thành một kiểu dữ liệu có cấu trúc an toàn thông qua Zod.\n- Discriminated Unions: Mẫu hình chuẩn mực để mô hình hóa trạng thái (Loading, Success, Error) giúp trình biên dịch tự động thu hẹp kiểu (Type Narrowing) chính xác 100%.",
        "decision_rules": "- Tuyệt đối cấm sử dụng từ khóa `any` trong toàn bộ codebase; sử dụng `unknown` nếu chưa rõ kiểu và bắt buộc phải narrow kiểu trước khi dùng.\n- Mọi dữ liệu đi vào từ network (API response, request body) bắt buộc phải qua Zod schema parse.",
        "failure_scenarios": "- Sử dụng ép kiểu mù quáng `const user = res.data as User;`, khi backend đổi API trả về null thì ứng dụng bị crash ngay khi truy cập `user.id`.",
        "workflow": "1. Bật toàn bộ các chế độ kiểm tra nghiêm ngặt trong `tsconfig.json` (`strict`, `noUncheckedIndexedAccess`).\n2. Cấu hình ESLint rule cấm `any` (`@typescript-eslint/no-explicit-any: error`).\n3. Áp dụng Branded Types cho các định danh ID cốt lõi.\n4. Xây dựng Zod schemas cho toàn bộ các điểm giao tiếp API bên ngoài.\n5. Chạy TypeScript type-checker trong CI để đảm bảo không có bất kỳ lỗi biên dịch nào.",
        "example": "```typescript\nimport { z } from 'zod';\n\n// 1. Branded Type cho UserId chống gán nhầm lẫn\ntype UserId = string & { readonly __brand: unique symbol };\n\n// 2. Runtime Schema với Zod\nconst UserSchema = z.object({\n  id: z.string().transform((val) => val as UserId),\n  email: z.string().email(),\n  role: z.enum(['ADMIN', 'USER']),\n});\n\ntype User = z.infer<typeof UserSchema>;\n\n// 3. Hàm xử lý an toàn: Parse, Don't Validate\nexport function parseUserData(input: unknown): User {\n  return UserSchema.parse(input); // Ném lỗi nếu sai cấu trúc ngay lập tức\n}\n```",
        "verification_commands": "```bash\n# Kiểm tra toàn bộ lỗi kiểu dữ liệu nghiêm ngặt trong dự án\nnpx tsc --noEmit\n```",
        "anti_patterns": "- Dùng toán tử ép kiểu không an toàn `!` (Non-null assertion operator) để qua mặt compiler thay vì kiểm tra null rõ ràng.\n- Viết generic types lồng nhau quá 5 tầng khiến lập trình viên khác không thể đọc hiểu.",
        "quality_gates": "- 0 lỗi biên dịch `tsc --noEmit` và 0 từ khóa `any` xuất hiện trong mã nguồn mới.\n- 100% API responses từ bên thứ ba đều được bảo vệ bằng runtime schema parser.",
        "security_constraints": "- Ngăn chặn lỗ hổng Prototype Pollution bằng cách lọc bỏ các thuộc tính không mong muốn qua `z.object().strip()`.",
        "expected_outputs": "- Cấu hình `tsconfig.json` tối ưu độ an toàn.\n- Bộ modules Zod schemas và Branded types chuẩn mực.",
        "related_skills": "dex-nodejs-runtime-diagnostics, dex-frontend-architecture, dex-api-contract-testing",
        "realistic_usage": "Một công ty fintech thường xuyên bị lỗi chuyển tiền nhầm tài khoản do lập trình viên truyền nhầm tham số hàm `transfer(targetAccountId, sourceAccountId)` vì cả hai đều là kiểu `string`. Sau khi chuyển sang dùng Branded Types `SourceAccountId` và `TargetAccountId`, trình biên dịch TypeScript đã tự động bắt lỗi ngay khi gán nhầm, loại bỏ hoàn toàn các lỗi sai sót nghiêm trọng."
    },

    # 152. dex-nodejs-runtime-diagnostics
    "dex-nodejs-runtime-diagnostics": {
        "desc": "Diagnose and resolve Node.js event-loop delays, memory leaks, unhandled promise rejections, and async context tracking using Clinic.js, V8 heap snapshots, and perf_hooks. Use when Node.js services degrade under load.",
        "purpose": "Chẩn đoán, phân tích và xử lý các vấn đề hiệu năng chuyên sâu trong môi trường Node.js Runtime (Event Loop Delays, Memory Leaks, Unhandled Promise Rejections, GC Pauses); sử dụng các công cụ chuyên dụng (Clinic.js, Chrome DevTools Heap Snapshots, `perf_hooks`, `async_hooks`) để tối ưu hóa khả năng chịu tải và độ ổn định của ứng dụng.",
        "activation": "- Dịch vụ Node.js bị tăng đột biến độ trễ P99 dù CPU chỉ mới dùng 40%.\n- Bộ nhớ RAM của tiến trình Node.js tăng dần theo thời gian và sập do `JavaScript heap out of memory`.\n- Xuất hiện cảnh báo `UnhandledPromiseRejection` làm tiến trình bị crash đột ngột.",
        "when_not_to_use": "- Không thực hiện profiling trực tiếp trên container production đang phục vụ khách hàng mà không giới hạn thời gian (gây suy giảm 20-30% hiệu năng).\n- Không dùng Node.js cho các tác vụ tính toán CPU-intensive kéo dài trong luồng chính (hãy dùng Worker Threads hoặc tách service riêng).",
        "inputs": "- File heap snapshot (`.heapsnapshot`) hoặc CPU profile (`.cpuprofile`).\n- Thông số Event Loop Delay từ Prometheus/OpenTelemetry.\n- Mã nguồn nghi ngờ gây nghẽn luồng bất đồng bộ.",
        "preconditions": "- Ứng dụng Node.js có thể khởi động với cờ `--inspect` hoặc tích hợp agent thu thập metrics.",
        "core_concepts": "- Event Loop Lag: Nếu một tác vụ đồng bộ chạy mất 100ms trên main thread (ví dụ: `JSON.parse` file 50MB, regex catastrophic backtracking), mọi kết nối khác đều bị đóng băng trong 100ms đó.\n- Memory Leak Causes trong Node.js: Biến toàn cục (Global variables), Closures giữ tham chiếu tới object lớn, Quên hủy Event Listeners (`EventEmitter.on` không có `removeListener`), Cache in-memory không có TTL/LRU eviction.\n- AsyncLocalStorage: Truy vết ngữ cảnh request (Trace ID, User Context) xuyên suốt các lời gọi async mà không phải truyền param thủ công.",
        "decision_rules": "- Nếu Event Loop Lag vượt quá 20ms: kích hoạt cảnh báo vàng; nếu > 100ms: kích hoạt cảnh báo đỏ.\n- Luôn bật cờ `--unhandled-rejections=strict` để phát hiện và xử lý triệt để các Promise lỗi.",
        "failure_scenarios": "- Lập trình viên sử dụng mảng tĩnh trong module scope để lưu log tạm, làm mảng phình to vô hạn và gây OOM crash sau 3 ngày chạy.",
        "workflow": "1. Cấu hình thu thập chỉ số Event Loop Delay bằng `perf_hooks.monitorEventLoopDelay()`.\n2. Chạy ứng dụng dưới tải giả lập kết hợp công cụ `clinic doctor` hoặc `clinic flame`.\n3. Nếu phát hiện rò rỉ bộ nhớ: chụp 2 bản Heap Snapshot (Snapshot 1 lúc bắt đầu tải, Snapshot 2 sau 10,000 requests) và dùng so sánh (Comparison view) trong Chrome DevTools để tìm object rò rỉ.\n4. Tối ưu hóa các đoạn code đồng bộ chặn main thread hoặc thay thế in-memory cache bằng Redis/LRU cache có giới hạn.\n5. Xác minh lại bằng bài kiểm thử tải ngâm (Soak test).",
        "example": "```javascript\n// Giám sát Event Loop Delay chuyên sâu bằng perf_hooks\nconst { monitorEventLoopDelay } = require('perf_hooks');\n\nconst h = monitorEventLoopDelay({ resolution: 20 });\nh.enable();\n\nsetInterval(() => {\n  const p99 = h.percentile(99) / 1e6; // Chuyển nanoseconds sang milliseconds\n  console.log(`Node.js Event Loop P99 Delay: ${p99.toFixed(2)}ms`);\n  if (p99 > 50) {\n    console.warn('CẢNH BÁO: Event loop đang bị chặn bởi tác vụ đồng bộ!');\n  }\n  h.reset();\n}, 5000);\n```",
        "verification_commands": "```bash\n# Phân tích hiệu năng chuyên sâu Node.js bằng Clinic.js Flamegraph\nnpx clinic flame -- node server.js\n```",
        "anti_patterns": "- Sử dụng các hàm đồng bộ chặn luồng (`fs.readFileSync`, `crypto.pbkdf2Sync`) trong request handler.\n- Lạm dụng `JSON.stringify` trên các đối tượng dữ liệu khổng lồ trong luồng chính.",
        "quality_gates": "- Event Loop Delay P99 phải duy trì dưới 10ms dưới điều kiện tải thiết kế.\n- 0 rò rỉ bộ nhớ được ghi nhận trong bài kiểm thử ngâm tải 6 tiếng liên tục.",
        "security_constraints": "- Cổng debug `--inspect` tuyệt đối không được mở ra ngoài mạng công cộng (chỉ bind vào `127.0.0.1` và truy cập qua SSH tunnel).",
        "expected_outputs": "- Báo cáo phân tích Clinic.js HTML Flamegraph.\n- Bản vá khắc phục triệt để lỗi rò rỉ bộ nhớ hoặc chặn Event Loop.",
        "related_skills": "dex-typescript-type-safety, dex-load-and-stress-testing, dex-performance-profiling",
        "realistic_usage": "Một API Gateway viết bằng Express.js cứ sau 48 giờ chạy lại bị khởi động lại do hết bộ nhớ. Sử dụng Chrome DevTools so sánh Heap Snapshots, kỹ sư phát hiện mỗi request đều đăng ký một listener mới vào một EventEmitter chung mà không bao giờ gỡ bỏ. Sau khi sửa lỗi rò rỉ listener, bộ nhớ ổn định ở mức 120MB phẳng suốt nhiều tháng."
    },

    # 153. dex-python-project-engineering
    "dex-python-project-engineering": {
        "desc": "Standardize production-grade Python projects using modern packaging (Poetry, Hatch, uv), strict type checking (Mypy, Pyright), linting (Ruff), and virtual environment isolation. Use to eradicate dependency hell and project fragmentation.",
        "purpose": "Thiết kế, chuẩn hóa và tối ưu hóa quy trình kỹ thuật cho các dự án Python hiện đại (Production-grade Python Engineering); áp dụng công cụ quản lý gói thế hệ mới (`uv`, Poetry, Hatch), kiểm tra kiểu tĩnh nghiêm ngặt (Mypy, Pyright), linter siêu tốc (Ruff), quản lý môi trường ảo cô lập và thiết lập cấu hình `pyproject.toml` đạt chuẩn PEP.",
        "activation": "- Dự án Python gặp vấn đề 'dependency hell', xung đột phiên bản gói hoặc cài đặt thư viện quá chậm chạp trong CI.\n- Codebase thiếu kiểm soát kiểu dữ liệu, liên tục phát sinh lỗi `AttributeError: 'NoneType' object has no attribute`.\n- Các công cụ format và lint (Flake8, Black, Isort) chạy chậm và xung đột lẫn nhau.",
        "when_not_to_use": "- Không sử dụng các file `requirements.txt` không khóa phiên bản (unpinned) cho các ứng dụng production.\n- Không tự tiện cài đặt thư viện trực tiếp vào môi trường Python toàn cục của hệ điều hành mà không có virtual environment.",
        "inputs": "- File cấu hình dự án (`pyproject.toml`).\n- Danh sách dependencies và dev-dependencies.\n- Cấu hình type checker và linter.",
        "preconditions": "- Đã cài đặt công cụ quản lý gói hiện đại (`uv` hoặc `poetry`) trên máy phát triển.",
        "core_concepts": "- `pyproject.toml` as the Standard: Toàn bộ cấu hình công cụ (Ruff, Mypy, Pytest, Coverage) và metadata của gói được tập trung vào một file duy nhất theo chuẩn PEP 517/518/621.\n- Fast Tooling with `uv` & `Ruff`: `uv` nhanh hơn pip 10-100 lần nhờ viết bằng Rust; `Ruff` thay thế hoàn toàn Black, Flake8, Isort với tốc độ xử lý hàng trăm ngàn dòng code trong chớp mắt.\n- Strict Static Typing: Mypy với cờ `--strict` biến Python thành ngôn ngữ có độ tin cậy kiểu gần như các ngôn ngữ tĩnh.",
        "decision_rules": "- Bắt buộc cam kết file khóa phiên bản (`uv.lock` hoặc `poetry.lock`) vào Git để bảo đảm tính tái lập 100% của môi trường.\n- Mọi hàm mới viết phải có đầy đủ Type Hints cho các tham số và giá trị trả về.",
        "failure_scenarios": "- Một thư viện phụ thuộc cập nhật phiên bản minor nhưng làm thay đổi API ngầm, khiến ứng dụng sập trên production do dùng `requirements.txt` không khóa phiên bản chính xác.",
        "workflow": "1. Khởi tạo dự án chuẩn hóa bằng `uv init` và định cấu hình `pyproject.toml`.\n2. Thiết lập cấu hình Ruff để vừa format code vừa kiểm tra quy chuẩn an ninh.\n3. Cấu hình Mypy ở chế độ nghiêm ngặt (`disallow_untyped_defs = true`).\n4. Tích hợp pre-commit hooks để tự động chạy Ruff và Mypy trước khi cho phép commit.\n5. Tối ưu hóa Dockerfile đa tầng sử dụng `uv` để tạo container image siêu nhẹ và build trong vài giây.",
        "example": "```toml\n# pyproject.toml chuẩn mực cho dự án Python hiện đại\n[project]\nname = \"enterprise-ai-service\"\nversion = \"5.0.0\"\nrequires-python = \">=3.11\"\ndependencies = [\n    \"fastapi>=0.110.0\",\n    \"pydantic>=2.6.0\",\n]\n\n[tool.ruff]\nline-length = 88\ntarget-version = \"py311\"\nselect = [\"E\", \"F\", \"I\", \"B\", \"UP\", \"S\"] # Chặn cả lỗi cú pháp và lỗ hổng bảo mật\n\n[tool.mypy]\npython_version = \"3.11\"\nstrict = true\ndisallow_untyped_defs = true\nignore_missing_imports = true\n```",
        "verification_commands": "```bash\n# Chạy linter và format siêu tốc bằng Ruff\nuv run ruff check . --fix\n# Kiểm tra kiểu dữ liệu tĩnh nghiêm ngặt bằng Mypy\nuv run mypy src/\n```",
        "anti_patterns": "- Sử dụng `from module import *` làm ô nhiễm namespace và vô hiệu hóa công cụ kiểm tra kiểu tĩnh.\n- Bắt ngoại lệ chung chung `except Exception: pass` làm nuốt chửng các lỗi nghiêm trọng.",
        "quality_gates": "- 100% mã nguồn vượt qua kiểm tra `mypy --strict` và `ruff check` không có lỗi.\n- Quá trình cài đặt dependencies trong CI phải hoàn thành dưới 15 giây nhờ `uv`.",
        "security_constraints": "- Kiểm tra lỗ hổng bảo mật trong dependencies bằng `uv run pip-audit` trước khi release.",
        "expected_outputs": "- File `pyproject.toml` và `uv.lock` chuẩn hóa.\n- Cấu hình Pre-commit hooks và Dockerfile tối ưu hóa tốc độ build.",
        "related_skills": "dex-unit-testing, dex-compatibility-matrix-testing, dex-ci-pipeline-optimization",
        "realistic_usage": "Một đội ngũ Data Science gặp rắc rối vì code Python chạy trên máy của từng người cho kết quả khác nhau và build CI mất 8 phút. Chuyên gia chuyển đổi sang sử dụng `uv` và `pyproject.toml` chuẩn hóa kèm Ruff và Mypy. Thời gian build CI giảm từ 8 phút xuống còn 18 giây, và 100% các xung đột thư viện đã được loại bỏ hoàn toàn."
    },

    # 154. dex-rust-unsafe-audit
    "dex-rust-unsafe-audit": {
        "desc": "Audit, verify, and minimize 'unsafe' code blocks in Rust, validating ownership invariants, raw pointer arithmetic, FFI boundaries, and undefined behavior using Miri and Loom. Use when building high-assurance systems.",
        "purpose": "Kiểm toán, thẩm định và tối thiểu hóa các khối mã nguồn không an toàn (`unsafe`) trong Rust; xác minh các bất biến về quyền sở hữu (Ownership Invariants), số học con trỏ thô (Raw Pointers), ranh giới FFI và triệt tiêu các hành vi không xác định (Undefined Behavior - UB) bằng các công cụ chuyên sâu như Miri và Loom.",
        "activation": "- Viết hoặc review các thư viện cốt lõi (Crates) có chứa từ khóa `unsafe`.\n- Xây dựng các cấu trúc dữ liệu tùy chỉnh hiệu năng cao (Lock-free data structures, Ring buffers).\n- Tích hợp giao tiếp FFI với các thư viện viết bằng C/C++.",
        "when_not_to_use": "- Không sử dụng `unsafe` nếu bài toán có thể giải quyết được bằng các cấu trúc an toàn có sẵn trong thư viện chuẩn (Safe Rust) với chi phí hiệu năng không đáng kể.\n- Không dùng `unsafe` chỉ để 'lách luật' kiểm tra của Borrow Checker.",
        "inputs": "- Mã nguồn Rust chứa các khối `unsafe`.\n- Tài liệu đặc tả các điều kiện bất biến an toàn (Safety Invariants) của hàm.\n- Bộ test cases kiểm thử các trường hợp biên.",
        "preconditions": "- Đã cài đặt Rust Nightly toolchain để chạy trình thông dịch Miri (`cargo miri`).",
        "core_concepts": "- Soundness vs Safety: Một hàm `unsafe fn` yêu cầu người gọi phải tự đảm bảo an toàn. Một hàm safe bọc ngoài unsafe code (Safe Abstraction) phải là 'sound' — nghĩa là bất kể tham số đầu vào là gì cũng không bao giờ kích hoạt Undefined Behavior.\n- Undefined Behavior (UB) trong Rust: Vi phạm quy tắc Aliasing (hai con trỏ cùng trỏ tới một vùng nhớ và ít nhất một con trỏ có quyền ghi `&mut`), Đọc bộ nhớ chưa khởi tạo, Dereference con trỏ null hoặc dangling.\n- Miri: Công cụ thông dịch mã trung gian (MIR) của Rust, có khả năng phát hiện 100% các lỗi vi phạm quy tắc aliasing (Stacked Borrows / Tree Borrows) khi runtime.",
        "decision_rules": "- Mọi khối `unsafe` bắt buộc phải có chú thích `// SAFETY:` giải thích chi tiết lý do tại sao đoạn code này không vi phạm bất biến an toàn.\n- Giới hạn phạm vi của khối `unsafe` ở mức tối thiểu (chỉ bọc đúng 1-2 dòng cần thiết).",
        "failure_scenarios": "- Tạo một tham chiếu khả biến `&mut T` từ một con trỏ thô trong khi một tham chiếu bất biến `&T` khác vẫn đang tồn tại, vi phạm quy tắc aliasing và bị compiler tối ưu hóa sai.",
        "workflow": "1. Quét tìm toàn bộ các vị trí sử dụng `unsafe` bằng công cụ `cargo geiger`.\n2. Rà soát từng khối `unsafe`, kiểm tra xem có thể thay thế bằng safe code không.\n3. Thêm tài liệu `// SAFETY:` bắt buộc cho từng khối.\n4. Thực thi test suite dưới trình kiểm tra Undefined Behavior của Miri.\n5. Kiểm tra các điều kiện Race condition đa luồng bằng thư viện Loom.",
        "example": "```rust\npub struct BoundedBuffer<T> {\n    ptr: *mut T,\n    capacity: usize,\n}\n\nimpl<T> BoundedBuffer<T> {\n    pub fn read_at(&self, index: usize) -> Option<&T> {\n        if index >= self.capacity {\n            return None;\n        }\n        // SAFETY: Chúng ta đã kiểm tra index < capacity,\n        // con trỏ đã được cấp phát hợp lệ và không có luồng nào đang ghi vào index này.\n        unsafe {\n            Some(&*self.ptr.add(index))\n        }\n    }\n}\n```",
        "verification_commands": "```bash\n# Kiểm tra Undefined Behavior bằng Miri trong môi trường Rust Nightly\ncargo +nightly miri test\n# Quét thống kê tỉ lệ unsafe code trong project\ncargo geiger\n```",
        "anti_patterns": "- Viết `unsafe` mà không có comment `// SAFETY:` giải thích căn cứ kỹ thuật.\n- Ép kiểu con trỏ tùy tiện làm sai lệch memory alignment của kiểu dữ liệu.",
        "quality_gates": "- 100% test cases phải PASS hoàn toàn dưới `cargo miri test` mà không có cảnh báo UB nào.\n- 0 khối unsafe nào không có phần giải trình `// SAFETY:`.",
        "security_constraints": "- Mọi hàm expose ra ngoài public API bắt buộc phải là Safe Function hoặc được đánh dấu rõ ràng `pub unsafe fn`.",
        "expected_outputs": "- Báo cáo kiểm toán `cargo geiger`.\n- Mã nguồn Rust đã được thẩm định an toàn kèm chú thích `// SAFETY:` chuẩn chỉ.",
        "related_skills": "dex-cpp-memory-safety, dex-ffi-boundary-contracts, dex-reproducible-benchmarking",
        "realistic_usage": "Một công ty blockchain viết cấu trúc lưu trữ trạng thái bằng Rust dùng unsafe pointer để tối ưu tốc độ. Khi chạy dưới `cargo miri test`, họ bàng hoàng phát hiện hàm giải phóng bộ nhớ vi phạm quy tắc Stacked Borrows làm phát sinh Undefined Behavior tiềm ẩn. Họ đã tái cấu trúc lại an toàn bằng `std::mem::ManuallyDrop` và bảo vệ thành công tài sản người dùng."
    },

    # 155. dex-cpp-memory-safety
    "dex-cpp-memory-safety": {
        "desc": "Detect, eliminate, and prevent memory safety bugs in modern C++ (C++17/20) using AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), smart pointers, and RAII principles. Use when auditing legacy C++ or writing high-performance native engines.",
        "purpose": "Phát hiện, loại bỏ và ngăn ngừa các lỗ hổng an toàn bộ nhớ trong C++ hiện đại (Modern C++17/20); chuyển đổi sang mô hình RAII (Resource Acquisition Is Initialization), sử dụng con trỏ thông minh (`std::unique_ptr`, `std::shared_ptr`), và khai thác triệt để các bộ kiểm tra động (AddressSanitizer, MemorySanitizer, UndefinedBehaviorSanitizer) nhằm triệt tiêu các lỗi Use-After-Free, Buffer Overflow và Memory Leaks.",
        "activation": "- C++ codebase gặp hiện tượng crash ngẫu nhiên với lỗi `Segmentation fault (core dumped)`.\n- Phát hiện lỗ hổng bảo mật nghiêm trọng liên quan đến tràn bộ đệm (Buffer Overflow) hoặc Use-After-Free.\n- Hiện đại hóa mã nguồn C++ legacy cũ (C++98/03) sang chuẩn C++20 an toàn.",
        "when_not_to_use": "- Không tự quản lý bộ nhớ thủ công bằng `malloc/free` hoặc `new/delete` trong mã nguồn C++ hiện đại.\n- Không bật Sanitizers trong binary release production vì làm giảm hiệu năng thực thi.",
        "inputs": "- Mã nguồn C/C++ cần kiểm tra.\n- File cấu hình build (CMakeLists.txt, Makefile).\n- Bộ dữ liệu kiểm thử tải và fuzzer inputs.",
        "preconditions": "- Trình biên dịch hiện đại (Clang 14+ hoặc GCC 11+) có hỗ trợ đầy đủ các cờ Sanitizer.",
        "core_concepts": "- RAII & Smart Pointers: Mọi tài nguyên (bộ nhớ, file descriptor, mutex) phải được quản lý bởi một đối tượng trên Stack có destructor tự động thu dọn khi rời khỏi phạm vi (scope).\n- Memory Bugs phổ biến:\n  + Use-After-Free (UAF): Truy cập vào vùng nhớ sau khi đã bị giải phóng.\n  + Out-of-Bounds Access: Đọc/ghi ngoài giới hạn mảng.\n  + Memory Leak: Cấp phát bộ nhớ nhưng đánh mất con trỏ trỏ tới nó.\n- Sanitizers: ASan (bắt lỗi bộ nhớ), UBSan (bắt lỗi tràn số nguyên, null pointer dereference), TSan (bắt data race đa luồng).",
        "decision_rules": "- Tuyệt đối cấm sử dụng raw owning pointers (`T*` với `new`); luôn dùng `std::unique_ptr<T>` cho quyền sở hữu độc quyền.\n- Mọi commit mã nguồn C++ trong CI bắt buộc phải chạy qua test suite được compile với cờ ASan và UBSan.",
        "failure_scenarios": "- Trả về một tham chiếu (`return &localVar;`) trỏ tới một biến cục bộ trên Stack đã bị hủy sau khi hàm kết thúc.",
        "workflow": "1. Cấu hình CMake kích hoạt các cờ AddressSanitizer và UndefinedBehaviorSanitizer.\n2. Chạy toàn bộ test suite hiện có dưới trình biên dịch Clang/ASan để phát hiện lỗi ẩn.\n3. Thay thế các con trỏ thô bằng `std::unique_ptr` và `std::span` (thay thế mảng C-style).\n4. Rà soát việc khởi tạo biến để đảm bảo 100% biến được gán giá trị mặc định.\n5. Tích hợp Clang-Tidy static analysis để cưỡng chế các quy tắc C++ Core Guidelines.",
        "example": "```cmake\n# Cấu hình CMake kích hoạt Sanitizers trong chế độ Debug\nset(CMAKE_CXX_FLAGS_DEBUG \"${CMAKE_CXX_FLAGS_DEBUG} -fsanitize=address,undefined -fno-omit-frame-pointer -g\")\nset(CMAKE_LINKER_FLAGS_DEBUG \"${CMAKE_LINKER_FLAGS_DEBUG} -fsanitize=address,undefined\")\n```\n\n```cpp\n// Chuyển đổi mã nguồn C++ an toàn với RAII và smart pointers\n#include <memory>\n#include <span>\n#include <vector>\n\nclass SecurePacketProcessor {\npublic:\n    // Sử dụng std::span thay vì con trỏ thô kèm độ dài (Raw pointer + size)\n    void process(std::span<const uint8_t> packetData) {\n        if (packetData.empty()) return;\n        // Tự động giải phóng bộ nhớ khi ra khỏi hàm\n        auto buffer = std::make_unique<std::vector<uint8_t>>(packetData.begin(), packetData.end());\n        parseHeader(*buffer);\n    }\n};\n```",
        "verification_commands": "```bash\n# Build và chạy kiểm thử với Clang AddressSanitizer\ncmake -B build -DCMAKE_BUILD_TYPE=Debug\ncmake --build build\n./build/bin/run_tests\n```",
        "anti_patterns": "- Ép kiểu con trỏ bừa bãi bằng `reinterpret_cast` mà không kiểm tra quy tắc Strict Aliasing.\n- Sử dụng mảng tĩnh C-style `char buffer[256]` kết hợp với các hàm nguy hiểm như `strcpy` hoặc `sprintf`.",
        "quality_gates": "- 0 lỗi memory leak hoặc out-of-bounds nào được báo cáo bởi ASan/UBSan trên 100% test cases.\n- Vượt qua kiểm tra của Clang-Tidy với bộ quy tắc C++ Core Guidelines.",
        "security_constraints": "- Kích hoạt cờ bảo vệ Stack-Smashing (`-fstack-protector-strong`) và Control-Flow Integrity (CFI) trong bản release.",
        "expected_outputs": "- File CMakeLists.txt tích hợp Sanitizers và Clang-Tidy.\n- Báo cáo kết quả kiểm tra ASan sạch sẽ và mã nguồn C++ đã hiện đại hóa.",
        "related_skills": "dex-rust-unsafe-audit, dex-ffi-boundary-contracts, dex-reproducible-benchmarking",
        "realistic_usage": "Một engine render đồ họa 3D bị sập bất thình lình khi người dùng mở các file mô hình phức tạp. Bằng cách kích hoạt Clang AddressSanitizer trong CI, nhóm kỹ sư phát hiện ngay lập tức một lỗi Use-After-Free trong cây phân nhánh vật liệu khi đối tượng con tham chiếu tới đối tượng cha đã bị hủy. Chuyển đổi sang `std::weak_ptr` đã giải quyết dứt điểm lỗi crash."
    },

    # 156. dex-go-concurrency-patterns
    "dex-go-concurrency-patterns": {
        "desc": "Architect, synchronize, and debug high-throughput Go concurrent systems using channels, worker pools, sync.Pool, Context propagation, and race detection. Use when building scalable backend services in Golang.",
        "purpose": "Thiết kế, đồng bộ hóa và xử lý sự cố các hệ thống xử lý đồng thời hiệu năng cao trong Go (Golang Concurrency); áp dụng mô hình Worker Pools, Pipeline Channels, `sync.Pool`, truyền tải tín hiệu hủy qua `context.Context`, và triệt tiêu các lỗi Data Races, Goroutine Leaks và Deadlocks bằng công cụ Go Race Detector.",
        "activation": "- Dịch vụ Go bị rò rỉ bộ nhớ do số lượng Goroutines tăng vọt liên tục không giảm (Goroutine Leak).\n- Xuất hiện cảnh báo nguy hiểm `DATA RACE` khi chạy kiểm thử hoặc biên dịch với cờ `-race`.\n- Cần tối ưu hóa thông lượng xử lý hàng ngàn tác vụ nền song song mà không làm sập cơ sở dữ liệu.",
        "when_not_to_use": "- Không lạm dụng Goroutine cho các tác vụ tính toán siêu nhỏ in-memory (chi phí context switch của scheduler có thể lớn hơn thời gian chạy).\n- Không chia sẻ bộ nhớ chung mà không có cơ chế khóa bảo vệ (Mutex) hoặc truyền tin (Channel).",
        "inputs": "- Mã nguồn Go có sử dụng từ khóa `go`, channels hoặc các cấu trúc gói `sync`.\n- Số lượng tác vụ đồng thời mục tiêu (Concurrency limit).\n- Yêu cầu về thời gian timeout và hủy bỏ tác vụ.",
        "preconditions": "- Cài đặt Go toolchain phiên bản mới nhất (Go 1.21+).",
        "core_concepts": "- Share Memory by Communicating: 'Đừng giao tiếp bằng cách chia sẻ bộ nhớ; hãy chia sẻ bộ nhớ bằng cách giao tiếp' qua Channels.\n- Goroutine Leak: Một goroutine bị block vĩnh viễn do chờ đọc/ghi vào một channel không có ai nhận hoặc thiếu tín hiệu hủy từ Context.\n- `context.Context` Propagation: Mọi hàm thực hiện I/O hoặc đồng thời bắt buộc phải nhận `ctx context.Context` làm tham số đầu tiên để tôn trọng tín hiệu hủy bỏ hoặc timeout từ client.",
        "decision_rules": "- Bắt buộc kiểm tra `select` với trường hợp `case <-ctx.Done():` trong mọi vòng lặp chờ của goroutine.\n- Luôn chạy toàn bộ unit và integration tests với cờ `-race` trong CI pipeline.",
        "failure_scenarios": "- Gửi dữ liệu vào một unbuffered channel mà không có goroutine nào lắng nghe, khiến goroutine phát tin bị treo vĩnh viễn.",
        "workflow": "1. Thiết kế mô hình đồng thời: xác định luồng producer, worker pool và consumer.\n2. Cấu hình kích thước bounded worker pool để kiểm soát số lượng goroutine đồng thời.\n3. Truyền `context.Context` xuyên suốt các tầng xử lý.\n4. Sử dụng `sync.WaitGroup` hoặc `errgroup.Group` để thu thập kết quả và xử lý lỗi đồng bộ.\n5. Chạy kiểm thử tự động với cờ race detector `go test -race ./...`.",
        "example": "```go\n// Mô hình Worker Pool an toàn kèm Context Cancellation trong Go\npackage workerpool\n\nimport (\n\t\"context\"\n\t\"golang.org/x/sync/errgroup\"\n)\n\nfunc ProcessJobs(ctx context.Context, jobs []string, concurrency int) error {\n\tg, ctx := errgroup.WithContext(ctx)\n\tjobChan := make(chan string)\n\n\t// Khởi tạo các workers\n\tfor i := 0; i < concurrency; i++ {\n\t\tg.Go(func() error {\n\t\t\tfor {\n\t\t\t\tselect {\n\t\t\t\tcase <-ctx.Done():\n\t\t\t\t\treturn ctx.Err()\n\t\t\t\tcase job, ok := <-jobChan:\n\t\t\t\t\tif !ok {\n\t\t\t\t\t\treturn nil\n\t\t\t\t\t}\n\t\t\t\t\tif err := executeJob(ctx, job); err != nil {\n\t\t\t\t\t\treturn err\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t})\n\t}\n\n\t// Đẩy công việc vào channel\n\tg.Go(func() error {\n\t\tdefer close(jobChan)\n\t\tfor _, job := range jobs {\n\t\t\tselect {\n\t\t\tcase <-ctx.Done():\n\t\t\t\treturn ctx.Err()\n\t\t\tcase jobChan <- job:\n\t\t\t}\n\t\t}\n\t\treturn nil\n\t})\n\n\treturn g.Wait()\n}\n```",
        "verification_commands": "```bash\n# Chạy kiểm thử với cờ Go Race Detector\ngo test -v -race -count=5 ./...\n```",
        "anti_patterns": "- Bỏ qua lỗi `DATA RACE` và cho rằng 'nó hiếm khi xảy ra ngoài đời'.\n- Đọc/ghi biến map trong Go từ nhiều goroutine cùng lúc mà không có `sync.RWMutex` (kích hoạt panic fatal error của Go runtime).",
        "quality_gates": "- 0 lỗi data race được phát hiện khi chạy toàn bộ test suite với cờ `-race`.\n- Số lượng active goroutines trở về mức cơ sở sau khi hoàn thành đợt xử lý công việc.",
        "security_constraints": "- Ngăn chặn tấn công làm cạn kiệt tài nguyên (Goroutine Exhaustion DoS) bằng cách luôn giới hạn kích thước worker pool.",
        "expected_outputs": "- Package xử lý đồng thời hoàn chỉnh sử dụng `errgroup`.\n- Báo cáo kết quả kiểm thử `-race` sạch sẽ.",
        "related_skills": "dex-traffic-shaping-backpressure, dex-load-and-stress-testing, dex-backend-architecture",
        "realistic_usage": "Một dịch vụ xử lý webhook viết bằng Go bị sập vì số lượng goroutines tăng vọt lên 400,000 khi downstream API bị chậm. Bằng cách tái cấu trúc sang kiến trúc Bounded Worker Pool với kích thước cố định 500 workers kết hợp `errgroup`, dịch vụ giữ mức tiêu thụ RAM ổn định dưới 80MB và xử lý trơn tru hàng triệu webhook mỗi ngày."
    },

    # 157. dex-jvm-performance-diagnostics
    "dex-jvm-performance-diagnostics": {
        "desc": "Diagnose and tune JVM memory, garbage collection pauses (G1GC, ZGC), thread contention, and JIT compilation using JFR, async-profiler, and visualgc. Use when Java/Kotlin applications suffer latency spikes or GC stalls.",
        "purpose": "Chẩn đoán, phân tích và tối ưu hóa hiệu năng chuyên sâu cho các ứng dụng chạy trên Java Virtual Machine (JVM: Java, Kotlin, Scala); phân tích các điểm dừng do dọn rác (GC Pauses), tối ưu bộ thu gom rác thế hệ mới (G1GC, ZGC, Shenandoah), điều tra nghẽn tranh chấp luồng (Thread Contention) và phân tích hành vi của bộ biên dịch JIT thông qua Java Flight Recorder (JFR) và async-profiler.",
        "activation": "- Dịch vụ Java gặp các đợt tăng vọt độ trễ (Latency Spikes P99 > 1s) do các đợt dừng Stop-The-World của bộ Garbage Collector.\n- Ứng dụng ném lỗi `java.lang.OutOfMemoryError: Java heap space` hoặc `Metaspace`.\n- Tỉ lệ chiếm dụng CPU của JVM ở mức 100% nhưng thông lượng xử lý nghiệp vụ không tăng.",
        "when_not_to_use": "- Không tự ý thêm hàng chục cờ JVM tuning (`-XX:...`) phức tạp copy từ internet vào production mà không có dữ liệu đo lường thực nghiệm.\n- Không profiling liên tục với các công cụ instrumentation nặng (như JProfiler/YourKit) trên cụm production đang phục vụ tải đỉnh.",
        "inputs": "- File ghi chép nhật ký bay (`.jfr` file).\n- Garbage Collection logs (`-Xlog:gc*`).\n- JVM Heap Dumps (`.hprof`) khi xảy ra OOM.",
        "preconditions": "- Ứng dụng chạy trên JVM hiện đại (OpenJDK 17 hoặc 21 LTS).",
        "core_concepts": "- Stop-The-World (STW): Khoảng thời gian toàn bộ luồng ứng dụng bị tạm dừng để GC đánh dấu và di dời đối tượng trong bộ nhớ.\n- ZGC (Low-Latency GC): Bộ thu gom rác có khả năng giữ thời gian tạm dừng STW dưới 1ms bất kể kích thước Heap từ 16MB đến 16TB.\n- Allocation Rate vs Promotion Rate: Tốc độ cấp phát đối tượng mới quá nhanh khiến các đối tượng sống ngắn bị đẩy sớm sang Old Generation, kích hoạt Full GC nặng nề.",
        "decision_rules": "- Với các ứng dụng yêu cầu độ trễ cực thấp (P99 < 10ms): kích hoạt ZGC (`-XX:+UseZGC -XX:+ZGenerational`).\n- Bắt buộc bật cờ tự động sinh Heap Dump khi xảy ra OOM (`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/log/`).",
        "failure_scenarios": "- Cấu hình dung lượng Heap quá lớn (`-Xmx32g`) với bộ GC cũ (CMS/Parallel) khiến một đợt Full GC có thể làm đóng băng toàn bộ hệ sinh thái trong 30 giây.",
        "workflow": "1. Bật GC logging tiêu chuẩn trong Java 17+ (`-Xlog:gc*:file=/var/log/gc.log:time,uptime,level,tags:filecount=5,filesize=50m`).\n2. Chạy async-profiler để lấy Flamegraph phân bổ bộ nhớ và CPU mà không gây gián đoạn hệ thống.\n3. Phân tích file GC log bằng công cụ GCeasy hoặc `jclarity`.\n4. Điều chỉnh các thông số Heap Size và chuyển đổi sang Generational ZGC.\n5. Kiểm tra lại sự cải thiện của P99 latency dưới bài kiểm thử tải mô phỏng.",
        "example": "```bash\n# Cấu hình cờ JVM tối ưu cho Java 21 microservices độ trễ thấp\nJAVA_OPTS=\"-Xms4g -Xmx4g \\\n  -XX:+UseZGC \\\n  -XX:+ZGenerational \\\n  -XX:+HeapDumpOnOutOfMemoryError \\\n  -XX:HeapDumpPath=/var/dumps/oom.hprof \\\n  -Xlog:gc*:file=/var/log/gc.log:time,level,tags:filecount=5,filesize=20M \\\n  -Djava.security.egd=file:/dev/./urandom\"\n```",
        "verification_commands": "```bash\n# Chạy async-profiler thu thập CPU flamegraph trong 30 giây\n./async-profiler/bin/asprof -d 30 -f /tmp/flamegraph.html <PID>\n```",
        "anti_patterns": "- Gọi hàm `System.gc()` thủ công trong mã nguồn ứng dụng.\n- Đặt kích thước Heap khởi đầu `-Xms` quá nhỏ so với kích thước tối đa `-Xmx`, khiến JVM liên tục phải xin thêm bộ nhớ từ hệ điều hành.",
        "quality_gates": "- Thời gian tạm dừng GC Pause P99 phải dưới 2ms đối với các microservices tài chính.\n- Không xảy ra bất kỳ đợt Full GC nào trong quá trình vận hành tải bình thường.",
        "security_constraints": "- Bảo vệ file Heap Dump sinh ra vì nó có thể chứa các thông tin nhạy cảm (mật khẩu, khóa giải mã) trong bộ nhớ heap.",
        "expected_outputs": "- File ghi vết JFR / Flamegraph phân tích điểm nghẽn CPU và phân bổ đối tượng.\n- Bộ cờ khởi động JVM tối ưu hóa cho môi trường container Kubernetes.",
        "related_skills": "dex-performance-profiling, dex-load-and-stress-testing, dex-backend-architecture",
        "realistic_usage": "Một hệ thống giao dịch chứng khoán viết bằng Spring Boot bị trễ đột biến 800ms cứ mỗi 15 phút một lần, khiến các lệnh giao dịch bị hủy do timeout. Sử dụng async-profiler và phân tích GC log, kỹ sư phát hiện bộ G1GC bị quá tải do một thư viện mapping tạo ra hàng triệu đối tượng DTO rác mỗi giây. Chuyển sang dùng Java 21 Generational ZGC kết hợp tái cấu trúc object reuse đã đưa thời gian GC pause về mức dưới 0.8ms ổn định tuyệt đối."
    },

    # 158. dex-dotnet-application-engineering
    "dex-dotnet-application-engineering": {
        "desc": "Architect, optimize, and diagnose modern cross-platform .NET (C# / ASP.NET Core) applications leveraging dependency injection lifetimes, async/await mechanics, Span<T>, and dotnet-dump/dotnet-trace. Use when building enterprise .NET systems.",
        "purpose": "Thiết kế, xây dựng và tối ưu hóa ứng dụng .NET hiện đại đa nền tảng (Modern .NET 8/9, C#, ASP.NET Core); quản trị vòng đời Dependency Injection (Transient, Scoped, Singleton), làm chủ cơ chế `async/await` không gây deadlock, khai thác tối đa cấu trúc `Span<T>` / `Memory<T>` không cấp phát bộ nhớ, và điều tra sự cố hiệu năng bằng các công cụ CLI chẩn đoán (`dotnet-dump`, `dotnet-trace`, `dotnet-gcdump`).",
        "activation": "- Dịch vụ ASP.NET Core chạy trên Linux/Kubernetes bị treo (hang) do ThreadPool Starvation hoặc Sync-over-Async.\n- Nâng cấp ứng dụng .NET Framework cũ sang .NET 8 đa nền tảng.\n- Cần tối ưu hóa thông lượng API xử lý dữ liệu lớn yêu cầu Zero-allocation.",
        "when_not_to_use": "- Không sử dụng các phương thức đồng bộ chặn luồng như `.Result` hoặc `.Wait()` trên Task (gây ra Deadlock và ThreadPool Starvation).\n- Không đăng ký service Scoped vào bên trong một service Singleton (Captive Dependency bug).",
        "inputs": "- Mã nguồn C# / Solution `.sln`.\n- File cấu hình `appsettings.json` và cấu hình runtime `runtimeconfig.json`.\n- Bản ghi trace hoặc dump lấy từ môi trường Linux container.",
        "preconditions": "- Đã cài đặt .NET SDK 8.0+ và bộ công cụ chẩn đoán toàn cục `dotnet-dump`, `dotnet-trace`.",
        "core_concepts": "- Captive Dependencies: Lỗi tiêm một Scoped service (như `DbContext`) vào một Singleton service, khiến DbContext không bao giờ được giải phóng và giữ kết nối DB vĩnh viễn.\n- ThreadPool Starvation: Xảy ra khi lập trình viên gọi code đồng bộ chặn luồng (`Task.Wait()`), làm cạn kiệt các luồng xử lý của ThreadPool và làm tê liệt toàn bộ API server.\n- `Span<T>` & Zero-Allocation: Cho phép thao tác cắt chuỗi, đọc byte trực tiếp trên vùng nhớ contiguous mà không cần cấp phát thêm đối tượng mới trên Heap, giảm áp lực cực lớn cho .NET GC.",
        "decision_rules": "- Bật chế độ phân tích Dependency Injection lúc khởi động (`ValidateScopes = true`, `ValidateOnBuild = true`).\n- 100% các thao tác I/O (Database, HTTP, Disk) bắt buộc phải sử dụng API bất đồng bộ kèm `CancellationToken`.",
        "failure_scenarios": "- Lỗi gọi `httpClient.GetAsync().Result` trong controller làm cạn kiệt ThreadPool của ASP.NET Core khi có tải đồng thời lớn.",
        "workflow": "1. Cấu hình kiểm tra tính hợp lệ của DI container trong `Program.cs`.\n2. Rà soát codebase loại bỏ hoàn toàn các anti-pattern Sync-over-Async.\n3. Áp dụng `Span<T>` và `ArrayPool<T>` cho các hàm xử lý parser chuỗi và byte buffer.\n4. Thu thập dữ liệu trace khi có tải bằng `dotnet-trace collect --process-id <PID>`.\n5. Đóng gói container Linux tối giản sử dụng Alpine/Chiseled images.",
        "example": "```csharp\n// Tối ưu hóa ASP.NET Core: Zero-Allocation parsing với ReadOnlySpan<char>\npublic static class DateParserFast\n{\n    public static bool TryParseYear(ReadOnlySpan<char> input, out int year)\n    {\n        // Không sinh ra chuỗi tạm (string allocation) trên Heap\n        if (input.Length >= 4 && int.TryParse(input.Slice(0, 4), out year))\n        {\n            return true;\n        }\n        year = 0;\n        return false;\n    }\n}\n```",
        "verification_commands": "```bash\n# Thu thập heap dump từ tiến trình .NET trên Linux\ndotnet-dump collect -p <PID>\n# Phân tích dump tìm rò rỉ bộ nhớ\ndotnet-dump analyze core_dump.dmp\n```",
        "anti_patterns": "- Gọi `Task.Run()` bừa bãi cho các tác vụ I/O ngắn hạn trong ASP.NET Core.\n- Không truyền `CancellationToken` xuống các câu lệnh truy vấn Entity Framework Core.",
        "quality_gates": "- 0 lỗi Captive Dependency được phát hiện khi khởi động ứng dụng với `ValidateScopes = true`.\n- Vượt qua kiểm thử tải không phát sinh hiện tượng ThreadPool Starvation.",
        "security_constraints": "- Mã hóa dữ liệu Data Protection Keys của ASP.NET Core bằng AWS KMS hoặc Azure Key Vault khi triển khai đa instance.",
        "expected_outputs": "- Solution .NET chuẩn mực kiến trúc Clean Architecture.\n- Báo cáo phân tích hiệu năng và tài liệu cấu hình chẩn đoán production.",
        "related_skills": "dex-backend-architecture, dex-load-and-stress-testing, dex-database-design",
        "realistic_usage": "Một dịch vụ thanh toán ASP.NET Core trên Kubernetes bị timeout hàng loạt mỗi khi traffic đạt 2,000 RPS. Chạy `dotnet-trace`, đội ngũ phát hiện một hàm tiện ích cũ sử dụng `.GetAwaiter().GetResult()` gây nghẽn ThreadPool. Sau khi chuyển hoàn toàn sang `async/await` và áp dụng `Span<char>` để parse mã giao dịch, CPU server giảm 60% và hệ thống đáp ứng 8,000 RPS dễ dàng."
    },

    # 159. dex-webassembly-integration
    "dex-webassembly-integration": {
        "desc": "Compile, integrate, and optimize WebAssembly (WASM) modules across browser and server runtimes (Wasmtime, Wasmer), managing linear memory, FFI boundary overhead, and sandbox security. Use when running near-native compute in web or edge environments.",
        "purpose": "Thiết kế, biên dịch, tích hợp và tối ưu hóa các module WebAssembly (WASM: Rust/C++ sang WebAssembly) trên môi trường trình duyệt web và máy chủ (Wasmtime, Wasmer); quản lý vùng nhớ tuyến tính (Linear Memory), tối ưu hóa chi phí vượt ranh giới giao tiếp (FFI Boundary Overhead), và thiết lập môi trường sandbox an toàn cho phép thực thi mã nguồn tính toán phức tạp.",
        "activation": "- Cần mang các thuật toán tính toán nặng (xử lý đồ họa, nén/giải nén video, mã hóa mật mã học, AI inference cục bộ) chạy mượt mà trên trình duyệt web.\n- Xây dựng hệ thống Plugin cho phép người dùng chạy code mở rộng trong môi trường cô lập an toàn trên máy chủ.\n- Tái sử dụng thư viện C++/Rust có sẵn trong dự án web/Node.js.",
        "when_not_to_use": "- Không dùng WebAssembly cho các thao tác thao tác DOM đơn giản hoặc CRUD thông thường (chi phí FFI giữa JS và WASM sẽ làm ứng dụng chậm hơn JS thuần).\n- Không dùng WASM cho các ứng dụng yêu cầu truy cập trực tiếp vào phần cứng hoặc hệ thống file không thông qua WASI.",
        "inputs": "- Mã nguồn ngôn ngữ gốc (Rust với `wasm-bindgen` hoặc C++ với Emscripten).\n- Giao diện kết nối JavaScript/TypeScript (Bindings).\n- Module WASM đã được biên dịch (`.wasm`).",
        "preconditions": "- Đã cài đặt `wasm-pack` (cho Rust) hoặc Emscripten SDK (cho C++).",
        "core_concepts": "- Linear Memory: Vùng nhớ của module WASM là một mảng byte liên tục (`ArrayBuffer`). Việc truyền dữ liệu lớn giữa JS và WASM nên được thực hiện bằng cách chia sẻ con trỏ trên linear memory thay vì copy chuỗi.\n- WASI (WebAssembly System Interface): Giao diện chuẩn mực cho phép module WASM chạy ngoài trình duyệt trên máy chủ (Server-side WASM) có thể truy cập file, network an toàn.\n- FFI Overhead: Lời gọi hàm giữa JavaScript và WebAssembly có độ trễ nhất định. Cần gom nhóm các thao tác (Batch processing) thay vì gọi hàng triệu lần qua lại ranh giới.",
        "decision_rules": "- Nếu truyền dữ liệu lớn (ảnh/video > 1MB): truyền con trỏ và kích thước bộ nhớ, thao tác trực tiếp trên `Uint8Array` của WASM Memory.\n- Bắt buộc chạy công cụ tối ưu hóa `wasm-opt -O3` để giảm kích thước file WASM trước khi phân phối.",
        "failure_scenarios": "- Cấp phát bộ nhớ trong WASM từ JavaScript nhưng quên gọi hàm giải phóng của module gốc, gây rò rỉ bộ nhớ nghiêm trọng trên trình duyệt.",
        "workflow": "1. Viết logic tính toán lõi bằng Rust và định nghĩa các API export bằng `#[wasm_bindgen]`.\n2. Biên dịch mã nguồn sang file `.wasm` tối ưu bằng lệnh `wasm-pack build --target web`.\n3. Tối ưu kích thước file bằng công cụ `wasm-opt` (giảm tới 40% dung lượng).\n4. Tích hợp module WASM vào ứng dụng Frontend/Node.js thông qua luồng nạp bất đồng bộ (`WebAssembly.instantiateStreaming`).\n5. Xây dựng các bài benchmark so sánh hiệu năng trực tiếp với JavaScript.",
        "example": "```rust\n// Rust: Mã nguồn thuật toán xử lý ảnh biên dịch sang WebAssembly\nuse wasm_bindgen::prelude::*;\n\n#[wasm_bindgen]\npub fn apply_grayscale(image_data: &mut [u8]) {\n    // Lặp qua các pixel (R, G, B, A) và tính độ xám trực tiếp trên linear memory\n    for chunk in image_data.chunks_exact_mut(4) {\n        let gray = (0.299 * chunk[0] as f32 + 0.587 * chunk[1] as f32 + 0.114 * chunk[2] as f32) as u8;\n        chunk[0] = gray;\n        chunk[1] = gray;\n        chunk[2] = gray;\n    }\n}\n```",
        "verification_commands": "```bash\n# Biên dịch và tối ưu hóa module Rust sang WASM\nwasm-pack build --target web --release\nwasm-opt -O3 pkg/image_filter_bg.wasm -o pkg/image_filter_bg.wasm\n```",
        "anti_patterns": "- Gọi hàm WASM bên trong một vòng lặp JS hàng triệu lần (gây nghẽn FFI).\n- Nạp file WASM lớn đồng bộ làm đơ luồng giao diện của người dùng (bắt buộc dùng `instantiateStreaming` và Web Workers).",
        "quality_gates": "- Dung lượng file `.wasm` sau khi nén Gzip/Brotli phải dưới 200KB cho các module frontend.\n- Hiệu năng xử lý thuật toán phải nhanh hơn JavaScript tối thiểu gấp 2 lần.",
        "security_constraints": "- Module WASM không được phép có quyền truy cập trực tiếp vào DOM hoặc Cookies của người dùng nếu không qua sandbox proxy.",
        "expected_outputs": "- Module WebAssembly (`.wasm`) và JavaScript bindings (`.js`, `.d.ts`).\n- Bộ test suite tích hợp và benchmark so sánh hiệu năng.",
        "related_skills": "dex-ffi-boundary-contracts, dex-reproducible-benchmarking, dex-frontend-architecture",
        "realistic_usage": "Một ứng dụng chỉnh sửa ảnh trực tuyến gặp khó khăn khi bộ lọc làm mịn da viết bằng JavaScript mất 1,800ms cho mỗi bức ảnh 4K. Chuyển đổi thuật toán sang Rust và biên dịch sang WebAssembly chạy trong Web Worker, thời gian xử lý giảm xuống còn 140ms, mang lại trải nghiệm mượt mà thời gian thực cho người dùng."
    },

    # 160. dex-ffi-boundary-contracts
    "dex-ffi-boundary-contracts": {
        "desc": "Design, document, and validate robust Foreign Function Interface (FFI) boundaries (C ABI) across languages, ensuring memory ownership contracts, alignment, and error translation. Use when binding native code across language ecosystems.",
        "purpose": "Thiết kế, đặc tả tài liệu và kiểm chứng các hợp đồng ranh giới giao tiếp đa ngôn ngữ (Foreign Function Interface - FFI Contracts: C ABI); bảo đảm tính toàn vẹn về quyền sở hữu bộ nhớ (Memory Ownership Contracts), căn chỉnh dữ liệu (Data Alignment/Padding), lan truyền mã lỗi an toàn và chống sập tiến trình khi truyền dữ liệu giữa các hệ sinh thái ngôn ngữ khác nhau (Node.js/Python/Go kết nối với C/Rust/C++).",
        "activation": "- Viết Native Extensions cho Node.js (Node-API / N-API) hoặc Python (CFFI / PyO3 / ctypes).\n- Tích hợp một thư viện mã nguồn gốc (C/C++ shared library `.so`/`.dll`) vào ứng dụng cấp cao.\n- Xảy ra lỗi crash tiến trình bí ẩn hoặc hỏng dữ liệu (Memory Corruption) tại điểm giao tiếp giữa hai ngôn ngữ.",
        "when_not_to_use": "- Không sử dụng FFI nếu hai dịch vụ có thể giao tiếp hiệu quả qua các giao thức mạng nội bộ (gRPC / Unix Domain Sockets) mà không cần chung tiến trình.\n- Không để các ngoại lệ (C++ Exceptions / Rust Panics) thoát ra ngoài ranh giới C ABI (dẫn đến Undefined Behavior và crash ngay lập tức).",
        "inputs": "- Header file C (`.h`) đặc tả C ABI.\n- Mã nguồn Native implementation và mã nguồn Caller wrapper.\n- Định nghĩa cấu trúc dữ liệu (`struct`) ở cả hai phía.",
        "preconditions": "- Cả hai phía đều thống nhất tuân thủ chuẩn gọi hàm C calling convention (`extern \"C\"`, `__cdecl` hoặc `__stdcall`).",
        "core_concepts": "- The C ABI as Lingua Franca: Chuẩn giao tiếp nhị phân C (C Application Binary Interface) là mẫu số chung duy nhất mà mọi ngôn ngữ lập trình đều hiểu và tương thích.\n- Ownership Rule of Thumb: 'Bên nào cấp phát (Allocate) thì bên đó phải giải phóng (Deallocate)'. Tuyệt đối không để phía Python/JS tự ý free một con trỏ được cấp phát bởi thư viện C/Rust mà không thông qua hàm deallocator chính thức của thư viện đó.\n- Panic / Exception Boundary: Ngoại lệ không bao giờ được bay qua ranh giới FFI. Mọi lỗi phải được bắt lại và chuyển thành mã số lỗi nguyên thủy (Error Code) hoặc cấu trúc kết quả.",
        "decision_rules": "- Bắt buộc đánh dấu cấu trúc dữ liệu dùng chung bằng thuộc tính `#[repr(C)]` trong Rust hoặc `#pragma pack` trong C để đảm bảo thứ tự và padding của các trường byte khớp nhau 100%.\n- Mọi hàm FFI phải trả về `int32_t` mã lỗi hoặc `struct FfiResult` rõ ràng.",
        "failure_scenarios": "- Cấu trúc struct ở phía C có padding 4 bytes nhưng phía Python ctypes không khai báo padding, khiến các giá trị đọc được bị lệch byte và làm sai lệch toàn bộ dữ liệu.",
        "workflow": "1. Định nghĩa file C Header `.h` chuẩn mực chứa các hàm `extern \"C\"` và struct `#[repr(C)]`.\n2. Viết mã nguồn thư viện gốc, bọc toàn bộ code trong khối `catch-all` để ngăn chặn panic/exception.\n3. Cung cấp hàm giải phóng bộ nhớ đi kèm (ví dụ: `free_my_buffer(void* ptr)`).\n4. Viết wrapper an toàn (Safe Wrapper) ở ngôn ngữ gọi (Python/Node.js) sử dụng RAII/Destructor để tự động gọi hàm free.\n5. Xây dựng test suite kiểm tra rò rỉ bộ nhớ tại ranh giới FFI bằng Valgrind hoặc ASan.",
        "example": "```rust\n// Rust: Định nghĩa C ABI an toàn cho thư viện native chia sẻ\n#[repr(C)]\npub struct CalculationResult {\n    pub value: f64,\n    pub error_code: i32,\n}\n\n#[no_mangle]\npub extern \"C\" fn calculate_risk(input_ptr: *const f64, length: usize) -> CalculationResult {\n    // Bắt toàn bộ panic không cho thoát ra ngoài C ABI\n    std::panic::catch_unwind(|| {\n        if input_ptr.is_null() {\n            return CalculationResult { value: 0.0, error_code: -1 };\n        }\n        let slice = unsafe { std::slice::from_raw_parts(input_ptr, length) };\n        let sum: f64 = slice.iter().sum();\n        CalculationResult { value: sum * 1.5, error_code: 0 }\n    }).unwrap_or(CalculationResult { value: 0.0, error_code: -99 })\n}\n```",
        "verification_commands": "```bash\n# Kiểm tra danh sách exported symbols của file thư viện nhị phân\nnm -D target/release/libmymath.so | grep calculate_risk\n```",
        "anti_patterns": "- Để Rust panic hoặc C++ exception văng trực tiếp qua ranh giới C ABI.\n- Giải phóng vùng nhớ của chuỗi bằng hàm `free()` của C trong khi chuỗi được cấp phát bởi Go runtime.",
        "quality_gates": "- 100% structs dùng qua FFI đều có khai báo `repr(C)` và căn chỉnh padding chuẩn xác.\n- Không có bất kỳ rò rỉ bộ nhớ nào tại ranh giới FFI sau 1,000,000 lượt gọi lặp lại.",
        "security_constraints": "- Kiểm tra con trỏ Null (`is_null()`) và kiểm tra kích thước bộ đệm (Buffer size bounds) trước khi đọc dữ liệu từ phía caller.",
        "expected_outputs": "- File C header `.h` và mã nguồn native exports.\n- Safe binding wrapper module cho ngôn ngữ cấp cao (Python/TypeScript).",
        "related_skills": "dex-rust-unsafe-audit, dex-webassembly-integration, dex-cpp-memory-safety",
        "realistic_usage": "Một ứng dụng Python AI cần gọi thuật toán giải mã vector viết bằng C++. Ban đầu, ứng dụng hay bị crash ngẫu nhiên do C++ ném ngoại lệ khi dữ liệu hỏng. Sau khi thiết lập hợp đồng FFI chuẩn với `#[repr(C)]`, bọc ngoại lệ thành mã lỗi và xây dựng safe wrapper bằng `ctypes`, hệ thống hoạt động ổn định 100% và tăng tốc độ xử lý lên 40 lần so với Python thuần."
    }
}

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    skills_base = os.path.join(root_dir, ".agents", "skills")
    
    print(f"=== GENERATING GROUP O (141-150) & GROUP P (151-160) ===")
    print(f"Target directory: {skills_base}")
    
    created_count = 0
    for skill_id, data in SKILLS_O_P.items():
        skill_dir = os.path.join(skills_base, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        skill_path = os.path.join(skill_dir, "SKILL.md")
        
        content = SKILL_TEMPLATE.format(
            skill_id=skill_id,
            desc=data["desc"],
            purpose=data["purpose"],
            activation=data["activation"],
            when_not_to_use=data["when_not_to_use"],
            inputs=data["inputs"],
            preconditions=data["preconditions"],
            core_concepts=data["core_concepts"],
            decision_rules=data["decision_rules"],
            failure_scenarios=data["failure_scenarios"],
            workflow=data["workflow"],
            example=data["example"],
            verification_commands=data["verification_commands"],
            anti_patterns=data["anti_patterns"],
            quality_gates=data["quality_gates"],
            security_constraints=data["security_constraints"],
            expected_outputs=data["expected_outputs"],
            related_skills=data["related_skills"],
            realistic_usage=data["realistic_usage"]
        )
        
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
            
        created_count += 1
        print(f"[{created_count}/20] Created {skill_id}")

    print(f"\nSUCCESS: Generated {created_count} skills for Group O & P.")

if __name__ == "__main__":
    main()
