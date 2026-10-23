---
name: dex-dart-flutter-state-debugging
description: Profile, diagnose, and optimize Dart Flutter reactive state lifecycles, widget rebuild cascades, memory leaks, and DevTools performance traces. Use when debugging unresponsive Flutter apps or memory footprint issues.
---

# dex-dart-flutter-state-debugging

## 1. Purpose & Scope
Chẩn đoán và khắc phục sự cố vòng đời trạng thái (State Lifecycle) trong ứng dụng Dart Flutter; phát hiện và tối ưu hóa hiện tượng tái dựng giao diện dây chuyền (Widget Rebuild Cascades), rò rỉ bộ nhớ (Memory Leaks trong StreamControllers và Notifiers), và phân tích vết hiệu năng qua Flutter DevTools.

## 2. When to Use
- Khi ứng dụng Flutter bị tụt khung hình (Jank / Drop frames dưới 60fps) khi người dùng cuộn danh sách hoặc thao tác trên màn hình.
- Khi bộ nhớ RAM của ứng dụng tăng liên tục và không tự giải phóng sau khi người dùng chuyển trang.
- Khi giao diện không cập nhật đúng dữ liệu sau khi state thay đổi hoặc bị cập nhật lặp lại vô tận.

## 3. When NOT to Use
- Khi ứng dụng là website HTML/JS truyền thống hoặc ứng dụng native viết bằng Kotlin/Swift.
- Khi chỉ thay đổi màu sắc hoặc kích thước text đơn giản không ảnh hưởng tới logic quản lý trạng thái.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn Flutter, công cụ quản lý state đang dùng (Provider, Riverpod, Bloc, hoặc Signals), Flutter SDK và DevTools.
- **Quyền hạn truy cập:** Quyền chạy ứng dụng ở chế độ Profile Mode (`flutter run --profile`).

## 5. Core Concepts & Taxonomy
- **Widget Rebuild Cascade:** Hiện tượng một widget gốc (Root Widget) gọi `setState()` hoặc cập nhật Provider làm toàn bộ cây widget con bên dưới phải rebuild lại không cần thiết.
- **`const` Constructor Optimization:** Sử dụng từ khóa `const` để báo hiệu cho Flutter framework biết widget là bất biến và bỏ qua việc tạo lại đối tượng trong bộ nhớ.
- **Dispose Lifecycle Contract:** Bắt buộc phải đóng các kết nối (`StreamController.close()`, `TextEditingController.dispose()`, `AnimationController.dispose()`) trong hàm `dispose()` của State.

## 6. Step-by-Step Execution Workflow
1. Khởi động ứng dụng Flutter ở chế độ Profile Mode và mở Flutter DevTools (tab Performance và Memory).
2. Bật cờ `Track Widget Rebuilds` để trực quan hóa số lần mỗi widget bị vẽ lại trên màn hình.
3. Nhận diện các widget bị rebuild liên tục và thu hẹp phạm vi lắng nghe state (sử dụng `Selector`, `Consumer`, hoặc `ref.watch` cục bộ).
4. Bổ sung từ khóa `const` cho toàn bộ các widget tĩnh và cấu hình linter `prefer_const_constructors`.
5. Thực hiện Snapshot bộ nhớ RAM (Memory Allocation Profile) trước và sau khi mở một màn hình 10 lần: kiểm tra xem số lượng instances có tăng dần không.
6. Rà soát và bổ sung lệnh `dispose()` cho tất cả controllers và listeners bị bỏ quên.
7. Chạy lại bài đo kiểm để xác nhận tốc độ hiển thị đạt chuẩn 60fps/120fps ổn định.

## 7. Concrete Examples
### Ví dụ tối ưu hóa tái dựng widget và quản lý vòng đời trong Flutter:
```dart
import 'package:flutter/material.dart';

class OptimizedCounterView extends StatefulWidget {
  const OptimizedCounterView({super.key});

  @override
  State<OptimizedCounterView> createState() => _OptimizedCounterViewState();
}

class _OptimizedCounterViewState extends State<OptimizedCounterView> {
  late final ValueNotifier<int> _counter;
  late final TextEditingController _textController;

  @override
  void initState() {
    super.initState();
    _counter = ValueNotifier<int>(0);
    _textController = TextEditingController();
  }

  @override
  void dispose() {
    // BẮT BUỘC: Hủy controller để chống rò rỉ bộ nhớ
    _counter.dispose();
    _textController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('State Debugging')), // const widget không bị rebuild
      body: Center(
        // CHỈ rebuild widget con này khi counter thay đổi, không rebuild toàn bộ Scaffold
        child: ValueListenableBuilder<int>(
          valueListenable: _counter,
          builder: (context, value, child) {
            return Text('Count: $value', style: const TextStyle(fontSize: 24));
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _counter.value++,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## 8. Anti-Patterns & Common Traps
- **Calling setState at Root Widget:** Đặt `setState()` ở cấp độ toàn màn hình khiến toàn bộ layout phức tạp bị vẽ lại từ đầu sau mỗi thao tác gõ phím.
- **Missing dispose Calls:** Quên gọi `controller.dispose()` khiến các Stream tiếp tục lắng nghe ngầm trong RAM sau khi màn hình đã bị đóng.
- **Creating Objects inside build Method:** Khởi tạo `Paint()`, `TextStyle()` hoặc danh sách mới bên trong hàm `build()` gây áp lực lớn lên bộ thu gom rác (GC pressure).

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Mã nguồn tuân thủ 100% quy tắc phân tích tĩnh `flutter_lints` (không có warning về `prefer_const_constructors`).
- **QG-07**: Tốc độ khung hình duy trì ổn định không bị giật lag (Zero jank frames > 16.6ms) trong bài kiểm thử cuộn danh sách.
- **QG-10**: Không có hiện tượng rò rỉ bộ nhớ (Memory Leak) sau 20 chu kỳ mở và đóng màn hình.

## 10. Security & Safety Boundaries
- Xóa sạch nội dung bộ nhớ đệm của các trường nhập dữ liệu nhạy cảm (như thẻ tín dụng hoặc mật khẩu) ngay trong hàm `dispose()`.
- Tránh lưu trữ trạng thái người dùng nhạy cảm dưới dạng biến toàn cục công khai (global variables).

## 11. Platform Adapters
- **Profiling Tools**: Flutter DevTools, Observatory, Dart VM Service.
- **State Management**: Riverpod, flutter_bloc, Provider, Signals.

## 12. Deliverables & Output Artifacts
- Mã nguồn Flutter đã được tối ưu hóa ranh giới State và cấu hình `const`.
- Báo cáo phân tích Memory Leak trước và sau khi khắc phục.
- Biểu đồ Timeline Performance ghi nhận tốc độ khung hình 60fps/120fps.

## 13. Related & Complementary Skills
dex-mobile-performance-profiling, dex-frontend-performance, dex-concurrency-state

## 14. Realistic Usage Example
```powershell
# Chạy phân tích tĩnh mã nguồn Flutter để phát hiện vi phạm quy tắc linter
flutter analyze

# Chạy kiểm thử tự động hiệu năng widget
flutter test test/performance/widget_rebuild_test.dart
```
