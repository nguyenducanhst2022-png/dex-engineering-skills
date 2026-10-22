---
name: dex-javascript-sourcemap-recovery
description: Reconstruct original TypeScript/JavaScript source trees from production sourcemap files (.map), analyze bundle composition, and detect inadvertently exposed private API keys or internal test endpoints. Use when auditing public web assets for data leakage or diagnosing production client errors. (Strictly authorized/defensive).
---

# dex-javascript-sourcemap-recovery

## 1. Purpose & Scope
Khôi phục lại cây cấu trúc thư mục và mã nguồn TypeScript/JavaScript gốc từ các tệp Source Map (`.map`) vô tình bị để lộ trên môi trường sản xuất; phân tích thành phần gói đóng gói (Bundle Composition), phát hiện rò rỉ khóa bí mật (API Keys), thông tin cấu hình nhạy cảm và các đường dẫn endpoint thử nghiệm nội bộ; phục vụ kiểm toán phòng thủ rò rỉ dữ liệu web.

## 2. When to Use
- Khi kiểm toán an ninh bề mặt tấn công bên ngoài (External Attack Surface) của website doanh nghiệp.
- Khi điều tra một lỗi sập client trên production cần đối chiếu với dòng mã nguồn gốc.
- Khi xác minh xem quy trình đóng gói CI/CD có vô tình đẩy các tệp `.map` bí mật lên CDN công khai hay không.

## 3. When NOT to Use
- Khi cố tình khai thác để đánh cắp sở hữu trí tuệ của các tổ chức khác mà không có sự ủy quyền kiểm toán.
- Khi phân tích các tệp nhị phân đã biên dịch sang mã máy C++.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Đường dẫn tệp JavaScript đóng gói và tệp `.map` tương ứng, công cụ phục hồi `source-map` hoặc script Python/Node.js.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **VLQ (Variable-Length Quantity) Encoding:** Giải thuật nén ánh xạ từng dòng và cột giữa mã nguồn đã nén (Minified) và mã nguồn gốc.
- **Source Map Sources Content:** Mảng `sourcesContent` bên trong file `.map` thường chứa toàn bộ 100% nội dung mã nguồn gốc chưa nén.
- **Information Leakage Risk:** Tệp sourcemap có thể để lộ chú thích mã nguồn, thông tin tác giả, biến môi trường nhúng và cấu trúc thư mục nội bộ.

## 6. Step-by-Step Execution Workflow
1. Kiểm tra sự tồn tại của header `SourceMap` hoặc chú thích `//# sourceMappingURL=` trong tệp JS.
2. Tải và phân tích cú pháp tệp JSON của sourcemap.
3. Trích xuất mảng `sources` và `sourcesContent` để tái tạo lại toàn bộ cây thư mục mã nguồn gốc.
4. Quét tự động toàn bộ mã nguồn vừa khôi phục bằng công cụ Secret Scanner (như TruffleHog) để tìm khóa API bị lộ.
5. Lập biên bản báo cáo rò rỉ và đề xuất biện pháp chặn tệp `.map` trên máy chủ web.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Defensive Sourcemap Extractor Script
import fs from 'fs';
import path from 'path';

export function extractSourceMap(mapFilePath: string, outputDir: string) {
  const mapData = JSON.parse(fs.readFileSync(mapFilePath, 'utf-8'));
  const { sources, sourcesContent } = mapData;

  if (!sourcesContent) {
    console.warn('Sourcemap contains paths but no sourcesContent.');
    return;
  }

  sources.forEach((sourcePath: string, index: number) => {
    const cleanPath = sourcePath.replace(/^webpack:\/\//, '').replace(/^\.\//, '');
    const fullOutPath = path.join(outputDir, cleanPath);
    
    fs.mkdirSync(path.dirname(fullOutPath), { recursive: true });
    fs.writeFileSync(fullOutPath, sourcesContent[index] || '', 'utf-8');
  });
  console.log(`Reconstructed ${sources.length} original source files into ${outputDir}`);
}
```

## 8. Anti-Patterns & Common Traps
- Đẩy tệp sourcemap lên server web công khai mà không thiết lập xác thực hoặc hạn chế IP truy cập.
- Nhúng các token bảo mật thật vào tệp cấu hình frontend trong quá trình build rồi dựa vào việc nén mã (minification) để giấu.
- Không xóa các tài liệu nhạy cảm hoặc comment nội bộ trước khi xuất bản bản dựng ra công chúng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Phát hiện và cảnh báo 100% các tệp sourcemap bị phơi bày công khai trên CDN môi trường sản xuất.
- QG-02: Không tìm thấy bất kỳ secret key, password hoặc token nhạy cảm nào trong mã nguồn khôi phục được.
- QG-03: Cấu hình CI/CD được cập nhật để tự động tách biệt tệp `.map` vào hệ thống theo dõi lỗi nội bộ (Sentry).

## 10. Security & Safety Boundaries
- Thông báo ngay lập tức cho đội ngũ an ninh thông tin khi phát hiện khóa API quản trị bị lộ trong tệp sourcemap công khai.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm toán rò rỉ mã nguồn `SOURCEMAP_LEAKAGE_AUDIT.md`.
1. Script tự động kiểm tra sự tồn tại của sourcemap trên đường ống triển khai.

## 13. Related & Complementary Skills
- [`dex-javascript-bundle-deobfuscation`](.agents/skills/dex-javascript-bundle-deobfuscation/SKILL.md)
- [`dex-secrets-management`](.agents/skills/dex-secrets-management/SKILL.md)
- [`dex-security-audit`](.agents/skills/dex-security-audit/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kiểm toán an ninh website thanh toán trước đợt kiểm tra PCI-DSS. Kỹ sư kích hoạt `dex-javascript-sourcemap-recovery`, phát hiện tệp `main.bundle.js.map` vẫn đang mở công khai trên CDN, chứa toàn bộ mã nguồn TypeScript gốc và một token Stripe Test Secret Key bị bỏ quên trong mã, giúp doanh nghiệp thu hồi token và khóa file map kịp thời.
