---
name: dex-multi-agent-orchestration
description: Multi-agent coordination, role division, concurrent subagent task execution, cross-agent peer reviews, and conflict-free code integration. Prevents collision between autonomous agents. Use when orchestrating multiple specialized agents, running parallel engineering tracks, or conducting peer agent reviews.
---

# DEX Multi-Agent Orchestration

## 1. Purpose
Điều phối nhiều AI Agent cùng tham gia phát triển một dự án phần mềm một cách có trật tự, phân chia vai trò rõ ràng, cho phép thực thi song song trên các vùng mã nguồn biệt lập, thực hiện review chéo lẫn nhau và hợp nhất mã nguồn an toàn dưới sự giám sát của một Agent điều phối trung tâm.

Quy trình đa Agent chuẩn:
`Phân tích → Chia nhiệm vụ → Phân công Agent → Thực thi song song → Review chéo → Tích hợp code → Kiểm thử → Sửa lỗi → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Mỗi AI Agent đảm nhiệm một vai trò duy nhất và rõ ràng. Duy nhất một Agent điều phối toàn bộ dự án để tránh xung đột mã nguồn và mất kiểm soát.**
Ghi nhớ sống còn: **Nhiều AI Agent không đồng nghĩa với hiệu quả cao hơn. Hiệu quả chỉ đến từ phân công đúng, phối hợp tốt và kiểm chứng kết quả chéo.**

## 2. When to Use
- Khi dự án có nhiều module độc lập có thể phát triển song song (ví dụ: Frontend Agent, Backend API Agent, Database Migration Agent, QA Test Agent).
- Khi cần một Agent chuyên trách đóng vai trò Reviewer để kiểm tra mã nguồn do Agent Coder viết ra trước khi hợp nhất.
- Khi một nhiệm vụ quá lớn vượt quá giới hạn ngữ cảnh (Context Window) của một Agent đơn lẻ.

## 3. When Not to Use
- Nhiệm vụ nhỏ, sửa lỗi cục bộ trong 1-2 file mà một Agent có thể giải quyết nhanh chóng trong 1 bước.
- Khi các tác vụ có tính phụ thuộc tuần tự chặt chẽ (Task B bắt buộc phải có output của Task A mới bắt đầu được).

## 4. Inputs
- Danh sách các vai trò Agent chuyên biệt (Orchestrator, Frontend Engineer, Backend Engineer, QA Engineer, Security Reviewer).
- Bản phân rã nhiệm vụ và ma trận vùng mã nguồn độc lập (File isolation boundaries).
- Kênh giao tiếp và quy ước payload trao đổi giữa các Agent.

## 5. Workflow

### Bước 1: Phân Rã & Cách Ly Vùng Mã Nguồn (Task & Code Isolation)
- Agent điều phối (Lead Orchestrator) phân chia dự án thành các phần độc lập tuyệt đối:
  - Agent A (Backend): Toàn quyền trên thư mục `backend/`, cấm sửa `frontend/`.
  - Agent B (Frontend): Toàn quyền trên thư mục `frontend/`, cấm sửa `backend/`.
  - Agent C (QA): Soạn thảo và chạy các bài kiểm tra E2E độc lập trong `tests/e2e/`.

### Bước 2: Phân Công & Giao Nhiệm Vụ (Explicit Assignment)
- Orchestrator gửi Task Brief cụ thể cho từng Agent con (sử dụng chuẩn `dex-task-delegation`), nêu rõ: Mục tiêu, Giới hạn thư mục, API Contract và Tiêu chí nghiệm thu.

### Bước 3: Thực Thi Song Song Độc Lập (Parallel Execution)
- Các Agent con làm việc song song trên các nhánh Git riêng biệt (ví dụ `agent/backend-feature` và `agent/frontend-feature`).
- Mỗi Agent tự thực hiện quy trình `Analyze → Implement → Verify` trong phạm vi của mình.

### Bước 4: Kiểm Tra Chéo (Cross-Agent Peer Review)
- Khi một Agent con hoàn thành: Mã nguồn của nó được chuyển giao cho Agent Reviewer (hoặc Orchestrator) để tiến hành Code Review:
  - Kiểm tra xem có vi phạm phạm vi thư mục không?
  - Kiểm tra xem code có đáp ứng đúng API Contract đã thỏa thuận không?
  - Đánh giá chất lượng và chạy lại bộ test của Agent đó.

### Bước 5: Hợp Nhất & Tích Hợp Tập Trung (Central Integration)
- Duy nhất Agent điều phối trung tâm được phép thực hiện lệnh Merge các nhánh con vào nhánh chính.
- Tiến hành chạy toàn bộ bộ kiểm thử tích hợp chung (Integration Test Suite) để xác nhận các phần ghép nối hoàn hảo với nhau.

### Bước 6: Xử Lý Xung Đột & Ổn Định (Conflict Resolution & Stabilization)
- Nếu phát sinh xung đột tích hợp: Agent điều phối yêu cầu Agent gây xung đột điều chỉnh lại, hoặc tự mình giải quyết dựa trên API contract chuẩn.

## 6. Quality Gates
- **QG-01 (Strict Boundary Isolation)**: Không có bất kỳ Agent con nào chỉnh sửa file ngoài vùng được phân quyền.
- **QG-05 (All Subagent Tests PASS)**: 100% bài kiểm thử của tất cả các Agent con đều đạt PASS.
- **QG-08 (Cross-Review Approved)**: Có xác nhận phê duyệt (APPROVE) từ Agent Reviewer trước khi merge.

## 7. Safety Rules (4 Nguyên Tắc Multi-Agent)
1. **Task Isolation (Phân lập nhiệm vụ)**: Phân chia nhiệm vụ và vùng mã nguồn rõ ràng, không để hai Agent cùng sửa một file cùng thời điểm.
2. **Parallel Execution (Thực thi song song có chọn lọc)**: Chỉ chạy song song những công việc thực sự độc lập.
3. **Cross Review (Kiểm tra chéo)**: Agent viết code không được tự duyệt code của chính mình; phải có Agent khác hoặc Orchestrator kiểm chứng.
4. **Central Orchestration (Một đầu mối điều phối)**: Luôn có một Agent trưởng làm đầu mối kiểm soát tích hợp, ngăn chặn tình trạng hỗn loạn "nhiều thầy nhiều ma".

## 8. Expected Outputs
1. Bản đồ phân công công việc (Agent Assignment Matrix).
2. Các nhánh Git tính năng độc lập từ các Agent con.
3. Báo cáo Review chéo giữa các Agent.
4. Nhánh mã nguồn tích hợp hoàn chỉnh và ổn định.

## 9. Failure Handling
- Nếu một Agent con bị lỗi hoặc tạo code sai lệch hợp đồng: Orchestrator lập tức cô lập nhánh của Agent đó, yêu cầu sửa lỗi trong phạm vi cô lập, không để lỗi lây lan sang các Agent khác.

## 10. Completion Criteria
- Tất cả các Agent con hoàn thành nhiệm vụ được giao.
- Toàn bộ mã nguồn được hợp nhất thành công không còn xung đột.
- Test tích hợp toàn hệ thống đạt 100% PASS.

---

## Real-world Example
Xây dựng tính năng "Xuất báo cáo PDF":
1. *Orchestrator*: Thỏa thuận interface: `POST /api/reports/pdf` trả về PDF stream.
2. *Agent Backend*: Viết service sinh PDF bằng Puppeteer trong `src/services/pdf/`, chạy 5 unit tests PASS.
3. *Agent Frontend*: Viết nút "Tải PDF" và xử lý download blob trong `src/components/ReportView/`, chạy 3 component tests PASS.
4. *Review chéo*: Agent Backend kiểm tra payload frontend gửi lên → Khớp 100%.
5. *Orchestrator*: Merge cả 2 nhánh và chạy E2E test tải thử file PDF thật thành công.
