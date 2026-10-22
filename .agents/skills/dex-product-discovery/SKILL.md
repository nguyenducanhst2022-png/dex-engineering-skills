---
name: dex-product-discovery
description: Structure product discovery, user research synthesis, Jobs-to-be-Done (JTBD), opportunity solution trees, assumption testing, and rapid prototyping hypotheses. Use when validating what to build before writing production code.
---

# dex-product-discovery

## 1. Purpose & Scope
Thiết kế và chuẩn hóa quy trình khám phá sản phẩm (Product Discovery Framework) theo phương pháp kỹ thuật dựa trên dữ liệu và bằng chứng; chuyển hóa các nhu cầu mơ hồ của người dùng thành bài toán kỹ thuật rõ ràng; áp dụng khung lý thuyết Khách hàng Thuê Sản phẩm Làm Việc Gì (Jobs-to-be-Done - JTBD), xây dựng Cây Cơ Hội - Giải Pháp (Opportunity Solution Tree), lập bản đồ giả định rủi ro (Assumption Mapping: Feasibility, Viability, Usability) và thiết kế các kịch bản thử nghiệm nhanh (Rapid Prototypes / Spike Experiments) trước khi đầu tư nguồn lực viết mã nguồn thực tế.

## 2. When to Use
- Khi nhận được yêu cầu tính năng lớn từ ban giám đốc hoặc khách hàng nhưng chưa rõ giải pháp nào mang lại giá trị thực tế cao nhất.
- Khi đội ngũ kỹ thuật có nguy cơ tốn 2 tháng phát triển một tính năng phức tạp nhưng khi ra mắt không ai sử dụng (Feature Factory Trap).
- Khi cần xác thực tính khả thi kỹ thuật (Technical Feasibility) và mức độ chấp nhận của người dùng (Value Risk) cho một ý tưởng mới.

## 3. When NOT to Use
- Tối ưu hóa thuật toán hoặc sửa lỗi phần mềm cụ thể (dùng `dex-root-cause-debugging`).
- Thiết lập pipeline tự động hóa CI/CD (dùng `dex-cicd-automation`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Dữ liệu phỏng vấn người dùng, phản hồi khách hàng (Customer Feedback) và số liệu sử dụng thực tế (Product Analytics).
- Mục tiêu chiến lược của doanh nghiệp (OKRs: Tăng tỷ lệ chuyển đổi, giảm tỷ lệ rời bỏ).
- Năng lực công nghệ hiện tại và các ràng buộc thời gian/chi phí.
- **Điều kiện tiên quyết**:
- Có quyền tiếp cận người dùng mục tiêu hoặc kho dữ liệu phản hồi của khách hàng.
- Sự đồng thuận giữa Product Manager, Tech Lead và Product Designer.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Jobs-to-be-Done (JTBD) Paradigm**: Người dùng không mua sản phẩm của bạn; họ 'thuê' sản phẩm để giải quyết một bước tiến triển trong cuộc sống của họ: `Khi [Hoàn cảnh], tôi muốn [Động lực], để tôi có thể [Kết quả mong đợi]`.
- **Opportunity Solution Tree (Teresa Torres)**: Mô hình hình cây nối từ Mục tiêu kinh doanh (Outcome) -> Các cơ hội / Nỗi đau của người dùng (Opportunities) -> Các giải pháp tiềm năng (Solutions) -> Các thí nghiệm kiểm chứng (Experiments).
- **Risk Quadruple (Marty Cagan)**: 4 rủi ro sản phẩm lớn cần kiểm chứng: Giá trị (Value: Người ta có mua không?), Khả năng sử dụng (Usability: Người ta có biết dùng không?), Tính khả thi (Feasibility: Kỹ sư có làm được không?), Khả thi kinh doanh (Viability: Có sinh lời và hợp pháp không?).
- **Quy tắc quyết định kỹ thuật**:
- **Không Viết Mã Nguồn Sản Xuất Khi Chưa Kiểm Chứng Rủi Ro Giá Trị**: Cấm nhảy thẳng vào lập trình khi chưa xác thực được tối thiểu 5-10 người dùng sẵn sàng sử dụng giải pháp.
- **Kiểm Thử Kỹ Thuật Bằng Spike Ngắn Hạn (Time-boxed Spikes)**: Tác vụ kiểm tra tính khả thi kỹ thuật không được kéo dài quá 2-3 ngày làm việc của 1 kỹ sư.
- **Đo Lường Bằng Kết Quả (Outcomes) Thay Vì Đầu Ra (Outputs)**: Thành công không đo bằng số lượng tính năng hoàn thành (Story Points), mà đo bằng sự thay đổi hành vi tích cực của người dùng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Xây dựng giải pháp kỹ thuật quá hoàn hảo cho một bài toán không ai quan tâm**: Mất 3 tháng xây kiến trúc Microservices phân tán cho một tính năng mà chỉ 2 người dùng bấm thử -> Khắc phục: Dùng phương pháp Fake Door Test hoặc Prototype trên Figma để đo lường nhu cầu trước.
- **Hỏi người dùng 'Bạn có muốn tính năng X không?'**: Người dùng luôn trả lời 'Có' nhưng không bao giờ dùng khi ra mắt -> Khắc phục: Phỏng vấn hành vi trong quá khứ ('Lần gần đây nhất bạn gặp vấn đề này là khi nào?') thay vì hỏi ý kiến tương lai.

## 6. Step-by-Step Execution Workflow
1. Xác định Mục tiêu Kinh doanh mong đợi (Desired Outcome: ví dụ Giảm thời gian tạo hóa đơn từ 5 phút xuống 1 phút).
2. Phân tích dữ liệu phỏng vấn và trích xuất các nỗi đau chính của người dùng theo cấu trúc JTBD.
3. Xây dựng Cây Cơ Hội - Giải Pháp: Nhóm các giải pháp tương ứng với từng nỗi đau.
4. Lập Bản đồ Giả định (Assumption Mapping): Phân loại các giả định theo 2 trục: Mức độ quan trọng (Importance) và Mức độ chắc chắn (Uncertainty).
5. Lựa chọn giả định rủi ro cao nhất (Top Leap-of-Faith Assumptions) để thiết kế thí nghiệm.
6. Thực thi Spike kỹ thuật hoặc nguyên mẫu thử nghiệm (Clickable Prototype, Wizard of Oz, Landing Page Test) trong 1 tuần.
7. Tổng hợp bằng chứng định lượng/định tính và ra quyết định: Triển khai (Build), Điều chỉnh (Pivot), hoặc Hủy bỏ (Kill).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# Opportunity Solution Tree & Assumption Test Canvas

### 1. Desired Outcome
Tăng tỷ lệ hoàn tất onboarding thành công của người dùng doanh nghiệp từ 42% lên 65% trong Quý 4.

### 2. Opportunity (Nỗi đau người dùng)
"Người dùng gặp khó khăn và tốn quá nhiều thời gian khi nhập thủ công 50 danh mục sản phẩm vào hệ thống mới."
- **JTBD**: "Khi tôi mới chuyển sang dùng phần mềm mới, tôi muốn nhập kho hàng cũ nhanh chóng, để tôi có thể bắt đầu bán hàng ngay trong ngày."

### 3. Potential Solutions
- **Giải pháp A**: Cung cấp file mẫu Excel và bộ import thông minh tự khớp cột.
- **Giải pháp B**: Tính năng dùng AI chụp ảnh hóa đơn giấy/bảng giá tự sinh danh mục.
- **Giải pháp C**: Tích hợp API đồng bộ 1-click từ nền tảng cũ (Shopify, KiotViet).

### 4. Assumption Mapping & Experiment (Giải pháp B - AI Scanning)
- **Giả định tính khả thi (Feasibility)**: Mô hình OCR/Vision AI có thể nhận diện chính xác >90% tên sản phẩm và giá từ ảnh chụp mờ.
- **Thí nghiệm kiểm chứng (Spike)**: Kỹ sư làm 1 script Python gọi Claude Vision API test trên mẫu 30 ảnh hóa đơn thực tế của khách hàng (Time-box: 2 ngày).
- **Tiêu chuẩn thành công**: Tỷ lệ nhận diện đúng >= 90% với thời gian phản hồi < 3 giây.
- **Kết quả thực tế**: Đạt 94% độ chính xác. Đủ điều kiện kỹ thuật để đưa vào backlog phát triển chính thức.
```

### Lệnh xác minh & thực thi:
- Kiểm tra bằng chứng phỏng vấn: Lưu trữ tối thiểu 5 bản ghi chép phỏng vấn người dùng thực tế
- Kiểm tra code Spike thử nghiệm: Chạy script PoC kiểm tra độ chính xác thuật toán: `python spike/test_ocr_accuracy.py`
- Đo lường chỉ số kích hoạt giả định (Fake Door Test Analytics): Kiểm tra tỷ lệ click vào nút thử nghiệm tính năng

## 8. Anti-Patterns & Common Traps
- **Confirmation Bias (Thiên kiến xác nhận)**: Chỉ tìm kiếm các câu trả lời đồng tình với ý tưởng của mình và phớt lờ các phản hồi tiêu cực của người dùng.
- **Nghiên cứu quá đà không chịu ra mắt (Analysis Paralysis)**: Dành 6 tháng nghiên cứu mà không đưa được bất kỳ nguyên mẫu nào ra thử nghiệm.
- **Nhầm lẫn giữa yêu cầu giải pháp của khách hàng và nỗi đau cốt lõi**: Khách hàng đòi 'thêm nút bấm màu đỏ' trong khi nỗi đau thực sự là họ không tìm thấy chức năng tìm kiếm.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Có văn bản tài liệu hóa Opportunity Solution Tree và ít nhất 1 giả định cốt lõi được kiểm chứng.
- QG-02: Tiêu chí thành công định lượng (Success Criteria) được xác lập trước khi tiến hành thí nghiệm.
- QG-06: PoC kỹ thuật (Spike) có mã nguồn kiểm chứng tính khả thi và thời gian chạy rõ ràng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Tuyệt đối không đưa dữ liệu khách hàng thực tế vào các công cụ thử nghiệm của bên thứ ba khi chưa có thỏa thuận bảo mật (NDA/DPA).
- Thông báo rõ ràng cho người dùng khi họ tham gia vào các phiên thử nghiệm sản phẩm sớm.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Bản đồ Cây Cơ Hội - Giải Pháp (Opportunity Solution Tree).
- Tài liệu kiểm chứng giả định (Assumption Testing Canvas).
- Báo cáo kết quả PoC kỹ thuật và đề xuất tính năng cho Backlog.

## 13. Related & Complementary Skills
- `dex-feature-prioritization`: Đưa các cơ hội đã kiểm chứng vào ma trận ưu tiên RICE.
- `dex-analytics-instrumentation`: Gắn chỉ số đo lường hành vi người dùng khi tính năng ra mắt.
- `dex-specification-driven`: Chuyển hóa giải pháp discovery thành đặc tả kỹ thuật chi tiết.

## 14. Realistic Usage Example
### Tình huống thực tế:
Ban giám đốc muốn đội ngũ kỹ thuật xây dựng tính năng 'Hỏi đáp AI trên dữ liệu công ty' mất ước tính 6 tuần công. Thay vì bắt tay vào code ngay, kỹ sư trưởng áp dụng `dex-product-discovery`. Họ tạo một bản nguyên mẫu Spike trong 2 ngày sử dụng giao diện Streamlit đơn giản và cho 15 nhân viên dùng thử. Kết quả phát hiện 80% câu hỏi của người dùng thực chất là tra cứu chính sách nghỉ phép và lương thưởng có sẵn trong sổ tay PDF. Đội ngũ chuyển hướng sang giải pháp tối ưu mục tra cứu nội bộ sẵn có, tiết kiệm được hơn 1 tháng phát triển lãng phí.
