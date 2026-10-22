---
name: dex-feature-prioritization
description: Prioritize product features and technical initiatives quantitatively using RICE, Value vs Effort, WSJF, and dependency graph analysis. Use when deciding what engineering tasks to build next under resource constraints.
---

# dex-feature-prioritization

## 1. Purpose & Scope
Thiết lập quy trình ưu tiên tính năng sản phẩm và các sáng kiến kỹ thuật (Quantitative Feature Prioritization) một cách định lượng, minh bạch và dựa trên dữ liệu; loại bỏ các quyết định cảm tính hoặc ý kiến của người có chức vụ cao nhất (HiPPO - Highest Paid Person's Opinion); áp dụng các khung đánh giá chuẩn quốc tế: RICE Scoring (Reach, Impact, Confidence, Effort), Ma trận Giá trị vs Nỗ lực (Value vs Effort), WSJF (Weighted Shortest Job First) và phân tích đồ thị phụ thuộc kỹ thuật (Dependency Graph Analysis) để tối ưu hóa giá trị bàn giao trong điều kiện nguồn lực hữu hạn.

## 2. When to Use
- Khi backlog sản phẩm có hàng trăm yêu cầu tính năng nhưng nguồn lực kỹ thuật chỉ đáp ứng được 20% trong quý.
- Khi có xung đột gay gắt giữa việc phát triển tính năng mới bán hàng và việc tái cấu trúc nợ kỹ thuật (Technical Debt).
- Khi các tính năng bị tắc nghẽn liên tục do phụ thuộc chéo vào nhau mà không được phân tích thứ tự trước sau.

## 3. When NOT to Use
- Xử lý sự cố production nghiêm trọng (dùng `dex-root-cause-debugging` và quy trình Incident).
- Khám phá nhu cầu ban đầu của người dùng (dùng `dex-product-discovery`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các đề xuất tính năng và sáng kiến kỹ thuật trong Backlog.
- Ước tính quy mô người dùng tiếp cận (Reach) và mức độ ảnh hưởng (Impact: 0.25 đến 3).
- Mức độ tự tin về số liệu (Confidence: 50% đến 100%).
- Ước tính nỗ lực kỹ thuật (Effort: Person-months hoặc Story Points).
- **Điều kiện tiên quyết**:
- Dữ liệu phân tích người dùng sẵn có để tính toán Reach.
- Sự tham gia đánh giá nỗ lực kỹ thuật của Tech Lead / Senior Engineers.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **The RICE Mathematical Formula**: Điểm số ưu tiên được tính bằng công thức toán học: `RICE Score = (Reach × Impact × Confidence) / Effort`.
- **Cost of Delay (CoD) & WSJF**: Trong phương pháp Agile/SAFe, WSJF ưu tiên các công việc có Giá trị trì hoãn cao nhất chia cho Kích thước công việc: `WSJF = Cost of Delay / Job Size` (Làm việc ngắn mà giá trị cao trước).
- **Technical Debt Inclusion**: Nợ kỹ thuật không được coi là việc phụ; nợ kỹ thuật được tính điểm RICE dựa trên Impact giảm thiểu rủi ro hệ thống và Effort dọn dẹp.
- **Quy tắc quyết định kỹ thuật**:
- **Tự Tin Thấp Bắt Buộc Giảm Điểm**: Nếu tính năng không có số liệu chứng minh (chỉ là dự đoán), điểm Confidence tối đa chỉ được đặt là 50% (0.5), tự động hạ thứ hạng ưu tiên.
- **Quy Chuẩn Nỗ Lực Tối Thiểu 0.5**: Điểm Effort không bao giờ được đặt bằng 0; tối thiểu là 0.5 (nửa tháng người) để phản ánh chi phí kiểm thử, review và phát hành.
- **Ưu Tiên Mở Khóa Điểm Nghẽn Đồ Thị (Bottleneck First)**: Nếu tính năng A là điều kiện tiên quyết (Prerequisite) để phát triển 3 tính năng khác, tính năng A sẽ được cộng điểm ưu tiên phụ thuộc.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lạm phát điểm Impact (Tất cả tính năng đều được chấm 3 - Massive)**: Do Product Manager muốn đẩy tính năng của mình lên đầu -> Khắc phục: Chuẩn hóa thang đo Impact bằng rubric rõ ràng (3 = Tăng doanh thu >20%, 2 = Tăng >10%, 1 = Tăng 5%, 0.5 = Nhỏ, 0.25 = Tối thiểu).
- **Bỏ quên nợ kỹ thuật khiến hệ thống sập khi tính năng mới ra mắt**: Chỉ ưu tiên tính năng người dùng thấy được -> Khắc phục: Dành cố định tỷ trọng 20-30% dung lượng Sprint (Capacity Allocation) riêng cho các đầu việc hạ tầng và nợ kỹ thuật.

## 6. Step-by-Step Execution Workflow
1. Thu thập và chuẩn hóa danh sách các ứng viên tính năng vào bảng đánh giá.
2. Ước tính Reach: Số lượng người dùng sẽ tiếp xúc với tính năng trong một khung thời gian (ví dụ 1 quý).
3. Đánh giá Impact theo thang chuẩn: 3 (Massive), 2 (High), 1 (Medium), 0.5 (Low), 0.25 (Minimal).
4. Đánh giá Confidence dựa trên bằng chứng: 100% (High confidence - có số liệu analytics), 80% (Medium - có phỏng vấn người dùng), 50% (Low - chỉ là giả định).
5. Kỹ sư ước tính Effort theo Person-months.
6. Áp dụng công thức tính RICE Score và sắp xếp danh sách từ cao xuống thấp.
7. Rà soát đồ thị phụ thuộc kỹ thuật (Dependency Graph) để điều chỉnh thứ tự thực thi hợp lý.
8. Trình bày kết quả minh bạch cho các bên liên quan và chốt Sprint/Quarterly Roadmap.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# RICE Prioritization Matrix (Q4 Engineering Backlog)

| Hạng | Tên Tính Năng / Sáng Kiến | Reach (Người/Q) | Impact (0.25-3) | Confidence (50-100%) | Effort (Person-M) | **RICE Score** | Quyết Định |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **1** | Thanh toán 1-Click Apple/Google Pay | 50,000 | 2.0 (High) | 100% (1.0) | 1.0 | **100,000** | **Làm ngay (Sprint 1)** |
| **2** | Nâng cấp DB Connection Pool & Read Replica | 80,000 | 1.0 (Medium) | 100% (1.0) | 1.0 | **80,000** | **Làm ngay (Tech Debt)** |
| **3** | Tự động hoàn thuế VAT điện tử | 5,000 | 3.0 (Massive) | 80% (0.8) | 1.5 | **8,000** | **Xếp sau (Sprint 3)** |
| **4** | Giao diện Dark Mode tùy biến theme | 20,000 | 0.5 (Low) | 80% (0.8) | 2.0 | **4,000** | **Tạm hoãn** |
| **5** | Đề xuất sản phẩm bằng mô hình GenAI | 10,000 | 2.0 (High) | 50% (0.5) | 3.0 | **3,333** | **Cần làm Discovery thêm** |
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính toán công thức RICE: Xác nhận điểm số được tính chính xác bằng thuật toán: `python -c "reach=50000; impact=2.0; conf=1.0; effort=1.0; print((reach*impact*conf)/effort)"`
- Kiểm tra chu trình phụ thuộc trong backlog: Chạy script kiểm tra đồ thị phụ thuộc không có vòng lặp (A phụ thuộc B, B phụ thuộc A)
- Rà soát tỷ lệ phân bổ tài nguyên: Xác nhận ít nhất 20% effort được phân bổ cho Tech Debt và Reliability

## 8. Anti-Patterns & Common Traps
- **Xếp ưu tiên theo người nói to nhất trong phòng họp**: Phá vỡ tính kỷ luật của kỹ thuật dựa trên dữ liệu.
- **Thay đổi độ ưu tiên liên tục giữa chừng Sprint**: Gây lãng phí công sức chuyển đổi ngữ cảnh (Context Switching Cost).
- **Tách riêng backlog kỹ thuật và backlog sản phẩm**: Khiến việc kỹ thuật không bao giờ được ưu tiên thực thi.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các tính năng đưa vào kế hoạch quý đều có điểm số RICE định lượng kèm bằng chứng.
- QG-04: Đồ thị phụ thuộc kỹ thuật không có chu trình phụ thuộc khép kín.
- QG-11: Tỷ lệ phân bổ năng lực đáp ứng tối thiểu 20% cho nợ kỹ thuật và an ninh hạ tầng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Các sáng kiến khắc phục lỗ hổng bảo mật nghiêm trọng (CRITICAL Security Vulnerabilities) có quyền ưu tiên đặc cách (Security Override) không cần qua chấm điểm RICE thông thường.
- Không chia sẻ dữ liệu doanh thu chi tiết trong bảng RICE cho các bên không có thẩm quyền.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Bảng tính ma trận ưu tiên RICE Matrix hoàn chỉnh.
- Sơ đồ đồ thị phụ thuộc giữa các tính năng (Feature Dependency Graph).
- Lộ trình phát triển sản phẩm (Product Roadmap) có sự đồng thuận của các bên.

## 13. Related & Complementary Skills
- `dex-product-discovery`: Cung cấp dữ liệu đầu vào và các giải pháp đã kiểm chứng cho RICE.
- `dex-technical-debt-refactoring`: Đưa các hạng mục nợ kỹ thuật vào bảng đánh giá ưu tiên.
- `dex-runbook-automation`: Tối ưu hóa quy trình vận hành để giải phóng effort cho tính năng mới.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ có Product Manager muốn làm tính năng Dark Mode (được khách hàng yêu cầu nhiều trên Twitter), trong khi Tech Lead yêu cầu nâng cấp cụm Database đang quá tải. Áp dụng `dex-feature-prioritization`, bảng tính RICE chỉ ra rằng việc nâng cấp Database có Reach 80,000 người dùng, độ tự tin 100% và ngăn ngừa nguy cơ sập toàn hệ thống, đạt điểm RICE 80,000, trong khi Dark Mode chỉ đạt 4,000 điểm. Nhờ số liệu toán học minh bạch, Product Manager vui vẻ đồng ý nhường ưu tiên cho việc nâng cấp hạ tầng trước.
