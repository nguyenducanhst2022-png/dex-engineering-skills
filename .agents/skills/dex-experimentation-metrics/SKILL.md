---
name: dex-experimentation-metrics
description: Architect feature flagging, experimentation platforms, A/B testing infrastructure, statistical significance evaluation, rollout strategies (canary/percentage), and metric telemetry. Use when launching new features, running experiments, or canary rollouts.
---

# dex-experimentation-metrics

## 1. Purpose & Scope
Thiết kế và triển khai cơ sở hạ tầng Thí nghiệm Tính năng (Feature Flagging & A/B Testing Infrastructure); hỗ trợ các chiến lược phát hành tính năng linh hoạt (Canary Releases, Tỷ lệ phần trăm người dùng, Lọc theo thuộc tính người dùng), đánh giá ý nghĩa thống kê của thử nghiệm (Statistical Significance / P-Value calculation), và theo dõi số liệu viễn trắc sản phẩm (Product & Performance Metrics Telemetry).

## 2. When to Use
- Khi cần triển khai tính năng mới một cách an toàn mà không cần phụ thuộc vào chu kỳ deploy mã nguồn.
- Khi muốn chạy thử nghiệm 2 phiên bản giao diện thanh toán (Biến thể A vs Biến thể B) để đo lường tỷ lệ chuyển đổi (Conversion Rate).
- Khi phát hành tính năng nặng cho 1% người dùng trước (Canary) để kiểm tra lỗi trước khi mở rộng ra 100%.

## 3. When NOT to Use
- Cấu hình tham số môi trường tĩnh không thay đổi theo người dùng (dùng `.env`).
- Quản lý phân quyền người dùng theo vai trò nghiệp vụ (dùng `dex-access-control-tenancy`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Tên cờ tính năng (Feature Flag Key) và trạng thái mặc định.
- Quy tắc nhắm mục tiêu (Targeting Rules: Nhóm beta testers, quốc gia, tỷ lệ % ngẫu nhiên dựa trên User ID hash).
- Chỉ số mục tiêu cần đo lường (Conversion Rate, Tỷ lệ click, Độ trễ API).

**Điều kiện tiên quyết:**
- Có hệ thống quản lý Feature Flag (PostHog, LaunchDarkly, Unleash, hoặc module cờ tự xây dựng trên Redis).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Giá Trị Mặc Định Luôn Là Trạng Thái An Toàn (Safe Fallback Default)**: Nếu dịch vụ Feature Flag bị mất kết nối hoặc quá thời gian chờ (Timeout), hệ thống phải tự động trả về giá trị an toàn mặc định (thường là `false` - biến thể cũ).
- **Phân Bổ Nhất Quán (Deterministic Assignment)**: Cùng một người dùng đăng nhập trên điện thoại và máy tính phải được chỉ định vào cùng một biến thể thử nghiệm.
- **Cờ Tính Năng Phải Có Hạn Sử Dụng (No Stale Flags)**: Cờ thử nghiệm phải được dọn dẹp khỏi mã nguồn trong vòng 30 ngày sau khi hoàn tất thử nghiệm.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Flag server bị nghẽn làm chậm toàn bộ ứng dụng**: Do gọi HTTP request kiểm tra flag trên mỗi request của khách -> Khắc phục: Sử dụng Local Evaluation SDK với cơ chế streaming/polling đồng bộ định kỳ vào bộ nhớ RAM cục bộ.
- **Người dùng tải lại trang bị nhảy lung tung giữa 2 giao diện**: Do dùng thuật toán random không dựa trên User ID cố định -> Khắc phục: Sử dụng thuật toán MurmurHash3 trên chuỗi `userId + flagKey` modulo 100.

## 6. Step-by-Step Execution Workflow
1. Khai báo cờ tính năng mới trong hệ thống quản lý với mô tả rõ ràng và người sở hữu.
2. Bọc mã nguồn mới bằng câu lệnh điều kiện kiểm tra trạng thái cờ: `if (flags.isEnabled('new-checkout-v2', userContext))`.
3. Triển khai cơ chế băm phân bổ người dùng có tính nhất quán (Consistent Hashing trên `userId + flagKey`): Đảm bảo một người dùng luôn nhìn thấy cùng một biến thể A hoặc B trong suốt phiên trải nghiệm.
4. Gắn thẻ viễn trắc (Telemetry Event Tagging): Mỗi khi sự kiện nghiệp vụ xảy ra (ví dụ: click mua hàng), tự động đính kèm metadata về biến thể cờ hiện tại.
5. Thu thập số liệu và tính toán ý nghĩa thống kê (Kiểm định Chi-squared hoặc T-test) để xác định biến thể chiến thắng với độ tin cậy >= 95%.
6. Lập kế hoạch dọn dẹp cờ (Flag Cleanup): Khi tính năng đã phát hành 100% ổn định, lập tức tạo PR xóa cờ và mã nguồn cũ để tránh nợ kỹ thuật.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// checkout.service.ts - Feature flag controlled flow
export async function processCheckout(cart: Cart, user: User) {
  const isV2Enabled = await featureFlags.evaluate('checkout-redesign-v2', {
    key: user.id,
    attributes: { country: user.country, isBeta: user.isBetaUser }
  });

  if (isV2Enabled) {
    metrics.track('checkout_v2_initiated', { userId: user.id });
    return executeOptimizedCheckoutV2(cart, user);
  }
  return executeLegacyCheckoutV1(cart, user);
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính toán phân bổ hash nhất quán: `npm run test:flag-hashing`
- Kiểm tra trạng thái cờ tính năng qua CLI: `dex flag get new-checkout-v2`
- Đánh giá ý nghĩa thống kê của mẫu thử nghiệm: `python scripts/analyze_experiment.py --flag new-checkout-v2`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Cờ tính năng có logic an toàn dự phòng (Fallback) khi dịch vụ flag gặp sự cố.
- QG-08: Thời gian đánh giá cờ cục bộ trong bộ nhớ diễn ra dưới 1ms (Local In-Memory Evaluation).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Không đưa các thông tin nhạy cảm của người dùng (PII, Mật khẩu) vào payload thuộc tính gửi lên server phân tích cờ.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Cấu hình cờ tính năng và luật phân bổ người dùng.
- Tích hợp cờ vào mã nguồn với mã dự phòng sạch sẽ.
- Báo cáo phân tích số liệu thử nghiệm A/B với chỉ số P-Value cụ thể.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-experimentation-metrics**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
