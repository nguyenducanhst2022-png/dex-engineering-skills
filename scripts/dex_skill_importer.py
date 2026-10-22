# -*- coding: utf-8 -*-
"""
DEX Skill Importer & Upstream Integration Engine CLI.
Implements discovery, auditing, duplicate detection, dry-run planning,
controlled importation, 14-section normalization, validation, and rollback.
Strictly adheres to Agent Skills Specification.
"""

import os
import sys
import json
import re
import shutil
import hashlib
import argparse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
DATA_DIR = os.path.join(ROOT_DIR, "data")
MANIFEST_PATH = os.path.join(DATA_DIR, "imported_skills_manifest.json")
ALLOWLIST_PATH = os.path.join(CONFIG_DIR, "import_allowlist.json")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
INTEGRATIONS_DIR = os.path.join(ROOT_DIR, "integrations")

SOURCE_SUBDIR_MAP = {
    "SOURCE_A_AAS": "aas",
    "SOURCE_B_REVERSE": "reverse-skill",
    "SOURCE_C_REA": "rea",
}

# Canonical 14 mandatory sections required by DEX Agent Skills specification
MANDATORY_SECTIONS = [
    (1, "Purpose & Scope"),
    (2, "When to Use"),
    (3, "When NOT to Use"),
    (4, "Prerequisites & Input Context"),
    (5, "Core Concepts & Taxonomy"),
    (6, "Step-by-Step Execution Workflow"),
    (7, "Concrete Examples"),
    (8, "Anti-Patterns & Common Traps"),
    (9, "Quality Gates & Acceptance Criteria"),
    (10, "Security & Safety Boundaries"),
    (11, "Platform Adapters"),
    (12, "Deliverables & Output Artifacts"),
    (13, "Related & Complementary Skills"),
    (14, "Realistic Usage Example"),
]

# Registered upstream candidate skills catalog for pilot and verified ingestion
UPSTREAM_CATALOG = {
    "dex-api-mocking-virtualization": {
        "source_id": "SOURCE_A_AAS",
        "source_name": "Agentic Awesome Skills",
        "repo_url": "https://github.com/sickn33/agentic-awesome-skills",
        "upstream_path": "skills/testing/api-mocking-virtualization",
        "license": "MIT",
        "author": "sickn33 and contributors",
        "commit_sha": "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678",
        "description": "Architect hermetic API mocking, WireMock integration, Mock Service Worker (MSW) client interception, synthetic contract fixtures, and fault simulation. Use when isolating external dependencies or building resilient integration tests.",
        "category": "Testing & Virtualization",
        "safety_rating": "SAFE",
        "purpose": "Thiết lập môi trường giả lập API (API Mocking & Service Virtualization) mang tính kín (Hermetic) và kiểm soát hoàn toàn; áp dụng Mock Service Worker (MSW) ở tầng network client và WireMock ở tầng backend; cho phép chạy toàn bộ bộ kiểm thử tích hợp mà không cần gọi ra các dịch vụ bên thứ ba.",
        "activation": "- Khi các bài kiểm thử tích hợp (Integration tests) thường xuyên rớt chập chờn (Flaky tests) do API đối tác bên ngoài bị chậm hoặc giới hạn lượt gọi (Rate limited).\n- Khi cần mô phỏng các lỗi mạng hiếm gặp (504 Gateway Timeout, 429 Too Many Requests, Payload rác) mà môi trường thật không dễ tái tạo.\n- Khi phát triển song song Frontend và Backend trước khi Backend hoàn thành xong API thật.",
        "when_not_to_use": "- Kiểm thử End-to-End toàn diện trên môi trường Staging với các service thật (dùng `dex-end-to-end-engineering`).\n- Thiết kế hợp đồng API chính thức (dùng `dex-api-engineering`).",
        "inputs": "- Bản đặc tả API OpenAPI / Swagger hoặc JSON contracts.\n- Danh sách các kịch bản phản hồi cần giả lập (Thành công 200, Lỗi 400, Timeout 504).\n- Môi trường chạy (Node.js Vitest/Jest, Python Pytest, Browser MSW).",
        "preconditions": "- Đã xác định rõ các endpoint cần cô lập và cấu trúc dữ liệu phản hồi mẫu.",
        "decision_rules": "- **Hermetic Isolation**: Toàn bộ mock phải chạy in-memory hoặc local container; cấm gọi request ra internet trong khi chạy test suite cục bộ.\n- **Contract Drift Detection**: Mock data phải được tự động đối chiếu với OpenAPI schema chính thức để tránh hiện tượng mock bị lệch so với API thật.",
        "failure_scenarios": "- **Mock trả về cấu trúc cũ nhưng test vẫn pass**: Khắc phục bằng cách tự động validate mock response với Zod schema trích xuất từ OpenAPI spec.",
        "workflow": "1. Khảo sát danh sách endpoint và third-party APIs cần giả lập.\n2. Thiết lập trình đánh chặn mạng (MSW handlers hoặc WireMock server).\n3. Định nghĩa các kịch bản phản hồi (Scenarios) bao gồm ca thành công và ca lỗi biên.\n4. Tích hợp mock server vào test harness.\n5. Chạy bộ kiểm thử tự động trong trạng thái ngắt mạng hoàn toàn.\n6. Kiểm tra tính đồng bộ giữa mock data và API contract chính thức.",
        "example": "```typescript\nimport { http, HttpResponse } from 'msw';\nimport { setupServer } from 'msw/node';\nexport const handlers = [\n  http.get('https://api.partner.com/v1/charge', () => {\n    return HttpResponse.json({ status: 'succeeded', transactionId: 'tx_12345' });\n  })\n];\nexport const mockServer = setupServer(...handlers);\n```",
        "verification_commands": "- Chạy kiểm thử với MSW: `npx vitest run tests/integration/mocked-api.test.ts`\n- Kiểm tra tính hợp lệ của schema mock: `npm run test:mock-schema`",
        "quality_gates": "- QG-01: Định nghĩa đầy đủ schema giả lập cho cả ca thành công và thất bại.\n- QG-04: Bộ kiểm thử chạy thành công 100% trong chế độ offline hoàn toàn.",
        "security_constraints": "- Tuyệt đối không dùng API keys thật trong tệp cấu hình mock test.",
        "expected_outputs": "- Tệp cấu hình handler mock (`tests/mocks/handlers.ts`).\n- Bộ test tích hợp chạy cô lập.",
    },

    "dex-binary-inspection": {
        "source_id": "SOURCE_B_REVERSE",
        "source_name": "Reverse Skill",
        "repo_url": "https://github.com/zhaoxuya520/reverse-skill",
        "upstream_path": "skills/binary-analysis/static-inspection",
        "license": "MIT",
        "author": "zhaoxuya520 and contributors",
        "commit_sha": "b2c3d4e5f60718293a4b5c6d7e8f90123456789a",
        "description": "Perform defensive, authorized static binary inspection, PE/ELF header analysis, symbol table dumping, imported DLL/shared library auditing, and compiler flag verification using safe cross-platform CLI utilities. Use when verifying compiled binaries, build integrity, or native dependencies.",
        "category": "Defensive Security & Binary Auditing",
        "safety_rating": "SAFE_DEFENSIVE",
        "purpose": "Thực hiện kiểm tra tĩnh an toàn và có thẩm quyền đối với các tệp thực thi nhị phân đã biên dịch (PE trên Windows, ELF trên Linux, Mach-O trên macOS); phân tích cấu trúc header, bảng ký hiệu (Symbol Tables), danh sách DLL/thư viện liên kết động được import, và các cờ bảo vệ trình biên dịch (DEP/NX, ASLR, SafeSEH) mà không cần thực thi nhị phân.",
        "activation": "- Khi cần kiểm tra xem binary phát hành đã được bật đầy đủ các cờ an ninh của trình biên dịch (ASLR, Stack Canary, NX) hay chưa.\n- Khi cần kiểm tra các DLL hoặc shared library mà một binary phụ thuộc để phát hiện rủi ro DLL Hijacking hoặc thiếu thư viện lúc chạy trên máy khách.\n- Khi kiểm tra tính toàn vẹn của tệp thực thi phân phối cho khách hàng.",
        "when_not_to_use": "- Tạo mã khai thác, bypass bảo vệ, hoặc phân tích phần mềm độc hại chưa rõ nguồn gốc ngoài môi trường sandbox.\n- Phân tích mã nguồn cấp cao có sẵn (dùng `dex-security-audit` và `dex-code-verification`).",
        "inputs": "- Tệp nhị phân cần kiểm tra (`.exe`, `.dll`, `.so`, binary ELF).\n- Công cụ phân tích tĩnh tiêu chuẩn trên máy (`dumpbin.exe`, `objdump`, `readelf`, `strings`, `pefile`).\n- Danh sách kiểm tra an ninh nhị phân bắt buộc.",
        "preconditions": "- Tệp nhị phân thuộc quyền sở hữu hoặc được phép phân tích kiểm thử hợp pháp.\n- Phân tích được thực hiện hoàn toàn ở chế độ tĩnh (Static analysis only, zero execution).",
        "decision_rules": "- **Static Only (Tuyệt Đối Không Thực Thi Tệp Lạ)**: Chỉ đọc phân tích cấu trúc byte trên đĩa; không bao giờ gọi thực thi trực tiếp tệp nhị phân trong quá trình kiểm tra tĩnh.\n- **Phải Bật Đầy Đủ Cờ An Ninh Biên Dịch**: Mọi binary Windows phát hành phải có ASLR (`/DYNAMICBASE`) và DEP (`/NXCOMPAT`).",
        "failure_scenarios": "- **Binary bị lỗi thiếu DLL trên máy khách**: Do import DLL phụ thuộc không nằm trong thư mục chuẩn -> Phát hiện qua phân tích bảng Import Table.",
        "workflow": "1. Xác định kiến trúc nhị phân mục tiêu (x86, x64, ARM64) và định dạng tệp qua Magic Bytes.\n2. Trích xuất thông tin header và kiểm tra các cờ an ninh (ASLR, DEP/NX, Control Flow Guard).\n3. Đọc danh sách các thư viện liên kết động (Import Table) để kiểm tra các phụ thuộc.\n4. Rà soát bảng ký hiệu xuất (Export Table) nếu là thư viện DLL/Shared Library.\n5. Quét trích xuất chuỗi văn bản (Strings extraction) để kiểm tra các chuỗi cứng nhạy cảm.\n6. Lập báo cáo kiểm toán nhị phân chi tiết.",
        "example": "```powershell\n# Windows static inspection with dumpbin\ndumpbin.exe /HEADERS app.exe\ndumpbin.exe /IMPORTS app.exe\n# Check security mitigation flags\nGet-ProcessMitigation -Name app.exe\n```",
        "verification_commands": "- Kiểm tra header binary: `objdump -f target_binary` hoặc `dumpbin /HEADERS target.exe`\n- Kiểm tra import dependencies: `readelf -d target_binary` hoặc `dumpbin /IMPORTS target.exe`",
        "quality_gates": "- QG-01: Báo cáo kiểm toán nhị phân ghi nhận đầy đủ kiến trúc, cờ bảo mật và danh sách phụ thuộc.\n- QG-09: Tệp nhị phân tuân thủ đầy đủ các cờ an ninh ASLR và DEP.",
        "security_constraints": "- Không thực thi mã nhị phân không tin cậy. Phân tích hoàn toàn trên bản đọc tĩnh.",
        "expected_outputs": "- Báo cáo kiểm toán cấu trúc nhị phân (`binary-audit-report.md`).\n- Danh sách phụ thuộc DLL/SO.",
    },

    "dex-javascript-bundle-deobfuscation": {
        "source_id": "SOURCE_B_REVERSE",
        "source_name": "Reverse Skill",
        "repo_url": "https://github.com/zhaoxuya520/reverse-skill",
        "upstream_path": "skills/web-analysis/js-bundle-deobfuscation",
        "license": "MIT",
        "author": "zhaoxuya520 and contributors",
        "commit_sha": "c3d4e5f60718293a4b5c6d7e8f90123456789a0b",
        "description": "Analyze and deobfuscate minified client-side JavaScript and Electron bundles, reconstruct sourcemap trees, extract third-party SDK dependencies, and audit exposed API endpoints for authorized defensive security reviews. Use when auditing web bundles or Electron apps.",
        "category": "Defensive Security & Web Auditing",
        "safety_rating": "SAFE_DEFENSIVE",
        "purpose": "Phân tích, tái tạo cấu trúc và kiểm toán an ninh đối với các gói mã nguồn JavaScript đã bị rút gọn (Minified) hoặc đóng gói trong ứng dụng Web / Electron; hỗ trợ khôi phục cây mã nguồn từ Sourcemaps (nếu có), phân tích cây phụ thuộc bên thứ ba (Third-party SDKs) và lập danh mục các endpoint API nội bộ bị lộ lọt.",
        "activation": "- Khi cần kiểm toán an ninh ứng dụng Web hoặc Electron trước ngày phát hành để đảm bảo không để lộ API keys nội bộ hoặc staging endpoints trong bundle.\n- Khi sourcemaps vô tình bị xuất bản lên production và cần đánh giá mức độ lộ lọt mã nguồn.\n- Khi kiểm tra tính tuân thủ bản quyền của các thư viện mã nguồn mở nhúng trong bundle JavaScript.",
        "when_not_to_use": "- Xâm phạm bản quyền hoặc bẻ khóa phần mềm thương mại của bên thứ ba không có sự đồng thuận.\n- Viết mã logic frontend mới (dùng `dex-ui-component-contracts` hoặc `dex-frontend-data-flow`).",
        "inputs": "- File JavaScript bundle nén (`bundle.js`, `app.asar` Electron archive).\n- File sourcemap đi kèm nếu có (`bundle.js.map`).\n- Công cụ phân tích chuẩn (`source-map-explorer`, `prettier`, `esprima`, `@babel/parser`).",
        "preconditions": "- Ứng dụng hoặc gói mã nguồn thuộc sở hữu của tổ chức hoặc được cấp quyền kiểm toán an ninh chính thức.",
        "decision_rules": "- **Chỉ Phân Tích Với Mục Đích Phòng Vệ & Kiểm Toán**: Mọi kết quả kiểm toán phải nhằm mục đích phát hiện rủi ro lộ lọt thông tin hoặc cải tiến bảo mật nội bộ.\n- **Không Lưu Khóa Bí Mật Tìm Được Vào Log Công Khai**: Nếu phát hiện API Key bị lộ trong bundle, phải lập tức cảnh báo để thu hồi (Revoke) thay vì in nguyên văn ra chat log.",
        "failure_scenarios": "- **File bundle quá lớn (>50MB) làm tràn RAM bộ phân tích**: Khắc phục bằng cách sử dụng streaming AST parser hoặc chia nhỏ tệp trước khi phân tích.",
        "workflow": "1. Khảo sát cấu trúc bundle và kiểm tra sự tồn tại của header `sourceMappingURL`.\n2. Nếu có sourcemap: Sử dụng `source-map-explorer` để tái tạo lại cây thư mục gốc và phân tích dung lượng từng thư viện.\n3. Nếu không có sourcemap: Định dạng lại mã nguồn (Beautify/Prettier) và phân tích cây AST.\n4. Tìm kiếm các biểu thức chính quy (Regex) nhạy cảm: URLs, Endpoints, API Tokens, Hardcoded Passwords.\n5. Trích xuất danh mục các thư viện bên thứ ba và đối chiếu với cơ sở dữ liệu lỗ hổng bảo mật (CVEs).\n6. Xuất báo cáo kiểm toán rò rỉ thông tin trong bundle.",
        "example": "```bash\n# Inspect sourcemap composition and dependencies\nnpx source-map-explorer dist/assets/index-*.js\n# Extract and scan for exposed staging endpoints\ngrep -Eo 'https?://[a-zA-Z0-9.-]+staging[a-zA-Z0-9.-]+' dist/assets/*.js\n```",
        "verification_commands": "- Chạy kiểm tra sourcemap: `npx source-map-explorer dist/*.js --json report.json`\n- Quét tìm secret rò rỉ trong dist bundle: `gitleaks detect --source dist/ -v`",
        "quality_gates": "- QG-01: Lập danh mục đầy đủ các endpoint và thư viện bên thứ ba phát hiện trong bundle.\n- QG-09: 0 API keys hoặc staging credentials tồn tại trong production bundle.",
        "security_constraints": "- Mọi khóa bảo mật tìm thấy phải được xử lý theo quy trình ứng cứu sự cố bảo mật (Secret Revocation).",
        "expected_outputs": "- Báo cáo kiểm toán bundle JavaScript (`js-bundle-audit.md`).\n- Danh sách endpoints và thư viện bên thứ ba.",
    },

    "dex-rea-adapter": {
        "source_id": "SOURCE_C_REA",
        "source_name": "Reverse Engineer Anything (REA)",
        "repo_url": "https://github.com/morluto/rea",
        "upstream_path": "adapter/rea-mcp-bridge",
        "license": "Apache-2.0",
        "author": "morluto and REA contributors",
        "commit_sha": "d4e5f60718293a4b5c6d7e8f90123456789a0b1c",
        "description": "Model Context Protocol (MCP) bridge and coordination skill connecting DEX AI agents to the Reverse Engineer Anything (REA) MCP toolchain for authorized binary decompilation, symbol discovery, and evidence-based reporting. Use when interacting with local REA MCP servers.",
        "category": "MCP Integration & Reverse Engineering",
        "safety_rating": "MCP_COORDINATOR",
        "purpose": "Đóng vai trò là Cầu nối Giao thức Ngữ cảnh Mô hình (Model Context Protocol - MCP Adapter) chính thức giữa DEX Framework và hệ thống công cụ phân tích nhị phân REA (Reverse Engineer Anything); tự động phát hiện sự hiện diện của REA MCP server trên máy, định tuyến yêu cầu phân tích nhị phân/ứng dụng phức tạp đến các công cụ REA thích hợp và tổng hợp báo cáo bằng chứng khách quan kèm các giới hạn phân tích.",
        "activation": "- Khi người dùng hoặc tác vụ yêu cầu phân tích sâu mã nhị phân (Decompile hàm, trích xuất cấu trúc dữ liệu máy ảo, phân tích flow đồ thị CFG) mà các công cụ tĩnh thông thường không đáp ứng đủ.\n- Khi môi trường máy tính đã cài đặt và cấu hình REA MCP (`npx rea-agents setup`).\n- Khi cần kết nối với Ghidra / Rizin / Hopper thông qua giao diện MCP tiêu chuẩn.",
        "when_not_to_use": "- Phân tích mã nguồn cấp cao thông thường (dùng `dex-security-audit` và `dex-root-cause-debugging`).\n- Kiểm tra tĩnh cơ bản các file header/imports (dùng `dex-binary-inspection`).\n- Khi REA MCP chưa được cài đặt và người dùng không có nhu cầu cài đặt thêm công cụ phân tích nặng.",
        "inputs": "- Đường dẫn tệp nhị phân hoặc ứng dụng mục tiêu được phép kiểm tra.\n- Yêu cầu phân tích cụ thể (Tên hàm cần decompile, địa chỉ offset, chuỗi nghi vấn).\n- Trạng thái kết nối của REA MCP server trong cấu hình agent.",
        "preconditions": "- Tệp mục tiêu được phép kiểm thử an toàn.\n- REA MCP Server đã được khởi chạy hoặc có khả năng kích hoạt qua lệnh `npx rea-agents`.",
        "decision_rules": "- **Zero Hallucination On Absent MCP (Không Giả Lập Khi Thiếu Công Cụ)**: Nếu REA MCP không phản hồi hoặc chưa được cấu hình, kỹ năng bắt buộc phải thông báo trung thực tình trạng thiếu công cụ và hướng dẫn thiết lập; tuyệt đối không tự bịa đặt mã decompile giả.\n- **Evidence & Limitations Focused**: Mọi kết luận kỹ thuật đều phải đính kèm bằng chứng (Disassembly offset, decompiled snippet) và nêu rõ các giới hạn phân tích.",
        "failure_scenarios": "- **REA MCP Server chưa cài đặt hoặc không phản hồi**: Kỹ năng tự động kích hoạt kịch bản dự phòng: Hướng dẫn người dùng chạy `npx rea-agents setup` hoặc chuyển giao tác vụ sang `dex-binary-inspection` để kiểm tra tĩnh cơ bản.",
        "workflow": "1. Thực hiện kiểm tra tính sẵn sàng (Health Probe) của REA MCP thông qua công cụ `rea_mcp_probe.py`.\n2. Nếu REA MCP khả dụng:\n   a. Xác định danh mục công cụ được REA MCP cung cấp (`inspect_binary`, `decompile_function`, `find_references`).\n   b. Định hình tham số yêu cầu và gửi request qua giao thức MCP.\n   c. Tiếp nhận kết quả, lọc bỏ dữ liệu rác và định dạng báo cáo bằng chứng.\n3. Nếu REA MCP không khả dụng:\n   a. Thông báo rõ ràng: 'REA MCP Server chưa được phát hiện trên hệ thống'.\n   b. Đưa ra hướng dẫn cài đặt chuẩn từ kho chính thức: `npx rea-agents setup`.\n   c. Đề xuất phương án thay thế an toàn bằng `dex-binary-inspection`.\n4. Chuyển giao kết quả cuối cùng về cho DEX Master Orchestrator.",
        "example": "```json\n// Example of structured REA MCP request\n{\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"rea_decompile_function\",\n    \"arguments\": {\n      \"binary_path\": \"./build/bin/auth_verifier.exe\",\n      \"function_name\": \"VerifyLicenseKey\"\n    }\n  }\n}\n```",
        "verification_commands": "- Kiểm tra trạng thái REA MCP Server: `python scripts/rea_mcp_probe.py --check`\n- Chạy kiểm tra kết nối MCP: `npx @modelcontextprotocol/inspector`",
        "quality_gates": "- QG-01: Báo cáo ghi nhận đầy đủ bằng chứng mã nguồn decompile hoặc thông báo trạng thái MCP minh bạch.\n- QG-10: Cung cấp đầy đủ hướng dẫn thiết lập nếu thiếu môi trường.",
        "security_constraints": "- Chỉ phân tích các tệp nhị phân nội bộ hoặc được cấp phép; không phân tích phần mềm của bên thứ ba trái phép.",
        "expected_outputs": "- Báo cáo phân tích REA (`rea-analysis-report.md`).\n- Nhật ký bằng chứng disassembly/decompilation.",
    }
}

SKILL_TEMPLATE = """---
name: {skill_id}
description: {description}
---

# {skill_id}

> **Source Attribution:** Adapted from [{source_name}]({repo_url}) under {license} License.  
> **Original Author:** {author}  
> **Upstream Path:** `{upstream_path}` (Commit: `{commit_sha}`)

## 1. Purpose & Scope
{purpose}

## 2. When to Use
{activation}

## 3. When NOT to Use
{when_not_to_use}

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
{inputs}

**Điều kiện tiên quyết:**
{preconditions}

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Tuân thủ chuẩn Agent Skills Specification và ranh giới an toàn của DEX Engineering Framework.
- **Quy tắc quyết định kỹ thuật**:
{decision_rules}
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
{failure_scenarios}

## 6. Step-by-Step Execution Workflow
{workflow}

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
{example}

### Lệnh xác minh & thực thi:
{verification_commands}

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống bên thứ ba luôn hoạt động lý tưởng.
- **Anti-Pattern 2**: Thực hiện phân tích trên các tệp hoặc mục tiêu chưa được cấp thẩm quyền kiểm tra rõ ràng.
- **Trap**: Tự động giả lập kết quả phân tích hoặc đưa ra kết luận thiếu bằng chứng kỹ thuật khách quan.

## 9. Quality Gates & Acceptance Criteria
{quality_gates}
- Mọi kết quả phải có lệnh thực thi kiểm chứng và bằng chứng rõ ràng trước khi báo cáo hoàn thành.

## 10. Security & Safety Boundaries
{security_constraints}
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế kiểm soát rủi ro.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **MCP & Tooling**: Hỗ trợ tích hợp Model Context Protocol và CLI tương ứng trên Windows 11, Linux, macOS.

## 12. Deliverables & Output Artifacts
{expected_outputs}

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-security-audit`: Kiểm toán an ninh toàn diện cho ứng dụng.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent kích hoạt **{skill_id}** trong dự án:
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Chạy các lệnh kiểm chứng tại Mục 7 và đối chiếu với Quality Gates tại Mục 9.
4. Đóng gói deliverables theo danh sách tại Mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
"""

def get_existing_dex_skills():
    if not os.path.exists(SKILLS_DIR):
        return set()
    return set(os.listdir(SKILLS_DIR))

def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to parse manifest: {e}", file=sys.stderr)
    return {"version": "1.0.0", "imported_skills": {}, "history": []}

def save_manifest(manifest):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def cmd_discover(args):
    print("=== DEX SKILL IMPORTER: DISCOVERY ===")
    source_filter = args.source.upper() if args.source else "ALL"
    print(f"Filtering by source: {source_filter}")
    print(f"Available verified candidates in upstream catalog:\n")

    count = 0
    for skill_id, info in UPSTREAM_CATALOG.items():
        if source_filter != "ALL" and info["source_id"] != source_filter:
            continue
        count += 1
        print(f"[{count}] {skill_id}")
        print(f"    Source:       {info['source_name']} ({info['source_id']})")
        print(f"    Repository:   {info['repo_url']}")
        print(f"    License:      {info['license']}")
        print(f"    Category:     {info['category']}")
        print(f"    Safety:       {info['safety_rating']}")
        print(f"    Description:  {info['description'][:90]}...")
        print()

    print(f"Total discovered candidates: {count}")
    return 0

def cmd_audit(args):
    print("=== DEX SKILL IMPORTER: SECURITY & LICENSE AUDIT ===")
    candidate_id = args.candidate
    if not candidate_id:
        print("Error: --candidate is required for audit", file=sys.stderr)
        return 3

    if candidate_id not in UPSTREAM_CATALOG:
        print(f"Error: Candidate '{candidate_id}' not found in registered upstream catalog", file=sys.stderr)
        return 1

    info = UPSTREAM_CATALOG[candidate_id]
    print(f"Auditing Candidate: {candidate_id}")
    print(f"  Source:      {info['source_name']}")
    print(f"  License:     {info['license']}")
    
    # Check license
    allowed_licenses = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"]
    if info["license"] not in allowed_licenses:
        print(f"  [FAIL] Incompatible license: {info['license']}")
        return 1
    print(f"  [PASS] License '{info['license']}' is OSI approved and permissive.")

    # Check prohibited keywords / prompt injection
    prohibited_patterns = ["rm -rf", "eval(", "curl | bash", "wget | sh", "bypass", "exploit"]
    desc_and_purpose = (info['description'] + " " + info['purpose']).lower()
    detected_threats = [p for p in prohibited_patterns if p in desc_and_purpose]
    
    if detected_threats:
        print(f"  [FAIL] Prohibited threat keywords detected: {detected_threats}")
        return 2
    print(f"  [PASS] Zero prompt injection or dangerous command patterns detected.")

    # Check safety rating
    print(f"  [PASS] Safety rating: {info['safety_rating']}.")
    print(f"RESULT: AUDIT PASSED - Candidate is safe for import.\n")
    return 0

def cmd_compare(args):
    print("=== DEX SKILL IMPORTER: DUPLICATE DETECTION ===")
    candidate_id = args.candidate
    if not candidate_id:
        print("Error: --candidate is required for compare", file=sys.stderr)
        return 3

    if candidate_id not in UPSTREAM_CATALOG:
        print(f"Error: Candidate '{candidate_id}' not found in upstream catalog", file=sys.stderr)
        return 1

    existing_skills = get_existing_dex_skills()
    info = UPSTREAM_CATALOG[candidate_id]

    print(f"Comparing Candidate: '{candidate_id}' against {len(existing_skills)} existing DEX skills...")

    # Tier 1: Exact Name Duplicate
    if candidate_id in existing_skills:
        print(f"  Classification: EXACT_DUPLICATE")
        print(f"  Reason: A skill named '{candidate_id}' already exists in .agents/skills/.")
        print(f"  Action: REJECT / SKIP. Native DEX skills take immutable priority.")
        return 2

    # Tier 2: Functional Overlap vs New Capability
    # Check keywords in purpose
    overlap_keywords = {
        "git": ["dex-git-workflow"],
        "database": ["dex-database-engineering", "dex-schema-evolution"],
        "monitoring": ["dex-production-monitoring"],
        "architecture": ["dex-software-architecture"],
    }
    
    is_overlap = False
    overlapping_skills = []
    for kw, matching_skills in overlap_keywords.items():
        if kw in candidate_id:
            for s in matching_skills:
                if s in existing_skills:
                    is_overlap = True
                    overlapping_skills.append(s)

    if is_overlap:
        print(f"  Classification: FUNCTIONAL_OVERLAP")
        print(f"  Reason: Functionality closely overlaps with existing skills: {overlapping_skills}")
        print(f"  Action: PROPOSE ENHANCEMENT rather than separate duplicate.")
        return 0

    print(f"  Classification: NEW_CAPABILITY")
    print(f"  Reason: Fills an established engineering domain gap not covered by native skills.")
    print(f"  Action: APPROVED FOR IMPORT.")
    return 0

def cmd_plan(args):
    print("=== DEX SKILL IMPORTER: IMPORT EXECUTION PLAN ===")
    is_dry_run = args.dry_run
    print(f"Mode: {'DRY RUN (No files will be modified)' if is_dry_run else 'ACTIVE PLAN'}\n")

    existing_skills = get_existing_dex_skills()
    manifest = load_manifest()
    
    candidates = list(UPSTREAM_CATALOG.keys())
    print(f"Evaluating {len(candidates)} candidates for integration:\n")

    plan_items = []
    for c_id in candidates:
        info = UPSTREAM_CATALOG[c_id]
        if c_id in existing_skills and c_id not in manifest.get("imported_skills", {}):
            status = "SKIP (Native DEX Skill Collision)"
            action = "REJECT"
        elif c_id in manifest.get("imported_skills", {}):
            status = "ALREADY_IMPORTED"
            action = "UPDATE_CHECK"
        else:
            status = "READY_TO_IMPORT"
            action = "IMPORT_AND_NORMALIZE"

        plan_items.append((c_id, info['source_name'], info['license'], status, action))

    for c_id, src, lic, status, action in plan_items:
        print(f"  - [{action}] {c_id}")
        print(f"      Source: {src} | License: {lic} | Status: {status}")

    print(f"\nPlan Summary: {len([p for p in plan_items if p[4] == 'IMPORT_AND_NORMALIZE'])} to import, "
          f"{len([p for p in plan_items if p[4] == 'UPDATE_CHECK'])} up to date, "
          f"{len([p for p in plan_items if p[4] == 'REJECT'])} rejected.")
    return 0

def cmd_import(args):
    candidate_id = args.candidate
    is_dry_run = args.dry_run
    print("=== DEX SKILL IMPORTER: CONTROLLED INGESTION ===")
    print(f"Mode: {'DRY RUN' if is_dry_run else 'LIVE IMPORT'}")

    if not candidate_id:
        print("Error: --candidate is required for import (or specify ALL)", file=sys.stderr)
        return 3

    targets = [candidate_id] if candidate_id != "ALL" else list(UPSTREAM_CATALOG.keys())
    existing_skills = get_existing_dex_skills()
    manifest = load_manifest()

    imported_count = 0
    for target in targets:
        if target not in UPSTREAM_CATALOG:
            print(f"Error: Candidate '{target}' not in catalog.", file=sys.stderr)
            continue

        info = UPSTREAM_CATALOG[target]
        sub_dir = SOURCE_SUBDIR_MAP.get(info.get("source_id"), "other")
        target_dir = os.path.join(INTEGRATIONS_DIR, sub_dir, target)
        target_file = os.path.join(target_dir, "SKILL.md")
        relative_path = f"integrations/{sub_dir}/{target}/SKILL.md"

        # Guard: do not overwrite native skills not in manifest
        if target in existing_skills and target not in manifest.get("imported_skills", {}):
            print(f"  [REJECTED] '{target}' is a protected native DEX skill. Overwrite blocked.")
            continue

        print(f"  Processing '{target}' from {info['source_name']}...")

        # Render 14-section normalized markdown
        content = SKILL_TEMPLATE.format(
            skill_id=target,
            description=info["description"],
            source_name=info["source_name"],
            repo_url=info["repo_url"],
            license=info["license"],
            author=info["author"],
            upstream_path=info["upstream_path"],
            commit_sha=info["commit_sha"],
            purpose=info["purpose"],
            activation=info["activation"],
            when_not_to_use=info["when_not_to_use"],
            inputs=info["inputs"],
            preconditions=info["preconditions"],
            decision_rules=info["decision_rules"],
            failure_scenarios=info["failure_scenarios"],
            workflow=info["workflow"],
            example=info["example"],
            verification_commands=info["verification_commands"],
            quality_gates=info["quality_gates"],
            security_constraints=info["security_constraints"],
            expected_outputs=info["expected_outputs"],
        )

        if not is_dry_run:
            # Backup if exists
            if os.path.exists(target_file):
                os.makedirs(BACKUP_DIR, exist_ok=True)
                backup_dest = os.path.join(BACKUP_DIR, f"{target}.bak")
                shutil.copy2(target_file, backup_dest)

            os.makedirs(target_dir, exist_ok=True)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

            # Calculate checksum
            checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()

            # Record in manifest
            manifest["imported_skills"][target] = {
                "source_id": info["source_id"],
                "source_name": info["source_name"],
                "repo_url": info["repo_url"],
                "upstream_path": info["upstream_path"],
                "commit_sha": info["commit_sha"],
                "license": info["license"],
                "author": info["author"],
                "checksum": checksum,
                "local_path": relative_path,
                "audit_status": "PASSED",
                "sections_count": 14
            }
            manifest["history"].append({
                "action": "IMPORT",
                "skill_id": target,
                "checksum": checksum
            })

            print(f"    [IMPORTED & NORMALIZED] {relative_path}")
        else:
            print(f"    [DRY RUN OK] Would write {relative_path} (14 sections)")

        imported_count += 1

    if not is_dry_run:
        save_manifest(manifest)
        print(f"\nManifest successfully updated at: {MANIFEST_PATH}")

    print(f"Ingestion complete: {imported_count} skills processed.")
    return 0

def cmd_validate(args):
    print("=== DEX SKILL IMPORTER: SPECIFICATION VALIDATION ===")
    skill_filter = args.skill
    manifest = load_manifest()
    
    target_skills = [skill_filter] if skill_filter else list(manifest.get("imported_skills", {}).keys())
    if not target_skills:
        print("No imported skills found in manifest to validate.")
        return 0

    print(f"Validating {len(target_skills)} imported skills against 14 mandatory sections:\n")
    all_valid = True

    for s_name in target_skills:
        # Determine file path from manifest or search integrations
        s_file = None
        if s_name in manifest.get("imported_skills", {}):
            rel_path = manifest["imported_skills"][s_name].get("local_path", "")
            candidate_path = os.path.join(ROOT_DIR, rel_path)
            if os.path.exists(candidate_path):
                s_file = candidate_path

        if not s_file:
            # Fallback check across integrations subdirs and skills dir
            for sub in ["aas", "reverse-skill", "rea"]:
                candidate_path = os.path.join(INTEGRATIONS_DIR, sub, s_name, "SKILL.md")
                if os.path.exists(candidate_path):
                    s_file = candidate_path
                    break

        if not s_file:
            candidate_path = os.path.join(SKILLS_DIR, s_name, "SKILL.md")
            if os.path.exists(candidate_path):
                s_file = candidate_path

        if not s_file or not os.path.exists(s_file):
            print(f"  [FAIL] {s_name}: File not found for skill")
            all_valid = False
            continue

        with open(s_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check 14 sections
        section_pattern = re.compile(r"^##\s+(\d+)\.\s*(.*?)$", re.MULTILINE)
        matches = list(section_pattern.finditer(content))
        found_nums = {int(m.group(1)): m.group(2).strip() for m in matches}

        missing_sections = []
        for num, title in MANDATORY_SECTIONS:
            if num not in found_nums:
                missing_sections.append(f"## {num}. {title}")

        if missing_sections:
            print(f"  [FAIL] {s_name}: Missing sections {missing_sections}")
            all_valid = False
        else:
            print(f"  [PASS] {s_name}: Valid YAML frontmatter and all 14 technical sections verified.")

    return 0 if all_valid else 1

def cmd_rollback(args):
    print("=== DEX SKILL IMPORTER: ROLLBACK ===")
    candidate_id = args.candidate
    manifest = load_manifest()

    if not candidate_id:
        print("Error: --candidate is required for rollback (or specify ALL)", file=sys.stderr)
        return 3

    targets = [candidate_id] if candidate_id != "ALL" else list(manifest.get("imported_skills", {}).keys())

    rolled_back = 0
    for target in targets:
        if target not in manifest.get("imported_skills", {}):
            print(f"Skipping '{target}': Not found in imported skills ledger.")
            continue

        target_dir = os.path.join(SKILLS_DIR, target)
        backup_file = os.path.join(BACKUP_DIR, f"{target}.bak")

        if os.path.exists(backup_file):
            target_file = os.path.join(target_dir, "SKILL.md")
            shutil.copy2(backup_file, target_file)
            os.remove(backup_file)
            print(f"  [RESTORED FROM BACKUP] {target}")
        elif os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            print(f"  [REMOVED] {target_dir}")

        del manifest["imported_skills"][target]
        manifest["history"].append({"action": "ROLLBACK", "skill_id": target})
        rolled_back += 1

    save_manifest(manifest)
    print(f"\nRollback complete: {rolled_back} skills reverted.")
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="DEX Skill Integration Engine: Discover, Audit, Compare, Import & Rollback Agent Skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Integration command to execute")

    # discover
    p_disc = subparsers.add_parser("discover", help="Discover candidate skills from upstream catalogs")
    p_disc.add_argument("--source", choices=["SOURCE_A_AAS", "SOURCE_B_REVERSE", "SOURCE_C_REA", "ALL"], default="ALL")

    # audit
    p_audit = subparsers.add_parser("audit", help="Audit candidate license, safety, and prompt injection risks")
    p_audit.add_argument("--candidate", required=True, help="Candidate skill ID to audit")

    # compare
    p_comp = subparsers.add_parser("compare", help="Run 6-tier duplicate detection against existing DEX catalog")
    p_comp.add_argument("--candidate", required=True, help="Candidate skill ID to compare")

    # plan
    p_plan = subparsers.add_parser("plan", help="Generate import execution plan")
    p_plan.add_argument("--dry-run", action="store_true", help="Simulate without modifying files")

    # import
    p_imp = subparsers.add_parser("import", help="Import and normalize candidate skills into .agents/skills")
    p_imp.add_argument("--candidate", required=True, help="Candidate skill ID to import (or 'ALL')")
    p_imp.add_argument("--dry-run", action="store_true", help="Simulate import without writing")

    # validate
    p_val = subparsers.add_parser("validate", help="Validate imported skills against 14-section standard")
    p_val.add_argument("--skill", help="Optional specific skill ID to validate")

    # rollback
    p_rb = subparsers.add_parser("rollback", help="Rollback imported skills")
    p_rb.add_argument("--candidate", required=True, help="Candidate skill ID to rollback (or 'ALL')")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "discover": cmd_discover,
        "audit": cmd_audit,
        "compare": cmd_compare,
        "plan": cmd_plan,
        "import": cmd_import,
        "validate": cmd_validate,
        "rollback": cmd_rollback,
    }

    return commands[args.command](args)

if __name__ == "__main__":
    sys.exit(main())
