---
name: dex-feature-flags
description: Feature flags engineering, progressive delivery, staged canary rollouts, kill switches, and flag cleanup lifecycles. Decouples code deployment from feature release for zero-risk rollouts. Use when releasing high-risk features, conducting A/B experiments, or implementing instant kill-switches.
---

# DEX Feature Flags & Progressive Delivery

## 1. Purpose & Scope
Tách biệt hoàn toàn việc triển khai mã nguồn (Deployment) khỏi việc kích hoạt tính năng (Release) cho người dùng cuối thông qua Feature Flags (Feature Toggles); cho phép phát hành theo từng giai đoạn (Staged Rollout), thử nghiệm canary trên nhóm người dùng nhỏ và kích hoạt cơ chế tắt khẩn cấp (Instant Kill-Switch) chỉ trong 1 giây mà không cần deploy lại code khi xảy ra sự cố.

Quy trình phát hành an toàn với Feature Flag:
`Phát triển tính năng → Kiểm thử → Bật thử nghiệm → Giám sát → Mở rộng dần → Hoàn tất rollout → Dọn dẹp cờ → Ổn định`

Nguyên tắc cốt lõi: **Triển khai code lên máy chủ ≠ Kích hoạt cho người dùng sử dụng. Luôn luôn phải có phương án tắt tính năng tức thì (Kill-switch) khi xảy ra lỗi nghiêm trọng.**
Ghi nhớ sống còn: **Feature Flag tốt = Triển khai không rủi ro + Rollout từng bước + Tắt khẩn cấp trong 1 giây + Có kế hoạch dọn dẹp cờ.**

## 2. When to Use
- Khi phát hành các tính năng mới có rủi ro cao (Thay đổi thuật toán gợi ý, cổng thanh toán mới, giao diện mới).
- Khi muốn mở tính năng trước cho đội ngũ nội bộ (Internal Dogfooding / Beta testers) kiểm tra trước khi mở cho toàn bộ người dùng.
- Khi cần chạy thử nghiệm phân tách A/B Testing để đo lường tỷ lệ chuyển đổi.
- Khi triển khai liên tục (Trunk-based development) nơi code chưa hoàn thiện vẫn có thể merge vào nhánh chính nhưng được giấu sau cờ tắt.

## 3. When NOT to Use
- Các bản vá lỗi cú pháp nhỏ, cập nhật tài liệu hoặc sửa lỗi khẩn cấp đơn giản.
- Để tồn tại hàng chục Feature Flags cũ đã bật 100% qua nhiều tháng mà không bao giờ dọn dẹp mã nguồn.

## 4. Prerequisites & Input Context
- Hệ thống quản lý cờ (Environment variables, LaunchDarkly, Unleash, Flipt, PostHog, hoặc bảng cấu hình DB).
- Tỷ lệ rollout mong muốn (ví dụ: 5% người dùng → 25% → 50% → 100%).
- Tiêu chí sức khỏe hệ thống để quyết định tiếp tục rollout hay dừng khẩn cấp (Error rate, latency).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác kỹ thuật phải có thể kiểm chứng độc lập với số liệu rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Khởi Tạo Cờ Tính Năng (Flag Declaration)
- Đặt tên cờ rõ nghĩa, có tiền tố phân loại:
  - `ff_new_payment_checkout_v2`: Boolean flag.
  - Thiết lập giá trị mặc định luôn là `FALSE` (Tắt) trong môi trường production cho đến khi có lệnh bật chủ động.

### Bước 2: Bọc Mã Nguồn Trong Khối Điều Kiện (Flag Wrapping)
- Bọc code tính năng mới trong nhánh điều kiện:
  ```typescript
  if (featureFlags.isEnabled('ff_new_payment_checkout_v2', userContext)) {
    return renderNewCheckout();
  } else {
    return renderLegacyCheckout(); // Nhánh fallback an toàn
  }
  ```

### Bước 3: Kiểm Thử Cả Hai Trạng Thái (Dual-State Verification)
- Viết bài kiểm thử tự động cho CẢ HAI trường hợp:
  - Khi Flag = `FALSE`: Hệ thống chạy nhánh cũ bình thường, không có lỗi.
  - Khi Flag = `TRUE`: Hệ thống chạy nhánh mới chính xác theo yêu cầu.

### Bước 4: Kích Hoạt Thử Nghiệm Nội Bộ (Canary / Beta Rollout)
- Bật cờ cho nhóm người dùng nội bộ (nhân viên công ty / whitelist user IDs).
- Thu thập phản hồi và theo dõi log lỗi.

### Bước 5: Mở Rộng Dần Theo Tỷ Lệ (Progressive Percentage Rollout)
- Tăng dần tỷ lệ người dùng tiếp cận:
  - Ngày 1: Mở cho 5% traffic. Theo dõi tỷ lệ lỗi 5xx trong 2-4 tiếng.
  - Ngày 2: Mở cho 25% traffic.
  - Ngày 3: Mở cho 50% rồi nâng lên 100%.

### Bước 6: Kích Hoạt Tắt Khẩn Cấp Nếu Có Lỗi (Emergency Kill-Switch)
- Nếu tại bất kỳ bước nào tỷ lệ lỗi tăng vọt hoặc khách hàng khiếu nại: Chuyển ngay giá trị cờ về `FALSE`. Toàn bộ hệ thống quay về luồng cũ ngay lập tức mà không cần rollback Git hay redeploy.

### Bước 7: Dọn Dẹp Cờ Tính Năng (Flag Retirement & Tech Debt Cleanup)
- Sau khi tính năng đã bật 100% ổn định trong 1-2 tuần:
  - Lập task kỹ thuật dọn dẹp: Xóa biến cờ, xóa khối `if-else`, xóa nhánh code cũ thừa.
  - Tránh để mã nguồn trở thành "rừng cờ" (Flag Spaghetti Debt).

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-feature-flags
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Flag Default Safe)**: Giá trị mặc định của cờ trong cấu hình sản xuất luôn là OFF.
- **QG-05 (Both Flag Branches PASS)**: Cả hai nhánh bật và tắt đều có unit test và đạt 100% PASS.
- **QG-10 (Kill-Switch Verified)**: Đã kiểm chứng thao tác tắt cờ đưa hệ thống về trạng thái cũ an toàn.

## 10. Security & Safety Boundaries
- **Luôn Có Nhánh Fallback Cũ**: Không được xóa nhánh code cũ chừng nào tính năng mới chưa được rollout 100% và chạy ổn định.
- **Không Lồng Quá 2 Cờ Nhau**: Tuyệt đối tránh việc lồng các khối Feature Flag vào nhau (`if (flagA) { if (flagB) ... }`) vì sẽ tạo ra tổ hợp trạng thái không thể kiểm thử hết.
- **Bắt Buộc Có Hạn Sử Dụng (Flag TTL)**: Mỗi cờ tính năng phải có ngày hết hạn dự kiến để đội ngũ kỹ thuật dọn dẹp.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Mã nguồn tích hợp Feature Flag sạch sẽ, có fallback an toàn.
2. Bài kiểm thử cho cả 2 trạng thái ON và OFF.
3. Kế hoạch rollout theo tỷ lệ kèm tiêu chí kích hoạt Kill-switch.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-feature-flags** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
