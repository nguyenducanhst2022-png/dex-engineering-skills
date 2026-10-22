---
name: dex-ui-ux-pro-max-adapter
description: Design intelligence bridge connecting DEX AI agents to UI/UX Pro Max search engine for data-driven UI styles, color palettes, typography pairings, design system generation, and 22 framework-specific implementation guidelines. Use when designing user interfaces, redesigning web/mobile screens, or establishing design tokens.
---

# dex-ui-ux-pro-max-adapter

> **Source Attribution:** Adapted from [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) under the MIT License.  
> **Original Author:** NextLevelBuilder  
> **Upstream Repository:** `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` (Pinned Commit: `04cfb449bd8494811ad63e94172a308fa25a551a`)  
> **Mount Directory:** `integrations/ui-ux-pro-max/`  

---

## 1. Purpose & Scope
Đóng vai trò là cầu nối trí tuệ thiết kế (Design Intelligence Bridge) chính thức giữa DEX Engineering Skills Framework và công cụ tìm kiếm dữ liệu thiết kế **UI/UX Pro Max**; truy xuất các tập dữ liệu thiết kế thực nghiệm đã được chuẩn hóa (12 domain tra cứu, 22 tech stack, hàng ngàn quy tắc thiết kế giao diện) để kiến tạo hệ thống Design System chuẩn mực, gợi ý phong cách giao diện (UI Style), bảng màu (Color Palette), cặp phông chữ (Typography Pairing), bố cục đáp ứng (Responsive Layout) và quy chuẩn tiếp cận (Accessibility WCAG 2.1 AA).

Quy trình vận hành chuẩn:
`Phát hiện yêu cầu UI/UX → Gọi Search Engine thực tế → Phân tích dữ liệu thiết kế → Sinh Design Tokens chuẩn → Định hình Component Contracts → Kiểm thử Accessibility & Visual → Bàn giao UI hoàn chỉnh`

---

## 2. When to Use
Kỹ năng này được tự động kích hoạt bởi Master Orchestrator hoặc người dùng khi xuất hiện các yêu cầu:
- Thiết kế mới trang web, ứng dụng SaaS, landing page, hoặc ứng dụng di động/desktop.
- Cải thiện hoặc tái cấu trúc giao diện hiện có (Redesign dashboard, refresh UI/UX).
- Xây dựng hoặc mở rộng hệ thống thiết kế (Create/extend Design System, design tokens).
- Lựa chọn bảng màu chuyên nghiệp, cặp phông chữ Google Fonts phù hợp với ngành hàng/sản phẩm.
- Nâng cấp giao diện chế độ tối/sáng (Dark mode/Light mode theming).
- Tối ưu hóa bố cục đáp ứng (Responsive layout) và luồng trải nghiệm người dùng (UX improvements).
- Khắc phục các vi phạm tiếp cận người khuyết tật (Fix accessibility, color contrast, focus rings).
- Tra cứu hướng dẫn triển khai giao diện chuyên biệt theo tech stack (React, Next.js, Tailwind, Vue, Svelte, SwiftUI, Flutter, WinUI, v.v.).

---

## 3. When NOT to Use
- **Tác vụ Backend thuần túy**: Phát triển API REST/gRPC, xử lý cơ sở dữ liệu SQL/NoSQL, worker hàng đợi hoặc serverless function không có giao diện đồ họa.
- **Tác vụ DevOps & Hạ tầng**: Cấu hình Kubernetes, Terraform IaC, CI/CD pipeline, mạng Docker hoặc phân quyền Cloud IAM.
- **Tự ý viết lại toàn bộ giao diện đang ổn định**: Khi người dùng chỉ yêu cầu sửa đổi một nút bấm nhỏ hoặc sửa lỗi logic, không được tự ý xóa bỏ mã giao diện hiện tại để áp đặt một style hoàn toàn mới.
- **Giả lập kết quả tìm kiếm khi thiếu công cụ**: Nếu upstream runtime chưa được phát hiện, tuyệt đối không bịa đặt dữ liệu tra cứu giả mà phải thông báo trạng thái `NOT INSTALLED` kèm hướng dẫn cài đặt minh bạch.

---

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Mục tiêu sản phẩm hoặc bài toán nghiệp vụ (ví dụ: "Fintech analytics dashboard", "E-commerce checkout").
- Đối tượng người dùng mục tiêu (B2B Enterprise, Gen-Z consumers, Internal operators).
- Tech stack của dự án (Next.js, React + Tailwind, Vue 3, Svelte, SwiftUI, v.v.).
- Phong cách hoặc Design Tokens hiện có (nếu có dự án trước, bảo vệ các lựa chọn màu sắc cốt lõi của người dùng).

**Điều kiện tiên quyết:**
- Python 3.10+ khả dụng trên hệ thống.
- Runtime của UI/UX Pro Max khả dụng thông qua phát hiện tự động của `scripts/ui_ux_pro_max_runner.py` (external path hoặc local vendored runtime).

---

## 5. Core Concepts & Taxonomy
1. **Thuật toán Khớp BM25 & Semantic Search**:
   Tra cứu từ khóa đa chiều trên các tập dữ liệu CSV chuẩn hóa:
   - `styles.csv`: 60+ phong cách UI (Bento Grid, Glassmorphism, Swiss Minimalism, Neu-Brutalism, v.v.).
   - `colors.csv`: Hàng trăm bảng màu ngành nghề kèm mã HEX, CSS variables và vai trò ngữ nghĩa.
   - `typography.csv` & `google-fonts.csv`: Cặp phông chữ đề xuất kèm link import Google Fonts.
   - `ux-guidelines.csv`: Hơn 100 quy tắc công thái học và phòng tránh bẫy UX (anti-patterns).
   - `stacks/*.csv`: 22 tệp hướng dẫn tối ưu cho từng framework giao diện cụ thể.
2. **Design Dials (Bộ điều chỉnh thông số thiết kế)**:
   - `--variance (1–10)`: Tùy biến độ biến thiên bố cục (1 = tối giản đối xứng, 10 = bất đối xứng phá cách).
   - `--motion (1–10)`: Tùy biến cường độ animation (1 = tinh tế nhẹ nhàng, 10 = vũ đạo GSAP sống động).
   - `--density (1–10)`: Tùy biến mật độ thông tin (1 = thoáng đãng rộng rãi, 10 = bảng điều khiển chuyên sâu).
3. **Phân cấp Token Ngữ Nghĩa (3-Tier Design Tokens)**:
   - Global Tokens (`#2563EB`, `16px`) → Semantic Tokens (`--color-primary`, `--spacing-md`) → Component Tokens (`--button-bg`, `--card-padding`).

---

## 6. Step-by-Step Execution Workflow

### Bước 1: Kiểm Tra Trạng Thái Runtime (Runtime Health Check)
```bash
python scripts/ui_ux_pro_max_runner.py --status
```
Nếu trạng thái trả về `Installed: False`, thông báo cho người dùng hướng dẫn cài đặt và dừng quá trình tra cứu sâu.

### Bước 2: Khám Phá & Đề Xuất Hệ Thống Thiết Kế (Design System Generation)
Chạy bộ sinh Design System cho chủ đề sản phẩm:
```bash
python scripts/ui_ux_pro_max_runner.py "<product_query>" --design-system
```
Trích xuất: UI Style, Bảng màu ngữ nghĩa (Primary, Secondary, Accent, Background, Border), Cặp phông chữ Google Fonts, và Danh sách chống chỉ định (Anti-patterns).

### Bước 3: Tra Cứu Hướng Dẫn Kỹ Thuật Theo Tech Stack
```bash
python scripts/ui_ux_pro_max_runner.py "<topic>" --stack <framework> --json
```
Ví dụ: `--stack html-tailwind` hoặc `--stack nextjs`.

### Bước 4: Chuyển Giao Sang DEX Design System Tokens
Ánh xạ các biến màu và spacing thu thập được sang kỹ năng `dex-design-system-tokens` để xuất ra `tailwind.config.js` hoặc file CSS variables chuẩn W3C Design Tokens.

### Bước 5: Định Nghĩa Giao Ước Thành Phần (Component Contracts)
Sử dụng `dex-ui-component-contracts` để khai báo TypeScript props, slots và 5 trạng thái bắt buộc (Default, Hover/Active, Focus, Disabled, Loading/Skeleton).

### Bước 6: Kiểm Toán Khả Năng Tiếp Cận & Hồi Quy Trực Quan
Phối hợp cùng `dex-ux-accessibility` để kiểm tra độ tương phản màu (tối thiểu 4.5:1), hỗ trợ phím Tab, thẻ ngữ nghĩa Semantic HTML, và kiểm thử hồi quy thị giác qua `dex-visual-regression`.

---

## 7. Concrete Examples
### Ví Dụ 1: Gọi CLI runner tra cứu phong cách giao diện dạng JSON
```bash
python scripts/ui_ux_pro_max_runner.py "fintech dashboard" --domain style --json
```

### Ví Dụ 2: Sinh toàn bộ tài liệu Design System dạng Markdown
```bash
python scripts/ui_ux_pro_max_runner.py "healthcare patient portal" --design-system --format markdown
```

### Ví Dụ 3: Gọi hàm Python từ adapter script
```python
from ui_ux_pro_max_runner import search

result = search("e-commerce checkout", stack="react", json_output=True)
print(f"Matched {result.get('count', 0)} best practices for React.")
```

---

## 8. Anti-Patterns & Common Traps
- **Lạm Dụng Toàn Diện Khi Sửa Cục Bộ**: Tự ý ghi đè toàn bộ token màu của dự án khách hàng khi họ chỉ nhờ chỉnh sửa một nút bấm.
- **Ảo Giác Kết Quả Tra Cứu**: Bịa ra thông tin hex color hoặc font chữ khi search runner không phản hồi hoặc trả về mã lỗi.
- **Không Khớp Tech Stack**: Đưa mã nguồn JSX/Tailwind vào dự án đang sử dụng Svelte hoặc Flutter.
- **Bỏ Qua Tiếp Cận WCAG**: Lựa chọn màu sắc tương phản kém (dưới 4.5:1) chỉ vì cảm quan "thẩm mỹ nghệ thuật".

---

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Cây thư mục Git sạch sẽ hoặc đã stash trước khi áp dụng thay đổi mã nguồn UI.
- **QG-02**: Không có lỗi cú pháp hoặc lỗi gõ phím trong file CSS/TypeScript được sinh ra.
- **QG-03**: Bằng chứng tra cứu từ `ui_ux_pro_max_runner.py` phải là kết quả thực tế (exit code 0), không dùng dữ liệu mô phỏng.
- **QG-08**: Toàn bộ liên kết biểu tượng và file tham chiếu trong tài liệu bàn giao đều chính xác.
- **QG-14**: Đáp ứng tiêu chuẩn tiếp cận người khuyết tật WCAG 2.1 AA (độ tương phản, phím Tab, focus state rõ ràng).

---

## 10. Security & Safety Boundaries
- Kỹ năng hoạt động hoàn toàn ở chế độ đọc dữ liệu (Read-only query) trong quá trình tra cứu thông số thiết kế.
- Không tự ý thực thi các lệnh cài đặt npm/pip toàn cục khi chưa có sự chấp thuận của người dùng.
- Không gửi bất kỳ dữ liệu mã nguồn hoặc tài sản độc quyền của người dùng ra các dịch vụ AI bên ngoài; toàn bộ quá trình tìm kiếm được thực hiện 100% cục bộ (Local execution).

---

## 11. Platform Adapters
- **Windows 11 / PowerShell**: `python scripts/ui_ux_pro_max_runner.py "<query>" --json`
- **Linux / macOS Bash**: `python3 scripts/ui_ux_pro_max_runner.py "<query>" --json`
- **OpenAI Codex / VS Code**: Gọi trực tiếp CLI script từ terminal runner và tiếp nhận cấu trúc JSON hoặc Markdown.
- **Claude Code / Cursor**: Nhận diện qua file hướng dẫn tích hợp và thực thi search cục bộ.

---

## 12. Deliverables & Output Artifacts
1. **Bản Đặc Tả Design System (MASTER.md hoặc Design Brief)**:
   - Bảng màu ngữ nghĩa (Semantic Palette kèm mã HEX và biến CSS).
   - Cặp phông chữ Typography kèm mã nhúng Google Fonts.
   - Nguyên tắc Spacing, Border Radius, và Shadows.
   - Danh sách Anti-patterns cần tuyệt đối tránh.
2. **Mã Nguồn Tokens & Components**:
   - Cấu hình theme (`tailwind.config.js` hoặc file CSS `:root { ... }`).
   - Component template tuân thủ 5 trạng thái tương tác và tiêu chuẩn tiếp cận.

---

## 13. Related & Complementary Skills
- [`dex-design-system-tokens`](.agents/skills/dex-design-system-tokens/SKILL.md): Chuẩn hóa và đồng bộ hóa các biến CSS và Design Tokens W3C.
- [`dex-ui-component-contracts`](.agents/skills/dex-ui-component-contracts/SKILL.md): Định nghĩa props interface và boundaries cho component.
- [`dex-ux-accessibility`](.agents/skills/dex-ux-accessibility/SKILL.md): Đảm bảo kiểm toán WCAG 2.1 AA và điều hướng bàn phím.
- [`dex-visual-regression`](.agents/skills/dex-visual-regression/SKILL.md): Chụp pixel snapshot bảo vệ giao diện khỏi sai lệch bố cục.
- [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md): Đo lường Core Web Vitals và tối ưu bundle frontend.

---

## 14. Realistic Usage Example

### Kịch Bản: Thiết Kế Bảng Điều Khiển Tài Chính (Fintech Analytics Dashboard)

#### Đầu vào từ người dùng:
*"Tôi cần thiết kế giao diện bảng điều khiển phân tích tài chính doanh nghiệp bằng Next.js và Tailwind CSS, hỗ trợ cả Dark mode và Light mode, phong cách chuyên nghiệp, mật độ thông tin cao."*

#### Các bước thực thi của Adapter:
1. **Kiểm tra runtime**:
   ```bash
   python scripts/ui_ux_pro_max_runner.py --status
   ```
2. **Sinh Design System chuẩn tài chính**:
   ```bash
   python scripts/ui_ux_pro_max_runner.py "fintech banking dashboard" --design-system
   ```
   *Kết quả thu nhận:*
   - **Style Category**: Data-Dense Dashboard / Swiss Minimalism.
   - **Primary Palette**: Navy Blue (`#0F172A`), Tech Gold (`#F59E0B`), Slate Border (`#334155`).
   - **Typography**: IBM Plex Sans (Heading & Body).
   - **Google Fonts Import**:
     ```css
     @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');
     ```
3. **Tra cứu quy chuẩn Next.js & Tailwind**:
   ```bash
   python scripts/ui_ux_pro_max_runner.py "responsive data table KPI cards" --stack nextjs --json
   ```
4. **Tích hợp với DEX Skills**:
   - Chuyển mã màu và spacing sang `dex-design-system-tokens` để tạo CSS variables cho Dark/Light mode.
   - Sử dụng `dex-ui-component-contracts` định nghĩa contract cho `KPICard` và `TransactionTable`.
   - Sử dụng `dex-ux-accessibility` đảm bảo các bảng dữ liệu có đầy đủ thẻ `<th>`, `scope="col"` và tỉ lệ tương phản chữ đạt trên 4.5:1.
