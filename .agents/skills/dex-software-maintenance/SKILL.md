---
name: dex-software-maintenance
description: Long-term software maintenance, application lifecycle management, dependency upgrade roadmaps, technical debt prioritization, and deprecation policies. Balances stability with modernization. Use when triaging maintenance backlogs, upgrading end-of-life runtimes, or managing multi-version roadmaps.
---

# DEX Software Maintenance & Evolution

## 1. Purpose
Quản trị vòng đời bảo trì và phát triển dài hạn của phần mềm (Software Maintenance & Evolution); thiết lập lộ trình nâng cấp (Roadmap) có kiểm soát, ưu tiên xử lý các khoản nợ kỹ thuật và lỗ hổng bảo mật, đảm bảo hệ thống luôn ổn định, an toàn và tiến hóa bền vững mà không bị gián đoạn hoạt động kinh doanh.

Quy trình bảo trì chuẩn:
`Giám sát → Thu thập vấn đề → Đánh giá ưu tiên → Lập Roadmap → Nâng cấp → Kiểm thử → Phát hành → Tiếp tục theo dõi`

Nguyên tắc cốt lõi: **Không nâng cấp liên tục chỉ vì ngoài kia có công nghệ mới. Mọi sự thay đổi đưa vào hệ thống phải thực sự mang lại giá trị kinh doanh hoặc giải quyết rủi ro bảo mật thực tế, không tạo ra rủi ro không cần thiết.**
Ghi nhớ sống còn: **Bảo trì tốt = Hệ thống luôn chạy ổn định + Nâng cấp có kế hoạch + Kiểm soát rủi ro + Giữ giá trị lâu dài.**

## 2. When to Use
- Khi định kỳ rà soát và đánh giá sức khỏe dự án (Quarterly / Monthly maintenance review).
- Khi runtime hoặc thư viện cốt lõi sắp hết hạn hỗ trợ (End-of-Life - EOL), ví dụ Node.js 18 EOL cần lên Node.js 20/22.
- Khi lập kế hoạch phân bổ nguồn lực giữa: Sửa lỗi tồn đọng (Bug fixes), Trả nợ kỹ thuật (Technical debt), Tối ưu hiệu năng và Phát triển tính năng mới.
- Khi cần ban hành chính sách ngưng hỗ trợ (Deprecation Policy) cho các API hoặc tính năng cũ.

## 3. When Not to Use
- Xử lý các sự cố khẩn cấp (P0 hotfixes) đang làm sập hệ thống (dùng `dex-root-cause-debugging`).
- Viết lại toàn bộ hệ thống từ đầu (Rewrite from scratch) chỉ vì sở thích cá nhân của lập trình viên mới.

## 4. Inputs
- Backlog danh sách các lỗi tồn đọng và yêu cầu cải tiến.
- Báo cáo lỗ hổng bảo mật và tình trạng hết hạn của các dependencies.
- Bản phân tích chi phí và lợi ích (Cost-Benefit Analysis) của các đợt nâng cấp.

## 5. Workflow

### Bước 1: Khảo Sát & Đánh Giá Hiện Trạng Hệ Thống (Health Audit)
- Kiểm tra toàn diện:
  - Số lượng bug tồn đọng chưa giải quyết theo mức độ ưu tiên.
  - Các thư viện phụ thuộc đã lỗi thời hoặc chứa cảnh báo an ninh.
  - Mức độ bao phủ kiểm thử (Test coverage) hiện tại có đủ an toàn để nâng cấp không.

### Bước 2: Phân Loại Hạng Mục Công Việc Bảo Trì (Work Item Classification)
- Phân chia công việc thành 4 nhóm rõ ràng:
  1. **Security & Compliance**: Vá lỗ hổng khẩn cấp, tuân thủ pháp lý (Ưu tiên số 1).
  2. **Corrective Maintenance**: Sửa các bug ảnh hưởng đến trải nghiệm người dùng.
  3. **Preventive Maintenance**: Nâng cấp runtime EOL, refactor nợ kỹ thuật có nguy cơ bùng phát.
  4. **Perfective Maintenance**: Tối ưu hiệu năng, nâng cấp giao diện, mở rộng tính năng.

### Bước 3: Đánh Giá Ưu Tiên Theo Ma Trận Tác Động / Rủi Ro (Prioritization Matrix)
- Sử dụng công thức: $\text{Priority} = \frac{\text{Giá trị mang lại} \times \text{Mức độ khẩn cấp}}{\text{Rủi ro} \times \text{Chi phí thực hiện}}$.
- Kiên quyết từ chối các đề xuất nâng cấp thư viện lớn nếu lợi ích mang lại bằng 0 nhưng rủi ro gãy hệ thống lại rất cao.

### Bước 4: Xây Dựng Lộ Trình Tiến Hóa Theo Từng Phiên Bản (Evolution Roadmap)
- Chia lộ trình bảo trì thành các mốc phiên bản SemVer cụ thể:
  - *Phiên bản v1.1.0*: Nâng cấp Node.js runtime lên v20 LTS và cập nhật các bản vá bảo mật.
  - *Phiên bản v1.2.0*: Tái cấu trúc module thanh toán và cải thiện tốc độ API.
- Mỗi phiên bản có phạm vi nhỏ gọn, rõ ràng, có tiêu chí nghiệm thu độc lập.

### Bước 5: Thực Hiện Nâng Cấp Có Kiểm Soát & Hồi Quy Chặt Chẽ (Safe Upgrade)
- Áp dụng các kỹ năng `dex-change-impact-analysis`, `dex-testing-engineering` và `dex-git-workflow` trong từng bước nâng cấp.
- Đảm bảo 100% test suite vượt qua trước khi phát hành.

### Bước 6: Cập Nhật Tài Liệu Kỹ Thuật & Deprecation Notice
- Cập nhật `README.md`, `CHANGELOG.md` và tài liệu kiến trúc.
- Nếu có hàm/API chuẩn bị bị xóa bỏ: Gắn nhãn `@deprecated` trước ít nhất 1-2 phiên bản trước khi xóa hẳn.

### Bước 7: Tiếp Tục Giám Sát Sau Nâng Cấp (Post-upgrade Monitoring)
- Theo dõi hệ thống giám sát trong 48 giờ sau khi đưa phiên bản bảo trì lên production.

## 6. Quality Gates
- **QG-01 (Maintenance Scope Confined)**: Mỗi đợt bảo trì chỉ tập trung vào một mục tiêu cụ thể, không trộn lẫn quá nhiều việc.
- **QG-06 (No Regressions from Upgrades)**: Việc nâng cấp thư viện không làm thay đổi hành vi nghiệp vụ của phần mềm.
- **QG-09 (Changelog & Docs Synchronized)**: Tất cả các nâng cấp đều được ghi nhận đầy đủ trong `CHANGELOG.md`.

## 7. Safety Rules
- **Không Đổi Công Nghệ Khi Không Có Lý Do Kỹ Thuật Thuyết Phục**: Tuyệt đối cấm việc viết lại cả dự án bằng framework mới chỉ vì framework đó đang là trào lưu trên mạng xã hội.
- **Bắt Buộc Kiểm Tra Tính Tương Thích Ngược**: Mọi thay đổi bảo trì phải tôn trọng các client và dữ liệu hiện hữu.
- **Luôn Có Phương Án Khôi Phục (Rollback Strategy)**: Trước mỗi đợt nâng cấp lớn, phải đảm bảo có bản sao lưu cơ sở dữ liệu và khả năng rollback image/code trong vòng 5 phút.

## 8. Expected Outputs
1. Bản đánh giá sức khỏe phần mềm (Health Audit Report).
2. Lộ trình bảo trì theo từng phiên bản (Maintenance Roadmap trong `TASKS.md`).
3. Các bản cập nhật mã nguồn ổn định, tương thích ngược.

## 9. Failure Handling
- Nếu việc nâng cấp một thư viện cốt lõi làm phát sinh hàng loạt lỗi không thể sửa trong thời gian dự kiến: Hủy bỏ đợt nâng cấp, giữ nguyên phiên bản cũ ổn định và lập kế hoạch cách ly module đó trước.

## 10. Completion Criteria
- Các lỗ hổng bảo mật và thư viện EOL được cập nhật thành công.
- Toàn bộ hệ thống hoạt động ổn định, tài liệu phản ánh chính xác trạng thái hiện tại.

---

## Real-world Example
Kế hoạch bảo trì định kỳ quý 4:
- *Mục tiêu*: Nâng cấp Node.js từ v18 lên v20 LTS (Active LTS).
- *Tác động*: Kiểm tra 32 dependencies xem có package nào không tương thích với Node 20 không → Phát hiện package `node-sass` lỗi thời → Thay thế bằng `sass-embedded`.
- *Kiểm thử*: Chạy toàn bộ 180 unit/integration tests trên container `node:20-alpine` → PASS 100%.
- *Ghi nhận*: Cập nhật `package.json`, `.nvmrc`, `Dockerfile` và `CHANGELOG.md` phiên bản `v1.4.0`.
