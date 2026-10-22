---
name: dex-geospatial-data-pipelines
description: Architect high-throughput geospatial data pipelines using Uber H3 discrete global grids, Google S2 geometry, PostGIS spatial indexing, and GeoJSON/WKB serialization. Use when building ride-hailing routing, geofencing alert engines, or spatial delivery analytics.
---

# dex-geospatial-data-pipelines

## 1. Purpose & Scope
Thiết kế và hiện thực hóa các đường ống xử lý dữ liệu không gian địa lý (Geospatial Data Pipelines) thông lượng cao; ứng dụng hệ thống lưới lục giác toàn cầu Uber H3, hình học Google S2, chỉ mục không gian PostGIS (R-Tree / GIST) và tuần tự hóa dữ liệu GeoJSON/WKB; phục vụ các hệ thống định tuyến gọi xe, hàng rào địa lý (Geofencing) thời gian thực và phân tích bán kính giao hàng.

## 2. When to Use
- Khi xây dựng ứng dụng tìm kiếm tài xế hoặc địa điểm gần nhất trong bán kính 5km cho hàng triệu người dùng đồng thời.
- Khi cần gom cụm (Clustering) hàng triệu điểm tọa độ GPS thành các vùng lục giác đồng đều để trực quan hóa bản đồ nhiệt.
- Khi kiểm tra xem một phương tiện có đi vào hoặc đi ra khỏi khu vực hàng rào địa lý được chỉ định hay không.

## 3. When NOT to Use
- Khi ứng dụng chỉ lưu trữ địa chỉ văn bản thông thường không cần tính toán khoảng cách hay ranh giới không gian.
- Khi tính toán khoảng cách phẳng thuần túy trong phòng thí nghiệm không xét đến độ cong của Trái Đất.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư viện Uber H3 (`h3-js` hoặc Python `h3`), cơ sở dữ liệu hỗ trợ không gian PostGIS hoặc DuckDB Spatial, hiểu biết về hệ tọa độ WGS84 (EPSG:4326).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **H3 Hexagonal Hierarchical Spatial Index:** Chia bề mặt Trái Đất thành các ô lục giác đều với 16 cấp độ phân giải (Resolution 0 đến 15); mỗi ô có đúng một mã băm số nguyên 64-bit duy nhất.
- **Neighbor Traversal Efficiency:** Các ô lục giác có khoảng cách tới 6 ô lân cận hoàn toàn bằng nhau (không bị méo mó như ô vuông), giúp thuật toán tìm kiếm lân cận $O(1)$ cực nhanh.
- **GIST Spatial Indexing:** Cấu trúc cây R-Tree trong PostGIS giúp tìm kiếm các đối tượng hình học giao nhau (`ST_Intersects`) trong vài mili-giây.

## 6. Step-by-Step Execution Workflow
1. Chuyển đổi cặp tọa độ kinh độ/vĩ độ (Longitude, Latitude) thành mã lục giác H3 cấp độ phù hợp (ví dụ Res 8 ~ 460 mét).
2. Lưu mã H3 index dưới dạng số nguyên 64-bit trong cơ sở dữ liệu để đánh chỉ mục B-Tree cực nhanh.
3. Khi tìm kiếm lân cận, gọi hàm `h3.gridDisk(centerH3, kRing)` để lấy danh sách các ô xung quanh.
4. Thực hiện truy vấn dữ liệu bằng toán tử `IN (:neighborH3List)` thay vì tính toán khoảng cách cầu Haversine tốn CPU trên từng dòng.
5. Kiểm tra độ trễ truy vấn khi phục vụ 5,000 yêu cầu tìm tài xế mỗi giây.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import h3 from 'h3-js';

// High-Performance Geospatial Spatial Hashing
export function indexDriverLocation(lat: number, lng: number): string {
  // Resolution 8 corresponds to ~460m edge length
  return h3.latLngToCell(lat, lng, 8);
}

export function findNearbyDriverH3Cells(lat: number, lng: number, radiusKm: number): string[] {
  const originCell = h3.latLngToCell(lat, lng, 8);
  // Approx 1 ring is ~0.9km
  const kRings = Math.ceil(radiusKm / 0.9);
  return h3.gridDisk(originCell, kRings);
}

// SQL Query becomes super-fast B-Tree lookup:
// SELECT * FROM active_drivers WHERE h3_index = ANY($1);
```

## 8. Anti-Patterns & Common Traps
- Tính toán khoảng cách Haversine bằng lệnh toán học `acos(sin()...)` trên toàn bộ bảng 10 triệu dòng cho mỗi lần người dùng mở app (làm đơ toàn bộ database).
- Nhầm lẫn thứ tự giữa Kinh độ (Longitude/X) và Vĩ độ (Latitude/Y) dẫn đến việc định vị địa điểm rơi xuống biển.
- Dùng hệ thống lưới ô vuông (Latitude/Longitude Grid) khiến các ô bị méo mó nghiêm trọng khi tiến về hai cực của Trái Đất.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Độ trễ tìm kiếm tài xế lân cận trong bán kính 3km duy trì dưới 5ms trên tập dữ liệu 500,000 xe.
- QG-02: 100% tọa độ vị trí được chuyển đổi chính xác sang mã H3 Index theo chuẩn WGS84.
- QG-03: Không có lỗi tràn số nguyên khi lưu trữ mã H3 Index 64-bit trong cơ sở dữ liệu.

## 10. Security & Safety Boundaries
- Làm mờ tọa độ GPS chính xác của người dùng ở khu vực nhạy cảm (nhà riêng) bằng cách chỉ lưu trữ ở độ phân giải H3 vừa phải để bảo vệ quyền riêng tư.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module lập chỉ mục không gian địa lý H3 `GeospatialH3Pipeline.ts`.
1. Kịch bản cấu hình bảng dữ liệu không gian PostGIS `postgis_spatial_setup.sql`.

## 13. Related & Complementary Skills
- [`dex-database-query-plans`](.agents/skills/dex-database-query-plans/SKILL.md)
- [`dex-data-pipelines`](.agents/skills/dex-data-pipelines/SKILL.md)
- [`dex-search-engineering`](.agents/skills/dex-search-engineering/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Hệ thống giao đồ ăn bị sập máy chủ vào giờ ăn trưa do 200,000 khách hàng cùng lúc mở app tìm nhà hàng gần nhất, khiến câu lệnh tính khoảng cách Haversine làm nghẽn CPU database 100%. Kỹ sư kích hoạt `dex-geospatial-data-pipelines`, chuyển sang đánh chỉ mục lục giác Uber H3 Res 8, biến câu truy vấn hình học nặng nề thành một phép tra cứu B-Tree đơn giản, giảm tải CPU từ 100% xuống 8%.
