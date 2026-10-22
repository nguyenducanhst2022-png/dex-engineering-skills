---
name: dex-extension-storage-migration
description: Manage schema versioning, asynchronous data migrations, and corruption recovery for chrome.storage.local and chrome.storage.sync across extension updates. Use when migrating user settings across major versions, syncing cross-device data, or recovering from quota-exceeded storage errors.
---

# dex-extension-storage-migration

## 1. Purpose & Scope
Quản lý cơ chế phân phiên bản lược đồ dữ liệu (Schema Versioning), di chuyển dữ liệu bất đồng bộ (Data Migration) và tự phục hồi khi dữ liệu bị hỏng trong `chrome.storage.local` và `chrome.storage.sync`; đảm bảo cập nhật phiên bản extension mượt mà, đồng bộ cài đặt đa thiết bị và xử lý sự cố vượt hạn mức dung lượng (Quota Exceeded).

## 2. When to Use
- Khi nâng cấp phiên bản extension có thay đổi cấu trúc dữ liệu cài đặt của người dùng.
- Khi chuyển đổi từ lưu trữ cục bộ (`local`) sang lưu trữ đồng bộ đám mây (`sync`) hoặc ngược lại.
- Khi nhận được thông báo lỗi vượt quá giới hạn lưu trữ (Storage Quota Exceeded).

## 3. When NOT to Use
- Khi quản lý di chuyển cơ sở dữ liệu quan hệ PostgreSQL/MySQL dưới backend.
- Khi chỉ lưu trữ các giá trị tạm thời không cần bảo toàn qua các lần cập nhật extension.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kiến thức về các hạn mức của `chrome.storage` (Sync quota: 100KB tổng, 8KB/item; Local quota: 10MB), sự kiện `chrome.runtime.onInstalled`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Linear Schema Migrations:** Áp dụng tuần tự các bước nâng cấp cấu trúc từ phiên bản cũ lên phiên bản mới (v1 -> v2 -> v3).
- **Storage Quota Governance:** Tự động nén dữ liệu hoặc di dời các dữ liệu lớn sang `chrome.storage.local` khi `chrome.storage.sync` chạm ngưỡng cảnh báo.
- **Safe Fallback & Corruption Recovery:** Luôn tạo bản sao lưu dự phòng (Snapshot) trước khi thực hiện di chuyển dữ liệu.

## 6. Step-by-Step Execution Workflow
1. Lưu số hiệu phiên bản cấu trúc dữ liệu hiện tại trong khóa `__schema_version`.
2. Lắng nghe sự kiện `chrome.runtime.onInstalled` với lý do `details.reason === 'update'`.
3. So sánh phiên bản dữ liệu đã lưu với phiên bản yêu cầu của mã nguồn mới.
4. Thực hiện chuỗi hàm di chuyển (Migration Pipeline) tuần tự cho từng bước nhảy phiên bản.
5. Kiểm tra tính toàn vẹn của dữ liệu sau di chuyển và cập nhật lại `__schema_version`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Safe Storage Migration Runner
export async function runStorageMigrations() {
  const current = await chrome.storage.local.get(['__schema_version']);
  let version = current.__schema_version || 1;

  if (version < 2) {
    // Migration v1 -> v2: Flatten theme options
    const v1Data = await chrome.storage.local.get(['userTheme', 'fontSize']);
    await chrome.storage.local.set({
      preferences: {
        theme: v1Data.userTheme || 'system',
        fontSize: v1Data.fontSize || 14
      },
      __schema_version: 2
    });
    await chrome.storage.local.remove(['userTheme', 'fontSize']);
    version = 2;
  }
}
```

## 8. Anti-Patterns & Common Traps
- Thay đổi cấu trúc dữ liệu mà không viết hàm migration khiến người dùng bị mất toàn bộ cấu hình cũ khi extension tự động cập nhật.
- Lưu trữ dữ liệu nhị phân hoặc chuỗi base64 khổng lồ vào `chrome.storage.sync` làm sập giới hạn 8KB của trình duyệt.
- Xóa sạch dữ liệu của người dùng khi gặp lỗi đọc cấu hình thay vì kích hoạt luồng khôi phục dự phòng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các lần cập nhật có thay đổi lược đồ đều có mã kiểm thử di chuyển dữ liệu tương ứng.
- QG-02: Không làm mất bất kỳ cài đặt người dùng nào khi nâng cấp từ phiên bản cũ nhất lên phiên bản mới nhất.
- QG-03: Có cơ chế tự động dọn dẹp các khóa dữ liệu lỗi thời (Orphaned keys).

## 10. Security & Safety Boundaries
- Mã hóa các dữ liệu cấu hình nhạy cảm trước khi đồng bộ lên dịch vụ lưu trữ đám mây của trình duyệt.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Hệ thống di chuyển dữ liệu lưu trữ `StorageMigrationPipeline.ts`.
1. Bộ test tự động kiểm thử di chuyển dữ liệu qua các phiên bản.

## 13. Related & Complementary Skills
- [`dex-schema-evolution`](.agents/skills/dex-schema-evolution/SKILL.md)
- [`dex-browser-extension-mv3`](.agents/skills/dex-browser-extension-mv3/SKILL.md)
- [`dex-storage-lifecycle`](.agents/skills/dex-storage-lifecycle/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát hành phiên bản 3.0 của extension với cấu trúc cài đặt mới dạng module. Kỹ sư kích hoạt `dex-extension-storage-migration` để tự động chuyển đổi cấu hình của 50,000 người dùng hiện tại mà không ai bị mất dữ liệu phím tắt hoặc tài khoản liên kết đã lưu.
