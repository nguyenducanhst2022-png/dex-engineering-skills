---
name: dex-technical-debt-refactoring
description: Systematic technical debt assessment, safe code refactoring, code smell eradication, and behavioral preservation. Improves modularity, readability, and maintainability while guaranteeing zero breaking regressions with automated test harnesses. Use when refactoring legacy code, cleaning up duplicated logic, or untangling complex methods.
---

# DEX Technical Debt & Refactoring

## 1. Purpose & Scope
Đánh giá và kiểm soát nợ kỹ thuật (Technical Debt), thực hiện tái cấu trúc mã nguồn (Refactoring) an toàn và bài bản nhằm cải thiện khả năng đọc, tính dễ bảo trì và khả năng mở rộng của phần mềm mà tuyệt đối **không làm thay đổi hành vi nghiệp vụ hiện tại**.

Quy trình tái cấu trúc chuẩn:
`Phân tích code → Phát hiện nợ kỹ thuật → Đánh giá mức độ → Lập kế hoạch → Refactor → Kiểm thử hồi quy → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Cải thiện cấu trúc nội tại của code mà không làm thay đổi hành vi bên ngoài hoặc phá vỡ các chức năng hiện có.**
Ghi nhớ sống còn: **Refactoring tốt = Code sạch hơn + Dễ bảo trì hơn + Không phá chức năng cũ.**

## 2. When to Use
- Khi một hàm hoặc module trở nên quá phức tạp, khó đọc, độ phức tạp Cyclomatic quá cao (>10-15).
- Khi xuất hiện tình trạng lặp code (Code duplication / Copy-paste programming) ở nhiều nơi.
- Khi cần chuẩn bị nền tảng mã nguồn sạch trước khi bổ sung một tính năng phức tạp mới.
- Khi cần loại bỏ các "mùi khó chịu của code" (Code Smells: Long Method, Large Class, Primitive Obsession, Feature Envy).

## 3. When NOT to Use
- Sửa lỗi phần mềm đang xảy ra (khi đó phải dùng `dex-root-cause-debugging` trước).
- Đồng thời vừa thêm tính năng mới vừa viết lại toàn bộ cấu trúc trong cùng một commit.
- Khi mã nguồn hiện tại hoàn toàn chưa có bất kỳ bài kiểm tra (Unit test) nào để bảo vệ hành vi cũ.

## 4. Prerequisites & Input Context
- Vùng mã nguồn legacy hoặc phức tạp cần tái cấu trúc.
- Bộ kiểm thử hiện hữu của module (nếu chưa có, phải viết bổ sung Characterization Tests trước).
- Bản phân tích các chỉ số code quality (ví dụ: SonarQube, ESLint complexity report).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Khảo Sát & Phát Hiện Mùi Code (Code Smell Detection)
- Nhận diện các vấn đề nợ kỹ thuật phổ biến:
  - Hàm quá dài (>50 dòng), có quá nhiều mức thụt đầu dòng (Nested if-else).
  - Tên biến, tên hàm tối nghĩa, không phản ánh đúng ý đồ kinh doanh.
  - Sử dụng "Magic numbers" hoặc "Magic strings" rải rác.
  - Phụ thuộc cứng vào các triển khai cụ thể thay vì abstraction.

### Bước 2: Thiết Lập Lưới An Toàn Kiểm Thử (Establish Test Harness)
- **Bắt buộc**: Kiểm tra xem module đã có đủ bài kiểm thử để bao quát toàn bộ các ca sử dụng hiện tại hay chưa.
- Nếu chưa có: Viết ngay các bài kiểm tra đặc tả hành vi hiện tại (Characterization Tests) để "đóng băng" hành vi của hệ thống trước khi tái cấu trúc.
- Chạy test đảm bảo 100% PASS trước khi sửa bất kỳ dòng mã nguồn nào.

### Bước 3: Lập Kế Hoạch Từng Bước Nhỏ (Micro-step Planning)
- Chia quá trình tái cấu trúc thành các thao tác vi mô:
  - Tách hàm (Extract Method).
  - Đổi tên biến/hàm cho rõ nghĩa (Rename Variable/Function).
  - Thay thế câu lệnh điều kiện lồng nhau bằng Guard Clauses.
  - Thay thế tham số rời rạc bằng Đối tượng tham số (Introduce Parameter Object).

### Bước 4: Thực Hiện Tái Cấu Trúc Vi Mô (Incremental Refactoring)
- Chỉ thực hiện một thao tác vi mô duy nhất tại một thời điểm.
- Giữ logic bên ngoài (Public API / Interface) hoàn toàn không thay đổi.

### Bước 5: Chạy Kiểm Thử Hồi Quy Sau Mỗi Bước Nhỏ (Instant Regression Test)
- Ngay sau mỗi thao tác (ví dụ vừa tách xong một hàm), chạy lại toàn bộ test suite.
- Nếu test xanh (PASS): Tiếp tục thao tác nhỏ kế tiếp.
- Nếu test đỏ (FAIL): Lập tức hoàn tác lại thao tác vừa làm, kiểm tra tại sao hành vi bị thay đổi.

### Bước 6: Ổn Định & Ghi Nhận Lịch Sử (Stabilize & Commit)
- Lưu commit chuẩn: `refactor(billing): extract discount calculation into separate pure function`.
- Không gộp nhiều thay đổi không liên quan vào cùng một commit.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-technical-debt-refactoring
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Scope Confined)**: Chỉ tái cấu trúc nội bộ module mục tiêu, không đổi interface công khai.
- **QG-05 (100% Tests Pass)**: Toàn bộ bài test cũ đạt PASS 100% mà không cần phải sửa đổi assertion của test.
- **QG-06 (Zero Behavior Change)**: Xác nhận không có sự thay đổi nào về hành vi đầu ra đối với cùng một tập dữ liệu đầu vào.
- **QG-08 (Clean Refactor Diff)**: Git diff thể hiện rõ mục đích dọn dẹp, không trộn lẫn tính năng mới.

## 10. Security & Safety Boundaries
- **Không Refactor Khi Chưa Có Test**: Tuyệt đối không bao giờ tái cấu trúc một đoạn mã legacy phức tạp khi chưa có test suite bảo vệ.
- **Không Đổi Hành Vi Trong Quá Trình Refactor**: Nếu muốn thay đổi logic nghiệp vụ, phải làm thành 2 bước riêng biệt: Refactor trước để code sạch → Sau đó mới thêm tính năng trong commit khác.
- **Nguyên Tắc Hướng Đạo Sinh (Boy Scout Rule)**: Hãy luôn để mã nguồn sạch hơn lúc bạn mới tiếp cận một chút, nhưng không được biến nhiệm vụ sửa một lỗi nhỏ thành cuộc đại tu toàn bộ dự án.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Mã nguồn sạch sẽ, dễ hiểu, tuân thủ nguyên tắc SOLID và DRY.
2. Bộ kiểm thử hồi quy bảo vệ hành vi cũ.
3. Không có bất kỳ lỗi hồi quy nào phát sinh.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-technical-debt-refactoring** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
