---
name: dex-context-engineering
description: AI context optimization, persistent project memory architecture, documentation governance, and context relevance filtering. Establishes single sources of truth (AGENTS.md, SPEC.md, ARCHITECTURE.md, TASKS.md) to eliminate agent hallucination. Use when organizing project documentation, setting up agent context, or preventing memory drift.
---

# DEX Context Engineering

## 1. Purpose
Tổ chức, chuẩn hóa và quản lý ngữ cảnh (Context) cũng như bộ nhớ dài hạn cho AI Coding Agent; đảm bảo Agent luôn hiểu đúng dự án, nắm vững mục tiêu, biết rõ những gì đã làm, đang làm và chưa được phép chạm vào, không bị phụ thuộc một cách mù quáng vào lịch sử hội thoại tạm thời.

Quy trình quản lý ngữ cảnh chuẩn:
`Thu thập ngữ cảnh → Phân loại → Chuẩn hóa → Lưu tài liệu → Cung cấp cho AI → Thực thi → Kiểm chứng → Cập nhật ngữ cảnh`

Nguyên tắc cốt lõi: **AI phải hiểu đúng hiện trạng dự án, biết chính xác những gì đã hoàn thành, đang thực hiện và chưa được phép thay đổi. Không phụ thuộc hoàn toàn vào bộ nhớ hội thoại chat ngắn hạn.**
Ghi nhớ sống còn: **AI giỏi + Ngữ cảnh sai = Code sai. Ngữ cảnh tốt giúp AI hiểu dự án, giữ đúng mục tiêu và hạn chế tối đa việc sửa nhầm.**

## 2. When to Use
- Khi bắt đầu một dự án mới cần thiết lập tài liệu gốc cho AI (Single Source of Truth).
- Khi hội thoại của Agent bị dài (context window sắp đầy) cần cô đọng và lưu trữ trạng thái vào file tài liệu dự án bền vững.
- Khi Agent có dấu hiệu "quên" mục tiêu ban đầu, suy diễn sai cấu trúc hoặc tự ý đảo ngược các quyết định kỹ thuật đã thống nhất.
- Khi bàn giao công việc giữa các phiên làm việc (Session hand-off).

## 3. When Not to Use
- Tạo thêm hàng chục file tài liệu rườm rà, trùng lặp khi dự án đã có sẵn tài liệu tương đương chuẩn xác.
- Nhồi nhét toàn bộ mã nguồn của cả dự án vào prompt gây quá tải ngữ cảnh và làm giảm độ chính xác của AI.

## 4. Inputs
- Cấu trúc thư mục hiện tại của dự án.
- Bộ tài liệu cốt lõi chuẩn:
  - `README.md`: Hướng dẫn tổng quan và khởi chạy.
  - `AGENTS.md`: Chỉ dẫn vận hành, quy ước code và công cụ cho AI.
  - `SPEC.md`: Đặc tả tính năng và tiêu chí nghiệm thu.
  - `ARCHITECTURE.md`: Sơ đồ kiến trúc và luồng dữ liệu.
  - `TASKS.md`: Danh sách công việc, trạng thái TODO / IN PROGRESS / DONE.
  - `CHANGELOG.md`: Lịch sử các phiên bản đã phát hành.

## 5. Workflow

### Bước 1: Thu Thập & Lọc Nhiễu Ngữ Cảnh (Context Relevance Filtering)
- Chỉ trích xuất các thông tin thực sự liên quan trực tiếp đến nhiệm vụ hiện tại.
- Loại bỏ các thông tin rác, log debug cũ, các đoạn chat lan man không liên quan đến kỹ thuật.

### Bước 2: Thiết Lập Nguồn Chân Lý Duy Nhất (Single Source of Truth)
- Đảm bảo mỗi thông tin kỹ thuật chỉ được lưu tại một nơi duy nhất:
  - Quy ước code và lệnh build → Lưu trong `AGENTS.md`.
  - Tiến độ công việc → Lưu trong `TASKS.md`.
  - Quyết định kiến trúc → Lưu trong `ARCHITECTURE.md` hoặc `docs/adr/`.
- Tuyệt đối không để xảy ra tình trạng thông tin trong tài liệu mâu thuẫn với mã nguồn thực tế.

### Bước 3: Chuẩn Hóa Bộ Nhớ Bền Vững (Persistent Documentation)
- Mọi thỏa thuận kỹ thuật quan trọng phát sinh trong quá trình chat phải được ghi nhận ngay lập tức vào các file Markdown trong repository.
- File Markdown trong repo chính là bộ nhớ bền vững (Long-term Memory) trường tồn qua các phiên làm việc của AI.

### Bước 4: Cung Cấp Ngữ Cảnh Tối Ưu Cho AI (Progressive Context Injection)
- Khi bắt đầu phiên làm việc: Yêu cầu AI đọc file tài liệu tóm tắt trước (`AGENTS.md`, `TASKS.md`).
- Chỉ nạp chi tiết các file mã nguồn liên quan trực tiếp khi AI chuẩn bị chỉnh sửa (Progressive Disclosure).

### Bước 5: Đối Chiếu & Xác Thực Ngữ Cảnh (Context Validation)
- Yêu cầu AI luôn đối chiếu thông tin trong tài liệu với mã nguồn thực tế:
  - Nếu tài liệu ghi hàm `A()` có 2 tham số, nhưng code thực tế có 3 tham số → AI phải tin vào mã nguồn thực tế và đề xuất cập nhật lại tài liệu.

### Bước 6: Cập Nhật Trạng Thái Tiến Độ (Context Synchronization)
- Ngay sau khi hoàn thành một nhiệm vụ nhỏ: Cập nhật ngay file `TASKS.md` (chuyển từ `[ ]` sang `[x]`) và cập nhật `CHANGELOG.md`.

## 6. Quality Gates
- **QG-01 (Context-Aware Scope)**: AI hiểu đúng phạm vi và không chạm vào các phần đã ghi rõ là cấm sửa trong `AGENTS.md`.
- **QG-09 (Documentation Synchronized)**: `TASKS.md` và các tài liệu liên quan phản ánh chính xác 100% trạng thái thực tế của code sau khi sửa.

## 7. Safety Rules (4 Nguyên Tắc Context Engineering)
1. **Context Relevance (Sự phù hợp của ngữ cảnh)**: Chỉ cung cấp thông tin liên quan, tránh nhồi nhét làm loãng bộ nhớ của AI.
2. **Single Source of Truth (Nguồn chân lý duy nhất)**: Mỗi thông tin quan trọng chỉ nằm ở một file chuẩn, không sao chép rải rác gây mâu thuẫn.
3. **Persistent Documentation (Lưu trữ bền vững)**: Lưu kiến thức quan trọng vào file tài liệu trong Git, không để phụ thuộc vào lịch sử chat tạm bợ.
4. **Context Validation (Kiểm chứng ngữ cảnh)**: Luôn đối chiếu ngữ cảnh tài liệu với mã nguồn và kết quả thực tế từ terminal.

## 8. Expected Outputs
1. Bộ tài liệu ngữ cảnh chuẩn (`AGENTS.md`, `TASKS.md`, `SPEC.md`).
2. Trạng thái nhiệm vụ được cập nhật minh bạch, không bị mất dấu.
3. AI thực thi chính xác theo quy ước dự án mà không cần phải nhắc lại quy tắc nhiều lần.

## 9. Failure Handling
- Khi AI bị ảo giác (Hallucination) hoặc quên ngữ cảnh: Yêu cầu AI đọc lại trực tiếp file `AGENTS.md` và `TASKS.md`, dừng việc suy diễn từ lịch sử chat.

## 10. Completion Criteria
- Các quyết định kỹ thuật và tiến độ nhiệm vụ được đồng bộ đầy đủ vào repository.
- Không có sự mâu thuẫn giữa tài liệu hướng dẫn và mã nguồn thực tế.

---

## Real-world Example
File `TASKS.md` quản lý tiến độ:
```markdown
# Project Roadmap & Tasks

## Sprint 1: Authentication
- [x] Task 1.1: Thiết kế User schema trong database (Hoàn thành - Commit `a1b2c3d`)
- [x] Task 1.2: Triển khai password hashing với bcrypt (Hoàn thành - Commit `e4f5g6h`)
- [/] Task 1.3: Triển khai JWT token login API (Đang thực hiện)
- [ ] Task 1.4: Middleware bảo vệ route private (Chưa bắt đầu)
```
AI khi bắt đầu phiên làm việc chỉ cần đọc `TASKS.md` là biết ngay mình đang ở đâu, cần làm gì tiếp theo mà không cần hỏi lại người dùng.
