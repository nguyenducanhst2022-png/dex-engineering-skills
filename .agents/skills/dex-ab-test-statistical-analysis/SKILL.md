---
name: dex-ab-test-statistical-analysis
description: Conduct rigorous A/B test statistical analyses, verifying Sample Ratio Mismatch (SRM), applying two-tailed hypothesis tests, CUPED variance reduction, and sequential testing bounds. Use when validating product experiment conclusions without false discovery traps.
---

# dex-ab-test-statistical-analysis

## 1. Purpose & Scope
Thực hiện phân tích thống kê thử nghiệm A/B (A/B Testing Statistical Analysis) nghiêm ngặt; kiểm tra hiện tượng sai lệch tỷ lệ mẫu (Sample Ratio Mismatch - SRM), áp dụng kiểm định giả thuyết hai phía (Two-Tailed Hypothesis Testing), kỹ thuật giảm phương sai CUPED (Controlled-experiment Using Pre-Experiment Data) và cận kiểm định tuần tự (Sequential Testing); ngăn ngừa các cạm bẫy khám phá giả và quyết định sai lầm trong kinh doanh.

## 2. When to Use
- Khi nghiệm thu kết quả của một đợt thử nghiệm A/B tính năng mới để quyết định có nên phát hành chính thức (Rollout 100%) hay không.
- Khi cần kiểm tra xem sự chênh lệch số lượng người dùng giữa nhóm A và nhóm B có phải do lỗi kỹ thuật chia nhóm (SRM) hay không.
- Khi muốn rút ngắn thời gian chạy thử nghiệm từ 4 tuần xuống 2 tuần bằng phương pháp giảm phương sai CUPED.

## 3. When NOT to Use
- Khi thử nghiệm chỉ có vài chục người dùng không đủ quy mô mẫu thống kê (Sample Size).
- Khi kiểm tra sự cố kỹ thuật hạ tầng không liên quan đến hành vi người dùng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Dữ liệu người dùng tham gia thử nghiệm có gắn nhãn nhóm (Variant A / Variant B), công cụ tính toán thống kê (SciPy hoặc script Python).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Sample Ratio Mismatch (SRM):** Hiện tượng tỷ lệ người dùng thực tế giữa nhóm Kiểm soát và nhóm Thử nghiệm bị lệch so với thiết kế (ví dụ kỳ vọng 50:50 nhưng thực tế là 52:48), báo hiệu lỗi kỹ thuật chia nhóm và làm vô hiệu hóa toàn bộ kết quả test.
- **CUPED Variance Reduction:** Tận dụng dữ liệu hành vi của người dùng trước khi thử nghiệm để loại bỏ nhiễu phương sai, giúp phát hiện hiệu ứng nhỏ hơn với cùng dung lượng mẫu.
- **Peeking Problem & Sequential Bounds:** Không được liên tục kiểm tra giá trị p-value mỗi ngày và dừng test ngay khi thấy p < 0.05 (vi phạm nghiêm trọng xác suất thống kê).

## 6. Step-by-Step Execution Workflow
1. Kiểm tra tính hợp lệ của phân phối mẫu bằng bài kiểm định Chi-square ($p > 0.01$) để loại trừ lỗi SRM.
2. Tính toán phương sai ban đầu và áp dụng công thức điều chỉnh CUPED dựa trên dữ liệu pre-experiment.
3. Thực hiện kiểm định t-test hai mẫu độc lập hoặc kiểm định z-test cho tỷ lệ chuyển đổi.
4. Tính toán khoảng tin cậy 95% cho mức độ nâng cao hiệu quả (Relative Lift).
5. Lập biên bản báo cáo kết luận thử nghiệm `EXPERIMENT_DECISION_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# SRM Check & CUPED Variance Reduction
import scipy.stats as stats
import numpy as np

def verify_srm(control_count: int, treatment_count: int) -> tuple[bool, float]:
    total = control_count + treatment_count
    expected = [total / 2.0, total / 2.0]
    chi2, p_val = stats.chisquare([control_count, treatment_count], expected)
    # If p_val < 0.001, SRM is present (Critical Flaw)
    return p_val >= 0.001, p_val

def apply_cuped(y_variant: np.ndarray, x_pre_variant: np.ndarray, x_pre_all: np.ndarray) -> np.ndarray:
    # theta = cov(Y, X) / var(X)
    covariance = np.cov(y_variant, x_pre_variant)[0, 1]
    variance_x = np.var(x_pre_all)
    theta = covariance / variance_x if variance_x > 0 else 0
    return y_variant - theta * (x_pre_variant - np.mean(x_pre_all))
```

## 8. Anti-Patterns & Common Traps
- Liên tục mở dashboard xem p-value mỗi sáng và bấm dừng test ăn mừng ngay khi p-value vừa chạm 0.04 (lỗi 'Peeking Problem' làm tăng tỷ lệ dương tính giả lên 30%).
- Bỏ qua bước kiểm tra SRM, dẫn đến việc đưa ra kết luận kinh doanh dựa trên một mẫu thử nghiệm bị lỗi phân bổ trầm trọng.
- Chạy thử nghiệm cùng lúc 20 biến thể mà không hiệu chỉnh mức ý nghĩa thống kê (lỗi so sánh bội Bonferroni Correction).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Bài kiểm định SRM đạt $p > 0.001$ trước khi tiến hành bất kỳ phân tích số liệu chuyển đổi nào.
- QG-02: Thử nghiệm đạt đủ kích thước mẫu tối thiểu (Minimum Sample Size) đã được tính toán từ trước (Power >= 80%).
- QG-03: Khoảng tin cậy 95% của chỉ số đo lường không cắt qua điểm 0 đối với các tính năng được duyệt rollout.

## 10. Security & Safety Boundaries
- Bảo vệ thông tin chiến lược thử nghiệm kinh doanh; không công khai dữ liệu đo lường doanh thu chi tiết ra ngoài doanh nghiệp.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo phân tích thống kê thử nghiệm `EXPERIMENT_DECISION_REPORT.md`.
1. Script tự động kiểm tra SRM và tính toán CUPED `ab_evaluator.py`.

## 13. Related & Complementary Skills
- [`dex-analytics-cohort-retention`](.agents/skills/dex-analytics-cohort-retention/SKILL.md)
- [`dex-feature-flags`](.agents/skills/dex-feature-flags/SKILL.md)
- [`dex-data-quality-audits`](.agents/skills/dex-data-quality-audits/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Đội ngũ sản phẩm hào hứng vì nút bấm mua hàng mới làm tăng tỷ lệ chuyển đổi 8% với $p = 0.02$. Kỹ sư kích hoạt `dex-ab-test-statistical-analysis` để kiểm toán, phát hiện bài kiểm tra SRM có $p = 0.00001$ (lệch mẫu do một phiên bản Android cũ bị crash không nạp được nhóm B). Sau khi sửa lỗi phân chia nhóm và chạy lại, kết quả thật cho thấy nút mới không hề có tác dụng, cứu công ty khỏi một quyết định thiết kế sai lầm.
