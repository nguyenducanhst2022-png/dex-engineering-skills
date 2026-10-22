---
name: dex-container-image-engineering
description: Engineer production-grade, secure, minimal container images using multi-stage builds, non-root users, distroless/alpine bases, reproducible layers, SBOM generation (Syft), and vulnerability scanning (Trivy). Use when containerizing applications or optimizing container security and size.
---

# dex-container-image-engineering

## 1. Purpose & Scope
Thiết kế, xây dựng và tối ưu hóa Container Images đạt tiêu chuẩn môi trường sản xuất; áp dụng multi-stage builds nhằm giảm thiểu kích thước image, sử dụng minimal base images (Distroless / Alpine / Scratch), chạy dưới non-root user (UID 10001+), tối ưu hóa thứ tự layer caching, tạo Software Bill of Materials (SBOM) và quét lỗ hổng bảo mật tự động bằng Trivy / Grype.

## 2. When to Use
- Khi đóng gói ứng dụng mới vào Docker / OCI container image.
- Khi container image hiện tại quá lớn (>500MB - 1GB) gây chậm trễ thời gian pull trong CI/CD hoặc auto-scaling.
- Khi kiểm toán an ninh container phát hiện image chạy bằng quyền root hoặc chứa các CVE nghiêm trọng từ hệ điều hành cơ sở.

## 3. When NOT to Use
- Điều phối nhiều container trên cụm máy chủ (dùng `dex-kubernetes-deployment`).
- Thiết lập hạ tầng ảo hóa máy chủ hoặc VPC mạng (dùng `dex-infrastructure-as-code`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mã nguồn ứng dụng, tệp mô tả dependencies (`package.json`, `go.mod`, `requirements.txt`).
- Runtime target và các công cụ biên dịch yêu cầu.
- Yêu cầu bảo mật: Non-root UID, cấm shell trong production, hạn chế volume ghi.
- **Điều kiện tiên quyết**:
- Docker hoặc Podman / Buildah được cài đặt và cấu hình buildkit (`DOCKER_BUILDKIT=1`).
- Công cụ quét an ninh Trivy hoặc Grype sẵn sàng trong pipeline.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Multi-Stage Build Pattern**: Tách biệt hoàn toàn stage biên dịch (chứa compiler, SDK, build tools) khỏi stage phát hành (chỉ chứa binary runtime và tệp tĩnh).
- **Layer Caching Invariance**: Đặt các bước ít thay đổi (cài đặt package dependencies) lên trước các bước thay đổi thường xuyên (copy mã nguồn ứng dụng).
- **Least-Privilege Container Runtime**: Chạy container với cờ `USER 10001:10001` và `read-only root filesystem`.
- **Quy tắc quyết định kỹ thuật**:
- **Cấm Dùng Base Image `latest`**: Bắt buộc gắn tag cụ thể kèm SHA256 digest (ví dụ: `node:20.11-alpine@sha256:...`).
- **Không Chạy Bằng Root**: Tuyệt đối không để container thực thi dưới quyền UID 0 trong môi trường production.
- **Không Chứa Secret trong Image**: Không truyền API key, token qua lệnh `ENV` hoặc `ARG` mà không sử dụng Docker Secret Mounts (`--mount=type=secret`).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗ hổng bảo mật nghiêm trọng trong OS packages**: Base image chứa curl, bash cũ có CVE -> Khắc phục: Chuyển sang Google Container Tools Distroless image (chỉ có runtime không có shell/package manager).
- **Build cache bị phá vỡ mỗi lần sửa 1 dòng code**: Lệnh `COPY . .` được đặt trước `npm install` -> Khắc phục: Đưa `COPY package*.json` và `RUN npm ci` lên trước `COPY src/`.

## 6. Step-by-Step Execution Workflow
1. Phân tích dependencies và xác định runtime runtime tối thiểu (Go binary tĩnh dùng `scratch`, Node/Python dùng `distroless` hoặc `alpine`).
2. Viết Dockerfile đa tầng (Multi-Stage): Giai đoạn 1 `builder` tải dependencies và biên dịch; Giai đoạn 2 `runner` chỉ copy artifact cần thiết.
3. Tạo user không đặc quyền (`appuser`, UID 10001) và cấp quyền sở hữu thư mục làm việc (`chown -R appuser:appgroup /app`).
4. Cấu hình tệp `.dockerignore` loại bỏ triệt để: `.git`, `node_modules`, `tests`, `*.md`, `.env*`.
5. Xây dựng image với BuildKit và quét an ninh bằng Trivy: `trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:v1`.
6. Sinh SBOM (Software Bill of Materials) theo định dạng SPDX hoặc CycloneDX bằng công cụ `syft`.
7. Đẩy image lên OCI Container Registry kèm chữ ký Cosign.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```dockerfile
# syntax=docker/dockerfile:1.4
# Stage 1: Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /build
RUN apk add --no-cache ca-certificates git
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /build/server ./cmd/server

# Stage 2: Runtime stage
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /app
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder --chown=nonroot:nonroot /build/server /app/server
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app/server"]
```

### Lệnh xác minh & thực thi:
- Build image với BuildKit: `docker buildx build -t myapp:latest --load .`
- Quét lỗ hổng an ninh: `trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:latest`
- Kiểm tra user non-root: `docker run --rm myapp:latest id` (phải trả về UID > 0)
- Sinh SBOM: `syft myapp:latest -o cyclonedx-json=sbom.json`

## 8. Anti-Patterns & Common Traps
- **Dùng Ubuntu Full Image cho Go/Rust Service**: Khiến image nặng 800MB thay vì 15MB distroless.
- **Lưu secret build-time vào Dockerfile**: `RUN echo $TOKEN > /root/.token` (layer vẫn còn vết trong image history).
- **Bỏ qua .dockerignore**: Copy cả thư mục `.git` và file bí mật `.env.local` vào image.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Image size tối ưu (<100MB cho Go/Rust, <200MB cho Node/Python).
- QG-07: Quét an ninh 0 lỗ hổng nghiêm trọng (0 CRITICAL CVEs).
- QG-10: Container chạy dưới quyền non-root (UID != 0).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Chặn hoàn toàn việc chạy container ở chế độ `--privileged`.
- Cấu hình file system chỉ đọc (`read-only root filesystem`) trong production deployment.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- `Dockerfile` tối ưu hóa đa tầng (multi-stage).
- Tệp `.dockerignore` đầy đủ.
- File tài liệu SBOM `sbom.json` và báo cáo quét bảo mật Trivy.

## 13. Related & Complementary Skills
- `dex-kubernetes-deployment`: Triển khai image lên cụm Kubernetes.
- `dex-cicd-automation`: Tự động hóa build và quét container trong pipeline CI/CD.
- `dex-supply-chain-security`: Ký image và xác thực nguồn gốc artifact.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư tiếp nhận nhiệm vụ container hóa một microservice Node.js. Áp dụng `dex-container-image-engineering`, kỹ sư tạo Dockerfile multi-stage với base image `node:20-alpine`, cấu hình user `node`, loại bỏ devDependencies bằng `npm prune --production`, tạo `.dockerignore` ngăn leak `.env`, và thiết lập bước quét Trivy trong GitHub Actions chặn build nếu phát hiện CVE CRITICAL.
