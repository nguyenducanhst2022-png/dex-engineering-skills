---
name: dex-javascript-bundle-deobfuscation
description: Analyze and deobfuscate minified client-side JavaScript and Electron bundles, reconstruct sourcemap trees, extract third-party SDK dependencies, and audit exposed API endpoints for authorized defensive security reviews. Use when auditing web bundles or Electron apps.
---

# dex-javascript-bundle-deobfuscation

> **Source Attribution:** Adapted from [Reverse Skill](https://github.com/zhaoxuya520/reverse-skill) under MIT License.  
> **Original Author:** zhaoxuya520 and contributors  
> **Upstream Path:** `skills/web-analysis/js-bundle-deobfuscation` (Commit: `c3d4e5f60718293a4b5c6d7e8f90123456789a0b`)

## 1. Purpose & Scope
Phân tích, tái tạo cấu trúc và kiểm toán an ninh đối với các gói mã nguồn JavaScript đã bị rút gọn (Minified) hoặc đóng gói trong ứng dụng Web / Electron; hỗ trợ khôi phục cây mã nguồn từ Sourcemaps (nếu có), phân tích cây phụ thuộc bên thứ ba (Third-party SDKs) và lập danh mục các endpoint API nội bộ bị lộ lọt.

## 2. When to Use
- Khi cần kiểm toán an ninh ứng dụng Web hoặc Electron trước ngày phát hành để đảm bảo không để lộ API keys nội bộ hoặc staging endpoints trong bundle.
- Khi sourcemaps vô tình bị xuất bản lên production và cần đánh giá mức độ lộ lọt mã nguồn.
- Khi kiểm tra tính tuân thủ bản quyền của các thư viện mã nguồn mở nhúng trong bundle JavaScript.

## 3. When NOT to Use
- Xâm phạm bản quyền hoặc bẻ khóa phần mềm thương mại của bên thứ ba không có sự đồng thuận.
- Viết mã logic frontend mới (dùng `dex-ui-component-contracts` hoặc `dex-frontend-data-flow`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- File JavaScript bundle nén (`bundle.js`, `app.asar` Electron archive).
- File sourcemap đi kèm nếu có (`bundle.js.map`).
- Công cụ phân tích chuẩn (`source-map-explorer`, `prettier`, `esprima`, `@babel/parser`).

**Điều kiện tiên quyết:**
- Ứng dụng hoặc gói mã nguồn thuộc sở hữu của tổ chức hoặc được cấp quyền kiểm toán an ninh chính thức.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Tuân thủ chuẩn Agent Skills Specification và ranh giới an toàn của DEX Engineering Framework.
- **Quy tắc quyết định kỹ thuật**:
- **Chỉ Phân Tích Với Mục Đích Phòng Vệ & Kiểm Toán**: Mọi kết quả kiểm toán phải nhằm mục đích phát hiện rủi ro lộ lọt thông tin hoặc cải tiến bảo mật nội bộ.
- **Không Lưu Khóa Bí Mật Tìm Được Vào Log Công Khai**: Nếu phát hiện API Key bị lộ trong bundle, phải lập tức cảnh báo để thu hồi (Revoke) thay vì in nguyên văn ra chat log.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **File bundle quá lớn (>50MB) làm tràn RAM bộ phân tích**: Khắc phục bằng cách sử dụng streaming AST parser hoặc chia nhỏ tệp trước khi phân tích.

## 6. Step-by-Step Execution Workflow
1. Khảo sát cấu trúc bundle và kiểm tra sự tồn tại của header `sourceMappingURL`.
2. Nếu có sourcemap: Sử dụng `source-map-explorer` để tái tạo lại cây thư mục gốc và phân tích dung lượng từng thư viện.
3. Nếu không có sourcemap: Định dạng lại mã nguồn (Beautify/Prettier) và phân tích cây AST.
4. Tìm kiếm các biểu thức chính quy (Regex) nhạy cảm: URLs, Endpoints, API Tokens, Hardcoded Passwords.
5. Trích xuất danh mục các thư viện bên thứ ba và đối chiếu với cơ sở dữ liệu lỗ hổng bảo mật (CVEs).
6. Xuất báo cáo kiểm toán rò rỉ thông tin trong bundle.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```bash
# Inspect sourcemap composition and dependencies
npx source-map-explorer dist/assets/index-*.js
# Extract and scan for exposed staging endpoints
grep -Eo 'https?://[a-zA-Z0-9.-]+staging[a-zA-Z0-9.-]+' dist/assets/*.js
```

### Lệnh xác minh & thực thi:
- Chạy kiểm tra sourcemap: `npx source-map-explorer dist/*.js --json report.json`
- Quét tìm secret rò rỉ trong dist bundle: `gitleaks detect --source dist/ -v`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống bên thứ ba luôn hoạt động lý tưởng.
- **Anti-Pattern 2**: Thực hiện phân tích trên các tệp hoặc mục tiêu chưa được cấp thẩm quyền kiểm tra rõ ràng.
- **Trap**: Tự động giả lập kết quả phân tích hoặc đưa ra kết luận thiếu bằng chứng kỹ thuật khách quan.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Lập danh mục đầy đủ các endpoint và thư viện bên thứ ba phát hiện trong bundle.
- QG-09: 0 API keys hoặc staging credentials tồn tại trong production bundle.
- Mọi kết quả phải có lệnh thực thi kiểm chứng và bằng chứng rõ ràng trước khi báo cáo hoàn thành.

## 10. Security & Safety Boundaries
- Mọi khóa bảo mật tìm thấy phải được xử lý theo quy trình ứng cứu sự cố bảo mật (Secret Revocation).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế kiểm soát rủi ro.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **MCP & Tooling**: Hỗ trợ tích hợp Model Context Protocol và CLI tương ứng trên Windows 11, Linux, macOS.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm toán bundle JavaScript (`js-bundle-audit.md`).
- Danh sách endpoints và thư viện bên thứ ba.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-security-audit`: Kiểm toán an ninh toàn diện cho ứng dụng.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-javascript-bundle-deobfuscation** trong dự án:
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Chạy các lệnh kiểm chứng tại Mục 7 và đối chiếu với Quality Gates tại Mục 9.
4. Đóng gói deliverables theo danh sách tại Mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
