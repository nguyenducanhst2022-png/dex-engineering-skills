---
name: dex-javascript-bundle-obfuscation-audit
description: Analyze commercial and client-side JavaScript bundles for anti-debugging techniques, control flow flattening, string encryption, and hidden telemetry without violating compliance boundaries. Use when auditing web client security and third-party SDKs.
---

# dex-javascript-bundle-obfuscation-audit

## 1. Purpose & Scope
Phân tích và kiểm toán các gói JavaScript bundle thương mại phía client; nhận diện các kỹ thuật làm rối mã nguồn (control flow flattening, mã hóa chuỗi, biến đổi AST), cơ chế chống debug (anti-debugging) và phát hiện các luồng thu thập dữ liệu từ xa (telemetry) tiềm ẩn mà không vi phạm ranh giới pháp lý.

## 2. When to Use
- Khi đánh giá rủi ro an ninh của các SDK bên thứ ba nhúng vào website ngân hàng hoặc thương mại điện tử.
- Khi điều tra các script đáng ngờ được nạp động từ các nhà cung cấp quảng cáo hoặc phân tích dữ liệu.
- Khi xác minh xem mã nguồn JavaScript nội bộ đã được làm rối và bảo vệ thích đáng trước khi phân phối hay chưa.

## 3. When NOT to Use
- Khi kiểm toán mã nguồn mở nội bộ đã có sẵn source maps và mã nguồn TypeScript rõ ràng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File JavaScript bundle (.js), công cụ định dạng và giải mã AST (Babel, Acorn, Prettier, webcrack).
- **Quyền hạn truy cập:** Quyền phân tích mã nguồn tĩnh trong môi trường trình duyệt sandbox.

## 5. Core Concepts & Taxonomy
- **Control Flow Flattening:** Kỹ thuật biến đổi cấu trúc lệnh tuần tự thành một vòng lặp vô hạn kết hợp switch-case lớn để che giấu logic nghiệp vụ.
- **String Array Encoding:** Lưu trữ toàn bộ chuỗi ký tự vào một mảng toàn cục và truy xuất qua các hàm giải mã phức tạp kèm xoay vòng mảng (array rotation).
- **Anti-Tampering & Debugger Traps:** Đoạn mã tự động kích hoạt câu lệnh `debugger` liên tục hoặc kiểm tra thời gian thực thi (timing checks) để làm đơ công cụ DevTools.

## 6. Step-by-Step Execution Workflow
1. Định dạng lại mã nguồn nén (de-minification) bằng Prettier hoặc js-beautify để phục hồi cấu trúc trực quan.
2. Phân tích cây cú pháp trừu tượng (AST) để phát hiện mảng chuỗi mã hóa và các hàm xoay vòng.
3. Áp dụng kỹ thuật giải mã hằng số tĩnh (Constant Propagation & Folding) để phục hồi các chuỗi ký tự ban đầu.
4. Rà soát các bẫy chống debug (`Function('debugger')()`) và vô hiệu hóa chúng trong môi trường phân tích.
5. Trích xuất toàn bộ các địa chỉ mạng (URLs, Endpoints) và các API gọi ra ngoài (`fetch`, `XMLHttpRequest`, `sendBeacon`).
6. Lập báo cáo kiểm toán phân loại các hành vi nghiệp vụ thực tế của script.

## 7. Concrete Examples
### Phục hồi chuỗi mã hóa và làm phẳng AST bằng script Node.js:
```javascript
import { parse } from '@babel/parser';
import traverse from '@babel/traverse';
import generate from '@babel/generator';

// Phân tích AST của bundle bị làm rối
const code = `var _0x12ab = ['Hello', 'World']; console.log(_0x12ab[0]);`;
const ast = parse(code);

traverse(ast, {
  MemberExpression(path) {
    // Thay thế truy xuất mảng hằng số bằng giá trị chuỗi thực tế
    if (path.node.object.name === '_0x12ab' && path.node.property.type === 'NumericLiteral') {
      const index = path.node.property.value;
      path.replaceWith({ type: 'StringLiteral', value: ['Hello', 'World'][index] });
    }
  }
});

const output = generate(ast).code;
console.log('Restored code:', output);
```

## 8. Anti-Patterns & Common Traps
- **Running Untrusted JS in Live Browser:** Mở trực tiếp script đáng ngờ trên trình duyệt đang đăng nhập tài khoản thực tế thay vì chạy trong sandbox cô lập.
- **Manual Guessing:** Cố gắng đọc hiểu thủ công hàng chục nghìn dòng lệnh bị làm phẳng luồng mà không dùng công cụ AST.
- **Tampering with Third-Party Licensers:** Sửa đổi mã nguồn nhằm phá vỡ cơ chế kiểm tra bản quyền trái phép vượt ngoài phạm vi ủy quyền kiểm toán.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các endpoint mạng bên ngoài được trích xuất và phân loại mục đích dữ liệu.
- **QG-04**: Giải mã thành công tối thiểu 80% các chuỗi ký tự bị mã hóa trong các hàm cốt lõi.
- **QG-09**: Toàn bộ quá trình phân tích được thực hiện trên môi trường sandbox không có kết nối ra Internet.

## 10. Security & Safety Boundaries
- Ngăn ngừa các cuộc tấn công Magecart hoặc chuỗi cung ứng web (Web Supply Chain Attacks) thông qua các SDK phân tích của bên thứ ba.

## 11. Platform Adapters
- **Tools**: webcrack, Babel AST, esprima, Prettier, mitmproxy, Chrome DevTools Protocol.

## 12. Deliverables & Output Artifacts
- Mã nguồn JavaScript đã được định dạng và gỡ bỏ một phần làm rối (de-obfuscated).
- Danh sách toàn bộ các URL, domain và API endpoints được script gọi tới.
- Báo cáo phân tích rủi ro an ninh và quyền riêng tư dữ liệu.

## 13. Related & Complementary Skills
dex-javascript-bundle-deobfuscation, dex-binary-provenance-matching, dex-sbom-binary-correlation

## 14. Realistic Usage Example
```powershell
# Giải mã và làm rõ cấu trúc bundle bằng webcrack
npx webcrack dist/vendor-bundle.js -o deobfuscated_src/

# Quét tìm các chuỗi URL hoặc domain trong mã nguồn phục hồi
Select-String -Path "deobfuscated_src/**/*.js" -Pattern "https?://[a-zA-Z0-9.-]+"
```
