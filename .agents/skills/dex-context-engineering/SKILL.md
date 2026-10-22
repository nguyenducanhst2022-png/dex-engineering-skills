---
name: dex-context-engineering
description: AI context optimization, persistent project memory architecture, documentation governance, and context relevance filtering. Establishes single sources of truth (AGENTS.md, SPEC.md, ARCHITECTURE.md, TASKS.md) to eliminate agent hallucination. Use when organizing project documentation, setting up agent context, or preventing memory drift.
---

# DEX Context Engineering

## 1. Purpose & Scope
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

## 3. When NOT to Use
- Tạo thêm hàng chục file tài liệu rườm rà, trùng lặp khi dự án đã có sẵn tài liệu tương đương chuẩn xác.
- Nhồi nhét toàn bộ mã nguồn của cả dự án vào prompt gây quá tải ngữ cảnh và làm giảm độ chính xác của AI.

## 4. Prerequisites & Input Context
- Cấu trúc thư mục hiện tại của dự án.
- Bộ tài liệu cốt lõi chuẩn:
  - `README.md`: Hướng dẫn tổng quan và khởi chạy.
  - `AGENTS.md`: Chỉ dẫn vận hành, quy ước code và công cụ cho AI.
  - `SPEC.md`: Đặc tả tính năng và tiêu chí nghiệm thu.
  - `ARCHITECTURE.md`: Sơ đồ kiến trúc và luồng dữ liệu.
  - `TASKS.md`: Danh sách công việc, trạng thái TODO / IN PROGRESS / DONE.
  - `CHANGELOG.md`: Lịch sử các phiên bản đã phát hành.

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
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

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-context-engineering
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Context-Aware Scope)**: AI hiểu đúng phạm vi và không chạm vào các phần đã ghi rõ là cấm sửa trong `AGENTS.md`.
- **QG-09 (Documentation Synchronized)**: `TASKS.md` và các tài liệu liên quan phản ánh chính xác 100% trạng thái thực tế của code sau khi sửa.

## 10. Security & Safety Boundaries
1. **Context Relevance (Sự phù hợp của ngữ cảnh)**: Chỉ cung cấp thông tin liên quan, tránh nhồi nhét làm loãng bộ nhớ của AI.
2. **Single Source of Truth (Nguồn chân lý duy nhất)**: Mỗi thông tin quan trọng chỉ nằm ở một file chuẩn, không sao chép rải rác gây mâu thuẫn.
3. **Persistent Documentation (Lưu trữ bền vững)**: Lưu kiến thức quan trọng vào file tài liệu trong Git, không để phụ thuộc vào lịch sử chat tạm bợ.
4. **Context Validation (Kiểm chứng ngữ cảnh)**: Luôn đối chiếu ngữ cảnh tài liệu với mã nguồn và kết quả thực tế từ terminal.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Bộ tài liệu ngữ cảnh chuẩn (`AGENTS.md`, `TASKS.md`, `SPEC.md`).
2. Trạng thái nhiệm vụ được cập nhật minh bạch, không bị mất dấu.
3. AI thực thi chính xác theo quy ước dự án mà không cần phải nhắc lại quy tắc nhiều lần.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-context-engineering** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
