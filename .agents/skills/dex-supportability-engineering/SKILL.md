---
name: dex-supportability-engineering
description: Design, instrument, and automate user-facing self-service diagnostics, actionable error states, debug bundles, and supportability runbooks. Use to empower users to self-resolve issues and slash support escalations.
---

# dex-supportability-engineering

## 1. Purpose & Scope
Thiết kế, xây dựng và tự động hóa các công cụ chẩn đoán tự phục vụ hướng tới người dùng (Supportability Engineering: User-facing Self-Service Diagnostics, Actionable Error Messages, Diagnostic Bundles Export, Tracing IDs); trao quyền cho người dùng tự xử lý sự cố, hỗ trợ đội ngũ Chăm sóc khách hàng (Support Tier 1/2) điều tra nhanh chóng và cắt giảm tối đa các ca chuyển cấp (escalations) lên đội ngũ kỹ sư phần mềm.

## 2. When to Use
- Đội ngũ kỹ sư liên tục bị ngắt quãng công việc để điều tra các lỗi của khách hàng mà không có đủ thông tin hoặc log.
- Thông báo lỗi trên ứng dụng hiển thị chung chung kiểu 'Đã có lỗi xảy ra' khiến người dùng bối rối và gọi điện tổng đài.
- Khách hàng doanh nghiệp yêu cầu công cụ kiểm tra sức khỏe kết nối hệ thống (System Self-Test tool) tại chỗ.

## 3. When NOT to Use
- Không hiển thị thông tin nhạy cảm của hệ thống (như Database Connection String, Server Internal IP, Raw Stack Traces) trực tiếp lên màn hình người dùng.
- Không để các công cụ chẩn đoán tự phục vụ trở nên quá phức tạp đối với người dùng không chuyên về kỹ thuật.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Lịch sử các ticket hỗ trợ phổ biến nhất từ Zendesk/Intercom.
- Các mã lỗi định danh chuẩn hóa (Machine-readable Error Codes).
- Thông tin ngữ cảnh phiên làm việc của người dùng (Session ID, Correlation ID, App Version).
- **Điều kiện tiên quyết**:
- Hệ thống có cơ chế tạo mã định danh truy vết duy nhất (Trace ID / Request ID) cho mỗi yêu cầu.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Actionable Error Messages: Một thông báo lỗi đạt chuẩn phải chứa 3 thành phần:
  1. Chuyện gì đã xảy ra (bằng ngôn ngữ đời thường, không dùng mã kỹ thuật).
  2. Tại sao nó xảy ra (nguyên nhân có thể).
  3. Hành động người dùng có thể làm tiếp theo để tự khắc phục (nút 'Thử lại', link 'Kiểm tra mạng', hoặc số hotline).
- One-Click Diagnostic Bundle: Nút bấm cho phép người dùng xuất file nén chứa log ẩn danh, thông số cấu hình mạng và thông tin phần cứng để gửi cho đội kỹ thuật khi cần hỗ trợ sâu.
- Self-Service Connectivity Tester: Trang kiểm tra tự động xem máy khách có bị chặn tường lửa tới các server API hoặc WebSocket của công ty hay không.
- **Quy tắc quyết định kỹ thuật**:
- 100% màn hình báo lỗi bắt buộc phải hiển thị mã `Support ID` (tương ứng với Trace ID trong log) kèm nút bấm 'Copy mã lỗi'.
- Mọi lỗi do người dùng (Client-side error: sai định dạng, quá hạn mức) phải hướng dẫn cách sửa ngay tại chỗ.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Hiển thị trang trắng xóa (White Screen of Death) hoặc màn hình crash không có nút quay lại, buộc người dùng phải gỡ ứng dụng cài lại.

## 6. Step-by-Step Execution Workflow
1. Rà soát danh sách 20 lý do hàng đầu khiến người dùng phải mở ticket hỗ trợ.
2. Chuẩn hóa danh mục mã lỗi toàn hệ thống kèm bài viết giải thích chi tiết trong Help Center.
3. Xây dựng màn hình Error Boundary trên Frontend hiển thị đầy đủ Trace ID và nút tự sửa lỗi.
4. Tích hợp tính năng xuất Diagnostic Bundle an toàn vào mục Cài đặt của ứng dụng.
5. Xây dựng tài liệu hướng dẫn xử lý (Support Runbook) cho nhân viên Chăm sóc khách hàng.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// React Error Boundary hiển thị thông báo lỗi thân thiện kèm Support ID
export function ErrorFallback({ error, resetErrorBoundary }: any) {
  const supportId = window.__CORRELATION_ID__ || 'N/A';

  return (
    <div className="error-container">
      <h2>Không thể tải dữ liệu đơn hàng</h2>
      <p>Kết nối mạng của bạn có thể đang bị gián đoạn hoặc máy chủ đang bảo trì ngắn hạn.</p>
      <div className="action-buttons">
        <button onClick={resetErrorBoundary} className="btn-retry">Thử tải lại</button>
        <a href="/network-test" className="btn-test">Kiểm tra đường truyền</a>
      </div>
      <div className="support-meta">
        <span>Mã hỗ trợ: <code>{supportId}</code></span>
        <button onClick={() => navigator.clipboard.writeText(supportId)}>Copy mã</button>
      </div>
    </div>
  );
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm thử tự động kích hoạt Error Boundary và xác minh hiển thị Support ID
npx playwright test tests/supportability/error-boundary.spec.ts
```

## 8. Anti-Patterns & Common Traps
- Hiển thị mã lỗi HTTP trần trụi như 'Lỗi 500' mà không kèm theo bất kỳ giải thích nào.
- Bắt khách hàng đọc từng dòng log qua điện thoại thay vì cung cấp nút xuất file chẩn đoán tự động.

## 9. Quality Gates & Acceptance Criteria
- Giảm 40% số lượng ticket hỗ trợ liên quan đến các lỗi kết nối mạng và cấu hình thông thường.
- 100% màn hình lỗi có chứa Correlation ID hợp lệ tương ứng với hệ thống Distributed Tracing.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- File Diagnostic Bundle trước khi xuất phải tự động bôi đen (Sanitize) toàn bộ mật khẩu, tokens và thông tin nhạy cảm của khách hàng.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Thành phần UI Error Boundary chuẩn hóa kèm Trace ID.
- Bộ công cụ tự chẩn đoán kết nối mạng (Network Self-Test Component) và Support Runbooks.

## 13. Related & Complementary Skills
dex-user-journey-mapping, dex-alert-quality-engineering, dex-distributed-tracing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng hội nghị truyền hình B2B thường xuyên nhận hàng trăm cuộc gọi phàn nàn 'Không kết nối được phòng họp'. Nhóm Supportability Engineering đã bổ sung nút 'Kiểm tra đường truyền trước khi vào họp': hệ thống tự động kiểm tra Micro, Camera, và cổng kết nối tường lửa WebRTC trong 3 giây và chỉ ra chính xác 'Cổng 3478 của công ty bạn đang bị chặn'. Nhờ tính năng này, 70% người dùng tự liên hệ IT nội bộ mở cổng, giúp giảm 65% áp lực cho đội ngũ tổng đài.
