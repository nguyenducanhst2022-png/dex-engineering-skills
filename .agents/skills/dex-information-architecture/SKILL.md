---
name: dex-information-architecture
description: Structure, categorize, and label application information, navigation systems, and content hierarchies using card sorting, taxonomy modeling, and findability principles. Use when structuring complex enterprise portals or knowledge bases.
---

# dex-information-architecture

## 1. Purpose & Scope
Thiết kế, phân loại và cấu trúc hóa kiến trúc thông tin (Information Architecture - IA); xây dựng hệ thống điều hướng (Navigation Systems), cấu trúc phân cấp nội dung (Content Hierarchy) và hệ thống nhãn (Taxonomy & Labeling) thông qua phương pháp Card Sorting và Findability Principles, giúp người dùng tìm thấy thông tin cần thiết một cách tự nhiên và nhanh chóng nhất.

## 2. When to Use
- Ứng dụng hoặc cổng thông tin doanh nghiệp phát triển quá lớn, menu điều hướng trở nên rối rắm với hàng chục mục con.
- Người dùng liên tục gửi ticket hỗ trợ hỏi về các tính năng đã có sẵn nhưng họ không tìm thấy.
- Tái cấu trúc lại trang tài liệu kỹ thuật hoặc hệ thống quản lý tri thức nội bộ.

## 3. When NOT to Use
- Không thiết kế cây điều hướng quá sâu (>4 cấp con), khiến người dùng phải bấm chuột liên tục để tới đích.
- Không sắp xếp menu theo cơ cấu tổ chức phòng ban nội bộ của công ty (người dùng ngoài không quan tâm phòng ban nào làm tính năng đó).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh mục toàn bộ các màn hình, tính năng và nội dung hiện có (Content Inventory).
- Kết quả nghiên cứu Card Sorting từ nhóm người dùng mục tiêu.
- Lịch sử các từ khóa được tìm kiếm nhiều nhất trên thanh tìm kiếm nội bộ.
- **Điều kiện tiên quyết**:
- Có bản kiểm kê nội dung (Content Audit) đầy đủ của hệ thống hiện tại.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Findability vs Discoverability:
  + Findability: Khả năng người dùng tìm thấy một nội dung cụ thể mà họ đã biết trước rằng nó tồn tại.
  + Discoverability: Khả năng người dùng vô tình phát hiện ra các tính năng hoặc nội dung mới hữu ích mà họ chưa từng biết.
- Card Sorting (Mở vs Đóng): Kỹ thuật cho người dùng tự sắp xếp các thẻ tính năng vào các nhóm mà họ cảm thấy hợp lý nhất, giúp phát hiện mô hình tư duy (Mental Models) tự nhiên của họ.
- Progressive Disclosure trong IA: Chỉ hiển thị các thông tin quan trọng nhất ở tầng trên cùng, các chi tiết nâng cao chỉ mở ra khi người dùng chủ động yêu cầu.
- **Quy tắc quyết định kỹ thuật**:
- Tuân thủ quy tắc '3 Clicks Rule' (khuyến nghị): Người dùng có thể tiếp cận 90% thông tin quan trọng trong vòng không quá 3 lần tương tác.
- Sử dụng ngôn từ phổ thông, tránh các thuật ngữ chuyên ngành nội bộ trên thanh điều hướng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Nhét tất cả các tính năng vào một menu 'Khác' (Miscellaneous/Others), biến nó thành một thùng rác chứa các tính năng vô thừa nhận.

## 6. Step-by-Step Execution Workflow
1. Thực hiện kiểm kê toàn bộ nội dung hiện tại vào bảng tính (Content Inventory).
2. Tổ chức buổi Card Sorting với tối thiểu 15 người dùng đại diện.
3. Xây dựng sơ đồ cây kiến trúc thông tin (Site Map / Tree Architecture).
4. Kiểm chứng tính hiệu quả bằng bài kiểm tra Tree Testing (yêu cầu người dùng tìm đường trong menu chỉ có chữ thô).
5. Chốt cấu trúc điều hướng chính thức và chuyển giao cho đội ngũ Frontend.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# Sơ đồ Kiến trúc Thông tin (Information Architecture Tree)

└── [Home] Trang tổng quan
    ├── [Quản lý Đơn hàng] (Orders)
    │   ├── Đơn chờ xử lý
    │   ├── Đơn hoàn thành
    │   └── Yêu cầu đổi trả
    ├── [Kho hàng & Sản phẩm] (Catalog)
    │   ├── Danh mục sản phẩm
    │   └── Kiểm kê tồn kho
    ├── [Báo cáo & Phân tích] (Analytics)
    │   ├── Doanh thu bán hàng
    │   └── Báo cáo khách hàng
    └── [Cài đặt Hệ thống] (Settings)
        ├── Hồ sơ doanh nghiệp
        ├── Phân quyền nhân viên
        └── Kết nối API
```

### Lệnh xác minh & thực thi:
```bash
# Đo lường tỉ lệ hoàn thành nhiệm vụ tìm đường bằng Tree Testing benchmark
# (Yêu cầu đạt Task Completion Rate > 80%)
```

## 8. Anti-Patterns & Common Traps
- Đặt tên nhãn menu trừu tượng hoặc chơi chữ khiến người dùng không đoán được bên trong có gì.
- Để cấu trúc menu thay đổi vị trí ngẫu nhiên giữa các trang khác nhau.

## 9. Quality Gates & Acceptance Criteria
- Tỉ lệ tìm kiếm đúng đường (Direct Path Success Rate) trong Tree Testing đạt tối thiểu 80%.
- Độ sâu điều hướng tối đa không vượt quá 3 tầng thư mục.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Ẩn hoàn toàn các mục menu mà người dùng không có quyền truy cập (RBAC-driven navigation) để tránh lộ diện kiến trúc bảo mật.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Sơ đồ cây kiến trúc thông tin (Site Map Diagram).
- Bảng đối soát thuật ngữ nhãn điều hướng (Taxonomy & Labeling Dictionary).

## 13. Related & Complementary Skills
dex-user-journey-mapping, dex-usability-study-design, dex-frontend-architecture

## 14. Realistic Usage Example
### Tình huống thực tế:
Một nền tảng SaaS B2B có 80 tính năng khác nhau khiến khách hàng than phiền là quá khó dùng. Bằng cách thực hiện Card Sorting với 30 khách hàng doanh nghiệp và tái cấu trúc lại Kiến trúc Thông tin từ 12 menu chính xuống còn 4 nhóm vai trò rõ ràng, số lượng ticket yêu cầu hướng dẫn sử dụng đã giảm 55% trong tháng đầu tiên.
