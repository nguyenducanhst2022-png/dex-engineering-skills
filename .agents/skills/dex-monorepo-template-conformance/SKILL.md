---
name: dex-monorepo-template-conformance
description: Audit, enforce, and scaffold standardized directory structures, toolchain files, linting configs, and GitHub workflows across monorepo packages. Use when scaling multi-package repositories without architectural decay.
---

# dex-monorepo-template-conformance

## 1. Purpose & Scope
Kiểm toán, thực thi và khởi tạo cấu trúc thư mục chuẩn mực (Monorepo Template Conformance); chuẩn hóa các file cấu hình công cụ, quy tắc linter, kịch bản CI GitHub Actions và tài liệu giữa các gói package bên trong monorepo; ngăn ngừa sự suy thoái kiến trúc theo thời gian.

## 2. When to Use
- Khi monorepo phát triển lên hàng chục hoặc hàng trăm packages và mỗi nhóm lại tự ý cấu hình một kiểu khác nhau.
- Khi cần tạo nhanh một package mới (service, library, UI component) tuân thủ 100% tiêu chuẩn kỹ thuật của công ty.
- Khi cập nhật cấu hình chung (tsconfig, eslint, license) và muốn tự động đồng bộ tới toàn bộ các packages.

## 3. When NOT to Use
- Khi dự án là một repository đơn lẻ độc lập không nằm trong kiến trúc monorepo đa gói.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Monorepo chứa nhiều packages, bộ template mẫu chuẩn mực, công cụ scaffold (Plop, Turborepo generators, Manypkg).
- **Quyền hạn truy cập:** Quyền sửa đổi cấu hình các gói package con trong monorepo.

## 5. Core Concepts & Taxonomy
- **Golden Template Pattern:** Gói mẫu tiêu chuẩn chứa đầy đủ cấu hình chuẩn mực nhất mà mọi gói mới đều phải tuân theo.
- **Conformance Linter:** Công cụ tự động quét toàn bộ các package để phát hiện các file cấu hình bị thiếu, phiên bản thư viện dùng chung bị lệch, hoặc cấu trúc thư mục sai quy chuẩn.
- **Dependency Synchronization:** Đảm bảo các packages bên trong monorepo luôn sử dụng cùng một phiên bản của các thư viện bên ngoài (ví dụ: tất cả cùng dùng `react@18.2.0`).

## 6. Step-by-Step Execution Workflow
1. Xây dựng các mẫu khởi tạo chuẩn (Golden Templates) cho từng loại gói: UI Library, Node API Service, Python Worker, Go Microservice.
2. Định nghĩa danh mục các file bắt buộc phải có trong mỗi package: `package.json`, `tsconfig.json`, `README.md`, `tests/`.
3. Sử dụng công cụ `manypkg` hoặc script tùy biến để kiểm toán tính nhất quán của các trường manifest.
4. Kế thừa các cấu hình gốc dùng chung (Shared Base Configs) thông qua cơ chế `extends`.
5. Tích hợp lệnh kiểm tra tuân thủ cấu trúc vào pipeline CI: gắn cờ các package không tuân thủ.
6. Cung cấp lệnh dòng lệnh tự động sửa lỗi (Auto-Fix) để đồng bộ hóa cấu hình toàn bộ monorepo chỉ bằng một thao tác.

## 7. Concrete Examples
### Kiểm toán tính nhất quán của monorepo bằng manypkg và script Conformance:
```json
// packages/my-lib/tsconfig.json - Ke thua cau hinh chuan muc
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

```powershell
# Chay kiem toan tinh nhat quan cua cac dependencies giua cac packages
npx @manypkg/cli check

# Tu dong dong bo phien ban thu vien dung chung bi sai lech
npx @manypkg/cli fix
```

## 8. Anti-Patterns & Common Traps
- **Copy-Paste Package Scaffolding:** Tạo package mới bằng cách sao chép nguyên vẹn một package cũ kèm theo các file rác và cấu hình lỗi thời.
- **Fragmented Dependency Versions:** Package A dùng `lodash@4.17.20`, trong khi Package B dùng `lodash@4.17.21` làm tăng dung lượng bundle và gây lỗi khó lường.
- **Standalone Unlinked Configs:** Tự viết các file `tsconfig` hoặc `eslint` riêng rẽ trong từng package mà không kế thừa từ cấu hình chuẩn dùng chung.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các packages trong monorepo tuân thủ đầy đủ cấu trúc thư mục quy định.
- **QG-04**: Lệnh kiểm toán `manypkg check` không phát hiện bất kỳ sự sai lệch phiên bản thư viện dùng chung nào.
- **QG-07**: Tất cả các package mới đều được tạo ra từ công cụ scaffold chuẩn.

## 10. Security & Safety Boundaries
- Đảm bảo các file cấu hình bảo mật (như chính sách quét phụ thuộc, linters) được áp dụng đồng bộ không có ngoại lệ.

## 11. Platform Adapters
- **Tools**: @manypkg/cli, Syncpack, Plop.js, Turborepo Generators, Nx Generators.

## 12. Deliverables & Output Artifacts
- Bộ template chuẩn mực cho các loại package monorepo.
- Công cụ tự động scaffold và kiểm toán tuân thủ cấu trúc.
- Script kiểm tra và tự động đồng bộ hóa phiên bản thư viện dùng chung.

## 13. Related & Complementary Skills
dex-polyglot-build-orchestration, dex-package-publishing-preflight, dex-toolchain-version-pinning

## 14. Realistic Usage Example
```powershell
# Kiểm tra sự tuân thủ quy chuẩn của toàn bộ packages
npx syncpack list-mismatches

# Tạo một package mới tuân thủ 100% quy chuẩn
npx turbo gen workspace
```
