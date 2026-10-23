---
name: dex-flaky-test-remediation
description: Systematically detect, isolate, diagnose, and remediate non-deterministic (flaky) tests caused by race conditions, network latency, shared mutable state, and unseeded randomness. Use when CI pipeline reliability drops due to intermittent test failures.
---

# dex-flaky-test-remediation

## 1. Purpose & Scope
Phát hiện, cô lập, chẩn đoán nguyên nhân gốc rễ và xử lý dứt điểm các bài kiểm thử không tiền định (flaky tests - lúc pass lúc fail trên cùng một commit), loại bỏ tình trạng kỹ sư phớt lờ cảnh báo CI hoặc ấn re-run bừa bãi.

## 2. When to Use
- CI pipeline ngẫu nhiên bị fail và pass trở lại khi ấn 'Re-run failed jobs'.
- Xuất hiện các lỗi liên quan đến `TimeoutError`, `Element not found`, hoặc dữ liệu bị trùng lặp.
- Tỉ lệ thành công của build CI tổng thể sụt giảm dưới 95%.

## 3. When NOT to Use
- Không dùng để sửa các lỗi fail nhất quán (deterministic failures do logic bug thật).
- Không áp dụng biện pháp tạm bợ bằng cách tăng `sleep(10)` hoặc gán retry vô tội vạ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Lịch sử chạy CI của các bài test bị nghi ngờ flaky.
- Mã nguồn bài test và phần mềm đang được kiểm thử.
- Log chi tiết và stack trace của các lần fail.
- **Điều kiện tiên quyết**:
- Có khả năng chạy lặp lại bài test độc lập nhiều lần cục bộ (ví dụ: `pytest --count=100` hoặc Playwright repeat).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Root causes của Flaky Test: Race conditions trong async code, phụ thuộc vào timezone/đồng hồ hệ thống, chia sẻ cơ sở dữ liệu chung giữa các luồng test, thứ tự thực thi test không độc lập.
- Quarantining: Tách riêng bài test flaky ra khỏi merge-blocking CI ngay khi phát hiện để bảo vệ năng suất của team trong khi điều tra.
- **Quy tắc quyết định kỹ thuật**:
- Nếu bài test phụ thuộc thời gian: thay thế `time.sleep` bằng `wait_until` condition hoặc mock system clock.
- Nếu bài test xung đột dữ liệu: sử dụng unique ID ngẫu nhiên cho mỗi test session thay vì ID tĩnh.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Xóa luôn bài test flaky thay vì sửa, làm mất vùng phủ kiểm thử đối với logic quan trọng.

## 6. Step-by-Step Execution Workflow
1. Thu thập dữ liệu tần suất fail của bài test trên CI trong 30 ngày qua.
2. Cách ly bài test vào nhóm quarantine (không chặn merge nhưng vẫn ghi log).
3. Tái hiện lỗi trên máy local bằng cách chạy lặp lại 100 lần kèm giả lập CPU throttling và network jitter.
4. Xác định nguyên nhân gốc (shared state, async wait, random seed, time dependency).
5. Tái cấu trúc test sử dụng explicit assertions và isolated fixtures.
6. Chạy xác minh 200 lần liên tiếp không lỗi trước khi đưa bài test trở lại blocking suite.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// TRƯỚC (Flaky):
await page.click('#submit-btn');
await page.waitForTimeout(3000); // Nguy cơ flaky khi mạng chậm!
expect(await page.textContent('#status')).toBe('Done');

// SAU (Ổn định):
await page.click('#submit-btn');
await expect(page.locator('#status')).toHaveText('Done', { timeout: 10000 });
```

### Lệnh xác minh & thực thi:
```bash
# Chạy lặp lại 100 lần để kiểm tra độ ổn định
pytest tests/e2e/test_checkout.py --count=100 -n auto
```

## 8. Anti-Patterns & Common Traps
- Tự động retry 3 lần để che giấu lỗi mà không sửa nguyên nhân gốc.
- Lạm dụng `sleep(5000)` làm phình to thời gian chạy test suite.

## 9. Quality Gates & Acceptance Criteria
- Bài test sau khi sửa phải PASS 100 lần liên tiếp trên CI runner.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Không lưu credential hoặc token thật trong các test fixtures cô lập.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Báo cáo chẩn đoán nguyên nhân gốc của flaky test.
- PR sửa mã nguồn test và dỡ bỏ trạng thái quarantine.

## 13. Related & Complementary Skills
dex-testing-engineering, dex-test-data-management, dex-cicd-automation

## 14. Realistic Usage Example
### Tình huống thực tế:
Một test case E2E Playwright mua hàng hay bị fail vào ban đêm trên CI runner. Chuyên gia phát hiện test case dùng tên user cứng 'testuser', khi chạy song song 2 worker ban đêm bị trùng unique key trong DB. Chuyển sang tạo user `testuser_${Date.now()}` đã dứt điểm lỗi.
