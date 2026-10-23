---
name: dex-jvm-performance-diagnostics
description: Diagnose and tune JVM memory, garbage collection pauses (G1GC, ZGC), thread contention, and JIT compilation using JFR, async-profiler, and visualgc. Use when Java/Kotlin applications suffer latency spikes or GC stalls.
---

# dex-jvm-performance-diagnostics

## 1. Purpose & Scope
Chẩn đoán, phân tích và tối ưu hóa hiệu năng chuyên sâu cho các ứng dụng chạy trên Java Virtual Machine (JVM: Java, Kotlin, Scala); phân tích các điểm dừng do dọn rác (GC Pauses), tối ưu bộ thu gom rác thế hệ mới (G1GC, ZGC, Shenandoah), điều tra nghẽn tranh chấp luồng (Thread Contention) và phân tích hành vi của bộ biên dịch JIT thông qua Java Flight Recorder (JFR) và async-profiler.

## 2. When to Use
- Dịch vụ Java gặp các đợt tăng vọt độ trễ (Latency Spikes P99 > 1s) do các đợt dừng Stop-The-World của bộ Garbage Collector.
- Ứng dụng ném lỗi `java.lang.OutOfMemoryError: Java heap space` hoặc `Metaspace`.
- Tỉ lệ chiếm dụng CPU của JVM ở mức 100% nhưng thông lượng xử lý nghiệp vụ không tăng.

## 3. When NOT to Use
- Không tự ý thêm hàng chục cờ JVM tuning (`-XX:...`) phức tạp copy từ internet vào production mà không có dữ liệu đo lường thực nghiệm.
- Không profiling liên tục với các công cụ instrumentation nặng (như JProfiler/YourKit) trên cụm production đang phục vụ tải đỉnh.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File ghi chép nhật ký bay (`.jfr` file).
- Garbage Collection logs (`-Xlog:gc*`).
- JVM Heap Dumps (`.hprof`) khi xảy ra OOM.
- **Điều kiện tiên quyết**:
- Ứng dụng chạy trên JVM hiện đại (OpenJDK 17 hoặc 21 LTS).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Stop-The-World (STW): Khoảng thời gian toàn bộ luồng ứng dụng bị tạm dừng để GC đánh dấu và di dời đối tượng trong bộ nhớ.
- ZGC (Low-Latency GC): Bộ thu gom rác có khả năng giữ thời gian tạm dừng STW dưới 1ms bất kể kích thước Heap từ 16MB đến 16TB.
- Allocation Rate vs Promotion Rate: Tốc độ cấp phát đối tượng mới quá nhanh khiến các đối tượng sống ngắn bị đẩy sớm sang Old Generation, kích hoạt Full GC nặng nề.
- **Quy tắc quyết định kỹ thuật**:
- Với các ứng dụng yêu cầu độ trễ cực thấp (P99 < 10ms): kích hoạt ZGC (`-XX:+UseZGC -XX:+ZGenerational`).
- Bắt buộc bật cờ tự động sinh Heap Dump khi xảy ra OOM (`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/log/`).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cấu hình dung lượng Heap quá lớn (`-Xmx32g`) với bộ GC cũ (CMS/Parallel) khiến một đợt Full GC có thể làm đóng băng toàn bộ hệ sinh thái trong 30 giây.

## 6. Step-by-Step Execution Workflow
1. Bật GC logging tiêu chuẩn trong Java 17+ (`-Xlog:gc*:file=/var/log/gc.log:time,uptime,level,tags:filecount=5,filesize=50m`).
2. Chạy async-profiler để lấy Flamegraph phân bổ bộ nhớ và CPU mà không gây gián đoạn hệ thống.
3. Phân tích file GC log bằng công cụ GCeasy hoặc `jclarity`.
4. Điều chỉnh các thông số Heap Size và chuyển đổi sang Generational ZGC.
5. Kiểm tra lại sự cải thiện của P99 latency dưới bài kiểm thử tải mô phỏng.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```bash
# Cấu hình cờ JVM tối ưu cho Java 21 microservices độ trễ thấp
JAVA_OPTS="-Xms4g -Xmx4g \
  -XX:+UseZGC \
  -XX:+ZGenerational \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/dumps/oom.hprof \
  -Xlog:gc*:file=/var/log/gc.log:time,level,tags:filecount=5,filesize=20M \
  -Djava.security.egd=file:/dev/./urandom"
```

### Lệnh xác minh & thực thi:
```bash
# Chạy async-profiler thu thập CPU flamegraph trong 30 giây
./async-profiler/bin/asprof -d 30 -f /tmp/flamegraph.html <PID>
```

## 8. Anti-Patterns & Common Traps
- Gọi hàm `System.gc()` thủ công trong mã nguồn ứng dụng.
- Đặt kích thước Heap khởi đầu `-Xms` quá nhỏ so với kích thước tối đa `-Xmx`, khiến JVM liên tục phải xin thêm bộ nhớ từ hệ điều hành.

## 9. Quality Gates & Acceptance Criteria
- Thời gian tạm dừng GC Pause P99 phải dưới 2ms đối với các microservices tài chính.
- Không xảy ra bất kỳ đợt Full GC nào trong quá trình vận hành tải bình thường.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Bảo vệ file Heap Dump sinh ra vì nó có thể chứa các thông tin nhạy cảm (mật khẩu, khóa giải mã) trong bộ nhớ heap.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- File ghi vết JFR / Flamegraph phân tích điểm nghẽn CPU và phân bổ đối tượng.
- Bộ cờ khởi động JVM tối ưu hóa cho môi trường container Kubernetes.

## 13. Related & Complementary Skills
dex-performance-optimization, dex-load-and-stress-testing, dex-software-architecture

## 14. Realistic Usage Example
### Tình huống thực tế:
Một hệ thống giao dịch chứng khoán viết bằng Spring Boot bị trễ đột biến 800ms cứ mỗi 15 phút một lần, khiến các lệnh giao dịch bị hủy do timeout. Sử dụng async-profiler và phân tích GC log, kỹ sư phát hiện bộ G1GC bị quá tải do một thư viện mapping tạo ra hàng triệu đối tượng DTO rác mỗi giây. Chuyển sang dùng Java 21 Generational ZGC kết hợp tái cấu trúc object reuse đã đưa thời gian GC pause về mức dưới 0.8ms ổn định tuyệt đối.
