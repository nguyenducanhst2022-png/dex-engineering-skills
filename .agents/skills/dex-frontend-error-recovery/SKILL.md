---
name: dex-frontend-error-recovery
description: Implement robust frontend error boundaries, optimistic mutation rollbacks, exponential backoff network retries, and contextual fallback states to prevent white-screen crashes. Use when building mission-critical client applications, payment flows, or real-time collaborative editors.
---

# dex-frontend-error-recovery

## 1. Purpose & Scope
Thiết kế và hiện thực hóa cơ chế phục hồi lỗi phía frontend (Frontend Error Recovery) mạnh mẽ; cô lập sự cố bằng React Error Boundaries, hoàn tác cập nhật lạc quan (Optimistic Mutation Rollbacks), tự động thử lại mạng với thuật toán lùi lũy thừa (Exponential Backoff) và ngăn chặn hoàn toàn hiện tượng sập trắng màn hình (White Screen of Death).

## 2. When to Use
- Khi ứng dụng web gặp lỗi ngoại lệ JavaScript chưa được bắt khiến toàn bộ giao diện bị biến mất.
- Khi thực hiện các thao tác quan trọng có rủi ro cao như thanh toán, chuyển tiền hoặc lưu trữ tài liệu trực tuyến.
- Khi kết nối mạng của người dùng thường xuyên chập chờn gây lỗi request thất bại giữa chừng.

## 3. When NOT to Use
- Khi xử lý lỗi cú pháp mã nguồn trong quá trình phát triển (Compile-time error).
- Khi thiết kế cơ chế khôi phục thảm họa cơ sở dữ liệu dưới tầng hạ tầng backend.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư viện quản lý trạng thái, client gửi request HTTP (Fetch/Axios), framework UI hỗ trợ Error Boundaries (React/Vue/Svelte).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Granular Error Boundaries:** Chia nhỏ ranh giới lỗi theo từng phân vùng (Widget Boundary) để lỗi của một widget con không làm sập toàn bộ trang.
- **Optimistic UI Rollback:** Cập nhật giao diện ngay lập tức cho trải nghiệm nhanh, nhưng lưu lại ảnh chụp trạng thái cũ để hoàn tác mượt mà nếu máy chủ trả về lỗi.
- **Exponential Backoff with Jitter:** Tự động gửi lại request sau các khoảng thời gian tăng dần $2^n$ cộng thêm độ trễ ngẫu nhiên để tránh gây nghẽn máy chủ.

## 6. Step-by-Step Execution Workflow
1. Bọc các module độc lập trong các thành phần `ErrorBoundary` chuyên biệt.
2. Thiết kế giao diện Fallback UI thân thiện kèm nút bấm 'Thử lại' (Retry) cho từng khối chức năng.
3. Cài đặt interceptor cho các request mạng để tự động thử lại tối đa 3 lần với thuật toán Exponential Backoff khi gặp mã lỗi 5xx hoặc mất mạng.
4. Lưu trạng thái dự phòng của biểu mẫu vào `sessionStorage` để người dùng không bị mất dữ liệu khi phải tải lại trang.
5. Gửi báo cáo telemetry lỗi chi tiết về máy chủ giám sát.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Robust Exponential Backoff Retry Utility
export async function fetchWithRetry(url: string, options: RequestInit = {}, retries = 3, baseDelayMs = 500): Promise<Response> {
  try {
    const response = await fetch(url, options);
    if (!response.ok && response.status >= 500 && retries > 0) {
      throw new Error(`Server error: ${response.status}`);
    }
    return response;
  } catch (err) {
    if (retries === 0) throw err;
    const delay = baseDelayMs * Math.pow(2, 3 - retries) + Math.random() * 200;
    await new Promise(resolve => setTimeout(resolve, delay));
    return fetchWithRetry(url, options, retries - 1, baseDelayMs);
  }
}
```

## 8. Anti-Patterns & Common Traps
- Bọc một Error Boundary duy nhất ở cấp gốc cao nhất (Root App), khiến bất kỳ lỗi nhỏ nào ở footer cũng làm toàn bộ ứng dụng biến mất.
- Thử lại request mạng liên tục trong vòng lặp vô hạn mà không có thời gian chờ (Infinite Retry Loop) gây quá tải server.
- Nuốt lỗi ngầm (`catch (e) {}`) mà không ghi log telemetry khiến đội ngũ kỹ thuật không biết người dùng đang gặp sự cố.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Không bao giờ xuất hiện hiện tượng 'màn hình trắng' hoàn toàn khi xảy ra lỗi runtime trong bất kỳ component nào.
- QG-02: 100% các thao tác cập nhật lạc quan (Optimistic Updates) có cơ chế hoàn tác dữ liệu chính xác khi request thất bại.
- QG-03: Lỗi ngoại lệ được báo cáo tự động về dịch vụ theo dõi kèm đầy đủ stack trace và ngữ cảnh người dùng.

## 10. Security & Safety Boundaries
- Không hiển thị stack trace kỹ thuật chi tiết chứa đường dẫn máy chủ hoặc thông tin nội bộ trên giao diện Fallback của người dùng cuối.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bộ component React `GranularErrorBoundary.tsx`.
1. Thư viện gửi request có tự phục hồi `fetchWithRetry.ts`.

## 13. Related & Complementary Skills
- [`dex-reliability-engineering`](.agents/skills/dex-reliability-engineering/SKILL.md)
- [`dex-ui-component-contracts`](.agents/skills/dex-ui-component-contracts/SKILL.md)
- [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Người dùng đang nhập biểu mẫu thanh toán thẻ tín dụng thì kết nối mạng bị rớt tạm thời trong 1 giây. Nhờ `dex-frontend-error-recovery`, ứng dụng tự động thử lại request với độ trễ lũy thừa mà không làm mất thông tin người dùng đã nhập, hoàn tất thanh toán thành công mà người dùng không nhận thấy sự gián đoạn.
