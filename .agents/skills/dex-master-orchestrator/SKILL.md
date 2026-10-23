---
name: dex-master-orchestrator
description: Master control plane to analyze engineering requests, select execution modes (QUICK, STANDARD, STRICT), coordinate across 400 specialized DEX skills (Groups A to AN) and segregated integrations, drive the Polyglot Script Engine across 11 languages, enforce 15 Quality Gates, and generate evidence-based audit reports. Use whenever starting any software engineering workflow.
---

# DEX Master Orchestrator

## 1. Purpose & Scope
Điều phối toàn bộ vòng đời phát triển, vận hành, bảo mật, tự động hóa đa ngôn ngữ và hiện đại hóa phần mềm theo chuẩn **DEX Engineering Skills Framework v8.0**. Master Orchestrator đóng vai trò là bộ não điều khiển trung tâm (Root Control Plane) chịu trách nhiệm:
1. Phân tích sâu sắc ý định và yêu cầu kỹ thuật của kỹ sư, phân loại miền kỹ nghệ và đánh giá rủi ro tác vụ.
2. Lựa chọn chế độ thực thi tối ưu (`QUICK`, `STANDARD`, hoặc `STRICT`).
3. Tra cứu danh mục **400 Specialized DEX Skills** (chia đều trong 40 nhóm chuyên môn chuẩn tắc A–AN, từ index 001 đến 400) cùng 5 bộ tích hợp bên thứ ba cách ly (`integrations/`).
4. Kích hoạt tập kỹ năng tối thiểu cần thiết theo nguyên lý công bố tiệm tiến (Progressive Disclosure) và định tuyến 2 tầng (Group-Level → Skill-Level).
5. Điều phối **DEX Polyglot Script Engine** hỗ trợ 11 ngôn ngữ lập trình (Python, TypeScript, JavaScript, PowerShell, Bash, Rust, Go, C++, C#, Java, PHP) qua CLI `dex.py` và các wrapper bản địa (`dex.ps1`, `dex.bat`, `dex.sh`).
6. Kiểm soát nghiêm ngặt **15 Quality Gates (QG-01 đến QG-15)** và tổng hợp báo cáo nghiệm thu kèm bằng chứng thực thi minh bạch.

Triết lý cốt lõi v8.0:
`DISCOVER → AUDIT → SPECIFY → PLAN → BUILD → REVIEW → INTEGRATE → VALIDATE → DEBUG → STABILIZE → COMMIT → RELEASE → MAINTAIN`

## 2. When to Use
- Bắt đầu bất kỳ tác vụ kỹ thuật phần mềm mới nào từ người dùng, agent phụ trợ hoặc hệ thống CI/CD.
- Khi cần xác định chính xác lộ trình kỹ thuật cho các bài toán phức tạp, liên nhóm (ví dụ: Enterprise Architecture, Distributed Systems Deep Engineering, Applied AI Systems, Extended Polyglot Engineering, Advanced UI/UX, Authorized Software Inspection, ML Platforms, Developer Platforms, Advanced Security & Trust, SkillOps Quality & Governance).
- Khi tác vụ đòi hỏi sự phối hợp tuần tự hoặc song song giữa nhiều kỹ năng chuyên biệt trong 400 skills.
- Khi cần kiểm soát rủi ro, bảo vệ branch Git và đảm bảo không có bất kỳ bước kiểm tra an ninh hay chất lượng nào bị bỏ qua.
- Khi cần biên dịch, lint, typecheck, kiểm thử hoặc benchmark các dự án đa ngôn ngữ thông qua Polyglot Engine.

## 3. When NOT to Use
- Trả lời các câu hỏi lý thuyết hoặc tra cứu định nghĩa đơn giản không làm thay đổi mã nguồn hay trạng thái hệ thống.
- Khi người dùng đã chỉ định tường minh một kỹ năng chuyên biệt duy nhất và không yêu cầu điều phối đa bước (ví dụ: `dex-secretless-cicd-oidc` trên một workflow cụ thể).
- Khi đang ở giữa một tiến trình con do một chuyên môn khác đang trực tiếp xử lý (tránh can thiệp lặp vòng).

## 4. Prerequisites & Input Context
- **Yêu cầu của người dùng**: Mục tiêu nghiệp vụ, mô tả lỗi, yêu cầu kiến trúc hoặc kế hoạch phát hành.
- **Ngữ cảnh dự án**: `README.md`, `ARCHITECTURE.md`, `ROUTING_MATRIX.md`, `SKILLS_INDEX.md`, `CHANGELOG.md`, `manifests/dex-skills.json`.
- **Trạng thái kho mã nguồn**: Trạng thái Git (`git status`, commit hash, branch bảo vệ).
- **Môi trường kỹ thuật**: Windows 11, Linux, macOS, toolchains (Python, Node.js, CMake, PowerShell, và các công cụ được cài đặt cục bộ), container, cloud providers và MCP servers.

## 5. Core Concepts & Taxonomy
- **Nguyên lý Điều phối Tối thiểu (Principle of Minimal Sufficient Skills)**: Tuyệt đối không bao giờ nạp toàn bộ 400 kỹ năng vào cùng một phiên làm việc; chỉ chọn lọc chính xác các kỹ năng cốt lõi (Primary) và bổ trợ (Complementary) cho nhiệm vụ hiện tại để tránh gây nhiễu và tràn context window.
- **Tính Xác định & Minh Bạch (Determinism & Auditability)**: Mọi quyết định lựa chọn kỹ năng và đánh giá chất lượng phải dựa trên bằng chứng kỹ thuật khách quan, có thể tái lập được.
- **Phân Cấp Danh Mục 40 Nhóm Kỹ Năng Chuyên Môn Chuẩn Tắc (Groups A to AN)**:
  1. **Group A (001–010) Core Engineering**: Quy trình lập trình, ủy nhiệm, kiểm chứng, Git, tổ chức code, gỡ lỗi, tối ưu hiệu năng, bảo mật, CI/CD, phát hành.
  2. **Group B (011–020) Architecture & AI Agents**: Giám sát production, nợ kỹ thuật, kiến trúc, database, API, kiểm thử, agent engineering, multi-agent, context, đặc tả.
  3. **Group C (021–030) Production Engineering**: Phân tích tác động, phụ thuộc, độ tin cậy, tương tranh, khả năng tiếp cận, feature flags, code review, acceptance, bảo trì, E2E.
  4. **Group D (031–040) Frontend Engineering**: Hợp đồng UI, Design tokens, luồng dữ liệu frontend, biểu mẫu, định tuyến, hiệu năng web, SSR/SEO, đa ngôn ngữ, visual regression, tương thích trình duyệt.
  5. **Group E (041–050) Backend & Integration**: DDD, hàng đợi tác vụ ngầm, chiến lược cache, giao thức thời gian thực, xử lý file, search, event-driven, thao tác idempotent, thông báo, tác vụ định kỳ.
  6. **Group F (051–060) Data Engineering**: Hợp đồng dữ liệu, data pipeline, kiểm toán chất lượng dữ liệu, data lineage, tiến hóa schema, tối ưu query plan, vòng đời lưu trữ, lưu giữ dữ liệu, hoạch định dung lượng, phục hồi thảm họa.
  7. **Group G (061–070) AI & LLM Engineering**: Tích hợp LLM, pipeline RAG, đánh giá retrieval, đánh giá prompt, đánh giá model, hợp đồng tool calling, phân quyền agent, kiểm soát chi phí token, quan sát AI, quản trị dataset.
  8. **Group H (071–080) Developer Experience**: Bootstrap repository, quản trị monorepo, kỹ thuật CLI, kiến trúc plugin, đa nền tảng, đóng gói Windows, tài liệu dạng code, sinh code, công cụ lập trình viên, tự động hóa semver.
  9. **Group I (081–090) Security & Reliability**: Vòng đời phiên xác thực, phân quyền đa người thuê, quản trị bí mật, an toàn chuỗi cung ứng, mô hình hóa mối đe dọa, kiểm thử thuộc tính, thử nghiệm hỗn loạn, chỉ số thử nghiệm, tiến hóa hợp đồng API, postmortem sự cố.
  10. **Group J (091–100) Cloud & Infrastructure**: Đóng gói container tối ưu, triển khai Kubernetes, IaC Terraform, tích hợp dịch vụ cloud qua Workload Identity, triển khai zero-downtime Canary, mạng Service Mesh, chẩn đoán mạng phân tán, SLO & ngân sách lỗi, truy vết phân tán OpenTelemetry, FinOps tối ưu chi phí cloud.
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
  24. **Group X (231–240) Authorized Reverse Engineering**: PE/ELF structure inspection, native symbol mapping, disassembly CFG reconstruction, managed assembly inspection, Electron artifact analysis, JavaScript sourcemap recovery, mobile package static audit, firmware metadata inspection, binary diff regression, reverse evidence chain.
  25. **Group Y (241–250) Protocols & Service Integration**: MQTT client reliability, WebSocket session recovery, stream processing semantics, event schema registry, HTTP client connection pooling, OAuth/OIDC integration, webhook signature validation, API pagination cursors, service contract simulation, offline message delivery.
  26. **Group Z (251–260) AI Agent Operations**: LLM evaluation dataset design, agent task planning validation, agent trace replay, LLM human review gates, retrieval permission filtering, multimodal evaluation, AI safety red-teaming, agent long-running task checkpoints, MCP client integration, inference latency optimization.
  27. **Group AA (261–270) Advanced Data & Analytics**: SQL metric semantic layer, time-series diagnostics, data anomaly detection, feature store engineering, analytics cohort retention, A/B test statistical analysis, geospatial data pipelines, data warehouse cost tuning, backfill reconciliation, machine learning data drift.
  28. **Group AB (271–280) Native, Graphics & Game Engineering**: Chess engine search testing, simulation determinism, physics engine validation, game loop timing, rendering frame pacing, GPU shader profiling, GPU resource lifetime, native plugin ABI testing, real-time input latency, asset pipeline optimization.
  29. **Group AC (281–290) Software Trust & Distribution**: Open-source license scanning, third-party attribution, artifact signature verification, dependency vulnerability intelligence, secret rotation drills, code signing release process, software update trust chains, vulnerability disclosure workflows, maintainer contribution governance, release reproducibility audit.
  30. **Group AD (291–300) Advanced SkillOps Governance**: Skill catalog taxonomy, skill source integrity, skill risk scoring, skill reference graph, skill routing conflict tests, skill execution evidence ledger, skill documentation drift, skill upgrade migrations, skill rollback verification, skill retirement governance.
  31. **Group AE (301–310) Enterprise Software Architecture**: ADR architecture decision records, modular monolith boundaries, saga compensation workflows, CQRS projection management, multi-region data residency, tenant provisioning lifecycle, legacy strangler migration, public API deprecation, configuration schema design, contract-first development.
  32. **Group AF (311–320) Distributed Systems Deep Engineering**: Exactly-once delivery claims audit, message poison queue recovery, distributed lock lease safety, scheduler misfire recovery, regional outage exercises, partition fault simulation, event replay safety, consumer lag control, hot partition mitigation, clock skew resilience.
  33. **Group AG (321–330) Applied AI Systems**: Embedding data preparation, hybrid search fusion (RRF), RAG freshness control, context window budgeting, agent tool output sanitization, model output calibration, AI feedback labeling, prompt version experiments, inference provider rate controls, human-AI workflow design.
  34. **Group AH (331–340) Extended Polyglot Engineering**: Kotlin Multiplatform builds, Swift concurrency review, Dart/Flutter state debugging, Ruby Gem engineering, PHP framework hardening, Scala effect systems, Elixir OTP supervision, Zig build engineering, Lua embedding safety, shell portability testing.
  35. **Group AI (341–350) Advanced UI/UX Engineering**: Design token migration (W3C DTCG), component state matrices, typography scale localization, high-density dashboard layouts, gesture interaction accessibility (WCAG 2.5), RTL/BiDi layout readiness, animation storyboard specs, chart visualization accessibility, perceived performance patterns, cross-platform UI parity.
  36. **Group AJ (351–360) Authorized Software Inspection**: Binary provenance matching (SLSA), debug symbols correlation (PDB/DWARF), toolchain reproducibility audit, installer package static review (MSI/PKG), SBOM binary correlation, mobile permission surface diffing, JS bundle obfuscation audits, macOS entitlements review, firmware image structure diffing, reverse engineering reporting.
  37. **Group AK (361–370) ML Platform & Data Systems**: Online-offline feature parity, training data leakage audits, model serving canary rollouts, ML experiment reproducibility (DVC), data label quality assessment (Cleanlab), batch inference pipeline tuning, vector embedding migration, real-time analytics windowing, metadata catalog lineage, data masking and synthetic generation.
  38. **Group AL (371–380) Developer Platform & Polyglot Tooling**: Developer workstation bootstrap, toolchain version pinning (mise), polyglot build orchestration, build cache integrity, cross-language contract tests (Pact), reproducible devcontainers, CLI command contracts, Windows/Linux path compatibility, package publishing preflight, monorepo template conformance.
  39. **Group AM (381–390) Advanced Security & Trust**: Secretless CI/CD authentication (OIDC), ephemeral test credentials (Vault), container runtime isolation (gVisor/Kata), API authorization matrix tests (BOLA/BOPLA), privacy-safe observability, DNS/TLS certificate monitoring, incident evidence preservation (Forensics/WORM), SaaS risk surface reviews, dependency update risk scoring, service account lifecycle.
  40. **Group AN (391–400) SkillOps Quality & Governance**: Skill catalog reconciliation, Agent Skills spec compatibility, skill example test fixtures, instruction injection testing, runtime capability probing, semantic routing evaluations, upstream license diffing, cross-platform release matrices, skill quality scorecards, execution sandbox policies.
- **Ranh Giới Kỹ Năng Tích Hợp Thứ Ba (`integrations/`)**: 5 kỹ năng mở rộng từ bên ngoài (`integrations/agentic-awesome-skills/dex-api-mocking-virtualization`, `integrations/reverse-skill/dex-binary-inspection`, `integrations/reverse-skill/dex-javascript-bundle-deobfuscation`, `integrations/rea/dex-rea-adapter`, `integrations/ui-ux-pro-max/dex-ui-ux-pro-max-adapter`) được quản lý trong không gian riêng biệt, không tính gộp vào 400 kỹ năng bản địa, chỉ kích hoạt khi có yêu cầu đặc thù và luôn chịu sự giám sát an ninh của Master Orchestrator.
- **Quy tắc Loại trừ Backend của UI/UX Pro Max**: Chặn kích hoạt trên các tác vụ backend, database hoặc DevOps. Bộ adapter `dex-ui-ux-pro-max-adapter` phối hợp cùng `dex-design-system-tokens` và `dex-design-token-migration` CHỈ ĐƯỢC PHÉP kích hoạt cho các tác vụ thiết kế giao diện (UI style, bảng màu, typography, bố cục layout, component styling); TUYỆT ĐỐI KHÔNG kích hoạt cho các tác vụ logic backend, database migrations, CI/CD pipelines, phân tích nhị phân hoặc quản trị đám mây.

## 6. Step-by-Step Execution Workflow
### Bước 1: Tiếp nhận, Phân loại & Xác định Phạm vi (Triage & Scoping)
1. Đọc và phân tích yêu cầu của người dùng, xác định mục tiêu và phạm vi ảnh hưởng (Scope Boundary).
2. Phân loại yêu cầu vào một hoặc nhiều miền kỹ thuật trong 40 nhóm chuẩn tắc (Groups A đến AN).
3. Đánh giá mức độ rủi ro (Risk Profile) của thay đổi đối với người dùng, dữ liệu và bảo mật.

### Bước 2: Lựa chọn Chế độ Thực thi (Execution Mode)
- **QUICK MODE** (Rủi ro thấp):
  - *Áp dụng*: Sửa lỗi chính tả, chỉnh sửa UI text nhỏ, cập nhật tài liệu hoặc cấu hình đơn giản.
  - *Chu trình*: Analyze → Implement → Verify → Report.
- **STANDARD MODE** (Rủi ro trung bình):
  - *Áp dụng*: Phát triển tính năng mới tiêu chuẩn, tái cấu trúc module vừa, nâng cấp dependencies, viết CLI tool, thiết lập DevContainer.
  - *Chu trình*: Analyze → Specify → Plan → Implement → Test → Review → Report.
- **STRICT MODE** (Rủi ro cao / Bắt buộc kiểm soát gắt gao):
  - *Áp dụng*: Kiến trúc doanh nghiệp cốt lõi, Distributed sagas, Database migration, phân quyền BOLA/BOPLA, Secretless OIDC, Cloud IaC, AI agents có tool call, Phân tích nhị phân và dịch ngược, Thao tác tài chính, Phát hành package lên registry công cộng.
  - *Chu trình*: Specification → Impact Analysis → Security and Risk Review → Implementation → Regression Tests → Approval → Release.

### Bước 3: Định tuyến Kỹ năng Chuyên biệt Tối thiểu (Skill Routing)
Master Orchestrator tra cứu bảng ma trận định tuyến (`ROUTING_MATRIX.md`) theo mô hình 2 tầng (Group → Skill):
- **Enterprise Architecture**: `dex-architecture-decision-records` → `dex-modular-monolith-boundaries` → `dex-saga-compensation-workflows` → `dex-contract-first-development`.
- **Distributed Systems Deep Engineering**: `dex-exactly-once-claims-audit` → `dex-distributed-lock-lease-safety` → `dex-consumer-lag-control` → `dex-clock-skew-resilience`.
- **Applied AI Systems**: `dex-embedding-data-preparation` → `dex-hybrid-search-fusion` → `dex-agent-tool-output-sanitization` → `dex-model-output-calibration`.
- **Extended Polyglot Engineering**: `dex-kotlin-multiplatform-builds` → `dex-swift-concurrency-review` → `dex-elixir-otp-supervision` → `dex-zig-build-engineering`.
- **Advanced UI/UX Engineering**: `dex-design-token-migration` → `dex-component-state-matrix` → `dex-gesture-interaction-accessibility` → `dex-cross-platform-ui-parity`.
- **Authorized Software Inspection**: `dex-binary-provenance-matching` → `dex-debug-symbols-correlation` → `dex-installer-package-static-review` → `dex-reverse-engineering-reporting`.
- **ML Platform & Data Systems**: `dex-online-offline-feature-parity` → `dex-training-data-leakage-audit` → `dex-model-serving-canary-rollouts` → `dex-vector-embedding-migration`.
- **Developer Platform & Polyglot Tooling**: `dex-developer-workstation-bootstrap` → `dex-toolchain-version-pinning` → `dex-polyglot-build-orchestration` → `dex-cross-language-contract-tests`.
- **Advanced Security & Trust**: `dex-secretless-cicd-oidc` → `dex-ephemeral-test-credentials` → `dex-container-runtime-isolation` → `dex-api-authorization-matrix-tests`.
- **SkillOps Quality & Governance**: `dex-skill-catalog-reconciliation` → `dex-agent-skills-spec-compatibility` → `dex-instruction-injection-testing` → `dex-semantic-routing-evaluations`.

### Bước 4: Tích hợp Polyglot Script Engine
Khi tác vụ liên quan đến build, test, lint, hoặc chẩn đoán môi trường đa ngôn ngữ:
1. Gọi CLI Polyglot: `python scripts/polyglot/dex.py <command> --lang <lang>` hoặc qua wrapper `.\scripts\polyglot\wrappers\dex.ps1`.
2. Kiểm tra tính sẵn sàng của runtime bằng lệnh `doctor`.
3. Nếu runtime không có trên máy, trả về `TOOL_NOT_AVAILABLE` kèm hướng dẫn cài đặt xác thực, tuyệt đối không crash unhandled exception.
4. Đảm bảo mọi kết quả thực thi tuân thủ hợp đồng JSON schema (`result.schema.json`).

### Bước 5: Kiểm soát Chuyển Giai đoạn qua 15 Quality Gates (QG-01 đến QG-15)
Tại mỗi bước thực thi, Master Orchestrator kiểm tra các cổng chất lượng bắt buộc:
- Nếu bất kỳ cổng nào chưa đạt: **DỪNG LẠI (BLOCK)**, yêu cầu khắc phục triệt để trước khi tiếp tục.
- Không cho phép bỏ qua cổng chất lượng bằng giả định hoặc báo cáo giả mạo.

### Bước 6: Báo cáo Kiểm chứng Minh bạch (Final Audit Synthesis)
Tổng hợp kết quả sau khi hoàn thành toàn bộ chuỗi công việc:
1. Tóm tắt các thay đổi đã thực hiện và tệp mã nguồn tương ứng.
2. Trạng thái chi tiết 15 Quality Gates (PASS / FAIL / SKIP / NOT VERIFIED).
3. Bằng chứng thực nghiệm (Terminal outputs, kết quả chạy test, log đo lường).
4. Khuyến nghị và hướng dẫn nghiệm thu cho người dùng.

## 7. Concrete Examples
```bash
# Lệnh kiểm tra tính toàn vẹn của toàn bộ 401 Native DEX Skills và 5 Integrations
python scripts/validate_skills.py

# Lệnh đối soát và đồng bộ hóa danh mục kỹ năng
python scripts/discover_skills.py

# Lệnh kiểm toán toàn bộ kỹ năng và chấm điểm chất lượng
python scripts/audit_skills.py

# Lệnh đánh giá độ chính xác định tuyến 40 kịch bản
python scripts/evaluate_routing.py

# Lệnh chẩn đoán năng lực môi trường đa ngôn ngữ
python scripts/polyglot/dex.py doctor

# Lệnh kiểm thử toàn diện test suite
pytest tests/ scripts/polyglot/tests/ -v
```

## 8. Anti-Patterns & Common Traps
- **Trap 1 (Over-Activation)**: Kích hoạt hàng chục kỹ năng cùng một lúc cho một nhiệm vụ nhỏ gây lãng phí context và phân tán sự tập trung.
- **Trap 2 (Bypass Gates)**: Tự ý chuyển từ chế độ STRICT xuống QUICK chỉ để né tránh các bài kiểm thử bắt buộc.
- **Trap 3 (Hallucinated Results)**: Tự nhận định trạng thái PASS mà không thực sự chạy lệnh kiểm chứng trong môi trường thực tế.
- **Trap 4 (Catalog Inflation)**: Đếm gộp các kỹ năng bên thứ ba vào danh mục 400 kỹ năng bản địa của DEX.
- **Trap 5 (UI/UX Misrouting to Backend)**: Kích hoạt UI/UX Pro Max cho các tác vụ database, API microservices hoặc cloud infrastructure.
- **Trap 6 (Unchecked Tool Invocation)**: Chạy lệnh biên dịch cho ngôn ngữ vắng mặt trên máy chủ thay vì trả về `TOOL_NOT_AVAILABLE`.

## 9. Quality Gates & Acceptance Criteria
Master Orchestrator kiểm soát nghiêm ngặt 15 cổng chất lượng:
- **QG-01 (Scope & Acceptance Defined)**: Phạm vi và tiêu chuẩn nghiệm thu được xác định rõ ràng, không sửa đổi ngoài phạm vi.
- **QG-02 (Unique Identification)**: Không trùng lặp định danh giữa 401 DEX skills và third-party plugins.
- **QG-03 (Metadata Conformance)**: File `SKILL.md` có YAML frontmatter hợp lệ theo chuẩn Agent Skills Specification.
- **QG-04 (Distinct Responsibilities)**: Mỗi kỹ năng có ranh giới trách nhiệm riêng biệt, không chồng chéo chức năng.
- **QG-05 (Dependencies & References)**: Mọi liên kết tài liệu, tệp tin và scripts đều hợp lệ, không bị broken link.
- **QG-06 (Script Security)**: Mọi script thực thi được rà soát không chứa lệnh hủy diệt hay mã độc (shell=False, bounded output, timeout).
- **QG-07 (License & Provenance)**: Mọi nội dung bên thứ ba đều có ghi chú nguồn gốc và giấy phép rõ ràng trong `THIRD_PARTY_NOTICES.md`.
- **QG-08 (Routing Validity)**: Định tuyến chính xác tới các kỹ năng khả dụng trong danh mục 400 skills (F1 >= 0.85).
- **QG-09 (Permissions Enforced)**: Quyền hạn được kiểm soát ở mức tối thiểu (Least Privilege).
- **QG-10 (Safe Import & Rollback)**: Có cơ chế phục hồi và rollback rõ ràng cho mọi hành động rủi ro.
- **QG-11 (Execution Scenarios Evaluated)**: Các kịch bản thực thi đại diện (Scenarios A through L) được đánh giá thực nghiệm.
- **QG-12 (Documentation Agreement)**: Tài liệu mô tả hoàn toàn khớp với mã nguồn thực tế.
- **QG-13 (Git Diff Cleanliness)**: Git diff sạch sẽ, commit tuân thủ quy ước, không có file thừa.
- **QG-14 (Regression Tests Passing)**: Toàn bộ bài kiểm thử tự động đạt 100% PASS trên môi trường mục tiêu.
- **QG-15 (Evidence-Based Completion)**: Mọi tuyên bố hoàn thành đều có log terminal hoặc báo cáo thực chứng.

## 10. Security & Safety Boundaries
- **Không phá vỡ an toàn Git**: Tuyệt đối không tự ý chạy `git push --force` hay `git reset --hard` trên các nhánh công khai.
- **Bảo mật thông tin xác thực**: Không bao giờ ghi lại API token, private key hoặc dữ liệu định danh người dùng vào logs hoặc artifacts (tự động khử khuẩn qua `sanitize_secrets`).
- **Cách ly môi trường Production**: Mọi tác vụ có khả năng gây gián đoạn phải có cơ chế xác nhận tương tác và rollback tức thì.
- **Thực thi Subprocess An toàn**: Không dùng `shell=True` cho các lệnh động; giới hạn thời gian thực thi tối đa 60 giây và bộ đệm 512KB.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn qua định dạng `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Polyglot Execution Engine**: Điều phối 11 ngôn ngữ lập trình qua Python CLI và native shell wrappers.
- **Môi trường IDE & CLI**: Hoạt động trơn tru trên VS Code, Cursor, Windsurf, PowerShell và POSIX terminals.

## 12. Deliverables & Output Artifacts
1. Bản phân loại nhiệm vụ, đánh giá rủi ro và chế độ thực thi (`QUICK`, `STANDARD`, `STRICT`).
2. Kế hoạch định tuyến chuỗi kỹ năng chuyên biệt trong 400 skills.
3. Bảng theo dõi 15 Quality Gates trong suốt chu trình thực hiện.
4. Báo cáo nghiệm thu kết thúc tác vụ kèm bằng chứng thực nghiệm rõ ràng.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Cội nguồn điều phối trung tâm.
- Toàn bộ 400 kỹ năng chuyên môn từ `dex-development-workflow` (001) đến `dex-execution-sandbox-policies` (400).
- Các adapter mở rộng bên thứ ba trong thư mục `integrations/`.

## 14. Realistic Usage Example
### Tình huống thực tế:
Người dùng gửi yêu cầu: *"Xây dựng hệ thống giao dịch phân tán với quy trình saga bù trừ, bảo vệ bằng xác thực secretless OIDC CI/CD, kiểm toán bộ nhớ đệm cache và phân tích nhị phân ELF."*
1. **Phân tích (Analyze)**: Master Orchestrator nhận diện đây là tác vụ phức tạp liên quan đến Enterprise Architecture (Group AE), Advanced Security (Group AM), Developer Tooling (Group AL), và Authorized Software Inspection (Group AJ).
2. **Chọn chế độ (Mode)**: Chọn **STRICT MODE** do có thay đổi về giao dịch phân tán, xác thực đám mây và phân tích nhị phân.
3. **Định tuyến (Routing)**: Kích hoạt chuỗi kỹ năng: `dex-saga-compensation-workflows` → `dex-secretless-cicd-oidc` → `dex-build-cache-integrity` → `dex-binary-provenance-matching` → `dex-reverse-engineering-reporting`.
4. **Kiểm soát (Gates)**: Kiểm tra tuần tự từ QG-01 đến QG-15 tại từng mốc chuyển giao.
5. **Nghiệm thu (Delivery)**: Tổng hợp báo cáo kiểm thử saga compensation, cấu hình OIDC GitHub Actions, chứng thực chữ ký Cosign và biên bản chuỗi bằng chứng pháp lý với tỷ lệ lỗi 0%.
