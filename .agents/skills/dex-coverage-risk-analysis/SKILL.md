---
name: dex-coverage-risk-analysis
description: Correlate code coverage metrics with code churn, production defect density, and business criticality to prioritize high-value test engineering. Use when optimizing QA effort and eliminating testing blind spots.
---

# dex-coverage-risk-analysis

## 1. Purpose & Scope
Kết hợp chỉ số độ bao phủ kiểm thử (code coverage) với tần suất sửa đổi mã nguồn (code churn), mật độ lỗi production trong quá khứ và mức độ quan trọng nghiệp vụ để xác định các 'điểm mù nguy hiểm' (high-risk blind spots), từ đó ưu tiên viết test cho những nơi có rủi ro cao nhất thay vì chạy theo 100% coverage hình thức.

## 2. When to Use
- Đội ngũ có nguồn lực hạn chế, không thể nâng độ bao phủ toàn bộ dự án từ 40% lên 90%.
- Sau các sự cố production nghiêm trọng tại những vùng mã nguồn tưởng chừng ít thay đổi.
- Cần chiến lược kiểm thử thực tế cho dự án legacy lớn.

## 3. When NOT to Use
- Không áp dụng quy định cấm merge code máy móc chỉ dựa trên con số phần trăm line coverage thuần túy.
- Không dùng để đánh giá năng suất cá nhân của từng kỹ sư.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Báo cáo coverage chi tiết (lcov.info, coverage.xml).
- Lịch sử Git commits trong 6 tháng gần nhất (git log phân tích churn).
- Danh sách bug tickets và incidents liên quan đến các module.
- **Điều kiện tiên quyết**:
- Có công cụ đo coverage hoạt động trong CI và lịch sử commit Git rõ ràng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Risk-based Testing: Vùng code có Churn cao (thay đổi liên tục) + Coverage thấp = Điểm nóng rủi ro cực đại (Critical Risk Zone).
- Dumb Coverage: 100% coverage ở các file DTO/Constants không mang lại giá trị thực tế.
- **Quy tắc quyết định kỹ thuật**:
- Nếu một file có hơn 10 commits/tháng và coverage < 50%: bắt buộc bổ sung integration test trước khi chấp nhận tính năng mới.
- Nếu file phức tạp (Cyclomatic Complexity > 15) chưa có test: xếp độ ưu tiên kiểm thử mức P0.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Viết thêm hàng loạt test case rỗng không có assert để tăng coverage đối phó với chỉ tiêu của quản lý.

## 6. Step-by-Step Execution Workflow
1. Xuất dữ liệu coverage theo từng file từ test suite hiện tại.
2. Chạy script phân tích Git churn để đếm số lần sửa đổi và số dòng code thay đổi cho từng file.
3. Xây dựng ma trận phân tán (Scatter plot): Trục X là Độ phức tạp/Tần suất sửa đổi, Trục Y là % Coverage.
4. Xác định Top 10 file nằm ở góc nguy hiểm (High Churn / Low Coverage).
5. Lập kế hoạch bổ sung test tập trung đúng vào các nhánh luồng chính của 10 file này.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Phân tích rủi ro kết hợp Git churn và coverage
def calculate_risk_score(churn_count, cyclomatic_complexity, coverage_pct):
    # Điểm rủi ro càng cao càng cần viết test khẩn cấp
    uncovered_factor = (100.0 - coverage_pct) / 100.0
    return (churn_count * 0.4 + cyclomatic_complexity * 0.6) * uncovered_factor
```

### Lệnh xác minh & thực thi:
```bash
# Phân tích nhanh Git churn cho các file trong src/
git log --name-only --format='' --since='3 months ago' src/ | sort | uniq -c | sort -nr | head -n 15
```

## 8. Anti-Patterns & Common Traps
- Ép buộc 100% line coverage toàn bộ dự án dẫn đến các bài test vô bổ chỉ gọi hàm mà không kiểm tra kết quả.
- Bỏ qua các file logic thanh toán phức tạp chỉ vì nó nằm trong hệ thống legacy cũ.

## 9. Quality Gates & Acceptance Criteria
- 100% các file thuộc vùng rủi ro cao (High Churn / High Complexity) phải đạt tối thiểu 80% branch coverage.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Dữ liệu phân tích rủi ro không được chứa thông tin bảo mật hay dữ liệu riêng tư.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Báo cáo ma trận rủi ro Coverage-Churn (Risk Heatmap).
- Danh sách backlog các test cases cần bổ sung theo thứ tự ưu tiên ROI.

## 13. Related & Complementary Skills
dex-mutation-testing, dex-git-flow-and-cherry-picking, dex-unit-testing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty thương mại điện tử có tỉ lệ coverage chung chỉ 52%. Thay vì dàn trải nguồn lực, chuyên gia phân tích ma trận churn-coverage và phát hiện file `coupon_evaluator.py` thay đổi 34 lần trong quý nhưng chỉ có 28% coverage. Họ bổ sung 12 test cases tập trung, chặn đứng 3 lỗi tính sai mã giảm giá trong đợt sale Black Friday.
