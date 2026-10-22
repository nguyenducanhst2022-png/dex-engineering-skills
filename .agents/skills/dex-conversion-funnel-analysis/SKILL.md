---
name: dex-conversion-funnel-analysis
description: Instrument, analyze, and optimize conversion funnels, drop-off rates, and user friction across acquisition, activation, and checkout flows using event schemas and cohort analytics. Use when identifying revenue leaks in product funnels.
---

# dex-conversion-funnel-analysis

## 1. Purpose & Scope
Thiết lập công cụ đo lường (Event Instrumentation), phân tích và tối ưu hóa phễu chuyển đổi (Conversion Funnel Analysis); xác định chính xác các điểm rò rỉ doanh thu, các bước có tỉ lệ bỏ cuộc (Drop-off Rates) cao bất thường trong luồng kích hoạt và thanh toán thông qua dữ liệu phân tích sự kiện (Event-driven Analytics) và phân tích nhóm thuần tập (Cohort Analysis).

## 2. When to Use
- Doanh thu hoặc tỉ lệ đăng ký thành viên mới sụt giảm mà không rõ nguyên nhân ở bước nào.
- Vừa ra mắt luồng giao diện mới và cần đo lường xem tỉ lệ chuyển đổi tăng hay giảm so với luồng cũ.
- Chuẩn bị chạy chiến dịch tiếp thị lớn và cần bảo đảm phễu chuyển đổi hoạt động tối ưu không bị nghẽn.

## 3. When NOT to Use
- Không phân tích phễu dựa trên dữ liệu sự kiện bị gửi trùng lặp hoặc thiếu định danh người dùng nhất quán.
- Không đưa ra kết luận vội vã khi kích thước mẫu dữ liệu (Sample Size) còn quá nhỏ chưa đủ ý nghĩa thống kê.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Lược đồ sự kiện phân tích (Analytics Event Schema: Track calls, Pageviews).
- Dữ liệu phễu từ công cụ phân tích (Mixpanel, Amplitude, PostHog, BigQuery).
- Các thuộc tính phân đoạn (Segmentation properties: Thiết bị, Quốc gia, Trình duyệt).
- **Điều kiện tiên quyết**:
- Các sự kiện tracking đã được gắn thẻ và kiểm tra tính hợp lệ trên môi trường production.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Phễu chuyển đổi tuần tự (Strict Order Funnel): Người dùng phải hoàn thành lần lượt: Bước 1 (Xem sản phẩm) -> Bước 2 (Thêm vào giỏ) -> Bước 3 (Bắt đầu thanh toán) -> Bước 4 (Thanh toán thành công) trong một khung thời gian nhất định (ví dụ 24 giờ).
- Drop-off Point: Bước có độ dốc giảm mạnh nhất trong phễu. Ví dụ: 10,000 người vào bước 2 nhưng chỉ có 1,500 người sang bước 3 (tỉ lệ rớt 85%) => Điểm nóng cần điều tra lỗi kỹ thuật hoặc rào cản UX.
- Event Schema Hygiene: Đặt tên sự kiện chuẩn theo công thức `Object + Action` (ví dụ: `Order_Completed`, `Cart_Item_Added`), tránh tình trạng lộn xộn giữa chữ hoa, chữ thường và dấu gạch dưới.
- **Quy tắc quyết định kỹ thuật**:
- Nếu tỉ lệ drop-off tại một bước kỹ thuật tăng vọt > 15% sau một bản release: gắn cờ nghi ngờ có bug kỹ thuật và điều tra log ngay lập tức.
- Bắt buộc phân tích phễu tách biệt theo nền tảng (iOS vs Android vs Web) để tránh số liệu nền tảng này che giấu lỗi của nền tảng kia.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Lập trình viên gắn sai vị trí bắn sự kiện `Order_Completed` vào nút bấm 'Đặt hàng' thay vì gắn tại trang xác nhận thanh toán thành công, khiến số liệu báo cáo doanh thu bị ảo.

## 6. Step-by-Step Execution Workflow
1. Thiết kế bảng theo dõi sự kiện (Tracking Plan) định rõ từng bước của phễu và các thuộc tính đi kèm.
2. Triển khai mã nguồn tracking chuẩn hóa phía Client và Server.
3. Xây dựng biểu đồ phễu trên công cụ phân tích (PostHog/Amplitude).
4. Phân đoạn dữ liệu theo loại thiết bị, tốc độ mạng và nguồn truy cập để tìm điểm bất thường.
5. Đề xuất các cải tiến kỹ thuật (ví dụ: giảm số trường nhập liệu, tối ưu tốc độ tải) và kiểm chứng lại sau 2 tuần.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// Mã nguồn tracking sự kiện chuẩn hóa TypeScript
interface CheckoutStartedProperties {
  cart_id: string;
  total_value: number;
  item_count: number;
  payment_method_selected: string;
}

export function trackCheckoutStep(stepNumber: number, props: CheckoutStartedProperties) {
  analytics.track('Checkout_Step_Completed', {
    step: stepNumber,
    timestamp: new Date().toISOString(),
    ...props
  });
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm toán tính hợp lệ của schema sự kiện tracking bằng Avo CLI
npx avo pull --check
```

## 8. Anti-Patterns & Common Traps
- Đổi tên sự kiện tùy tiện trong code làm đứt gãy toàn bộ biểu đồ phễu lịch sử trên dashboard.
- Bắn sự kiện tracking ở phía client mà không xử lý trường hợp người dùng cài đặt Ad-blocker chặn mất request.

## 9. Quality Gates & Acceptance Criteria
- 100% các bước chính trong luồng thanh toán đều có sự kiện tracking tương ứng.
- Độ sai lệch dữ liệu sự kiện giữa Client Analytics và Server Database dưới 2%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Tuyệt đối cấm đưa thông tin thẻ tín dụng (CVV, PAN) hoặc mật khẩu vào thuộc tính của sự kiện tracking.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Bảng kế hoạch theo dõi sự kiện (Event Tracking Plan Schema).
- Báo cáo phân tích phễu chuyển đổi và danh sách các điểm rò rỉ cần khắc phục.

## 13. Related & Complementary Skills
dex-feature-adoption-analysis, dex-user-journey-mapping, dex-product-requirements-writing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một sàn thương mại điện tử nhận thấy tỉ lệ hoàn tất thanh toán trên Web Mobile thấp hơn 40% so với iOS App. Phân tích sâu phễu chuyển đổi theo từng trường form, họ phát hiện 70% người dùng trên Android bị rớt ở bước nhập 'Mã bưu chính' do bàn phím số không tự bật lên. Đổi thuộc tính input sang `type="numeric" inputmode="numeric"` đã giúp tỉ lệ hoàn thành đơn hàng tăng thêm 18%, mang về thêm $250,000 doanh thu mỗi tháng.
