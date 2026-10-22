---
name: dex-virtualized-infinite-lists
description: Implement high-performance windowed list virtualization (TanStack Virtual, react-window) supporting dynamic row heights, scroll restoration, sticky headers, and stable infinite paging. Use when rendering feeds with 10,000+ items, large data tables, or chat message logs.
---

# dex-virtualized-infinite-lists

## 1. Purpose & Scope
Hiện thực hóa danh sách ảo hóa (List Virtualization / Windowing) hiệu năng cao cho dữ liệu cực lớn (10,000+ phần tử); chỉ dựng các nút DOM thực tế nằm trong khung nhìn hiển thị (Viewport), hỗ trợ chiều cao hàng động, khôi phục vị trí cuộn chuột và phân trang vô tận mượt mà.

## 2. When to Use
- Khi ứng dụng phải hiển thị danh sách lớn dữ liệu (bảng giao dịch tài chính, nhật ký log, tin nhắn chat).
- Khi trang web bị đơ, giật hoặc tiêu tốn hàng trăm megabyte RAM do tạo ra quá nhiều DOM nodes.
- Khi cuộn qua danh sách dài bị giật khung hình và rớt FPS nghiêm trọng.

## 3. When NOT to Use
- Khi danh sách dữ liệu cố định dưới 100 phần tử đơn giản.
- Khi cần in ấn toàn bộ nội dung trang ra giấy (Print Stylesheet).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kích thước khung chứa danh sách, hàm lấy dữ liệu phân trang, thư viện ảo hóa mục tiêu (TanStack Virtual hoặc react-window).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Windowing Concept:** Chỉ tạo ra từ 10 đến 20 DOM nodes thực tế cho các phần tử nhìn thấy được, dịch chuyển vị trí bằng `transform: translateY()`.
- **Overscan Padding:** Dựng trước thêm một số phần tử ở phía trên và phía dưới khung nhìn để người dùng không thấy khoảng trắng khi cuộn nhanh.
- **Dynamic Size Measurement:** Tự động đo lường và cập nhật chiều cao thực tế của các hàng có nội dung co giãn linh hoạt.

## 6. Step-by-Step Execution Workflow
1. Bọc danh sách trong một thẻ container có thanh cuộn với thuộc tính `overflow-y: auto`.
2. Khởi tạo Virtualizer với số lượng phần tử tổng và hàm ước tính chiều cao ban đầu.
3. Áp dụng vị trí tuyệt đối (`position: absolute`) và `transform` cho từng hàng được ảo hóa.
4. Lắng nghe sự kiện cuộn để kích hoạt tải thêm trang mới khi người dùng cuộn gần tới đáy danh sách.
5. Kiểm tra mức độ tiêu thụ RAM của trình duyệt trong quá trình cuộn liên tục.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { useVirtualizer } from '@tanstack/react-virtual';
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
}
```

## 8. Anti-Patterns & Common Traps
- Render trực tiếp 20,000 thẻ `div` vào DOM cùng lúc khiến trình duyệt đơ trong vài giây.
- Thiết lập giá trị `overscan` quá lớn làm mất đi lợi ích giảm tải DOM của kỹ thuật ảo hóa.
- Quên khai báo thuộc tính `position: relative` ở thẻ cha khiến các phần tử con bị nhảy loạn xạ vị trí.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Số lượng phần tử DOM trong trang không vượt quá 50 nodes bất kể danh sách có 100,000 bản ghi.
- QG-02: Tốc độ cuộn chuột duy trì ổn định ở mức 60fps mà không xuất hiện khoảng trắng nhấp nháy.
- QG-03: Khôi phục chính xác vị trí cuộn khi người dùng quay lại từ trang chi tiết.

## 10. Security & Safety Boundaries
- Đảm bảo các dữ liệu được render động trong danh sách ảo hóa đều được escape cẩn thận, ngăn ngừa tấn công XSS qua dữ liệu mảng.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Component danh sách ảo hóa tái sử dụng `VirtualizedDataTable.tsx`.
1. Tài liệu hướng dẫn xử lý chiều cao hàng co giãn động.

## 13. Related & Complementary Skills
- [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md)
- [`dex-ui-component-contracts`](.agents/skills/dex-ui-component-contracts/SKILL.md)
- [`dex-layout-composition-patterns`](.agents/skills/dex-layout-composition-patterns/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Xây dựng màn hình xem nhật ký hệ thống máy chủ (Log Viewer) hiển thị 50,000 dòng log theo thời gian thực. Áp dụng `dex-virtualized-infinite-lists` để chỉ giữ lại 30 dòng trong DOM, giảm 95% mức sử dụng bộ nhớ và giúp việc tìm kiếm log diễn ra mượt mà không bị treo tab trình duyệt.
