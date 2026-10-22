---
name: dex-software-maintenance
description: Long-term software maintenance, application lifecycle management, dependency upgrade roadmaps, technical debt prioritization, and deprecation policies. Balances stability with modernization. Use when triaging maintenance backlogs, upgrading end-of-life runtimes, or managing multi-version roadmaps.
---

# DEX Software Maintenance & Evolution

## 1. Purpose & Scope
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

## 3. When NOT to Use
- Xử lý các sự cố khẩn cấp (P0 hotfixes) đang làm sập hệ thống (dùng `dex-root-cause-debugging`).
- Viết lại toàn bộ hệ thống từ đầu (Rewrite from scratch) chỉ vì sở thích cá nhân của lập trình viên mới.

## 4. Prerequisites & Input Context
- Backlog danh sách các lỗi tồn đọng và yêu cầu cải tiến.
- Báo cáo lỗ hổng bảo mật và tình trạng hết hạn của các dependencies.
- Bản phân tích chi phí và lợi ích (Cost-Benefit Analysis) của các đợt nâng cấp.

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác kỹ thuật phải có thể kiểm chứng độc lập với số liệu rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
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

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-software-maintenance
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Maintenance Scope Confined)**: Mỗi đợt bảo trì chỉ tập trung vào một mục tiêu cụ thể, không trộn lẫn quá nhiều việc.
- **QG-06 (No Regressions from Upgrades)**: Việc nâng cấp thư viện không làm thay đổi hành vi nghiệp vụ của phần mềm.
- **QG-09 (Changelog & Docs Synchronized)**: Tất cả các nâng cấp đều được ghi nhận đầy đủ trong `CHANGELOG.md`.

## 10. Security & Safety Boundaries
- **Không Đổi Công Nghệ Khi Không Có Lý Do Kỹ Thuật Thuyết Phục**: Tuyệt đối cấm việc viết lại cả dự án bằng framework mới chỉ vì framework đó đang là trào lưu trên mạng xã hội.
- **Bắt Buộc Kiểm Tra Tính Tương Thích Ngược**: Mọi thay đổi bảo trì phải tôn trọng các client và dữ liệu hiện hữu.
- **Luôn Có Phương Án Khôi Phục (Rollback Strategy)**: Trước mỗi đợt nâng cấp lớn, phải đảm bảo có bản sao lưu cơ sở dữ liệu và khả năng rollback image/code trong vòng 5 phút.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Bản đánh giá sức khỏe phần mềm (Health Audit Report).
2. Lộ trình bảo trì theo từng phiên bản (Maintenance Roadmap trong `TASKS.md`).
3. Các bản cập nhật mã nguồn ổn định, tương thích ngược.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-software-maintenance** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
