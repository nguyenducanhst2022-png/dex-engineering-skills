---
name: dex-operational-game-days
description: Plan, orchestrate, and facilitate controlled chaos engineering game days and failure injection exercises to validate team incident response and system resilience. Use to prepare teams for catastrophic production events.
---

# dex-operational-game-days

## 1. Purpose & Scope
Lập kế hoạch, điều phối và thực thi các buổi diễn tập sự cố thực chiến có kiểm soát (Operational Game Days / Chaos Engineering Drills); chủ động cấy lỗi hạ tầng (kill pod, ngắt mạng, làm đầy ổ đĩa, trễ database) nhằm kiểm chứng năng lực phản ứng của đội ngũ kỹ sư và độ bền vững của hệ thống trong môi trường an toàn.

## 2. When to Use
- Chuẩn bị phát hành phiên bản hệ sinh thái mới với kiến trúc phân tán phức tạp.
- Định kỳ hàng quý để tôi luyện phản xạ xử lý sự cố cho các kỹ sư mới.
- Xác minh xem các cơ chế tự động phục hồi (Auto-healing, Failover) có thực sự hoạt động như thiết kế hay không.

## 3. When NOT to Use
- Không diễn tập trên Production vào những ngày cao điểm kinh doanh của công ty.
- Tuyệt đối không cấy lỗi nếu không có nút dừng khẩn cấp (Blast Radius & Abort Button) được kiểm chứng trước.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Giả thuyết kiểm chứng (Hypothesis: 'Nếu Region US-East bị mất kết nối, hệ thống sẽ tự chuyển sang US-West trong 60 giây và khách hàng không thấy lỗi 5xx').
- Công cụ cấy lỗi (Chaos Mesh, LitmusChaos, Gremlin, AWS Fault Injection Simulator).
- Kế hoạch an toàn và phân công vai trò (Incident Commander, Chaos Injector, Observers).
- **Điều kiện tiên quyết**:
- Có dashboard giám sát thời gian thực hiển thị chỉ số trải nghiệm người dùng (Steady-state metrics).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Blast Radius Control: Giới hạn phạm vi ảnh hưởng của lỗi (ví dụ: chỉ cấy lỗi trên 10% traffic thử nghiệm hoặc môi trường Staging).
- Stop-the-World Button: Bất kỳ ai trong buổi diễn tập nhận thấy rủi ro vượt tầm kiểm soát đều có quyền bấm nút hủy để hoàn trả hệ thống về nguyên trạng ngay lập tức.
- Steady-State Hypothesis: Đo lường trạng thái bình thường của hệ thống trước khi cấy lỗi để so sánh sự suy giảm trong suốt quá trình thử nghiệm.
- **Quy tắc quyết định kỹ thuật**:
- Nếu chỉ số nghiệp vụ cốt lõi giảm quá 5% trên môi trường thực tế: kích hoạt Abort ngay lập tức.
- Mọi kết quả dù thành công hay thất bại đều phải được ghi nhận công tâm, không trừng phạt (Blameless culture).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Kịch bản cấy lỗi làm xóa mất dữ liệu vĩnh viễn do không cô lập môi trường lưu trữ an toàn.

## 6. Step-by-Step Execution Workflow
1. Họp thống nhất kịch bản và giả thuyết cần kiểm chứng với các bên liên quan.
2. Kiểm tra trạng thái bình thường (Steady-state) của toàn bộ hệ thống.
3. Bắt đầu cấy lỗi ở mức nhẹ nhất (ví dụ: tạo 100ms network latency).
4. Quan sát phản ứng của hệ thống giám sát và hành động xử lý của đội trực ca.
5. Dừng cấy lỗi, kiểm tra khả năng tự phục hồi của hệ thống về trạng thái ban đầu.
6. Tổ chức buổi tổng kết rút kinh nghiệm và tạo danh sách cải tiến kỹ thuật.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Kịch bản Chaos Mesh: Giả lập trễ mạng 300ms đối với Database Pods
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: db-delay-game-day
spec:
  action: delay
  mode: all
  selector:
    namespaces: ['production-staging']
    labelSelectors: {'app': 'postgres'}
  delay:
    latency: '300ms'
    jitter: '20ms'
  duration: '10m'
```

### Lệnh xác minh & thực thi:
```bash
# Áp dụng kịch bản chaos và sẵn sàng lệnh xóa rollback khẩn cấp
kubectl apply -f chaos-scenario.yaml
# Lệnh Abort khẩn cấp:
kubectl delete -f chaos-scenario.yaml
```

## 8. Anti-Patterns & Common Traps
- Diễn tập bí mật kiểu đánh úp mà không thông báo cho ban quản lý và lead trực ca, gây hoảng loạn không cần thiết.
- Không chuẩn bị trước lệnh rollback dẫn đến hệ thống bị kẹt trong trạng thái lỗi sau buổi diễn tập.

## 9. Quality Gates & Acceptance Criteria
- Đội ngũ kỹ sư phát hiện và cô lập được lỗi trong vòng 5 phút kể từ khi cấy lỗi.
- Hệ thống tự động phục hồi 100% trong vòng 2 phút sau khi ngừng cấy lỗi.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Tuân thủ nghiêm ngặt ranh giới môi trường được cấp phép, không bao giờ để kịch bản chaos lan sang các cụm dữ liệu khách hàng chưa được bảo vệ.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Bản kế hoạch Game Day chi tiết (Run of Show).
- Báo cáo kết quả diễn tập và danh sách các lỗ hổng kiến trúc được phát hiện.

## 13. Related & Complementary Skills
dex-service-failover, dex-oncall-handover, dex-load-and-stress-testing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ngân hàng tổ chức Game Day giả lập sự cố sập một Availability Zone trên AWS. Trong buổi diễn tập, họ phát hiện cơ chế DNS failover bị kẹt do TTL của nhà mạng bị cache 24 giờ. Nhờ phát hiện trước trong môi trường diễn tập có kiểm soát, họ đã kịp thời chuyển sang dùng Anycast IP trước khi sự cố thật xảy ra.
