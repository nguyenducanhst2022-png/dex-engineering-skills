---
name: dex-cryptographic-api-review
description: Audit, verify, and enforce correct cryptographic API usage, key derivation (Argon2id, PBKDF2), secure random generation, and authenticated encryption (AES-GCM, ChaCha20-Poly1305). Use when implementing encryption and hashing in software.
---

# dex-cryptographic-api-review

## 1. Purpose & Scope
Kiểm toán, thẩm định và cưỡng chế việc sử dụng đúng đắn các giao diện lập trình mật mã học (Cryptographic APIs); áp dụng các thuật toán mã hóa có xác thực dữ liệu (Authenticated Encryption: AES-GCM, ChaCha20-Poly1305), thuật toán dẫn xuất khóa an toàn (Key Derivation: Argon2id, PBKDF2), bộ sinh số ngẫu nhiên chuẩn mật mã (CSPRNG), và triệt tiêu các lỗi nguy hiểm chết người như tái sử dụng Nonce/IV hoặc dùng thuật toán lỗi thời (MD5, SHA1, DES, ECB mode).

## 2. When to Use
- Phát triển tính năng băm mật khẩu, mã hóa dữ liệu nhạy cảm lưu trong database (Encryption-at-Rest) hoặc ký số dữ liệu.
- Kết quả rà soát mã nguồn phát hiện việc sử dụng các hàm mật mã học không an toàn (`Math.random()`, `DES`, `AES-ECB`).
- Chuẩn bị cho kỳ kiểm toán an ninh mật mã chuyên sâu.

## 3. When NOT to Use
- Tuyệt đối không bao giờ tự phát minh ra thuật toán mật mã hoặc cơ chế mã hóa riêng ('Don't roll your own crypto'). Luôn luôn sử dụng các thư viện chuẩn đã được kiểm chứng qua nhiều năm (Libsodium, Web Crypto API, cryptography trong Python).
- Không dùng thuật toán băm nhanh thông thường (SHA-256) để băm mật khẩu người dùng (phải dùng thuật toán kháng phần cứng chuyên dụng như Argon2id hoặc bcrypt).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Đoạn mã nguồn thực hiện các thao tác mã hóa, giải mã, băm hoặc sinh khóa.
- Loại dữ liệu cần bảo vệ (Mật khẩu, Thẻ tín dụng, Dữ liệu truyền thông thời gian thực).
- Tiêu chuẩn mật mã học mục tiêu (NIST Cryptographic Standards).
- **Điều kiện tiên quyết**:
- Có quyền truy cập vào các thư viện mật mã học chuẩn mực của ngôn ngữ.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Authenticated Encryption with Associated Data (AEAD):
  + Mã hóa truyền thống (như AES-CBC) chỉ bảo đảm tính bí mật nhưng không chống được việc kẻ tấn công sửa đổi bản mã (Bit-flipping attacks). AEAD (AES-GCM, ChaCha20-Poly1305) vừa mã hóa vừa tạo ra một Authentication Tag; nếu bản mã bị sửa dù chỉ 1 bit, hàm giải mã sẽ lập tức từ chối và báo lỗi.
- The Nonce-Reuse Disaster: Trong AES-GCM, nếu bạn mã hóa hai bản tin khác nhau với cùng một Khóa (Key) và cùng một Nonce (Number Used Once), kẻ tấn công có thể thu hồi khóa xác thực và giải mã toàn bộ dữ liệu. Nonce bắt buộc phải là duy nhất cho mỗi lần mã hóa.
- CSPRNG vs PRNG: `Math.random()` hoặc `rand()` là bộ sinh số ngẫu nhiên giả lập có thể dự đoán được; tuyệt đối chỉ dùng `crypto.randomBytes()` hoặc `secrets.token_bytes()` cho mục đích an ninh.
- **Quy tắc quyết định kỹ thuật**:
- Băm mật khẩu người dùng: Bắt buộc sử dụng Argon2id (ưu tiên số 1) hoặc bcrypt với work factor tối thiểu 12.
- Mã hóa dữ liệu đối xứng: Bắt buộc sử dụng AES-256-GCM hoặc ChaCha20-Poly1305 với Nonce ngẫu nhiên 96-bit (12 bytes) cho mỗi lần mã hóa.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Sử dụng chế độ AES ở chế độ ECB (`AES/ECB/PKCS5Padding`), khiến các khối dữ liệu giống nhau sinh ra các khối bản mã giống nhau, làm lộ hình ảnh gốc (lỗ hổng kinh điển ECB Penguin).

## 6. Step-by-Step Execution Workflow
1. Quét tìm toàn bộ các vị trí gọi thư viện crypto trong codebase.
2. Loại bỏ các thuật toán đã bị bẻ gãy: MD5, SHA-1, DES, RC4, AES-ECB.
3. Thay thế các hàm băm mật khẩu cũ bằng Argon2id.
4. Đảm bảo mọi thao tác mã hóa đối xứng đều sử dụng chuẩn AEAD kèm Nonce sinh ngẫu nhiên an toàn.
5. Kiểm tra việc so sánh chuỗi mật mã sử dụng hàm so sánh thời gian cố định (Constant-time comparison) để chống tấn công Timing Attacks.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Mã hóa dữ liệu an toàn đạt chuẩn NIST bằng AES-256-GCM (Python Cryptography)
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_sensitive_data(plaintext: bytes, master_key: bytes) -> bytes:
    # Sinh Nonce ngẫu nhiên 96-bit (12 bytes) duy nhất cho mỗi lần mã hóa
    nonce = os.urandom(12)
    aesgcm = AESGCM(master_key)
    # Mã hóa kèm sinh Authentication Tag
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    # Đóng gói Nonce đi kèm bản mã (Nonce không cần giữ bí mật, chỉ cần duy nhất)
    return nonce + ciphertext

def decrypt_sensitive_data(payload: bytes, master_key: bytes) -> bytes:
    nonce = payload[:12]
    ciphertext = payload[12:]
    aesgcm = AESGCM(master_key)
    # Tự động ném lỗi nếu dữ liệu bị sửa đổi (Tampered)
    return aesgcm.decrypt(nonce, ciphertext, None)
```

### Lệnh xác minh & thực thi:
```bash
# Quét mã nguồn tìm các hàm mật mã học không an toàn bằng Semgrep
semgrep scan --config p/cryptography
```

## 8. Anti-Patterns & Common Traps
- Hardcode Master Key trực tiếp trong mã nguồn hoặc commit lên Git.
- So sánh mật khẩu hoặc mã hash bằng toán tử `==` thông thường (dễ bị tấn công Timing Attack; phải dùng `crypto.timingSafeEqual`).

## 9. Quality Gates & Acceptance Criteria
- 0 thuật toán lỗi thời (MD5, SHA1, DES, ECB) nào tồn tại trong toàn bộ dự án.
- 100% các phép mã hóa dữ liệu đối xứng đều sử dụng chế độ Authenticated Encryption (AEAD).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Khóa mã hóa phải được lưu trữ trong dịch vụ quản lý khóa chuyên dụng (AWS KMS, HashiCorp Vault) và có chính sách tự động xoay vòng khóa định kỳ.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Module thư viện mã hóa chuẩn mực của dự án.
- Báo cáo kiểm toán an ninh mật mã học và danh sách các thuật toán đã chuẩn hóa.

## 13. Related & Complementary Skills
dex-sast-finding-triage, dex-web-security-headers, dex-cloud-iam-policy-review

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng y tế lưu trữ số thẻ bảo hiểm y tế trong database bằng thuật toán AES-ECB. Khi kiểm toán an ninh, chuyên gia phát hiện ra các bệnh nhân có cùng nhóm máu và bệnh án đều sinh ra các đoạn mã hóa giống nhau, làm lộ thông tin nhạy cảm. Nhóm đã nâng cấp toàn bộ hệ thống sang AES-256-GCM với Nonce ngẫu nhiên, giải quyết triệt để nguy cơ rò rỉ dữ liệu y tế.
