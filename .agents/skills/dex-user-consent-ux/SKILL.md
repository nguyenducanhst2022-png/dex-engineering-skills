---
name: dex-user-consent-ux
description: Design, implement, and audit transparent, accessible, and compliant user consent flows and privacy controls (GDPR, CCPA, Cookie banners) avoiding dark patterns. Use when capturing consent for cookies, tracking, or AI data usage.
---

# dex-user-consent-ux

## 1. Purpose & Scope
Thiết kế, xây dựng và kiểm toán các luồng thu thập sự đồng thuận của người dùng (User Consent Flows) và giao diện kiểm soát quyền riêng tư (Privacy Preferences Controls: GDPR, CCPA, ePrivacy Directive, Cookie Banners); loại bỏ hoàn toàn các thủ thuật lừa hướng (Dark Patterns), bảo đảm tính minh bạch, khả năng tiếp cận và cho phép người dùng rút lại quyền đồng thuận một cách dễ dàng.

## 2. When to Use
- Triển khai cookie banner hoặc hộp thoại xin quyền thu thập dữ liệu trên ứng dụng web/mobile.
- Thu thập sự đồng thuận của người dùng cho việc sử dụng dữ liệu cá nhân để huấn luyện các mô hình AI.
- Chuẩn bị cho kỳ rà soát tuân thủ pháp lý về quyền riêng tư dữ liệu quốc tế.

## 3. When NOT to Use
- Không sử dụng các thiết kế lừa dối (Dark Patterns: nút 'Đồng ý' to màu xanh nổi bật trong khi nút 'Từ chối' là chữ xám tí hon bị ẩn sâu).
- Không ngầm mặc định tích sẵn các ô checkbox đồng thuận (Pre-ticked checkboxes là hành vi phạm luật GDPR nghiêm trọng).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh mục các loại cookie và dữ liệu theo dõi được sử dụng (Cần thiết, Phân tích, Quảng cáo).
- Yêu cầu pháp lý khu vực mục tiêu (GDPR tại EU, CCPA tại California).
- Nền tảng quản lý sự đồng thuận (OneTrust, Cookiebot hoặc giải pháp tự xây dựng).
- **Điều kiện tiên quyết**:
- Có khả năng chặn (Block) việc nạp các script bên thứ ba (Google Analytics, Meta Pixel) cho đến khi người dùng chủ động bấm đồng ý.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Điều kiện hợp lệ của sự đồng thuận theo GDPR: Tự do (Freely given), Cụ thể (Specific), Được thông báo rõ ràng (Informed), Rõ ràng không mập mờ (Unambiguous affirmative action).
- Equal Prominence: Nút 'Từ chối tất cả' (Reject All) phải có kích thước, vị trí và độ tương phản ngang hàng với nút 'Chấp nhận tất cả' (Accept All).
- Granular Consent: Cho phép người dùng tùy chọn bật/tắt riêng rẽ từng mục đích sử dụng (ví dụ: cho phép Cookies chức năng nhưng cấm Cookies tiếp thị).
- **Quy tắc quyết định kỹ thuật**:
- Mọi script phân tích và tiếp thị bắt buộc phải bị chặn nạp (Zero-cookie policy) cho đến khi nhận được tín hiệu đồng thuận từ người dùng.
- Phải cung cấp liên kết 'Cài đặt quyền riêng tư' thường trực ở chân trang (Footer) để người dùng có thể đổi ý bất kỳ lúc nào.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Hệ thống vẫn âm thầm gửi dữ liệu tracking về máy chủ trước khi người dùng kịp nhìn thấy hoặc bấm chọn trên banner đồng thuận.

## 6. Step-by-Step Execution Workflow
1. Phân loại toàn bộ các cookies và script bên thứ ba trong ứng dụng.
2. Thiết kế giao diện hộp thoại xin quyền với nút Chấp nhận và Từ chối ngang bằng nhau.
3. Cấu hình cơ chế Conditional Script Loading dựa trên trạng thái đồng thuận lưu trong LocalStorage.
4. Xây dựng trang quản lý tùy chọn quyền riêng tư chi tiết cho người dùng.
5. Kiểm tra tự động bằng Playwright để chứng minh không có cookie theo dõi nào được tạo ra khi bấm 'Từ chối'.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// Quản lý trạng thái đồng thuận và nạp script có điều kiện
interface UserConsent {
  necessary: boolean; // Luôn luôn là true
  analytics: boolean;
  marketing: boolean;
}

export function applyConsent(consent: UserConsent) {
  localStorage.setItem('user_consent_preferences', JSON.stringify(consent));
  
  if (consent.analytics) {
    loadGoogleAnalytics();
  } else {
    unloadAnalyticsCookies();
  }
  
  if (consent.marketing) {
    loadMetaPixel();
  }
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm thử tự động chứng minh không có network request tracking khi bấm Reject
npx playwright test tests/privacy/consent-flow.spec.ts
```

## 8. Anti-Patterns & Common Traps
- Làm mờ toàn bộ màn hình và bắt buộc người dùng phải bấm đồng ý mới cho đọc nội dung (Cookie Wall vi phạm luật EU).
- Làm cho nút 'Từ chối' trở nên cực kỳ khó tìm hoặc bắt người dùng phải bấm qua 10 bước cài đặt phức tạp.

## 9. Quality Gates & Acceptance Criteria
- 0 script theo dõi nào được phép chạy trước khi có sự đồng thuận chủ động của người dùng.
- Đạt 100% tiêu chí tuân thủ kiểm tra Dark Patterns theo hướng dẫn của EDPB (European Data Protection Board).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Lưu trữ bản ghi chứng nhận đồng thuận (Consent Audit Log) có mã hóa để phục vụ việc thanh tra pháp lý.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Module giao diện Cookie Consent Banner chuẩn mực.
- Bộ test E2E kiểm chứng việc chặn script tracking khi từ chối.

## 13. Related & Complementary Skills
dex-accessibility-automation, dex-user-journey-mapping, dex-feature-adoption-analysis

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty SaaS tại Việt Nam mở rộng thị trường sang Đức và bị cơ quan bảo vệ dữ liệu địa phương cảnh báo phạt vì Cookie Banner không có nút 'Từ chối tất cả'. Đội ngũ đã tái thiết kế lại giao diện Consent UX minh bạch, nút Chấp nhận và Từ chối hiển thị song song rõ ràng và tích hợp cơ chế chặn script chặt chẽ, giúp công ty tuân thủ 100% luật GDPR và tạo dựng niềm tin vững chắc với khách hàng Châu Âu.
