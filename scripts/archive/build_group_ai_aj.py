# -*- coding: utf-8 -*-
"""
DEX ENGINEERING SKILLS FRAMEWORK v8.0 — GENERATOR
Builds Group AI (Skills 341–350: Advanced UI/UX Engineering)
and Group AJ (Skills 351–360: Authorized Software Inspection).
All skills strictly implement the 14 mandatory sections standard.
"""

import os
import sys

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

SKILLS_AI_AJ = [
    # =========================================================================
    # GROUP AI: Advanced UI/UX Engineering (Skills 341–350)
    # =========================================================================
    {
        "id": "dex-design-token-migration",
        "name": "dex-design-token-migration",
        "desc": "Automate migration from hardcoded CSS/SCSS styling and legacy design tokens to modern W3C Design Tokens Community Group (DTCG) formats and CSS custom properties. Use when consolidating divergent design tokens or refactoring legacy component stylesheets.",
        "purpose": "Tự động hóa chuyển đổi các giá trị giao diện hardcoded (màu sắc, khoảng cách, font, shadow) và hệ thống token cũ sang định dạng chuẩn W3C Design Tokens Community Group (DTCG) và CSS Custom Properties; bảo đảm tính nhất quán đa nền tảng và hỗ trợ chuyển đổi theme động.",
        "when_use": "- Khi chuẩn hóa hệ thống Design System từ các biến Sass/Less rời rạc sang chuẩn DTCG JSON.\n- Khi triển khai cơ chế Dark Mode hoặc Multi-branding yêu cầu các token ngữ nghĩa (semantic tokens) động.\n- Khi thực hiện kiểm toán CSS codebase để triệt tiêu các mã màu hex và kích thước px phân mảnh.",
        "when_not_use": "- Khi dự án là landing page đơn lẻ, tĩnh, không có kế hoạch mở rộng hoặc đa theme.\n- Khi chưa có sự đồng thuận giữa đội ngũ UI/UX Design (Figma) và Engineering về quy ước đặt tên token.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File định nghĩa token (Figma Tokens JSON, Style Dictionary config, SCSS variables) và codebase giao diện hiện hữu.\n- **Quyền hạn truy cập:** Quyền ghi vào thư mục style/tokens và component libraries.",
        "concepts": "- **Design Tokens Format Module (DTCG):** Chuẩn mở JSON quy định kiểu dữ liệu token (`$value`, `$type`, `$description`).\n- **Token Tiering:** Kiến trúc 3 tầng: Global/Reference Tokens (`color.blue.500`) -> Semantic Tokens (`color.background.interactive.hover`) -> Component Tokens (`button.primary.bg`).\n- **Style Dictionary:** Công cụ build biến đổi token từ nguồn JSON sang CSS, SCSS, Swift, Android XML.",
        "workflow": "1. Khảo sát và trích xuất tất cả các biến màu sắc, typography, spacing từ SCSS, CSS Modules, Styled Components.\n2. Chuẩn hóa phân loại token thành 3 tầng: Base/Primitive, Semantic/Alias, và Component-specific.\n3. Biên dịch cấu trúc JSON tuân thủ đặc tả W3C DTCG Format.\n4. Cấu hình Style Dictionary để xuất ra CSS Custom Properties có fallback an toàn.\n5. Xây dựng AST Codemod (jscodeshift hoặc Stylelint plugin) để tự động thay thế mã màu hardcoded bằng biến token tương ứng.\n6. Chạy visual regression testing để xác thực giao diện không bị lệch pixel sau khi chuyển đổi.",
        "examples": """### Cấu trúc W3C DTCG Token và cấu hình Style Dictionary:
```json
{
  "color": {
    "semantic": {
      "surface": {
        "primary": {
          "$value": "{color.base.neutral.0}",
          "$type": "color",
          "$description": "Nền chính cho các card và view viewports"
        },
        "brand": {
          "$value": "{color.base.blue.600}",
          "$type": "color",
          "$description": "Màu nhận diện thương hiệu cho các điểm nhấn chính"
        }
      }
    }
  }
}
```

```javascript
// style-dictionary.config.js
export default {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'src/styles/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables',
        options: { outputReferences: true }
      }]
    }
  }
};
```""",
        "antipatterns": "- **Direct Global Token Usage:** Sử dụng trực tiếp token cơ sở như `var(--color-blue-500)` trong component thay vì dùng token ngữ nghĩa `var(--color-action-primary)`.\n- **Unbound Circular Tokens:** Khai báo token tham chiếu vòng lặp khiến trình biên dịch bị treo.\n- **Silent Breaking Overrides:** Ghi đè biến CSS cục bộ làm phá vỡ tính nhất quán của theme toàn hệ thống.",
        "gates": "- **QG-01**: 100% token JSON vượt qua xác thực cú pháp JSON Schema của W3C DTCG.\n- **QG-04**: Quá trình biên dịch token xuất ra CSS variables hợp lệ không bị cảnh báo Stylelint.\n- **QG-07**: Không còn mã màu hex hoặc kích thước px hardcoded trong các component mới.",
        "security": "- Kiểm tra định dạng token file không chứa các payload CSS injection hoặc biểu thức `url()` độc hại.",
        "adapters": "- **Build Tools**: Style Dictionary v4, Token Studio, Stylelint.\n- **Platforms**: Web (CSS/SCSS), iOS (Swift), Android (Compose/XML).",
        "deliverables": "- File JSON chuẩn W3C DTCG token.\n- File CSS variables và TypeScript type definitions cho token.\n- Script Codemod tự động chuyển đổi mã nguồn cũ.",
        "related": "dex-design-system-foundations, dex-visual-hierarchy-composition, dex-theme-lifecycle-management",
        "usage": """```powershell
# Chạy Style Dictionary để biên dịch tokens sang CSS custom properties
npx style-dictionary build

# Kiểm tra các giá trị hardcoded còn sót lại trong CSS codebase
npx stylelint "src/**/*.css" --config .stylelintrc-token-check.json
```"""
    },
    {
        "id": "dex-component-state-matrix",
        "name": "dex-component-state-matrix",
        "desc": "Systematically specify, render, and visually verify all interactive UI component permutations across rest, hover, active, focus-visible, disabled, loading, error, and empty states. Use when building robust design systems and preventing interactive UX regressions.",
        "purpose": "Hệ thống hóa, mô phỏng và kiểm chứng trực quan toàn bộ ma trận trạng thái của UI component bao gồm idle, hover, active, focus-visible, disabled, loading, invalid, và empty; đảm bảo trải nghiệm tương tác liền mạch và khả năng tiếp cận chuẩn WCAG.",
        "when_use": "- Khi phát triển component mới cho thư viện UI hoặc Design System trung tâm.\n- Khi audit khả năng tiếp cận (a11y) của các trường nhập liệu và nút bấm tương tác.\n- Khi phát hiện lỗi giao diện chỉ xuất hiện ở các trạng thái biên như loading kết hợp disabled.",
        "when_not_use": "- Khi dựng mockup tĩnh phục vụ mục đích phỏng vấn ý tưởng ban đầu trong thời gian ngắn.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Component specification, Storybook hoặc môi trường test trực quan tương đương.\n- **Quyền hạn truy cập:** Quyền ghi vào thư mục stories và test của component.",
        "concepts": "- **Component Permutation Matrix:** Tích Descartes của tất cả các biến thể (variants: primary, secondary) x kích thước (sm, md, lg) x trạng thái tương tác.\n- **Focus-Visible Discipline:** Chỉ hiển thị viền focus nổi bật khi người dùng điều hướng bằng bàn phím (Tab), không gây khó chịu khi click chuột.\n- **State Collision Handling:** Định nghĩa thứ tự ưu tiên khi nhiều trạng thái đồng thời xuất hiện (ví dụ: disabled có ưu tiên cao hơn hover và active).",
        "workflow": "1. Liệt kê toàn bộ các trạng thái khả dĩ của component: Idle, Hover, Active, Focus, Focus-Visible, Disabled, Loading, Error, Empty.\n2. Thiết lập bảng ma trận ưu tiên trạng thái (State Precedence Table) để xử lý xung đột.\n3. Viết Storybook stories hiển thị song song toàn bộ ma trận trạng thái trên cùng một view.\n4. Tích hợp kiểm thử tự động giả lập tương tác bàn phím và con trỏ chuột bằng Playwright hoặc Cypress.\n5. Xác nhận tỷ lệ tương phản màu sắc (Color Contrast Ratio) ở mọi trạng thái đều đạt chuẩn WCAG 2.2 AA (>= 4.5:1 hoặc >= 3:1 cho focus ring).\n6. Đóng gói component kèm tài liệu trực quan minh họa từng trạng thái.",
        "examples": """### Định nghĩa ma trận trạng thái trong Storybook (React / TypeScript):
```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Design System/Button/StateMatrix',
  component: Button,
};
export default meta;

export const AllStatesMatrix: StoryObj = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
      <div>
        <h4>Normal / Idle</h4>
        <Button variant="primary">Submit</Button>
      </div>
      <div>
        <h4>Hover State</h4>
        <Button variant="primary" className="pseudo-hover">Submit</Button>
      </div>
      <div>
        <h4>Focus-Visible</h4>
        <Button variant="primary" className="pseudo-focus-visible">Submit</Button>
      </div>
      <div>
        <h4>Loading State</h4>
        <Button variant="primary" isLoading>Submit</Button>
      </div>
      <div>
        <h4>Disabled State</h4>
        <Button variant="primary" disabled>Submit</Button>
      </div>
    </div>
  ),
};
```""",
        "antipatterns": "- **Missing Disabled Interaction Block:** Chỉ đổi màu nút bấm sang xám nhưng không chặn sự kiện click hoặc submit trong JavaScript.\n- **Outline None Without Alternative:** Ẩn viền focus mặc định (`outline: none`) mà không tạo kiểu focus ring thay thế cho người dùng bàn phím.\n- **Flickering Loading Jitter:** Đổi kích thước component đột ngột khi hiển thị spinner làm dịch chuyển bố cục xung quanh (Layout Shift).",
        "gates": "- **QG-01**: Tất cả các component tương tác đều có Storybook story bao phủ 100% các trạng thái trong ma trận.\n- **QG-03**: Trạng thái focus-visible luôn có viền tương phản tối thiểu 3:1 so với nền liền kề.\n- **QG-07**: Component disabled không kích hoạt bất kỳ callback sự kiện nào khi click hoặc nhấn phím.",
        "security": "- Ngăn ngừa tấn công Clickjacking bằng cách kiểm tra các component có thể che khuất nút tương tác bằng CSS opacity.",
        "adapters": "- **Catalog & UI Testing**: Storybook, Chromatic, Playwright Component Testing, Jest-DOM.",
        "deliverables": "- File Storybook matrix story cho component.\n- Bộ quy tắc CSS trạng thái tương tác hoàn chỉnh.\n- Test suite xác thực chặn sự kiện khi disabled.",
        "related": "dex-wcag-compliance-audit, dex-design-token-migration, dex-gesture-interaction-accessibility",
        "usage": """```powershell
# Chạy Storybook để kiểm tra ma trận trạng thái
npm run storybook

# Chạy visual regression test xác thực trạng thái tương tác
npx playwright test tests/visual/button-matrix.spec.ts
```"""
    },
    {
        "id": "dex-typography-scale-localization",
        "name": "dex-typography-scale-localization",
        "desc": "Engineer scalable, multilingual typography systems supporting diverse script densities, character heights, diacritics, and vertical alignments across Latin, CJK, Arabic, and Indic scripts. Use when building global software interfaces.",
        "purpose": "Thiết kế và triển khai thang tỷ lệ typography có khả năng co giãn linh hoạt và bản địa hóa đa ngôn ngữ; xử lý hoàn hảo các đặc thù về mật độ chữ, dấu thanh phụ, chiều cao dòng (line-height) cho các hệ chữ viết khác nhau như Latin, Tiếng Việt, CJK, Ả Rập và Indic.",
        "when_use": "- Khi mở rộng ứng dụng phục vụ thị trường toàn cầu với các ngôn ngữ có dấu hoặc ký tự phức tạp.\n- Khi văn bản tiếng Việt bị cắt ngọn dấu thanh hoặc văn bản tiếng Đức bị tràn khối chứa (overflow).\n- Khi cần thiết lập fallback font stack tối ưu hiệu năng hiển thị cho từng ngôn ngữ mục tiêu.",
        "when_not_use": "- Khi ứng dụng chỉ phục vụ duy nhất một ngôn ngữ nội bộ và không có kế hoạch quốc tế hóa.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Danh sách ngôn ngữ hỗ trợ (locales), font files hoặc webfont providers, bảng phân bổ font metrics.\n- **Quyền hạn truy cập:** Quyền sửa đổi cấu hình theme typography và CSS global.",
        "concepts": "- **Font Metrics Override:** Điều chỉnh `ascent-override`, `descent-override`, và `line-gap-override` trong `@font-face` để triệt tiêu hiện tượng lệch dòng khi tải fallback font.\n- **Script Expansion Factor:** Hệ số giãn nở độ dài chuỗi ký tự theo ngôn ngữ (ví dụ: tiếng Đức dài hơn tiếng Anh khoảng 30%, tiếng Phần Lan dài hơn 35%).\n- **Diacritic Clearance:** Đảm bảo chiều cao dòng tối thiểu để các dấu thanh ghép tiếng Việt (như ể, ễ, ậ) hoặc dấu nguyên âm Ả Rập không bị chém mất.",
        "workflow": "1. Khảo sát danh sách các ký tự đặc biệt và dấu thanh của toàn bộ locale cần hỗ trợ.\n2. Thiết lập thang đo kiểu chữ sử dụng đơn vị tương đối `rem` và `clamp()` để đáp ứng hiển thị co giãn linh hoạt.\n3. Cấu hình quy tắc `@font-face` kèm thuộc tính `unicode-range` để nạp chính xác subset font cần thiết cho từng ngôn ngữ.\n4. Tinh chỉnh `line-height` cơ sở tối thiểu 1.4 - 1.6 cho các hệ chữ có dấu thanh cao (như tiếng Việt, Thái, Ả Rập).\n5. Thiết lập cơ chế font fallback thông minh khớp với x-height và cap-height của web font để tránh Cumulative Layout Shift (CLS).\n6. Kiểm thử tự động trên nhiều kích thước màn hình và ngôn ngữ giả lập (pseudo-localization) để phát hiện tràn viền.",
        "examples": """### Cấu hình CSS @font-face tối ưu hóa metrics và subset tiếng Việt:
```css
/* Web Font chính */
@font-face {
  font-family: 'AppSans';
  src: url('/fonts/app-sans-vietnamese.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9;
}

/* Fallback Font căn chỉnh metrics để triệt tiêu CLS */
@font-face {
  font-family: 'AppSans-Fallback';
  src: local('Arial');
  ascent-override: 95%;
  descent-override: 25%;
  line-gap-override: 0%;
  size-adjust: 102%;
}

:root {
  --font-base: 'AppSans', 'AppSans-Fallback', -apple-system, BlinkMacSystemFont, sans-serif;
  --line-height-body: 1.5; /* Bảo vệ an toàn dấu thanh tiếng Việt */
}
```""",
        "antipatterns": "- **Hardcoded Line-Height in Pixels:** Đặt `line-height: 20px` cố định trong khi kích thước chữ là `18px`, khiến các dấu thanh phụ bị cắt ngọn trên trình duyệt.\n- **Monolithic CJK Webfont Ingestion:** Nạp toàn bộ bộ font chữ Hán/Nhật/Hàn kích thước 15MB mà không chia cắt subset (dynamic font slicing).\n- **Ignoring Text Truncation in Multi-language:** Sử dụng `text-overflow: ellipsis` trên một dòng cho các tiêu đề quan trọng trong giao diện đa ngôn ngữ.",
        "gates": "- **QG-01**: CLS (Cumulative Layout Shift) nhỏ hơn 0.05 khi chuyển đổi giữa fallback font và web font.\n- **QG-03**: 100% các ký tự dấu thanh phụ tiếng Việt và CJK hiển thị đầy đủ, không bị cắt ngọn hoặc chồng đè lên dòng trên.\n- **QG-06**: Tỷ lệ font subset tải xuống tiết kiệm tối thiểu 60% băng thông so với file font gốc.",
        "security": "- Nạp font từ các CDN uy tín có kiểm tra SRI (Subresource Integrity) hoặc tự host font trên cùng domain để ngăn ngừa rò rỉ dữ liệu.",
        "adapters": "- **Tools**: glyphhanger, fonttools, capsizecss, Font Squirrel Webfont Generator.",
        "deliverables": "- Bảng cấu hình Typography Tokens đa ngôn ngữ.\n- File CSS font-face tối ưu metrics chống nhảy layout (CLS).\n- Báo cáo kiểm thử hiển thị trên các locale trọng điểm.",
        "related": "dex-fluid-typography-scaling, dex-rtl-bidi-layout-readiness, dex-cross-platform-ui-parity",
        "usage": """```powershell
# Tạo font subset woff2 chỉ chứa các ký tự cần thiết cho tiếng Việt
npx glyphhanger --subset=*.ttf --whitelist="A-Z,a-z,0-9,ĂÂĐÊÔƠƯăâđêôơư" --formats=woff2

# Kiểm tra Layout Shift bằng Lighthouse CI
npx lighthouserc autorun
```"""
    },
    {
        "id": "dex-high-density-dashboard-layout",
        "name": "dex-high-density-dashboard-layout",
        "desc": "Architect high-density information layouts for data-intensive enterprise cockpits, financial terminals, and monitoring consoles. Use when structuring large volumes of real-time widgets without sacrificing visual hierarchy and cognitive load.",
        "purpose": "Thiết kế và cấu trúc giao diện bảng điều khiển (Dashboard) mật độ thông tin cao cho các hệ thống giám sát thời gian thực, thiết bị đầu cuối tài chính và trung tâm điều hành; duy trì sự rõ ràng về mặt phân cấp thị giác và kiểm soát tải nhận thức của người vận hành.",
        "when_use": "- Khi xây dựng giao diện giám sát viễn thám, sàn giao dịch tài chính, hoặc bảng điều khiển DevOps (NOC/SOC).\n- Khi người dùng cần quan sát đồng thời hàng chục biểu đồ, bảng dữ liệu, và chỉ số KPI mà không phải cuộn trang liên tục.\n- Khi cần hỗ trợ chế độ xem đa màn hình và kích thước lưới linh hoạt (bố cục widget tùy biến).",
        "when_not_use": "- Khi phát triển ứng dụng tiêu dùng (B2C) hoặc mobile onboarding đòi hỏi giao diện tối giản, nhiều khoảng trắng thoáng.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Danh sách widget dữ liệu, tần suất cập nhật dữ liệu thời gian thực, chuẩn kích thước màn hình người dùng mục tiêu.\n- **Quyền hạn truy cập:** Quyền sửa đổi component layout và hệ thống Grid.",
        "concepts": "- **Information Density vs. Cognitive Overload:** Mật độ thông tin cao không đồng nghĩa với lộn xộn; cần áp dụng quy tắc nhóm thị giác (Gestalt Law of Proximity) và viền phân cách vi mô.\n- **Virtual Widget Rendering:** Chỉ render các ô widget nằm trong khung nhìn hiển thị để tiết kiệm CPU/DOM nodes.\n- **Data Sparklines & Micro-Visualizations:** Sử dụng biểu đồ đường mini không trục để tóm tắt xu hướng mà không chiếm diện tích quý giá.",
        "workflow": "1. Xác định phân cấp độ ưu tiên của các luồng thông tin: Chỉ số cốt lõi (Tier 1), Biểu đồ xu hướng (Tier 2), Bảng chi tiết (Tier 3).\n2. Thiết lập hệ thống lưới CSS Grid 12 hoặc 24 cột với rãnh (gutters) nhỏ gọn (8px hoặc 12px).\n3. Tối ưu kích thước khoảng đệm (padding) trong các cell dữ liệu và áp dụng bảng màu trung tính cho khung chứa.\n4. Triển khai kỹ thuật virtual rendering cho các bảng dữ liệu hàng nghìn dòng bên trong widget.\n5. Áp dụng debounce và throttle cho các cập nhật thời gian thực qua WebSocket để tránh giật lag render.\n6. Cung cấp phím tắt bàn phím và khả năng phóng to toàn màn hình (Focus Mode) cho từng widget riêng lẻ.",
        "examples": """### Bố cục Dashboard mật độ cao bằng CSS Grid:
```css
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 8px; /* Rãnh gọn gàng cho mật độ hiển thị cao */
  padding: 8px;
  background-color: var(--color-surface-sunken);
}

.widget-kpi {
  grid-column: span 3;
  padding: 8px 12px;
  background: var(--color-surface-card);
  border: 1px solid var(--color-border-subtle);
  border-radius: 4px;
}

.widget-chart-large {
  grid-column: span 8;
  height: 320px;
}

.widget-feed-stream {
  grid-column: span 4;
  height: 320px;
  overflow-y: auto;
}
```""",
        "antipatterns": "- **Color Rainbow Saturation:** Dùng quá nhiều màu sắc rực rỡ khiến mắt người dùng bị mỏi và không phân biệt được cảnh báo khẩn cấp.\n- **DOM Tree Explosion:** Render hàng nghìn thẻ HTML div lồng nhau cho mỗi hàng dữ liệu làm đơ giao diện khi có luồng dữ liệu mới.\n- **Layout Shifting on Live Push:** Cập nhật số liệu làm thay đổi chiều rộng widget khiến toàn bộ lưới dashboard bị giật nhảy liên tục.",
        "gates": "- **QG-01**: Tốc độ khung hình duy trì ổn định >= 55 FPS khi nhận cập nhật dữ liệu 10 lần/giây.\n- **QG-03**: Tất cả các màu sắc cảnh báo (Critical, Warning, Normal) đều có sự khác biệt rõ rệt về độ sáng và biểu tượng đi kèm (không phụ thuộc hoàn toàn vào màu sắc).\n- **QG-08**: Số lượng DOM nodes trên toàn trang không vượt quá 2,500 nodes tại bất kỳ thời điểm nào.",
        "security": "- Khử khuẩn dữ liệu thời gian thực (XSS sanitization) trước khi hiển thị vào các feed stream của dashboard.",
        "adapters": "- **Layout & Virtualization**: CSS Grid, TanStack Virtual, React-Grid-Layout, ECharts, uPlot.",
        "deliverables": "- Cấu trúc component Grid Dashboard responsive.\n- Bộ stylesheet tối ưu mật độ hiển thị (High-Density Theme).\n- Benchmark hiệu năng render dữ liệu thời gian thực.",
        "related": "dex-virtualized-infinite-lists, dex-perceived-performance-patterns, dex-chart-visualization-accessibility",
        "usage": """```powershell
# Đo số lượng DOM nodes và FPS khi nhận live data
npx playwright test tests/perf/high-density-dashboard.spec.ts

# Kiểm tra hiệu năng render bằng Chrome DevTools trace
npx lighthouse http://localhost:3000/dashboard --preset=desktop --view
```"""
    },
    {
        "id": "dex-gesture-interaction-accessibility",
        "name": "dex-gesture-interaction-accessibility",
        "desc": "Design and validate touch, swipe, pinch, and multi-finger gesture interactions with accessible single-pointer and keyboard alternatives compliant with WCAG 2.5 Input Modalities. Use when engineering modern mobile-first web and native touch interfaces.",
        "purpose": "Thiết kế, chuẩn hóa và kiểm chứng các tương tác cử chỉ chạm vuốt (gestures) trên thiết bị di động và màn hình cảm ứng; bảo đảm luôn cung cấp giải pháp thay thế bằng con trỏ đơn (single-pointer) và bàn phím theo tiêu chí WCAG 2.5 Input Modalities.",
        "when_use": "- Khi xây dựng các tính năng tương tác cử chỉ như vuốt để xóa (swipe to delete), kéo thả (drag and drop), hoặc chụm mở để thu phóng (pinch to zoom).\n- Khi ứng dụng di động cần đáp ứng tiêu chuẩn tiếp cận tiếp cận cho người dùng có khiếm khuyết vận động.\n- Khi kiểm toán tuân thủ WCAG 2.2 cho các ứng dụng Hybrid hoặc Progressive Web Apps.",
        "when_not_use": "- Khi ứng dụng chỉ hoạt động trên môi trường dòng lệnh CLI hoặc máy chủ không có giao diện đồ họa cảm ứng.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Đặc tả cử chỉ tương tác (gesture spec), thiết bị thử nghiệm cảm ứng hoặc trình giả lập touch events.\n- **Quyền hạn truy cập:** Quyền sửa đổi logic xử lý sự kiện tương tác người dùng.",
        "concepts": "- **WCAG 2.5.1 Pointer Gestures:** Bất kỳ thao tác nào yêu cầu cử chỉ đa điểm (multipoint) hoặc cử chỉ dựa trên đường dẫn (path-based) đều phải có phương thức tương tác đơn giản chỉ bằng một lần nhấp (single-pointer alternative).\n- **WCAG 2.5.2 Pointer Cancellation:** Cho phép người dùng hủy thao tác bằng cách di chuyển ngón tay ra khỏi vùng kích hoạt trước khi nhấc lên (Up-Event Triggering).\n- **Minimum Target Size:** Kích thước vùng bấm tối thiểu đạt 24x24 CSS pixels (WCAG 2.2 Level AA) hoặc khuyến nghị 44x44 / 48x48 pixels.",
        "workflow": "1. Khảo sát danh mục tất cả các cử chỉ tương tác trong ứng dụng: Swipe, Drag, Pinch, Double-tap, Long-press.\n2. Thiết kế nút bấm hoặc menu tùy chọn tương đương cho mỗi cử chỉ (ví dụ: cung cấp nút 'Xóa' trong menu tùy chọn bên cạnh cử chỉ vuốt ngang).\n3. Gắn bộ lắng nghe sự kiện `pointerup` thay vì `pointerdown` để cho phép hủy bỏ hành động vô ý.\n4. Cung cấp cơ chế xác nhận trước các hành động phá hủy dữ liệu được kích hoạt từ cử chỉ cảm ứng.\n5. Đảm bảo toàn bộ các mục tiêu tương tác có kích thước vùng chạm tối thiểu đạt chuẩn.\n6. Kiểm thử tương tác song song với bàn phím (phím Enter, Space, mũi tên) và phần mềm đọc màn hình (TalkBack, VoiceOver).",
        "examples": """### Xử lý cử chỉ vuốt kèm cơ chế Single-Pointer và Phím tắt dự phòng:
```typescript
interface DismissibleItemProps {
  id: string;
  onDismiss: (id: string) => void;
  title: string;
}

export const DismissibleItem: React.FC<DismissibleItemProps> = ({ id, onDismiss, title }) => {
  return (
    <div className="item-row" role="listitem">
      <span>{title}</span>
      {/* Nút hành động đơn lẻ dự phòng cho người dùng không thể thực hiện thao tác vuốt */}
      <button 
        type="button" 
        className="btn-action-fallback"
        aria-label={`Xóa mục ${title}`}
        onClick={() => onDismiss(id)}
      >
        Xóa
      </button>
    </div>
  );
};
```""",
        "antipatterns": "- **Gesture-Only Actions:** Cung cấp tính năng quan trọng (như xóa thư hoặc lưu trữ) độc quyền qua thao tác vuốt mà không có nút bấm tương đương.\n- **Trigger on PointerDown:** Kích hoạt giao dịch hoặc xóa dữ liệu ngay khi vừa chạm màn hình, không cho phép người dùng kéo ra ngoài để hủy.\n- **Tiny Touch Target:** Đặt các nút icon có kích thước 16x16px nằm sát nhau trên màn hình cảm ứng khiến người dùng liên tục bấm nhầm.",
        "gates": "- **QG-01**: 100% các cử chỉ vuốt hoặc kéo thả đều có nút bấm đơn giản thay thế trên giao diện.\n- **QG-03**: Vùng tương tác cảm ứng đạt kích thước tối thiểu 24x24 CSS pixels (đạt chuẩn WCAG 2.2 AA).\n- **QG-07**: Không có hành động không thể hoàn tác nào được kích hoạt từ sự kiện pointerdown.",
        "security": "- Ngăn chặn hiện tượng 'Tapjacking' hoặc 'Pointer Spoofing' bằng cách kiểm tra thuộc tính `isTrusted` trên PointerEvents.",
        "adapters": "- **Libraries**: Hammer.js, interact.js, Framer Motion, React-Use-Gesture.\n- **Testing**: Playwright Touch Emulation, axe-core.",
        "deliverables": "- Component cử chỉ chạm vuốt kèm cơ chế fallback bàn phím.\n- Bộ kiểm thử tự động xác minh kích thước vùng chạm.\n- Tài liệu hướng dẫn thao tác tương tác đa phương thức.",
        "related": "dex-wcag-compliance-audit, dex-component-state-matrix, dex-mobile-first-responsive-patterns",
        "usage": """```powershell
# Chạy kiểm thử tự động kiểm tra kích thước vùng bấm (Target Size)
npx playwright test tests/a11y/target-size.spec.ts

# Giả lập sự kiện chạm vuốt trên môi trường mobile
npx cypress run --spec "cypress/e2e/gestures.cy.ts" --config viewportWidth=375,viewportHeight=667
```"""
    },
    {
        "id": "dex-rtl-bidi-layout-readiness",
        "name": "dex-rtl-bidi-layout-readiness",
        "desc": "Audit, refactor, and automate bidirectional (BiDi) layout mirroring for Right-to-Left (RTL) scripts including Arabic, Hebrew, and Persian. Use when globalizing web and mobile interfaces.",
        "purpose": "Kiểm toán, tái cấu trúc và tự động hóa cơ chế phản chiếu giao diện hai chiều (BiDi) cho các hệ chữ viết từ Phải qua Trái (Right-to-Left - RTL) như tiếng Ả Rập, Hebrew và Ba Tư; thay thế các thuộc tính CSS vật lý bằng các thuộc tính logic (CSS Logical Properties).",
        "when_use": "- Khi mở rộng sản phẩm sang thị trường Trung Đông và Bắc Phi (MENA region).\n- Khi giao diện hiển thị các khối nội dung hỗn hợp kết hợp cả chữ tiếng Anh và tiếng Ả Rập.\n- Khi phát hiện các biểu tượng điều hướng (như mũi tên quay lại) hoặc lề căn chỉnh bị ngược chiều.",
        "when_not_use": "- Khi ứng dụng chỉ phục vụ thị trường bản địa thuần LTR và không có kế hoạch mở rộng thị trường Ả Rập.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Codebase giao diện hiện tại, tài liệu định nghĩa danh sách ngôn ngữ RTL hỗ trợ.\n- **Quyền hạn truy cập:** Quyền sửa đổi CSS framework và component templates.",
        "concepts": "- **CSS Logical Properties:** Thay thế các thuộc tính vật lý cố định (`margin-left`, `padding-right`, `left`, `right`) bằng các thuộc tính logic (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`).\n- **Directional Icon Mirroring:** Một số biểu tượng thể hiện hướng di chuyển theo thời gian (như mũi tên back/forward) phải lật ngược trong RTL, trong khi biểu tượng đồng hồ hoặc media controls thì giữ nguyên.\n- **BiDi Isolation:** Sử dụng thẻ `<bdi>` hoặc thuộc tính `unicode-bidi: isolate` để cách ly các chuỗi văn bản hỗn hợp (như số điện thoại, mã đơn hàng) khỏi việc bị đảo lộn ký tự.",
        "workflow": "1. Quét toàn bộ codebase để phát hiện và gắn cờ các thuộc tính CSS định hướng vật lý (`left`, `right`, `margin-left`, `float: left`).\n2. Thay thế hàng loạt bằng CSS Logical Properties (`inline-start`, `inline-end`, `inset-inline`).\n3. Cấu hình thuộc tính `dir=\"rtl\"` tự động trên thẻ `<html>` dựa trên ngôn ngữ người dùng lựa chọn.\n4. Phân loại danh mục biểu tượng: Biểu tượng cần phản chiếu (Back, Forward, Chevron) vs Biểu tượng bất biến (Play, Pause, Download).\n5. Bọc các chuỗi dữ liệu động hỗn hợp (tên người dùng kèm số) bằng thẻ `<bdi>` để tránh lỗi vỡ thứ tự hiển thị.\n6. Kiểm thử tự động trên cả hai chế độ LTR và RTL bằng công cụ chụp ảnh so sánh trực quan (Visual Regression Testing).",
        "examples": """### Chuyển đổi thuộc tính vật lý sang CSS Logical Properties:
```css
/* Trước đây: Phụ thuộc chiều cố định (Lỗi hiển thị trên RTL) */
.user-card {
  margin-left: 16px;
  padding-right: 24px;
  text-align: left;
  border-left: 4px solid var(--color-primary);
}

/* Hiện đại: Sử dụng CSS Logical Properties (Tự động thích ứng cả LTR và RTL) */
.user-card {
  margin-inline-start: 16px;
  padding-inline-end: 24px;
  text-align: start;
  border-inline-start: 4px solid var(--color-primary);
}

/* Phản chiếu biểu tượng điều hướng trong ngữ cảnh RTL */
[dir="rtl"] .icon-directional {
  transform: scaleX(-1);
}
```""",
        "antipatterns": "- **Mirroring Everything Blindly:** Lật ngược cả thanh điều khiển media (nút Play/Pause) hoặc đồ thị thời gian theo trục ngang gây bối rối cho người dùng bản địa.\n- **Hardcoded Direction Attribute:** Ghi cứng `dir=\"ltr\"` trên các component con làm vô hiệu hóa thuộc tính RTL của trang cha.\n- **Phone Number Reversal:** Không cách ly số điện thoại khiến dấu cộng và các chữ số bị đảo vị trí hiển thị trong văn bản tiếng Ả Rập.",
        "gates": "- **QG-01**: 0% thuộc tính CSS vật lý (`margin-left/right`, `left/right`) còn sót lại trong các file style chung.\n- **QG-04**: Toàn bộ các trang kiểm thử hiển thị chính xác ở cả hai thuộc tính `dir=\"ltr\"` và `dir=\"rtl\"`.\n- **QG-07**: Các chuỗi văn bản hỗn hợp (số, mã đơn, email) hiển thị nguyên vẹn thứ tự ký tự.",
        "security": "- Tránh các cuộc tấn công Trojan Source bằng cách kiểm tra và loại bỏ các ký tự điều khiển BiDi ẩn (như `U+202E` Right-to-Left Override) trong đầu vào người dùng.",
        "adapters": "- **Tools**: postcss-logical, stylelint-use-logical-spec, rtlcss, BiDi Checker.",
        "deliverables": "- Bộ quy tắc PostCSS chuyển đổi logical properties.\n- Cấu hình Stylelint phát hiện thuộc tính vật lý.\n- Báo cáo kiểm thử trực quan trên môi trường RTL.",
        "related": "dex-typography-scale-localization, dex-cross-platform-ui-parity, dex-design-token-migration",
        "usage": """```powershell
# Chạy Stylelint để phát hiện các thuộc tính vật lý cần chuyển sang Logical Properties
npx stylelint "src/**/*.css" --config .stylelintrc-logical.json

# Tạo tự động phiên bản RTL stylesheet bằng RTLCSS
npx rtlcss src/styles/main.css dist/styles/main.rtl.css
```"""
    },
    {
        "id": "dex-animation-storyboard-specs",
        "name": "dex-animation-storyboard-specs",
        "desc": "Specify, storyboard, and engineer performant UI motion choreography with strict respects for prefers-reduced-motion media queries and 60fps compositor limits. Use when designing cohesive micro-interactions and transitions.",
        "purpose": "Đặc tả, vẽ kịch bản (storyboard) và lập trình các hiệu ứng chuyển động (motion choreography) mượt mà 60fps; bảo đảm hiệu năng tối ưu trên GPU compositor và tuân thủ nghiêm ngặt cài đặt giảm chuyển động `prefers-reduced-motion` của người dùng.",
        "when_use": "- Khi thiết kế chuỗi chuyển động phức tạp (như mở modal, chuyển tiếp trang, hoặc các vi tương tác phản hồi thao tác).\n- Khi các hiệu ứng hoạt họa gây giật lag (frame drops) hoặc gây chóng mặt, buồn nôn cho người dùng có chứng rối loạn tiền đình.\n- Khi cần đồng nhất ngôn ngữ chuyển động (timing curves, duration) giữa bản thiết kế Figma và mã nguồn thực tế.",
        "when_not_use": "- Khi xây dựng giao diện tài liệu tĩnh thuần túy không có yếu tố tương tác động.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Bảng thông số chuyển động (Duration, Easing curve, Delay), thiết bị thử nghiệm đo lường FPS.\n- **Quyền hạn truy cập:** Quyền sửa đổi CSS animations và motion scripts.",
        "concepts": "- **Compositor-Only Properties:** Chỉ hoạt họa hóa các thuộc tính `transform` và `opacity` để trình duyệt thực thi trên GPU mà không kích hoạt Layout và Paint.\n- **Choreography Timing Tokens:** Sử dụng các token thời gian chuẩn hóa: Micro (100-150ms), Macro (200-300ms), Complex (400-500ms).\n- **WCAG 2.3.3 Animation from Interactions:** Tôn trọng truy vấn `prefers-reduced-motion: reduce` bằng cách vô hiệu hóa hoặc thay thế chuyển động dịch chuyển bằng hiệu ứng fade đơn giản.",
        "workflow": "1. Xây dựng kịch bản chuyển cảnh (Storyboard) chi tiết cho từng giai đoạn: Enter, Active, Exit.\n2. Lựa chọn đường cong chuyển động (Easing Bézier) phù hợp với tính chất vật lý của thương hiệu.\n3. Viết mã CSS hoặc Framer Motion chỉ sử dụng `transform` và `opacity`.\n4. Bổ sung truy vấn `@media (prefers-reduced-motion: reduce)` để tắt hoàn toàn các chuyển động di chuyển lớn.\n5. Đo lường hiệu năng chuyển động bằng Chrome DevTools Rendering Panel, bảo đảm đạt 60fps ổn định.\n6. Xuất mã token chuyển động vào hệ thống Design Token dùng chung.",
        "examples": """### Khai báo Animation mượt mà và tôn trọng cài đặt giảm chuyển động:
```css
/* Đường cong chuyển dịch tiêu chuẩn */
:root {
  --motion-duration-enter: 250ms;
  --motion-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-dialog {
  opacity: 1;
  transform: translateY(0) scale(1);
  transition: opacity var(--motion-duration-enter) ease-out,
              transform var(--motion-duration-enter) var(--motion-ease-out);
  will-change: transform, opacity;
}

/* Vô hiệu hóa chuyển động cho người dùng nhạy cảm tiền đình */
@media (prefers-reduced-motion: reduce) {
  .modal-dialog {
    transition: opacity 150ms ease-in-out !important;
    transform: none !important;
  }
}
```""",
        "antipatterns": "- **Animating Layout Triggers:** Hoạt họa hóa các thuộc tính `top`, `left`, `width`, `height`, `margin` khiến CPU liên tục tính toán lại layout (Reflow) gây giật màn hình.\n- **Ignoring Reduced Motion:** Không hỗ trợ `prefers-reduced-motion` gây khó chịu nghiêm trọng cho người dùng mắc chứng nhạy cảm chuyển động.\n- **Endless Uncontrolled Spinners:** Để các hiệu ứng xoay tròn hoạt động liên tục trong nền làm hao pin thiết bị di động.",
        "gates": "- **QG-01**: Tốc độ khung hình duy trì ổn định 60fps trong suốt quá trình thực thi hiệu ứng.\n- **QG-03**: 100% hiệu ứng chuyển động đều bị tắt hoặc chuyển sang fade-in khi kích hoạt `prefers-reduced-motion: reduce`.\n- **QG-05**: Không có thuộc tính gây Layout hoặc Paint nào bị đưa vào danh sách transition.",
        "security": "- Tránh các hiệu ứng nhấp nháy vượt quá 3 lần/giây để ngăn ngừa nguy cơ co giật do nhạy cảm ánh sáng (Photosensitive Seizures - WCAG 2.3.1).",
        "adapters": "- **Libraries**: Framer Motion, GSAP, Web Animations API (WAAPI), CSS Animations.",
        "deliverables": "- Bảng đặc tả Storyboard và Motion Tokens.\n- Module CSS/TS Animation hiệu năng cao.\n- Báo cáo kiểm thử FPS và tuân thủ WCAG Motion.",
        "related": "dex-60fps-web-animation, dex-component-state-matrix, dex-perceived-performance-patterns",
        "usage": """```powershell
# Kiểm tra hỗ trợ prefers-reduced-motion tự động bằng Playwright
npx playwright test tests/a11y/reduced-motion.spec.ts

# Ghi lại dấu vết hiệu năng chuyển động bằng Chrome Trace
npx lighthouse http://localhost:3000 --only-categories=performance
```"""
    },
    {
        "id": "dex-chart-visualization-accessibility",
        "name": "dex-chart-visualization-accessibility",
        "desc": "Engineer accessible, keyboard-navigable data visualizations and charts with high-contrast color palettes, tactile pattern textures, screen reader summaries, and alternative tabular representations. Use when building enterprise reporting and data dashboards.",
        "purpose": "Thiết kế và triển khai các biểu đồ dữ liệu có khả năng tiếp cận cao (Accessible Charts); hỗ trợ điều hướng bàn phím, bảng màu tương phản thân thiện với người mù màu, hoa văn kết cấu (patterns), mô tả tóm tắt cho screen reader và chế độ xem bảng dữ liệu thay thế.",
        "when_use": "- Khi các biểu đồ trong báo cáo chỉ phân biệt các chuỗi dữ liệu bằng màu sắc khiến người mù màu không đọc được.\n- Khi người dùng sử dụng bàn phím không thể tương tác hoặc kiểm tra dữ liệu chi tiết của từng điểm dữ liệu trên biểu đồ.\n- Khi hệ thống kiểm toán yêu cầu tuân thủ đầy đủ WCAG 2.2 AA cho các công cụ trực quan hóa dữ liệu.",
        "when_not_use": "- Khi hình ảnh trực quan chỉ là hình minh họa trang trí thuần túy (decorative icons) không mang giá trị thông tin số liệu.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Thư viện biểu đồ (D3, Chart.js, Recharts, ECharts), bộ dữ liệu định dạng JSON.\n- **Quyền hạn truy cập:** Quyền sửa đổi component trực quan hóa dữ liệu.",
        "concepts": "- **Color-Blind Safe Palettes:** Bộ màu được thiết kế để phân biệt rõ ràng dưới các hội chứng mù màu phổ biến (Protanopia, Deuteranopia, Tritanopia).\n- **Pattern Fills:** Bổ sung các đường sọc chéo, chấm bi hoặc nét đứt vào các thanh biểu đồ để phân biệt chuỗi dữ liệu mà không phụ thuộc vào màu sắc.\n- **Accessible Data Table Alternative:** Luôn cung cấp một nút bấm để chuyển đổi linh hoạt giữa biểu đồ đồ họa và bảng số liệu HTML ngữ nghĩa (`<table>`).",
        "workflow": "1. Lựa chọn bảng màu biểu đồ an toàn với người mù màu có độ tương phản tối thiểu 3:1 so với nền.\n2. Tích hợp hoa văn họa tiết (SVG patterns) cho các vùng diện tích hoặc các cột biểu đồ.\n3. Cấu hình cấu trúc SVG ngữ nghĩa: gắn thẻ `<title>`, `<desc>` và các thuộc tính `role=\"graphics-document\"`.\n4. Bổ sung hỗ trợ điều hướng bằng phím mũi tên giữa các điểm dữ liệu và thông báo giá trị qua `aria-live`.\n5. Cung cấp nút chuyển đổi hiển thị bảng dữ liệu thay thế kèm chức năng tải file CSV.\n6. Kiểm thử biểu đồ với công cụ giả lập mù màu và phần mềm đọc màn hình NVDA / VoiceOver.",
        "examples": """### Tạo biểu đồ cột SVG có hỗ trợ Pattern và Screen Reader:
```html
<svg role="graphics-document" aria-label="Biểu đồ doanh thu quý 1 đến quý 4" viewBox="0 0 400 200">
  <defs>
    <!-- Hoa văn sọc chéo để phân biệt không cần màu -->
    <pattern id="diagonal-stripe" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#1e293b" stroke-width="2" />
    </pattern>
  </defs>
  
  <rect x="50" y="50" width="40" height="150" fill="url(#diagonal-stripe)" 
        tabindex="0" role="graphics-symbol" aria-label="Quý 1: 150 triệu VNĐ" />
  <rect x="120" y="30" width="40" height="170" fill="#3b82f6" 
        tabindex="0" role="graphics-symbol" aria-label="Quý 2: 170 triệu VNĐ" />
</svg>

<button type="button" aria-expanded="false" onclick="toggleTableView()">
  Xem dưới dạng bảng số liệu
</button>
```""",
        "antipatterns": "- **Color-Only Encoding:** Phân biệt 5 đường biểu đồ khác nhau chỉ bằng các sắc thái màu xanh lá cây và đỏ.\n- **Canvas Black Box:** Vẽ biểu đồ lên thẻ `<canvas>` mà không cung cấp cấu trúc DOM dự phòng hoặc mô tả văn bản thay thế.\n- **Hover-Only Data Tooltips:** Chỉ hiển thị giá trị số liệu khi di chuột, khiến người dùng duyệt bằng bàn phím hoàn toàn không thể tiếp cận.",
        "gates": "- **QG-01**: Mọi biểu đồ đều có chế độ xem bảng dữ liệu HTML thay thế hoặc bản mô tả tóm tắt số liệu.\n- **QG-03**: Tất cả các điểm dữ liệu đều có thể nhận focus và đọc được thông tin bằng bàn phím.\n- **QG-06**: Bảng màu vượt qua bài kiểm tra mô phỏng mù màu không có chuỗi dữ liệu nào bị trùng độ sáng.",
        "security": "- Tránh đưa dữ liệu chưa khử khuẩn vào các nhãn tooltip SVG để ngăn ngừa lỗ hổng DOM-based XSS.",
        "adapters": "- **Chart Libraries**: D3.js, Chart.js, Recharts, Observable Plot, Highcharts Highcharts-A11y.",
        "deliverables": "- Component biểu đồ tích hợp hỗ trợ a11y đầy đủ.\n- Bảng màu tương thích mù màu và bộ SVG patterns.\n- Chế độ xem bảng dữ liệu dự phòng có thể chuyển đổi.",
        "related": "dex-wcag-compliance-audit, dex-high-density-dashboard-layout, dex-component-state-matrix",
        "usage": """```powershell
# Kiểm toán khả năng tiếp cận biểu đồ bằng axe-core
npx cypress run --spec "cypress/e2e/chart-a11y.cy.ts"

# Kiểm tra phân biệt màu sắc với công cụ giả lập mù màu
npx pa11y http://localhost:3000/reports/sales --reporter json
```"""
    },
    {
        "id": "dex-perceived-performance-patterns",
        "name": "dex-perceived-performance-patterns",
        "desc": "Engineer perceived performance optimization strategies including skeleton screens, optimistic UI updates, staggered micro-transitions, and instant interaction feedback. Use when improving user-facing responsiveness during network latency.",
        "purpose": "Thiết kế và lập trình các chiến lược tối ưu hóa hiệu năng cảm nhận (Perceived Performance); áp dụng màn hình khung xương (skeleton screens), cập nhật giao diện lạc quan (optimistic UI), hiệu ứng vi chuyển đổi so le và phản hồi xúc giác ngay lập tức để xóa bỏ cảm giác chờ đợi do độ trễ mạng.",
        "when_use": "- Khi các thao tác mạng (lưu dữ liệu, thích bài viết, gửi tin nhắn) có độ trễ từ 300ms - 2000ms gây gián đoạn trải nghiệm.\n- Khi màn hình trắng xuất hiện trong lúc tải dữ liệu ban đầu khiến người dùng nghĩ ứng dụng bị treo.\n- Khi cần nâng cao chỉ số Interaction to Next Paint (INP) và Core Web Vitals.",
        "when_not_use": "- Khi thao tác mang tính rủi ro cao hoặc không thể đảo ngược (như thanh toán tiền, xóa tài khoản vĩnh viễn) đòi hỏi phải chờ xác nhận từ server.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Luồng tương tác người dùng, API endpoints có độ trễ cao, thư viện quản lý trạng thái (React Query, SWR, Zustand).\n- **Quyền hạn truy cập:** Quyền sửa đổi logic tương tác frontend và component loading.",
        "concepts": "- **Optimistic UI:** Cập nhật giao diện ngay lập tức như thể yêu cầu đã thành công trên máy chủ; tự động khôi phục (rollback) và hiển thị thông báo lỗi nếu API thất bại.\n- **Skeleton Screens vs. Spinners:** Màn hình khung xương tạo cảm giác nội dung đang dần hiển thị và giảm thời gian chờ đợi nhận thức so với con trỏ xoay vòng đơn điệu.\n- **Immediate Visual Feedback:** Cung cấp phản hồi xúc giác/thị giác trong vòng 50-100ms sau khi người dùng bấm chuột.",
        "workflow": "1. Khảo sát các điểm chạm tương tác có độ trễ lớn trong ứng dụng.\n2. Thiết kế skeleton screen có cấu trúc hình học khớp chính xác với nội dung thực tế để tránh xô lệch layout (CLS).\n3. Triển khai cơ chế Optimistic Updates cho các thao tác like, bookmark, toggle, hoặc gửi bình luận.\n4. Cài đặt cơ chế khôi phục trạng thái (rollback) an toàn kèm thông báo Toast khi request gặp lỗi.\n5. Áp dụng hiệu ứng xuất hiện so le (staggered animations) nhẹ nhàng cho danh sách nội dung mới tải về.\n6. Đo lường chỉ số thời gian tương tác cảm nhận và tỷ lệ người dùng thoát trang do chờ đợi.",
        "examples": """### Cập nhật giao diện lạc quan (Optimistic Update) với TanStack Query:
```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function useOptimisticLike(postId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newLikedState: boolean) => api.toggleLike(postId, newLikedState),
    onMutate: async (newLikedState) => {
      // Hủy bỏ các truy vấn đang thực thi để tránh ghi đè dữ liệu lạc quan
      await queryClient.cancelQueries({ queryKey: ['post', postId] });
      const previousPost = queryClient.getQueryData(['post', postId]);

      // Cập nhật ngay lập tức giao diện người dùng
      queryClient.setQueryData(['post', postId], (old: any) => ({
        ...old,
        isLiked: newLikedState,
        likesCount: old.likesCount + (newLikedState ? 1 : -1),
      }));

      return { previousPost };
    },
    onError: (err, newLikedState, context) => {
      // Khôi phục lại trạng thái cũ nếu server báo lỗi
      if (context?.previousPost) {
        queryClient.setQueryData(['post', postId], context.previousPost);
      }
    },
  });
}
```""",
        "antipatterns": "- **Skeleton Layout Mismatch:** Kích thước skeleton không khớp với nội dung thực tế làm layout bị nhảy mạnh khi tải xong (gây tăng điểm CLS).\n- **Optimistic Financial Transactions:** Tự ý hiển thị trạng thái chuyển tiền thành công trước khi có xác nhận từ cổng thanh toán.\n- **Silent Rollback Without Feedback:** Khôi phục trạng thái cũ khi gặp lỗi mà không đưa ra bất kỳ thông báo nào cho người dùng biết thao tác đã thất bại.",
        "gates": "- **QG-01**: Phản hồi thị giác tức thì xuất hiện trong vòng dưới 100ms kể từ khi người dùng click.\n- **QG-03**: Cơ chế rollback hoạt động chính xác 100% trong điều kiện mạng giả lập ngoại tuyến (offline).\n- **QG-05**: Không làm tăng điểm số CLS (Cumulative Layout Shift giữ ở mức < 0.1).",
        "security": "- Đảm bảo các dữ liệu hiển thị lạc quan không làm lộ thông tin bảo mật trước khi được server xác thực quyền truy cập.",
        "adapters": "- **Data Fetching**: TanStack Query, SWR, Apollo Client.\n- **Animation**: CSS animations, Framer Motion.",
        "deliverables": "- Component Skeleton Screen khớp layout.\n- Hooks xử lý Optimistic UI kèm logic rollback hoàn chỉnh.\n- Báo cáo đo lường Core Web Vitals (INP, CLS).",
        "related": "dex-60fps-web-animation, dex-component-state-matrix, dex-high-density-dashboard-layout",
        "usage": """```powershell
# Kiểm tra chỉ số Interaction to Next Paint (INP) bằng Lighthouse CLI
npx lighthouse http://localhost:3000 --only-categories=performance

# Giả lập nghẽn mạng chậm và kiểm tra cơ chế rollback giao diện
npx playwright test tests/e2e/optimistic-ui.spec.ts
```"""
    },
    {
        "id": "dex-cross-platform-ui-parity",
        "name": "dex-cross-platform-ui-parity",
        "desc": "Establish and automate cross-platform design parity audits across Web, iOS, Android, and Desktop ensuring consistent brand expression while honoring native platform UX conventions. Use when maintaining multi-platform product suites.",
        "purpose": "Thiết lập quy trình kiểm toán và tự động hóa tính tương đương về thiết kế đa nền tảng (Cross-Platform UI Parity) giữa Web, iOS, Android và Desktop; bảo đảm trải nghiệm thương hiệu đồng nhất trong khi vẫn tôn trọng các quy ước UX bản địa của từng hệ điều hành.",
        "when_use": "- Khi phát triển song song ứng dụng trên nhiều nền tảng (React Web, React Native / Flutter, Swift iOS, Kotlin Android).\n- Khi người dùng phản ánh tính năng hoặc giao diện trên Android hoạt động khác biệt bất thường so với iOS.\n- Khi đồng bộ hóa hệ thống Design System giữa các nền tảng công nghệ khác nhau.",
        "when_not_use": "- Khi ứng dụng được thiết kế độc quyền cho một hệ điều hành duy nhất và tận dụng toàn bộ các API đặc thù của hệ điều hành đó.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Bản thiết kế giao diện đa nền tảng, mã nguồn các ứng dụng client, danh mục tiêu chí đánh giá quy ước UX.\n- **Quyền hạn truy cập:** Quyền truy cập các repository ứng dụng Web, iOS và Android.",
        "concepts": "- **Brand Consistency vs. Platform Conventions:** Giữ nguyên các giá trị cốt lõi của thương hiệu (màu sắc, typography, giọng điệu) nhưng tôn trọng quy ước nền tảng (nút Back trên Android, thanh Navigation Bar dưới đáy của iOS, Context Menu trên Desktop).\n- **Parity Scorecard:** Bảng điểm đánh giá mức độ tương đương về tính năng, bố cục, luồng thao tác và khả năng tiếp cận giữa các nền tảng.\n- **Token Mapping Layer:** Ánh xạ cùng một bộ Design Tokens sang các định dạng native: CSS Variables (Web), XML/Compose Colors (Android), Assets Catalogs / Swift (iOS).",
        "workflow": "1. Xây dựng ma trận tính năng và màn hình đối sánh giữa Web, iOS, Android và Desktop.\n2. Rà soát sự khác biệt về quy ước tương tác (Back button, Pull-to-refresh, Bottom Sheet vs Modal).\n3. Tự động hóa quá trình xuất token từ nguồn duy nhất (Single Source of Truth) tới tất cả các nền tảng client.\n4. Thực hiện chụp màn hình tự động (Visual Snapshots) trên các thiết bị thực tế hoặc giả lập.\n5. Chấm điểm độ tương đương (Parity Index) và gắn cờ các sai lệch về bố cục hoặc hành vi.\n6. Họp đồng bộ giữa các đội ngũ kỹ sư client để thống nhất lộ trình thu hẹp khoảng cách khác biệt.",
        "examples": """### Bảng tiêu chí đánh giá Cross-Platform UI Parity:
| Tiêu chí | Web | iOS (SwiftUI) | Android (Jetpack Compose) | Trạng thái Parity |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Color** | `--color-brand-600` | `Color("Brand600")` | `MaterialTheme.colorScheme.primary` | Đạt chuẩn (100%) |
| **Typography Hierarchy** | Inter font scale | San Francisco | Roboto | Đạt chuẩn (Native) |
| **Navigation Pattern** | Top Header / Sidebar | Bottom TabBar | Bottom Navigation / Rail | Chuẩn quy ước |
| **Modal / Dialog** | Centered Modal Dialog | Action Sheet / Sheet | Bottom Sheet / AlertDialog | Chuẩn quy ước |
| **Swipe Dismiss** | Nút đóng rõ ràng | Vuốt xuống để đóng | Nút Back phần cứng/cử chỉ | Đạt chuẩn |
""",
        "antipatterns": "- **Force iOS Patterns on Android:** Bắt buộc giao diện Android phải dùng thanh điều hướng và biểu tượng của iOS làm người dùng Android xa lạ.\n- **Divergent Token Releases:** Cập nhật bảng màu trên Web nhưng bỏ quên ứng dụng Mobile trong 6 tháng khiến nhận diện thương hiệu bị phân mảnh.\n- **Ignoring Desktop Scaling:** Mang nguyên vẹn giao diện ứng dụng di động kéo dãn lên màn hình Desktop 4K mà không tối ưu mật độ hiển thị.",
        "gates": "- **QG-01**: 100% token thương hiệu (Brand Colors, Typography Scale) được phân phối đồng bộ từ cùng một nguồn mã nguồn.\n- **QG-04**: Điểm số Parity Scorecard giữa các nền tảng đạt tối thiểu 90% tính năng cốt lõi.\n- **QG-07**: Không có vi phạm quy ước cơ bản của hệ điều hành (như thiếu hỗ trợ nút Back trên Android).",
        "security": "- Bảo đảm các chính sách bảo mật sinh trắc học (FaceID, TouchID, Android Biometric) được triển khai nhất quán và an toàn trên các phiên bản client.",
        "adapters": "- **Build & Sync**: Style Dictionary, Fastlane, GitHub Actions.\n- **Testing**: Appium, Maestro, Percy, BrowserStack.",
        "deliverables": "- Ma trận đánh giá Cross-Platform UI Parity.\n- Pipeline đồng bộ hóa Design Tokens đa nền tảng.\n- Bộ kịch bản kiểm thử trực quan trên thiết bị thực tế.",
        "related": "dex-design-token-migration, dex-component-state-matrix, dex-mobile-first-responsive-patterns",
        "usage": """```powershell
# Chạy kiểm thử tự động so sánh giao diện đa nền tảng với Maestro
maestro test .maestro/cross-platform-flow.yaml

# Xuất tokens đồng bộ cho Web, iOS và Android
npm run build-tokens-all-platforms
```"""
    },

    # =========================================================================
    # GROUP AJ: Authorized Software Inspection & Binary Review (Skills 351–360)
    # =========================================================================
    {
        "id": "dex-binary-provenance-matching",
        "name": "dex-binary-provenance-matching",
        "desc": "Verify cryptographic provenance, build attestation signatures, and SLSA Level 3/4 compliance between compiled executable binaries and their authoritative source repositories. Use when conducting authorized supply-chain security audits.",
        "purpose": "Xác minh nguồn gốc mật mã (Cryptographic Provenance), chữ ký chứng thực bản dựng (Build Attestation) và mức độ tuân thủ tiêu chuẩn SLSA giữa file thực thi nhị phân đã biên dịch và kho mã nguồn gốc; ngăn ngừa các nguy cơ chèn mã độc trong chuỗi cung ứng phần mềm.",
        "when_use": "- Khi kiểm toán an ninh chuỗi cung ứng trước khi triển khai các file nhị phân của bên thứ ba vào môi trường production.\n- Khi xác minh tính xác thực của các bản phát hành nhị phân từ các dự án mã nguồn mở.\n- Khi triển khai quy chuẩn SLSA (Supply-chain Levels for Software Artifacts) cho pipeline CI/CD nội bộ.",
        "when_not_use": "- Khi tiến hành kiểm thử các bản dựng thử nghiệm nội bộ cục bộ không yêu cầu chứng thực nguồn gốc.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File nhị phân mục tiêu (ELF, PE, Mach-O), file chữ ký số, chứng chỉ x509, hoặc bản ghi in-toto / Sigstore Cosign attestation.\n- **Quyền hạn truy cập:** Quyền chạy công cụ phân tích nhị phân và truy cập transparency log (Rekor).",
        "concepts": "- **SLSA Attestation:** Bản ghi chứng nhận bản dựng được ký số mô tả quy trình, môi trường và commit SHA đã tạo ra artifact.\n- **Sigstore / Cosign:** Công nghệ ký số không khóa (keyless signing) dựa trên OpenID Connect và nhật ký minh bạch Rekor.\n- **Deterministic Hash Matching:** So sánh mã băm SHA-256 của file nhị phân với bản ghi đã công bố trên kênh phân phối chính thức.",
        "workflow": "1. Trích xuất mã băm mật mã (SHA-256, SHA-512) của file nhị phân mục tiêu.\n2. Truy vấn chứng thực bản dựng (attestation predicate) từ Sigstore Rekor log hoặc tệp `.attestation` đính kèm.\n3. Kiểm tra tính hợp lệ của chuỗi chứng chỉ x509 và danh tính người ký (OIDC Issuer, Repository Workflow).\n4. So sánh commit SHA được ghi nhận trong attestation với commit trên authoritative git branch.\n5. Đối chiếu môi trường build (GitHub Actions runner, hardened builder container) với chính sách SLSA yêu cầu.\n6. Lập báo cáo kết luận mức độ tin cậy và chứng chỉ xuất xứ của file nhị phân.",
        "examples": """### Xác minh chữ ký và chứng thực xuất xứ bằng Cosign:
```powershell
# Xác minh chữ ký bản dựng nhị phân qua Sigstore
cosign verify-blob `
  --certificate ./release-binary.cert `
  --signature ./release-binary.sig `
  --certificate-identity "https://github.com/my-org/my-repo/.github/workflows/release.yml@refs/heads/main" `
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" `
  ./target-executable.exe

# Kiểm tra bản ghi chứng thực nguồn gốc SLSA
cosign verify-blob-attestation `
  --type slsaprovenance `
  --certificate ./release-binary.cert `
  --signature ./release-binary.attestation `
  ./target-executable.exe
```""",
        "antipatterns": "- **Blind Hash Download:** Tải file hash từ cùng một máy chủ không bảo mật với file nhị phân mà không có xác thực chữ ký PGP/Cosign độc lập.\n- **Ignoring Builder Identity:** Chỉ kiểm tra file có chữ ký nhưng không xác minh danh tính người ký có thuộc tổ chức được ủy quyền hay không.\n- **Trusting Modifiable Tags:** Xác minh bản dựng dựa trên Git Tag thay vì dùng Git Commit SHA bất biến.",
        "gates": "- **QG-01**: Chữ ký số và chuỗi chứng chỉ x509 của file nhị phân hoàn toàn hợp lệ.\n- **QG-04**: Bản chứng thực nguồn gốc (attestation) liên kết chính xác tới commit SHA trong kho mã nguồn chính thức.\n- **QG-09**: Mức độ tuân thủ SLSA đạt tối thiểu Level 3 (bản dựng được tạo từ môi trường cô lập, không thể sửa đổi).",
        "security": "- Cảnh báo và cô lập ngay lập tức các tệp nhị phân có chữ ký không hợp lệ hoặc danh tính người ký không trùng khớp với tác giả chính thức.",
        "adapters": "- **Tools**: Cosign, Rekor CLI, in-toto, slsa-verifier, GitHub CLI (`gh attestation verify`).",
        "deliverables": "- Báo cáo xác minh nguồn gốc mật mã của file nhị phân.\n- Bản sao dữ liệu attestation đã được giải mã.\n- Chứng chỉ kết quả kiểm toán tuân thủ SLSA.",
        "related": "dex-reproducible-build-audit, dex-software-license-compliance-scan, dex-sbom-binary-correlation",
        "usage": """```powershell
# Xác minh attestation bản dựng bằng GitHub CLI
gh attestation verify target-binary.tar.gz --repo my-org/my-repo

# Kiểm tra mã băm SHA256 đối chiếu
Get-FileHash -Algorithm SHA256 ./target-binary.tar.gz
```"""
    },
    {
        "id": "dex-debug-symbols-correlation",
        "name": "dex-debug-symbols-correlation",
        "desc": "Correlate stripped and unstripped binaries with debug symbols (PDB, DWARF, dSYM) to reconstruct call stacks, demangle symbols, and verify source-code mapping accuracy. Use when triaging native crash dumps and conducting authorized binary analysis.",
        "purpose": "Tương quan và liên kết giữa file nhị phân đã tước bỏ ký hiệu (stripped) với kho debug symbols (PDB, DWARF, dSYM); tái tạo call stack chính xác, giải mã tên hàm (symbol demangling) và xác thực tính khớp đúng của source code mapping phục vụ điều tra sự cố crash hoặc phân tích nhị phân được ủy quyền.",
        "when_use": "- Khi phân tích các file crash dump (minidump `.dmp`, core dump) từ môi trường sản xuất không có mã nguồn đi kèm.\n- Khi xác minh symbol server có cung cấp đúng phiên bản PDB/DWARF khớp với bản build nhị phân đang chạy hay không.\n- Khi kiểm toán tính bảo mật để đảm bảo file nhị phân thương mại đã được tước bỏ hoàn toàn thông tin đường dẫn nhạy cảm.",
        "when_not_use": "- Khi làm việc với các ngôn ngữ thông dịch (Python, JavaScript) đã có source maps ở định dạng web chuẩn.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File nhị phân thực thi, tệp debug symbol tương ứng (.pdb trên Windows, .dwarf/.debug trên Linux, .dSYM trên macOS).\n- **Quyền hạn truy cập:** Quyền chạy công cụ phân tích debug symbols (llvm-symbolizer, dumpbin, gdb, c++filt).",
        "concepts": "- **Debug Identifier / GUID:** Mã định danh duy nhất (RSDS GUID và Age trên Windows PE; Build ID trên Linux ELF) dùng để ghép cặp chính xác giữa binary và symbol file.\n- **Symbol Demangling:** Chuyển đổi tên hàm bị mã hóa nội bộ của compiler (mangled name như `_ZN7MyClass8doActionEi`) về dạng dễ đọc (`MyClass::doAction(int)`).\n- **Stripping Verification:** Kiểm tra bảo đảm các bảng ký hiệu không cần thiết đã được loại bỏ khỏi file phát hành thương mại.",
        "workflow": "1. Trích xuất Build ID (Linux) hoặc Debug Directory RSDS GUID (Windows) từ file nhị phân mục tiêu.\n2. Tìm kiếm và nạp tệp debug symbols (DWARF/PDB) có mã định danh khớp chính xác từ Symbol Server.\n3. Đối chiếu địa chỉ bộ nhớ tương đối (RVA) trong crash dump với các hàm và dòng code trong source map.\n4. Thực hiện demangle tên các hàm C++/Rust để tái cấu trúc cây gọi hàm (Call Stack).\n5. Kiểm tra rà soát các đường dẫn file mã nguồn nhúng trong symbol để phát hiện lộ lọt cấu trúc thư mục nội bộ.\n6. Tổng hợp báo cáo tương quan ký hiệu và cấu trúc ngăn xếp điều tra.",
        "examples": """### Kiểm tra RSDS GUID và demangle symbol:
```powershell
# Kiểm tra thông tin Debug Directory của file PE trên Windows
dumpbin /HEADERS /LOADCONFIG ./app.exe | Select-String -Pattern "RSDS", "Format"

# Demangle ký hiệu C++ bị mã hóa
c++filt _ZN4Core8Database10initializeERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
# Kết quả: Core::Database::initialize(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)

# Tương quan địa chỉ crash với mã nguồn bằng llvm-symbolizer
llvm-symbolizer --obj=./app.elf 0x401124
```""",
        "antipatterns": "- **Mismatched Symbol Age:** Dùng file PDB có cùng tên nhưng khác phiên bản build khiến call stack bị dịch chuyển sai địa chỉ dòng code.\n- **Leaking Internal Paths:** Để nguyên đường dẫn ổ đĩa phát triển tuyệt đối (`C:\\Users\\admin\\SecretProject\\src`) trong file nhị phân phát hành ra ngoài.\n- **Ignoring Optimization Inlining:** Quên tính toán các hàm đã bị trình biên dịch inline dẫn tới việc thiếu mắt xích trong cây gọi hàm.",
        "gates": "- **QG-01**: Mã GUID / Build ID giữa file nhị phân và file debug symbol khớp tuyệt đối 100%.\n- **QG-04**: Toàn bộ các địa chỉ trong call stack điều tra đều được giải mã thành tên hàm và số dòng code cụ thể.\n- **QG-08**: Bản nhị phân phát hành thương mại không chứa các bảng ký hiệu nội bộ không mong muốn.",
        "security": "- Kiểm tra loại bỏ thông tin nhạy cảm và credentials tình cờ bị nhúng vào bảng chuỗi (string table) của debug symbols.",
        "adapters": "- **Tools**: dumpbin, llvm-symbolizer, c++filt, gdb, WinDbg, symchk, dwarfdump.",
        "deliverables": "- Báo cáo phân giải call stack chi tiết.\n- Bảng đối chiếu mã định danh Build ID / GUID.\n- Khuyến nghị cấu hình compiler flags phục vụ strip symbols an toàn.",
        "related": "dex-binary-provenance-matching, dex-reverse-engineering-reporting, dex-toolchain-reproducibility-audit",
        "usage": """```powershell
# Xác thực tính tương thích của symbol PDB trên Windows
symchk /v ./app.exe /s C:\\Symbols

# Kiểm tra Build ID của file nhị phân Linux ELF
readelf -n ./app.elf | grep "Build ID"
```"""
    },
    {
        "id": "dex-toolchain-reproducibility-audit",
        "name": "dex-toolchain-reproducibility-audit",
        "desc": "Audit build environments, toolchain configurations, timestamp non-determinism, and compilation flags to achieve bit-for-bit reproducible builds. Use when certifying supply chain integrity and eliminating compiler backdoors.",
        "purpose": "Kiểm toán môi trường build, cấu hình toolchain, các yếu tố bất định (timestamps, thứ tự file, biến môi trường) và cờ biên dịch để đạt được khả năng tái tạo bản dựng chuẩn xác đến từng bit (Bit-for-Bit Reproducible Builds); loại trừ nguy cơ chèn mã độc ẩn từ compiler.",
        "when_use": "- Khi chứng nhận an ninh chuỗi cung ứng cho các phần mềm quan trọng (hệ điều hành, ví tiền mã hóa, firmware).\n- Khi hai kỹ sư biên dịch cùng một commit git nhưng sinh ra hai file nhị phân có mã băm SHA-256 khác nhau.\n- Khi xây dựng quy trình kiểm toán độc lập cho phép bên thứ ba tự biên dịch và kiểm chứng artifact.",
        "when_not_use": "- Khi đang trong giai đoạn phát triển tính năng cục bộ (local prototyping) cần tốc độ lặp nhanh mà không quan tâm đến mã băm bản dựng.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Mã nguồn dự án, build scripts (Makefile, CMakeLists.txt, Cargo.toml), môi trường build container hóa.\n- **Quyền hạn truy cập:** Quyền chạy quy trình build lặp lại trong môi trường cô lập.",
        "concepts": "- **Reproducible Builds:** Khả năng tạo ra các file nhị phân giống hệt nhau từng byte khi biên dịch từ cùng một mã nguồn trong cùng điều kiện toolchain.\n- **SOURCE_DATE_EPOCH:** Tiêu chuẩn biến môi trường quy định mốc thời gian cố định thay cho thời gian thực của hệ thống khi đóng gói file.\n- **Diffoscope:** Công cụ phân tích sâu sự khác biệt giữa hai gói nhị phân (archive, executable, container image).",
        "workflow": "1. Thực hiện biên dịch bản dựng lần 1 trong môi trường A (ghi lại mã băm SHA-256).\n2. Thực hiện biên dịch bản dựng lần 2 trong môi trường B có các biến thể có chủ đích (thay đổi múi giờ, tên thư mục, user build).\n3. So sánh mã băm của hai artifact đầu ra; nếu khác biệt, sử dụng `diffoscope` để khoanh vùng nguyên nhân.\n4. Khắc phục các nguồn gây bất định: cố định `SOURCE_DATE_EPOCH`, sắp xếp thứ tự file alphabet trước khi nén, loại bỏ macro `__DATE__` và `__TIME__`.\n5. Cấu hình cờ biên dịch chuẩn hóa đường dẫn (ví dụ: `-ffile-prefix-map` trong GCC/Clang, `--remap-path-prefix` trong Rust).\n6. Đóng gói môi trường build vào container không trạng thái và ban hành hướng dẫn tái tạo độc lập.",
        "examples": """### Thiết lập cờ chuẩn hóa đường dẫn và thời gian cố định:
```bash
# Thiết lập biến môi trường chuẩn hóa thời gian
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)

# Cờ biên dịch GCC / Clang triệt tiêu bất định về đường dẫn và macro thời gian
export CFLAGS="-ffile-prefix-map=$(pwd)=. -Wno-builtin-macro-redefined -D__DATE__=\\\"\\\" -D__TIME__=\\\"\\\""

# Cờ Rust Cargo chuẩn hóa đường dẫn
export RUSTFLAGS="--remap-path-prefix=$(pwd)=/build"

# Chạy so sánh sai khác chi tiết nếu bản dựng không đồng nhất
diffoscope build1/output.tar.gz build2/output.tar.gz --html diff_report.html
```""",
        "antipatterns": "- **Embedded Build Timestamps:** Nhúng trực tiếp thời gian biên dịch vào header của file khiến mỗi lần build đều sinh mã băm khác nhau.\n- **Filesystem Order Dependence:** Đọc danh sách file nguồn bằng hàm duyệt thư mục không sắp xếp thứ tự dẫn tới thứ tự link các object files bị thay đổi.\n- **Unpinned Floating Toolchains:** Sử dụng trình biên dịch phiên bản `latest` thay vì cố định chính xác compiler digest.",
        "gates": "- **QG-01**: Hai lần build độc lập sinh ra file nhị phân có mã băm SHA-256 giống hệt nhau 100%.\n- **QG-04**: Báo cáo diffoscope không phát hiện bất kỳ sự khác biệt nào ngoài những vùng dữ liệu đã được giải trình hợp lý.\n- **QG-09**: Môi trường build hoàn toàn cô lập, không truy cập Internet trong quá trình compile.",
        "security": "- Ngăn ngừa các cuộc tấn công kiểu 'Reflections on Trusting Trust' và mã độc chèn vào toolchain bằng cách cho phép nhiều bên độc lập cùng biên dịch và đối soát mã băm.",
        "adapters": "- **Tools**: diffoscope, reprotest, Docker, Nix, Bazel.",
        "deliverables": "- Container định nghĩa môi trường build tái tạo được.\n- Báo cáo phân tích so sánh bit-for-bit từ diffoscope.\n- Tài liệu hướng dẫn xác minh độc lập cho bên thứ ba.",
        "related": "dex-binary-provenance-matching, dex-reproducible-build-audit, dex-debug-symbols-correlation",
        "usage": """```powershell
# Chạy kiểm toán khả năng tái tạo với reprotest
reprotest --vary=-all "cargo build --release" ./target/release/app

# So sánh nhanh mã băm của 2 bản dựng độc lập
Get-FileHash ./build_a/app.exe, ./build_b/app.exe
```"""
    },
    {
        "id": "dex-installer-package-static-review",
        "name": "dex-installer-package-static-review",
        "desc": "Inspect desktop installer bundles (MSI, NSIS, Inno Setup, PKG, DMG, AppImage) for embedded scripts, privilege escalation risks, persistence mechanisms, and bundled payload integrity. Use when reviewing third-party desktop distributions.",
        "purpose": "Thanh tra và kiểm toán tĩnh các gói cài đặt phần mềm máy tính (MSI, NSIS, Inno Setup, PKG, DMG, AppImage); phát hiện các kịch bản thực thi ngầm, nguy cơ leo thang đặc quyền, cơ chế duy trì persistence bất thường và kiểm tra tính toàn vẹn của các payload đi kèm.",
        "when_use": "- Khi đánh giá an ninh phần mềm của đối tác trước khi cấp phép cài đặt lên máy trạm nhân viên doanh nghiệp.\n- Khi kiểm toán gói cài đặt do chính tổ chức đóng gói để phát hiện các file hoặc registry key thừa thãi.\n- Khi thẩm định các phần mềm thương mại không cung cấp mã nguồn mở.",
        "when_not_use": "- Khi phân tích các ứng dụng SaaS chạy thuần túy trên nền tảng trình duyệt không yêu cầu cài đặt phần mềm cục bộ.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File cài đặt (setup.exe, installer.msi, app.pkg, app.dmg), công cụ trích xuất và phân tích gói.\n- **Quyền hạn truy cập:** Quyền thực thi công cụ giải nén trong môi trường phân tích tĩnh cô lập.",
        "concepts": "- **Custom Actions in MSI:** Các hành động tùy biến trong gói MSI (DLL, VBScript, JScript) thường là nơi ẩn giấu mã độc hoặc các hành vi nguy hiểm.\n- **Persistence Mechanisms:** Các khóa Registry tự khởi động (`Run`, `RunOnce`), Scheduled Tasks hoặc Windows Services được tạo ra trong quá trình cài đặt.\n- **Privilege Demarcation:** Gói cài đặt có đòi quyền Administrator/Root một cách không cần thiết cho các ứng dụng chỉ chạy ở phạm vi người dùng (Per-User Install) hay không.",
        "workflow": "1. Trích xuất toàn bộ nội dung của gói cài đặt mà không thực thi file (sử dụng 7-Zip, lessmsi, innoextract, pkgutil).\n2. Quét toàn bộ mã băm các file thành phần qua cơ sở dữ liệu mẫu mã độc (VirusTotal, nội bộ YARA).\n3. Rà soát các kịch bản cài đặt tùy biến (Custom Actions, NSIS scripts, Pre/Post-install scripts trong PKG).\n4. Kiểm tra các thay đổi cấu hình hệ thống: khóa Registry, biến môi trường PATH, dịch vụ hệ điều hành mới.\n5. Xác minh chữ ký số của gói cài đặt và tất cả các file thực thi nhị phân con bên trong.\n6. Lập báo cáo kiểm toán tĩnh đánh giá mức độ rủi ro và các khuyến nghị an toàn.",
        "examples": """### Trích xuất và kiểm tra gói cài đặt MSI / Inno Setup:
```powershell
# Trích xuất bảng và file từ MSI bằng lessmsi
lessmsi x ./vendor-installer.msi ./extracted_msi/

# Xem danh sách các Custom Actions có thể chứa script can thiệp hệ thống
lessmsi table -t CustomAction ./vendor-installer.msi

# Giải nén gói cài đặt Inno Setup mà không cần chạy file thực thi
innoextract --extract ./setup-inno.exe

# Kiểm tra chữ ký Authenticode của gói cài đặt
Get-AuthenticodeSignature ./vendor-installer.msi
```""",
        "antipatterns": "- **Running Installer to Analyze It:** Nhấp đúp chuột để chạy file cài đặt trên máy làm việc chính thay vì trích xuất tĩnh trong môi trường cô lập.\n- **Ignoring Bundled Dependencies:** Chỉ quét file `.exe` bọc ngoài mà bỏ qua các file DLL hoặc công cụ bên thứ ba nằm nén sâu bên trong gói.\n- **Overprivileged Installation:** Đòi quyền SYSTEM / Administrator cho các tiện ích đơn giản chỉ cần ghi dữ liệu vào thư mục `%LocalAppData%`.",
        "gates": "- **QG-01**: Chữ ký Authenticode / Apple Developer ID của gói cài đặt hoàn toàn hợp lệ.\n- **QG-06**: Không chứa bất kỳ Custom Action nào thực thi các tập lệnh không rõ nguồn gốc (VBScript, PowerShell không ký số).\n- **QG-08**: Toàn bộ các file nhị phân trích xuất đều sạch mã độc và được ghi nhận trong danh mục thành phần.",
        "security": "- Cảnh báo ngay lập tức nếu gói cài đặt cố tình tắt Windows Defender, sửa file hosts hoặc mở cổng tường lửa mà không thông báo cho người dùng.",
        "adapters": "- **Tools**: lessmsi, 7-Zip, innoextract, pkgutil, hdiutil, YARA, Sigcheck.",
        "deliverables": "- Cây thư mục giải nén toàn bộ artifact từ bộ cài.\n- Báo cáo kiểm toán các Custom Actions và Registry keys.\n- Chứng chỉ đánh giá rủi ro an ninh cài đặt.",
        "related": "dex-binary-provenance-matching, dex-sbom-binary-correlation, dex-macos-entitlements-review",
        "usage": """```powershell
# Kiểm tra chi tiết chữ ký số và chứng chỉ của bộ cài
sigcheck.exe -h -vt ./vendor-installer.msi

# Quét các file đã giải nén bằng bộ luật YARA phát hiện persistence
yara -r rules/installer_persistence.yar ./extracted_msi/
```"""
    },
    {
        "id": "dex-sbom-binary-correlation",
        "name": "dex-sbom-binary-correlation",
        "desc": "Correlate declared Software Bill of Materials (SBOM) manifests in CycloneDX or SPDX format with actual strings, embedded libraries, and symbols found inside compiled binaries. Use when verifying supply-chain honesty and identifying undeclared dependencies.",
        "purpose": "Đối chiếu và tương quan giữa danh mục thành phần phần mềm được công bố (SBOM) theo định dạng CycloneDX/SPDX với các chuỗi ký tự, thư viện nhúng và bảng ký hiệu thực tế tìm thấy bên trong file nhị phân đã biên dịch; phát hiện các phụ thuộc khai báo thiếu hoặc mã nguồn mở bị che giấu.",
        "when_use": "- Khi kiểm tra tính trung thực của SBOM do nhà cung cấp phần mềm cung cấp trước khi mua bản quyền.\n- Khi xác minh xem một lỗ hổng bảo mật mới công bố (CVE) có thực sự hiện diện trong file nhị phân đang chạy hay không.\n- Khi kiểm toán tuân thủ bản quyền mã nguồn mở (Open Source License Compliance).",
        "when_not_use": "- Khi dự án là ứng dụng monolith nội bộ đã có quy trình phân tích thành phần phụ thuộc trực tiếp từ lockfiles.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File nhị phân mục tiêu, file SBOM công bố (CycloneDX JSON hoặc SPDX JSON).\n- **Quyền hạn truy cập:** Quyền chạy công cụ quét thành phần nhị phân (Syft, Tern, strings, binwalk).",
        "concepts": "- **Declared vs. Observed SBOM:** Sự khác biệt giữa danh mục thành phần mà nhà phát triển tuyên bố (Declared) và những gì thực sự có mặt trong bản nhị phân cuối cùng (Observed).\n- **Fingerprinting Embedded Libraries:** Nhận diện thư viện C/C++ nhúng tĩnh (static linking) thông qua các chuỗi bản quyền, bảng hằng số mã hóa, hoặc hàm đặc trưng.\n- **PURL (Package URL):** Chuẩn định danh định dạng gói tin duy nhất (`pkg:cargo/tokio@1.28.0`, `pkg:npm/express@4.18.2`).",
        "workflow": "1. Phân tích cú pháp file SBOM công bố (CycloneDX/SPDX) để trích xuất danh sách PURL và phiên bản.\n2. Chạy công cụ phân tích nhị phân (Syft, cve-bin-tool) trực tiếp trên file thực thi để sinh danh mục quan sát được (Observed SBOM).\n3. Thực hiện trích xuất chuỗi ký tự (strings) và bảng import để tìm các dấu hiệu nhận biết thư viện bên thứ ba.\n4. So sánh hai danh mục: gắn cờ các thư viện có trong file nhị phân nhưng không được khai báo trong SBOM (Undeclared Dependencies).\n5. Kiểm tra các thư viện có khai báo trong SBOM nhưng không tìm thấy dấu vết sử dụng (Dead Dependencies).\n6. Xuất báo cáo chênh lệch (SBOM Discrepancy Matrix) kèm đánh giá rủi ro an ninh và bản quyền.",
        "examples": """### Tạo SBOM quan sát từ nhị phân và đối chiếu với SBOM khai báo:
```powershell
# Tạo SBOM thực tế từ file nhị phân bằng Syft
syft packages file:./target-binary.exe -o cyclonedx-json=observed-sbom.json

# Chạy script Python đối chiếu giữa Declared và Observed SBOM
python -c "
import json
with open('declared-sbom.json') as f: dec = json.load(f)
with open('observed-sbom.json') as f: obs = json.load(f)

dec_comps = {c['name'] for c in dec.get('components', [])}
obs_comps = {c['name'] for c in obs.get('components', [])}

undeclared = obs_comps - dec_comps
print(f'Phat hien {len(undeclared)} thu vien khong khai bao: {undeclared}')
"
```""",
        "antipatterns": "- **Trusting Vendor SBOM Unchecked:** Chấp nhận tài liệu SBOM của đối tác mà không có bất kỳ bước kiểm tra đối soát độc lập nào trên file nhị phân thực tế.\n- **Missing Static Links:** Bỏ sót các thư viện C/C++ nhúng tĩnh như OpenSSL, zlib, SQLite được compile trực tiếp vào file thực thi.\n- **Ignoring Outdated Transitive Deps:** Chỉ liệt kê các thư viện cấp 1 mà che giấu các thư viện phụ thuộc bắc cầu chứa lỗ hổng bảo mật.",
        "gates": "- **QG-01**: 100% các thành phần nhị phân bên thứ ba tìm thấy đều có mặt trong SBOM đã phê duyệt.\n- **QG-04**: Không có thư viện nào bị phát hiện sai lệch phiên bản so với bản công bố.\n- **QG-09**: Độ phủ kiểm toán đối chiếu đạt tối thiểu 95% diện tích các file nhị phân phân phối.",
        "security": "- Phát hiện các thành phần phần mềm bị nhiễm mã độc hoặc các phiên bản thư viện đã bị thu hồi (yanked/deprecated) vì lý do bảo mật.",
        "adapters": "- **Tools**: Syft, Grype, cve-bin-tool, Binwalk, CycloneDX CLI, SPDX Tools.",
        "deliverables": "- Ma trận sai lệch SBOM (Declared vs Observed).\n- Danh sách các thư viện nhúng không khai báo.\n- Báo cáo rủi ro lỗ hổng CVE tương ứng với các thành phần thực tế.",
        "related": "dex-binary-provenance-matching, dex-software-license-compliance-scan, dex-dependency-vulnerability-remediation",
        "usage": """```powershell
# Quét lỗ hổng trực tiếp từ file nhị phân bằng Grype
grype file:./target-binary.exe

# Chuyển đổi và chuẩn hóa định dạng SBOM bằng cyclonedx-cli
cyclonedx-cli validate --input-file observed-sbom.json
```"""
    },
    {
        "id": "dex-mobile-permission-surface-diffing",
        "name": "dex-mobile-permission-surface-diffing",
        "desc": "Extract, diff, and risk-score Android manifests (AndroidManifest.xml) and iOS Property Lists (Info.plist) across application releases to detect silent permission creep and capability expansion. Use when conducting mobile app security reviews.",
        "purpose": "Trích xuất, so sánh sai khác (diffing) và chấm điểm rủi ro các quyền hạn ứng dụng di động trong `AndroidManifest.xml` (Android) và `Info.plist` (iOS) qua các phiên bản phát hành; phát hiện hiện tượng leo thang quyền âm thầm (permission creep) và mở rộng bề mặt tấn công không cần thiết.",
        "when_use": "- Khi đánh giá phiên bản cập nhật của ứng dụng di động trước khi duyệt phát hành lên Play Store / App Store.\n- Khi kiểm toán ứng dụng của bên thứ ba để đảm bảo không đòi hỏi quyền vị trí nền, danh bạ, hoặc micro bất thường.\n- Khi triển khai chính sách quyền tối thiểu (Least Privilege) cho các ứng dụng mobile doanh nghiệp.",
        "when_not_use": "- Khi phân tích các ứng dụng backend web API không chạy trên thiết bị di động.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File cài đặt ứng dụng Android (.apk, .aab) hoặc iOS (.ipa), công cụ trích xuất manifest (aapt2, apkanalyzer, plutil).\n- **Quyền hạn truy cập:** Quyền chạy công cụ giải mã và phân tích file cài đặt di động.",
        "concepts": "- **Dangerous Permissions:** Nhóm quyền yêu cầu người dùng cấp phép tại thời điểm chạy (Runtime Permissions) trên Android (Camera, Location, Contacts, Microphone).\n- **Silent Permission Creep:** Việc phiên bản mới âm thầm bổ sung thêm các quyền truy cập nhạy cảm mà người dùng không để ý khi nhấn cập nhật.\n- **Exported Components:** Các Activity, Service, Broadcast Receiver có `android:exported=\"true\"` có thể bị các ứng dụng độc hại khác trên máy gọi tới.",
        "workflow": "1. Giải nén và trích xuất `AndroidManifest.xml` từ file APK bằng `aapt2` hoặc `apktool`.\n2. Trích xuất `Info.plist` và các chuỗi giải thích quyền (`NS...UsageDescription`) từ file IPA.\n3. So sánh danh sách quyền hạn giữa phiên bản hiện tại ($v_N$) và phiên bản trước ($v_{N-1}$).\n4. Chấm điểm rủi ro cho từng quyền mới được bổ sung dựa trên mức độ nhạy cảm dữ liệu.\n5. Kiểm tra tính hợp lệ và minh bạch của chuỗi lý do xin quyền (Usage Descriptions) hiển thị cho người dùng.\n6. Rà soát các thành phần được export để đảm bảo có gắn quyền bảo vệ (custom permission) phù hợp.",
        "examples": """### Trích xuất và so sánh quyền Android bằng aapt2:
```powershell
# Trích xuất danh sách permissions từ file APK v1 và v2
aapt2 dump permissions app-v1.apk > perms-v1.txt
aapt2 dump permissions app-v2.apk > perms-v2.txt

# So sánh sự khác biệt để phát hiện quyền mới được thêm vào
Compare-Object -ReferenceObject (Get-Content perms-v1.txt) -DifferenceObject (Get-Content perms-v2.txt)

# Trích xuất chuỗi lý do xin quyền trên iOS IPA
plutil -p Payload/App.app/Info.plist | Select-String -Pattern "UsageDescription"
```""",
        "antipatterns": "- **Blanket Permissions Request:** Xin toàn bộ các quyền nhạy cảm (Vị trí chính xác, Đọc danh bạ) ngay khi người dùng vừa mở app lần đầu.\n- **Vague Usage Descriptions:** Ghi lý do xin quyền hời hợt như 'Ứng dụng cần quyền này để hoạt động tốt hơn' vi phạm chính sách của Apple App Store.\n- **Unprotected Exported Services:** Đặt `exported=\"true\"` cho Service xử lý thanh toán mà không yêu cầu chữ ký bảo vệ (Signature Permission).",
        "gates": "- **QG-01**: 100% các quyền mới bổ sung đều có văn bản giải trình nghiệp vụ được phê duyệt.\n- **QG-06**: Không có quyền nguy hiểm (Dangerous Permission) nào bị thêm vào mà không thông qua đánh giá an ninh.\n- **QG-08**: Tất cả các trường `NSUsageDescription` trên iOS đều mô tả chi tiết, rõ ràng mục đích sử dụng.",
        "security": "- Chặn đứng việc rò rỉ dữ liệu cá nhân thông qua việc lạm dụng quyền đọc bộ nhớ chung (External Storage) hoặc ghi âm nền.",
        "adapters": "- **Tools**: aapt2, apkanalyzer, apktool, plutil, MobSF, androguard.",
        "deliverables": "- Báo cáo đối chiếu quyền hạn giữa hai phiên bản (Diff Matrix).\n- Bảng chấm điểm rủi ro bề mặt tấn công ứng dụng.\n- Khuyến nghị thu hẹp danh sách quyền về mức tối thiểu cần thiết.",
        "related": "dex-installer-package-static-review, dex-macos-entitlements-review, dex-binary-provenance-matching",
        "usage": """```powershell
# Phân tích tự động APK bằng apkanalyzer
apkanalyzer manifest permissions app-release.apk

# Kiểm tra các components exported không an toàn
python -c "
import xml.etree.ElementTree as ET
# Phân tích file AndroidManifest.xml đã decode
tree = ET.parse('AndroidManifest.xml')
for elem in tree.findall('.//*[@android:exported=\"true\"]', {'android': 'http://schemas.android.com/apk/res/android'}):
    print('Exported component:', elem.tag, elem.attrib)
"
```"""
    },
    {
        "id": "dex-javascript-bundle-obfuscation-audit",
        "name": "dex-javascript-bundle-obfuscation-audit",
        "desc": "Analyze commercial and client-side JavaScript bundles for anti-debugging techniques, control flow flattening, string encryption, and hidden telemetry without violating compliance boundaries. Use when auditing web client security and third-party SDKs.",
        "purpose": "Phân tích và kiểm toán các gói JavaScript bundle thương mại phía client; nhận diện các kỹ thuật làm rối mã nguồn (control flow flattening, mã hóa chuỗi, biến đổi AST), cơ chế chống debug (anti-debugging) và phát hiện các luồng thu thập dữ liệu từ xa (telemetry) tiềm ẩn mà không vi phạm ranh giới pháp lý.",
        "when_use": "- Khi đánh giá rủi ro an ninh của các SDK bên thứ ba nhúng vào website ngân hàng hoặc thương mại điện tử.\n- Khi điều tra các script đáng ngờ được nạp động từ các nhà cung cấp quảng cáo hoặc phân tích dữ liệu.\n- Khi xác minh xem mã nguồn JavaScript nội bộ đã được làm rối và bảo vệ thích đáng trước khi phân phối hay chưa.",
        "when_not_use": "- Khi kiểm toán mã nguồn mở nội bộ đã có sẵn source maps và mã nguồn TypeScript rõ ràng.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File JavaScript bundle (.js), công cụ định dạng và giải mã AST (Babel, Acorn, Prettier, webcrack).\n- **Quyền hạn truy cập:** Quyền phân tích mã nguồn tĩnh trong môi trường trình duyệt sandbox.",
        "concepts": "- **Control Flow Flattening:** Kỹ thuật biến đổi cấu trúc lệnh tuần tự thành một vòng lặp vô hạn kết hợp switch-case lớn để che giấu logic nghiệp vụ.\n- **String Array Encoding:** Lưu trữ toàn bộ chuỗi ký tự vào một mảng toàn cục và truy xuất qua các hàm giải mã phức tạp kèm xoay vòng mảng (array rotation).\n- **Anti-Tampering & Debugger Traps:** Đoạn mã tự động kích hoạt câu lệnh `debugger` liên tục hoặc kiểm tra thời gian thực thi (timing checks) để làm đơ công cụ DevTools.",
        "workflow": "1. Định dạng lại mã nguồn nén (de-minification) bằng Prettier hoặc js-beautify để phục hồi cấu trúc trực quan.\n2. Phân tích cây cú pháp trừu tượng (AST) để phát hiện mảng chuỗi mã hóa và các hàm xoay vòng.\n3. Áp dụng kỹ thuật giải mã hằng số tĩnh (Constant Propagation & Folding) để phục hồi các chuỗi ký tự ban đầu.\n4. Rà soát các bẫy chống debug (`Function('debugger')()`) và vô hiệu hóa chúng trong môi trường phân tích.\n5. Trích xuất toàn bộ các địa chỉ mạng (URLs, Endpoints) và các API gọi ra ngoài (`fetch`, `XMLHttpRequest`, `sendBeacon`).\n6. Lập báo cáo kiểm toán phân loại các hành vi nghiệp vụ thực tế của script.",
        "examples": """### Phục hồi chuỗi mã hóa và làm phẳng AST bằng script Node.js:
```javascript
import { parse } from '@babel/parser';
import traverse from '@babel/traverse';
import generate from '@babel/generator';

// Phân tích AST của bundle bị làm rối
const code = `var _0x12ab = ['Hello', 'World']; console.log(_0x12ab[0]);`;
const ast = parse(code);

traverse(ast, {
  MemberExpression(path) {
    // Thay thế truy xuất mảng hằng số bằng giá trị chuỗi thực tế
    if (path.node.object.name === '_0x12ab' && path.node.property.type === 'NumericLiteral') {
      const index = path.node.property.value;
      path.replaceWith({ type: 'StringLiteral', value: ['Hello', 'World'][index] });
    }
  }
});

const output = generate(ast).code;
console.log('Restored code:', output);
```""",
        "antipatterns": "- **Running Untrusted JS in Live Browser:** Mở trực tiếp script đáng ngờ trên trình duyệt đang đăng nhập tài khoản thực tế thay vì chạy trong sandbox cô lập.\n- **Manual Guessing:** Cố gắng đọc hiểu thủ công hàng chục nghìn dòng lệnh bị làm phẳng luồng mà không dùng công cụ AST.\n- **Tampering with Third-Party Licensers:** Sửa đổi mã nguồn nhằm phá vỡ cơ chế kiểm tra bản quyền trái phép vượt ngoài phạm vi ủy quyền kiểm toán.",
        "gates": "- **QG-01**: 100% các endpoint mạng bên ngoài được trích xuất và phân loại mục đích dữ liệu.\n- **QG-04**: Giải mã thành công tối thiểu 80% các chuỗi ký tự bị mã hóa trong các hàm cốt lõi.\n- **QG-09**: Toàn bộ quá trình phân tích được thực hiện trên môi trường sandbox không có kết nối ra Internet.",
        "security": "- Ngăn ngừa các cuộc tấn công Magecart hoặc chuỗi cung ứng web (Web Supply Chain Attacks) thông qua các SDK phân tích của bên thứ ba.",
        "adapters": "- **Tools**: webcrack, Babel AST, esprima, Prettier, mitmproxy, Chrome DevTools Protocol.",
        "deliverables": "- Mã nguồn JavaScript đã được định dạng và gỡ bỏ một phần làm rối (de-obfuscated).\n- Danh sách toàn bộ các URL, domain và API endpoints được script gọi tới.\n- Báo cáo phân tích rủi ro an ninh và quyền riêng tư dữ liệu.",
        "related": "dex-javascript-bundle-deobfuscation, dex-binary-provenance-matching, dex-sbom-binary-correlation",
        "usage": """```powershell
# Giải mã và làm rõ cấu trúc bundle bằng webcrack
npx webcrack dist/vendor-bundle.js -o deobfuscated_src/

# Quét tìm các chuỗi URL hoặc domain trong mã nguồn phục hồi
Select-String -Path "deobfuscated_src/**/*.js" -Pattern "https?://[a-zA-Z0-9.-]+"
```"""
    },
    {
        "id": "dex-macos-entitlements-review",
        "name": "dex-macos-entitlements-review",
        "desc": "Inspect, diff, and audit macOS application entitlements, sandbox escape vectors, Hardened Runtime configurations, and code signing provisions. Use when conducting macOS application security architecture and compliance reviews.",
        "purpose": "Thanh tra, so sánh và kiểm toán các quyền cấp phép (Entitlements), cấu hình Hardened Runtime, tính toàn vẹn của chữ ký số (Code Signing) và rủi ro thoát hộp cát (Sandbox Escape) trên các ứng dụng macOS (.app); bảo đảm ứng dụng tuân thủ nguyên tắc đặc quyền tối thiểu của Apple.",
        "when_use": "- Khi chuẩn bị nộp ứng dụng macOS lên Mac App Store hoặc phân phối qua cơ chế công chứng (Notarization).\n- Khi kiểm toán an ninh ứng dụng máy tính chạy trên hệ điều hành macOS.\n- Khi phát hiện ứng dụng yêu cầu các quyền hạn nguy hiểm như tắt xác thực thư viện (`com.apple.security.cs.disable-library-validation`).",
        "when_not_use": "- Khi phát triển ứng dụng di động iOS thuần túy hoặc ứng dụng chạy trên máy chủ Linux/Windows.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File ứng dụng macOS (`.app`), chứng chỉ Apple Developer, công cụ dòng lệnh macOS (`codesign`, `security`, `spctl`).\n- **Quyền hạn truy cập:** Quyền thực thi các tiện ích phân tích chữ ký trên máy macOS hoặc môi trường giả lập.",
        "concepts": "- **App Sandbox:** Cơ chế cô lập ứng dụng trong một thư mục sandbox riêng biệt, chỉ được truy cập tài nguyên hệ thống thông qua các quyền khai báo tường minh.\n- **Hardened Runtime:** Cơ chế bảo vệ tính toàn vẹn của tiến trình, ngăn chặn kỹ thuật chèn mã (code injection), can thiệp bộ nhớ hoặc tải thư viện không có chữ ký.\n- **Dangerous Entitlements:** Các quyền làm suy yếu hàng rào bảo vệ như `allow-jit`, `allow-unsigned-executable-memory`, `disable-library-validation`.",
        "workflow": "1. Trích xuất thông tin chữ ký số và trạng thái Notarization của file `.app` bằng `codesign` và `spctl`.\n2. Trích xuất toàn bộ danh sách Entitlements ở định dạng XML Property List.\n3. Rà soát từng entitlement: đối chiếu với yêu cầu nghiệp vụ thực tế của ứng dụng.\n4. Đánh giá rủi ro đặc biệt đối với quyền tắt kiểm tra thư viện (`disable-library-validation`) do có thể bị tấn công DLL Hijacking (Dylib Injection).\n5. Kiểm tra các quyền truy cập phần cứng nhạy cảm: Camera, Microphone, Location, AddressBook.\n6. Lập báo cáo kiểm toán an ninh macOS kèm danh sách các quyền cần thu hồi hoặc thắt chặt.",
        "examples": """### Trích xuất và kiểm toán Entitlements trên macOS:
```bash
# Trích xuất toàn bộ entitlements từ file binary của ứng dụng
codesign -d --entitlements :- /Applications/TargetApp.app/Contents/MacOS/TargetApp

# Kiểm tra trạng thái Hardened Runtime và cờ bảo vệ
codesign -dvvv --deep /Applications/TargetApp.app

# Đánh giá tính hợp lệ với hệ thống Gatekeeper của Apple
spctl --assess --type execute --verbose=4 /Applications/TargetApp.app
```

```xml
<!-- Ví dụ entitlements XML cần kiểm toán kỹ lưỡng -->
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <!-- Rủi ro cao: Cho phép nạp dylib không cùng nhóm chữ ký số -->
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>
```""",
        "antipatterns": "- **Disabling Library Validation by Default:** Tắt xác thực dylib chỉ để tiện debug trong quá trình phát triển nhưng quên gỡ bỏ khi đóng gói release.\n- **Unsandboxed Distribution:** Phân phối ứng dụng không bật App Sandbox mà không có lý do kiến trúc chính đáng.\n- **Temporary Exception Abuse:** Lạm dụng quyền ngoại lệ tạm thời (`com.apple.security.temporary-exception.files.all-files`) để đọc toàn bộ ổ đĩa người dùng.",
        "gates": "- **QG-01**: Ứng dụng vượt qua kiểm tra Gatekeeper (`spctl --assess`) với trạng thái accepted.\n- **QG-06**: Quyền `disable-library-validation` bị cấm tuyệt đối trừ khi có giải trình ngoại lệ kiến trúc bắt buộc.\n- **QG-08**: Tất cả các entitlements khai báo đều tương ứng trực tiếp với tính năng người dùng có thể kiểm chứng.",
        "security": "- Triệt tiêu các nguy cơ tấn công leo thang đặc quyền cục bộ (Local Privilege Escalation) thông qua Dylib Hijacking.",
        "adapters": "- **Tools**: codesign, spctl, security, plutil, otool, dyld_info.",
        "deliverables": "- File XML danh mục entitlements đã được làm sạch.\n- Báo cáo kiểm toán chữ ký số và Hardened Runtime.\n- Bảng đối soát rủi ro các quyền đặc quyền.",
        "related": "dex-installer-package-static-review, dex-mobile-permission-surface-diffing, dex-binary-provenance-matching",
        "usage": """```powershell
# Chạy script Python phân tích cú pháp entitlements XML
python -c "
import plistlib, subprocess
# Trích xuất và đọc entitlements từ app macOS
xml_data = subprocess.check_output(['codesign', '-d', '--entitlements', ':-', '/Applications/TargetApp.app'])
plist = plistlib.loads(xml_data)
for k, v in plist.items():
    print(f'{k} => {v}')
"
```"""
    },
    {
        "id": "dex-firmware-image-structure-diffing",
        "name": "dex-firmware-image-structure-diffing",
        "desc": "Extract, unpack, and structurally compare IoT and embedded firmware images across releases to identify changed partitions, updated kernel modules, modified rootfs assets, and exposed secrets. Use when conducting authorized hardware security reviews.",
        "purpose": "Trích xuất, giải nén và so sánh cấu trúc các ảnh firmware nhúng (IoT, thiết bị mạng, vi điều khiển); xác định các phân vùng bị thay đổi, các kernel modules được cập nhật, tài nguyên rootfs bị chỉnh sửa và phát hiện các khóa bí mật hoặc mật khẩu hardcoded bị lộ qua các bản cập nhật.",
        "when_use": "- Khi kiểm toán an ninh thiết bị IoT trước khi đưa vào hệ thống mạng doanh nghiệp.\n- Khi phân tích bản cập nhật firmware của nhà cung cấp để kiểm tra xem lỗ hổng đã thực sự được vá hay chưa.\n- Khi kiểm tra tính toàn vẹn của firmware tự build so với firmware chuẩn của nhà sản xuất.",
        "when_not_use": "- Khi phân tích các ứng dụng phần mềm thuần túy không có yếu tố nhúng hoặc hệ thống tệp nhị phân nén phần cứng.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File ảnh firmware (.bin, .img, .hex), công cụ trích xuất firmware (binwalk, squashfs-tools, sasquatch).\n- **Quyền hạn truy cập:** Quyền chạy công cụ phân tích nhị phân trong môi trường an toàn.",
        "concepts": "- **Firmware Anatomy:** Cấu trúc điển hình gồm: Bootloader (U-Boot) + Kernel (uImage/zImage) + Root Filesystem (SquashFS, UBIFS, CramFS) + Cấu hình NVRAM.\n- **Signature Entropy Analysis:** Đồ thị entropy giúp phân biệt vùng dữ liệu nén, vùng mã thực thi và vùng mã hóa dữ liệu.\n- **Silent Shadow Updates:** Nhà sản xuất cập nhật tính năng hoặc vá lỗi nhưng không ghi rõ trong changelog chính thức.",
        "workflow": "1. Thực hiện quét chữ ký và tính toán entropy của ảnh firmware bằng `binwalk` để xác định cấu trúc phân vùng.\n2. Trích xuất toàn bộ hệ thống tệp root filesystem (SquashFS / UBIFS) sang thư mục phân tích.\n3. Thực hiện tương tự cho phiên bản firmware trước đó ($v_{N-1}$).\n4. Chạy công cụ so sánh cấu trúc thư mục để phát hiện các file nhị phân, cấu hình, script bị thêm mới hoặc sửa đổi.\n5. Quét tìm các chuỗi nhạy cảm: khóa SSH private keys, mật khẩu shadow, API tokens trong hệ thống tệp đã trích xuất.\n6. Kiểm tra phiên bản Linux kernel và các driver hạt nhân (.ko) để phát hiện các CVE chưa được xử lý.",
        "examples": """### Phân tích và trích xuất hệ thống tệp firmware bằng binwalk:
```bash
# Quét chữ ký cấu trúc bên trong ảnh firmware
binwalk firmware-v2.0.bin

# Trích xuất tự động toàn bộ phân vùng SquashFS
binwalk -e -M firmware-v2.0.bin

# So sánh sai khác cấu trúc hệ thống tệp giữa 2 bản firmware
diff -ruN _firmware-v1.0.bin.extracted/squashfs-root _firmware-v2.0.bin.extracted/squashfs-root > firmware_diff.patch

# Quét tìm SSH keys hoặc chứng chỉ nhúng trong rootfs
find _firmware-v2.0.bin.extracted/ -name "*.pem" -o -name "*.key" -o -name "id_rsa*"
```""",
        "antipatterns": "- **Flashing Directly Without Review:** Nạp trực tiếp firmware mới vào thiết bị phần cứng thực tế mà không qua phân tích tĩnh trước.\n- **Ignoring Monolithic Blobs:** Bỏ qua các phân vùng dữ liệu không nén được mà không kiểm tra entropy để xem liệu chúng có bị mã hóa hay không.\n- **Overlooking Default Credentials:** Quên kiểm tra file `/etc/passwd` và `/etc/shadow` xem có tài khoản backdoor mặc định hay không.",
        "gates": "- **QG-01**: Trích xuất thành công tối thiểu phân vùng root filesystem chính của ảnh firmware.\n- **QG-06**: Không có private key, mật khẩu mặc định hoặc token nhạy cảm nào bị nhúng trong rootfs.\n- **QG-09**: Tất cả các tệp nhị phân thay đổi đều được ghi nhận và đối chiếu với changelog phát hành.",
        "security": "- Ngăn ngừa các lỗ hổng nghiêm trọng cho phép chiếm quyền điều khiển từ xa (RCE) trên các thiết bị biên IoT hoặc router mạng.",
        "adapters": "- **Tools**: binwalk, squashfs-tools, sasquatch, ubi_reader, cve-bin-tool, strings.",
        "deliverables": "- Cây thư mục root filesystem đã được giải nén hoàn chỉnh.\n- Bản so sánh sai khác (patch diff) giữa hai phiên bản firmware.\n- Báo cáo lỗ hổng CVE và các phát hiện khóa bí mật bị lộ.",
        "related": "dex-installer-package-static-review, dex-binary-provenance-matching, dex-reverse-engineering-reporting",
        "usage": """```powershell
# Quét entropy của file firmware để phát hiện vùng dữ liệu mã hóa
binwalk -E firmware.bin

# Tìm kiếm các chuỗi mật khẩu hoặc API keys nhúng
Select-String -Path "_firmware.bin.extracted/**/*" -Pattern "password", "api_key", "secret"
```"""
    },
    {
        "id": "dex-reverse-engineering-reporting",
        "name": "dex-reverse-engineering-reporting",
        "desc": "Synthesize technical findings from disassemblers, decompilers, binary diffing, and dynamic traces into authoritative, verifiable, and legally compliant engineering reports. Use when documenting authorized security assessments and interoperability research.",
        "purpose": "Tổng hợp và biên soạn các phát hiện kỹ thuật từ công cụ dịch ngược (Ghidra, IDA Pro, Binary Ninja), công cụ diffing nhị phân và nhật ký trace động thành các báo cáo kỹ thuật chuẩn mực, có thể kiểm chứng độc lập và tuân thủ đầy đủ khuôn khổ pháp lý; phục vụ đánh giá an ninh được ủy quyền hoặc nghiên cứu khả năng tương tác.",
        "when_use": "- Khi hoàn thành một đợt kiểm toán an ninh nhị phân hoặc dịch ngược phần mềm được ủy quyền hợp pháp.\n- Khi cần giải thích các phát hiện kỹ thuật phức tạp (như buffer overflow, logic flaw) cho cả ban quản lý và đội ngũ kỹ thuật.\n- Khi lưu trữ chuỗi bằng chứng (Chain of Custody) phục vụ các vụ việc pháp lý hoặc giải quyết tranh chấp quyền sở hữu trí tuệ.",
        "when_not_use": "- Khi tiến hành các hoạt động phân tích không được ủy quyền hoặc vi phạm thỏa thuận cấp phép người dùng cuối (EULA).",
        "prereqs": "- **Ngữ cảnh đầu vào:** Nhật ký phân tích từ decompiler, đồ thị luồng điều khiển (CFG), mã băm mẫu thử, biên bản ủy quyền phân tích.\n- **Quyền hạn truy cập:** Quyền tổng hợp tài liệu bảo mật và truy xuất kho lưu trữ bằng chứng.",
        "concepts": "- **Verifiability & Reproducibility:** Mọi nhận định trong báo cáo đều phải đi kèm địa chỉ bộ nhớ cụ thể (RVA), mã giả (pseudocode), hoặc kịch bản tái hiện (PoC) để người khác có thể kiểm chứng độc lập.\n- **Executive Summary vs. Technical Deep-Dive:** Báo cáo phải có phần tóm tắt tác động nghiệp vụ cho lãnh đạo và phần phân tích chi tiết cấp byte cho kỹ sư.\n- **Legal Compliance & Scope Boundaries:** Ghi rõ phạm vi ủy quyền (Scope of Authorization), các điều khoản miễn trừ trách nhiệm và các giới hạn đạo đức nghề nghiệp.",
        "workflow": "1. Thu thập toàn bộ bằng chứng kỹ thuật: mã băm SHA-256 mẫu thử, phiên bản công cụ phân tích, ảnh chụp CFG, đoạn mã giả.\n2. Lập cấu trúc báo cáo chuẩn mực: Tóm tắt tổng quan, Phạm vi công việc, Phương pháp luận, Phát hiện chi tiết, Khuyến nghị khắc phục.\n3. Định dạng các địa chỉ bộ nhớ và mã giả theo quy chuẩn thống nhất (ví dụ: `sub_401000`, `RVA + 0x1200`).\n4. Xếp hạng mức độ nghiêm trọng của từng phát hiện theo chuẩn CVSS v3.1 / v4.0.\n5. Đính kèm hướng dẫn tái tạo từng bước (Step-by-step reproduction guide) có thể kiểm chứng.\n6. Thực hiện bình duyệt chéo (Peer Review) nội bộ trước khi ban hành báo cáo chính thức.",
        "examples": """### Cấu trúc một báo cáo phân tích dịch ngược kỹ thuật chuẩn mực:
```markdown
# Báo Cáo Đánh Giá An Ninh Nhị Phân — Mã Tài Liệu: SEC-REV-2026-01

### 1. Thông Tin Mẫu Phân Tích
- **Tên tệp:** `network_daemon.elf`
- **Mã băm SHA-256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Kiến trúc:** x86_64 ELF (Linux 64-bit, dynamically linked)
- **Công cụ sử dụng:** Ghidra 11.0, GDB 14.1, Diffoscope 250

### 2. Tóm Tắt Phát Hiện (Executive Summary)
Phát hiện lỗ hổng tràn bộ đệm dựa trên ngăn xếp (Stack-based Buffer Overflow) tại hàm xử lý gói tin xác thực `parse_auth_packet()`. Lỗ hổng cho phép kẻ tấn công thực thi mã từ xa (RCE) với quyền root mà không cần đăng nhập.

### 3. Phân Tích Kỹ Thuật Chi Tiết (Technical Deep-Dive)
- **Địa chỉ bộ nhớ:** `0x004018A0` (`parse_auth_packet`)
- **Nguyên nhân cốt lõi:** Sử dụng hàm không an toàn `strcpy` để sao chép dữ liệu người dùng vào bộ đệm cố định 256 bytes trên stack.
```c
// Mã giả trích xuất từ Ghidra tại RVA 0x004018A0:
void parse_auth_packet(char *user_input) {
    char local_buffer[256];
    // Nguy cơ: user_input không được kiểm tra độ dài
    strcpy(local_buffer, user_input);
}
```

### 4. Hướng Dẫn Khắc Phục (Remediation)
Thay thế `strcpy` bằng hàm có giới hạn độ dài an toàn `strncpy(local_buffer, user_input, sizeof(local_buffer) - 1)` hoặc sử dụng các cấu trúc chuỗi có quản lý kích thước.
```""",
        "antipatterns": "- **Speculative Claims:** Đưa ra kết luận lỗ hổng bảo mật dựa trên suy đoán mà không có bằng chứng mã giả hoặc trace cụ thể.\n- **Omitting Sample Hashes:** Không ghi lại mã băm SHA-256 của file nhị phân khiến việc đối chiếu lại mẫu thử trong tương lai bất khả thi.\n- **Disclosing Raw Exploits Without Mitigation:** Cung cấp mã khai thác vũ khí hóa mà không đưa ra giải pháp vá lỗi phòng vệ tương ứng.",
        "gates": "- **QG-01**: 100% mẫu phân tích đều có mã băm SHA-256 bất biến và thông tin môi trường ghi nhận rõ ràng.\n- **QG-04**: Mọi đoạn mã giả trích dẫn đều có địa chỉ bộ nhớ RVA chính xác tương ứng.\n- **QG-09**: Báo cáo có đầy đủ khuyến nghị khắc phục chi tiết cho từng phát hiện được nêu.",
        "security": "- Tuân thủ nghiêm ngặt các quy định về tiết lộ thông tin có trách nhiệm (Coordinated Vulnerability Disclosure) để bảo vệ người dùng cuối.",
        "adapters": "- **Disassemblers**: Ghidra, IDA Pro, Binary Ninja, Radare2.\n- **Documentation**: Markdown, Pandoc, LaTeX, AsciiDoc.",
        "deliverables": "- Báo cáo phân tích dịch ngược kỹ thuật (PDF / Markdown).\n- Kho lưu trữ các đoạn script phân tích và cấu hình IDA/Ghidra database.\n- Bảng ma trận các phát hiện được phân loại theo điểm số CVSS.",
        "related": "dex-debug-symbols-correlation, dex-binary-provenance-matching, dex-firmware-image-structure-diffing",
        "usage": """```powershell
# Chuyển đổi báo cáo Markdown sang tài liệu PDF hoàn chỉnh bằng Pandoc
pandoc reverse_report.md -o reverse_report.pdf --toc --highlight-style=tango

# Xác thực mã băm SHA256 của mẫu thử ghi trong báo cáo
Get-FileHash -Algorithm SHA256 ./samples/target_sample.bin
```"""
    }
]

def generate_skills():
    total = len(SKILLS_AI_AJ)
    created = 0
    print("=== GENERATING GROUP AI & AJ (Skills 341–360) ===")

    for idx, skill in enumerate(SKILLS_AI_AJ, 1):
        skill_id = skill["id"]
        skill_dir = os.path.join(SKILLS_DIR, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        file_path = os.path.join(skill_dir, "SKILL.md")

        content = f"""---
name: {skill["name"]}
description: {skill["desc"]}
---

# {skill["id"]}

## 1. Purpose & Scope
{skill["purpose"]}

## 2. When to Use
{skill["when_use"]}

## 3. When NOT to Use
{skill["when_not_use"]}

## 4. Prerequisites & Input Context
{skill["prereqs"]}

## 5. Core Concepts & Taxonomy
{skill["concepts"]}

## 6. Step-by-Step Execution Workflow
{skill["workflow"]}

## 7. Concrete Examples
{skill["examples"]}

## 8. Anti-Patterns & Common Traps
{skill["antipatterns"]}

## 9. Verification Quality Gates
{skill["gates"]}

## 10. Security & Risk Mitigation
{skill["security"]}

## 11. Platform Adapters & Extensibility
{skill["adapters"]}

## 12. Expected Deliverables
{skill["deliverables"]}

## 13. Related Skills & Synergy
{skill["related"]}

## 14. Realistic Usage Scenario & Verification Commands
{skill["usage"]}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"[{idx:02d}/{total:02d}] Created: {skill_id}")

    print(f"\nSuccessfully generated {created}/{total} skills for Groups AI & AJ.")

if __name__ == "__main__":
    generate_skills()
