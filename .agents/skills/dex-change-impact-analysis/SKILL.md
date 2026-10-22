---
name: dex-change-impact-analysis
description: Blast radius estimation, dependency mapping, regression risk assessment, and pre-modification impact analysis. Maps upstream and downstream dependencies before altering shared code. Use prior to refactoring, modifying shared utilities, altering database schemas, or changing public API signatures.
---

# DEX Change Impact Analysis

## 1. Purpose & Scope
Phân tích toàn diện và định lượng bán kính ảnh hưởng (Blast Radius) cũng như rủi ro tiềm ẩn của một thay đổi trước khi viết hoặc sửa bất kỳ dòng mã nguồn nào, giúp lập kế hoạch kiểm thử hồi quy chính xác và ngăn chặn các sự cố "sửa một chỗ, hỏng mười chỗ".

Quy trình phân tích tác động chuẩn:
`Xác định thay đổi → Phân tích phụ thuộc → Đánh giá rủi ro → Lập kế hoạch → Sửa code → Kiểm thử hồi quy → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Trước khi sửa đổi một hàm, module hay cơ sở dữ liệu, bắt buộc phải biết rõ những module, API, database và chức năng nào đang phụ thuộc vào nó.**
Ghi nhớ sống còn: **Biết trước phạm vi ảnh hưởng = Sửa code tự tin + Không gây lỗi dây chuyền + Kiểm thử đúng trọng tâm.**

## 2. When to Use
- Trước khi chỉnh sửa các hàm tiện ích dùng chung (Shared Utilities), thư viện nội bộ hoặc Base classes.
- Trước khi sửa đổi kiểu dữ liệu (Types / Interfaces) hoặc chữ ký hàm (Function Signatures) được gọi ở nhiều file.
- Trước khi thực hiện migration cơ sở dữ liệu hoặc thay đổi cấu trúc bảng.
- Khi người dùng yêu cầu tái cấu trúc một thành phần lõi của hệ thống.

## 3. When NOT to Use
- Tạo một file mới hoàn toàn độc lập chưa có ai phụ thuộc vào.
- Sửa đổi nội bộ logic của một private method trong một component lá (Leaf component) không ai import.

## 4. Prerequisites & Input Context
- Tệp tin, hàm hoặc bảng dữ liệu dự kiến sẽ bị thay đổi.
- Nội dung thay đổi dự kiến (Đổi tham số, đổi kiểu trả về, đổi logic nghiệp vụ).
- Cây phụ thuộc mã nguồn (Dependency graph) hoặc kết quả tìm kiếm tham chiếu trong dự án.

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác kỹ thuật phải có thể kiểm chứng độc lập với số liệu rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Xác Định Thay Đổi Cụ Thể (Proposed Delta)
- Định nghĩa chính xác nội dung dự kiến can thiệp:
  - Thay đổi logic nội tại (Internal behavior)?
  - Thay đổi giao diện công khai (Public API / Signature / Return type)?
  - Thay đổi cấu trúc dữ liệu cơ sở dữ liệu (Schema change)?

### Bước 2: Quét & Lập Bản Đồ Phụ Thuộc (Dependency Mapping)
- Sử dụng các công cụ tìm kiếm và phân tích tĩnh để lập danh sách toàn bộ các thành phần phụ thuộc:
  - **Phụ thuộc xuôi (Downstream callers)**: Những file, controller, service nào đang `import` và gọi hàm này?
  - **Phụ thuộc ngược (Upstream dependencies)**: Hàm này đang phụ thuộc vào những service nào khác?
  - **Tác động dữ liệu (Data impact)**: Có làm ảnh hưởng đến dữ liệu lịch sử trong DB không?

### Bước 3: Đánh Giá Mức Độ Rủi Ro & Bán Kính Ảnh Hưởng (Blast Radius Assessment)
- Phân loại mức độ rủi ro theo thang đo:
  - **RỦI RO THẤP**: Chỉ ảnh hưởng nội bộ 1 file lá, 0 downstream caller.
  - **RỦI RO TRUNG BÌNH**: Ảnh hưởng 2-5 files cùng một module nghiệp vụ.
  - **RỦI RO CAO / NGHIÊM TRỌNG**: Hàm dùng chung toàn hệ thống (>10 callers), thay đổi schema DB lõi, ảnh hưởng đến xác thực/thanh toán.

### Bước 4: Lập Kế Hoạch Thay Đổi & Danh Sách Kiểm Thử Bắt Buộc (Impact Mitigation Plan)
- Nếu thay đổi signature: Lên danh sách tất cả các nơi gọi cần được cập nhật đồng thời.
- Lập Checklist các bài kiểm thử hồi quy bắt buộc phải chạy lại sau khi sửa code.

### Bước 5: Triển Khai Thay Đổi Có Kiểm Soát (Controlled Execution)
- Tiến hành sửa code theo đúng danh sách đã lập ở Bước 4.
- Đảm bảo tính nhất quán giữa caller và callee.

### Bước 6: Kiểm Thử Hồi Quy Toàn Diện Bán Kính Ảnh Hưởng (Regression Verification)
- Chạy 100% các bài test của tất cả các module nằm trong bán kính ảnh hưởng.
- Xác nhận không có caller nào bị lỗi thời hoặc truyền thiếu tham số.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-change-impact-analysis
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Blast Radius Fully Mapped)**: Có danh sách đầy đủ tất cả các file bị ảnh hưởng trước khi code.
- **QG-06 (No Downstream Regressions)**: Toàn bộ các module phụ thuộc tiếp tục hoạt động chính xác sau thay đổi.
- **QG-08 (Diff Aligned with Impact Plan)**: Git diff chỉ chứa các thay đổi đã được dự báo trong bản phân tích tác động.

## 10. Security & Safety Boundaries
- **Cấm Sửa "Liều" (No Blind Refactoring)**: Tuyệt đối không thay đổi kiểu trả về của hàm dùng chung mà không kiểm tra xem ai đang sử dụng giá trị trả về đó.
- **Bắt Buộc Báo Động Khi Bán Kính Lớn**: Nếu một thay đổi ảnh hưởng trên 5 module, Orchestrator bắt buộc phải nâng cấp lên **STRICT MODE** và cảnh báo người dùng.
- **Ưu Tiên Tương Thích Ngược**: Khi có thể, hãy hỗ trợ cả cách gọi cũ (ví dụ overload tham số hoặc gán default value) để giảm thiểu rủi ro phải sửa đồng loạt quá nhiều nơi.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Báo cáo phân tích tác động (Impact Analysis Report): Danh sách file bị ảnh hưởng, Mức độ rủi ro, Danh sách test cần chạy.
2. Bản cập nhật mã nguồn đồng bộ trên toàn bộ bán kính ảnh hưởng.
3. Bằng chứng kiểm thử hồi quy đạt PASS 100%.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-change-impact-analysis** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
