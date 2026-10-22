---
name: dex-master-orchestrator
description: Master control plane to analyze engineering requests, select execution modes (QUICK, STANDARD, STRICT), coordinate across 120 specialized DEX skills (Groups A to L) and third-party integrations, enforce 12 Quality Gates, and generate evidence-based audit reports. Use whenever starting any software engineering workflow.
---

# DEX Master Orchestrator

## 1. Purpose & Scope
Điều phối toàn bộ vòng đời phát triển, vận hành và hiện đại hóa phần mềm theo chuẩn **DEX Engineering Skills Pack v4.0**. Master Orchestrator đóng vai trò là bộ não điều khiển trung tâm (Root Control Plane) chịu trách nhiệm: phân tích sâu yêu cầu của kỹ sư, phân loại độ phức tạp và rủi ro tác vụ, lựa chọn chế độ thực thi thông minh (`QUICK`, `STANDARD`, hoặc `STRICT`), tra cứu danh mục **120 Specialized DEX Skills** (chia đều trong 12 nhóm chuyên môn A–L) cùng các bộ chuyển đổi tích hợp bên thứ ba (`integrations/`), kích hoạt tập kỹ năng tối thiểu cần thiết, kiểm soát nghiêm ngặt **12 Quality Gates (QG-01 đến QG-12)** và tổng hợp báo cáo nghiệm thu kèm bằng chứng thực thi minh bạch.

Triết lý cốt lõi v4.0:
`Analyze → Specify → Plan → Implement → Verify → Debug → Stabilize → Review → Commit → Release → Maintain → Operate`

## 2. When to Use
- Bắt đầu bất kỳ tác vụ kỹ thuật phần mềm mới nào từ người dùng hoặc hệ thống CI/CD.
- Khi cần xác định chính xác lộ trình kỹ thuật cho các bài toán phức tạp, liên nhóm (ví dụ: Cloud migration, Mobile offline-first architecture, SOC 2 compliance, Zero-downtime rollout).
- Khi tác vụ đòi hỏi sự phối hợp tuần tự hoặc song song giữa nhiều kỹ năng chuyên biệt trong 120 skills.
- Khi cần kiểm soát rủi ro, bảo vệ branch Git và đảm bảo không có bất kỳ bước kiểm tra an ninh hay chất lượng nào bị AI bỏ qua.

## 3. When NOT to Use
- Trả lời các câu hỏi lý thuyết hoặc tra cứu định nghĩa đơn giản không làm thay đổi mã nguồn.
- Khi người dùng đã chỉ định tường minh một kỹ năng chuyên biệt duy nhất và không yêu cầu điều phối đa bước (ví dụ: `dex-security-audit` trên một file cụ thể).
- Khi đang ở giữa một tiến trình con do một chuyên môn khác đang trực tiếp xử lý (tránh can thiệp lặp vòng).

## 4. Prerequisites & Input Context
- **Yêu cầu của người dùng**: Mục tiêu nghiệp vụ, mô tả lỗi, yêu cầu kiến trúc hoặc kế hoạch phát hành.
- **Ngữ cảnh dự án**: `README.md`, `ARCHITECTURE.md`, `ROUTING_MATRIX.md`, `SKILLS_INDEX.md`, `CHANGELOG.md`.
- **Trạng thái kho mã nguồn**: Trạng thái Git (`git status`, commit hash, branch bảo vệ).
- **Môi trường kỹ thuật**: Windows 11, Linux, macOS, runtime (Node.js, Python, Go, Rust, Java, Swift, Kotlin), container và cloud providers.

## 5. Core Concepts & Taxonomy
- **Nguyên lý Điều phối Tối thiểu (Principle of Minimal Necessary Skills)**: Không bao giờ nạp toàn bộ 120 kỹ năng vào cùng một phiên làm việc; chỉ chọn lọc chính xác các kỹ năng cốt lõi (Primary) và bổ trợ (Complementary) cho nhiệm vụ hiện tại.
- **Tính Xác định & Minh Bạch (Determinism & Auditability)**: Mọi quyết định lựa chọn kỹ năng và đánh giá chất lượng phải dựa trên bằng chứng kỹ thuật khách quan, có thể tái lập được.
- **Phân Cấp Danh Mục 12 Nhóm Kỹ Năng Chuyên Môn (Groups A to L)**:
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
- **Ranh Giới Kỹ Năng Tích Hợp Thứ Ba (`integrations/`)**: Các kỹ năng mở rộng từ bên ngoài (`integrations/aas`, `integrations/reverse-skill`, `integrations/rea`) được quản lý trong không gian riêng biệt, chỉ được kích hoạt khi có yêu cầu đặc thù và luôn chịu sự giám sát của Master Orchestrator.

## 6. Step-by-Step Execution Workflow
### Bước 1: Tiếp nhận, Phân loại & Xác định Phạm vi (Triage & Scoping)
1. Đọc và phân tích yêu cầu của người dùng, xác định mục tiêu và phạm vi ảnh hưởng (Scope Boundary).
2. Phân loại yêu cầu vào một trong 12 miền kỹ thuật (Groups A đến L).
3. Đánh giá mức độ rủi ro (Risk Profile) của thay đổi đối với người dùng, dữ liệu và bảo mật.

### Bước 2: Lựa chọn Chế độ Thực thi (Execution Mode)
- **QUICK MODE** (Rủi ro thấp):
  - *Áp dụng*: Sửa lỗi chính tả, chỉnh sửa UI text nhỏ, cập nhật tài liệu hoặc cấu hình đơn giản.
  - *Chu trình*: Analyze → Implement → Verify → Report.
- **STANDARD MODE** (Rủi ro trung bình):
  - *Áp dụng*: Phát triển tính năng mới tiêu chuẩn, tái cấu trúc module vừa, nâng cấp dependencies, viết CLI tool.
  - *Chu trình*: Analyze → Plan → Implement → Test → Review → Report.
- **STRICT MODE** (Rủi ro cao / Bắt buộc kiểm soát gắt gao):
  - *Áp dụng*: Kiến trúc cốt lõi, Database schema migration, phân quyền/bảo mật, Cloud IaC, Mobile release, SOC 2 compliance, ORR.
  - *Chu trình*: Specification → Impact Analysis → Risk Assessment → Plan → Implement → Verification → Security Audit → 12 Quality Gates → Approval → Commit.

### Bước 3: Định tuyến Kỹ năng Chuyên biệt Tối thiểu (Skill Routing)
Master Orchestrator tra cứu bảng ma trận định tuyến (`ROUTING_MATRIX.md`) và kích hoạt tổ hợp kỹ năng phù hợp:
- **Cloud & Kubernetes Migration**: `dex-infrastructure-as-code` → `dex-container-image-engineering` → `dex-kubernetes-deployment` → `dex-zero-downtime-rollouts` → `dex-slo-error-budgets`.
- **Mobile Offline-First Feature**: `dex-mobile-offline-sync` → `dex-android-app-architecture` / `dex-ios-app-architecture` → `dex-native-device-integration` → `dex-mobile-performance-profiling`.
- **Desktop Application Hardening**: `dex-electron-security` / `dex-tauri-desktop-integration` → `dex-desktop-ipc-design` → `dex-desktop-update-delivery`.
- **Production Incident & Reliability**: `dex-network-troubleshooting` → `dex-distributed-tracing` → `dex-runbook-automation` → `dex-incident-postmortems`.
- **Product Launch & Compliance**: `dex-privacy-impact-assessment` → `dex-compliance-control-mapping` → `dex-analytics-instrumentation` → `dex-operational-readiness-review`.

### Bước 4: Kiểm soát Chuyển Giai đoạn qua 12 Quality Gates (QG-01 đến QG-12)
Tại mỗi bước thực thi, Master Orchestrator kiểm tra các cổng chất lượng bắt buộc.
- Nếu bất kỳ cổng nào chưa đạt: **DỪNG LẠI (BLOCK)**, yêu cầu khắc phục triệt để trước khi tiếp tục.
- Không cho phép bỏ qua cổng chất lượng bằng giả định hoặc báo cáo giả mạo.

### Bước 5: Báo cáo Kiểm chứng Minh bạch (Final Audit Synthesis)
Tổng hợp kết quả sau khi hoàn thành toàn bộ chuỗi công việc:
1. Tóm tắt các thay đổi đã thực hiện và tệp mã nguồn tương ứng.
2. Trạng thái chi tiết 12 Quality Gates (PASS / FAIL / SKIP).
3. Bằng chứng thực nghiệm (Terminal outputs, kết quả chạy test, log đo lường).
4. Khuyến nghị và hướng dẫn nghiệm thu cho người dùng.

## 7. Concrete Examples
```bash
# Lệnh kiểm tra tính toàn vẹn của toàn bộ 121 DEX Skills
python scripts/validate_skills.py

# Lệnh kiểm thử toàn diện test suite
pytest tests/ -v
```

## 8. Anti-Patterns & Common Traps
- **Trap 1 (Over-Activation)**: Kích hoạt hàng chục kỹ năng cùng một lúc cho một nhiệm vụ nhỏ gây lãng phí context và phân tán sự tập trung.
- **Trap 2 (Bypass Gates)**: Tự ý chuyển từ chế độ STRICT xuống QUICK chỉ để né tránh các bài kiểm thử bắt buộc.
- **Trap 3 (Hallucinated Results)**: Tự nhận định trạng thái PASS mà không thực sự chạy lệnh kiểm chứng trong môi trường thực tế.

## 9. Quality Gates & Acceptance Criteria
Master Orchestrator kiểm soát nghiêm ngặt 12 cổng chất lượng:
- **QG-01 (Scope Control)**: Phạm vi thay đổi được xác định rõ ràng, không sửa đổi ngoài phạm vi.
- **QG-02 (Acceptance Criteria)**: Đáp ứng đầy đủ các tiêu chí nghiệm thu đã thỏa thuận.
- **QG-03 (Metadata & Frontmatter)**: File `SKILL.md` có YAML frontmatter hợp lệ và tên khớp thư mục.
- **QG-04 (Unique Identification)**: Không trùng lặp định danh giữa 121 DEX skills và third-party plugins.
- **QG-05 (Distinct Responsibility)**: Mỗi kỹ năng có ranh giới trách nhiệm riêng biệt, không chồng chéo vô nghĩa.
- **QG-06 (Reference Integrity)**: Mọi liên kết tài liệu, tệp tin và scripts đều hợp lệ, không bị broken link.
- **QG-07 (Security & Safety)**: Không có hardcoded secrets, tuân thủ nguyên tắc đặc quyền tối thiểu.
- **QG-08 (License & Attribution)**: Mọi nội dung bên thứ ba đều có ghi chú nguồn gốc và giấy phép rõ ràng.
- **QG-09 (Safe Import & Rollback)**: Có cơ chế phục hồi và rollback rõ ràng cho mọi hành động rủi ro.
- **QG-10 (Routing Validity)**: Định tuyến chính xác tới các kỹ năng khả dụng trong danh mục.
- **QG-11 (Executable Verification)**: Toàn bộ bài kiểm thử tự động đạt 100% PASS trên môi trường mục tiêu.
- **QG-12 (Git Hygiene & Review)**: Git diff sạch sẽ, commit tuân thủ quy ước Conventional Commits.

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
2. Kế hoạch định tuyến chuỗi kỹ năng chuyên biệt.
3. Bảng theo dõi 12 Quality Gates trong suốt chu trình thực hiện.
4. Báo cáo nghiệm thu kết thúc tác vụ kèm bằng chứng thực nghiệm rõ ràng.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Cội nguồn điều phối trung tâm.
- Toàn bộ 120 kỹ năng chuyên môn từ `dex-development-workflow` (01) đến `dex-operational-readiness-review` (120).
- Các adapter mở rộng bên thứ ba trong thư mục `integrations/`.

## 14. Realistic Usage Example
### Tình huống thực tế:
Người dùng gửi yêu cầu: *"Xây dựng tính năng đồng bộ dữ liệu ngoại tuyến (Offline Sync) cho ứng dụng di động Android và triển khai backend API lên cụm Kubernetes với zero-downtime rolling update."*
1. **Phân tích (Analyze)**: Master Orchestrator nhận diện đây là tác vụ phức tạp liên quan đến Mobile (Group K), Backend (Group E) và Cloud (Group J).
2. **Chọn chế độ (Mode)**: Chọn **STRICT MODE** do có thay đổi về kiến trúc dữ liệu và triển khai hạ tầng.
3. **Định tuyến (Routing)**: Kích hoạt chuỗi kỹ năng: `dex-specification-driven` → `dex-mobile-offline-sync` → `dex-android-app-architecture` → `dex-kubernetes-deployment` → `dex-zero-downtime-rollouts` → `dex-slo-error-budgets`.
4. **Kiểm soát (Gates)**: Kiểm tra tuần tự từ QG-01 đến QG-12 tại từng mốc chuyển giao.
5. **Nghiệm thu (Delivery)**: Tổng hợp báo cáo kiểm thử unit test, build kết quả và xác nhận rollout thành công với tỷ lệ lỗi 0%.
