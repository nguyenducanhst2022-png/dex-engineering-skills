# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — BUILDER FOR GROUPS U & V (Skills 201–220)
Group U: Visual Design Intelligence (201–210)
Group V: Advanced Web Experiences (211–220)
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

GROUP_U_V_SKILLS = [
    # --- GROUP U: Visual Design Intelligence ---
    {
        "id": "dex-design-brief-synthesis",
        "index": 201,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Synthesize business requirements, user personas, and brand identity into an actionable visual design brief with aesthetic tokens, layout guidelines, and accessibility constraints. Use when kicking off new frontend projects, UI redesigns, or translating PRDs into design specifications.",
        "purpose": "Tổng hợp yêu cầu kinh doanh, chân dung người dùng (personas) và định vị thương hiệu thành bản đặc tả thiết kế trực quan (Visual Design Brief) có tính hành động cao; xác lập ngôn ngữ thị giác, bảng màu ngữ nghĩa, tỷ lệ typography và tiêu chuẩn trải nghiệm người dùng.",
        "when_use": [
            "Khi khởi động dự án frontend mới hoặc giai đoạn tái thiết kế giao diện (UI redesign).",
            "Khi cần chuyển đổi tài liệu Product Requirements Document (PRD) sang ngôn ngữ thị giác và cấu trúc component.",
            "Khi cần thống nhất phong cách thẩm mỹ giữa Product Managers, Designers và Frontend Engineers."
        ],
        "when_not_use": [
            "Khi chỉ sửa các lỗi CSS nhỏ hoặc tinh chỉnh pixel đơn lẻ trong component đã có.",
            "Khi chưa có mục tiêu kinh doanh hoặc đối tượng người dùng rõ ràng."
        ],
        "prereqs": "Tài liệu yêu cầu sản phẩm (PRD), hướng dẫn nhận diện thương hiệu (Brand Guidelines), hồ sơ người dùng mục tiêu.",
        "concepts": [
            "Aesthetic Intent: Xác định rõ trạng thái cảm xúc (ví dụ: Modern Enterprise, Minimalist, Cyberpunk).",
            "Design Token Primitives: Thiết lập các biến số nền tảng về màu sắc, khoảng cách và kiểu chữ.",
            "Accessibility Baselines: Đặt mục tiêu tương phản tối thiểu WCAG 2.1 AA/AAA ngay từ khâu thiết kế."
        ],
        "steps": [
            "Thu thập mục tiêu sản phẩm, chân dung người dùng và ràng buộc thương hiệu từ stakeholder.",
            "Xác định tính cách giao diện (archetype) và các nguyên lý thiết kế chủ đạo (Design Principles).",
            "Đặc tả hệ thống màu sắc ngữ nghĩa (semantic palette), tỷ lệ font (type scale) và thang khoảng cách (spacing scale).",
            "Thiết lập cấu trúc bố cục lưới (grid), breakpoints responsive và quy tắc phân cấp thị giác.",
            "Xuất bản tài liệu `DESIGN_BRIEF.md` và đồng bộ token cơ sở vào hệ thống tokens."
        ],
        "code_lang": "json",
        "code_example": """{
  "$schema": "https://dex.dev/schemas/design-brief.json",
  "project": "dex-cloud-console",
  "archetype": "High-Density Enterprise SaaS",
  "designPrinciples": [
    "Information density over decorative whitespace",
    "Instant telemetry readability with APCA 75+ contrast",
    "Predictable keyboard-driven navigation flows"
  ],
  "visualTokens": {
    "colorModes": ["light", "dark", "high-contrast"],
    "baseFontFamily": "Inter, system-ui, sans-serif",
    "baseUnit": 4,
    "targetWCAG": "WCAG_2_1_AA"
  }
}""",
        "antipatterns": [
            "Bắt đầu code giao diện mà không có tài liệu định hướng phong cách dẫn đến UI chắp vá.",
            "Lựa chọn màu sắc thuần túy theo sở thích cá nhân mà bỏ qua kiểm tra độ tương phản và ngữ cảnh sử dụng.",
            "Thiết kế bố cục cứng nhắc theo một độ phân giải duy nhất, gây vỡ giao diện trên màn hình khác."
        ],
        "quality_gates": [
            "QG-01: Tài liệu `DESIGN_BRIEF.md` hoàn chỉnh với đầy đủ bảng màu, typography và lưới bố cục.",
            "QG-02: Bảng màu đáp ứng tỷ lệ tương phản tối thiểu 4.5:1 cho văn bản thông thường theo WCAG 2.1 AA.",
            "QG-03: Được phê duyệt bởi cả bộ phận kỹ thuật frontend và quản lý sản phẩm."
        ],
        "security": "Không nhúng các tài nguyên hình ảnh hoặc font chữ không có bản quyền thương mại; bảo vệ bí mật dự án trong tài liệu brief.",
        "deliverables": [
            "Tài liệu `DESIGN_BRIEF.md` chuẩn hóa.",
            "Bảng token khởi tạo ban đầu `tokens.brief.json`.",
            "Checklist tiêu chí kiểm tra thiết kế trực quan."
        ],
        "related": ["dex-visual-hierarchy-audit", "dex-design-system-tokens", "dex-color-contrast-systems"],
        "scenario": "Đội ngũ phát triển chuẩn bị xây dựng phân hệ quản trị hạ tầng đám mây. Kỹ sư kích hoạt `dex-design-brief-synthesis` để chuyển đổi tài liệu PRD dài 30 trang thành một Design Brief cô đọng, định hình giao diện bảng điều khiển mật độ cao với chế độ Dark Mode chuẩn xác."
    },
    {
        "id": "dex-visual-hierarchy-audit",
        "index": 202,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Audit and restructure visual hierarchy, content emphasis, information density, and reading order across complex screens to eliminate competing focal points. Use when evaluating confusing UI layouts, cluttered dashboards, or high-friction landing pages.",
        "purpose": "Kiểm toán và tái cấu trúc phân cấp thị giác (Visual Hierarchy), độ nổi bật của nội dung, mật độ thông tin và thứ tự đọc trên các màn hình phức tạp; triệt tiêu các điểm nhấn thị giác cạnh tranh nhau, dẫn dắt ánh nhìn người dùng đến các hành động chuyển đổi chính.",
        "when_use": [
            "Khi màn hình hiển thị quá nhiều nút bấm, thẻ thông tin khiến người dùng bị quá tải nhận thức (cognitive overload).",
            "Khi tỷ lệ chuyển đổi hoặc hoàn thành tác vụ trên trang quan trọng bị sụt giảm.",
            "Trước khi phát hành một tính năng phức tạp có nhiều mức độ ưu tiên thông tin khác nhau."
        ],
        "when_not_use": [
            "Khi kiểm tra hiệu năng tải trang thuần túy (Network/Render latency) - dùng `dex-frontend-performance`.",
            "Khi viết unit test cho các logic tính toán nội bộ không có giao diện người dùng."
        ],
        "prereqs": "Ảnh chụp màn hình (Figma/Live UI), DOM tree hiện tại, thứ tự ưu tiên nghiệp vụ của từng khối nội dung.",
        "concepts": [
            "Visual Weight: Mức độ hút mắt dựa trên kích thước, độ tương phản màu sắc, vị trí và khoảng trống.",
            "F-Shape / Z-Pattern: Đường quét mắt tự nhiên của người dùng theo thói quen đọc văn hóa.",
            "Focal Point Isolation: Giới hạn tối đa một điểm nhấn thị giác chính (Primary CTA) trên mỗi vùng nhìn."
        ],
        "steps": [
            "Liệt kê tất cả các phần tử trên màn hình và gắn nhãn mức độ ưu tiên: Primary, Secondary, Tertiary.",
            "Áp dụng phương pháp làm mờ (Squint Test / Blur Filter) để nhận diện các điểm sáng gây phân tán ánh nhìn.",
            "Đo lường tỷ lệ tương phản và độ lớn phông chữ để đảm bảo trật tự đọc tuyến tính rõ ràng.",
            "Tái cấu trúc bố cục, tăng padding âm (whitespace) xung quanh phần tử trọng tâm và giảm sắc độ của phần tử phụ.",
            "Lập biên bản đánh giá phân cấp thị giác kèm kiến nghị tinh chỉnh CSS/DOM."
        ],
        "code_lang": "css",
        "code_example": """/* Enforcing Strict Visual Hierarchy */
.primary-action-card {
  border: 2px solid var(--color-brand-primary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

.secondary-meta-card {
  border: 1px solid var(--color-border-subtle);
  background-color: var(--color-surface-subdued);
  color: var(--color-text-muted);
  opacity: 0.85;
}""",
        "antipatterns": [
            "Đặt từ 3 nút bấm phong cách `filled primary` cạnh nhau trên cùng một thẻ.",
            "Dùng màu đỏ báo động cho các thông tin trạng thái thông thường làm mất tác dụng của cảnh báo lỗi.",
            "Thu nhỏ cỡ chữ quá mức (<11px) để nhồi nhét dữ liệu thay vì cấu trúc lại thông tin."
        ],
        "quality_gates": [
            "QG-01: Điểm nhấn thị giác chính (Primary Focal Point) chiếm vị trí ưu tiên và được nhận diện trong 3 giây đầu.",
            "QG-02: Tỷ lệ phân cấp kích cỡ font chữ giữa Title, Subtitle và Body tuân thủ hệ số tỷ lệ tối thiểu 1.25x.",
            "QG-03: Không có xung đột màu sắc giữa các trạng thái cảnh báo và màu sắc nhận diện thương hiệu."
        ],
        "security": "Không ẩn giấu các điều khoản dịch vụ hoặc cảnh báo bảo mật quan trọng bằng kỹ thuật giảm kích thước chữ.",
        "deliverables": [
            "Báo cáo `VISUAL_HIERARCHY_AUDIT.md` phân tích trước và sau khi tối ưu.",
            "Sơ đồ luồng quét mắt (Eye-path diagram) và bản vá CSS định hình phân cấp."
        ],
        "related": ["dex-design-brief-synthesis", "dex-layout-composition-patterns", "dex-ux-accessibility"],
        "scenario": "Trang thanh toán của hệ thống e-commerce có 4 nút bấm cùng màu xanh lá cây gây nhầm lẫn khi người dùng muốn nhập mã giảm giá. Áp dụng `dex-visual-hierarchy-audit` để hạ cấp nút áp dụng mã thành dạng ghost button và làm nổi bật nút 'Đặt hàng ngay'."
    },
    {
        "id": "dex-layout-composition-patterns",
        "index": 203,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Evaluate and engineer responsive layout compositions including 12-column grids, asymmetric Bento boxes, editorial flows, and split-screen dashboards. Use when selecting page architecture, organizing multi-card views, or designing responsive breakpoints.",
        "purpose": "Đánh giá, lựa chọn và hiện thực hóa các mô hình bố cục không gian (Layout Compositions) hiện đại: hệ thống lưới 12 cột, bố cục Bento Box bất đối xứng, dòng chảy bài viết (editorial flow) và bố cục chia màn hình (split-screen); đảm bảo co giãn mượt mà trên mọi thiết bị.",
        "when_use": [
            "Khi xây dựng cấu trúc trang mới cho landing page, portal quản trị hoặc ứng dụng đa phương tiện.",
            "Khi tổ chức các thẻ nội dung có kích thước và mức độ quan trọng không đồng đều.",
            "Khi giải quyết vấn đề tràn nội dung (overflow) hoặc khoảng trống thừa vô lý trên màn hình siêu rộng (Ultrawide)."
        ],
        "when_not_use": [
            "Khi thiết kế các phần tử nội dòng (inline elements) đơn giản như badge, icon hoặc breadcrumbs.",
            "Khi hệ thống đã có template khung cứng cố định không cho phép thay đổi cấu trúc trang."
        ],
        "prereqs": "Đặc tả các thành phần nội dung, kích thước màn hình mục tiêu (mobile, tablet, desktop, ultrawide), hệ thống spacing token.",
        "concepts": [
            "Bento Grid Architecture: Gom nhóm thông tin theo các khối chữ nhật có kích thước tỷ lệ hài hòa (1x1, 1x2, 2x2).",
            "CSS Subgrid & Grid Template Areas: Định nghĩa cấu trúc lưới phân tầng bảo toàn sự gióng hàng giữa các thẻ con.",
            "Container Queries (`@container`): Co giãn bố cục dựa trên không gian thực của component cha thay vì viewport toàn trang."
        ],
        "steps": [
            "Phân tích dạng nội dung và xác định mô hình bố cục phù hợp (Bento, 12-col grid, Masonry hoặc Master-Detail).",
            "Thiết lập CSS Grid layout với các vùng định danh `grid-template-areas` trực quan.",
            "Khai báo Container Queries để các component con tự thích ứng khi nằm ở cột hẹp hay cột rộng.",
            "Kiểm tra co giãn trên các mốc kích thước cực hạn (320px mobile đến 3840px 4K monitor).",
            "Xác nhận các quy tắc chuyển đổi bố cục không gây giật cục hoặc chồng chéo nội dung."
        ],
        "code_lang": "css",
        "code_example": """/* Bento Grid Layout Pattern */
.bento-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  gap: var(--space-4);
}

.bento-card-featured {
  grid-column: span 2;
  grid-row: span 2;
}

.bento-card-stat {
  grid-column: span 1;
}

@container (max-width: 640px) {
  .bento-container {
    grid-template-columns: 1fr;
  }
}""",
        "antipatterns": [
            "Sử dụng lồng ghép quá nhiều thẻ `div` với `display: flex` phức tạp thay vì dùng một cấu trúc `CSS Grid` duy nhất.",
            "Cố định chiều cao phần tử bằng pixel cứng (`height: 300px`) khiến nội dung bị tràn khi chữ phóng to.",
            "Thiết kế chỉ nghĩ đến desktop rồi ép co cụm trên mobile khiến người dùng phải cuộn ngang bất tiện."
        ],
        "quality_gates": [
            "QG-01: Không xuất hiện thanh cuộn ngang (horizontal scrollbar) không mong muốn ở bất kỳ breakpoint nào.",
            "QG-02: Cấu trúc lưới duy trì khoảng cách `gap` đồng bộ theo thang spacing chuẩn.",
            "QG-03: Kiểm tra hiển thị đạt chuẩn trên cả 4 kích thước: Mobile (375px), Tablet (768px), Desktop (1440px), 4K (2560px)."
        ],
        "security": "Ngăn ngừa hiện tượng Clickjacking bằng cách kiểm soát cấu trúc frame và không cho phép chèn đè iframe vô hình lên bố cục.",
        "deliverables": [
            "Mẫu CSS Layout module chuẩn hóa (`layout.bento.css`).",
            "Bộ quy tắc responsive breakpoint và container query guidelines."
        ],
        "related": ["dex-visual-hierarchy-audit", "dex-fluid-typography-engineering", "dex-ui-component-contracts"],
        "scenario": "Xây dựng dashboard tổng hợp telemetry IoT. Áp dụng kỹ năng `dex-layout-composition-patterns` để tạo Bento Grid đa tầng hiển thị biểu đồ nhiệt độ chính ở khung 2x2, các trạng thái pin ở khung 1x1 và tự động gập thành 1 cột trên mobile."
    },
    {
        "id": "dex-color-contrast-systems",
        "index": 204,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Engineer mathematical APCA and WCAG 2.1 AA/AAA color contrast relationships across semantic UI states, light/dark themes, and interactive focus states. Use when building accessible color palettes, styling data visualizations, or remediating contrast failures.",
        "purpose": "Xây dựng hệ thống bảng màu toán học đáp ứng tiêu chuẩn tương phản WCAG 2.1 (AA/AAA) và giải thuật APCA (Accessible Perceptual Contrast Algorithm); đảm bảo khả năng đọc hoàn hảo trên các trạng thái giao diện, chế độ sáng/tối (Light/Dark mode) và độ tương phản cao.",
        "when_use": [
            "Khi xây dựng hoặc refactor bảng màu cho Design System của doanh nghiệp.",
            "Khi nhận báo cáo kiểm toán tiếp cận (Accessibility Audit) cảnh báo lỗi độ tương phản thấp.",
            "Khi thiết kế biểu đồ trực quan hóa dữ liệu có nhiều series màu sắc cần phân biệt rõ ràng."
        ],
        "when_not_use": [
            "Khi làm việc với các phần tử đồ họa trang trí thuần túy không mang ý nghĩa thông tin hoặc điều hướng.",
            "Khi trạng thái phần tử bị vô hiệu hóa (disabled state) mà tiêu chuẩn WCAG có ngoại lệ cho phép."
        ],
        "prereqs": "Mã màu hex/hsl của thương hiệu, danh sách các trạng thái tương tác (default, hover, focus, active, disabled).",
        "concepts": [
            "WCAG 2.1 Relative Luminance: Tỷ lệ tương phản 4.5:1 (normal text) và 3:1 (large text / UI components).",
            "APCA (Advanced Perceptual Contrast Algorithm): Đo lường độ tương phản theo cảm nhận thị giác thực tế của não bộ.",
            "Semantic Color Tokens: Tách biệt màu sắc chức năng (success, warning, error, info) khỏi màu thương hiệu."
        ],
        "steps": [
            "Thu thập danh mục màu nền (surface/background) và màu tiền cảnh (text/icon).",
            "Chạy script tính toán Relative Luminance và tỷ lệ tương phản cho từng cặp màu phối hợp.",
            "Kiểm tra tính đọc được trên cả 2 nền Light và Dark mode, tự động điều chỉnh sắc độ (Lightness/Chroma) nếu vi phạm.",
            "Thiết lập đường viền chỉ báo tiêu điểm (focus indicator) với tỷ lệ tương phản tối thiểu 3:1 so với nền lân cận.",
            "Xuất ra ma trận kiểm toán tương phản màu sắc `CONTRAST_MATRIX.json`."
        ],
        "code_lang": "typescript",
        "code_example": """// Mathematical WCAG Contrast Ratio Calculation
export function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

export function getContrastRatio(rgb1: [number, number, number], rgb2: [number, number, number]): number {
  const lum1 = getLuminance(...rgb1);
  const lum2 = getLuminance(...rgb2);
  const brightest = Math.max(lum1, lum2);
  const darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}""",
        "antipatterns": [
            "Dùng chữ màu xám nhạt `#A0AEC0` trên nền trắng `#FFFFFF` (tỷ lệ chỉ đạt ~2.4:1, vi phạm nặng WCAG).",
            "Chỉ dùng duy nhất màu sắc để biểu thị trạng thái (ví dụ chấm đỏ/xanh) mà không kèm icon hoặc nhãn văn bản cho người mù màu.",
            "Chuyển đổi sang Dark Mode bằng cách đảo ngược màu cơ học khiến nền xám quá chói mắt."
        ],
        "quality_gates": [
            "QG-01: 100% văn bản nội dung thông thường đạt tỷ lệ tương phản >= 4.5:1.",
            "QG-02: 100% thành phần điều khiển giao diện (inputs, borders, icons) đạt tỷ lệ >= 3:1.",
            "QG-03: Vượt qua bài kiểm tra mô phỏng 3 dạng mù màu chính: Protanopia, Deuteranopia và Tritanopia."
        ],
        "security": "Đảm bảo các thông báo cảnh báo bảo mật và lỗi xác thực luôn có độ tương phản cao nhất để người dùng chú ý kịp thời.",
        "deliverables": [
            "Ma trận tương phản màu sắc `CONTRAST_MATRIX.json`.",
            "Hệ thống token màu CSS/Tailwind đã được hiệu chuẩn tương phản."
        ],
        "related": ["dex-design-system-tokens", "dex-ux-accessibility", "dex-ui-visual-qa-review"],
        "scenario": "Kiểm toán hệ thống ngân hàng trực tuyến. Áp dụng `dex-color-contrast-systems` để rà soát toàn bộ 48 cặp màu UI, phát hiện 12 cặp chữ xám không đủ tương phản trên nền xám phụ và tự động nâng sắc độ từ `#888` lên `#595959` để đạt chuẩn AA."
    },
    {
        "id": "dex-fluid-typography-engineering",
        "index": 205,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Implement mathematical fluid typography scales using CSS clamp(), responsive modular scales, dynamic optical sizing, and optimal line-height geometry. Use when establishing typography tokens, eliminating layout shifts from font loading, or optimizing reading comfort.",
        "purpose": "Hiện thực hóa hệ thống typography co giãn liên tục (Fluid Typography) dựa trên hàm toán học `clamp()`, modular scale tỷ lệ vàng, optical sizing động và tỷ lệ chiều cao dòng (line-height) tối ưu; loại bỏ hoàn toàn hiện tượng giật cục khi nhảy breakpoint màn hình.",
        "when_use": [
            "Khi xây dựng typography tokens cho ứng dụng responsive đa màn hình.",
            "Khi muốn tiêu đề co giãn mượt mà theo kích thước viewport mà không cần viết hàng chục `@media` query rời rạc.",
            "Khi tối ưu trải nghiệm đọc cho các bài viết dạng dài (long-form editorial) hoặc tài liệu kỹ thuật."
        ],
        "when_not_use": [
            "Cho các nhãn nhỏ trong bảng dữ liệu hoặc UI cố định không được phép co giãn.",
            "Khi các trình duyệt mục tiêu là trình duyệt nhúng cổ điển không hỗ trợ hàm toán học CSS `clamp()`."
        ],
        "prereqs": "Khoảng viewport tối thiểu và tối đa (ví dụ: 360px đến 1440px), kích thước font tối thiểu và tối đa tương ứng.",
        "concepts": [
            "Linear Interpolation Equation: `clamp(min, preferred_vw, max)` với độ dốc tính toán theo `slope = (max - min) / (max_vw - min_vw)`.",
            "Dynamic Line-Height: Kích thước chữ càng lớn thì tỷ lệ `line-height` càng giảm dần (ví dụ 1.1 cho H1, 1.5 cho Body).",
            "Variable Font Optical Sizing: Tự động điều chỉnh độ dày và chi tiết chữ theo kích thước hiển thị (`font-optical-sizing: auto`)."
        ],
        "steps": [
            "Xác định kích thước cơ sở (base font-size) và tỷ lệ bước nhảy (Modular Ratio, ví dụ: 1.25 Major Third).",
            "Thiết lập cận dưới màn hình `min_width` và cận trên `max_width`.",
            "Áp dụng công thức nội suy tuyến tính để tính toán giá trị `y-axis intersection` và `slope in vw`.",
            "Tạo biến CSS Custom Properties cho từng cấp bậc: `--font-display`, `--font-h1`, `--font-h2`, `--font-body`.",
            "Kiểm tra trực quan độ mượt khi thay đổi kích thước cửa sổ trình duyệt (Window Resize Test)."
        ],
        "code_lang": "css",
        "code_example": """/* Fluid Typography Calculation */
:root {
  /* min: 32px @ 375px viewport, max: 64px @ 1440px viewport */
  /* slope = (64 - 32) / (1440 - 375) = 0.03004 => 3.004vw */
  /* intercept = 32 - (375 * 0.03004) = 20.73px */
  --font-h1-fluid: clamp(2rem, 1.295rem + 3.004vw, 4rem);
  --font-body-fluid: clamp(1rem, 0.941rem + 0.25vw, 1.125rem);
}

h1 {
  font-size: var(--font-h1-fluid);
  line-height: 1.15;
  letter-spacing: -0.02em;
}""",
        "antipatterns": [
            "Dùng `font-size: 5vw` trực tiếp mà không có hàm `clamp()` bọc ngoài, dẫn đến chữ quá bé trên mobile hoặc quá khổng lồ trên màn hình 4K.",
            "Giữ nguyên `line-height: 1.5` cho tiêu đề kích thước 48px khiến khoảng trống giữa các dòng bị loãng quá mức.",
            "Dùng đơn vị pixel tuyệt đối làm mất khả năng phóng to chữ của người dùng khi cài đặt trợ năng trình duyệt."
        ],
        "quality_gates": [
            "QG-01: Cỡ chữ co giãn liên tục, không có hiện tượng vỡ layout hoặc nhảy bước khi resize.",
            "QG-02: Đơn vị font cơ sở tôn trọng cài đặt gốc của người dùng (`rem` thay vì `px` cứng).",
            "QG-03: Chiều dài dòng đọc (Measure) của văn bản body duy trì trong ngưỡng tối ưu từ 45 đến 75 ký tự."
        ],
        "security": "Không nạp các webfont từ các CDN không đáng tin cậy để ngăn ngừa tấn công man-in-the-middle hoặc lộ dữ liệu người dùng qua font fingerprinting.",
        "deliverables": [
            "Module CSS Typography tokens `typography.fluid.css`.",
            "Bảng tính toán tham số clamp cho toàn bộ các cấp bậc tiêu đề."
        ],
        "related": ["dex-design-system-tokens", "dex-layout-composition-patterns", "dex-frontend-performance"],
        "scenario": "Xây dựng portal tin tức công nghệ đa nền tảng. Sử dụng `dex-fluid-typography-engineering` để thiết lập thang đo tiêu đề co giãn mượt mà từ 28px trên iPhone mini lên tới 72px trên màn hình Ultrawide 34 inch mà không cần đến một dòng media query nào."
    },
    {
        "id": "dex-motion-interaction-specification",
        "index": 206,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Specify purposeful UI motion choreographies, spring physics curves, transition durations, and strict prefers-reduced-motion accessibility fallbacks. Use when authoring design tokens for animation, adding micro-interactions, or engineering page transitions.",
        "purpose": "Đặc tả các chuyển động tương tác (UI Motion & Micro-interactions) có mục đích rõ ràng, dựa trên vật lý đàn hồi (spring physics) và đường cong gia tốc tự nhiên; thiết lập các khoảng thời gian chuyển tiếp tối ưu và cơ chế an toàn cho người dùng mẫn cảm tiền đình (`prefers-reduced-motion`).",
        "when_use": [
            "Khi thêm hiệu ứng chuyển cảnh trang (page transition) hoặc mở modal dialog.",
            "Khi đặc tả chuyển động cho các nút bấm, menu thả xuống và thanh thông báo toast.",
            "Khi cần đồng bộ ngôn ngữ chuyển động (Motion Tokens) giữa Figma và mã nguồn frontend."
        ],
        "when_not_use": [
            "Khi tạo các animation trang trí lặp đi lặp lại vô tận gây mất tập trung người dùng.",
            "Khi tối ưu hiệu năng tính toán dữ liệu của backend."
        ],
        "prereqs": "Danh sách các tương tác UI cần hiệu ứng, thời gian thực thi mong muốn, thư viện animation mục tiêu (CSS, Framer Motion, GSAP).",
        "concepts": [
            "Choreography & Staggering: Trình tự xuất hiện có thứ bậc giữa các phần tử liên quan (ví dụ các item trong danh sách xuất hiện cách nhau 50ms).",
            "Physics-Based Easing: Sử dụng cubic-bezier tự nhiên (Deceleration curve cho phần tử vào, Acceleration cho phần tử ra).",
            "Vestibular Safety: Tôn trọng hoàn toàn truy vấn `@media (prefers-reduced-motion: reduce)` bằng cách chuyển chuyển động trượt sang mờ dần (fade)."
        ],
        "steps": [
            "Phân loại các dạng chuyển động: Micro-interaction (<200ms), Context Transition (200-400ms), Expressive (>400ms).",
            "Xác định đường cong chuyển động chuẩn: `--ease-out-back`, `--ease-in-out-smooth`.",
            "Triển khai quy tắc CSS hoặc hook React có xử lý `prefers-reduced-motion`.",
            "Kiểm tra hiệu năng animation đạt chuẩn 60fps/120fps bằng Chrome DevTools Performance panel.",
            "Đóng gói thành bộ token `motion.tokens.json`."
        ],
        "code_lang": "css",
        "code_example": """/* Motion Tokens with Vestibular Safety */
:root {
  --motion-duration-fast: 150ms;
  --motion-duration-normal: 250ms;
  --motion-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-sheet {
  transition: transform var(--motion-duration-normal) var(--motion-ease-out),
              opacity var(--motion-duration-fast) linear;
}

@media (prefers-reduced-motion: reduce) {
  .modal-sheet {
    transition: opacity var(--motion-duration-fast) linear;
    transform: none !important;
  }
}""",
        "antipatterns": [
            "Lạm dụng animation dài hơn 500ms cho các tác vụ thường ngày khiến người dùng cảm thấy hệ thống chậm chạp.",
            "Animate các thuộc tính kích hoạt Layout Thrashing như `left`, `top`, `width`, `height` thay vì dùng `transform` và `opacity`.",
            "Bỏ qua truy vấn `prefers-reduced-motion` khiến người dùng bị chóng mặt hoặc buồn nôn khi sử dụng."
        ],
        "quality_gates": [
            "QG-01: 100% animation chỉ tác động lên thuộc tính `transform` và `opacity`.",
            "QG-02: Có kiểm thử tự động xác nhận hiệu ứng trượt bị vô hiệu hóa khi bật `prefers-reduced-motion`.",
            "QG-03: Tốc độ khung hình duy trì ổn định không rớt dưới 58fps trong suốt quá trình chuyển động."
        ],
        "security": "Không chèn mã JavaScript độc hại thông qua các trình phân tích SVG animation hoặc lặp lại vô hạn gây nghẽn CPU (Denial of Service).",
        "deliverables": [
            "Bộ Motion Tokens chuẩn `motion.tokens.json`.",
            "Bộ quy tắc CSS chuyển động an toàn trợ năng."
        ],
        "related": ["dex-web-animation-performance", "dex-ux-accessibility", "dex-ui-component-contracts"],
        "scenario": "Thiết kế tương tác mở ngăn kéo sidebar cho ứng dụng SaaS. Áp dụng `dex-motion-interaction-specification` để tạo đường cong trượt gia tốc 250ms tự nhiên và tự động chuyển sang hiệu ứng mờ dần nhẹ nhàng 100ms khi người dùng kích hoạt cài đặt giảm chuyển động trên hệ điều hành."
    },
    {
        "id": "dex-dashboard-data-storytelling",
        "index": 207,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Architect analytical dashboard layouts that convey data stories, prioritize high-value KPI metrics, separate operational signals from decorative charts, and facilitate decision-making. Use when building enterprise BI portals, executive dashboards, or telemetry interfaces.",
        "purpose": "Thiết kế kiến trúc bảng điều khiển (Dashboard) và trực quan hóa dữ liệu theo lối kể chuyện (Data Storytelling); tổ chức phân cấp các chỉ số KPI then chốt, tách bạch tín hiệu vận hành thực tế khỏi các biểu đồ trang trí vô ích, giúp người dùng ra quyết định nhanh chóng và chuẩn xác.",
        "when_use": [
            "Khi xây dựng bảng điều khiển quản trị (Executive Dashboard) hoặc cổng phân tích dữ liệu BI.",
            "Khi người dùng phàn nàn dashboard có quá nhiều đồ thị nhưng không biết thông tin nào cần hành động ngay.",
            "Khi thiết kế hệ thống giám sát cảnh báo và telemetry thời gian thực."
        ],
        "when_not_use": [
            "Khi xây dựng các biểu mẫu nhập liệu CRUD thông thường.",
            "Khi xử lý logic truy vấn SQL dưới tầng cơ sở dữ liệu."
        ],
        "prereqs": "Danh sách các chỉ số kinh doanh mục tiêu, tần suất cập nhật dữ liệu, vai trò người xem (Giám đốc, Kỹ sư vận hành, Nhân viên phân tích).",
        "concepts": [
            "Inverted Pyramid of Information: Đặt số liệu tổng quan (High-level KPIs) ở trên cùng, xu hướng ở giữa và chi tiết giao dịch ở dưới.",
            "Chart-to-Data Matching: Chọn đúng loại biểu đồ (Line chart cho xu hướng thời gian, Bar chart cho so sánh danh mục, Bullet chart cho mục tiêu).",
            "Cognitive Load Reduction: Loại bỏ rác biểu đồ (Chartjunk) như lưới quá đậm, bóng đổ thừa thãi hoặc 3D không cần thiết."
        ],
        "steps": [
            "Xác định câu hỏi kinh doanh cốt lõi mà dashboard cần giải đáp trong 5 giây đầu tiên.",
            "Thiết kế thẻ tóm tắt chỉ số chính (Hero KPI Cards) kèm chỉ báo phần trăm biến động so với kỳ trước.",
            "Lựa chọn loại biểu đồ trực quan chính xác và áp dụng bảng màu dữ liệu có chủ đích (Màu xám cho bối cảnh, màu nổi bật cho ngoại lệ).",
            "Tạo cơ chế lọc dữ liệu tương tác (date range, categories) đồng bộ trên tất cả biểu đồ.",
            "Kiểm tra khả năng giải thích dữ liệu với người dùng thực tế."
        ],
        "code_lang": "typescript",
        "code_example": """// KPI Metric Visual Model Contract
export interface DashboardMetricSummary {
  metricId: string;
  label: string;
  currentValue: number;
  formattedValue: string;
  changeRate: number; // e.g. +0.125 for +12.5%
  trendDirection: 'upward' | 'downward' | 'neutral';
  isAnomaly: boolean;
  sparklinePoints: number[];
}""",
        "antipatterns": [
            "Sử dụng biểu đồ tròn (Pie chart) có nhiều hơn 5 lát cắt khiến người xem không thể so sánh tỷ lệ chính xác.",
            "Dùng biểu đồ 3D làm méo mó góc nhìn dữ liệu thực tế.",
            "Trộn lẫn quá nhiều màu sắc rực rỡ không đồng nhất khiến người dùng tưởng nhầm mọi dữ liệu đều đang bị cảnh báo lỗi."
        ],
        "quality_gates": [
            "QG-01: Chỉ số KPI quan trọng nhất được định vị tại vị trí ưu tiên góc trên bên trái màn hình.",
            "QG-02: Mỗi biểu đồ đều có tiêu đề rõ ràng, đơn vị đo lường và ghi chú nguồn dữ liệu.",
            "QG-03: Trực quan hóa dữ liệu hiển thị tốt ở độ phân giải tiêu chuẩn 1366x768 mà không bị cắt cụt trục số."
        ],
        "security": "Áp dụng cơ chế phân quyền xem dữ liệu theo vai trò (Role-Based Row Level Security) để không làm lộ số liệu nhạy cảm trên dashboard.",
        "deliverables": [
            "Bản thiết kế cấu trúc dashboard `dashboard.architecture.json`.",
            "Hướng dẫn trực quan hóa dữ liệu và lựa chọn biểu đồ cho hệ thống."
        ],
        "related": ["dex-visual-hierarchy-audit", "dex-layout-composition-patterns", "dex-analytics-instrumentation"],
        "scenario": "Phát triển dashboard tài chính cho ban giám đốc. Áp dụng `dex-dashboard-data-storytelling` để dọn dẹp 15 biểu đồ hỗn loạn, quy hoạch lại thành 3 thẻ KPI doanh thu - chi phí - lợi nhuận ở đầu trang, kèm một biểu đồ vùng so sánh kế hoạch và một bảng drill-down chi tiết giao dịch bất thường."
    },
    {
        "id": "dex-design-reference-evaluation",
        "index": 208,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Critically analyze visual design references, competitor benchmarks, and design inspiration against product requirements to extract reusable design principles without copyright infringement. Use during early product discovery, UI redesigns, or mood board evaluations.",
        "purpose": "Phân tích, đánh giá có phê phán các nguồn cảm hứng thiết kế, mẫu giao diện đối thủ cạnh tranh và sản phẩm mẫu; chắt lọc các nguyên lý trải nghiệm xuất sắc, mô hình tương tác hiệu quả và quy chuẩn thị giác mà tuyệt đối không sao chép vi phạm bản quyền hay tài sản sở hữu trí tuệ.",
        "when_use": [
            "Trong giai đoạn Product Discovery ban đầu hoặc chuẩn bị làm Moodboard cho dự án.",
            "Khi benchmark trải nghiệm người dùng của các sản phẩm hàng đầu trên thị trường.",
            "Khi cần giải thích cho stakeholder lý do nên hoặc không nên học tập một mô hình giao diện cụ thể."
        ],
        "when_not_use": [
            "Khi chỉ muốn copy mã nguồn HTML/CSS nguyên mẫu của trang web khác vào dự án.",
            "Khi hệ thống đã có design system hoàn thiện và chỉ việc áp dụng các component sẵn có."
        ],
        "prereqs": "Ảnh chụp tham khảo, danh sách URL sản phẩm cần benchmark, tiêu chí kinh doanh và giá trị khác biệt của sản phẩm.",
        "concepts": [
            "Functional Deconstruction: Bóc tách giao diện thành các lớp độc lập: Layout, Color Palette, Typography, Information Flow.",
            "Clean-Room Design Principle: Tiếp thu ý tưởng giải quyết vấn đề của đối thủ nhưng tự tay thiết kế và lập trình lại toàn bộ từ đầu.",
            "Context Appropriateness: Đánh giá xem giải pháp của đối thủ có thực sự phù hợp với tập người dùng mục tiêu của mình hay không."
        ],
        "steps": [
            "Thu thập từ 3 đến 5 mẫu thiết kế xuất sắc trong và ngoài ngành liên quan đến bài toán.",
            "Lập ma trận phân tích điểm mạnh, điểm yếu và các cơ hội cải tiến của từng mẫu tham khảo.",
            "Bóc tách các pattern hành vi người dùng (User Mental Model) thành công từ các mẫu.",
            "Lọc bỏ các yếu tố không phù hợp với nhận diện thương hiệu hoặc tài nguyên kỹ thuật hiện có.",
            "Tổng hợp thành tài liệu kiến nghị nguyên lý thiết kế `DESIGN_BENCHMARK_SYNTHESIS.md`."
        ],
        "code_lang": "markdown",
        "code_example": """<!-- Design Reference Evaluation Matrix -->
| Reference Product | Layout Pattern | Hierarchy Strengths | Weaknesses / Risks | Applicable Principle for DEX |
| :--- | :--- | :--- | :--- | :--- |
| Product A | Asymmetric Bento | Clear focal hero metric | Heavy scroll on mobile | Adopt 2x2 hero card for stats |
| Product B | Left-hand Rail + Tabs | Excellent deep navigation | High cognitive overhead | Keep 1-level clean sidebar |""",
        "antipatterns": [
            "Sao chép nguyên xi giao diện của đối thủ (Pixel-for-pixel cloning) dẫn đến rủi ro pháp lý và đánh mất bản sắc thương hiệu.",
            "Áp dụng phong cách thiết kế thời thượng (Trend-chasing) nhưng làm hỏng khả năng sử dụng của đối tượng người dùng chính.",
            "Không đánh giá tính khả thi kỹ thuật khiến thiết kế tham khảo không thể triển khai trên thực tế."
        ],
        "quality_gates": [
            "QG-01: Tài liệu đánh giá tham khảo bao gồm tối thiểu 3 sản phẩm đối chuẩn độc lập.",
            "QG-02: Không chứa tài sản đồ họa, vector logo hoặc mã nguồn độc quyền của bên thứ ba.",
            "QG-03: Có phần phân tích rõ ràng về tính khác biệt (Differentiation Factor) của sản phẩm nội bộ."
        ],
        "security": "Tuân thủ nghiêm ngặt quyền sở hữu trí tuệ, luật thương hiệu và các quy định về bảo vệ bí mật kinh doanh.",
        "deliverables": [
            "Báo cáo phân tích đối chuẩn `DESIGN_BENCHMARK_SYNTHESIS.md`.",
            "Danh mục các nguyên lý tương tác được phê duyệt để áp dụng."
        ],
        "related": ["dex-design-brief-synthesis", "dex-design-system-documentation", "dex-ui-ux-pro-max-adapter"],
        "scenario": "Đội ngũ phát triển chuẩn bị làm lại tính năng quản lý giỏ hàng. Kỹ sư kích hoạt `dex-design-reference-evaluation` để phân tích luồng thanh toán của 4 nền tảng e-commerce lớn, nhận diện mẫu accordion một trang là tối ưu nhất và đề xuất triển khai với phong cách tối giản riêng biệt."
    },
    {
        "id": "dex-design-system-documentation",
        "index": 209,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Author living design system documentation, component anatomies, token tables, interactive storybook examples, and usage do's and don'ts. Use when standardizing design system primitives, onboarding developers, or publishing UI style guides.",
        "purpose": "Xây dựng tài liệu hệ thống thiết kế sống (Living Design System Documentation); mô tả giải phẫu component (Component Anatomy), bảng chỉ mục design tokens, ví dụ tương tác trực quan (Storybook) và các quy tắc nên/không nên làm (Do's & Don'ts); tạo tiếng nói chung giữa Designer và Developer.",
        "when_use": [
            "Khi hoàn thành một component mới hoặc nâng cấp thư viện Design System của tổ chức.",
            "Khi cần đào tạo (onboarding) các lập trình viên frontend mới gia nhập dự án.",
            "Khi thiết lập tài liệu hướng dẫn phong cách UI (UI Style Guide) tập trung."
        ],
        "when_not_use": [
            "Khi đang trong giai đoạn thử nghiệm prototype dùng một lần rồi bỏ.",
            "Khi tài liệu chỉ mô tả logic nghiệp vụ backend không liên quan đến component giao diện."
        ],
        "prereqs": "Bộ component code đã hoàn thiện, danh sách props TypeScript, các token màu sắc/khoảng cách được sử dụng.",
        "concepts": [
            "Component Anatomy: Bóc tách rõ ràng các thành phần con cấu thành nên component (Icon, Label, Container, Badge).",
            "Single Source of Truth: Tài liệu tự động đồng bộ từ comment mã nguồn hoặc file định nghĩa token.",
            "Usage Rules (Do's and Don'ts): Cung cấp các ví dụ hình ảnh trực quan về cách sử dụng đúng và các lỗi thường gặp."
        ],
        "steps": [
            "Vẽ sơ đồ giải phẫu component và liệt kê tất cả các biến thể (Variants: Primary, Secondary, Destructive).",
            "Đặc tả bảng thuộc tính TypeScript (Props Table) kèm kiểu dữ liệu, giá trị mặc định và mô tả công dụng.",
            "Liệt kê danh sách Design Tokens liên kết với component (CSS variables).",
            "Soạn thảo các trường hợp sử dụng chuẩn (Do's) và các trường hợp cấm kỵ (Don'ts).",
            "Tích hợp tài liệu vào Storybook hoặc cổng tài liệu nội bộ."
        ],
        "code_lang": "markdown",
        "code_example": """# Button Component

## Anatomy
1. **Container**: Chứa toàn bộ phần tử, quy định padding và border-radius.
2. **Icon (Tùy chọn)**: Kích thước cố định 16x16px, căn giữa theo trục dọc.
3. **Label**: Chữ in thường, font-weight 600, không bị ngắt dòng.

## Usage Guidelines
- **Nên (Do)**: Dùng duy nhất một Button variant `primary` trên mỗi nhóm hành động.
- **Không nên (Don't)**: Thay đổi màu nền của button bằng inline-style không qua token.""",
        "antipatterns": [
            "Viết tài liệu tĩnh trên file Word/Confluence rồi bỏ quên không cập nhật khi mã nguồn component đã thay đổi.",
            "Chỉ liệt kê props kỹ thuật mà không giải thích khi nào nên chọn variant nào.",
            "Thiếu ví dụ code mẫu khiến lập trình viên phải tự đoán cách import và sử dụng."
        ],
        "quality_gates": [
            "QG-01: 100% props công khai đều có mô tả chi tiết và ví dụ minh họa.",
            "QG-02: Có phần hướng dẫn tiếp cận bàn phím (Keyboard Navigation) và ARIA role tương ứng.",
            "QG-03: Tài liệu được biên soạn dưới dạng Markdown/MDX lưu trữ cùng mã nguồn."
        ],
        "security": "Không đưa các token xác thực thật, thông tin nội bộ mật vào các ví dụ minh họa trong tài liệu công khai.",
        "deliverables": [
            "Tài liệu component chuẩn `Button.doc.md`.",
            "File cấu hình Storybook tương tác `Button.stories.tsx`."
        ],
        "related": ["dex-design-system-tokens", "dex-ui-component-contracts", "dex-documentation-as-code"],
        "scenario": "Hoàn thiện component DateRangePicker phức tạp cho Design System. Sử dụng `dex-design-system-documentation` để viết tài liệu MDX hoàn chỉnh, minh họa cấu trúc DOM, bảng 14 props, ma trận token màu và hướng dẫn sử dụng phím tắt bàn phím cho toàn bộ công ty."
    },
    {
        "id": "dex-ui-visual-qa-review",
        "index": 210,
        "group": "Group U",
        "domain": "Visual Design Intelligence",
        "description": "Conduct rigorous visual quality assurance (Visual QA) reviews against production builds, verifying pixel alignment, spacing token adherence, font rendering, and edge-case states. Use prior to release sign-off, after major frontend refactors, or during design handoff verification.",
        "purpose": "Thực hiện quy trình kiểm thử chất lượng trực quan (Visual QA Review) nghiêm ngặt trên bản dựng môi trường thực tế; xác minh sự trùng khớp so với bản thiết kế Figma, tính đồng bộ của khoảng cách (spacing tokens), độ mượt mà khi hiển thị phông chữ và các trạng thái biên (edge cases).",
        "when_use": [
            "Trước khi ký biên bản phát hành (Release Sign-off) cho các tính năng frontend lớn.",
            "Sau các đợt tái cấu trúc mã nguồn CSS hoặc nâng cấp thư viện UI component.",
            "Khi kiểm tra sự đồng nhất hiển thị giữa các hệ điều hành và trình duyệt khác nhau."
        ],
        "when_not_use": [
            "Khi kiểm thử logic nghiệp vụ backend hoặc API integration.",
            "Khi mã nguồn frontend còn đang trong quá trình lập trình dở dang chưa hoàn thiện giao diện."
        ],
        "prereqs": "File thiết kế Figma đã duyệt, đường dẫn môi trường Staging/Preview, danh sách các trạng thái dữ liệu (Empty, Loading, Error, Full).",
        "concepts": [
            "Pixel-Precision Overlay: So khớp ảnh chụp màn hình thực tế với bản thiết kế bằng kỹ thuật lớp phủ bán trong suốt (semi-transparent overlay).",
            "Token Compliance Check: Kiểm tra xem các giá trị padding, margin, font-size có lấy từ Design Tokens hay dùng giá trị tùy tiện (arbitrary values).",
            "State Completeness: Kiểm tra đầy đủ 5 trạng thái giao diện: Default, Hover, Focus, Active, Disabled."
        ],
        "steps": [
            "Chụp ảnh màn hình các component chính trên môi trường chạy thử nghiệm.",
            "Đặt lớp phủ so sánh với thiết kế gốc để phát hiện sai lệch vị trí hoặc kích thước.",
            "Kiểm tra việc sử dụng biến CSS token thay vì hardcode giá trị pixel.",
            "Kích hoạt các trạng thái biên: văn bản cực dài gây tràn dòng, danh sách rỗng, lỗi mất mạng.",
            "Lập biên bản Visual QA Report ghi nhận danh sách các lỗi lệch pixel kèm ảnh chụp minh họa."
        ],
        "code_lang": "markdown",
        "code_example": """<!-- Visual QA Defect Log -->
### VQA-01: Header Spacing Mismatch
- **Component**: TopNavigationBar
- **Expected**: Padding 16px (var(--space-4))
- **Actual**: Padding 22px (hardcoded inline style)
- **Severity**: Minor
- **Remediation**: Thay thế class inline bằng `p-4` chuẩn Design Token.""",
        "antipatterns": [
            "Chỉ kiểm tra giao diện khi có dữ liệu đẹp lý tưởng mà không test trường hợp dữ liệu rỗng hoặc chữ quá dài.",
            "Bỏ qua kiểm tra trên màn hình Retina/High-DPI khiến hình ảnh bị mờ hoặc vỡ nét.",
            "Duyệt phát hành vội vàng mà không chụp ảnh bằng chứng so khớp."
        ],
        "quality_gates": [
            "QG-01: 100% các thành phần UI tuân thủ bảng mã Spacing Token quy định.",
            "QG-02: Sai lệch vị trí so với thiết kế Figma không vượt quá 2px cho các phần tử căn chỉnh.",
            "QG-03: Không có hiện tượng vỡ layout khi văn bản dài gấp đôi mức trung bình."
        ],
        "security": "Đảm bảo các trạng thái hiển thị thông tin người dùng nhạy cảm (như số thẻ tín dụng) luôn được che giấu đúng quy cách trên giao diện.",
        "deliverables": [
            "Biên bản nghiệm thu chất lượng hình ảnh `VISUAL_QA_REPORT.md`.",
            "Bộ ảnh chụp so khớp trước và sau khi khắc phục lỗi lệch pixel."
        ],
        "related": ["dex-visual-regression", "dex-design-handoff-verification", "dex-ux-accessibility"],
        "scenario": "Kiểm tra phiên bản cập nhật trang thanh toán trước ngày Black Friday. Kỹ sư kích hoạt `dex-ui-visual-qa-review`, phát hiện 3 lỗi lệch spacing ở nút thanh toán trên Safari iOS và 1 lỗi tràn chữ khi tên người dùng dài hơn 40 ký tự, kịp thời vá lỗi trước giờ mở bán."
    },

    # --- GROUP V: Advanced Web Experiences ---
    {
        "id": "dex-web-animation-performance",
        "index": 211,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Profile and optimize 60fps web animation performance, eliminating layout thrashing, forced synchronous layouts, and excessive composite layers using GPU transforms and Will-Change budgets. Use when diagnosing UI jank, dropped frames, or heavy scroll animations.",
        "purpose": "Đo lường, lập hồ sơ hiệu năng (Profiling) và tối ưu hóa chuyển động web đạt chuẩn mượt mà 60fps/120fps; triệt tiêu hiện tượng giật hình (UI Jank), hiện tượng tính toán lại layout cưỡng bức (Forced Synchronous Layout / Layout Thrashing) và quản trị bộ nhớ GPU composite layers.",
        "when_use": [
            "Khi các hiệu ứng cuộn trang (scroll-driven animations) hoặc chuyển cảnh bị giật cục, rớt khung hình.",
            "Khi quạt tản nhiệt của máy tính người dùng kêu to bất thường khi lướt web do ngốn CPU.",
            "Trước khi triển khai các hiệu ứng thị giác phức tạp trên thiết bị di động cấu hình trung bình."
        ],
        "when_not_use": [
            "Khi animation chỉ là một hiệu ứng mờ dần (fade-in) đơn giản kéo dài 100ms trên một button duy nhất.",
            "Khi kiểm tra hiệu năng truy vấn API dưới backend."
        ],
        "prereqs": "Chrome DevTools Performance trace file, mã nguồn CSS/JS của animation, danh sách các thiết bị mục tiêu.",
        "concepts": [
            "Pixel Pipeline: JS -> Style -> Layout -> Paint -> Composite. Chỉ animate thuộc tính Composite (transform, opacity).",
            "Layout Thrashing: Đọc thuộc tính hình học (`offsetHeight`) rồi ghi thuộc tính kiểu dáng lặp đi lặp lại trong vòng lặp.",
            "Will-Change Budget: Khai báo `will-change: transform` có chọn lọc để đưa phần tử lên layer GPU riêng và thu hồi bộ nhớ sau khi hoàn tất."
        ],
        "steps": [
            "Ghi lại trace hiệu năng 5 giây bằng Chrome DevTools Performance tab khi đang chạy animation.",
            "Xác định các khung hình màu đỏ (Dropped Frames / Long Tasks) và kiểm tra nguyên nhân (Layout, Recalculate Style hay Paint).",
            "Thay thế toàn bộ các thuộc tính gây layout (`top`, `left`, `margin`) bằng `transform: translate3d()`.",
            "Đảm bảo các tác vụ đọc DOM được gom cụm trước các tác vụ ghi DOM (sử dụng `requestAnimationFrame`).",
            "Xác nhận lại khung hình đạt 60fps ổn định trên cấu hình CPU bị giảm tốc độ 4x (4x CPU Throttling)."
        ],
        "code_lang": "javascript",
        "code_example": """// Eliminating Layout Thrashing via RequestAnimationFrame
function animateCards(cards) {
  // 1. Batch Read Phase
  const heights = cards.map(c => c.getBoundingClientRect().height);
  
  // 2. Batch Write Phase inside RAF
  requestAnimationFrame(() => {
    cards.forEach((card, i) => {
      card.style.transform = `translate3d(0, ${heights[i]}px, 0)`;
    });
  });
}""",
        "antipatterns": [
            "Gán `will-change: transform` lên hàng trăm phần tử cùng lúc gây cạn kiệt VRAM bộ nhớ đồ họa.",
            "Đọc `element.scrollTop` ngay giữa vòng lặp cập nhật vị trí khiến trình duyệt phải tính toán lại toàn bộ trang liên tục.",
            "Dùng `setInterval` hoặc `setTimeout` để làm animation thay vì `requestAnimationFrame`."
        ],
        "quality_gates": [
            "QG-01: Không có sự kiện 'Layout' hoặc 'Paint' xuất hiện trong suốt quá trình chạy vòng lặp animation.",
            "QG-02: Tỷ lệ khung hình duy trì >= 58fps trên thiết bị mô phỏng 4x CPU Throttling.",
            "QG-03: Bộ nhớ GPU layer được giải phóng hoàn toàn sau khi animation kết thúc."
        ],
        "security": "Không cho phép mã người dùng chèn các kịch bản animation vô tận tiêu thụ 100% CPU trên trình duyệt client.",
        "deliverables": [
            "Bản phân tích Performance Profile trước và sau khi tối ưu.",
            "Mã nguồn animation CSS/JS đã được chuyển đổi sang chuẩn GPU Composite."
        ],
        "related": ["dex-motion-interaction-specification", "dex-frontend-performance", "dex-ui-visual-qa-review"],
        "scenario": "Trang giới thiệu sản phẩm mới bị giật mạnh khi người dùng cuộn chuột qua danh sách thẻ 3D. Sử dụng `dex-web-animation-performance` để phân tích trace, phát hiện hiệu ứng đang animate thuộc tính `top` và `box-shadow`, thay thế bằng `transform: translate3d` và đưa FPS từ 22fps lên thẳng 60fps mượt mà."
    },
    {
        "id": "dex-media-delivery-pipelines",
        "index": 212,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Engineer modern responsive media pipelines supporting next-gen image formats (AVIF, WebP), adaptive audio, responsive picture elements, CDN image transformations, and blurhash placeholders. Use when optimizing media-heavy web apps, portfolio sites, or e-commerce catalogs.",
        "purpose": "Thiết kế và triển khai đường ống phân phối đa phương tiện (Media Delivery Pipeline) hiện đại; hỗ trợ các định dạng hình ảnh thế hệ mới (AVIF, WebP), thẻ `<picture>` responsive thông minh, cơ chế chuyển đổi ảnh động qua CDN và chuỗi giữ chỗ làm mờ (Blurhash placeholders) triệt tiêu độ trễ hiển thị.",
        "when_use": [
            "Khi ứng dụng web có nhiều hình ảnh khiến dung lượng tải trang vượt quá 3MB.",
            "Khi chỉ số Largest Contentful Paint (LCP) bị chậm do thời gian tải ảnh banner chính quá lâu.",
            "Khi xây dựng trang thương mại điện tử hoặc cổng tin tức đa phương tiện."
        ],
        "when_not_use": [
            "Khi ứng dụng chỉ chứa các icon vector SVG nhỏ.",
            "Khi tối ưu hóa các tệp tài liệu văn bản tĩnh thuần túy."
        ],
        "prereqs": "Hạ tầng lưu trữ hình ảnh (S3, Cloudflare Images), thư viện tối ưu ảnh (Sharp), CDN hỗ trợ chuyển đổi tham số URL.",
        "concepts": [
            "Modern Format Negotiation: Ưu tiên AVIF (tiết kiệm thêm 30% dung lượng so với WebP) với fallback tự động về WebP và JPEG.",
            "Resolution Switching (`srcset` & `sizes`): Cung cấp đúng độ phân giải ảnh tương ứng với kích thước màn hình và DPI của thiết bị.",
            "Cumulative Layout Shift Elimination: Luôn khai báo `width` và `height` rõ ràng để trình duyệt đặt chỗ trước tỷ lệ khung hình (Aspect Ratio)."
        ],
        "steps": [
            "Tự động nén ảnh gốc sang các định dạng AVIF và WebP với mức chất lượng tối ưu (Quality 75-80).",
            "Sinh mã chuỗi Blurhash siêu nhẹ (dưới 30 byte) để hiển thị nền mờ trong lúc ảnh nét đang tải về.",
            "Bọc hình ảnh trong thẻ `<picture>` với đầy đủ các thẻ `<source type='image/avif'>` và `sizes` chính xác.",
            "Thêm thuộc tính `fetchpriority='high'` cho ảnh LCP đầu trang và `loading='lazy'` cho các ảnh phía dưới màn hình cuộn.",
            "Kiểm tra chỉ số Core Web Vitals trên PageSpeed Insights."
        ],
        "code_lang": "html",
        "code_example": """<!-- High-Performance Responsive Picture Pipeline -->
<picture>
  <source srcset="banner-384.avif 384w, banner-768.avif 768w, banner-1200.avif 1200w"
          type="image/avif" sizes="(max-width: 768px) 100vw, 1200px">
  <source srcset="banner-384.webp 384w, banner-768.webp 768w, banner-1200.webp 1200w"
          type="image/webp" sizes="(max-width: 768px) 100vw, 1200px">
  <img src="banner-768.jpg" width="1200" height="675" alt="Summer Promo"
       fetchpriority="high" decoding="async" class="object-cover w-full h-auto">
</picture>""",
        "antipatterns": [
            "Tải một bức ảnh gốc độ phân giải 4000x3000px nặng 8MB rồi dùng CSS co lại thành kích thước hiển thị 300x200px trên điện thoại.",
            "Dùng `loading='lazy'` cho cả bức ảnh banner chính trên cùng làm chậm chỉ số LCP nghiêm trọng.",
            "Không khai báo thuộc tính `width` và `height` trên thẻ `<img>` gây giật nảy giao diện khi ảnh tải xong (lỗi CLS)."
        ],
        "quality_gates": [
            "QG-01: Tổng dung lượng hình ảnh trên trang chủ giảm tối thiểu 60% sau khi áp dụng pipeline nén.",
            "QG-02: Điểm chỉ số LCP đạt mức 'Good' (<2.5s) trên thiết bị di động kết nối mạng 4G tiêu chuẩn.",
            "QG-03: Chỉ số CLS (Cumulative Layout Shift) duy trì bằng 0 liên quan đến việc nạp ảnh."
        ],
        "security": "Lọc bỏ toàn bộ siêu dữ liệu EXIF nhạy cảm (tọa độ GPS, thông tin máy ảnh) khỏi ảnh tải lên của người dùng trước khi xuất bản ra CDN.",
        "deliverables": [
            "Script tự động nén và tạo srcset hình ảnh `optimize-media.js`.",
            "Component React/Vue chuẩn `ResponsiveImage` tích hợp Blurhash."
        ],
        "related": ["dex-frontend-performance", "dex-caching-strategies", "dex-storage-lifecycle"],
        "scenario": "Trang sản phẩm thời trang có tốc độ tải trang chậm do mỗi sản phẩm tải ảnh JPEG 2MB. Sử dụng `dex-media-delivery-pipelines` để tự động chuyển đổi toàn bộ thư viện ảnh sang AVIF/WebP qua CDN, giảm kích thước trung bình xuống 120KB và cải thiện chỉ số LCP từ 5.4s xuống 1.8s."
    },
    {
        "id": "dex-hls-dash-playback",
        "index": 213,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Architect resilient HTTP Live Streaming (HLS) and MPEG-DASH adaptive bitrate playback engines with automated buffer stall recovery, multi-track audio, and WebVTT captions. Use when implementing custom video players, live streaming feeds, or multimedia learning platforms.",
        "purpose": "Thiết kế kiến trúc trình phát đa phương tiện phát sóng thích ứng (Adaptive Bitrate Streaming) chuẩn HLS và MPEG-DASH; tích hợp cơ chế tự động phục hồi khi nghẽn đệm dữ liệu (Buffer Stall Recovery), chuyển đổi luồng âm thanh đa ngôn ngữ và đồng bộ phụ đề WebVTT mượt mà.",
        "when_use": [
            "Khi xây dựng trình phát video trực tiếp (Live Stream) hoặc video theo yêu cầu (VOD) chất lượng cao.",
            "Khi người dùng gặp hiện tượng video dừng hình liên tục do tốc độ mạng không ổn định.",
            "Khi triển khai nền tảng học trực tuyến có yêu cầu phụ đề đa ngôn ngữ và chuyển đổi chất lượng động."
        ],
        "when_not_use": [
            "Khi chỉ phát một đoạn video nền (background video) ngắn 3 giây dạng MP4 lặp đi lặp lại.",
            "Khi truyền nhận âm thanh thoại thời gian thực hai chiều có độ trễ cực thấp (<200ms) - nên dùng WebRTC."
        ],
        "prereqs": "Tệp manifest HLS (.m3u8) hoặc DASH (.mpd), thư viện player (Hls.js hoặc Shaka Player), phần cứng giải mã Media Source Extensions (MSE).",
        "concepts": [
            "Adaptive Bitrate (ABR): Tự động đo lường băng thông mạng tức thời và điều chỉnh độ phân giải phân đoạn video (segment) tiếp theo.",
            "Buffer Management: Duy trì khoảng đệm an toàn (Buffer Ahead 30s) và dọn dẹp bộ đệm đã xem để chống tràn bộ nhớ RAM.",
            "Live Edge Synchronization: Điều chỉnh tốc độ phát nhẹ (1.05x hoặc 0.95x) để giữ khoảng cách với luồng trực tiếp mà không gây giật tiếng."
        ],
        "steps": [
            "Kiểm tra hỗ trợ Media Source Extensions (MSE) hoặc trình phát HLS gốc của trình duyệt.",
            "Khởi tạo thực thể Hls.js với cấu hình giới hạn kích thước buffer tối đa.",
            "Lắng nghe sự kiện lỗi mạng và lỗi giải mã để thực thi chiến lược hồi phục tự động (Stall Recovery Algorithm).",
            "Đăng ký danh sách phụ đề WebVTT và thiết lập giao diện tùy chỉnh cho phép người dùng chuyển track.",
            "Kiểm tra chuyển đổi độ phân giải mượt mà khi giả lập thay đổi tốc độ mạng từ 10Mbps xuống 1Mbps."
        ],
        "code_lang": "typescript",
        "code_example": """import Hls from 'hls.js';

export function initializePlayer(videoElement: HTMLVideoElement, streamUrl: string) {
  if (Hls.isSupported()) {
    const hls = new Hls({
      maxBufferLength: 30,
      maxMaxBufferLength: 60,
      enableWorker: true,
      lowLatencyMode: true
    });
    
    hls.loadSource(streamUrl);
    hls.attachMedia(videoElement);
    
    hls.on(Hls.Events.ERROR, (event, data) => {
      if (data.fatal) {
        switch (data.type) {
          case Hls.ErrorTypes.NETWORK_ERROR:
            hls.startLoad();
            break;
          case Hls.ErrorTypes.MEDIA_ERROR:
            hls.recoverMediaError();
            break;
          default:
            hls.destroy();
            break;
        }
      }
    });
    return hls;
  }
}""",
        "antipatterns": [
            "Để kích thước buffer video quá lớn khiến trình duyệt di động bị crash do tràn bộ nhớ (Out of Memory).",
            "Không xử lý các lỗi nghiêm trọng (`fatal errors`) làm video bị đứng hình vĩnh viễn khi mạng rớt gói tin.",
            "Tự động ép phát ở chất lượng cao nhất 4K ngay từ giây đầu tiên mà không đợi đo lường băng thông thực tế."
        ],
        "quality_gates": [
            "QG-01: Tỷ lệ dừng hình (Stall Rate) dưới 0.5% tổng thời gian phát trong điều kiện mạng biến động.",
            "QG-02: Thời gian bắt đầu phát video (Time-to-First-Frame) dưới 1.2 giây.",
            "QG-03: Tự động phục hồi thành công sau khi ngắt kết nối mạng giả lập 3 giây."
        ],
        "security": "Bảo vệ bản quyền nội dung bằng cách xác thực token chữ ký trên từng phân đoạn video (Encrypted HLS / DRM Integration).",
        "deliverables": [
            "Module trình phát video đa thích ứng `AdaptiveVideoPlayer.ts`.",
            "Chiến lược xử lý lỗi buffer và phục hồi luồng dữ liệu tự động."
        ],
        "related": ["dex-media-delivery-pipelines", "dex-frontend-error-recovery", "dex-realtime-protocols"],
        "scenario": "Xây dựng cổng truyền hình trực tiếp cho sự kiện thể thao. Sử dụng `dex-hls-dash-playback` để tích hợp trình phát HLS có cơ chế tự động hạ chất lượng xuống 480p khi người dùng vào vùng sóng yếu và tăng lại 1080p khi mạng ổn định, không để xảy ra hiện tượng đứng hình giữa trận đấu."
    },
    {
        "id": "dex-progressive-web-apps",
        "index": 214,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Engineer installable Progressive Web Apps (PWA) with Workbox offline caching strategies, background sync, Web App Manifests, service worker lifecycle governance, and seamless app updates. Use when building offline-capable web apps, mobile-friendly portals, or desktop web apps.",
        "purpose": "Xây dựng ứng dụng web lũy tiến (Progressive Web Apps - PWA) chuẩn công nghiệp có khả năng cài đặt như ứng dụng native; quản trị vòng đời Service Worker, thiết lập chiến lược lưu trữ bộ nhớ đệm ngoại tuyến (Offline Caching) qua Workbox, đồng bộ nền (Background Sync) và thông báo cập nhật phiên bản mượt mà.",
        "when_use": [
            "Khi ứng dụng cần hoạt động ổn định kể cả khi mất kết nối Internet hoàn toàn (Offline-first experience).",
            "Khi muốn cung cấp trải nghiệm cài đặt lên màn hình chính (Home Screen) của điện thoại và máy tính mà không cần thông qua App Store.",
            "Khi cần tăng tốc độ tải trang tức thì cho các lần truy cập tiếp theo thông qua cache service worker."
        ],
        "when_not_use": [
            "Khi ứng dụng yêu cầu các API phần cứng đặc thù mà trình duyệt không hỗ trợ (ví dụ can thiệp sâu hệ điều hành).",
            "Khi website chỉ là một trang tin tức tĩnh đơn giản cập nhật liên tục nội dung mới mà không cần cài đặt."
        ],
        "prereqs": "Môi trường kết nối bảo mật HTTPS, Web App Manifest (`manifest.json`), kiến thức về vòng đời Service Worker.",
        "concepts": [
            "Service Worker Lifecycle: Install -> Waiting -> Activate. Quản lý việc cập nhật phiên bản mà không làm gián đoạn phiên làm việc của người dùng.",
            "Caching Strategies: Stale-While-Revalidate cho tài nguyên thường xuyên thay đổi, Cache-First cho font và ảnh tĩnh, Network-First cho dữ liệu API quan trọng.",
            "Background Synchronization: Tự động lưu các hành động gửi dữ liệu khi mất mạng vào IndexedDB và gửi lại khi có mạng."
        ],
        "steps": [
            "Tạo tệp `manifest.webmanifest` chuẩn với đầy đủ icons, theme_color và display: standalone.",
            "Đăng ký Service Worker và tích hợp Workbox để định nghĩa các chiến lược bộ nhớ đệm.",
            "Thiết lập giao diện thông báo 'Đã có phiên bản mới, bấm để tải lại' (Skip Waiting Prompt).",
            "Xây dựng trang dự phòng khi ngoại tuyến (`offline.html`) cung cấp hướng dẫn cho người dùng.",
            "Kiểm tra ứng dụng vượt qua 100% tiêu chí PWA trong công cụ Google Lighthouse."
        ],
        "code_lang": "javascript",
        "code_example": """// Service Worker with Workbox Stale-While-Revalidate
import { registerRoute } from 'workbox-routing';
import { StaleWhileRevalidate, CacheFirst } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

// Cache Google Fonts with CacheFirst
registerRoute(
  ({ url }) => url.origin === 'https://fonts.googleapis.com',
  new CacheFirst({
    cacheName: 'google-fonts-cache',
    plugins: [new ExpirationPlugin({ maxEntries: 20, maxAgeSeconds: 365 * 24 * 60 * 60 })]
  })
);

// Cache API Requests with StaleWhileRevalidate
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/dashboard'),
  new StaleWhileRevalidate({
    cacheName: 'api-dashboard-cache',
    plugins: [new ExpirationPlugin({ maxEntries: 50, maxAgeSeconds: 5 * 60 })]
  })
);""",
        "antipatterns": [
            "Lưu cache API vĩnh viễn mà không có thời hạn hết hạn (Expiration Policy) khiến người dùng thấy dữ liệu cũ suốt đời.",
            "Tự động gọi `self.skipWaiting()` ngay lập tức trong nền làm tải lại trang bất ngờ khi người dùng đang nhập dữ liệu dở.",
            "Không cung cấp trang offline fallback khiến ứng dụng hiện màn hình lỗi khủng long của trình duyệt."
        ],
        "quality_gates": [
            "QG-01: Điểm PWA trên Google Lighthouse đạt 100/100.",
            "QG-02: Ứng dụng tải được giao diện cơ sở (App Shell) hoàn chỉnh trong chế độ máy bay (Airplane Mode).",
            "QG-03: Có thông báo xác nhận cập nhật phiên bản mới một cách minh bạch."
        ],
        "security": "Chỉ chạy Service Worker trên giao thức HTTPS; thiết lập phạm vi điều khiển (scope) chính xác để ngăn chặn việc đánh chặn tài nguyên trái phép.",
        "deliverables": [
            "Tệp cấu hình Web App Manifest `manifest.webmanifest`.",
            "Kịch bản Service Worker chuẩn `sw.ts` tích hợp Workbox.",
            "Component React thông báo cập nhật ứng dụng `ReloadPrompt.tsx`."
        ],
        "related": ["dex-mobile-offline-sync", "dex-caching-strategies", "dex-web-push-permission-flow"],
        "scenario": "Phát triển ứng dụng ghi chú cho kỹ sư công trường nơi sóng di động chập chờn. Kỹ sư kích hoạt `dex-progressive-web-apps` để biến website thành PWA có thể cài đặt lên điện thoại, lưu toàn bộ ghi chú vào IndexedDB khi mất mạng và tự động đồng bộ lên máy chủ ngay khi có 4G trở lại."
    },
    {
        "id": "dex-web-push-permission-flow",
        "index": 215,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Design high-conversion, contextual Web Push notification permission request flows, VAPID key authentication, and graceful push message delivery with fallback notification badges. Use when implementing user notifications, engagement alerts, or real-time web messaging.",
        "purpose": "Thiết kế luồng yêu cầu quyền nhận thông báo đẩy web (Web Push Notification Permission) theo ngữ cảnh với tỷ lệ chấp thuận cao; thiết lập cơ chế xác thực khóa VAPID an toàn, quản lý vòng đời đăng ký PushSubscription và xử lý thông điệp đẩy nền kèm biểu tượng chỉ báo số lượng.",
        "when_use": [
            "Khi triển khai tính năng gửi thông báo tức thời cho người dùng trên trình duyệt máy tính và điện thoại.",
            "Khi muốn cải thiện tỷ lệ người dùng bấm 'Cho phép' nhận thông báo thay vì bấm 'Chặn' do bị hỏi quá đột ngột.",
            "Khi cần cấu hình bảo mật truyền tin giữa máy chủ ứng dụng và dịch vụ Push Service của trình duyệt."
        ],
        "when_not_use": [
            "Khi người dùng chỉ cần nhận thông báo qua email hoặc tin nhắn SMS.",
            "Khi ứng dụng đang trong môi trường phát triển cục bộ không có kết nối HTTPS."
        ],
        "prereqs": "Cặp khóa định danh VAPID (Public/Private Key), quyền HTTPS, Service Worker đã được đăng ký thành công.",
        "concepts": [
            "Contextual Pre-Permission Primer: Hiển thị một modal giải thích lý do trước khi kích hoạt hộp thoại xin quyền mặc định của trình duyệt.",
            "VAPID (Voluntary Application Server Identification): Khóa ký điện tử xác thực máy chủ gửi tin nhắn với dịch vụ thông báo đẩy.",
            "Notification Action Buttons: Đính kèm các nút thao tác nhanh (như 'Xem chi tiết', 'Bỏ qua') ngay trên thông báo hệ thống."
        ],
        "steps": [
            "Tạo cặp khóa VAPID an toàn trên máy chủ backend.",
            "Xác định thời điểm vàng để xin quyền (ví dụ: ngay sau khi người dùng bấm 'Theo dõi đơn hàng').",
            "Hiển thị giao diện giải thích giá trị của việc nhận thông báo (Soft Ask Prompt).",
            "Khi người dùng đồng ý, gọi API `Notification.requestPermission()` và chuyển đổi `pushManager.subscribe()`.",
            "Gửi đối tượng `PushSubscription` lên máy chủ backend để lưu vào cơ sở dữ liệu."
        ],
        "code_lang": "typescript",
        "code_example": """// Contextual Push Permission Subscription
export async function subscribeUserToPush(publicVapidKey: string) {
  const registration = await navigator.serviceWorker.ready;
  
  // Convert URL base64 to Uint8Array for applicationServerKey
  const convertedVapidKey = urlBase64ToUint8Array(publicVapidKey);
  
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: convertedVapidKey
  });
  
  // Send subscription object to backend server
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription)
  });
  return subscription;
}""",
        "antipatterns": [
            "Bắn pop-up xin quyền thông báo ngay ở mili-giây đầu tiên khi người dùng vừa đặt chân vào trang web.",
            "Gửi các thông báo rác tiếp thị với tần suất dày đặc khiến người dùng vào cài đặt trình duyệt chặn hoàn toàn quyền của trang.",
            "Không xử lý trường hợp người dùng chọn 'Từ chối' (Denied), dẫn đến việc liên tục hiển thị lại nhắc nhở gây khó chịu."
        ],
        "quality_gates": [
            "QG-01: Tỷ lệ chấp nhận quyền thông báo tăng tối thiểu 35% so với việc xin quyền thô không có giao diện đệm.",
            "QG-02: Khóa riêng VAPID Private Key được lưu trữ an toàn trong Secret Manager, không bị lộ ra frontend.",
            "QG-03: Thông báo hiển thị đúng tiêu đề, nội dung và icon đại diện trên cả Windows, macOS và Android."
        ],
        "security": "Bảo vệ thông điệp đẩy bằng mã hóa payload tiêu chuẩn RFC 8291; không gửi các dữ liệu nhạy cảm cá nhân trong nội dung thông báo thô.",
        "deliverables": [
            "Module kích hoạt quyền thông báo theo ngữ cảnh `PushPermissionManager.ts`.",
            "Kịch bản Service Worker lắng nghe sự kiện push `sw-push-handler.js`."
        ],
        "related": ["dex-notification-delivery", "dex-progressive-web-apps", "dex-user-consent-ux"],
        "scenario": "Trang web đặt đồ ăn trực tuyến muốn thông báo trạng thái tài xế cho khách hàng. Áp dụng `dex-web-push-permission-flow` để chỉ hiển thị hộp thoại xin quyền sau khi đơn hàng được thanh toán thành công, giải thích rõ 'Bật thông báo để biết khi nào tài xế tới', giúp nâng tỷ lệ cấp quyền từ 12% lên 68%."
    },
    {
        "id": "dex-search-interface-experience",
        "index": 216,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Architect accessible, instant search interfaces with debounced typeahead suggestions, faceted multi-attribute filters, keyboard navigation (combobox pattern), and empty search recovery. Use when building e-commerce catalogs, knowledge bases, or document search portals.",
        "purpose": "Thiết kế kiến trúc giao diện tìm kiếm tức thì (Instant Search) có độ tiếp cận cao theo chuẩn WAI-ARIA Combobox Pattern; tích hợp cơ chế chống rung phím (Debounced Typeahead), bộ lọc đa thuộc tính (Faceted Filtering), điều hướng hoàn toàn bằng bàn phím và khả năng phục hồi gợi ý khi không tìm thấy kết quả.",
        "when_use": [
            "Khi xây dựng thanh tìm kiếm trung tâm cho ứng dụng tài liệu kỹ thuật hoặc kho sản phẩm thương mại điện tử.",
            "Khi người dùng gặp khó khăn trong việc tìm kiếm thông tin do giao diện không có gợi ý từ khóa.",
            "Khi cần tối ưu hóa trải nghiệm điều hướng bằng bàn phím (`ArrowUp`, `ArrowDown`, `Enter`, `Escape`)."
        ],
        "when_not_use": [
            "Khi chỉ lọc danh sách dữ liệu nhỏ dưới 10 phần tử đã có sẵn trên RAM.",
            "Khi xây dựng các câu lệnh truy vấn nội bộ của database dưới backend."
        ],
        "prereqs": "Endpoint API tìm kiếm hỗ trợ phân trang và từ khóa, danh mục các trường dữ liệu cần lọc (facets).",
        "concepts": [
            "Debounced Input: Trì hoãn việc gửi request API tìm kiếm từ 250ms đến 300ms sau khi người dùng ngừng gõ phím.",
            "WAI-ARIA Combobox Pattern: Quản lý thuộc tính `aria-expanded`, `aria-activedescendant` và `aria-controls` đúng tiêu chuẩn trợ năng.",
            "Zero-Result Recovery: Khi không có kết quả, cung cấp từ khóa gợi ý gần đúng (Did you mean?), các tìm kiếm phổ biến hoặc gợi ý xóa bớt bộ lọc."
        ],
        "steps": [
            "Xây dựng ô nhập liệu tìm kiếm với icon xóa nhanh và trạng thái loading trực quan.",
            "Bọc logic nhập liệu bằng hàm debounce để giảm tải 80% số lượng request lên máy chủ.",
            "Hiện thực hóa danh sách dropdown gợi ý với các phần tử có thể highlight từ khóa tìm kiếm.",
            "Lắng nghe sự kiện bàn phím để di chuyển vệt chọn lên xuống và phím Escape để đóng nhanh menu.",
            "Xây dựng trạng thái Empty State thông minh khi kết quả trả về bằng 0."
        ],
        "code_lang": "typescript",
        "code_example": """// Debounced Search Hook Pattern
import { useState, useEffect } from 'react';

export function useDebouncedSearch(query: string, delayMs = 300) {
  const [debouncedValue, setDebouncedValue] = useState(query);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(query.trim());
    }, delayMs);

    return () => clearTimeout(handler);
  }, [query, delayMs]);

  return debouncedValue;
}""",
        "antipatterns": [
            "Gửi request tìm kiếm sau từng ký tự được gõ mà không có debounce làm nghẽn server và xung đột thứ tự kết quả trả về.",
            "Bẫy tiêu điểm (Focus Trap) khiến người dùng bàn phím không thể nhấn Tab để thoát ra khỏi thanh tìm kiếm.",
            "Chỉ hiển thị dòng chữ cụt lủn 'Không tìm thấy kết quả' mà không đưa ra bất kỳ hướng dẫn hay gợi ý thay thế nào."
        ],
        "quality_gates": [
            "QG-01: Tuân thủ 100% tiêu chuẩn WAI-ARIA 1.2 cho Combobox Pattern.",
            "QG-02: Độ trễ phản hồi gợi ý giao diện dưới 150ms sau khi nhận được dữ liệu từ API.",
            "QG-03: Người dùng có thể hoàn thành toàn bộ chu trình tìm kiếm và chọn kết quả mà không cần chạm vào chuột máy tính."
        ],
        "security": "Khử nhiễm (Sanitize) toàn bộ chuỗi tìm kiếm trước khi render vào DOM để triệt tiêu lỗ hổng Cross-Site Scripting (XSS).",
        "deliverables": [
            "Component tìm kiếm thông minh `InstantSearchCombobox.tsx`.",
            "Bộ test tự động kiểm tra điều hướng bằng bàn phím với Playwright."
        ],
        "related": ["dex-search-engineering", "dex-ux-accessibility", "dex-ui-component-contracts"],
        "scenario": "Xây dựng cổng tài liệu nội bộ với 5,000 bài viết. Kỹ sư kích hoạt `dex-search-interface-experience` để thiết kế hộp tìm kiếm dạng Spotlight (tương tự macOS Cmd+K), hỗ trợ lọc theo danh mục, điều hướng phím mũi tên mượt mà và gợi ý từ khóa liên quan khi gõ sai chính tả."
    },
    {
        "id": "dex-virtualized-infinite-lists",
        "index": 217,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Implement high-performance windowed list virtualization (TanStack Virtual, react-window) supporting dynamic row heights, scroll restoration, sticky headers, and stable infinite paging. Use when rendering feeds with 10,000+ items, large data tables, or chat message logs.",
        "purpose": "Hiện thực hóa danh sách ảo hóa (List Virtualization / Windowing) hiệu năng cao cho dữ liệu cực lớn (10,000+ phần tử); chỉ dựng các nút DOM thực tế nằm trong khung nhìn hiển thị (Viewport), hỗ trợ chiều cao hàng động, khôi phục vị trí cuộn chuột và phân trang vô tận mượt mà.",
        "when_use": [
            "Khi ứng dụng phải hiển thị danh sách lớn dữ liệu (bảng giao dịch tài chính, nhật ký log, tin nhắn chat).",
            "Khi trang web bị đơ, giật hoặc tiêu tốn hàng trăm megabyte RAM do tạo ra quá nhiều DOM nodes.",
            "Khi cuộn qua danh sách dài bị giật khung hình và rớt FPS nghiêm trọng."
        ],
        "when_not_use": [
            "Khi danh sách dữ liệu cố định dưới 100 phần tử đơn giản.",
            "Khi cần in ấn toàn bộ nội dung trang ra giấy (Print Stylesheet)."
        ],
        "prereqs": "Kích thước khung chứa danh sách, hàm lấy dữ liệu phân trang, thư viện ảo hóa mục tiêu (TanStack Virtual hoặc react-window).",
        "concepts": [
            "Windowing Concept: Chỉ tạo ra từ 10 đến 20 DOM nodes thực tế cho các phần tử nhìn thấy được, dịch chuyển vị trí bằng `transform: translateY()`.",
            "Overscan Padding: Dựng trước thêm một số phần tử ở phía trên và phía dưới khung nhìn để người dùng không thấy khoảng trắng khi cuộn nhanh.",
            "Dynamic Size Measurement: Tự động đo lường và cập nhật chiều cao thực tế của các hàng có nội dung co giãn linh hoạt."
        ],
        "steps": [
            "Bọc danh sách trong một thẻ container có thanh cuộn với thuộc tính `overflow-y: auto`.",
            "Khởi tạo Virtualizer với số lượng phần tử tổng và hàm ước tính chiều cao ban đầu.",
            "Áp dụng vị trí tuyệt đối (`position: absolute`) và `transform` cho từng hàng được ảo hóa.",
            "Lắng nghe sự kiện cuộn để kích hoạt tải thêm trang mới khi người dùng cuộn gần tới đáy danh sách.",
            "Kiểm tra mức độ tiêu thụ RAM của trình duyệt trong quá trình cuộn liên tục."
        ],
        "code_lang": "typescript",
        "code_example": """import { useVirtualizer } from '@tanstack/react-virtual';
import React, { useRef } from 'react';

export function VirtualizedList({ items }: { items: string[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const rowVirtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48,
    overscan: 5,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflowY: 'auto', position: 'relative' }}>
      <div style={{ height: `${rowVirtualizer.getTotalSize()}px`, width: '100%', position: 'relative' }}>
        {rowVirtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`
            }}
          >
            {items[virtualRow.index]}
          </div>
        ))}
      </div>
    </div>
  );
}""",
        "antipatterns": [
            "Render trực tiếp 20,000 thẻ `div` vào DOM cùng lúc khiến trình duyệt đơ trong vài giây.",
            "Thiết lập giá trị `overscan` quá lớn làm mất đi lợi ích giảm tải DOM của kỹ thuật ảo hóa.",
            "Quên khai báo thuộc tính `position: relative` ở thẻ cha khiến các phần tử con bị nhảy loạn xạ vị trí."
        ],
        "quality_gates": [
            "QG-01: Số lượng phần tử DOM trong trang không vượt quá 50 nodes bất kể danh sách có 100,000 bản ghi.",
            "QG-02: Tốc độ cuộn chuột duy trì ổn định ở mức 60fps mà không xuất hiện khoảng trắng nhấp nháy.",
            "QG-03: Khôi phục chính xác vị trí cuộn khi người dùng quay lại từ trang chi tiết."
        ],
        "security": "Đảm bảo các dữ liệu được render động trong danh sách ảo hóa đều được escape cẩn thận, ngăn ngừa tấn công XSS qua dữ liệu mảng.",
        "deliverables": [
            "Component danh sách ảo hóa tái sử dụng `VirtualizedDataTable.tsx`.",
            "Tài liệu hướng dẫn xử lý chiều cao hàng co giãn động."
        ],
        "related": ["dex-frontend-performance", "dex-ui-component-contracts", "dex-layout-composition-patterns"],
        "scenario": "Xây dựng màn hình xem nhật ký hệ thống máy chủ (Log Viewer) hiển thị 50,000 dòng log theo thời gian thực. Áp dụng `dex-virtualized-infinite-lists` để chỉ giữ lại 30 dòng trong DOM, giảm 95% mức sử dụng bộ nhớ và giúp việc tìm kiếm log diễn ra mượt mà không bị treo tab trình duyệt."
    },
    {
        "id": "dex-web-canvas-rendering",
        "index": 218,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Engineer interactive, high-DPI HTML5 2D Canvas interfaces with dirty-rectangle redraw optimizations, spatial indexing (quadtrees), pan-zoom transformations, and pointer hit detection. Use when building interactive whiteboards, flowchart editors, or custom data visualizations.",
        "purpose": "Thiết kế và xây dựng giao diện đồ họa tương tác trên nền tảng HTML5 2D Canvas; hỗ trợ tối ưu độ phân giải cao (Retina / High-DPI screens), cơ chế vẽ lại vùng thay đổi (Dirty-Rectangle Redraw), cấu trúc dữ liệu không gian Quadtree để phát hiện va chạm con trỏ và ma trận biến đổi tọa độ pan-zoom mượt mà.",
        "when_use": [
            "Khi xây dựng bảng vẽ tương tác (Online Whiteboard), công cụ vẽ sơ đồ hoặc game 2D trên web.",
            "Khi số lượng phần tử đồ họa vượt quá khả năng xử lý của thẻ SVG hoặc DOM thông thường (>3,000 objects).",
            "Khi cần điều khiển từng pixel màu sắc và hiệu ứng ánh sáng đồ họa tùy biến."
        ],
        "when_not_use": [
            "Khi giao diện chỉ bao gồm các form nhập liệu, danh sách và văn bản thông thường.",
            "Khi cần hỗ trợ đầy đủ các tính năng trợ năng màn hình (Screen Reader) một cách tự nhiên mà không muốn giả lập ARIA."
        ],
        "prereqs": "Ngữ cảnh đồ họa `HTMLCanvasElement.getContext('2d')`, toán học vector và ma trận biến đổi không gian 2D.",
        "concepts": [
            "Device Pixel Ratio (DPR) Scaling: Nhân đôi kích thước bộ đệm canvas theo `window.devicePixelRatio` và co lại bằng CSS để triệt tiêu hiện tượng mờ chữ trên màn hình Retina.",
            "Quadtree Spatial Partitioning: Phân hoạch không gian thành cây 4 góc để tra cứu phần tử được bấm trúng (Hit Testing) với độ phức tạp $O(\\log N)$.",
            "Dirty Rectangle Redraw: Chỉ xóa và vẽ lại khu vực có phần tử di chuyển thay vì vẽ lại toàn bộ khung tranh (`clearRect` toàn màn hình)."
        ],
        "steps": [
            "Khởi tạo canvas và hiệu chuẩn kích thước theo tỷ lệ DPR của màn hình thiết bị.",
            "Thiết lập vòng lặp kết xuất đồ họa (Render Loop) sử dụng `requestAnimationFrame`.",
            "Xây dựng ma trận biến đổi tọa độ (View Matrix) hỗ trợ thao tác kéo (Pan) và thu phóng (Zoom).",
            "Đưa các thực thể hình học vào cây không gian Quadtree.",
            "Lắng nghe sự kiện chuột/cảm ứng, chuyển đổi tọa độ màn hình sang tọa độ thế giới canvas để kiểm tra va chạm."
        ],
        "code_lang": "typescript",
        "code_example": """// High-DPI Canvas Scaling Pattern
export function setupHighDpiCanvas(canvas: HTMLCanvasElement, width: number, height: number) {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;

  const ctx = canvas.getContext('2d');
  if (ctx) {
    ctx.scale(dpr, dpr);
  }
  return ctx;
}""",
        "antipatterns": [
            "Không hiệu chuẩn theo `devicePixelRatio` khiến nét vẽ trên màn hình điện thoại và MacBook bị nhòe mờ như ảnh nén chất lượng thấp.",
            "Dùng vòng lặp kiểm tra va chạm tuần tự $O(N)$ trên 10,000 vật thể khi di chuyển chuột khiến FPS sụt giảm thê thảm.",
            "Tạo mới đối tượng hoặc mảng trong mỗi khung hình render loop gây kích hoạt dọn rác (Garbage Collection) liên tục làm giật hình."
        ],
        "quality_gates": [
            "QG-01: Hình ảnh và văn bản trên Canvas hiển thị sắc nét trên cả màn hình chuẩn 1x và Retina 2x/3x.",
            "QG-02: Duy trì tốc độ khung hình 60fps khi tương tác kéo thả với tối thiểu 5,000 vật thể độc lập.",
            "QG-03: Độ chính xác phát hiện bấm trúng điểm ảnh (Hit-test accuracy) đạt tuyệt đối."
        ],
        "security": "Xử lý cẩn thận phương thức `toDataURL()` hoặc `getImageData()` khi vẽ ảnh từ domain khác để tránh lỗi ô nhiễm Canvas (Tainted Canvas CORS error).",
        "deliverables": [
            "Lớp quản lý tương tác Canvas `CanvasEngine2D.ts`.",
            "Module cấu trúc dữ liệu không gian `QuadtreeSpatialIndex.ts`."
        ],
        "related": ["dex-webgpu-rendering-fundamentals", "dex-simulation-determinism", "dex-frontend-performance"],
        "scenario": "Phát triển công cụ chỉnh sửa sơ đồ mạng lưới hạ tầng đám mây. Kỹ sư kích hoạt `dex-web-canvas-rendering` để vẽ hơn 8,000 node máy chủ, sử dụng Quadtree để hỗ trợ chọn và nối dây giữa các node với tốc độ 60fps mượt mà, không gặp hiện tượng trễ chuột."
    },
    {
        "id": "dex-webgpu-rendering-fundamentals",
        "index": 219,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Design safe, high-performance WebGPU rendering pipelines, WGSL shader compilations, memory buffer lifecycle management, and device-loss recovery with WebGL2 fallback. Use when implementing compute shaders in the browser, 3D product visualizers, or high-throughput visualization.",
        "purpose": "Thiết kế và triển khai đường ống kết xuất đồ họa và tính toán song song thế hệ mới trên WebGPU; lập trình shader ngôn ngữ WGSL, quản trị vòng đời bộ nhớ đệm (GPU Buffers), cơ chế tự phục hồi khi mất thiết bị (Device Loss Recovery) và phương án dự phòng WebGL2 tương thích ngược.",
        "when_use": [
            "Khi xây dựng các ứng dụng đồ họa 3D phức tạp, mô phỏng vật lý hạt hoặc tính toán AI/Machine Learning trực tiếp trên trình duyệt.",
            "Khi ứng dụng gặp giới hạn nghẽn cổ chai của WebGL do chi phí gọi lệnh vẽ (Draw Call Overhead) quá lớn.",
            "Khi cần tận dụng Compute Shaders để xử lý song song khối lượng dữ liệu khổng lồ trên GPU."
        ],
        "when_not_use": [
            "Khi ứng dụng chỉ hiển thị các bảng dữ liệu HTML hoặc biểu đồ kinh doanh thông thường.",
            "Khi trình duyệt của đối tượng khách hàng mục tiêu là các trình duyệt đời cũ chưa bật WebGPU."
        ],
        "prereqs": "Trình duyệt hỗ trợ WebGPU (`navigator.gpu`), card đồ họa hỗ trợ DirectX 12 / Metal / Vulkan, kiến thức về ngôn ngữ shader WGSL.",
        "concepts": [
            "Pipeline State Object (PSO): Đóng gói toàn bộ cấu hình shader, định dạng đỉnh và trạng thái blend thành đối tượng bất biến để tối ưu tốc độ thực thi trên GPU.",
            "Command Buffer Recording: Ghi lại danh sách các lệnh vẽ độc lập ngoài luồng trước khi gửi hàng loạt xuống hàng đợi `gpuQueue`.",
            "Device Loss Handling: Bắt sự kiện thiết bị GPU bị ngắt (do sleep, chuyển card màn hình) để khởi tạo lại tài nguyên mà không làm sập ứng dụng."
        ],
        "steps": [
            "Kiểm tra hỗ trợ `navigator.gpu` và yêu cầu `GPUAdapter` cùng `GPUDevice`.",
            "Viết và biên dịch mã nguồn Shader ngôn ngữ WGSL cho Vertex, Fragment hoặc Compute stage.",
            "Khởi tạo các bộ đệm `GPUBuffer` chứa tọa độ đỉnh và ma trận đồng nhất (Uniforms).",
            "Tạo Render Pipeline và cấu hình Bind Group liên kết bộ nhớ đệm với shader.",
            "Thiết lập cơ chế bắt lỗi `device.lost` để tái tạo tài nguyên và kích hoạt WebGL2 fallback nếu không thể khôi phục."
        ],
        "code_lang": "typescript",
        "code_example": """// Basic WebGPU Initialization & Pipeline
export async function initWebGPU(canvas: HTMLCanvasElement) {
  if (!navigator.gpu) throw new Error('WebGPU is not supported');
  
  const adapter = await navigator.gpu.requestAdapter();
  if (!adapter) throw new Error('No appropriate GPUAdapter found');
  
  const device = await adapter.requestDevice();
  const context = canvas.getContext('webgpu') as GPUCanvasContext;
  const presentationFormat = navigator.gpu.getPreferredCanvasFormat();
  
  context.configure({
    device,
    format: presentationFormat,
    alphaMode: 'premultiplied',
  });
  
  // Listen for device loss
  device.lost.then(info => {
    console.warn(`GPU Device lost: ${info.reason}`, info.message);
  });
  
  return { device, context, presentationFormat };
}""",
        "antipatterns": [
            "Tạo mới `GPURenderPipeline` hoặc nạp lại shader trong mỗi khung hình khiến GPU bị giật nghiêm trọng.",
            "Không giải phóng bộ nhớ `buffer.destroy()` khi hủy bỏ đối tượng đồ họa dẫn đến tràn bộ nhớ VRAM card màn hình.",
            "Giả định mọi máy khách đều có WebGPU mà không chuẩn bị giải pháp dự phòng WebGL2."
        ],
        "quality_gates": [
            "QG-01: Khởi tạo WebGPU pipeline thành công không có lỗi biên dịch WGSL shader trong console.",
            "QG-02: Ứng dụng tự động phục hồi hoặc thông báo nhẹ nhàng khi GPU bị mất thiết bị (Device Lost event).",
            "QG-03: Có sẵn module fallback sang WebGL2 khi `navigator.gpu` trả về null."
        ],
        "security": "Ngăn chặn việc khai thác lỗi tràn bộ đệm GPU hoặc tấn công kênh kề (Side-channel timing attacks) thông qua việc kiểm tra kỹ giới hạn kích thước buffer truyền vào compute shader.",
        "deliverables": [
            "Mẫu khởi tạo WebGPU chuẩn `WebGPURuntime.ts`.",
            "Bộ shader WGSL mẫu cho kết xuất 3D và tính toán song song."
        ],
        "related": ["dex-web-canvas-rendering", "dex-gpu-shader-profiling", "dex-gpu-resource-lifetime"],
        "scenario": "Phát triển công cụ xem trước mô hình 3D cho sản phẩm nội thất kiến trúc. Áp dụng `dex-webgpu-rendering-fundamentals` để tận dụng Compute Shaders tính toán phản chiếu ánh sáng chân thực với tốc độ 60fps trên trình duyệt Chrome và Safari hiện đại."
    },
    {
        "id": "dex-frontend-error-recovery",
        "index": 220,
        "group": "Group V",
        "domain": "Advanced Web Experiences",
        "description": "Implement robust frontend error boundaries, optimistic mutation rollbacks, exponential backoff network retries, and contextual fallback states to prevent white-screen crashes. Use when building mission-critical client applications, payment flows, or real-time collaborative editors.",
        "purpose": "Thiết kế và hiện thực hóa cơ chế phục hồi lỗi phía frontend (Frontend Error Recovery) mạnh mẽ; cô lập sự cố bằng React Error Boundaries, hoàn tác cập nhật lạc quan (Optimistic Mutation Rollbacks), tự động thử lại mạng với thuật toán lùi lũy thừa (Exponential Backoff) và ngăn chặn hoàn toàn hiện tượng sập trắng màn hình (White Screen of Death).",
        "when_use": [
            "Khi ứng dụng web gặp lỗi ngoại lệ JavaScript chưa được bắt khiến toàn bộ giao diện bị biến mất.",
            "Khi thực hiện các thao tác quan trọng có rủi ro cao như thanh toán, chuyển tiền hoặc lưu trữ tài liệu trực tuyến.",
            "Khi kết nối mạng của người dùng thường xuyên chập chờn gây lỗi request thất bại giữa chừng."
        ],
        "when_not_use": [
            "Khi xử lý lỗi cú pháp mã nguồn trong quá trình phát triển (Compile-time error).",
            "Khi thiết kế cơ chế khôi phục thảm họa cơ sở dữ liệu dưới tầng hạ tầng backend."
        ],
        "prereqs": "Thư viện quản lý trạng thái, client gửi request HTTP (Fetch/Axios), framework UI hỗ trợ Error Boundaries (React/Vue/Svelte).",
        "concepts": [
            "Granular Error Boundaries: Chia nhỏ ranh giới lỗi theo từng phân vùng (Widget Boundary) để lỗi của một widget con không làm sập toàn bộ trang.",
            "Optimistic UI Rollback: Cập nhật giao diện ngay lập tức cho trải nghiệm nhanh, nhưng lưu lại ảnh chụp trạng thái cũ để hoàn tác mượt mà nếu máy chủ trả về lỗi.",
            "Exponential Backoff with Jitter: Tự động gửi lại request sau các khoảng thời gian tăng dần $2^n$ cộng thêm độ trễ ngẫu nhiên để tránh gây nghẽn máy chủ."
        ],
        "steps": [
            "Bọc các module độc lập trong các thành phần `ErrorBoundary` chuyên biệt.",
            "Thiết kế giao diện Fallback UI thân thiện kèm nút bấm 'Thử lại' (Retry) cho từng khối chức năng.",
            "Cài đặt interceptor cho các request mạng để tự động thử lại tối đa 3 lần với thuật toán Exponential Backoff khi gặp mã lỗi 5xx hoặc mất mạng.",
            "Lưu trạng thái dự phòng của biểu mẫu vào `sessionStorage` để người dùng không bị mất dữ liệu khi phải tải lại trang.",
            "Gửi báo cáo telemetry lỗi chi tiết về máy chủ giám sát."
        ],
        "code_lang": "typescript",
        "code_example": """// Robust Exponential Backoff Retry Utility
export async function fetchWithRetry(url: string, options: RequestInit = {}, retries = 3, baseDelayMs = 500): Promise<Response> {
  try {
    const response = await fetch(url, options);
    if (!response.ok && response.status >= 500 && retries > 0) {
      throw new Error(`Server error: ${response.status}`);
    }
    return response;
  } catch (err) {
    if (retries === 0) throw err;
    const delay = baseDelayMs * Math.pow(2, 3 - retries) + Math.random() * 200;
    await new Promise(resolve => setTimeout(resolve, delay));
    return fetchWithRetry(url, options, retries - 1, baseDelayMs);
  }
}""",
        "antipatterns": [
            "Bọc một Error Boundary duy nhất ở cấp gốc cao nhất (Root App), khiến bất kỳ lỗi nhỏ nào ở footer cũng làm toàn bộ ứng dụng biến mất.",
            "Thử lại request mạng liên tục trong vòng lặp vô hạn mà không có thời gian chờ (Infinite Retry Loop) gây quá tải server.",
            "Nuốt lỗi ngầm (`catch (e) {}`) mà không ghi log telemetry khiến đội ngũ kỹ thuật không biết người dùng đang gặp sự cố."
        ],
        "quality_gates": [
            "QG-01: Không bao giờ xuất hiện hiện tượng 'màn hình trắng' hoàn toàn khi xảy ra lỗi runtime trong bất kỳ component nào.",
            "QG-02: 100% các thao tác cập nhật lạc quan (Optimistic Updates) có cơ chế hoàn tác dữ liệu chính xác khi request thất bại.",
            "QG-03: Lỗi ngoại lệ được báo cáo tự động về dịch vụ theo dõi kèm đầy đủ stack trace và ngữ cảnh người dùng."
        ],
        "security": "Không hiển thị stack trace kỹ thuật chi tiết chứa đường dẫn máy chủ hoặc thông tin nội bộ trên giao diện Fallback của người dùng cuối.",
        "deliverables": [
            "Bộ component React `GranularErrorBoundary.tsx`.",
            "Thư viện gửi request có tự phục hồi `fetchWithRetry.ts`."
        ],
        "related": ["dex-reliability-engineering", "dex-ui-component-contracts", "dex-frontend-performance"],
        "scenario": "Người dùng đang nhập biểu mẫu thanh toán thẻ tín dụng thì kết nối mạng bị rớt tạm thời trong 1 giây. Nhờ `dex-frontend-error-recovery`, ứng dụng tự động thử lại request với độ trễ lũy thừa mà không làm mất thông tin người dùng đã nhập, hoàn tất thanh toán thành công mà người dùng không nhận thấy sự gián đoạn."
    }
]

def build_markdown(meta):
    md = f"""---
name: {meta['id']}
description: {meta['description']}
---

# {meta['id']}

## 1. Purpose & Scope
{meta['purpose']}

## 2. When to Use
"""
    for item in meta['when_use']:
        md += f"- {item}\n"

    md += "\n## 3. When NOT to Use\n"
    for item in meta['when_not_use']:
        md += f"- {item}\n"

    md += f"""
## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** {meta['prereqs']}
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
"""
    for item in meta['concepts']:
        md += f"- **{item.split(':', 1)[0]}:**{item.split(':', 1)[1] if ':' in item else ''}\n"

    md += "\n## 6. Step-by-Step Execution Workflow\n"
    for i, step in enumerate(meta['steps'], 1):
        md += f"{i}. {step}\n"

    md += f"""
## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```{meta['code_lang']}
{meta['code_example']}
```

## 8. Anti-Patterns & Common Traps
"""
    for item in meta['antipatterns']:
        md += f"- {item}\n"

    md += "\n## 9. Quality Gates & Acceptance Criteria\n"
    for item in meta['quality_gates']:
        md += f"- {item}\n"

    md += f"""
## 10. Security & Safety Boundaries
- {meta['security']}
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
"""
    for item in meta['deliverables']:
        md += f"1. {item}\n"

    md += "\n## 13. Related & Complementary Skills\n"
    for r in meta['related']:
        md += f"- [`{r}`](.agents/skills/{r}/SKILL.md)\n"

    md += f"""
## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
{meta['scenario']}
"""
    return md

def generate_skills():
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    for s in GROUP_U_V_SKILLS:
        skill_dir = os.path.join(SKILLS_DIR, s["id"])
        os.makedirs(skill_dir, exist_ok=True)
        skill_file = os.path.join(skill_dir, "SKILL.md")
        content = build_markdown(s)
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Generated {s['id']} (Skill {s['index']:03d})")

if __name__ == "__main__":
    generate_skills()
