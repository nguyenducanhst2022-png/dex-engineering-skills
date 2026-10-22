---
name: dex-visual-regression
description: Automate visual regression testing, pixel-diff comparisons, responsive viewport snapshots, and UI baseline management with Playwright/Percy. Use when preventing unintended UI styling breakages or verifying design system refactors.
---

# dex-visual-regression

## 1. Purpose & Scope
Thiết lập hệ thống kiểm thử hồi quy thị giác (Visual Regression Testing) tự động; chụp ảnh chụp nhanh (Pixel-diff Snapshots) các thành phần giao diện trên nhiều độ phân giải màn hình khác nhau, phát hiện lập tức bất kỳ sự xê dịch layout, sai lệch màu sắc hay lỗi CSS nào trước khi merge mã nguồn.

## 2. When to Use
- Khi tái cấu trúc CSS toàn cục, nâng cấp thư viện Tailwind / Bootstrap, hoặc cập nhật Design Tokens.
- Khi phát triển các component quan trọng trong Design System cần đảm bảo độ chính xác pixel từng milimet.
- Khi một lỗi hiển thị giao diện nghiêm trọng bị lọt lên production do không có unit test nào bắt được lỗi CSS.

## 3. When NOT to Use
- Kiểm thử các component có chứa nội dung thời gian thay đổi liên tục (đồng hồ đếm ngược, dữ liệu ngẫu nhiên) mà không mock dữ liệu tĩnh.
- Kiểm thử logic xử lý nghiệp vụ API hoặc database.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các trang hoặc component quan trọng cần chụp snapshot.
- Ma trận độ phân giải (Mobile 375x667, Tablet 768x1024, Desktop 1280x800).
- Công cụ kiểm thử (Playwright Test, Percy, Loki, Chromatic).

**Điều kiện tiên quyết:**
- Có môi trường chạy trình duyệt headless nhất quán (Docker container hoặc Linux CI runner) để tránh sai lệch font chữ giữa Windows và macOS.
- Tất cả animation, video, GIF đều có cơ chế đóng băng (Freeze animations / `animation-play-state: paused`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Ngưỡng Sai Số Chặt Chẽ (Tolerance)**: Đặt `maxDiffPixelRatio` ở mức 0.005 - 0.01 (tối đa 0.5% - 1% pixel sai lệch do render vi mô).
- **Đồng Bộ Môi Trường CI**: Tuyệt đối không so sánh ảnh chụp trên Windows với ảnh chụp trên Ubuntu của GitHub Actions vì engine render font chữ khác nhau sẽ làm rớt test giả tạo.
- **Che Vùng Động**: Sử dụng mask (`mask: [page.locator('.dynamic-ad')]`) để che đi các vùng quảng cáo hoặc avatar người dùng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Test rớt hàng loạt do font chữ hệ điều hành**: Chạy test trên máy dev Windows pass nhưng lên CI Linux thì fail vì lệch font -> Khắc phục: Chạy visual regression trong Docker container chuẩn hóa `mcr.microsoft.com/playwright`.
- **Test rớt do animation chưa chạy xong**: Ảnh chụp lúc button đang fade-in nửa chừng -> Khắc phục: Đợi network idle và đợi selector chuyển sang trạng thái ổn định.

## 6. Step-by-Step Execution Workflow
1. Thiết lập kịch bản Playwright kiểm thử snapshot cho các thành phần UI trọng yếu.
2. Cấu hình mock dữ liệu tĩnh 100% để loại bỏ tính ngẫu nhiên.
3. Vô hiệu hóa animation và con trỏ nhấp nháy bằng CSS helper: `*, *::before { transition: none !important; animation: none !important; }`.
4. Chạy tạo ảnh chuẩn ban đầu (Baseline Snapshots): `npx playwright test --update-snapshots`.
5. Khi có thay đổi code: Chạy lệnh so sánh pixel-diff; nếu độ lệch vượt quá ngưỡng cho phép (ví dụ `maxDiffPixelRatio: 0.01`), bài test sẽ FAIL và xuất ảnh diff nổi bật vùng sai lệch màu đỏ.
6. Đánh giá vùng diff: Nếu thay đổi là cố ý -> Cập nhật baseline. Nếu là lỗi ngoài ý muốn -> Sửa CSS.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// tests/visual/button.spec.ts
test('nút bấm primary giữ nguyên giao diện chuẩn', async ({ page }) => {
  await page.goto('/components/button');
  const button = page.getByRole('button', { name: 'Thanh toán' });
  await expect(button).toHaveScreenshot('button-primary-default.png', {
    maxDiffPixelRatio: 0.005,
    animations: 'disabled'
  });
});
```

### Lệnh xác minh & thực thi:
- Chạy kiểm thử visual regression: `npx playwright test tests/visual/`
- Cập nhật ảnh chụp chuẩn: `npx playwright test tests/visual/ --update-snapshots`
- Xem báo cáo trực quan kèm ảnh so sánh: `npx playwright show-report`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-05: 100% các bài visual regression test đạt PASS trên môi trường CI chuẩn hóa.
- QG-08: Nếu có ảnh snapshot thay đổi trong Git diff, bắt buộc phải có giải thích rõ lý do thay đổi giao diện trong mô tả PR.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Đảm bảo dữ liệu hiển thị trên các ảnh chụp snapshot không chứa thông tin cá nhân (PII) thật của khách hàng.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Bộ kịch bản kiểm thử snapshot (`tests/visual/components.spec.ts`).
- Thư mục lưu trữ ảnh chụp chuẩn baseline (`tests/visual/__snapshots__/`).
- Báo cáo HTML trực quan hiển thị các vùng pixel bị lệch màu sắc.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-visual-regression**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
