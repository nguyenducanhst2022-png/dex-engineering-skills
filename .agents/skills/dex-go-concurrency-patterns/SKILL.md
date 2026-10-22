---
name: dex-go-concurrency-patterns
description: Architect, synchronize, and debug high-throughput Go concurrent systems using channels, worker pools, sync.Pool, Context propagation, and race detection. Use when building scalable backend services in Golang.
---

# dex-go-concurrency-patterns

## 1. Purpose & Scope
Thiết kế, đồng bộ hóa và xử lý sự cố các hệ thống xử lý đồng thời hiệu năng cao trong Go (Golang Concurrency); áp dụng mô hình Worker Pools, Pipeline Channels, `sync.Pool`, truyền tải tín hiệu hủy qua `context.Context`, và triệt tiêu các lỗi Data Races, Goroutine Leaks và Deadlocks bằng công cụ Go Race Detector.

## 2. When to Use
- Dịch vụ Go bị rò rỉ bộ nhớ do số lượng Goroutines tăng vọt liên tục không giảm (Goroutine Leak).
- Xuất hiện cảnh báo nguy hiểm `DATA RACE` khi chạy kiểm thử hoặc biên dịch với cờ `-race`.
- Cần tối ưu hóa thông lượng xử lý hàng ngàn tác vụ nền song song mà không làm sập cơ sở dữ liệu.

## 3. When NOT to Use
- Không lạm dụng Goroutine cho các tác vụ tính toán siêu nhỏ in-memory (chi phí context switch của scheduler có thể lớn hơn thời gian chạy).
- Không chia sẻ bộ nhớ chung mà không có cơ chế khóa bảo vệ (Mutex) hoặc truyền tin (Channel).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mã nguồn Go có sử dụng từ khóa `go`, channels hoặc các cấu trúc gói `sync`.
- Số lượng tác vụ đồng thời mục tiêu (Concurrency limit).
- Yêu cầu về thời gian timeout và hủy bỏ tác vụ.
- **Điều kiện tiên quyết**:
- Cài đặt Go toolchain phiên bản mới nhất (Go 1.21+).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Share Memory by Communicating: 'Đừng giao tiếp bằng cách chia sẻ bộ nhớ; hãy chia sẻ bộ nhớ bằng cách giao tiếp' qua Channels.
- Goroutine Leak: Một goroutine bị block vĩnh viễn do chờ đọc/ghi vào một channel không có ai nhận hoặc thiếu tín hiệu hủy từ Context.
- `context.Context` Propagation: Mọi hàm thực hiện I/O hoặc đồng thời bắt buộc phải nhận `ctx context.Context` làm tham số đầu tiên để tôn trọng tín hiệu hủy bỏ hoặc timeout từ client.
- **Quy tắc quyết định kỹ thuật**:
- Bắt buộc kiểm tra `select` với trường hợp `case <-ctx.Done():` trong mọi vòng lặp chờ của goroutine.
- Luôn chạy toàn bộ unit và integration tests với cờ `-race` trong CI pipeline.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Gửi dữ liệu vào một unbuffered channel mà không có goroutine nào lắng nghe, khiến goroutine phát tin bị treo vĩnh viễn.

## 6. Step-by-Step Execution Workflow
1. Thiết kế mô hình đồng thời: xác định luồng producer, worker pool và consumer.
2. Cấu hình kích thước bounded worker pool để kiểm soát số lượng goroutine đồng thời.
3. Truyền `context.Context` xuyên suốt các tầng xử lý.
4. Sử dụng `sync.WaitGroup` hoặc `errgroup.Group` để thu thập kết quả và xử lý lỗi đồng bộ.
5. Chạy kiểm thử tự động với cờ race detector `go test -race ./...`.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```go
// Mô hình Worker Pool an toàn kèm Context Cancellation trong Go
package workerpool

import (
	"context"
	"golang.org/x/sync/errgroup"
)

func ProcessJobs(ctx context.Context, jobs []string, concurrency int) error {
	g, ctx := errgroup.WithContext(ctx)
	jobChan := make(chan string)

	// Khởi tạo các workers
	for i := 0; i < concurrency; i++ {
		g.Go(func() error {
			for {
				select {
				case <-ctx.Done():
					return ctx.Err()
				case job, ok := <-jobChan:
					if !ok {
						return nil
					}
					if err := executeJob(ctx, job); err != nil {
						return err
					}
				}
			}
		})
	}

	// Đẩy công việc vào channel
	g.Go(func() error {
		defer close(jobChan)
		for _, job := range jobs {
			select {
			case <-ctx.Done():
				return ctx.Err()
			case jobChan <- job:
			}
		}
		return nil
	})

	return g.Wait()
}
```

### Lệnh xác minh & thực thi:
```bash
# Chạy kiểm thử với cờ Go Race Detector
go test -v -race -count=5 ./...
```

## 8. Anti-Patterns & Common Traps
- Bỏ qua lỗi `DATA RACE` và cho rằng 'nó hiếm khi xảy ra ngoài đời'.
- Đọc/ghi biến map trong Go từ nhiều goroutine cùng lúc mà không có `sync.RWMutex` (kích hoạt panic fatal error của Go runtime).

## 9. Quality Gates & Acceptance Criteria
- 0 lỗi data race được phát hiện khi chạy toàn bộ test suite với cờ `-race`.
- Số lượng active goroutines trở về mức cơ sở sau khi hoàn thành đợt xử lý công việc.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Ngăn chặn tấn công làm cạn kiệt tài nguyên (Goroutine Exhaustion DoS) bằng cách luôn giới hạn kích thước worker pool.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Package xử lý đồng thời hoàn chỉnh sử dụng `errgroup`.
- Báo cáo kết quả kiểm thử `-race` sạch sẽ.

## 13. Related & Complementary Skills
dex-traffic-shaping-backpressure, dex-load-and-stress-testing, dex-backend-architecture

## 14. Realistic Usage Example
### Tình huống thực tế:
Một dịch vụ xử lý webhook viết bằng Go bị sập vì số lượng goroutines tăng vọt lên 400,000 khi downstream API bị chậm. Bằng cách tái cấu trúc sang kiến trúc Bounded Worker Pool với kích thước cố định 500 workers kết hợp `errgroup`, dịch vụ giữ mức tiêu thụ RAM ổn định dưới 80MB và xử lý trơn tru hàng triệu webhook mỗi ngày.
