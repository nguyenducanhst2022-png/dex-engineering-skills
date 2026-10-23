---
name: dex-manga-reader-performance
description: Optimize high-performance long-strip (webtoon) and paginated manga reader engines. Implement virtualized canvas/DOM windowing, preemptive image prefetching, decode memory pooling, and scroll position restoration.
---

# dex-manga-reader-performance

## 1. Purpose & Scope
Thiết kế và tối ưu hóa hiệu năng cho trình đọc truyện tranh trực tuyến (Manga/Webtoon Reader Engine); áp dụng kỹ thuật ảo hóa danh sách trang (Virtualized Viewport Windowing), tiền tải thông minh hình ảnh tiếp theo (Preemptive Prefetching), quản lý vùng nhớ đệm giải mã ảnh (Bitmap Decode Memory Pooling) nhằm triệt tiêu hiện tượng lag giật và chống tràn RAM trên các thiết bị di động khi đọc các bộ truyện hàng trăm trang.

## 2. When to Use
- Khi xây dựng hoặc tái cấu trúc ứng dụng đọc truyện tranh kỹ thuật số dạng cuộn dọc liên tục (Webtoon / Long-strip) hoặc lật trang đôi (Double-page spread).
- Khi ứng dụng bị sập tab (Out of Memory - OOM crash) do tải quá nhiều hình ảnh chất lượng cao vào DOM cùng một lúc.
- Khi cần duy trì chính xác vị trí cuộn trang (scroll position restoration) sau khi xoay màn hình hoặc tải lại trang.

## 3. When NOT to Use
- Khi ứng dụng chỉ hiển thị bài viết văn bản thuần túy với 1-2 hình ảnh minh họa nhỏ.
- Khi đọc tài liệu PDF văn bản thông thường (nên dùng PDF.js chuyên dụng).

## 4. Prerequisites & Input Context
- **Công nghệ frontend:** React, Vue, Svelte hoặc Vanilla JS với HTML5 Canvas và IntersectionObserver.
- **Hạ tầng hình ảnh:** Máy chủ CDN hỗ trợ ảnh định dạng WebP/AVIF hiện đại.

## 5. Core Concepts & Taxonomy
- **DOM Virtualization:** Chỉ render vào cây DOM những trang truyện nằm trong viewport cộng thêm vùng đệm (buffer window 2 trang trước và sau); các trang còn lại được thay thế bằng placeholder có chiều cao tương ứng.
- **createImageBitmap Decoupling:** Giải mã dữ liệu nén của ảnh trên Background Web Worker bằng `createImageBitmap` thay vì giải mã trên Main UI Thread gây nghẽn giao diện.
- **Memory Ceiling Budget:** Giới hạn tổng dung lượng ảnh giải mã trong bộ nhớ RAM không vượt quá 150MB trên thiết bị di động.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo IntersectionObserver để theo dõi các phần tử giữ chỗ (placeholder element) của từng trang truyện.
2. Khi trang đi vào vùng đệm (buffer margin 1000px), kích hoạt pipeline tải ảnh bất đồng bộ.
3. Chuyển đổi Blob tải về thành Bitmap thông qua Web Worker hoặc `img.decode()` bất đồng bộ.
4. Đưa hình ảnh đã giải mã vào thẻ `<canvas>` hoặc `<img>` và giải phóng URL tạm bằng `URL.revokeObjectURL()`.
5. Khi trang cuộn ra xa khỏi viewport (cách hơn 3 màn hình), chủ động xóa thuộc tính `src` hoặc context của canvas để bộ thu gom rác (Garbage Collector) dọn dẹp RAM.
6. Lưu mốc phần trăm trang đã đọc vào `localStorage` kèm debounce 300ms.

## 7. Concrete Examples
### Module ao hoa va giai ma anh bat dong bo cho Webtoon Reader:
```javascript
class MangaVirtualScroller {
  constructor(container, pages) {
    this.container = container;
    this.pages = pages; // Danh sach URL cac trang
    this.renderedPages = new Map();
    this.initObserver();
  }

  initObserver() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const pageIdx = parseInt(entry.target.dataset.pageIndex, 10);
        if (entry.isIntersecting) {
          this.loadPageImage(pageIdx, entry.target);
        } else {
          this.unloadPageImage(pageIdx, entry.target);
        }
      });
    }, { rootMargin: '800px 0px 800px 0px' });
  }

  async loadPageImage(idx, element) {
    if (this.renderedPages.has(idx)) return;
    const imgUrl = this.pages[idx];
    
    const img = new Image();
    img.src = imgUrl;
    img.loading = 'eager';
    try {
      await img.decode(); // Giai ma truoc ngoai main-thread
      element.innerHTML = '';
      element.appendChild(img);
      this.renderedPages.set(idx, img);
    } catch (err) {
      console.error(`Failed to decode page ${idx}:`, err);
    }
  }

  unloadPageImage(idx, element) {
    if (this.renderedPages.has(idx)) {
      const img = this.renderedPages.get(idx);
      img.src = ''; // Huy lien ket bo nho bitmap
      element.innerHTML = `<div class="page-placeholder" style="height:${element.clientHeight}px"></div>`;
      this.renderedPages.delete(idx);
    }
  }
}
```

## 8. Anti-Patterns & Common Traps
- **Appending 100 Image Tags Directly:** Nối thẳng 100 thẻ `<img src="large_page.jpg">` vào DOM cùng lúc làm cạn kiệt RAM thiết bị và đóng băng luồng UI.
- **Layout Thrashing on Scroll:** Đọc liên tục các thuộc tính `offsetTop` và `clientHeight` trong sự kiện cuộn `window.onscroll` mà không bọc trong `requestAnimationFrame`.
- **Ignoring Network Tier:** Vẫn tải ảnh gốc 4K cho người dùng đang bật chế độ tiết kiệm dữ liệu (Data Saver mode).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tốc độ khung hình khi cuộn dọc duy trì ổn định 60fps (hoặc 120fps trên màn hình ProMotion) không rớt khung hình nghiêm trọng.
- **QG-02**: Mức tiêu thụ bộ nhớ RAM của tab trình duyệt giữ dưới 150MB trong suốt 50 trang cuộn liên tục.
- **QG-03**: Khôi phục chính xác 100% vị trí trang đang đọc sau khi người dùng reload trang.

## 10. Security & Safety Boundaries
- Ngăn chặn tấn công Pixel Flood / Decompression Bomb bằng cách giới hạn kích thước tối đa của hình ảnh được phép giải mã (chiều rộng tối đa 4096px).

## 11. Platform Adapters
- **Runtimes**: Modern Browsers (Chrome, Safari, Firefox), React Native WebView, Tauri Desktop Manga Readers.

## 12. Deliverables & Output Artifacts
- Thư viện điều phối ảo hóa trình đọc truyện (`MangaVirtualScroller.js`).
- Bộ benchmark đo lường bộ nhớ RAM và tỷ lệ FPS khi cuộn trang.

## 13. Related & Complementary Skills
dex-frontend-performance, dex-streaming-qoe-telemetry

## 14. Realistic Usage Example
```bash
# Kiem thu hieu nang cuon trang bang Lighthouse CLI
lighthouse https://example.com/reader/chapter-1 --only-categories=performance --view
```
