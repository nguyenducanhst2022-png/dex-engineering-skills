---
name: dex-lua-embedding-safety
description: Safely embed Lua scripting runtimes into host applications (C, C++, Rust, Go) with strict memory quotas, instruction execution limits, and sandboxed OS boundaries. Use when providing user plugin or scripting capabilities.
---

# dex-lua-embedding-safety

## 1. Purpose & Scope
Nhúng và kiểm soát an toàn môi trường thông dịch Lua (Lua Embedding Safety) vào các ứng dụng chủ (Host Applications viết bằng C, C++, Rust, Go); thiết lập hạn ngạch bộ nhớ RAM nghiêm ngặt (Memory Quotas), giới hạn số lượng lệnh CPU (Instruction Step Limits via Hooks), và cô lập ranh giới hệ điều hành (OS Sandboxing) ngăn chặn mã độc.

## 2. When to Use
- Khi phát triển hệ thống cho phép người dùng hoặc lập trình viên bên thứ ba viết kịch bản mở rộng (Plugins / User Scripts) như game engine, reverse proxy (OpenResty/Envoy), hoặc tự động hóa nghiệp vụ.
- Khi cần chạy mã nguồn không đáng tin cậy (Untrusted User Code) nhưng bắt buộc phải bảo đảm mã đó không thể đọc trộm file, chiếm dụng 100% CPU hoặc làm sập ứng dụng chủ.
- Khi xây dựng engine thực thi chính sách bảo mật động (Policy Decision Points).

## 3. When NOT to Use
- Khi ứng dụng không có tính năng cho phép bên ngoài nạp script động.
- Khi chỉ chạy các script nội bộ đáng tin cậy 100% do chính đội ngũ phát triển viết trong môi trường backend đóng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Môi trường thông dịch Lua (Lua 5.4, LuaJIT), ngôn ngữ ứng dụng chủ (C/C++, Rust với `mlua`), cấu hình giới hạn tài nguyên (CPU steps, Max RAM).
- **Quyền hạn truy cập:** Quyền cấu hình và khởi tạo Lua State trong ứng dụng chủ.

## 5. Core Concepts & Taxonomy
- **Standard Library Sanitization:** Vô hiệu hóa hoặc gỡ bỏ hoàn toàn các thư viện tiêu chuẩn nguy hiểm của Lua như `os` (chạy lệnh shell, xóa file), `io` (đọc ghi tệp tin), và `debug` (can thiệp bộ nhớ VM).
- **Instruction Count Hook (`lua_sethook`):** Cơ chế ngắt thực thi tự động của Lua VM sau khi đã chạy qua một số lượng bytecode instructions nhất định để chống vòng lặp vô tận (`while true do end`).
- **Custom Memory Allocator:** Cài đặt hàm cấp phát bộ nhớ riêng cho Lua State để theo dõi và từ chối cấp phát khi tổng dung lượng RAM của script vượt hạn ngạch cho phép.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo Lua State mới bằng API cô lập, tuyệt đối không gọi `luaL_openlibs()` tự do.
2. Chỉ nạp có chọn lọc các thư viện an toàn: `table`, `string`, `math`.
3. Gắn hàm cấp phát bộ nhớ có kiểm soát hạn ngạch (ví dụ: giới hạn tối đa 16MB RAM cho mỗi script).
4. Cài đặt Instruction Hook với cờ `LUA_MASKCOUNT` (ví dụ: kích hoạt ngắt sau mỗi 100,000 instructions) để kiểm tra timeout hoặc ép dừng script chạy quá thời gian.
5. Cung cấp các API an toàn từ ứng dụng chủ vào môi trường Lua thông qua các hàm bọc (Wrapper Functions) có kiểm tra kiểu tham số chặt chẽ.
6. Kiểm thử hộp cát bằng các script thử nghiệm độc hại (cố tình gọi `os.execute`, cấp phát bộ nhớ vô hạn, vòng lặp vô tận) để xác nhận sandbox bảo vệ thành công.

## 7. Concrete Examples
### Ví dụ thiết lập hạn ngạch bộ nhớ và hook chống vòng lặp vô tận trong C:
```c
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>
#include <stdlib.h>

typedef struct {
    size_t current_memory;
    size_t max_memory;
} MemoryQuota;

// Bộ cấp phát bộ nhớ tùy chỉnh kiểm soát hạn ngạch RAM của Lua
void* custom_allocator(void* ud, void* ptr, size_t osize, size_t nsize) {
    MemoryQuota* quota = (MemoryQuota*)ud;
    if (nsize == 0) {
        quota->current_memory -= osize;
        free(ptr);
        return NULL;
    }
    if (quota->current_memory - osize + nsize > quota->max_memory) {
        return NULL; // Hết hạn ngạch RAM -> Lua sẽ ném lỗi "not enough memory"
    }
    quota->current_memory = quota->current_memory - osize + nsize;
    return realloc(ptr, nsize);
}

// Hook kiểm tra số lượng chỉ lệnh CPU để chống vòng lặp vô tận
void instruction_count_hook(lua_State* L, lua_Debug* ar) {
    luaL_error(L, "CPU execution limit exceeded: Infinite loop detected.");
}

void init_safe_lua_sandbox() {
    MemoryQuota quota = { .current_memory = 0, .max_memory = 16 * 1024 * 1024 }; // 16MB
    lua_State* L = lua_newstate(custom_allocator, &quota);

    // Chỉ nạp thư viện an toàn, LOẠI BỎ os và io!
    luaL_requiref(L, "_G", luaopen_base, 1);
    luaL_requiref(L, "string", luaopen_string, 1);
    luaL_requiref(L, "math", luaopen_math, 1);

    // Đặt hook ngắt sau mỗi 1,000,000 instructions
    lua_sethook(L, instruction_count_hook, LUA_MASKCOUNT, 1000000);
}
```

## 8. Anti-Patterns & Common Traps
- **Opening All Standard Libraries:** Gọi `luaL_openlibs(L)` cho script của người dùng, cho phép kẻ tấn công gọi `os.execute('rm -rf /')` xóa sạch hệ thống chủ.
- **No CPU Instruction Limits:** Không cài đặt hook ngắt chỉ lệnh khiến script chứa `while true do end` chiếm dụng 100% CPU của thread chủ và làm treo máy chủ vĩnh viễn.
- **Unbounded Memory Usage:** Cho phép script tạo bảng dữ liệu khổng lồ khiến ứng dụng chủ bị hệ điều hành tiêu diệt do hết RAM (Out of Memory Killer).

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Thử nghiệm script độc hại chứa vòng lặp vô tận bị ngắt thành công trong dưới 100ms.
- **QG-06**: Không có script nào có thể truy cập được hệ thống file hoặc thực thi lệnh shell hệ điều hành.
- **QG-10**: Giới hạn bộ nhớ RAM được thực thi nghiêm ngặt, trả về lỗi an toàn khi script vượt quá hạn ngạch.

## 10. Security & Safety Boundaries
- Cách ly hoàn toàn môi trường Lua State giữa các người dùng khác nhau; không dùng chung Lua State cho nhiều request độc lập.
- Làm sạch dữ liệu trả về từ Lua script trước khi đưa vào các hàm xử lý nhạy cảm của ứng dụng chủ.

## 11. Platform Adapters
- **Engines**: Lua 5.4, LuaJIT.
- **Bindings**: Rust `mlua`, C/C++ Lua API, Go `gopher-lua`.

## 12. Deliverables & Output Artifacts
- Mã nguồn khởi tạo Lua Sandbox an toàn có kiểm soát RAM và CPU.
- Bộ kiểm tra các hàm thư viện chuẩn được phép và bị cấm.
- Bộ kiểm thử bảo mật tiêm script độc hại xác nhận hộp cát hoạt động an toàn.

## 13. Related & Complementary Skills
dex-native-plugin-abi-testing, dex-security-audit, dex-api-abuse-prevention

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử an toàn hộp cát Lua Sandbox
pytest tests/security/test_lua_embedding_sandbox.py -v
```
