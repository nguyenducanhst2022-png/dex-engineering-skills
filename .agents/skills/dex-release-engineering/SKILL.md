---
name: dex-release-engineering
description: Structured software release management, semantic versioning (SemVer), artifact packaging, automated changelog generation, and rollback planning. Enforces release readiness quality gates and deployment safety. Use when cutting new versions, building production packages, publishing releases, or preparing hotfixes.
---

# DEX Release Engineering

## 1. Purpose
Quản lý quy trình đóng gói và phát hành phần mềm chuyên nghiệp, tuân thủ Semantic Versioning (SemVer), tự động hóa ghi nhận Changelog, tạo gói phân phối sạch sẽ và chuẩn bị sẵn sàng phương án khôi phục (Rollback Plan) khi xảy ra sự cố.

Quy trình phát hành chuẩn:
`Hoàn thiện → Kiểm thử → Build → Đóng gói → Gắn Version → Phát hành → Giám sát → Bảo trì`

Nguyên tắc cốt lõi: **Chỉ phát hành phiên bản đã được kiểm chứng toàn diện, có tài liệu đầy đủ và có phương án khôi phục khả thi khi gặp lỗi.**
Ghi nhớ sống còn: **Code hoàn thiện ≠ Sản phẩm sẵn sàng phát hành.**

## 2. When to Use
- Khi toàn bộ các tính năng hoặc bản vá của một chu kỳ phát triển (Sprint / Milestone) đã hoàn tất và vượt qua mọi bài kiểm thử.
- Khi cần nâng số phiên bản ứng dụng (`major`, `minor`, `patch`) theo chuẩn SemVer.
- Khi tạo Git release tag, phát hành file nhị phân (Binaries / Docker Image / NPM package) hoặc triển khai lên môi trường Staging/Production.
- Khi phát hành bản vá khẩn cấp (Hotfix Release).

## 3. When Not to Use
- Trong quá trình phát triển tính năng dở dang trên các nhánh cục bộ.
- Khi còn bất kỳ bài kiểm thử nào đang bị rớt (FAIL) hoặc chưa được xác minh (`NOT VERIFIED`).

## 4. Inputs
- Trạng thái kho Git trên nhánh chính (`main`/`master`) sạch sẽ, không có uncommitted changes.
- Lịch sử commits kể từ phiên bản phát hành gần nhất (`git log <last-tag>..HEAD`).
- Số phiên bản hiện tại (từ `package.json`, `pyproject.toml`, `Cargo.toml`...).
- Báo cáo kết quả kiểm thử toàn diện và kiểm toán bảo mật.

## 5. Workflow

### Bước 1: Rà Soát Điều Kiện Tiên Quyết (Pre-release Verification)
- Xác minh 100% các Quality Gates bắt buộc đã đạt:
  - Tất cả Unit, Integration và E2E tests đạt PASS.
  - Quét bảo mật không còn lỗi nghiêm trọng.
  - Không có merge conflict hoặc file rác sót lại.

### Bước 2: Xác Định Số Phiên Bản Tiếp Theo (Semantic Versioning)
- Áp dụng nguyên tắc `MAJOR.MINOR.PATCH`:
  - **PATCH (x.y.Z)**: Sửa lỗi có khả năng tương thích ngược (Backward-compatible bug fixes).
  - **MINOR (x.Y.0)**: Bổ sung tính năng mới có khả năng tương thích ngược.
  - **MAJOR (X.0.0)**: Thay đổi phá vỡ tương thích (Breaking changes).

### Bước 3: Biên Dịch & Đóng Gói (Build & Artifact Packaging)
- Chạy lệnh build chính thức cho môi trường Production:
  - Tạo file build tối ưu (minified, bundled, source map tách biệt).
  - Đóng gói Docker image hoặc bundle tương ứng.
- Kiểm tra tính toàn vẹn của gói (Checksum / Hash verification).

### Bước 4: Tạo Nhật Ký Thay Đổi Tự Động (Changelog Generation)
- Cập nhật file `CHANGELOG.md` theo chuẩn Keep a Changelog:
  - Thêm tiêu đề phiên bản kèm ngày tháng: `## [1.2.0] - 2026-10-22`
  - Liệt kê các mục: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

### Bước 5: Gắn Nhãn Phiên Bản (Git Tagging)
- Tạo Git tag có chú thích (Annotated tag):
  ```bash
  git tag -a v1.2.0 -m "Release version 1.2.0: add coupon discount and user profile"
  ```
- Đẩy commit cập nhật changelog và tag lên remote:
  ```bash
  git push origin main --tags
  ```

### Bước 6: Soạn Thảo Kế Hoạch Khôi Phục Dự Phòng (Rollback Plan)
- Xác định rõ kịch bản: Nếu sau khi phát hành phiên bản mới gặp sự cố tê liệt:
  - Quy trình hoàn tác về tag phiên bản trước (`v1.1.9`) trong bao nhiêu phút?
  - Cơ chế rollback database (nếu có migration) đã được kiểm tra chưa?

### Bước 7: Bàn Giao Giám Sát Sau Phát Hành (Post-release Hand-off)
- Bàn giao việc theo dõi cho `dex-production-monitoring` để giám sát tỷ lệ lỗi (Error rate) và mức tiêu thụ tài nguyên trong 30-60 phút đầu tiên sau phát hành.

## 6. Quality Gates
- **QG-01 đến QG-10**: Đối với phát hành Production, bắt buộc áp dụng **STRICT MODE** — Toàn bộ 10 Quality Gates phải đạt trạng thái PASS (hoặc SKIP có biên bản phê duyệt).
- **QG-09 (Docs & Changelog Updated)**: `CHANGELOG.md` và `package.json` phiên bản mới được cập nhật nhất quán.

## 7. Safety Rules
- **Cấm Phát Hành Khi Test Chưa PASS**: Tuyệt đối không bao giờ tạo release tag khi test suite chưa chạy thành công trên commit đó.
- **Không Ghi Đè Release Tag (Immutable Releases)**: Một khi tag phiên bản đã được công bố ra ngoài, không bao giờ xóa hoặc trỏ tag đó sang commit khác. Nếu có lỗi, phải phát hành phiên bản Patch mới (`v1.2.1`).
- **Phải Có Phương Án Rollback**: Không phát hành phần mềm nếu không có phương án quay xe dự phòng rõ ràng.

## 8. Expected Outputs
1. File `CHANGELOG.md` được cập nhật chuyên nghiệp.
2. Git annotated tag (ví dụ: `v1.2.0`) trên commit phát hành.
3. Bản đóng gói sản phẩm (Production Build Artifact).
4. Kế hoạch rollback chi tiết (Rollback Strategy).

## 9. Failure Handling
- Nếu quá trình build production bị lỗi: Dừng phát hành, không tạo git tag, quay lại khắc phục lỗi build ở môi trường staging.
- Nếu sau khi release phát sinh sự cố nghiêm trọng: Thực thi Rollback Plan ngay lập tức về tag ổn định trước đó.

## 10. Completion Criteria
- Mã nguồn được đóng gói thành công, tag phiên bản đã tạo và đẩy lên Git.
- Changelog được ghi nhận rõ ràng và phương án rollback đã sẵn sàng.

---

## Real-world Example
Phát hành phiên bản `v1.0.0` cho hệ thống E-commerce:
1. *Kiểm tra*: 120/120 tests PASS, Audit 0 vulnerability.
2. *Changelog*: Cập nhật `CHANGELOG.md` ghi nhận tính năng Giỏ hàng, Thanh toán Stripe, Đăng ký thành viên.
3. *Đóng gói*: `npm run build` sinh thư mục `dist/` gọn gàng (bundle size: 450KB).
4. *Tag*: `git tag -a v1.0.0 -m "Release v1.0.0 - Initial Production Release"`.
5. *Rollback plan*: Nếu lỗi, chuyển traffic về container chạy image `v0.9.5-rc`.
