# AGENTS.md — AI Coding Agent Operating Guide

> **File mẫu hướng dẫn vận hành dự án dành riêng cho AI Coding Agents.**
> Hãy sao chép file này vào thư mục gốc của dự án (`AGENTS.md`) và tùy biến theo thông tin cụ thể của dự án bạn.

---

## 1. Project Context & Mission
- **Tên dự án**: [Tên Dự Án Của Bạn]
- **Mô tả**: [Mô tả ngắn gọn mục tiêu của hệ thống]
- **Ngôn ngữ & Runtime**: Node.js 20 LTS (TypeScript 5.x) / Python 3.12 / Go 1.22
- **Framework chính**: Express.js / Fastify / Next.js / FastAPI
- **Cơ sở dữ liệu**: PostgreSQL 16 (Prisma ORM) / Redis 7

---

## 2. Engineering Skill Framework: DEX Engineering Skills
Dự án này áp dụng bộ kỹ năng **DEX Engineering Skills Pack v1.0**.
Tất cả các tác vụ lập trình, kiểm thử và bảo trì PHẢI tuân thủ các quy tắc trong `.agents/skills/`.

### Quy trình Kích hoạt Mặc định:
Khi tiếp nhận yêu cầu từ người dùng, AI Agent LUÔN BẮT ĐẦU bằng việc kích hoạt:
👉 `dex-master-orchestrator`

Orchestrator sẽ đánh giá rủi ro và lựa chọn chế độ phù hợp:
- **QUICK MODE**: Sửa lỗi nhỏ, sửa typo, UI text (1-2 files).
- **STANDARD MODE**: Tính năng mới, refactor module vừa.
- **STRICT MODE**: Database migration, Authentication, Bảo mật, Release Production.

---

## 3. Lệnh Thao Tác Chuẩn (Standard Commands)

```bash
# Kiểm tra định dạng và quy chuẩn mã nguồn
npm run lint

# Kiểm tra kiểu dữ liệu tĩnh (Bắt buộc 0 lỗi)
npm run type-check

# Chạy toàn bộ Unit Tests
npm test

# Chạy bài kiểm thử cho một file cụ thể
npm test -- path/to/test.spec.ts

# Chạy build kiểm tra bản đóng gói Production
npm run build

# Chạy migration cơ sở dữ liệu trên môi trường test
npx prisma migrate dev
```

---

## 4. 7 Quy Tắc Bất Khả Xâm Phạm Cho AI (Universal Rules)

1. **Kiểm Soát Phạm Vi (Scope Control)**: Chỉ sửa các file thuộc phạm vi được giao. Cấm tự ý sửa file ngoài phạm vi.
2. **Kiểm Tra Thực Tế (Test Before Completion)**: Phải chạy lệnh test trong terminal thật và có output chứng minh trước khi báo hoàn thành.
3. **Sửa Tận Gốc (Root Cause First)**: Không sửa mò, không dùng `try-catch` rỗng để nuốt lỗi, không sửa triệu chứng.
4. **An Toàn Git (Git Safety)**: CẤM chạy `git push --force`, `git reset --hard` hoặc xóa branch khi chưa có sự đồng ý tường minh từ người dùng.
5. **Bảo Mật Tuyệt Đối (Zero Secrets)**: Không bao giờ hardcode token, mật khẩu hoặc API key vào mã nguồn.
6. **Không Báo Hoàn Thành Ảo (No False Completion)**: Nghiêm cấm bịa đặt log hoặc tuyên bố PASS khi chưa thực sự chạy lệnh.
7. **Tối Giản Hóa (Simplicity)**: Tuân thủ KISS và YAGNI. Không thêm thư viện ngoài nếu không có lý do chính đáng.

---

## 5. Tài Liệu Dự Án Tham Khảo (Single Sources of Truth)
- `README.md`: Hướng dẫn cài đặt và khởi chạy ứng dụng.
- `SPEC.md`: Bản đặc tả kỹ thuật và tiêu chí nghiệm thu của tính năng hiện tại.
- `ARCHITECTURE.md`: Sơ đồ kiến trúc và luồng dữ liệu.
- `TASKS.md`: Danh sách công việc và tiến độ chi tiết.
- `CHANGELOG.md`: Lịch sử các phiên bản phát hành.
