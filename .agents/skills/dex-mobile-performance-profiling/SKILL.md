---
name: dex-mobile-performance-profiling
description: Profile mobile startup time (TTID/TTFD), frame rendering & jank detection (60/120 fps), memory leak detection (LeakCanary, Instruments Allocations), and battery drain. Use when diagnosing slow performance or crashes on mobile devices.
---

# dex-mobile-performance-profiling

## 1. Purpose & Scope
Đo lường, định hình và tối ưu hóa hiệu năng ứng dụng di động (Mobile Performance Profiling) trên thiết bị thực tế; đo lường chính xác thời gian khởi động ứng dụng (Time to Initial Display - TTID, Time to Full Display - TTFD), phát hiện và loại bỏ tình trạng giật khung hình (UI Jank, Dropped Frames) duy trì ổn định 60/120 FPS, truy vết rò rỉ bộ nhớ (Memory Leaks) bằng LeakCanary và Xcode Instruments, và tối ưu hóa mức tiêu thụ năng lượng pin (Battery Drain & CPU Wake Locks).

## 2. When to Use
- Khi người dùng đánh giá 1 sao vì ứng dụng khởi động chậm chạp (>3-5 giây trên máy tầm trung).
- Khi thao tác cuộn danh sách (RecyclerView / LazyColumn / List) bị giật lag, đơ khung hình.
- Khi ứng dụng bị hệ điều hành tiêu diệt ngầm vì ngốn quá nhiều RAM hoặc hao pin bất thường khi chạy nền.

## 3. When NOT to Use
- Đo lường hiệu năng của backend API hoặc cơ sở dữ liệu server (dùng `dex-performance-optimization`).
- Đo lường Core Web Vitals của website trên trình duyệt (dùng `dex-frontend-performance`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Thiết bị di động thử nghiệm (Ưu tiên thiết bị phần cứng tầm trung, low-end Android và iPhone đời cũ).
- Các kịch bản người dùng quan trọng (User Journeys): Khởi động app, cuộn feed tin tức, mở trang chi tiết sản phẩm.
- Dấu vết đo lường (Perfetto Traces, Systrace, Xcode Trace files).
- **Điều kiện tiên quyết**:
- Ứng dụng được biên dịch ở cấu hình Release hoặc Profile (tắt cờ debuggable để đo đúng thực tế).
- Cài đặt công cụ đo lường chuyên sâu: Android Studio Profiler, Perfetto, Xcode Instruments (Time Profiler, Allocations).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **TTID vs TTFD Invariance**: TTID là thời điểm khung hình đầu tiên của ứng dụng hiện lên màn hình; TTFD là thời điểm toàn bộ dữ liệu nội dung đã sẵn sàng tương tác; mục tiêu vàng: TTID < 1000ms, TTFD < 1800ms trên máy phổ thông.
- **16ms / 8ms Frame Budget**: Để đạt 60 FPS (hoặc 120 FPS ProMotion), luồng UI chỉ có tối đa 16ms (hoặc 8ms) để hoàn thành layout, measure và draw; vượt quá mốc này sẽ gây ra hiện tượng rớt khung hình (Jank).
- **Retained Size vs Shallow Size**: Phân biệt giữa dung lượng của chính đối tượng (shallow) và dung lượng của toàn bộ cây đối tượng mà nó giữ tham chiếu không cho Garbage Collector thu hồi (retained size).
- **Quy tắc quyết định kỹ thuật**:
- **Luôn Đo Trên Bản Build Profile/Release**: Tuyệt đối không đo thời gian khởi động hoặc FPS trên bản Debug build (bản Debug có overhead của ART interpreter, logging và debug symbols làm sai lệch 200-300%).
- **Không Khởi Tạo Thư Viện Đồng Bộ Khi Khởi Động (App Startup Bloat)**: Tránh khởi tạo 10 SDK phân tích trong `Application.onCreate()`; áp dụng lazy initialization hoặc Android App Startup library.
- **Giám Sát Tỷ Lệ Khung Hình Chậm (Frozen Frames)**: Tỷ lệ khung hình mất hơn 700ms (Frozen frames) phải dưới 0.1% tổng số frame hiển thị.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Danh sách bị đơ 100ms mỗi khi cuộn**: Do khởi tạo lại đối tượng định dạng ngày tháng `SimpleDateFormat` hoặc allocate bitmap mới bên trong hàm render item -> Khắc phục: Tái sử dụng đối tượng (Object Reuse) và sử dụng thư viện tải ảnh Coil / Glide có bộ nhớ đệm bitmap.
- **App bị OOM crash sau 10 phút sử dụng**: LeakCanary phát hiện Activity bị leak do đăng ký EventBus / LocationListener mà không hủy đăng ký trong `onDestroy()` -> Khắc phục: Hủy đăng ký listener trong vòng đời tương ứng.

## 6. Step-by-Step Execution Workflow
1. Chuẩn bị bản build Profile với cờ baseline profile được tối ưu hóa.
2. Đo thời gian khởi động (Cold Start) bằng lệnh: `adb shell am start-activity -W -n com.example/.MainActivity`.
3. Ghi lại Perfetto Trace hoặc Xcode Time Profiler trong quá trình người dùng thao tác cuộn giao diện.
4. Phân tích CPU Flame Graph tìm kiếm các hàm tốn nhiều thời gian nhất trên Main Thread.
5. Tích hợp LeakCanary vào bản build nội bộ để tự động chụp Heap Dump khi có Activity/Fragment leak.
6. Kiểm tra mức tiêu thụ điện năng qua Android Battery Historian hoặc Xcode Energy Gauge.
7. Tối ưu hóa mã nguồn (chuyển việc nặng sang background thread, tối ưu view hierarchy) và đo lường đối chiếu lại.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```kotlin
// Android Jetpack Macrobenchmark đo lường thời gian khởi động (Startup Benchmark)
@RunWith(AndroidJUnit4::class)
class StartupBenchmark {
    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun startupCold() = benchmarkRule.measureRepeated(
        packageName = "com.example.myapp",
        metrics = listOf(StartupTimingMetric()),
        iterations = 5,
        startupMode = StartupMode.COLD
    ) {
        pressHome()
        startActivityAndWait()
    }
}
```

### Lệnh xác minh & thực thi:
- Đo thời gian khởi động trực tiếp qua adb: `adb shell am start-activity -W -n com.myapp/.MainActivity | grep TotalTime`
- Bật hiển thị cảnh báo giật lag đồ họa trên màn hình: `adb shell setprop debug.choreographer.skipwarning 1`
- Thu thập Perfetto Trace 10 giây: `adb shell perfetto -o /data/misc/perfetto-traces/trace.perfetto-trace -t 10s sched freq idle am wm gfx`

## 8. Anti-Patterns & Common Traps
- **Nén và giải mã ảnh kích thước gốc 4000x3000 vào ImageView 200x200**: Làm cạn kiệt bộ nhớ RAM chỉ sau 3 tấm ảnh.
- **Lồng quá nhiều tầng ViewGroup / Composable lặp lại**: Làm tăng độ sâu cây giao diện và thời gian measure.
- **Chạy vòng lặp tính toán nặng trong composable mà không có `remember`**: Tính toán lại từ đầu trên mỗi frame.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Cold Start time (TTID) dưới 1.2 giây trên thiết bị tham chiếu tiêu chuẩn.
- QG-08: Tỷ lệ khung hình giật (Janky frames) dưới 2% trong suốt quá trình cuộn danh sách.
- QG-11: 0 cảnh báo memory leak từ LeakCanary trong kịch bản kiểm thử tự động.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Tắt bộ ghi dấu vết profile (Tracing) trong bản build production công khai trên Play Store / App Store.
- Không lưu heap dump chứa dữ liệu người dùng lên các server phân tích không an toàn.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Báo cáo phân tích hiệu năng (Performance Profiling Report).
- File Perfetto trace hoặc Instruments trace lưu lại bằng chứng.
- Kế hoạch hành động tối ưu hóa code và kết quả đo lường đối chứng trước/sau.

## 13. Related & Complementary Skills
- `dex-android-app-architecture`: Tái cấu trúc mã nguồn để cải thiện hiệu năng Android.
- `dex-ios-app-architecture`: Tối ưu hóa SwiftUI render loop và memory management trên iOS.
- `dex-performance-optimization`: Tư duy tối ưu thuật toán và cấu trúc dữ liệu cốt lõi.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng thương mại điện tử bị phàn nàn là màn hình cuộn sản phẩm bị giật hình liên tục trên các thiết bị Android tầm trung. Áp dụng `dex-mobile-performance-profiling`, kỹ sư gắn Perfetto Trace và phát hiện hàm định dạng tiền tệ tệ hại `NumberFormat.getCurrencyInstance()` bị gọi lại hàng trăm lần trong mỗi lần vẽ item. Kỹ sư tối ưu bằng cách cache lại formatter và pre-compute giá hiển thị ở tầng ViewModel. Tỷ lệ Janky frames giảm ngay lập tức từ 14.8% xuống 0.6%, mang lại trải nghiệm cuộn mượt mà 60 FPS.
