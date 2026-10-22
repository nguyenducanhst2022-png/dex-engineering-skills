---
name: dex-master-orchestrator
description: Master control plane to analyze engineering requests, select execution modes (QUICK, STANDARD, STRICT), coordinate across 300 specialized DEX skills (Groups A to AD) and segregated integrations, enforce 15 Quality Gates, and generate evidence-based audit reports. Use whenever starting any software engineering workflow.
---

# DEX Master Orchestrator

## 1. Purpose & Scope
Điều phối toàn bộ vòng đời phát triển, vận hành, bảo mật và hiện đại hóa phần mềm theo chuẩn **DEX Engineering Skills Framework v6.0**. Master Orchestrator đóng vai trò là bộ não điều khiển trung tâm (Root Control Plane) chịu trách nhiệm: phân tích sâu ý định và yêu cầu kỹ thuật của kỹ sư, phân loại miền kỹ nghệ và đánh giá rủi ro tác vụ, lựa chọn chế độ thực thi tối ưu (`QUICK`, `STANDARD`, hoặc `STRICT`), tra cứu danh mục **300 Specialized DEX Skills** (chia đều trong 30 nhóm chuyên môn A–AD) cùng các bộ tích hợp bên thứ ba (`integrations/`), kích hoạt tập kỹ năng tối thiểu cần thiết theo nguyên lý công bố tiệm tiến (Progressive Disclosure), kiểm soát nghiêm ngặt **15 Quality Gates (QG-01 đến QG-15)** và tổng hợp báo cáo nghiệm thu kèm bằng chứng thực thi minh bạch.

Triết lý cốt lõi v6.0:
`DISCOVER → AUDIT → SPECIFY → PLAN → BUILD → REVIEW → INTEGRATE → VALIDATE → DEBUG → STABILIZE → COMMIT → RELEASE → MAINTAIN`

## 2. When to Use
- Bắt đầu bất kỳ tác vụ kỹ thuật phần mềm mới nào từ người dùng, agent phụ trợ hoặc hệ thống CI/CD.
- Khi cần xác định chính xác lộ trình kỹ thuật cho các bài toán phức tạp, liên nhóm (ví dụ: Cloud migration, Advanced Verification, AI Systems, SRE Resiliency, DevSecOps, Visual Design Intelligence, Browser Automation, Authorized Reverse Engineering, Protocol Integration, Autonomous Agent Operations, Stream Analytics, Game Engineering, Software Trust & Distribution, Advanced SkillOps).
- Khi tác vụ đòi hỏi sự phối hợp tuần tự hoặc song song giữa nhiều kỹ năng chuyên biệt trong 300 skills.
- Khi cần kiểm soát rủi ro, bảo vệ branch Git và đảm bảo không có bất kỳ bước kiểm tra an ninh hay chất lượng nào bị bỏ qua.

## 3. When NOT to Use
- Trả lời các câu hỏi lý thuyết hoặc tra cứu định nghĩa đơn giản không làm thay đổi mã nguồn hay trạng thái hệ thống.
- Khi người dùng đã chỉ định tường minh một kỹ năng chuyên biệt duy nhất và không yêu cầu điều phối đa bước (ví dụ: `dex-sast-finding-triage` trên một file cụ thể).
- Khi đang ở giữa một tiến trình con do một chuyên môn khác đang trực tiếp xử lý (tránh can thiệp lặp vòng).

## 4. Prerequisites & Input Context
- **Yêu cầu của người dùng**: Mục tiêu nghiệp vụ, mô tả lỗi, yêu cầu kiến trúc hoặc kế hoạch phát hành.
- **Ngữ cảnh dự án**: `README.md`, `ARCHITECTURE.md`, `ROUTING_MATRIX.md`, `SKILLS_INDEX.md`, `CHANGELOG.md`, `manifests/dex-skills.json`.
- **Trạng thái kho mã nguồn**: Trạng thái Git (`git status`, commit hash, branch bảo vệ).
- **Môi trường kỹ thuật**: Windows 11, Linux, macOS, runtime (Node.js, Python, Go, Rust, C++, Java, .NET), container, cloud providers và MCP servers.

## 5. Core Concepts & Taxonomy
- **Nguyên lý Điều phối Tối thiểu (Principle of Minimal Sufficient Skills)**: Tuyệt đối không bao giờ nạp toàn bộ 300 kỹ năng vào cùng một phiên làm việc; chỉ chọn lọc chính xác các kỹ năng cốt lõi (Primary) và bổ trợ (Complementary) cho nhiệm vụ hiện tại để tránh gây nhiễu và tràn context window.
- **Tính Xác định & Minh Bạch (Determinism & Auditability)**: Mọi quyết định lựa chọn kỹ năng và đánh giá chất lượng phải dựa trên bằng chứng kỹ thuật khách quan, có thể tái lập được.
- **Phân Cấp Danh Mục 30 Nhóm Kỹ Năng Chuyên Môn (Groups A to AD)**:
  1. **Group A (01–10) Core Engineering**: Quy trình lập trình, ủy nhiệm, kiểm chứng, Git, tổ chức code, gỡ lỗi, tối ưu hiệu năng, bảo mật, CI/CD, phát hành.
  2. **Group B (11–20) Architecture & AI Agents**: Giám sát production, nợ kỹ thuật, kiến trúc, database, API, kiểm thử, agent engineering, multi-agent, context, đặc tả.
  3. **Group C (21–30) Production Engineering**: Phân tích tác động, phụ thuộc, độ tin cậy, tương tranh, khả năng tiếp cận, feature flags, code review, acceptance, bảo trì, E2E.
  4. **Group D (31–40) Frontend Engineering**: Hợp đồng UI, Design tokens, luồng dữ liệu frontend, biểu mẫu, định tuyến, hiệu năng web, SSR/SEO, đa ngôn ngữ, visual regression, tương thích trình duyệt.
  5. **Group E (41–50) Backend & Integration**: DDD, hàng đợi tác vụ ngầm, chiến lược cache, giao thức thời gian thực, xử lý file, search, event-driven, thao tác idempotent, thông báo, tác vụ định kỳ.
  6. **Group F (51–60) Data Engineering**: Hợp đồng dữ liệu, data pipeline, kiểm toán chất lượng dữ liệu, data lineage, tiến hóa schema, tối ưu query plan, vòng đời lưu trữ, lưu giữ dữ liệu, hoạch định dung lượng, phục hồi thảm họa.
  7. **Group G (61–70) AI & LLM Engineering**: Tích hợp LLM, pipeline RAG, đánh giá retrieval, đánh giá prompt, đánh giá model, hợp đồng tool calling, phân quyền agent, kiểm soát chi phí token, quan sát AI, quản trị dataset.
  8. **Group H (71–80) Developer Experience**: Bootstrap repository, quản trị monorepo, kỹ thuật CLI, kiến trúc plugin, đa nền tảng, đóng gói Windows, tài liệu dạng code, sinh code, công cụ lập trình viên, tự động hóa semver.
  9. **Group I (81–90) Security & Reliability**: Vòng đời phiên xác thực, phân quyền đa người thuê, quản trị bí mật, an toàn chuỗi cung ứng, mô hình hóa mối đe dọa, kiểm thử thuộc tính, thử nghiệm hỗn loạn, chỉ số thử nghiệm, tiến hóa hợp đồng API, postmortem sự cố.
  10. **Group J (91–100) Cloud & Infrastructure**: Đóng gói container tối ưu, triển khai Kubernetes, IaC Terraform, tích hợp dịch vụ cloud qua Workload Identity, triển khai zero-downtime Canary, mạng Service Mesh, chẩn đoán mạng phân tán, SLO & ngân sách lỗi, truy vết phân tán OpenTelemetry, FinOps tối ưu chi phí cloud.
  11. **Group K (101–110) Mobile & Desktop Engineering**: Kiến trúc Android Compose, kiến trúc iOS SwiftUI, bảo mật Electron, tích hợp Tauri Rust, đồng bộ ngoại tuyến offline-first, pipeline phát hành di động Fastlane, đo lường hiệu năng di động, thiết kế IPC type-safe cho desktop, tích hợp phần cứng cảm biến, phân phối cập nhật tự động an toàn cho desktop.
  12. **Group L (111–120) Product & Operations Engineering**: Đánh giá tác động quyền riêng tư DPIA, ánh xạ kiểm soát tuân thủ SOC 2/ISO, nhật ký kiểm toán bất biến Merkle/WORM, phát hiện sai lệch cấu hình drift, khám phá sản phẩm JTBD, ma trận ưu tiên tính năng RICE, thiết kế hệ thống tracking analytics, phân loại và điều phối phản hồi người dùng, tự động hóa runbook vận hành, đánh giá mức độ sẵn sàng vận hành sản xuất ORR.
  13. **Group M (121–130) Advanced Software Verification**: Static analysis rule authoring, mutation testing, API fuzz testing, differential testing, flaky test remediation, test data management, compatibility matrix testing, reproducible benchmarking, formal invariant checks, coverage risk analysis.
  14. **Group N (131–140) Advanced SRE & Distributed Systems**: Load and stress testing, traffic shaping and backpressure, rate limiting and quotas, distributed consistency, service failover, alert quality engineering, log pipeline design, metric cardinality control, on-call handover, operational game days.
  15. **Group O (141–150) Advanced Cloud Platform**: Serverless architecture, edge runtime engineering, cloud IAM policy review, cloud network design, GitOps workflows, Kubernetes policy enforcement, platform service catalog, environment promotion, service discovery, cloud resource tagging.
  16. **Group P (151–160) Language & Runtime Engineering**: TypeScript type safety, Node.js runtime diagnostics, Python project engineering, Rust unsafe audit, C++ memory safety, Go concurrency patterns, JVM performance diagnostics, .NET application engineering, WebAssembly integration, FFI boundary contracts.
  17. **Group Q (161–170) Advanced AI Systems**: MCP server design, vector index design, reranking strategies, structured LLM output, prompt injection defense, grounding citation audit, agent memory governance, multimodal input pipelines, agent evaluation harness, LLM fallback routing.
  18. **Group R (171–180) Product Design & User Research**: User journey mapping, information architecture, usability study design, accessibility automation, design handoff verification, product requirements writing, conversion funnel analysis, feature adoption analysis, user consent UX, supportability engineering.
  19. **Group S (181–190) Application Security Specialists**: SAST finding triage, DAST scoping, API abuse prevention, web security headers, browser extension hardening, SBOM verification, vulnerability remediation, security logging and detection, cryptographic API review, secure build runners.
  20. **Group T (191–200) SkillOps Engineering**: Skill discovery indexer, skill license provenance, skill semantic deduplication, skill security screening, skill import packaging, skill upstream sync, skill activation evaluation, skill host adapters, skill dependency graph, skill quality benchmarking.
  21. **Group U (201–210) Visual Design Intelligence**: Design brief synthesis, visual hierarchy audit, layout composition patterns, color contrast systems, fluid typography engineering, motion interaction specification, dashboard data storytelling, design reference evaluation, design system documentation, UI visual QA review.
  22. **Group V (211–220) Advanced Web Experiences**: Web animation performance, media delivery pipelines, HLS/DASH playback, progressive web apps, web push permission flow, search interface experience, virtualized infinite lists, web canvas rendering, WebGPU rendering fundamentals, frontend error recovery.
  23. **Group W (221–230) Browser Extensions & Automation**: Browser extension MV3, extension message security, extension background lifecycle, extension content script isolation, extension storage migration, browser automation testing, CDP observability, headless UI verification, web permission UX, cross-origin integration.
  24. **Group X (231–240) Authorized Reverse Engineering**: PE/ELF structure inspection, native symbol mapping, disassembly CFG reconstruction, managed assembly inspection, Electron artifact analysis, JavaScript sourcemap recovery, mobile package static audit, firmware metadata inspection, binary diff regression, reverse evidence chain. *(Phân tích phòng thủ và ủy quyền hợp pháp)*.
  25. **Group Y (241–250) Protocols & Service Integration**: MQTT client reliability, WebSocket session recovery, stream processing semantics, event schema registry, HTTP client connection pooling, OAuth/OIDC integration, webhook signature validation, API pagination cursors, service contract simulation, offline message delivery.
  26. **Group Z (251–260) AI Agent Operations**: LLM evaluation dataset design, agent task planning validation, agent trace replay, LLM human review gates, retrieval permission filtering, multimodal evaluation, AI safety red-teaming, agent long-running task checkpoints, MCP client integration, inference latency optimization.
  27. **Group AA (261–270) Advanced Data & Analytics**: SQL metric semantic layer, time-series diagnostics, data anomaly detection, feature store engineering, analytics cohort retention, A/B test statistical analysis, geospatial data pipelines, data warehouse cost tuning, backfill reconciliation, machine learning data drift.
  28. **Group AB (271–280) Native, Graphics & Game Engineering**: Chess engine search testing, simulation determinism, physics engine validation, game loop timing, rendering frame pacing, GPU shader profiling, GPU resource lifetime, native plugin ABI testing, real-time input latency, asset pipeline optimization.
  29. **Group AC (281–290) Software Trust & Distribution**: Open-source license scanning, third-party attribution, artifact signature verification, dependency vulnerability intelligence, secret rotation drills, code signing release process, software update trust chains, vulnerability disclosure workflows, maintainer contribution governance, release reproducibility audit.
  30. **Group AD (291–300) Advanced SkillOps Governance**: Skill catalog taxonomy, skill source integrity, skill risk scoring, skill reference graph, skill routing conflict tests, skill execution evidence ledger, skill documentation drift, skill upgrade migrations, skill rollback verification, skill retirement governance.
- **Ranh Giới Kỹ Năng Tích Hợp Thứ Ba (`integrations/`)**: 5 kỹ năng mở rộng từ bên ngoài (`integrations/aas`, `integrations/reverse-skill`, `integrations/rea`, `integrations/ui-ux-pro-max`) được quản lý trong không gian riêng biệt, không tính gộp vào 300 kỹ năng bản địa, chỉ kích hoạt khi có yêu cầu đặc thù và luôn chịu sự giám sát an ninh của Master Orchestrator.

## 6. Step-by-Step Execution Workflow
### Bước 1: Tiếp nhận, Phân loại & Xác định Phạm vi (Triage & Scoping)
1. Đọc và phân tích yêu cầu của người dùng, xác định mục tiêu và phạm vi ảnh hưởng (Scope Boundary).
2. Phân loại yêu cầu vào một hoặc nhiều miền kỹ thuật trong 30 nhóm (Groups A đến AD).
3. Đánh giá mức độ rủi ro (Risk Profile) của thay đổi đối với người dùng, dữ liệu và bảo mật.

### Bước 2: Lựa chọn Chế độ Thực thi (Execution Mode)
- **QUICK MODE** (Rủi ro thấp):
  - *Áp dụng*: Sửa lỗi chính tả, chỉnh sửa UI text nhỏ, cập nhật tài liệu hoặc cấu hình đơn giản.
  - *Chu trình*: Analyze → Implement → Verify → Report.
- **STANDARD MODE** (Rủi ro trung bình):
  - *Áp dụng*: Phát triển tính năng mới tiêu chuẩn, tái cấu trúc module vừa, nâng cấp dependencies, viết CLI tool.
  - *Chu trình*: Analyze → Specify → Plan → Implement → Test → Review → Report.
- **STRICT MODE** (Rủi ro cao / Bắt buộc kiểm soát gắt gao):
  - *Áp dụng*: Kiến trúc cốt lõi, Database migration, phân quyền/bảo mật, Cloud IaC, AI agents có tool call, SOC 2 compliance, ORR, Reverse Engineering, Game physics, Multi-tenant RAG.
  - *Chu trình*: Specification → Impact Analysis → Security and Risk Review → Implementation → Regression Tests → Approval → Release.

### Bước 3: Định tuyến Kỹ năng Chuyên biệt Tối thiểu (Skill Routing)
Master Orchestrator tra cứu bảng ma trận định tuyến (`ROUTING_MATRIX.md`) và kích hoạt tổ hợp kỹ năng phù hợp:
- **UI/UX Design Intelligence & Interface Engineering**: `dex-ui-ux-pro-max-adapter` (tra cứu phong cách UI, màu sắc, font chữ từ UI/UX Pro Max tại `integrations/ui-ux-pro-max`) → `dex-design-system-tokens` → `dex-design-brief-synthesis` → `dex-visual-hierarchy-audit` → `dex-color-contrast-systems` → `dex-ui-visual-qa-review`. (*Chặn kích hoạt trên các tác vụ backend, database hoặc DevOps*).
- **Advanced Web Experiences & Streaming**: `dex-web-animation-performance` → `dex-progressive-web-apps` → `dex-hls-dash-playback` → `dex-virtualized-infinite-lists`.
- **Browser Extensions & Automation**: `dex-browser-extension-mv3` → `dex-extension-message-security` → `dex-browser-automation-testing` → `dex-headless-ui-verification`.
- **Authorized Reverse Engineering**: `dex-pe-elf-structure-inspection` → `dex-native-symbol-mapping` → `dex-disassembly-cfg-reconstruction` → `dex-reverse-evidence-chain`.
- **Protocols & Service Integration**: `dex-mqtt-client-reliability` → `dex-websocket-session-recovery` → `dex-stream-processing-semantics` → `dex-webhook-signature-validation`.
- **Autonomous Agent Operations**: `dex-llm-evaluation-dataset-design` → `dex-agent-task-planning-validation` → `dex-llm-human-review-gates` → `dex-retrieval-permission-filtering` → `dex-mcp-client-integration`.
- **Advanced Data & Analytics**: `dex-sql-metric-semantic-layer` → `dex-time-series-diagnostics` → `dex-data-anomaly-detection` → `dex-data-warehouse-cost-tuning`.
- **Native, Graphics & Game Engineering**: `dex-chess-engine-search-testing` → `dex-simulation-determinism` → `dex-game-loop-timing` → `dex-gpu-shader-profiling`.
- **Software Trust & Distribution**: `dex-open-source-license-scanning` → `dex-artifact-signature-verification` → `dex-code-signing-release-process` → `dex-release-reproducibility-audit`.
- **Advanced SkillOps Governance**: `dex-skill-catalog-taxonomy` → `dex-skill-source-integrity` → `dex-skill-routing-conflict-tests` → `dex-skill-execution-evidence-ledger`.

### Bước 4: Kiểm soát Chuyển Giai đoạn qua 15 Quality Gates (QG-01 đến QG-15)
Tại mỗi bước thực thi, Master Orchestrator kiểm tra các cổng chất lượng bắt buộc:
- Nếu bất kỳ cổng nào chưa đạt: **DỪNG LẠI (BLOCK)**, yêu cầu khắc phục triệt để trước khi tiếp tục.
- Không cho phép bỏ qua cổng chất lượng bằng giả định hoặc báo cáo giả mạo.

### Bước 5: Báo cáo Kiểm chứng Minh bạch (Final Audit Synthesis)
Tổng hợp kết quả sau khi hoàn thành toàn bộ chuỗi công việc:
1. Tóm tắt các thay đổi đã thực hiện và tệp mã nguồn tương ứng.
2. Trạng thái chi tiết 15 Quality Gates (PASS / FAIL / SKIP / NOT VERIFIED).
3. Bằng chứng thực nghiệm (Terminal outputs, kết quả chạy test, log đo lường).
4. Khuyến nghị và hướng dẫn nghiệm thu cho người dùng.

## 7. Concrete Examples
```bash
# Lệnh kiểm tra tính toàn vẹn của toàn bộ 301 Native DEX Skills và 5 Integrations
python scripts/validate_skills.py

# Lệnh kiểm thử toàn diện test suite
pytest tests/ -v
```

## 8. Anti-Patterns & Common Traps
- **Trap 1 (Over-Activation)**: Kích hoạt hàng chục kỹ năng cùng một lúc cho một nhiệm vụ nhỏ gây lãng phí context và phân tán sự tập trung.
- **Trap 2 (Bypass Gates)**: Tự ý chuyển từ chế độ STRICT xuống QUICK chỉ để né tránh các bài kiểm thử bắt buộc.
- **Trap 3 (Hallucinated Results)**: Tự nhận định trạng thái PASS mà không thực sự chạy lệnh kiểm chứng trong môi trường thực tế.
- **Trap 4 (Catalog Inflation)**: Đếm gộp các kỹ năng bên thứ ba vào danh mục 300 kỹ năng bản địa của DEX.

## 9. Quality Gates & Acceptance Criteria
Master Orchestrator kiểm soát nghiêm ngặt 15 cổng chất lượng:
- **QG-01 (Scope & Acceptance Defined)**: Phạm vi và tiêu chuẩn nghiệm thu được xác định rõ ràng, không sửa đổi ngoài phạm vi.
- **QG-02 (Unique Identification)**: Không trùng lặp định danh giữa 301 DEX skills và third-party plugins.
- **QG-03 (Metadata Conformance)**: File `SKILL.md` có YAML frontmatter hợp lệ theo chuẩn Agent Skills Specification.
- **QG-04 (Distinct Responsibilities)**: Mỗi kỹ năng có ranh giới trách nhiệm riêng biệt, không chồng chéo chức năng.
- **QG-05 (Dependencies & References)**: Mọi liên kết tài liệu, tệp tin và scripts đều hợp lệ, không bị broken link.
- **QG-06 (Script Security)**: Mọi script thực thi được rà soát không chứa lệnh hủy diệt hay mã độc.
- **QG-07 (License & Provenance)**: Mọi nội dung bên thứ ba đều có ghi chú nguồn gốc và giấy phép rõ ràng.
- **QG-08 (Routing Validity)**: Định tuyến chính xác tới các kỹ năng khả dụng trong danh mục 300 skills.
- **QG-09 (Permissions Enforced)**: Quyền hạn được kiểm soát ở mức tối thiểu (Least Privilege).
- **QG-10 (Safe Import & Rollback)**: Có cơ chế phục hồi và rollback rõ ràng cho mọi hành động rủi ro.
- **QG-11 (Execution Scenarios Evaluated)**: Các kịch bản thực thi đại diện được đánh giá thực nghiệm.
- **QG-12 (Documentation Agreement)**: Tài liệu mô tả hoàn toàn khớp với mã nguồn thực tế.
- **QG-13 (Git Diff Cleanliness)**: Git diff sạch sẽ, commit tuân thủ quy ước, không có file thừa.
- **QG-14 (Regression Tests Passing)**: Toàn bộ bài kiểm thử tự động đạt 100% PASS trên môi trường mục tiêu.
- **QG-15 (Evidence-Based Completion)**: Mọi tuyên bố hoàn thành đều có log terminal hoặc báo cáo thực chứng.

## 10. Security & Safety Boundaries
- **Không phá vỡ an toàn Git**: Tuyệt đối không tự ý chạy `git push --force` hay `git reset --hard` trên các nhánh công khai.
- **Bảo mật thông tin xác thực**: Không bao giờ ghi lại API token, private key hoặc dữ liệu định danh người dùng vào logs hoặc artifacts.
- **Cách ly môi trường Production**: Mọi tác vụ có khả năng gây gián đoạn phải có cơ chế xác nhận tương tác và rollback tức thì.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn qua định dạng `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường IDE & CLI**: Hoạt động trơn tru trên VS Code, Cursor, Windsurf, PowerShell và POSIX terminals.

## 12. Deliverables & Output Artifacts
1. Bản phân loại nhiệm vụ, đánh giá rủi ro và chế độ thực thi (`QUICK`, `STANDARD`, `STRICT`).
2. Kế hoạch định tuyến chuỗi kỹ năng chuyên biệt trong 300 skills.
3. Bảng theo dõi 15 Quality Gates trong suốt chu trình thực hiện.
4. Báo cáo nghiệm thu kết thúc tác vụ kèm bằng chứng thực nghiệm rõ ràng.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Cội nguồn điều phối trung tâm.
- Toàn bộ 300 kỹ năng chuyên môn từ `dex-development-workflow` (01) đến `dex-skill-retirement-governance` (300).
- Các adapter mở rộng bên thứ ba trong thư mục `integrations/`.

## 14. Realistic Usage Example
### Tình huống thực tế:
Người dùng gửi yêu cầu: *"Xây dựng hệ thống giao dịch thời gian thực với phân tích đồ họa game loop, bảo vệ bằng mã hóa chữ ký số artifact và kiểm toán cấu trúc nhị phân pe/elf."*
1. **Phân tích (Analyze)**: Master Orchestrator nhận diện đây là tác vụ phức tạp liên quan đến Protocols (Group Y), Game Engineering (Group AB), Trust & Distribution (Group AC), và Reverse Engineering (Group X).
2. **Chọn chế độ (Mode)**: Chọn **STRICT MODE** do có thay đổi về giao thức tài chính, nhị phân và chữ ký bảo mật.
3. **Định tuyến (Routing)**: Kích hoạt chuỗi kỹ năng: `dex-websocket-session-recovery` → `dex-game-loop-timing` → `dex-artifact-signature-verification` → `dex-pe-elf-structure-inspection` → `dex-reverse-evidence-chain`.
4. **Kiểm soát (Gates)**: Kiểm tra tuần tự từ QG-01 đến QG-15 tại từng mốc chuyển giao.
5. **Nghiệm thu (Delivery)**: Tổng hợp báo cáo kiểm thử socket, kết quả đo lường nhịp độ khung hình, chữ ký số Cosign và biên bản chuỗi bằng chứng pháp lý với tỷ lệ lỗi 0%.
