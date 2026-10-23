---
name: dex-polyglot-build-orchestration
description: Orchestrate multi-language, multi-package monorepo builds with incremental compilation, graph-aware task scheduling, and remote caching. Use when scaling complex software architectures composed of heterogeneous languages.
---

# dex-polyglot-build-orchestration

## 1. Purpose & Scope
Điều phối và tối ưu hóa quy trình biên dịch monorepo đa ngôn ngữ (Polyglot Build Orchestration); áp dụng cơ chế biên dịch gia tăng (incremental compilation), lập lịch thực thi dựa trên đồ thị phụ thuộc (Graph-Aware Task Scheduling) và bộ nhớ đệm từ xa (Remote Caching).

## 2. When to Use
- Khi repository chứa nhiều module viết bằng các ngôn ngữ khác nhau (frontend TypeScript, backend Go, ML Python, native core Rust).
- Khi thời gian build toàn bộ dự án kéo dài hàng chục phút làm chậm chu kỳ phản hồi của lập trình viên.
- Khi chỉ sửa một dòng code ở một module nhưng hệ thống bắt biên dịch lại toàn bộ các dự án không liên quan.

## 3. When NOT to Use
- Khi dự án là một repository đơn ngôn ngữ nhỏ chỉ có vài trăm dòng code và thời gian build dưới 10 giây.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn monorepo đa ngôn ngữ, công cụ điều phối build (Bazel, Nx, Turborepo, Pants, Earthly).
- **Quyền hạn truy cập:** Quyền sửa đổi file cấu hình build hệ thống và máy chủ lưu trữ cache.

## 5. Core Concepts & Taxonomy
- **Task Dependency Graph:** Đồ thị có hướng (DAG) thể hiện thứ tự các bước build và kiểm thử; các tác vụ độc lập được thực thi song song tự động.
- **Remote Caching:** Lưu trữ kết quả đầu ra của các tác vụ build vào bộ nhớ đệm đám mây dựa trên mã băm nội dung đầu vào (Input Hash); nếu đầu vào không đổi, kết quả được khôi phục ngay lập tức mà không cần biên dịch lại.
- **Hermetic Builds:** Quá trình biên dịch hoàn toàn khép kín, chỉ phụ thuộc vào các đầu vào đã khai báo tường minh, không bị ảnh hưởng bởi file rác trên máy chủ.

## 6. Step-by-Step Execution Workflow
1. Khảo sát cấu trúc repository và phân ranh giới các gói module độc lập.
2. Khai báo các mục tiêu build (Targets) và đồ thị phụ thuộc giữa các module trong file cấu hình (Nx, Bazel, Earthly).
3. Cấu hình cơ chế tính mã băm đầu vào (Inputs Hash) bao gồm mã nguồn, biến môi trường và phiên bản compiler.
4. Kích hoạt bộ nhớ đệm cục bộ và kết nối tới dịch vụ Remote Cache (S3 hoặc HTTP Cache Server).
5. Tối ưu hóa việc thực thi song song các tác vụ kiểm thử và linting trên các nhân CPU khả dụng.
6. Đo lường tỷ lệ trúng cache (Cache Hit Ratio) và thời gian hoàn thành build qua từng commit.

## 7. Concrete Examples
### Cấu hình điều phối tác vụ và Remote Cache bằng Turborepo (turbo.json):
```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", "package.json", "tsconfig.json"],
      "outputs": ["dist/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**", "tests/**"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    }
  }
}
```

## 8. Anti-Patterns & Common Traps
- **Blind Monolithic Scripts:** Viết một script shell tuần tự `cd frontend && npm run build && cd ../backend && go build` không có cache và không chạy song song.
- **Undeclared Task Dependencies:** Chạy test backend phụ thuộc vào binary của module khác nhưng không khai báo quan hệ phụ thuộc trong build graph.
- **Non-Hermetic Build Inputs:** Nhúng các biến động như thời gian hiện tại vào input hash khiến cache luôn bị trượt (Cache Miss).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các module có quan hệ phụ thuộc được thể hiện chính xác trong đồ thị DAG.
- **QG-04**: Tỷ lệ trúng cache (Cache Hit Rate) trên CI đạt tối thiểu 70% đối với các PR chỉ sửa đổi cục bộ.
- **QG-08**: Thời gian build khi trúng cache giảm tối thiểu 80% so với build sạch từ đầu.

## 10. Security & Safety Boundaries
- Bảo vệ toàn vẹn Remote Cache bằng chữ ký mật mã (HMAC) để ngăn ngừa việc đầu độc cache với mã độc biên dịch sẵn.

## 11. Platform Adapters
- **Orchestrators**: Turborepo, Nx, Bazel, Pantsbuild, Earthly, Make.

## 12. Deliverables & Output Artifacts
- File cấu hình đồ thị build monorepo hoàn chỉnh.
- Cấu hình tích hợp Remote Caching an toàn trên CI/CD.
- Dashboard đo lường thời gian build và hiệu suất cache.

## 13. Related & Complementary Skills
dex-build-cache-integrity, dex-toolchain-version-pinning, dex-cross-language-contract-tests

## 14. Realistic Usage Example
```powershell
# Chạy build song song có sử dụng cache bằng Turborepo
npx turbo run build --cache-dir=.turbo

# Kiểm tra trực quan đồ thị phụ thuộc của monorepo
npx nx graph
```
