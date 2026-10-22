# -*- coding: utf-8 -*-
"""
Generator for Group M (121-130: Advanced Software Verification) and Group N (131-140: Advanced SRE & Distributed Systems).
Adheres strictly to the Agent Skills Specification with 14 mandatory sections.
"""

import os
import sys

SKILL_TEMPLATE = """---
name: {skill_id}
description: {desc}
---

# {skill_id}

## 1. Purpose & Scope
{purpose}

## 2. When to Use
{activation}

## 3. When NOT to Use
{when_not_to_use}

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
{inputs}
- **Điều kiện tiên quyết**:
{preconditions}

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
{core_concepts}
- **Quy tắc quyết định kỹ thuật**:
{decision_rules}
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
{failure_scenarios}

## 6. Step-by-Step Execution Workflow
{workflow}

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
{example}

### Lệnh xác minh & thực thi:
{verification_commands}

## 8. Anti-Patterns & Common Traps
{anti_patterns}

## 9. Quality Gates & Acceptance Criteria
{quality_gates}
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
{security_constraints}
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
{expected_outputs}

## 13. Related & Complementary Skills
{related_skills}

## 14. Realistic Usage Example
### Tình huống thực tế:
{realistic_usage}
"""

SKILLS_M_N = {
    # 121. dex-static-analysis-rule-authoring
    "dex-static-analysis-rule-authoring": {
        "desc": "Design, test, and tune custom static analysis rules (AST matching, Semgrep, ESLint custom rules, CodeQL) to catch architectural violations, API misuse, and security anti-patterns with near-zero false positives. Use when enforcing custom repo patterns or deprecating risky APIs.",
        "purpose": "Thiết kế, kiểm thử và tinh chỉnh các quy tắc Static Analysis tùy chỉnh (dựa trên Abstract Syntax Tree - AST, Semgrep, ESLint custom plugins, CodeQL queries) nhằm tự động hóa việc phát hiện các vi phạm kiến trúc, lạm dụng API nội bộ và các anti-pattern bảo mật trước khi code được review hoặc merge.",
        "activation": "- Cần ngăn chặn việc sử dụng API nội bộ không an toàn hoặc đã bị deprecated trong codebase lớn.\n- Thiết lập quy chuẩn kiến trúc (ví dụ: cấm import direct Database layer từ Presentation layer).\n- Tự động hóa kiểm tra các lỗ hổng phổ biến mang tính đặc thù của dự án mà scanner mặc định không bắt được.",
        "when_not_to_use": "- Không dùng khi quy tắc có thể giải quyết đơn giản bằng TypeScript type checker hoặc linter có sẵn.\n- Không dùng để kiểm tra tính đúng đắn về mặt logic nghiệp vụ khi runtime (cần integration test).\n- Không dùng cho việc format mã nguồn (dùng Prettier/Black/Biome).",
        "inputs": "- File mã nguồn mẫu chứa đoạn code vi phạm (negative fixtures) và code hợp lệ (positive fixtures).\n- Đặc tả ngữ nghĩa của API hoặc kiến trúc cần cưỡng chế.\n- Công cụ static analysis mục tiêu (Semgrep, ESLint, Python AST).",
        "preconditions": "- Môi trường có cài đặt công cụ phân tích (ví dụ: `semgrep` CLI hoặc `@eslint/rule-tester`).\n- Bộ fixtures kiểm thử được cô lập rõ ràng.",
        "core_concepts": "- Phân tích AST (Abstract Syntax Tree) so với Regex matching thông thường: AST hiểu cấu trúc ngữ cảnh ngữ pháp của ngôn ngữ, tránh các false positive do chú thích hoặc chuỗi ký tự.\n- Tỉ lệ False Positive vs False Negative: Quy tắc tĩnh hữu dụng phải có tỉ lệ false positive gần như bằng 0 để các kỹ sư không bỏ qua cảnh báo.",
        "decision_rules": "- Nếu pattern xuất hiện trong hơn 50 file hiện tại: tạo autofix đi kèm quy tắc.\n- Nếu quy tắc có độ phức tạp phân tích luồng dữ liệu (taint analysis): sử dụng Semgrep Pro/CodeQL thay vì linter AST cơ bản.",
        "failure_scenarios": "- Viết quy tắc quá rộng khiến hàng trăm file vô tội bị báo lỗi làm nghẽn CI.\n- Bỏ qua các trường hợp alias import (`import { riskyFunc as safeFunc }`).",
        "workflow": "1. Thu thập tối thiểu 3 mẫu code vi phạm thực tế và 3 mẫu code hợp lệ tương đương.\n2. Viết biểu thức AST pattern hoặc Semgrep YAML definition.\n3. Chạy kiểm thử trên test fixtures và đo thời gian thực thi (phải dưới 100ms/file).\n4. Tích hợp quy tắc vào CI pipeline dưới chế độ warning trước khi kích hoạt blocking error.",
        "example": "```yaml\nrules:\n  - id: ban-direct-db-import-in-controller\n    languages: [typescript]\n    message: 'Không được import Prisma client trực tiếp trong Controllers. Hãy dùng Service layer.'\n    severity: ERROR\n    pattern: import { $PRISMA } from '@prisma/client'\n    paths:\n      include:\n        - 'src/controllers/**/*.ts'\n```",
        "verification_commands": "```bash\nsemgrep --config rules/custom-rules.yaml tests/fixtures/static-analysis/\n```",
        "anti_patterns": "- Dùng Regex thô ráp thay vì AST parser để phân tích cú pháp ngôn ngữ lập trình.\n- Không tạo negative test fixtures dẫn đến false positives tràn lan.",
        "quality_gates": "- Quy tắc phải bắt được 100% negative fixtures và 0% positive fixtures trong test suite.",
        "security_constraints": "- Quy tắc phân tích tĩnh phải chạy hoàn toàn offline, không gửi mã nguồn lên server bên thứ ba.",
        "expected_outputs": "- File định nghĩa quy tắc (`.semgrep.yml` hoặc plugin file).\n- Bộ test suite fixtures chứng minh độ chính xác.",
        "related_skills": "dex-sast-finding-triage, dex-code-review-excellence, dex-architecture-design",
        "realistic_usage": "Một dự án phát hiện nhiều lập trình viên gọi `db.queryRawUnsafe()` trong Controllers thay vì đi qua Repository. Chuyên gia thiết kế rule Semgrep chặn hoàn toàn pattern này tại pre-commit hook và CI."
    },

    # 122. dex-mutation-testing
    "dex-mutation-testing": {
        "desc": "Evaluate test suite effectiveness by injecting controlled faults (mutations) into source code to verify whether existing tests catch them, identifying assertion weaknesses. Use when improving high-risk system test suites beyond superficial code coverage metrics.",
        "purpose": "Đánh giá chất lượng thực tế của bộ unit test bằng cách cấy các lỗi giả lập (mutations: đổi toán tử, đảo điều kiện boolean, xóa lệnh gọi hàm) vào source code nhằm kiểm chứng xem test suite có phát hiện và fail (kill mutant) hay không, vượt qua nhược điểm đánh lừa của line coverage thông thường.",
        "activation": "- Bộ kiểm thử đạt >80% line coverage nhưng vẫn để lọt lỗi ngớ ngẩn lên production.\n- Các module tài chính, thanh toán, phân quyền hoặc tính toán logic cốt lõi cần độ tin cậy tuyệt đối.\n- Cần xác định các test assertions rỗng hoặc test case vô bổ.",
        "when_not_to_use": "- Không chạy mutation testing trên toàn bộ codebase monorepo lớn mà không có diff/incremental filter vì thời gian chạy rất lâu.\n- Không dùng cho code chỉ chứa boilerplate getters/setters/DTOs.",
        "inputs": "- Source code của module cần kiểm tra.\n- Bộ test suite hiện có của module đó.\n- Cấu hình công cụ mutation testing (`mutmut` cho Python, `Stryker` cho JS/TS, `PITest` cho Java).",
        "preconditions": "- Tất cả unit tests hiện tại phải đang PASS 100% trước khi bắt đầu đột biến.",
        "core_concepts": "- Mutation Score = (Killed Mutants / Total Mutants) * 100.\n- Survived Mutant: Lỗi cấy vào mã nguồn nhưng test suite vẫn PASS => Test assertion yếu hoặc thiếu test case biên.",
        "decision_rules": "- Nếu Mutation Score < 75% trên module cốt lõi: từ chối merge PR cho đến khi bổ sung assertion.\n- Với các mutant sống sót do dead code: loại bỏ dead code thay vì viết test thừa.",
        "failure_scenarios": "- Chạy mutation testing gây infinite loop do đột biến biến đếm vòng lặp (cần cấu hình timeout an toàn cho mỗi test runner).",
        "workflow": "1. Chạy test suite cơ sở để đảm bảo 100% test xanh.\n2. Cấu hình mutation runner cho các tệp đã sửa đổi trong PR (incremental mutation).\n3. Sinh ra mutants và thực thi test suite cho từng mutant.\n4. Phân tích danh sách Survived Mutants và bổ sung assertions thích hợp.\n5. Xuất báo cáo Mutation Score.",
        "example": "```json\n// stryker.config.json\n{\n  \"mutate\": [\"src/core/pricing-calculator.ts\"],\n  \"testRunner\": \"jest\",\n  \"reporters\": [\"html\", \"clear-text\"],\n  \"thresholds\": { \"high\": 85, \"low\": 75, \"break\": 70 }\n}\n```",
        "verification_commands": "```bash\nnpx stryker run\n# Hoặc cho Python:\nmutmut run --paths-to-mutate=src/payment/\n```",
        "anti_patterns": "- Chỉ tin tưởng vào 100% line coverage mà không kiểm tra độ sâu của assertion.\n- Bỏ qua timeout dẫn đến CI treo vô tận khi mutant tạo vòng lặp vô hạn.",
        "quality_gates": "- Mutation Score đạt tối thiểu 80% đối với các module thanh toán và bảo mật.",
        "security_constraints": "- Chỉ thực thi mutation testing trong môi trường sandbox với tài nguyên CPU/RAM được giới hạn.",
        "expected_outputs": "- Báo cáo HTML/JSON về tỉ lệ đột biến bị tiêu diệt.\n- PR cập nhật các test assertions bổ sung.",
        "related_skills": "dex-coverage-risk-analysis, dex-unit-testing, dex-formal-invariant-checks",
        "realistic_usage": "Một hàm tính lãi suất đạt 95% line coverage. Sau khi chạy Stryker, phát hiện mutant đổi `>` thành `>=` vẫn không làm test fail. Đội ngũ kỹ sư đã bổ sung test case tại đúng giá trị ngưỡng biên."
    },

    # 123. dex-api-fuzz-testing
    "dex-api-fuzz-testing": {
        "desc": "Execute coverage-guided and schema-based API fuzz testing (Schemathesis, RESTler) to discover 500 errors, unhandled boundary exceptions, memory leaks, and serialization flaws. Use when hardening REST/GraphQL APIs before production deployment.",
        "purpose": "Thực hiện kiểm thử mờ (Fuzz Testing) tự động trên các giao diện API (REST, GraphQL, gRPC) dựa trên OpenAPI/GraphQL schema, bơm hàng nghìn payload dị dạng, giá trị biên cực đoan và kiểu dữ liệu bất thường để phát hiện lỗi unhandled exceptions (HTTP 500), crash server hoặc rò rỉ dữ liệu.",
        "activation": "- Chuẩn bị phát hành phiên bản API public ra bên ngoài hoặc cho bên thứ ba tích hợp.\n- Cần kiểm tra độ bền vững (resilience) của input validation layer.\n- Sau khi tái cấu trúc lớn bộ phân giải JSON/gRPC parser.",
        "when_not_to_use": "- Không chạy API fuzzing trực tiếp trên môi trường Production đang phục vụ khách hàng thực tế.\n- Không dùng để kiểm thử luồng UI tương tác của người dùng.",
        "inputs": "- OpenAPI Specification (swagger.json/openapi.yaml) hoặc GraphQL Schema.\n- URL endpoint của môi trường Staging/Test được cấp quyền.\n- Thông tin xác thực (Bearer token / API key) của tài khoản test cô lập.",
        "preconditions": "- Môi trường Staging đã được backup dữ liệu và có thể rollback nhanh chóng.\n- Rate limit của môi trường test được điều chỉnh phù hợp cho công cụ fuzz.",
        "core_concepts": "- Schema-based Fuzzing: Dựa trên schema để sinh dữ liệu có cấu trúc hợp lệ về mặt cú pháp nhưng chứa giá trị biên nguy hiểm (ví dụ: chuỗi dài 1MB, số âm cực đại, null bytes, unicode đặc thù).\n- Server Invariant: API không bao giờ được trả về mã lỗi HTTP 500 (Internal Server Error) bất kể payload đầu vào là gì (phải trả về 400 Bad Request hoặc 422 Unprocessable Entity).",
        "decision_rules": "- Nếu bất kỳ request nào kích hoạt HTTP 500: ghi lại payload tối thiểu (minimal reproducible curl) và phân loại là P1 defect.\n- Nếu API bị crash hoặc rò rỉ stack trace: đánh dấu security vulnerability.",
        "failure_scenarios": "- Fuzzer tạo ra quá nhiều bản ghi rác làm đầy cơ sở dữ liệu test (cần cấu hình tự động dọn dẹp hoặc dùng database in-memory).",
        "workflow": "1. Tải và kiểm tra tính hợp lệ của OpenAPI specification.\n2. Cấu hình phạm vi endpoints cho phép fuzz và cấp test auth token.\n3. Chạy Schemathesis hoặc RESTler với kiểm tra các HTTP status invariants.\n4. Phân loại các lỗi HTTP 500 và lỗi timeout thành danh sách reproduction steps.\n5. Sửa lỗi validation trong backend và chạy regression fuzzing.",
        "example": "```bash\nschemathesis run http://localhost:8080/api/v1/openapi.json \\\n  --header \"Authorization: Bearer test-token\" \\\n  --checks all \\\n  --max-response-time 500 \\\n  --hypothesis-max-examples 200\n```",
        "verification_commands": "```bash\n# Xác minh bằng replay curl được sinh ra từ failure log\ncurl -X POST http://localhost:8080/api/v1/orders -H 'Content-Type: application/json' -d '{\"quantity\": -9223372036854775808}'\n```",
        "anti_patterns": "- Fuzzing vào endpoint gửi email thật gây spam người dùng.\n- Bỏ qua các lỗi HTTP 500 với lý do 'người dùng bình thường không bao giờ nhập thế này'.",
        "quality_gates": "- 0 lỗi HTTP 500 phát hiện được qua 10,000 requests fuzzed trên schema.\n- Mọi lỗi input validation phải trả về 4xx kèm error message cấu trúc an toàn.",
        "security_constraints": "- Chỉ thực hiện trên môi trường test nội bộ đã được cấp quyền văn bản.",
        "expected_outputs": "- Báo cáo tổng hợp Schemathesis JSON/HTML.\n- Danh sách cURL reproducer cho từng lỗi phát hiện được.",
        "related_skills": "dex-api-contract-testing, dex-api-abuse-prevention, dex-sast-finding-triage",
        "realistic_usage": "Đội ngũ fintech kiểm tra endpoint chuyển tiền bằng Schemathesis, phát hiện khi gửi số tiền dưới dạng số thực thập phân có 300 chữ số làm microservice Java ném `NumberFormatException` và sập pod. Đội ngũ đã thêm validation regex ngay tại API Gateway."
    },

    # 124. dex-differential-testing
    "dex-differential-testing": {
        "desc": "Compare behavior, output equivalence, and performance between two software implementations (legacy vs rewritten, compiler versions, or competing algorithms) across randomized inputs. Use during major refactorings, system migrations, and re-implementations.",
        "purpose": "So sánh hành vi, kết quả đầu ra và hiệu năng giữa hai phiên bản triển khai phần mềm (hệ thống cũ vs hệ thống viết lại, thuật toán mới vs thuật toán tham chiếu) trên cùng một tập dữ liệu đầu vào ngẫu nhiên hoặc thực tế nhằm phát hiện sai lệch nhỏ nhất về ngữ nghĩa.",
        "activation": "- Thay thế engine tính toán cũ bằng thuật toán mới tối ưu hơn.\n- Di chuyển từ cơ sở dữ liệu SQL sang NoSQL hoặc từ ORM này sang ORM khác.\n- Nâng cấp phiên bản compiler/runtime lớn (ví dụ Node.js 18 lên 22, Python 3.9 lên 3.12).",
        "when_not_to_use": "- Không dùng khi phiên bản mới cố ý thay đổi hoàn toàn API schema và business logic.\n- Không dùng cho các thao tác có side-effect ghi dữ liệu mà không có cơ chế shadow-run/dry-run an toàn.",
        "inputs": "- Triển khai nguồn A (Reference/Legacy implementation).\n- Triển khai nguồn B (Candidate/New implementation).\n- Bộ dữ liệu test cases hoặc generator sinh input ngẫu nhiên.",
        "preconditions": "- Cả hai phiên bản đều có thể chạy song song và nhận cùng định dạng input.",
        "core_concepts": "- Equivalence Oracle: Nếu hai hệ thống có cùng input hợp lệ thì output nghiệp vụ phải tương đương tuyệt đối.\n- Dual-run / Shadowing: Gửi đồng thời request đến cả 2 hệ thống và so sánh kết quả diff ngầm mà không ảnh hưởng tới người dùng.",
        "decision_rules": "- Nếu phát hiện bất kỳ sai khác nào về giá trị logic: ghi nhận minimal reproducer và hoãn release.\n- Nếu sai khác chỉ là thứ tự các key trong JSON: áp dụng canonical JSON normalizer trước khi so sánh.",
        "failure_scenarios": "- Các trường chứa giá trị không tiền định (non-deterministic: timestamps, UUID ngẫu nhiên) gây false diff.",
        "workflow": "1. Xác định hàm hoặc endpoint cần so sánh và các trường cần loại trừ (timestamp, trace-id).\n2. Xây dựng harness gọi song song cả Implementation A và B.\n3. Sinh hàng ngàn inputs ngẫu nhiên (Property-based inputs).\n4. Thu thập và so sánh output diff.\n5. Thu nhỏ input gây lỗi thành minimal reproduction test case.",
        "example": "```python\ndef test_differential_tax_calculation(random_order):\n    legacy_result = legacy_tax_engine.calculate(random_order)\n    new_result = rust_tax_engine.calculate(random_order)\n    assert round(legacy_result.amount, 2) == round(new_result.amount, 2), \\\n        f'Diff detected for input {random_order}: legacy={legacy_result.amount}, new={new_result.amount}'\n```",
        "verification_commands": "```bash\npytest tests/differential/test_tax_engine.py --count=5000\n```",
        "anti_patterns": "- Không chuẩn hóa dữ liệu trước khi so sánh (so sánh chuỗi thô thay vì semantic objects).\n- Chạy differential test trên database thật mà không rollback transaction.",
        "quality_gates": "- 100% kết quả khớp nhau trên 100,000 mẫu dữ liệu kiểm thử.",
        "security_constraints": "- Khi chạy shadow-traffic với dữ liệu thật, phải mask toàn bộ PII và thẻ tín dụng.",
        "expected_outputs": "- Harness code kiểm thử so sánh.\n- Báo cáo phân tích sai lệch và test case hồi quy.",
        "related_skills": "dex-refactoring-mastery, dex-reproducible-benchmarking, dex-unit-testing",
        "realistic_usage": "Một công ty logistics viết lại thuật toán tìm đường đi ngắn nhất từ Python sang C++ để giảm độ trễ. Nhờ differential testing trên 50,000 hành trình giả lập, họ phát hiện trường hợp đường một chiều bị thuật toán C++ xử lý sai lệch so với bản mẫu Python."
    },

    # 125. dex-flaky-test-remediation
    "dex-flaky-test-remediation": {
        "desc": "Systematically detect, isolate, diagnose, and remediate non-deterministic (flaky) tests caused by race conditions, network latency, shared mutable state, and unseeded randomness. Use when CI pipeline reliability drops due to intermittent test failures.",
        "purpose": "Phát hiện, cô lập, chẩn đoán nguyên nhân gốc rễ và xử lý dứt điểm các bài kiểm thử không tiền định (flaky tests - lúc pass lúc fail trên cùng một commit), loại bỏ tình trạng kỹ sư phớt lờ cảnh báo CI hoặc ấn re-run bừa bãi.",
        "activation": "- CI pipeline ngẫu nhiên bị fail và pass trở lại khi ấn 'Re-run failed jobs'.\n- Xuất hiện các lỗi liên quan đến `TimeoutError`, `Element not found`, hoặc dữ liệu bị trùng lặp.\n- Tỉ lệ thành công của build CI tổng thể sụt giảm dưới 95%.",
        "when_not_to_use": "- Không dùng để sửa các lỗi fail nhất quán (deterministic failures do logic bug thật).\n- Không áp dụng biện pháp tạm bợ bằng cách tăng `sleep(10)` hoặc gán retry vô tội vạ.",
        "inputs": "- Lịch sử chạy CI của các bài test bị nghi ngờ flaky.\n- Mã nguồn bài test và phần mềm đang được kiểm thử.\n- Log chi tiết và stack trace của các lần fail.",
        "preconditions": "- Có khả năng chạy lặp lại bài test độc lập nhiều lần cục bộ (ví dụ: `pytest --count=100` hoặc Playwright repeat).",
        "core_concepts": "- Root causes của Flaky Test: Race conditions trong async code, phụ thuộc vào timezone/đồng hồ hệ thống, chia sẻ cơ sở dữ liệu chung giữa các luồng test, thứ tự thực thi test không độc lập.\n- Quarantining: Tách riêng bài test flaky ra khỏi merge-blocking CI ngay khi phát hiện để bảo vệ năng suất của team trong khi điều tra.",
        "decision_rules": "- Nếu bài test phụ thuộc thời gian: thay thế `time.sleep` bằng `wait_until` condition hoặc mock system clock.\n- Nếu bài test xung đột dữ liệu: sử dụng unique ID ngẫu nhiên cho mỗi test session thay vì ID tĩnh.",
        "failure_scenarios": "- Xóa luôn bài test flaky thay vì sửa, làm mất vùng phủ kiểm thử đối với logic quan trọng.",
        "workflow": "1. Thu thập dữ liệu tần suất fail của bài test trên CI trong 30 ngày qua.\n2. Cách ly bài test vào nhóm quarantine (không chặn merge nhưng vẫn ghi log).\n3. Tái hiện lỗi trên máy local bằng cách chạy lặp lại 100 lần kèm giả lập CPU throttling và network jitter.\n4. Xác định nguyên nhân gốc (shared state, async wait, random seed, time dependency).\n5. Tái cấu trúc test sử dụng explicit assertions và isolated fixtures.\n6. Chạy xác minh 200 lần liên tiếp không lỗi trước khi đưa bài test trở lại blocking suite.",
        "example": "```typescript\n// TRƯỚC (Flaky):\nawait page.click('#submit-btn');\nawait page.waitForTimeout(3000); // Nguy cơ flaky khi mạng chậm!\nexpect(await page.textContent('#status')).toBe('Done');\n\n// SAU (Ổn định):\nawait page.click('#submit-btn');\nawait expect(page.locator('#status')).toHaveText('Done', { timeout: 10000 });\n```",
        "verification_commands": "```bash\n# Chạy lặp lại 100 lần để kiểm tra độ ổn định\npytest tests/e2e/test_checkout.py --count=100 -n auto\n```",
        "anti_patterns": "- Tự động retry 3 lần để che giấu lỗi mà không sửa nguyên nhân gốc.\n- Lạm dụng `sleep(5000)` làm phình to thời gian chạy test suite.",
        "quality_gates": "- Bài test sau khi sửa phải PASS 100 lần liên tiếp trên CI runner.",
        "security_constraints": "- Không lưu credential hoặc token thật trong các test fixtures cô lập.",
        "expected_outputs": "- Báo cáo chẩn đoán nguyên nhân gốc của flaky test.\n- PR sửa mã nguồn test và dỡ bỏ trạng thái quarantine.",
        "related_skills": "dex-unit-testing, dex-test-data-management, dex-ci-pipeline-optimization",
        "realistic_usage": "Một test case E2E Playwright mua hàng hay bị fail vào ban đêm trên CI runner. Chuyên gia phát hiện test case dùng tên user cứng 'testuser', khi chạy song song 2 worker ban đêm bị trùng unique key trong DB. Chuyển sang tạo user `testuser_${Date.now()}` đã dứt điểm lỗi."
    },

    # 126. dex-test-data-management
    "dex-test-data-management": {
        "desc": "Architect secure, isolated, synthetic, and ephemeral test data fixtures and databases with automated teardown and masking. Use when managing complex state across integration and end-to-end tests without test pollution.",
        "purpose": "Thiết kế, xây dựng và quản lý dữ liệu kiểm thử (test data) an toàn, biệt lập và có thể dọn dẹp tức thì (ephemeral); tạo lập synthetic data, làm sạch (masking/sanitization) dữ liệu nhạy cảm và bảo đảm tính độc lập giữa các test cases.",
        "activation": "- Các bài test phụ thuộc lẫn nhau do dùng chung cơ sở dữ liệu và sửa đổi cùng một bản ghi.\n- Cần dữ liệu phong phú để test các kịch bản biên nhưng không được dùng dữ liệu production thật do luật bảo mật (GDPR/HIPAA).\n- Quá trình reset database giữa các lần test quá chậm.",
        "when_not_to_use": "- Không dùng dữ liệu thật từ production mà chưa qua quy trình anonymization/masking nghiêm ngặt.\n- Không dùng cho các unit test đơn giản chỉ cần in-memory mocks.",
        "inputs": "- Lược đồ cơ sở dữ liệu (DML/DDL hoặc ORM models).\n- Các quy tắc ràng buộc toàn vẹn dữ liệu.\n- Danh sách các trường nhạy cảm cần ẩn danh (PII).",
        "preconditions": "- Có quyền tạo và hủy database schema tạm thời trong môi trường test (Docker/Testcontainers).",
        "core_concepts": "- Ephemeral Fixtures: Dữ liệu chỉ tồn tại trong phạm vi bài test và được rollback qua database transaction hoặc xóa sạch ngay sau đó.\n- Synthetic Data Generation: Dùng thư viện (Faker, FactoryBoy) sinh dữ liệu hợp lệ về mặt logic nhưng hoàn toàn giả lập.\n- Deterministic Seeding: Khởi tạo dữ liệu mẫu với fixed random seed để tái hiện chính xác lỗi khi cần.",
        "decision_rules": "- Với integration tests: ưu tiên bọc mỗi test case trong một Transaction và Rollback ở teardown.\n- Với E2E tests: sinh account/workspace riêng biệt với UUID ngẫu nhiên cho từng test run.",
        "failure_scenarios": "- Lỗi rò rỉ dữ liệu test vào môi trường production do sai lệch biến môi trường `DATABASE_URL`.",
        "workflow": "1. Phân loại các trường dữ liệu nhạy cảm trong hệ thống.\n2. Xây dựng Factory classes để sinh model entities với các giá trị mặc định an toàn.\n3. Thiết lập cơ chế Transaction Rollback hoặc Docker Testcontainers cho mỗi suite.\n4. Tích hợp kịch bản dọn dẹp dữ liệu mồ côi (cleanup sweep).\n5. Kiểm tra thời gian khởi tạo dữ liệu không vượt quá 10% tổng thời gian chạy test.",
        "example": "```python\nimport factory\nfrom src.models import User\n\nclass UserFactory(factory.Factory):\n    class Meta:\n        model = User\n    \n    id = factory.Faker('uuid4')\n    email = factory.Faker('safe_email')\n    full_name = factory.Faker('name')\n    is_active = True\n```",
        "verification_commands": "```bash\npytest --setup-show tests/integration/\n```",
        "anti_patterns": "- Hardcode ID như `user_id = 1` trong toàn bộ test suite.\n- Copy nguyên database production về máy local để test mà không che PII.",
        "quality_gates": "- 100% dữ liệu thử nghiệm được dọn dẹp sạch sau khi test runner kết thúc.\n- 0 trường PII thực tế nào xuất hiện trong fixtures repository.",
        "security_constraints": "- Tuyệt đối cấm sử dụng số thẻ tín dụng hoặc mật khẩu thật trong test factories.",
        "expected_outputs": "- Module Factories/Fixtures chuẩn hóa.\n- Script seed và reset database tự động.",
        "related_skills": "dex-flaky-test-remediation, dex-database-design, dex-integration-testing",
        "realistic_usage": "Một hệ thống SaaS bị chậm CI do phải seed 50MB SQL dump trước mỗi bài test. Đội ngũ chuyển đổi sang dùng FactoryBoy kết hợp PostgreSQL template databases, giảm thời gian chuẩn bị dữ liệu từ 45 giây xuống còn 800ms cho mỗi worker."
    },

    # 127. dex-compatibility-matrix-testing
    "dex-compatibility-matrix-testing": {
        "desc": "Define, automate, and execute matrix-based compatibility testing across operating systems, runtime versions, browsers, and dependency sets. Use when publishing open-source libraries, CLI tools, or multi-platform applications.",
        "purpose": "Xác định ma trận tương thích, tự động hóa và thực thi kiểm thử trên nhiều hệ điều hành (Ubuntu, macOS, Windows 11), nhiều phiên bản runtime (Node 18/20/22, Python 3.9/3.11/3.13) và các trình duyệt mục tiêu nhằm bảo đảm sản phẩm hoạt động ổn định trên mọi môi trường được hỗ trợ.",
        "activation": "- Phát hành thư viện mã nguồn mở hoặc SDK cho bên thứ ba.\n- Ứng dụng desktop hoặc CLI tool hỗ trợ cả Windows, macOS và Linux.\n- Chuẩn bị deprecate hoặc nâng cấp phiên bản runtime tối thiểu trong chính sách hỗ trợ.",
        "when_not_to_use": "- Không cần ma trận rộng cho ứng dụng web nội bộ chỉ chạy trên một phiên bản Docker container cố định.\n- Không chạy toàn bộ ma trận cho mọi commit nhỏ (dùng pull request filter).",
        "inputs": "- Danh sách OS, architectures (x86_64, arm64) và runtime versions cần hỗ trợ.\n- File cấu hình CI (GitHub Actions matrix).\n- Bộ test suite tích hợp của dự án.",
        "preconditions": "- Test suite có thể chạy không lỗi trên ít nhất một môi trường cơ sở.",
        "core_concepts": "- Combinatorial Matrix: Số lượng trường hợp kiểm thử là tích của các biến (OS x Runtime x Architecture). Cần lược bớt các tổ hợp ít rủi ro để tối ưu chi phí CI.\n- Fast-Fail Matrix: Hủy toàn bộ các job còn lại nếu một job trong ma trận bị lỗi nghiêm trọng để tiết kiệm tài nguyên.",
        "decision_rules": "- Trên commit nhánh feature: chỉ chạy trên 1 OS chính (Ubuntu) và 1 runtime mới nhất.\n- Trên PR vào main hoặc Release tag: bắt buộc chạy 100% ma trận tương thích.",
        "failure_scenarios": "- Mã nguồn sử dụng đường dẫn file phân cách bằng dấu gạch chéo `/` cứng, chạy tốt trên Linux nhưng fail hoàn toàn trên Windows (dùng `path.join` hoặc `pathlib.Path`).",
        "workflow": "1. Khảo sát tỉ lệ người dùng thực tế trên các nền tảng.\n2. Định nghĩa file cấu hình matrix trong GitHub Actions workflow.\n3. Xử lý các điểm khác biệt về OS (đường dẫn file, line endings CRLF vs LF, biến môi trường).\n4. Chạy ma trận và theo dõi các lỗi đặc thù theo từng nền tảng.\n5. Bổ sung các bản vá tương thích và cập nhật tài liệu chính thức.",
        "example": "```yaml\nstrategy:\n  matrix:\n    os: [ubuntu-latest, windows-latest, macos-latest]\n    node-version: [18.x, 20.x, 22.x]\n    exclude:\n      - os: macos-latest\n        node-version: 18.x\n```",
        "verification_commands": "```bash\n# Kiểm thử đa phiên bản cục bộ bằng tox cho Python:\ntox -e py310,py311,py312\n```",
        "anti_patterns": "- Giả định mọi môi trường đều có sẵn Bash shell hoặc các lệnh GNU coreutils.\n- Chạy ma trận quá cồng kềnh ngốn hết hạn mức CI phút hàng tháng.",
        "quality_gates": "- 100% jobs trong ma trận quy định phải PASS trước khi tạo bản release chính thức.",
        "security_constraints": "- Đảm bảo các runners độc lập không chia sẻ file tạm có chứa secrets.",
        "expected_outputs": "- File workflow ma trận CI (`.github/workflows/compat.yml`).\n- Bảng ma trận hỗ trợ chính thức trong tài liệu README.",
        "related_skills": "dex-ci-pipeline-optimization, dex-cross-platform-engineering, dex-python-project-engineering",
        "realistic_usage": "Một CLI tool bằng Node.js hoạt động tốt trên Mac của dev nhưng người dùng Windows báo lỗi không mở được file config. Sau khi đưa Windows runner vào ma trận test, nhóm phát hiện lỗi đọc ký tự xuống dòng CRLF và giải quyết triệt để."
    },

    # 128. dex-reproducible-benchmarking
    "dex-reproducible-benchmarking": {
        "desc": "Design, isolate, measure, and statistically analyze software benchmarks with controlled noise, CPU pinning, warmups, and variance tracking. Use when making performance-critical claims, optimizing algorithms, or preventing regressions.",
        "purpose": "Thiết kế, cô lập môi trường và đo lường benchmark hiệu năng có tính tái lập cao (reproducible); kiểm soát nhiễu hệ thống, thực hiện warmup chu kỳ, cố định CPU core và tính toán phương sai thống kê để bảo đảm các kết luận tối ưu hóa là xác thực.",
        "activation": "- Tuyên bố một thuật toán hoặc thư viện mới nhanh hơn giải pháp hiện tại.\n- Điều tra xem một bản refactor có gây suy giảm hiệu năng (performance regression) hay không.\n- Thiết lập benchmark đường cơ sở (baseline) cho hệ thống trước khi mở rộng quy mô.",
        "when_not_to_use": "- Không đo benchmark trên máy laptop đang cắm sạc/pin chập chờn hoặc đang mở nhiều tab trình duyệt.\n- Không benchmark các hàm có network I/O mà không giả lập độ trễ mạng ổn định.",
        "inputs": "- Đoạn mã nguồn hoặc API cần đo lường.\n- Bộ dữ liệu mẫu có kích thước chuẩn hóa.\n- Công cụ đo chuyên dụng (Criterion.rs, Google Benchmark, pytest-benchmark, Hyperfine).",
        "preconditions": "- Môi trường đo lường phải tắt các tác vụ nền không cần thiết (CPU governor đặt ở chế độ performance).",
        "core_concepts": "- Tái lập (Reproducibility): Chạy 5 lần độc lập vào 5 thời điểm khác nhau phải cho kết quả lệch không quá 3%.\n- JIT Compilation & Warmup: Trong Java/Node.js/V8, code cần chạy hàng ngàn lần trước khi đo để engine JIT tối ưu hóa xong.\n- Độ lệch chuẩn (Standard Deviation) và P99: Giá trị trung bình (Mean) thường che giấu các đột biến nghiêm trọng.",
        "decision_rules": "- Nếu độ lệch chuẩn giữa các lần đo > 5%: loại bỏ kết quả vì môi trường quá nhiễu, chạy lại sau khi khóa tải nền.\n- Đánh giá tối ưu hóa thành công khi hiệu năng tăng tối thiểu 10% với độ tin cậy thống kê 95% (p < 0.05).",
        "failure_scenarios": "- Trình biên dịch (Compiler) tối ưu hóa loại bỏ toàn bộ đoạn code đo lường (Dead Code Elimination) do kết quả không được sử dụng.",
        "workflow": "1. Chuẩn bị môi trường đo: cố định tần số CPU hoặc sử dụng dedicated CI runner.\n2. Viết benchmark harness sử dụng framework chuẩn, tiêu thụ kết quả (black box) để tránh Dead Code Elimination.\n3. Thực hiện giai đoạn Warmup đầy đủ.\n4. Thu thập hàng trăm iterations và ghi nhận phân phối thời gian (P50, P90, P99).\n5. So sánh trực tiếp với baseline bằng công cụ phân tích thống kê.\n6. Lưu trữ kết quả có thể so sánh trong kho dữ liệu benchmark.",
        "example": "```python\ndef test_json_parse_speed(benchmark):\n    payload = generate_standard_json_payload(1000)\n    # Đo thời gian hàm chạy lặp lại nhiều lần kèm warmup tự động\n    result = benchmark(parse_json_fast, payload)\n    assert result is not None\n```",
        "verification_commands": "```bash\npytest tests/benchmarks/ --benchmark-only --benchmark-compare --benchmark-autosave\n```",
        "anti_patterns": "- Đo thời gian chỉ bằng `console.time()` hoặc `time.time()` cho một lần chạy duy nhất.\n- So sánh benchmark chạy trên máy tính cá nhân với máy chủ sản xuất.",
        "quality_gates": "- Mọi tối ưu hóa phải có biểu đồ phân phối trước/sau chứng minh giảm latency P99.",
        "security_constraints": "- Không tải dữ liệu nhạy cảm của khách hàng làm tập mẫu cho public benchmarks.",
        "expected_outputs": "- File báo cáo benchmark (JSON, biểu đồ SVG/HTML).\n- Cam kết hiệu năng với số liệu sai số thống kê rõ ràng.",
        "related_skills": "dex-performance-profiling, dex-differential-testing, dex-jvm-performance-diagnostics",
        "realistic_usage": "Một kỹ sư khẳng định viết lại parser bằng WebAssembly giúp tăng tốc độ 3 lần. Sau khi chạy benchmark chuẩn với Criterion và loại bỏ chi phí FFI overhead, kết quả thực tế cho thấy với payload nhỏ (<1KB) bản WASM thực chất chậm hơn JS gốc 20%."
    },

    # 129. dex-formal-invariant-checks
    "dex-formal-invariant-checks": {
        "desc": "Specify, model, and verify critical domain invariants using stateful property-based testing and formal assertion contracts. Use when guaranteeing correctness in financial ledgers, cryptographic protocols, and consensus mechanisms.",
        "purpose": "Đặc tả, mô hình hóa và kiểm chứng các bất biến nghiệp vụ quan trọng (domain invariants) thông qua Stateful Property-based Testing và Assertion Contracts; đảm bảo rằng bất kể chuỗi hành động nào diễn ra, trạng thái của hệ thống vẫn luôn bảo toàn các quy tắc bất di bất dịch (ví dụ: tổng tiền trong sổ cái luôn cân bằng).",
        "activation": "- Phát triển hệ thống sổ cái tài chính, ví điện tử, sàn giao dịch.\n- Xây dựng máy trạng thái hữu hạn (Finite State Machine) phức tạp.\n- Cần chứng minh tính toàn vẹn dữ liệu trong các điều kiện xử lý đồng thời (concurrency).",
        "when_not_to_use": "- Không tuyên bố đây là 'chứng minh toán học tuyệt đối' (Formal Verification / Coq / TLA+) nếu chỉ chạy property-based testing.\n- Không cần thiết cho các trang CRUD thông tin cá nhân đơn giản.",
        "inputs": "- Danh sách các bất biến nghiệp vụ cốt lõi (Core Invariants).\n- Mô hình máy trạng thái của thực thể.\n- Bộ sinh chuỗi thao tác ngẫu nhiên (Hypothesis, fast-check).",
        "preconditions": "- Hệ thống có thể chuyển trạng thái thông qua các hàm/phương thức rõ ràng.",
        "core_concepts": "- Invariant: Mệnh đề logic luôn đúng trước và sau bất kỳ thao tác hợp lệ nào (ví dụ: `Balance >= 0`, `Total Credits == Total Debits`).\n- Stateful Testing: Sinh ra một chuỗi ngẫu nhiên các lệnh (Nạp -> Rút -> Khóa tài khoản -> Chuyển tiền) và kiểm tra bất biến sau mỗi bước.",
        "decision_rules": "- Nếu bất biến bị vi phạm tại bất kỳ chuỗi lệnh nào: framework phải tự động thu nhỏ chuỗi lệnh (Shrinking) thành chuỗi ngắn nhất để lập trình viên sửa lỗi.\n- Nếu trạng thái không thể phục hồi: ném InvariantViolationException ngay lập tức.",
        "failure_scenarios": "- Bỏ sót một nhánh trạng thái biên trong mô hình khiến lỗ hổng không được kiểm tra.",
        "workflow": "1. Phỏng vấn chuyên gia nghiệp vụ để liệt kê các bất biến toán học và kế toán.\n2. Viết State Machine Model đại diện bằng thư viện property testing (ví dụ: `hypothesis.stateful`).\n3. Định nghĩa các quy tắc chuyển đổi trạng thái (Rules).\n4. Chạy hàng vạn chuỗi thao tác ngẫu nhiên để tìm kiếm chuỗi phá vỡ bất biến.\n5. Thu thập lỗi nhỏ nhất (shrunk example) và tạo regression test.",
        "example": "```python\nfrom hypothesis.stateful import RuleBasedStateMachine, rule, invariant\n\nclass BankLedgerMachine(RuleBasedStateMachine):\n    def __init__(self):\n        super().__init__()\n        self.ledger = Ledger()\n\n    @rule(amount=st.integers(min_value=1, max_value=10000))\n    def deposit(self, amount):\n        self.ledger.deposit(amount)\n\n    @invariant()\n    def balance_must_equal_sum_of_transactions(self):\n        assert self.ledger.get_balance() == sum(t.amount for t in self.ledger.transactions)\n```",
        "verification_commands": "```bash\npytest tests/stateful/test_ledger.py --hypothesis-seed=42\n```",
        "anti_patterns": "- Nhầm lẫn giữa Unit Test (kiểm tra 1 input cụ thể) với Invariant Check (kiểm tra chân lý tổng quát).\n- Bỏ qua bước kiểm tra invariant sau khi rollback giao dịch lỗi.",
        "quality_gates": "- Kiểm chứng thành công tối thiểu 50,000 chuỗi chuyển đổi trạng thái ngẫu nhiên mà không vi phạm bất biến.",
        "security_constraints": "- Invariant check phải áp dụng kiểm tra chống Race condition (TOCTOU) trong môi trường concurrency.",
        "expected_outputs": "- Bộ mã nguồn Stateful Property-based Tests.\n- Tài liệu đặc tả các bất biến nghiệp vụ chính thức.",
        "related_skills": "dex-unit-testing, dex-database-design, dex-mutation-testing",
        "realistic_usage": "Một sàn giao dịch tiền điện tử áp dụng Stateful Invariant Testing cho hệ thống khớp lệnh. Sau 10,000 bước sinh lệnh ngẫu nhiên, họ phát hiện chuỗi: Đặt lệnh -> Hủy 1 phần -> Khớp lệnh -> Sửa giá làm số dư ví bị âm 0.00000001 do làm tròn số học."
    },

    # 130. dex-coverage-risk-analysis
    "dex-coverage-risk-analysis": {
        "desc": "Correlate code coverage metrics with code churn, production defect density, and business criticality to prioritize high-value test engineering. Use when optimizing QA effort and eliminating testing blind spots.",
        "purpose": "Kết hợp chỉ số độ bao phủ kiểm thử (code coverage) với tần suất sửa đổi mã nguồn (code churn), mật độ lỗi production trong quá khứ và mức độ quan trọng nghiệp vụ để xác định các 'điểm mù nguy hiểm' (high-risk blind spots), từ đó ưu tiên viết test cho những nơi có rủi ro cao nhất thay vì chạy theo 100% coverage hình thức.",
        "activation": "- Đội ngũ có nguồn lực hạn chế, không thể nâng độ bao phủ toàn bộ dự án từ 40% lên 90%.\n- Sau các sự cố production nghiêm trọng tại những vùng mã nguồn tưởng chừng ít thay đổi.\n- Cần chiến lược kiểm thử thực tế cho dự án legacy lớn.",
        "when_not_to_use": "- Không áp dụng quy định cấm merge code máy móc chỉ dựa trên con số phần trăm line coverage thuần túy.\n- Không dùng để đánh giá năng suất cá nhân của từng kỹ sư.",
        "inputs": "- Báo cáo coverage chi tiết (lcov.info, coverage.xml).\n- Lịch sử Git commits trong 6 tháng gần nhất (git log phân tích churn).\n- Danh sách bug tickets và incidents liên quan đến các module.",
        "preconditions": "- Có công cụ đo coverage hoạt động trong CI và lịch sử commit Git rõ ràng.",
        "core_concepts": "- Risk-based Testing: Vùng code có Churn cao (thay đổi liên tục) + Coverage thấp = Điểm nóng rủi ro cực đại (Critical Risk Zone).\n- Dumb Coverage: 100% coverage ở các file DTO/Constants không mang lại giá trị thực tế.",
        "decision_rules": "- Nếu một file có hơn 10 commits/tháng và coverage < 50%: bắt buộc bổ sung integration test trước khi chấp nhận tính năng mới.\n- Nếu file phức tạp (Cyclomatic Complexity > 15) chưa có test: xếp độ ưu tiên kiểm thử mức P0.",
        "failure_scenarios": "- Viết thêm hàng loạt test case rỗng không có assert để tăng coverage đối phó với chỉ tiêu của quản lý.",
        "workflow": "1. Xuất dữ liệu coverage theo từng file từ test suite hiện tại.\n2. Chạy script phân tích Git churn để đếm số lần sửa đổi và số dòng code thay đổi cho từng file.\n3. Xây dựng ma trận phân tán (Scatter plot): Trục X là Độ phức tạp/Tần suất sửa đổi, Trục Y là % Coverage.\n4. Xác định Top 10 file nằm ở góc nguy hiểm (High Churn / Low Coverage).\n5. Lập kế hoạch bổ sung test tập trung đúng vào các nhánh luồng chính của 10 file này.",
        "example": "```python\n# Phân tích rủi ro kết hợp Git churn và coverage\ndef calculate_risk_score(churn_count, cyclomatic_complexity, coverage_pct):\n    # Điểm rủi ro càng cao càng cần viết test khẩn cấp\n    uncovered_factor = (100.0 - coverage_pct) / 100.0\n    return (churn_count * 0.4 + cyclomatic_complexity * 0.6) * uncovered_factor\n```",
        "verification_commands": "```bash\n# Phân tích nhanh Git churn cho các file trong src/\ngit log --name-only --format='' --since='3 months ago' src/ | sort | uniq -c | sort -nr | head -n 15\n```",
        "anti_patterns": "- Ép buộc 100% line coverage toàn bộ dự án dẫn đến các bài test vô bổ chỉ gọi hàm mà không kiểm tra kết quả.\n- Bỏ qua các file logic thanh toán phức tạp chỉ vì nó nằm trong hệ thống legacy cũ.",
        "quality_gates": "- 100% các file thuộc vùng rủi ro cao (High Churn / High Complexity) phải đạt tối thiểu 80% branch coverage.",
        "security_constraints": "- Dữ liệu phân tích rủi ro không được chứa thông tin bảo mật hay dữ liệu riêng tư.",
        "expected_outputs": "- Báo cáo ma trận rủi ro Coverage-Churn (Risk Heatmap).\n- Danh sách backlog các test cases cần bổ sung theo thứ tự ưu tiên ROI.",
        "related_skills": "dex-mutation-testing, dex-git-flow-and-cherry-picking, dex-unit-testing",
        "realistic_usage": "Một công ty thương mại điện tử có tỉ lệ coverage chung chỉ 52%. Thay vì dàn trải nguồn lực, chuyên gia phân tích ma trận churn-coverage và phát hiện file `coupon_evaluator.py` thay đổi 34 lần trong quý nhưng chỉ có 28% coverage. Họ bổ sung 12 test cases tập trung, chặn đứng 3 lỗi tính sai mã giảm giá trong đợt sale Black Friday."
    },

    # 131. dex-load-and-stress-testing
    "dex-load-and-stress-testing": {
        "desc": "Design, script, and execute realistic load, spike, endurance, and stress tests using tools like K6, Locust, or Gatling to establish saturation points, latency percentiles, and capacity limits. Use before high-traffic events or capacity sizing.",
        "purpose": "Thiết kế kịch bản, lập trình và thực thi các bài kiểm thử tải (Load Testing), quá tải (Stress Testing), đột biến (Spike Testing) và ngâm tải dài hạn (Endurance Testing) bằng các công cụ chuyên dụng (K6, Locust, Gatling) để xác định ngưỡng bão hòa hệ thống, điểm đứt gãy, phân phối độ trễ (P95/P99) và năng lực xử lý tối đa.",
        "activation": "- Chuẩn bị cho các sự kiện lưu lượng truy cập lớn (Black Friday, Flash sale, Marketing campaigns).\n- Xác định năng lực tối đa (Capacity Sizing) của cụm microservices.\n- Đánh giá khả năng tự động co giãn (Auto-scaling) của hạ tầng Kubernetes/Cloud.",
        "when_not_to_use": "- Không chạy stress test lên production mà không có kế hoạch bảo trì hoặc sự đồng thuận của SRE on-call.\n- Không dùng máy cá nhân phát tải nếu băng thông mạng cục bộ không đủ lớn để tạo áp lực tải thực sự.",
        "inputs": "- Mục tiêu SLO/SLA (ví dụ: 5,000 RPS, P95 < 200ms, Error rate < 0.1%).\n- Kịch bản hành vi người dùng điển hình (User journeys: Login -> Browse -> Add to Cart -> Checkout).\n- Môi trường Staging có cấu hình tương đương (hoặc tỉ lệ 1:2) so với Production.",
        "preconditions": "- Hệ thống giám sát (APM, Prometheus, Grafana) đã sẵn sàng thu thập metrics của máy chủ mục tiêu.",
        "core_concepts": "- Phân loại kiểm thử tải:\n  + Load Test: Tải ổn định ở mức kỳ vọng để kiểm tra SLO.\n  + Stress Test: Tăng dần tải cho đến khi hệ thống bắt đầu nghẽn hoặc sập để tìm giới hạn tối đa.\n  + Spike Test: Đột ngột tăng vọt tải trong vài giây để kiểm tra khả năng co giãn và queue backpressure.\n  + Soak/Endurance Test: Duy trì tải trung bình trong 12-24 giờ để phát hiện rò rỉ bộ nhớ (Memory Leak) hoặc cạn kiệt Connection Pool.",
        "decision_rules": "- Nếu Error rate vượt quá 1% hoặc P99 latency vượt quá 2 giây: ngừng tăng tải và xác định bottleneck.\n- Nút thắt cổ chai thường gặp: Database connection pool bị đầy, CPU throttled, DNS lookup saturation.",
        "failure_scenarios": "- Tải quá mạnh làm nghẽn luôn network của máy phát tải (Load Generator saturation), dẫn đến số liệu đo lường bị sai lệch.",
        "workflow": "1. Thu thập số liệu traffic thực tế từ access logs để xây dựng mô hình tải (User mix percentage).\n2. Viết mã kịch bản tải bằng K6 (JavaScript).\n3. Chạy baseline test với 10 virtual users để kiểm tra tính chính xác của kịch bản.\n4. Thực hiện Ramp-up tải theo các giai đoạn định sẵn.\n5. Thu thập metrics CPU, RAM, IOPS, DB connections trong quá trình chạy tải.\n6. Phân tích kết quả P95/P99 latency và đưa ra khuyến nghị tinh chỉnh tài nguyên.",
        "example": "```javascript\nimport http from 'k6/http';\nimport { check, sleep } from 'k6';\n\nexport const options = {\n  stages: [\n    { duration: '2m', target: 500 }, // ramp-up to 500 users\n    { duration: '5m', target: 500 }, // stay at 500 users\n    { duration: '1m', target: 0 },   // ramp-down\n  ],\n  thresholds: {\n    http_req_duration: ['p(95)<300'], // 95% of requests must complete below 300ms\n    http_req_failed: ['rate<0.01'],   // error rate < 1%\n  },\n};\n\nexport default function () {\n  const res = http.get('https://staging-api.example.com/v1/catalog');\n  check(res, { 'status is 200': (r) => r.status === 200 });\n  sleep(1);\n}\n```",
        "verification_commands": "```bash\nk6 run --out json=results.json scripts/load-test.js\n```",
        "anti_patterns": "- Chỉ test tải endpoint đọc (GET) mà bỏ qua các endpoint ghi (POST/PUT) có transaction nặng.\n- Coi thường độ trễ P99 và chỉ nhìn vào độ trễ trung bình (Average).",
        "quality_gates": "- Đạt tối thiểu mục tiêu RPS đặt ra với P95 latency dưới ngưỡng cam kết và error rate < 0.1%.",
        "security_constraints": "- Kịch bản test tải không được phép làm lộ dữ liệu người dùng thật hoặc làm cạn kiệt số dư tài khoản thật.",
        "expected_outputs": "- Script kịch bản K6/Locust hoàn chỉnh.\n- Báo cáo phân tích hiệu năng và biểu đồ độ trễ kèm đề xuất cấu hình hạ tầng.",
        "related_skills": "dex-traffic-shaping-backpressure, dex-rate-limiting-quotas, dex-performance-profiling",
        "realistic_usage": "Một sàn vé chuẩn bị mở bán concert âm nhạc. Đội SRE thực hiện stress test K6 lên 20,000 users đồng thời. Họ phát hiện DB Redis bị nghẽn connection pool tại 8,000 RPS. Sau khi chuyển sang dùng Redis Cluster và cấu hình connection pool tái sử dụng, hệ thống chịu tải mượt mà 15,000 RPS."
    },

    # 132. dex-traffic-shaping-backpressure
    "dex-traffic-shaping-backpressure": {
        "desc": "Implement traffic shaping, backpressure mechanisms, leaky/token buckets, priority queues, and load-shedding to prevent cascading failures under extreme load. Use when distributed services face traffic surges.",
        "purpose": "Thiết kế và triển khai các cơ chế điều tiết lưu lượng (Traffic Shaping), kiểm soát áp lực ngược (Backpressure), cắt giảm tải có chọn lọc (Load Shedding) và hàng đợi ưu tiên (Priority Queuing) nhằm bảo vệ dịch vụ hạ tầng không bị quá tải sụp đổ dây chuyền (cascading failure) khi gặp cơn sóng dữ liệu đột biến.",
        "activation": "- Dịch vụ downstream xử lý chậm hơn tốc độ đẩy dữ liệu vào của upstream, khiến hàng đợi (Queue) phình to vô hạn và tràn bộ nhớ OOM.\n- Hệ thống đối mặt với traffic đột biến gấp 10 lần bình thường.\n- Cần ưu tiên các request thanh toán quan trọng hơn các request xem ảnh/thông tin phụ.",
        "when_not_to_use": "- Không áp dụng backpressure nếu hệ thống chỉ cần mở rộng tài nguyên tính toán (Horizontal Pod Autoscaling) đơn giản.\n- Không làm rớt các request của khách hàng nếu downstream service chưa thực sự cạn kiệt tài nguyên.",
        "inputs": "- Giới hạn tài nguyên của dịch vụ (CPU, RAM, Maximum In-flight Requests).\n- Phân loại độ ưu tiên của các luồng nghiệp vụ (Critical vs Non-critical).\n- Cấu hình hàng đợi (RabbitMQ, Kafka, Async Channel).",
        "preconditions": "- Kiến trúc hệ thống cho phép phản hồi mã trạng thái 429 (Too Many Requests) hoặc 503 (Service Unavailable) khi quá tải.",
        "core_concepts": "- Backpressure: Tín hiệu phản hồi từ downstream yêu cầu upstream chậm lại hoặc tạm dừng gửi tin.\n- Load Shedding: Chủ động từ chối nhanh (fail-fast) các request có độ ưu tiên thấp để giữ cho các request cốt lõi vẫn hoàn thành đúng hạn.\n- CoDel / Bounded Queues: Không bao giờ sử dụng hàng đợi không giới hạn (unbounded queue) vì sẽ dẫn đến OOM crash.",
        "decision_rules": "- Nếu độ trễ xếp hàng (Queue Waiting Time) vượt quá timeout của client: drop request ngay tại đầu vào thay vì tiếp tục xử lý vô ích.\n- Nếu CPU dịch vụ > 85%: kích hoạt chế độ load-shedding đối với các API phụ (recommendations, analytics).",
        "failure_scenarios": "- Xử lý tất cả các request đến cùng một lúc khiến toàn bộ hệ thống bị treo, dẫn đến 100% người dùng đều bị timeout thay vì 90% thành công và 10% bị từ chối lịch sự.",
        "workflow": "1. Xác định năng lực xử lý tối đa an toàn (Concurrency Limit) của service.\n2. Cấu hình giới hạn kích thước hàng đợi (Bounded Queue capacity).\n3. Tích hợp thuật toán điều tiết tải (ví dụ: Little's Law, CoDel hoặc Netflix Concurrency Limits).\n4. Thiết lập cờ phân loại độ ưu tiên cho các request (Header `X-Priority: High`).\n5. Kiểm thử giả lập quá tải để chứng minh dịch vụ không bị sập và tự phục hồi khi tải giảm.",
        "example": "```go\n// Giới hạn số lượng request đồng thời bằng buffered channel semaphore\ntype BoundedLimiter struct {\n    sem chan struct{}\n}\n\nfunc NewBoundedLimiter(maxConcurrent int) *BoundedLimiter {\n    return &BoundedLimiter{sem: make(chan struct{}, maxConcurrent)}\n}\n\nfunc (l *BoundedLimiter) Execute(w http.ResponseWriter, r *http.Request, handler http.HandlerFunc) {\n    select {\n    case l.sem <- struct{}{}:\n        defer func() { <-l.sem }()\n        handler(w, r)\n    default:\n        // Drop tải ngay lập tức nếu hàng đợi đầy (Load Shedding)\n        http.Error(w, \"Server Busy - Try again later\", http.StatusServiceUnavailable)\n    }\n}\n```",
        "verification_commands": "```bash\n# Bắn spike test để kiểm tra load-shedding trả về 503 thay vì sập service\nk6 run --vus 2000 --duration 30s scripts/spike-test.js\n```",
        "anti_patterns": "- Dùng hàng đợi không giới hạn (Unbounded Queue) trong bộ nhớ dẫn đến sập container do OOMKilled.\n- Tiếp tục xử lý request sau khi client đã disconnect hoặc hủy kết nối.",
        "quality_gates": "- Dịch vụ vẫn duy trì P95 latency ổn định cho 80% request ưu tiên khi tổng traffic vượt 300% tải thiết kế.",
        "security_constraints": "- Cơ chế load shedding không được làm rò rỉ thông tin kiến trúc nội bộ trong thông báo lỗi trả về client.",
        "expected_outputs": "- Middleware điều tiết backpressure và load-shedding.\n- Dashboard Grafana giám sát tỉ lệ shed requests và queue depth.",
        "related_skills": "dex-load-and-stress-testing, dex-rate-limiting-quotas, dex-service-failover",
        "realistic_usage": "Một dịch vụ streaming video bị sập mỗi khi có trận bóng đá trực tiếp do hàng triệu người kết nối cùng lúc. Sau khi triển khai Adaptive Concurrency Limiting, dịch vụ tự động drop các request load comment và gợi ý phim, bảo vệ luồng phát video trực tiếp cho 98% khán giả không bị giật lag."
    },

    # 133. dex-rate-limiting-quotas
    "dex-rate-limiting-quotas": {
        "desc": "Design and enforce multi-tier rate limiting and quota management using algorithms like Sliding Window Log, Token Bucket, and Redis-backed distributed stores. Use to prevent API abuse, ensure tenant fairness, and enforce subscription tiers.",
        "purpose": "Thiết kế, xây dựng và triển khai hệ thống phân tầng giới hạn tần suất gọi API (Rate Limiting) và hạn mức tài nguyên (Quotas) dựa trên các thuật toán tối ưu (Token Bucket, Leaky Bucket, Sliding Window Counter) với backend phân tán (Redis/Memcached); bảo đảm sự công bằng giữa các tenant, ngăn chặn lạm dụng và bảo vệ hệ sinh thái dịch vụ.",
        "activation": "- Một số người dùng hoặc bot tự động spam request làm cạn kiệt tài nguyên hệ sinh thái.\n- Triển khai gói dịch vụ SaaS phân tầng (Free: 100 req/min, Pro: 10,000 req/min).\n- Bảo vệ các API nhạy cảm (Đăng nhập, Quên mật khẩu, Gửi OTP SMS) chống tấn công Brute-force.",
        "when_not_to_use": "- Không áp dụng rate limit quá khắt khe đối với các giao tiếp nội bộ giữa các microservices tin cậy (dùng service mesh auth).\n- Không dùng thuật toán Fixed Window đơn giản cho các hệ thống yêu cầu độ chính xác cao vì dễ bị bùng nổ traffic tại điểm giao giữa 2 cửa sổ.",
        "inputs": "- Quy tắc hạn mức (Rate limits: số request trên đơn vị thời gian) theo từng route hoặc User Tier.\n- Khóa định danh khách hàng (API Key, User ID, Client IP, JWT Claim).\n- Cụm Redis phân tán hỗ trợ thực thi kịch bản nguyên tử (Lua script).",
        "preconditions": "- Hạ tầng Redis/Key-value store có độ trễ cực thấp (<2ms) để không làm tăng đáng kể độ trễ của API Gateway.",
        "core_concepts": "- Sliding Window Counter: Thuật toán cân bằng giữa độ chính xác của Sliding Log và tính tiết kiệm bộ nhớ của Fixed Window.\n- Distributed Rate Limiting: Dùng Redis Lua script để bảo đảm thao tác kiểm tra và tăng biến đếm là nguyên tử (Atomic Check-and-Set), tránh Race Condition.\n- HTTP Headers chuẩn: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`.",
        "decision_rules": "- Nếu request vượt hạn mức: trả về HTTP 429 Too Many Requests kèm header `Retry-After: <seconds>`.\n- Nếu Redis gặp sự cố: chuyển sang chế độ Fail-Open (cho phép đi qua) kèm cảnh báo khẩn tới SRE thay vì chặn đứng toàn bộ traffic khách hàng.",
        "failure_scenarios": "- Sử dụng Client IP làm khóa định danh duy nhất cho người dùng sau NAT proxy chung (ví dụ văn phòng công ty), khiến một người spam làm toàn bộ văn phòng bị khóa oan.",
        "workflow": "1. Xác định tiêu chí phân tầng quota theo tài khoản người dùng và loại endpoint.\n2. Viết Redis Lua script thực hiện thuật toán Sliding Window Counter.\n3. Xây dựng Middleware tích hợp tại API Gateway (Kong, Envoy, hoặc Express/FastAPI).\n4. Trả về đầy đủ các headers RateLimit tiêu chuẩn trong mọi phản hồi.\n5. Thiết lập cơ chế Fail-Open và giám sát tỉ lệ 429 trên Grafana.",
        "example": "```lua\n-- Redis Lua Script: Sliding Window Counter Rate Limiter\nlocal key = KEYS[1]\nlocal now = tonumber(ARGV[1])\nlocal window = tonumber(ARGV[2])\nlocal limit = tonumber(ARGV[3])\nlocal clearBefore = now - window\n\nredis.call('ZREMRANGEBYSCORE', key, 0, clearBefore)\nlocal currentRequests = redis.call('ZCARD', key)\n\nif currentRequests < limit then\n    redis.call('ZADD', key, now, now)\n    redis.call('EXPIRE', key, window)\n    return 1 -- Cho phép\nelse\n    return 0 -- Bị chặn (Rate limited)\nend\n```",
        "verification_commands": "```bash\n# Kiểm tra rate limit bằng curl lặp lại nhanh\nfor i in {1..15}; do curl -s -o /dev/null -w \"%{http_code}\\n\" http://localhost:8080/api/v1/auth/login; done\n```",
        "anti_patterns": "- Không sử dụng Lua Script dẫn đến Race condition khi hai request đến song song vượt qua kiểm tra hạn mức.\n- Đặt thời gian timeout của Redis quá lớn làm nghẽn toàn bộ luồng xử lý của API Gateway khi Redis chậm.",
        "quality_gates": "- Middleware rate limiter chỉ được phép làm tăng độ trễ trung bình của API tối đa 2ms.\n- Chặn chính xác 100% các request vượt ngưỡng hạn mức trong các bài test tự động.",
        "security_constraints": "- Chống việc người dùng qua mặt rate limiter bằng cách giả mạo Header `X-Forwarded-For` (chỉ tin tưởng IP từ trusted proxy).",
        "expected_outputs": "- Script Lua và mã nguồn middleware Rate Limiter.\n- Bộ test suite tự động kiểm chứng các kịch bản biên của rate limit.",
        "related_skills": "dex-api-abuse-prevention, dex-traffic-shaping-backpressure, dex-backend-architecture",
        "realistic_usage": "Một dịch vụ AI bị một bên thứ ba viết script crawl tự động làm tăng vọt chi phí inference OpenAI. Đội ngũ triển khai Sliding Window Rate Limiting tại Envoy Gateway, giới hạn mỗi API Key chỉ được 60 requests/phút. Chi phí API lập tức giảm 45% mà không ảnh hưởng tới khách hàng thông thường."
    },

    # 134. dex-distributed-consistency
    "dex-distributed-consistency": {
        "desc": "Analyze, design, and resolve distributed consistency challenges across microservices, including Saga patterns, transactional outboxes, idempotency keys, and conflict resolution. Use when splitting monoliths or managing multi-database transactions.",
        "purpose": "Phân tích, thiết kế và xử lý các bài toán nhất quán dữ liệu phân tán (Distributed Consistency) giữa các microservices và cơ sở dữ liệu phân tán; áp dụng mô hình Saga, Transactional Outbox, Idempotency Keys và các chiến lược giải quyết xung đột (Conflict Resolution) thay thế cho distributed transactions (2PC) nặng nề.",
        "activation": "- Tách ứng dụng đơn khối (Monolith) thành Microservices khiến một nghiệp vụ phải cập nhật dữ liệu trên nhiều cơ sở dữ liệu độc lập.\n- Hệ thống xử lý thanh toán, trừ tồn kho và gửi email thông báo cần đảm bảo tính nhất quán cuối cùng (Eventual Consistency).\n- Dữ liệu bị sai lệch, mất mát hoặc bị nhân đôi do network partition và service retry.",
        "when_not_to_use": "- Không áp dụng kiến trúc Saga phức tạp nếu toàn bộ dữ liệu vẫn nằm chung trong một cơ sở dữ liệu quan hệ (chỉ cần ACID transaction đơn giản).\n- Không áp dụng cho các dữ liệu phân tích chỉ đọc (read-only analytics).",
        "inputs": "- Luồng nghiệp vụ phân tán (Business transaction workflow).\n- Danh sách các dịch vụ và cơ sở dữ liệu tham gia.\n- Broker tin cậy cho messaging (Kafka, RabbitMQ, SQS).",
        "preconditions": "- Các dịch vụ có cơ chế lưu trữ bền vững (Durable storage) và hỗ trợ giao dịch cục bộ (Local ACID transaction).",
        "core_concepts": "- Định lý CAP và BASE: Chấp nhận tính Nhất quán cuối cùng (Eventual Consistency) để đổi lấy tính Sẵn sàng (Availability) và Khả năng chịu lỗi phân vùng (Partition Tolerance).\n- Transactional Outbox Pattern: Ghi sự kiện vào bảng Outbox trong cùng một local database transaction với dữ liệu nghiệp vụ, sau đó dùng Debezium hoặc Poller đẩy sang Message Broker để chống mất tin.\n- Idempotency Key: Khóa duy nhất đi kèm mỗi request giúp server phát hiện và bỏ qua các lệnh trùng lặp do mạng thử lại (retry).",
        "decision_rules": "- Với chuỗi hành động có khả năng lỗi ở giữa: bắt buộc thiết kế các hành động bù trừ (Compensating Transactions - ví dụ: Hoàn tiền nếu đặt vé máy bay thất bại).\n- Mọi message consumer phải thiết kế có tính chất bình thản (Idempotent Consumer).",
        "failure_scenarios": "- Thực hiện gọi REST API gửi sự kiện ngay giữa database transaction, nếu commit DB thất bại nhưng sự kiện đã bắn đi thì dữ liệu vĩnh viễn bị lệch.",
        "workflow": "1. Vẽ sơ đồ chuỗi trạng thái và các điểm thất bại tiềm năng trong quy trình phân tán.\n2. Thiết kế bảng `outbox` và bảng `idempotency_records` trong database của mỗi service.\n3. Triển khai Saga Orchestrator hoặc Choreography với các bước bù trừ rõ ràng.\n4. Tích hợp cơ chế kiểm tra Idempotency Key tại tầng API và Consumer.\n5. Viết kịch bản Chaos test ngắt kết nối giữa chừng để chứng minh dữ liệu tự phục hồi về trạng thái nhất quán.",
        "example": "```sql\n-- Bảng Transactional Outbox bảo đảm không mất sự kiện\nCREATE TABLE outbox_events (\n    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),\n    aggregate_type VARCHAR(64) NOT NULL,\n    aggregate_id VARCHAR(64) NOT NULL,\n    event_type VARCHAR(64) NOT NULL,\n    payload JSONB NOT NULL,\n    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),\n    processed BOOLEAN DEFAULT FALSE\n);\n```",
        "verification_commands": "```bash\n# Kiểm thử kịch bản gửi lặp lại 5 lần cùng 1 Idempotency-Key\nfor i in {1..5}; do curl -X POST http://localhost:8080/api/v1/orders -H 'Idempotency-Key: test-uuid-001' -d '{\"amount\": 100}'; done\n```",
        "anti_patterns": "- Lạm dụng Two-Phase Commit (2PC) trên môi trường Cloud/Microservices gây nghẽn và sập hệ thống khi có mạng chập chờn.\n- Viết Compensating transaction thiếu trường hợp xử lý lỗi khi chính hành động bù trừ cũng bị fail.",
        "quality_gates": "- 0 giao dịch bị treo ở trạng thái không xác định sau khi giả lập mất kết nối mạng giữa các dịch vụ.",
        "security_constraints": "- Khóa Idempotency và dữ liệu Event Payload phải được mã hóa nếu chứa thông tin PII hoặc thẻ tín dụng.",
        "expected_outputs": "- Sơ đồ kiến trúc Saga và danh sách Compensating actions.\n- Mã nguồn triển khai Transactional Outbox và Idempotent Handler.",
        "related_skills": "dex-distributed-tracing, dex-database-design, dex-service-failover",
        "realistic_usage": "Một sàn thương mại điện tử gặp sự cố khách hàng bị trừ tiền trong ví nhưng đơn hàng không được tạo do mạng timeout. Áp dụng Transactional Outbox kết hợp Saga Orchestration, khi bước tạo đơn lỗi, orchestrator tự động phát lệnh hoàn tiền vào ví trong vòng 3 giây, loại bỏ hoàn toàn các khiếu nại của khách."
    },

    # 135. dex-service-failover
    "dex-service-failover": {
        "desc": "Architect, configure, and validate automated service failover, multi-region routing, health-checking protocols, and circuit breakers (Envoy, Resilience4j). Use when engineering high-availability fault-tolerant services.",
        "purpose": "Thiết kế, cấu hình và kiểm chứng cơ chế chuyển đổi dự phòng tự động (Automated Failover), định tuyến đa vùng (Multi-region Routing), giao thức kiểm tra sức khỏe sâu (Deep Health Checks) và ngắt mạch (Circuit Breakers) nhằm bảo đảm dịch vụ duy trì hoạt động liên tục khi các cụm máy chủ hoặc vùng điện toán gặp sự cố nghiêm trọng.",
        "activation": "- Dịch vụ yêu cầu độ sẵn sàng cao (High Availability 99.99% - Four Nines).\n- Chuẩn bị kế hoạch khôi phục sau thảm họa (Disaster Recovery - DR) cho datacenter/cloud region.\n- Tránh tình trạng dịch vụ chết chìm khi phụ thuộc vào một nhà cung cấp bên thứ ba đang bị lỗi.",
        "when_not_to_use": "- Không cấu hình failover tự động cho các cơ sở dữ liệu Master-Slave nếu cơ chế chống phân rã não (Split-Brain) chưa được chứng minh an toàn.\n- Không dùng Circuit Breaker cho các thao tác nội bộ siêu nhanh in-memory.",
        "inputs": "- Kiến trúc phân bổ dịch vụ (Active-Active hoặc Active-Passive).\n- Các ngưỡng phát hiện lỗi (Failure thresholds: số lần lỗi liên tiếp, timeout limit).\n- Công cụ cân bằng tải và Service Mesh (Envoy, AWS Route53, Cloudflare, Resilience4j).",
        "preconditions": "- Có ít nhất 2 phiên bản độc lập của dịch vụ được triển khai ở 2 vùng/cụm máy chủ tách biệt.",
        "core_concepts": "- Circuit Breaker States: `CLOSED` (bình thường) -> `OPEN` (ngắt mạch, fail-fast lập tức để downstream hồi phục) -> `HALF-OPEN` (thử nghiệm gửi vài request để kiểm tra sức khỏe).\n- Split-Brain Prevention: Trong kiến trúc đa vùng, phải có cơ chế quorum (bầu chọn quá bán) để tránh 2 master cùng ghi dữ liệu gây hỏng database.\n- Deep vs Shallow Health Check: Shallow chỉ kiểm tra process sống (HTTP 200), Deep kiểm tra cả khả năng kết nối DB và bộ nhớ.",
        "decision_rules": "- Nếu tỉ lệ lỗi của endpoint > 50% trong 10 giây: chuyển Circuit Breaker sang trạng thái `OPEN` và trả về fallback data.\n- Chỉ kích hoạt chuyển vùng (Region Failover) khi mất kết nối hoàn toàn trên 3 kỳ health check liên tiếp (chống flap do mạng chập chờn ngắn hạn).",
        "failure_scenarios": "- Failover Thundering Herd: Khi Region A bị lỗi, toàn bộ traffic đổ dồn đột ngột sang Region B làm Region B cũng quá tải và sập theo (hiệu ứng domino).",
        "workflow": "1. Thiết lập endpoint `/healthz` (liveness) và `/ready` (readiness) chuẩn hóa.\n2. Cấu hình Circuit Breaker cho các lời gọi remote service với timeout và fallback rõ ràng.\n3. Thiết lập DNS Health Check với TTL ngắn (30-60 giây) để chuyển hướng traffic nhanh khi cần.\n4. Thực hiện diễn tập ngắt kết nối đột ngột của Region chính (Chaos drill).\n5. Xác minh thời gian chuyển đổi (RTO) và tỉ lệ mất mát dữ liệu (RPO).",
        "example": "```yaml\n# Cấu hình Envoy Circuit Breakers\ncircuit_breakers:\n  thresholds:\n    - priority: DEFAULT\n      max_connections: 1000\n      max_pending_requests: 100\n      max_requests: 1000\n      max_retries: 3\noutlier_detection:\n  consecutive_5xx: 3\n  interval: 10s\n  base_ejection_time: 30s\n  max_ejection_percent: 50\n```",
        "verification_commands": "```bash\n# Giả lập ngắt kết nối để kiểm tra Circuit Breaker nhảy sang OPEN\nfor i in {1..20}; do curl -s -w \"%{http_code}\\n\" http://localhost:8080/api/v1/external-data; done\n```",
        "anti_patterns": "- Cấu hình retry vô hạn với fixed delay làm dịch vụ downstream vừa phục hồi đã bị đè bẹp trở lại (phải dùng Exponential Backoff với Jitter).\n- Đặt Health Check kiểm tra quá nặng (ví dụ: quét toàn bộ bảng DB) khiến bản thân health check làm sập DB.",
        "quality_gates": "- Thời gian phát hiện lỗi và chuyển đổi sang instance dự phòng dưới 30 giây mà không cần con người can thiệp.",
        "security_constraints": "- Đảm bảo dữ liệu đồng bộ sang cụm dự phòng được mã hóa trên đường truyền (mTLS) và tại đích (Encryption at rest).",
        "expected_outputs": "- File cấu hình Envoy / Resilience4j / Route53 Failover.\n- Biên bản diễn tập kiểm tra chuyển đổi dự phòng.",
        "related_skills": "dex-distributed-consistency, dex-traffic-shaping-backpressure, dex-operational-game-days",
        "realistic_usage": "Dịch vụ cổng thanh toán tích hợp ngân hàng ngoài thường xuyên bị treo khiến các worker bị khóa hết luồng. Nhóm tích hợp Circuit Breaker với Resilience4j. Khi ngân hàng ngoài bị lỗi quá 5 lần liên tiếp, hệ thống lập tức mở mạch, trả về thông báo 'Ngân hàng đang bảo trì' trong 0.1ms và tự động thử lại sau 60 giây, bảo vệ ứng dụng chính chạy trơn tru."
    },

    # 136. dex-alert-quality-engineering
    "dex-alert-quality-engineering": {
        "desc": "Audit, refine, and eliminate noisy monitoring alerts by tuning thresholds, implementing deduplication, and ensuring all alerts are actionable with runbooks. Use to eradicate on-call alert fatigue and improve incident response.",
        "purpose": "Kiểm toán, tinh chỉnh và loại bỏ các cảnh báo giám sát gây nhiễu (Alert Fatigue); đánh giá ngưỡng cảnh báo dựa trên triệu chứng (Symptom-based Alerting) thay vì nguyên nhân phỏng đoán, thiết lập gom nhóm cảnh báo và bảo đảm 100% cảnh báo gửi tới kỹ sư trực đều có tính hành động (Actionable) kèm runbook xử lý rõ ràng.",
        "activation": "- Kỹ sư on-call nhận hàng chục cảnh báo mỗi đêm nhưng hầu hết là 'tự hết' hoặc không cần làm gì.\n- Alert fatigue dẫn đến việc kỹ sư bỏ lỡ cảnh báo sự cố nghiêm trọng thực sự.\n- Bị phàn nàn về các cảnh báo vô nghĩa như 'CPU > 80%' trong khi người dùng không hề bị ảnh hưởng.",
        "when_not_to_use": "- Không tắt các cảnh báo vi phạm SLO/SLA nghiêm trọng ảnh hưởng trực tiếp tới khách hàng.\n- Không xóa cảnh báo khi chưa tìm hiểu lý do tại sao nó được tạo ra ban đầu.",
        "inputs": "- Lịch sử cảnh báo trong 30-90 ngày qua từ PagerDuty/Opsgenie/Alertmanager.\n- Danh sách các cảnh báo thường xuyên bị 'Acknowledge rồi bỏ đó'.\n- Chỉ số SLO/SLI hiện tại của dịch vụ.",
        "preconditions": "- Có quyền truy cập vào cấu hình Prometheus Alertmanager hoặc Datadog/Grafana Alert rules.",
        "core_concepts": "- Symptom-based Alerting: Cảnh báo khi người dùng bị ảnh hưởng (ví dụ: Tỉ lệ lỗi HTTP 5xx tăng cao, Độ trễ thanh toán P99 > 2s). Không bao giờ đánh thức kỹ sư nửa đêm chỉ vì 'CPU máy chủ đạt 85%'.\n- Actionability: Một cảnh báo hợp lệ phải trả lời được câu hỏi: 'Kỹ sư nhận cảnh báo này cần làm hành động cụ thể gì ngay lập tức?'. Nếu câu trả lời là 'Không làm gì', hãy xóa cảnh báo hoặc chuyển sang kênh email/slack thông báo định kỳ.",
        "decision_rules": "- Nếu một cảnh báo kích hoạt hơn 3 lần một ngày nhưng không sinh ra incident nào: xóa bỏ hoặc nâng ngưỡng.\n- Mọi cảnh báo Pager/SMS bắt buộc phải có đường dẫn trực tiếp tới `runbook_url` hợp lệ.",
        "failure_scenarios": "- Tắt hết cảnh báo để 'yên tĩnh' dẫn đến hệ thống sập nửa ngày mà không ai hay biết.",
        "workflow": "1. Xuất báo cáo thống kê top 10 cảnh báo xuất hiện nhiều nhất trong tháng.\n2. Phân loại từng cảnh báo: Actionable vs Non-actionable.\n3. Chuyển đổi các cảnh báo đo nguyên nhân (Cause-based) sang đo lường vi phạm ngân sách lỗi SLO (Multi-window Multi-burn-rate Alerting).\n4. Bổ sung `runbook_url` chi tiết vào nhãn của mỗi rule.\n5. Đánh giá lại sau 2 tuần: mục tiêu giảm tối thiểu 60% số lượng cảnh báo rác đánh thức ban đêm.",
        "example": "```yaml\n# Rule cảnh báo chuẩn Google SRE: Multi-burn-rate Alerting\n- alert: HighErrorRateBurnRate\n  expr: (\n      rate(http_requests_total{status=~\"5..\"}[1h]) / rate(http_requests_total[1h])\n    ) > (14.4 * (1 - 0.999))\n  for: 2m\n  labels:\n    severity: critical\n  annotations:\n    summary: \"Dịch vụ đang tiêu thụ ngân sách lỗi (Error Budget) quá nhanh trong 1 giờ qua.\"\n    runbook_url: \"https://wiki.example.com/runbooks/high-error-rate\"\n```",
        "verification_commands": "```bash\n# Kiểm tra cú pháp và unit test cho alert rules của Prometheus\npromtool check rules rules/alerts.yaml\npromtool test rules tests/alerts-test.yaml\n```",
        "anti_patterns": "- Gửi cảnh báo rác vào một kênh Slack chung không ai đọc (kênh 'nghĩa địa cảnh báo').\n- Cảnh báo dựa trên con số tĩnh không tính đến chu kỳ ngày/đêm (ví dụ số đơn hàng giảm lúc 3 giờ sáng là bình thường).",
        "quality_gates": "- Giảm tỉ lệ false-positive alerts xuống dưới 5% tổng số cảnh báo nhận được.\n- 100% cảnh báo critical có runbook và dashboard đi kèm.",
        "security_constraints": "- Nội dung thông báo cảnh báo không được chứa mật khẩu, API keys hay thông tin PII của khách hàng.",
        "expected_outputs": "- Bảng kiểm toán chất lượng cảnh báo (Alert Audit Matrix).\n- File cấu hình alert rules đã được tinh chỉnh kèm bộ unit tests `promtool`.",
        "related_skills": "dex-metric-cardinality-control, dex-oncall-handover, dex-log-pipeline-design",
        "realistic_usage": "Một đội SRE bị quá tải với hơn 400 cảnh báo PagerDuty mỗi tuần, khiến các kỹ sư kiệt sức và xin nghỉ việc. Bằng cách áp dụng kiểm toán Alert Quality và chuyển sang mô hình Google SRE Multi-Burn-Rate, số lượng cảnh báo giảm từ 400 xuống còn 12 cảnh báo/tuần, và 100% các cảnh báo đó đều là sự cố thực sự cần xử lý."
    },

    # 137. dex-log-pipeline-design
    "dex-log-pipeline-design": {
        "desc": "Design scalable, structured, observable log collection and processing pipelines with correlation IDs, redaction of sensitive data (PII), and tiered storage policies. Use when centralizing telemetry across large distributed clusters.",
        "purpose": "Thiết kế, xây dựng và tối ưu hóa đường ống thu thập và xử lý nhật ký (Log Pipeline: Fluentbit, Vector, Logstash, Loki, Elasticsearch/OpenSearch); cấu trúc hóa JSON logs, gắn định danh tương quan (Correlation/Trace IDs), tự động bôi đen dữ liệu nhạy cảm (PII Redaction) và thiết lập chính sách lưu trữ phân tầng tiết kiệm chi phí.",
        "activation": "- Nhật ký phân tán rải rác trên hàng trăm container khiến việc điều tra sự cố gặp khó khăn.\n- Chi phí lưu trữ log trên Datadog/Splunk tăng phi mã vượt ngân sách.\n- Rò rỉ dữ liệu thẻ tín dụng hoặc mật khẩu vào log hệ thống vi phạm tiêu chuẩn bảo mật (PCI-DSS/GDPR).",
        "when_not_to_use": "- Không sử dụng log cho các số liệu thống kê thời gian thực cần tần suất cao (hãy dùng Prometheus metrics).\n- Không ghi log văn bản tự do (unstructured text) cho các hệ thống quy mô lớn.",
        "inputs": "- Định dạng log hiện tại của các dịch vụ (Stdout, syslog, file).\n- Khối lượng log sinh ra mỗi ngày (GB/ngày).\n- Yêu cầu tuân thủ về thời gian lưu trữ (Retention policy: Hot, Warm, Cold).",
        "preconditions": "- Các ứng dụng có thể ghi log ra chuẩn `stdout/stderr` dưới định dạng JSON có cấu trúc.",
        "core_concepts": "- Structured Logging: Mọi dòng log là một đối tượng JSON hợp lệ chứa các trường chuẩn hóa: `timestamp`, `level`, `trace_id`, `service`, `message`.\n- PII Redaction at the Edge: Làm sạch các trường nhạy cảm (`password`, `access_token`, `card_number`) ngay tại agent thu thập (Vector/Fluentbit) trước khi gửi qua mạng.\n- Tiered Storage: Dữ liệu log 7 ngày đầu lưu ở bộ nhớ nhanh (Hot/SSD), từ ngày 8-30 lưu ở Warm, sau 30 ngày nén đưa vào S3 Glacier (Cold) để lưu trữ pháp lý.",
        "decision_rules": "- Nếu log không chứa `trace_id`: gắn định danh tự sinh tại proxy đầu vào để đảm bảo truy vết toàn trình.\n- Không bao giờ lưu log DEBUG trên môi trường production trong điều kiện vận hành bình thường.",
        "failure_scenarios": "- Một dịch vụ bị lỗi vòng lặp in hàng triệu dòng log mỗi giây làm tắc nghẽn log collector và làm đầy ổ đĩa toàn bộ node Kubernetes.",
        "workflow": "1. Chuẩn hóa format JSON log trong thư viện framework dùng chung của công ty.\n2. Cấu hình Vector hoặc Fluentbit làm DaemonSet trên từng node để thu thập stdout.\n3. Viết bộ lọc regex/VRL để bôi đen dữ liệu nhạy cảm (PII scrubbing).\n4. Cấu hình đệm chống tràn (Disk buffer) trong trường hợp cụm Elasticsearch/Loki bị nghẽn.\n5. Thiết lập lifecycle policy tự động chuyển log cũ sang S3 và xóa sau hạn mức quy định.",
        "example": "```yaml\n# Vector configuration for PII redaction and structured routing\ntransforms:\n  redact_pii:\n    type: \"remap\"\n    inputs: [\"kubernetes_logs\"]\n    source: |\n      # Masking credit cards\n      .message = replace(.message, r'[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}', \"****-****-****-****\")\n      # Masking authorization headers\n      if exists(.headers.authorization) {\n        .headers.authorization = \"[REDACTED]\"\n      }\n```",
        "verification_commands": "```bash\n# Kiểm tra cấu hình Vector và giả lập luồng log\nvector validate --config /etc/vector/vector.yaml\n```",
        "anti_patterns": "- Ghi log chuỗi cộng chuỗi (string concatenation) thay vì structured logging.\n- Thu thập log trực tiếp từ container gửi qua HTTP đồng bộ khiến ứng dụng bị chậm theo khi log server lag.",
        "quality_gates": "- 100% log được phân loại có `trace_id` hợp lệ và 0% dữ liệu thẻ tín dụng thô lọt vào log storage.",
        "security_constraints": "- Quyền truy cập vào hệ thống log tập trung phải được kiểm soát nghiêm ngặt theo vai trò (RBAC) và có audit log người xem.",
        "expected_outputs": "- File cấu hình DaemonSet Vector/Fluentbit hoàn chỉnh.\n- Tài liệu chuẩn hóa cấu trúc JSON log chung cho toàn tổ chức.",
        "related_skills": "dex-alert-quality-engineering, dex-metric-cardinality-control, dex-distributed-tracing",
        "realistic_usage": "Một ngân hàng số phát hiện lập trình viên vô tình log toàn bộ request payload chứa OTP và số thẻ vào CloudWatch. Đội ngũ SRE đã triển khai đường ống Vector DaemonSet với bộ lọc VRL tự động bôi đen thông tin nhạy cảm ngay tại node cục bộ trong 0.2ms, ngăn chặn nguy cơ rò rỉ dữ liệu quy mô lớn."
    },

    # 138. dex-metric-cardinality-control
    "dex-metric-cardinality-control": {
        "desc": "Audit, manage, and prevent metric cardinality explosions in Prometheus and Datadog by enforcing label budgets, drop rules, and recording rules. Use when monitoring infrastructure costs surge or TSDB nodes crash.",
        "purpose": "Kiểm toán, quản lý và ngăn ngừa thảm họa bùng nổ số chiều metric (Metric Cardinality Explosion) trong hệ thống giám sát (Prometheus, Cortex, M3DB, Datadog); thiết lập ngân sách nhãn (Label Budget), loại bỏ các nhãn có giá trị vô hạn (UUID, email, IP) và tối ưu hóa chi phí giám sát.",
        "activation": "- Cụm Prometheus bị sập liên tục do lỗi OOM (Out Of Memory) khi quét dữ liệu time-series.\n- Hóa đơn chi phí Datadog/NewRelic tăng vọt hàng chục ngàn USD do số lượng custom metrics bùng nổ.\n- Tốc độ tải dashboard Grafana bị chậm chạp nghiêm trọng (>10s cho mỗi query).",
        "when_not_to_use": "- Không loại bỏ các nhãn định danh cần thiết cho việc phân loại SLO cốt lõi (như `status_code`, `method`, `service`).\n- Không dùng metrics để lưu trữ các dữ liệu mang tính sự kiện giao dịch (hãy dùng Distributed Tracing hoặc Logs).",
        "inputs": "- Báo cáo thống kê TSDB status (Prometheus `/api/v1/status/tsdb`).\n- Danh sách các metric có số lượng time-series lớn nhất.\n- Cấu hình Prometheus scrape configs hoặc OpenTelemetry collector.",
        "preconditions": "- Có quyền truy cập vào giao diện quản trị Prometheus hoặc API giám sát hạ tầng.",
        "core_concepts": "- Cardinality: Tổng số time-series duy nhất được tính bằng tích số các giá trị khả dĩ của tất cả các nhãn (Labels). Ví dụ: `http_requests_total{method=\"5\", path=\"100\", user_id=\"1,000,000\"}` tạo ra 500 triệu chuỗi thời gian, làm sập bất kỳ TSDB nào.\n- Bounded Labels: Chỉ sử dụng các nhãn có tập giá trị hữu hạn và nhỏ (ví dụ: HTTP status: 200, 400, 500; Region: us-east, ap-southeast).\n- Metric Relabeling: Cơ chế cắt bỏ nhãn xấu (drop label) ngay tại tầng thu thập dữ liệu.",
        "decision_rules": "- Tuyệt đối cấm đưa `user_id`, `email`, `order_id`, `ip_address` vào làm nhãn của Prometheus metric.\n- Bất kỳ metric nào sinh ra > 10,000 active series mà không có sự phê duyệt của SRE phải bị drop tại collector.",
        "failure_scenarios": "- Một lập trình viên đưa URL raw có chứa dynamic ID (`/users/123e4567-e89b-12d3`) vào label `path` thay vì URL template (`/users/:id`), khiến Prometheus chết ngắc sau 10 phút.",
        "workflow": "1. Truy vấn endpoint `/api/v1/status/tsdb` của Prometheus để tìm Top 10 metric có số series cao nhất.\n2. Phân tích nguyên nhân: xác định label nào có cardinality cao bất thường.\n3. Cập nhật mã nguồn ứng dụng để chuẩn hóa label (dùng route pattern thay vì raw path).\n4. Cấu hình `metric_relabel_configs` tại Prometheus/Otel Collector để drop các nhãn vi phạm.\n5. Áp dụng Recording Rules để tính toán trước các chỉ số tổng hợp, giảm tải cho Grafana.",
        "example": "```yaml\n# Prometheus scrape config relabeling to drop dangerous high-cardinality labels\nscrape_configs:\n  - job_name: 'api-service'\n    static_configs:\n      - targets: ['localhost:8080']\n    metric_relabel_configs:\n      - regex: '(user_id|session_token|email)'\n        action: labeldrop\n      - source_labels: [__name__]\n        regex: 'unwanted_debug_metric_.*'\n        action: drop\n```",
        "verification_commands": "```bash\n# Truy vấn top metrics có nhiều chuỗi thời gian nhất trên Prometheus\ncurl -s http://localhost:9090/api/v1/status/tsdb | jq '.data.seriesCountByMetricName[:10]'\n```",
        "anti_patterns": "- Gắn `timestamp` hoặc `hash` vào metric label.\n- Không thiết lập giới hạn `sample_limit` cho scrape job trong Prometheus.",
        "quality_gates": "- Giữ tổng số active time-series trên toàn cụm Prometheus trong ngân sách kiểm soát (< 1 triệu series/node).",
        "security_constraints": "- Loại bỏ các nhãn có thể vô tình làm lộ thông tin định danh cá nhân (PII) ra giao diện dashboard.",
        "expected_outputs": "- Báo cáo kiểm toán Cardinality và danh sách nhãn đã dọn dẹp.\n- File cấu hình `relabel_configs` và Recording Rules chuẩn hóa.",
        "related_skills": "dex-alert-quality-engineering, dex-log-pipeline-design, dex-distributed-tracing",
        "realistic_usage": "Một công ty công nghệ bị Prometheus OOM liên tục vào giờ cao điểm. Nhờ kiểm toán TSDB, họ phát hiện thư viện HTTP client tự động thêm header `User-Agent` của từng điện thoại khách hàng vào label của metric. Xóa bỏ label này lập tức giảm số series từ 2.4 triệu xuống còn 45,000, cứu sống hệ thống monitoring."
    },

    # 139. dex-oncall-handover
    "dex-oncall-handover": {
        "desc": "Structure and execute comprehensive on-call shifts, handovers, runbook updates, and incident post-shift briefings with zero knowledge loss. Use to professionalize engineering reliability operations.",
        "purpose": "Thiết lập quy trình bàn giao ca trực vận hành (On-call Handover) có cấu trúc, chuyên nghiệp và liền mạch; bảo đảm chuyển giao đầy đủ thông tin về các sự cố đang diễn ra, các cảnh báo bất thường, các thay đổi triển khai gần nhất và cập nhật runbook thực tế mà không làm thất thoát tri thức giữa các kỹ sư trực ca.",
        "activation": "- Thay đổi ca trực hàng tuần giữa các kỹ sư SRE / Dev on-call.\n- Sau một tuần trực có nhiều sự cố lớn hoặc các cảnh báo liên tục tái diễn.\n- Chuẩn bị cho các kỳ nghỉ lễ dài ngày đòi hỏi sự sẵn sàng cao độ.",
        "when_not_to_use": "- Không biến buổi bàn giao thành cuộc họp phê bình cá nhân về các sai sót trong ca trực.\n- Không bàn giao qua loa chỉ bằng một tin nhắn 'Mọi thứ ổn' trên Slack.",
        "inputs": "- Nhật ký sự cố PagerDuty trong 7 ngày qua.\n- Danh sách các release/deployment và thay đổi cấu hình hạ tầng trong ca trực.\n- Trạng thái các sự cố chưa giải quyết dứt điểm (Unresolved / Mitigated but not Root-caused).",
        "preconditions": "- Có template bàn giao ca trực chuẩn hóa trong công cụ tài liệu (Confluence, Notion, Markdown repo).",
        "core_concepts": "- Handover Meeting: Cuộc gặp ngắn 15-30 phút giữa kỹ sư sắp hết ca (Outgoing) và kỹ sư nhận ca mới (Incoming).\n- Actionable Follow-ups: Mọi giải pháp tạm thời (workaround) áp dụng trong ca trực bắt buộc phải được tạo ticket Jira để giải quyết triệt để.\n- Runbook Hygiene: Nếu một sự cố xảy ra mà runbook không có hoặc viết sai, kỹ sư trong ca trực có trách nhiệm cập nhật runbook trước khi bàn giao.",
        "decision_rules": "- Nếu có sự cố mức SEV-1/SEV-2 chưa đóng: kỹ sư outgoing phải ở lại cùng phối hợp cho đến khi hệ thống ổn định hoặc được sự đồng thuận bàn giao của lead.\n- Kiểm tra quyền truy cập (VPN, PagerDuty schedule, Cloud access) của kỹ sư incoming ngay trong buổi bàn giao.",
        "failure_scenarios": "- Kỹ sư hết ca tắt máy đi ngủ trong khi một sự cố nghiêm trọng đang âm ỉ diễn ra nhưng kỹ sư mới vào ca chưa nắm được bối cảnh.",
        "workflow": "1. Kỹ sư outgoing điền thông tin vào Handover Template trước giờ bàn giao 2 tiếng.\n2. Tổ chức buổi trao đổi trực tiếp (hoặc async call) đi qua từng mục trong biên bản.\n3. Rà soát danh sách alert silences và scheduled maintenances sắp tới.\n4. Kỹ sư incoming xác nhận nhận ca và kiểm tra công cụ nhận cảnh báo (điện thoại, app).\n5. Lưu trữ biên bản bàn giao vào kho lưu trữ nội bộ để phục vụ kiểm toán vận hành.",
        "example": "```markdown\n# On-Call Handover Report\n**Ca trực:** Tuần 42 (15/10 - 22/10)\n**Outgoing:** Alex Nguyen | **Incoming:** John Doe\n\n### 1. Tổng kết sự cố (Incidents):\n- INC-102 (SEV-2): DB connection pool timeout lúc 02:00 sáng thứ Ba. Đã tăng pool lên 200. Ticket xử lý gốc: JIRA-4521.\n\n### 2. Các cảnh báo cần lưu ý:\n- Alert `HighDiskUsage` trên node `worker-04` đang bị silence 24h để chờ bảo trì.\n\n### 3. Deployments sắp tới:\n- Migration database lớn vào 20:00 thứ Tư.\n```",
        "verification_commands": "```bash\n# Kiểm tra lịch trực PagerDuty và xác nhận ca trực hiện tại\npd schedule list-shifts --schedule-id=P123456\n```",
        "anti_patterns": "- Giấu giếm các sự cố nhỏ hoặc các thao tác thủ công không chuẩn trong ca trực.\n- Để kỹ sư mới vào công ty trực ca chính một mình mà không có shadow/mentor dự phòng.",
        "quality_gates": "- 100% các sự cố trong ca trực đều có liên kết tới Post-mortem hoặc Jira action item.\n- Kỹ sư nhận ca xác nhận đã truy cập được toàn bộ hệ thống giám sát và paging.",
        "security_constraints": "- Thu hồi các quyền truy cập tạm thời (Elevated break-glass access) đã cấp cho kỹ sư trong ca trực khi hết phiên.",
        "expected_outputs": "- Biên bản bàn giao ca trực hoàn chỉnh theo mẫu chuẩn.\n- Danh sách cập nhật tài liệu Runbooks cho các sự cố mới.",
        "related_skills": "dex-incident-retrospective-authoring, dex-alert-quality-engineering, dex-operational-game-days",
        "realistic_usage": "Một sự cố thanh toán bị lặp lại 3 lần trong 1 tháng vì mỗi lần kỹ sư trực chỉ khởi động lại pod mà không ghi lại. Sau khi áp dụng quy trình Handover chuẩn, kỹ sư ca trước ghi rõ cảnh báo rò rỉ bộ nhớ, kỹ sư ca sau đã chủ động phân tích heap dump và tìm ra lỗi leak trong thư viện HTTP client."
    },

    # 140. dex-operational-game-days
    "dex-operational-game-days": {
        "desc": "Plan, orchestrate, and facilitate controlled chaos engineering game days and failure injection exercises to validate team incident response and system resilience. Use to prepare teams for catastrophic production events.",
        "purpose": "Lập kế hoạch, điều phối và thực thi các buổi diễn tập sự cố thực chiến có kiểm soát (Operational Game Days / Chaos Engineering Drills); chủ động cấy lỗi hạ tầng (kill pod, ngắt mạng, làm đầy ổ đĩa, trễ database) nhằm kiểm chứng năng lực phản ứng của đội ngũ kỹ sư và độ bền vững của hệ thống trong môi trường an toàn.",
        "activation": "- Chuẩn bị phát hành phiên bản hệ sinh thái mới với kiến trúc phân tán phức tạp.\n- Định kỳ hàng quý để tôi luyện phản xạ xử lý sự cố cho các kỹ sư mới.\n- Xác minh xem các cơ chế tự động phục hồi (Auto-healing, Failover) có thực sự hoạt động như thiết kế hay không.",
        "when_not_to_use": "- Không diễn tập trên Production vào những ngày cao điểm kinh doanh của công ty.\n- Tuyệt đối không cấy lỗi nếu không có nút dừng khẩn cấp (Blast Radius & Abort Button) được kiểm chứng trước.",
        "inputs": "- Giả thuyết kiểm chứng (Hypothesis: 'Nếu Region US-East bị mất kết nối, hệ thống sẽ tự chuyển sang US-West trong 60 giây và khách hàng không thấy lỗi 5xx').\n- Công cụ cấy lỗi (Chaos Mesh, LitmusChaos, Gremlin, AWS Fault Injection Simulator).\n- Kế hoạch an toàn và phân công vai trò (Incident Commander, Chaos Injector, Observers).",
        "preconditions": "- Có dashboard giám sát thời gian thực hiển thị chỉ số trải nghiệm người dùng (Steady-state metrics).",
        "core_concepts": "- Blast Radius Control: Giới hạn phạm vi ảnh hưởng của lỗi (ví dụ: chỉ cấy lỗi trên 10% traffic thử nghiệm hoặc môi trường Staging).\n- Stop-the-World Button: Bất kỳ ai trong buổi diễn tập nhận thấy rủi ro vượt tầm kiểm soát đều có quyền bấm nút hủy để hoàn trả hệ thống về nguyên trạng ngay lập tức.\n- Steady-State Hypothesis: Đo lường trạng thái bình thường của hệ thống trước khi cấy lỗi để so sánh sự suy giảm trong suốt quá trình thử nghiệm.",
        "decision_rules": "- Nếu chỉ số nghiệp vụ cốt lõi giảm quá 5% trên môi trường thực tế: kích hoạt Abort ngay lập tức.\n- Mọi kết quả dù thành công hay thất bại đều phải được ghi nhận công tâm, không trừng phạt (Blameless culture).",
        "failure_scenarios": "- Kịch bản cấy lỗi làm xóa mất dữ liệu vĩnh viễn do không cô lập môi trường lưu trữ an toàn.",
        "workflow": "1. Họp thống nhất kịch bản và giả thuyết cần kiểm chứng với các bên liên quan.\n2. Kiểm tra trạng thái bình thường (Steady-state) của toàn bộ hệ thống.\n3. Bắt đầu cấy lỗi ở mức nhẹ nhất (ví dụ: tạo 100ms network latency).\n4. Quan sát phản ứng của hệ thống giám sát và hành động xử lý của đội trực ca.\n5. Dừng cấy lỗi, kiểm tra khả năng tự phục hồi của hệ thống về trạng thái ban đầu.\n6. Tổ chức buổi tổng kết rút kinh nghiệm và tạo danh sách cải tiến kỹ thuật.",
        "example": "```yaml\n# Kịch bản Chaos Mesh: Giả lập trễ mạng 300ms đối với Database Pods\napiVersion: chaos-mesh.org/v1alpha1\nkind: NetworkChaos\nmetadata:\n  name: db-delay-game-day\nspec:\n  action: delay\n  mode: all\n  selector:\n    namespaces: ['production-staging']\n    labelSelectors: {'app': 'postgres'}\n  delay:\n    latency: '300ms'\n    jitter: '20ms'\n  duration: '10m'\n```",
        "verification_commands": "```bash\n# Áp dụng kịch bản chaos và sẵn sàng lệnh xóa rollback khẩn cấp\nkubectl apply -f chaos-scenario.yaml\n# Lệnh Abort khẩn cấp:\nkubectl delete -f chaos-scenario.yaml\n```",
        "anti_patterns": "- Diễn tập bí mật kiểu đánh úp mà không thông báo cho ban quản lý và lead trực ca, gây hoảng loạn không cần thiết.\n- Không chuẩn bị trước lệnh rollback dẫn đến hệ thống bị kẹt trong trạng thái lỗi sau buổi diễn tập.",
        "quality_gates": "- Đội ngũ kỹ sư phát hiện và cô lập được lỗi trong vòng 5 phút kể từ khi cấy lỗi.\n- Hệ thống tự động phục hồi 100% trong vòng 2 phút sau khi ngừng cấy lỗi.",
        "security_constraints": "- Tuân thủ nghiêm ngặt ranh giới môi trường được cấp phép, không bao giờ để kịch bản chaos lan sang các cụm dữ liệu khách hàng chưa được bảo vệ.",
        "expected_outputs": "- Bản kế hoạch Game Day chi tiết (Run of Show).\n- Báo cáo kết quả diễn tập và danh sách các lỗ hổng kiến trúc được phát hiện.",
        "related_skills": "dex-service-failover, dex-oncall-handover, dex-load-and-stress-testing",
        "realistic_usage": "Một ngân hàng tổ chức Game Day giả lập sự cố sập một Availability Zone trên AWS. Trong buổi diễn tập, họ phát hiện cơ chế DNS failover bị kẹt do TTL của nhà mạng bị cache 24 giờ. Nhờ phát hiện trước trong môi trường diễn tập có kiểm soát, họ đã kịp thời chuyển sang dùng Anycast IP trước khi sự cố thật xảy ra."
    }
}

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    skills_base = os.path.join(root_dir, ".agents", "skills")
    
    print(f"=== GENERATING GROUP M (121-130) & GROUP N (131-140) ===")
    print(f"Target directory: {skills_base}")
    
    created_count = 0
    for skill_id, data in SKILLS_M_N.items():
        skill_dir = os.path.join(skills_base, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        skill_path = os.path.join(skill_dir, "SKILL.md")
        
        content = SKILL_TEMPLATE.format(
            skill_id=skill_id,
            desc=data["desc"],
            purpose=data["purpose"],
            activation=data["activation"],
            when_not_to_use=data["when_not_to_use"],
            inputs=data["inputs"],
            preconditions=data["preconditions"],
            core_concepts=data["core_concepts"],
            decision_rules=data["decision_rules"],
            failure_scenarios=data["failure_scenarios"],
            workflow=data["workflow"],
            example=data["example"],
            verification_commands=data["verification_commands"],
            anti_patterns=data["anti_patterns"],
            quality_gates=data["quality_gates"],
            security_constraints=data["security_constraints"],
            expected_outputs=data["expected_outputs"],
            related_skills=data["related_skills"],
            realistic_usage=data["realistic_usage"]
        )
        
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
            
        created_count += 1
        print(f"[{created_count}/20] Created {skill_id}")

    print(f"\nSUCCESS: Generated {created_count} skills for Group M & N.")

if __name__ == "__main__":
    main()
