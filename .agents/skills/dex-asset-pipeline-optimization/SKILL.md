---
name: dex-asset-pipeline-optimization
description: Architect modern game and graphics asset compilation pipelines with GPU texture compression (BC1-7, ASTC, KTX2/Basis Universal), mesh level-of-detail (LOD) simplification, and streaming bundles. Use when reducing game package sizes, eliminating runtime stalls, and optimizing VRAM footprints.
---

# dex-asset-pipeline-optimization

## 1. Purpose & Scope
Thiết kế và xây dựng đường ống biên dịch và đóng gói tài nguyên đồ họa (Asset Pipeline Optimization) hiện đại; nén ảnh texture trực tiếp sang định dạng nén phần cứng GPU (BC1-BC7 trên PC, ASTC trên Mobile, KTX2/Basis Universal trên Web), tự động tạo các cấp độ chi tiết lưới đa giác (Mesh Level-of-Detail - LOD) và phân phối theo gói luồng (Streaming Bundles); phục vụ giảm 70% dung lượng gói cài đặt và giảm tải bộ nhớ VRAM.

## 2. When to Use
- Khi dung lượng gói cài đặt game quá khổng lồ (vượt quá 50GB) và cần tối ưu hóa để người dùng tải nhanh.
- Khi game bị giật khựng mỗi khi chuyển vùng bản đồ do phải giải nén ảnh PNG/JPEG thô vào VRAM.
- Khi cần xuất bản trò chơi đa nền tảng từ máy tính để bàn cấu hình cao xuống điện thoại di động và WebGL.

## 3. When NOT to Use
- Khi ứng dụng chỉ chứa một vài hình ảnh vector SVG đơn giản.
- Khi làm việc với các tệp văn bản mã nguồn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Công cụ nén texture phần cứng (`basis_universal`, `astcenc`, `nvtt`), công cụ đơn giản hóa lưới đa giác (`meshoptimizer`), kịch bản tự động hóa đường ống tài nguyên.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Block Compression (BC / ASTC):** Định dạng nén ảnh mà GPU có thể đọc và giải nén trực tiếp trên chip nhớ VRAM mà không cần giải nén bung ra RAM, giúp tiết kiệm 75% bộ nhớ đồ họa.
- **Basis Universal / KTX2:** Định dạng texture trung gian siêu nhỏ gọn có thể tự động chuyển đổi (Transcode) sang định dạng phần cứng tốt nhất của thiết bị đích lúc chạy.
- **Mesh LOD Simplification:** Giảm số lượng đỉnh tam giác của các vật thể ở xa mà mắt người không nhận biết được, giúp giảm tải hàng triệu phép tính Vertex Shader.

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ thư mục tài nguyên hình ảnh gốc (PNG, TGA, TIFF) của dự án.
2. Chuyển đổi các texture sang định dạng KTX2 sử dụng nén UASTC hoặc ETC1S.
3. Tự động sinh chuỗi Mipmaps đầy đủ cho từng texture để chống răng cưa khi nhìn từ xa.
4. Chạy công cụ `meshoptimizer` để tạo 3 cấp độ chi tiết LOD cho toàn bộ các mô hình 3D (LOD0: 100%, LOD1: 50%, LOD2: 15%).
5. Đóng gói tài nguyên thành các tệp gói dữ liệu nén (Asset Bundles) có hỗ trợ tải luồng theo nhu cầu.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Compressing textures to KTX2 / Basis Universal
basisu -ktx2 -uastc -uastc_level 2 -mipmap input_texture.png -output_file albedo.ktx2

# Optimizing 3D mesh and generating LOD levels via gltfpack
gltfpack -i character_model.gltf -o character_optimized.glb -cc -tc -si 0.5

# Verifying VRAM savings
# Raw uncompressed 2048x2048 RGBA: 16 MB VRAM
# BC7 / ASTC 4x4 compressed: 4 MB VRAM (75% savings!)
```

## 8. Anti-Patterns & Common Traps
- Đóng gói ảnh PNG thô vào game rồi lúc chạy dùng hàm giải nén của CPU ra mảng byte khổng lồ để nạp vào GPU (làm đứng hình game và ngốn sạch VRAM).
- Quên tạo Mipmaps cho texture khiến các bề mặt ở xa bị lấp lánh chói mắt (Texture Shimmering) và lãng phí băng thông bộ nhớ.
- Hiển thị mô hình 100,000 tam giác cho một cái cây nằm ở đường chân trời cách xa nhân vật 1km.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% texture trong bản dựng phát hành sử dụng định dạng nén GPU chuẩn (BC/ASTC/KTX2).
- QG-02: Dung lượng cài đặt gói tài nguyên giảm tối thiểu 60% so với dữ liệu gốc ban đầu.
- QG-03: Mọi mô hình phức tạp hơn 5,000 tam giác đều có tối thiểu 2 cấp độ LOD tự động.

## 10. Security & Safety Boundaries
- Xác minh mã băm toàn vẹn (Integrity Checksums) của các gói tài nguyên tải về từ mạng để ngăn ngừa việc người chơi chỉnh sửa tệp game để gian lận (Asset Modding).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Đường ống tự động hóa biên dịch tài nguyên `compile_assets_pipeline.py`.
1. Báo cáo tối ưu hóa dung lượng gói và mức sử dụng VRAM `ASSET_OPTIMIZATION_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-gpu-resource-lifetime`](.agents/skills/dex-gpu-resource-lifetime/SKILL.md)
- [`dex-media-delivery-pipelines`](.agents/skills/dex-media-delivery-pipelines/SKILL.md)
- [`dex-webgpu-rendering-fundamentals`](.agents/skills/dex-webgpu-rendering-fundamentals/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Một game thế giới mở trên di động có dung lượng gói cài đặt lên tới 14GB khiến 60% người dùng bỏ cuộc khi tải. Kỹ sư kích hoạt `dex-asset-pipeline-optimization`, chuyển đổi toàn bộ thư viện ảnh sang KTX2 Basis Universal và tạo LOD cho cây cối, giảm dung lượng cài đặt xuống chỉ còn 3.8GB và giảm 65% mức sử dụng VRAM, giúp game chạy mượt trên cả các điện thoại Android giá rẻ.
