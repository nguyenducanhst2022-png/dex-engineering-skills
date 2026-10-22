---
name: dex-usability-study-design
description: Design, facilitate, and synthesize task-based usability studies (moderated and unmoderated) using think-aloud protocols and SUS scoring. Use to uncover behavioral UX defects before shipping products.
---

# dex-usability-study-design

## 1. Purpose & Scope
Thiết kế, điều phối và tổng hợp kết quả các buổi nghiên cứu trải nghiệm người dùng dựa trên nhiệm vụ (Task-based Usability Studies: có người điều phối Moderated hoặc tự thực hiện Unmoderated); áp dụng giao thức suy nghĩ thành tiếng (Think-aloud Protocol) và thang đo chuẩn hóa SUS (System Usability Scale) nhằm phát hiện sớm các rào cản hành vi trước khi phát hành sản phẩm.

## 2. When to Use
- Trước khi phát hành một tính năng lớn hoặc một ứng dụng mới ra thị trường.
- Khi chỉ số gắn bó của người dùng (User Retention) sụt giảm bất thường mà dữ liệu số liệu (Quantitative Data) không giải thích được lý do tại sao.
- Kiểm chứng các giả thuyết thiết kế giữa 2 phương án UI/UX cạnh tranh nhau.

## 3. When NOT to Use
- Không biến buổi thử nghiệm thành một buổi giới thiệu hay thuyết phục người dùng rằng 'tính năng này hay lắm'.
- Không đặt các câu hỏi dẫn dắt (Leading questions) kiểu như: 'Bạn có thấy nút này rất dễ bấm không?'.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Bản mẫu thử nghiệm tương tác (Figma Prototype hoặc Staging App).
- Danh sách các nhiệm vụ cụ thể cần người dùng thực hiện (Core Tasks).
- Tiêu chuẩn tuyển chọn người tham gia (Participant Screener).
- **Điều kiện tiên quyết**:
- Có kịch bản hướng dẫn người điều phối (Moderator Guide) và hệ thống ghi hình/ghi màn hình được người dùng đồng thuận.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Think-Aloud Protocol: Hướng dẫn người dùng liên tục nói ra những gì họ đang nghĩ, đang tìm kiếm và cảm thấy bối rối trong đầu khi thao tác trên màn hình.
- Quan sát Hành vi > Lắng nghe Lời nói: Những gì người dùng làm (vấp váp, bấm nhầm, tìm kiếm) phản ánh sự thật chính xác hơn nhiều so với những lời khen lịch sự của họ.
- System Usability Scale (SUS): Bộ 10 câu hỏi trắc nghiệm chuẩn quốc tế tính ra điểm số từ 0 đến 100. Điểm trung bình chuẩn là 68. Điểm > 80 là sản phẩm xuất sắc.
- **Quy tắc quyết định kỹ thuật**:
- Chỉ cần kiểm thử trên 5 người dùng cho mỗi nhóm đối tượng là đã có thể phát hiện được 85% các lỗi trải nghiệm lớn nhất (Quy tắc Nielsen Norman Group).
- Bất kỳ nhiệm vụ nào có tỉ lệ thất bại > 40% bắt buộc phải thiết kế lại trước khi release.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Người điều phối nhảy vào can thiệp hoặc chỉ dẫn khi thấy người dùng bị kẹt, làm mất đi cơ hội quan sát xem người dùng thực tế sẽ tự xoay xở như thế nào.

## 6. Step-by-Step Execution Workflow
1. Xây dựng Kịch bản Nhiệm vụ (Task Scenarios) thực tế, không dùng thuật ngữ định hướng.
2. Tuyển chọn 5-8 người dùng đúng tệp khách hàng mục tiêu.
3. Tiến hành các phiên thử nghiệm 45 phút, ghi lại màn hình và biểu cảm.
4. Cho người dùng điền bảng khảo sát điểm số SUS ngay sau buổi thử nghiệm.
5. Phân tích băng ghi hình, trích xuất các khoảnh khắc người dùng bối rối và lập bảng ưu tiên sửa lỗi.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# Usability Test Task Scenario
**Nhiệm vụ:** Bạn vừa chuyển nhà sang địa chỉ mới. Hãy tìm cách cập nhật địa chỉ giao hàng mặc định của bạn thành '123 Đường Lê Lợi, Quận 1, TP.HCM' và kiểm tra xem đơn hàng tiếp theo có áp dụng địa chỉ này không.

*Tiêu chí thành công của kỹ sư quan sát:*
- Người dùng tìm thấy mục cài đặt địa chỉ trong vòng dưới 60 giây.
- Người dùng không bấm nhầm vào mục 'Đổi thông tin thanh toán'.
- Hoàn tất không cần sự trợ giúp của người điều phối.
```

### Lệnh xác minh & thực thi:
```bash
# Tính toán điểm số SUS tự động từ file khảo sát csv
python scripts/calculate_sus_score.py --input survey_results.csv
```

## 8. Anti-Patterns & Common Traps
- Giúp đỡ người dùng khi họ lúng túng trong buổi kiểm thử.
- Coi phản hồi của một người dùng duy nhất là chân lý tuyệt đối mà không đối soát với các người dùng khác.

## 9. Quality Gates & Acceptance Criteria
- Điểm số System Usability Scale (SUS) đạt tối thiểu 75/100.
- Tỉ lệ hoàn thành nhiệm vụ cốt lõi (Task Completion Rate) đạt trên 85% không cần trợ giúp.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Bảo vệ quyền riêng tư: xóa toàn bộ các đoạn video ghi lại mật khẩu hoặc thông tin cá nhân của người tham gia thử nghiệm.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Báo cáo nghiên cứu khả năng sử dụng (Usability Findings Report).
- Điểm số SUS và danh sách video clip minh chứng các điểm nghẽn trải nghiệm.

## 13. Related & Complementary Skills
dex-user-journey-mapping, dex-accessibility-automation, dex-product-requirements-writing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ y tế chuẩn bị phát hành app đặt lịch khám bác sĩ. Qua buổi kiểm thử khả năng sử dụng với 5 bệnh nhân lớn tuổi, họ phát hiện 4/5 người không thể chọn được ngày khám vì giao diện lịch dùng font chữ quá mờ và các nút bấm quá sát nhau. Nhờ phát hiện trước khi ra mắt, nhóm đã tăng kích thước vùng chạm nút bấm và độ tương phản, giúp bệnh nhân lớn tuổi đặt lịch dễ dàng.
