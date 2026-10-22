---
name: dex-headless-ui-verification
description: Detect and reconcile behavioral and visual discrepancies between headless browser runners (Linux CI) and actual user graphical browsers (Windows/macOS) including font subpixel antialiasing and GPU acceleration flags. Use when debugging CI-only test failures, font rendering shifts, or canvas test flakes.
---

# dex-headless-ui-verification

## 1. Purpose & Scope
Phát hiện, đối chiếu và đồng nhất hóa các sai lệch về mặt hiển thị và hành vi giữa trình duyệt chạy không giao diện (Headless Browsers trên môi trường Linux CI) và trình duyệt có giao diện thực tế của người dùng (Headed Browsers trên Windows/macOS); xử lý các vấn đề khử răng cưa phông chữ (Subpixel Antialiasing), cờ tăng tốc phần cứng GPU và kích thước viewport ảo.

## 2. When to Use
- Khi các bài kiểm thử hình ảnh (Visual Regression Tests) chạy PASS trên máy cá nhân nhưng luôn bị FAIL trên GitHub Actions CI.
- Khi font chữ hiển thị trên Linux CI bị lệch vài pixel so với bản thiết kế trên macOS/Windows.
- Khi kiểm tra các thành phần giao diện sử dụng Canvas hoặc WebGL trong môi trường headless.

## 3. When NOT to Use
- Khi chỉ chạy các bài kiểm thử unit test logic không có liên quan đến hiển thị trình duyệt.
- Khi kiểm thử hiệu năng API máy chủ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Môi trường Docker/Linux CI, cài đặt gói font chuẩn (Noto Sans, Roboto), cờ cấu hình trình duyệt Chromium/Playwright.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Headless Mode Discrepancies:** Chế độ `--headless=new` hiện đại của Chromium gần gũi với trình duyệt thật hơn so với cờ headless cũ, nhưng vẫn thiếu GPU phần cứng thật.
- **Font Rasterization Differences:** Linux FreeType hiển thị chữ khác biệt nhẹ so với DirectWrite (Windows) và CoreText (macOS).
- **Software Rendering Override:** Sử dụng cờ `--use-gl=angle` hoặc SwiftShader để mô phỏng kết xuất đồ họa trên môi trường không có card đồ họa vật lý.

## 6. Step-by-Step Execution Workflow
1. Đồng bộ hóa môi trường chạy kiểm thử hình ảnh bằng một Docker container chuẩn hóa chứa đầy đủ bộ phông chữ hệ thống.
2. Kích hoạt cờ trình duyệt `--headless=new` thay vì cờ headless cũ.
3. Cấu hình cờ vô hiệu hóa sự khác biệt khử răng cưa của phông chữ (`--font-render-hinting=none`).
4. Thiết lập độ dung sai hình ảnh (Threshold Tolerance) phù hợp (ví dụ 0.2% đến 0.5% số pixel khác biệt).
5. Chạy thử nghiệm so khớp ảnh trên cả máy trạm cục bộ và máy chủ CI để xác nhận tính nhất quán.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Deterministic Headless Browser Configuration
import { chromium, LaunchOptions } from 'playwright';

export const deterministicBrowserConfig: LaunchOptions = {
  headless: true,
  args: [
    '--headless=new',
    '--disable-gpu',
    '--font-render-hinting=none',
    '--disable-skia-runtime-opts',
    '--disable-font-subpixel-positioning',
    '--force-color-profile=srgb',
  ],
};
```

## 8. Anti-Patterns & Common Traps
- Chạy visual regression test trực tiếp trên hệ điều hành của lập trình viên mà không qua Docker, khiến mỗi người tạo ra một bản ảnh mẫu (snapshot) khác nhau.
- Đặt độ dung sai sai khác pixel bằng 0% tuyệt đối giữa các hệ điều hành khác nhau.
- Quên cài đặt các gói font cơ bản trên máy chủ Linux CI khiến trình duyệt phải fallback về font chữ xấu xí làm sai lệch bố cục.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các bài visual regression test chạy ổn định và đồng nhất giữa máy trạm cá nhân và server CI.
- QG-02: Bộ container kiểm thử tích hợp đầy đủ các gói font chuẩn hóa và cờ khử răng cưa.
- QG-03: Không có ca kiểm thử nào thất bại chỉ vì lý do sai khác khử răng cưa phông chữ ở mức vi mô.

## 10. Security & Safety Boundaries
- Đảm bảo các container chạy headless browser không chạy dưới quyền `root` mà không có sandbox bảo vệ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Cấu hình Dockerfile chuẩn hóa cho CI visual testing `ci-runner.Dockerfile`.
1. Module khởi tạo trình duyệt với cờ khử sai lệch `deterministicBrowserConfig.ts`.

## 13. Related & Complementary Skills
- [`dex-visual-regression`](.agents/skills/dex-visual-regression/SKILL.md)
- [`dex-browser-automation-testing`](.agents/skills/dex-browser-automation-testing/SKILL.md)
- [`dex-compatibility-matrix-testing`](.agents/skills/dex-compatibility-matrix-testing/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Đội ngũ kỹ thuật bực bội vì các pull request liên tục bị chặn lại bởi lỗi visual test lệch 0.1% font chữ trên GitHub Actions. Kỹ sư kích hoạt `dex-headless-ui-verification`, chuẩn hóa môi trường runner bằng Docker container chứa font Noto Sans và cờ `--font-render-hinting=none`, đưa tỷ lệ pass test trên CI lên 100%.
