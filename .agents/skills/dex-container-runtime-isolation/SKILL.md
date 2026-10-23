---
name: dex-container-runtime-isolation
description: Harden, audit, and enforce container runtime boundaries using rootless containers, seccomp profiles, AppArmor/SELinux policies, and microVM sandboxes (gVisor, Kata). Use when running untrusted workloads and multi-tenant compute.
---

# dex-container-runtime-isolation

## 1. Purpose & Scope
Gia cố, kiểm toán và thực thi các ranh giới cô lập thời gian chạy của container (Container Runtime Isolation); áp dụng chế độ container không root (Rootless), hồ sơ lọc cuộc gọi hệ thống (seccomp profiles), chính sách AppArmor/SELinux và hộp cát microVM (gVisor, Kata Containers) nhằm ngăn chặn hoàn toàn nguy cơ thoát hộp cát (Container Escape).

## 2. When to Use
- Khi nền tảng cho phép người dùng hoặc khách hàng tải lên và thực thi mã tùy biến (Untrusted Code Execution).
- Khi chạy các dịch vụ nhiều người thuê (Multi-Tenant Compute) trên cùng một cụm máy chủ phần cứng.
- Khi kiểm toán tuân thủ an ninh container theo chuẩn CIS Kubernetes Benchmark.

## 3. When NOT to Use
- Khi tiến hành phát triển ứng dụng cục bộ trên máy trạm mà không có yêu cầu đặc biệt về bảo mật cô lập.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cấu hình Docker / Kubernetes Pod Security Standards, kernel Linux hỗ trợ namespaces và cgroups v2.
- **Quyền hạn truy cập:** Quyền quản trị cụm máy chủ (Root / ClusterAdmin) để cài đặt runtime handlers.

## 5. Core Concepts & Taxonomy
- **Rootless Containers:** Tiến trình bên trong container chạy dưới quyền user thông thường kể cả khi ánh xạ thành UID 0 trong namespace, bảo đảm không có quyền root thật trên máy chủ.
- **Seccomp (Secure Computing Mode):** Lọc và chặn đứng các cuộc gọi hệ thống (syscalls) nguy hiểm mà container không bao giờ cần dùng (như `ptrace`, `reboot`, `clone3`).
- **MicroVM / Kernel Sandboxing (gVisor):** Đánh chặn các syscalls của ứng dụng và xử lý thông qua một kernel độc lập viết bằng Go (Sentry), không cho phép tương tác trực tiếp với host kernel.

## 6. Step-by-Step Execution Workflow
1. Khảo sát danh sách các syscalls mà ứng dụng thực sự cần thực thi bằng công cụ audit (`strace` hoặc `ebpf`).
2. Xây dựng hồ sơ lọc Seccomp chặn đứng hơn 250 syscalls không cần thiết.
3. Cấu hình `SecurityContext` trong Kubernetes Pod: bật `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, và `runAsNonRoot: true`.
4. Tích hợp runtime handler gVisor (`runsc`) hoặc Kata Containers cho các namespace chứa mã không tin cậy.
5. Kiểm tra khả năng chống chịu bằng cách chạy các công cụ giả lập tấn công thoát hộp cát (Container Escape PoCs).
6. Giám sát các sự kiện vi phạm chính sách thời gian thực bằng Falco hoặc Tetragon.

## 7. Concrete Examples
### Cấu hình Pod Kubernetes bảo mật cao (Restricted Security Profile) và gVisor:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hardened-untrusted-runner
spec:
  runtimeClassName: gvisor # Chay tren nhan gVisor cach ly hoan toan host kernel
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: runner
    image: untrusted-user-code:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL # Loai bo 100% Linux Capabilities
    resources:
      limits:
        memory: "512Mi"
        cpu: "500m"
```

## 8. Anti-Patterns & Common Traps
- **Running in Privileged Mode:** Chạy container với cờ `--privileged` làm vô hiệu hóa toàn bộ cơ chế bảo vệ của Linux kernel.
- **Mounting Docker Socket:** Gắn kết `/var/run/docker.sock` vào trong container cho phép bất kỳ ai bên trong chiếm quyền root toàn bộ máy chủ host.
- **Mutable Root Filesystem:** Cho phép ghi vào thư mục gốc của container khiến mã độc có thể tải thêm công cụ tấn công vào hệ thống.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% container chạy mã bên ngoài bắt buộc sử dụng runtime sandbox (gVisor hoặc Kata).
- **QG-04**: `allowPrivilegeEscalation` được đặt là `false` và toàn bộ Capabilities bị gỡ bỏ (`drop: [ALL]`).
- **QG-06**: Hệ thống tệp gốc của container là chỉ đọc (`readOnlyRootFilesystem: true`).

## 10. Security & Safety Boundaries
- Chặn đứng hoàn toàn các cuộc tấn công khai thác lỗ hổng kernel Linux (Dirty COW, Dirty Pipe) từ bên trong container.

## 11. Platform Adapters
- **Runtimes**: gVisor (runsc), Kata Containers, Podman Rootless, containerd.
- **Monitoring**: Falco, Cilium Tetragon, Tracee.

## 12. Deliverables & Output Artifacts
- Hồ sơ lọc Seccomp tùy biến cho từng loại workload.
- Mẫu cấu hình Kubernetes Pod Security Standards (Restricted).
- Kịch bản kiểm thử thẩm định ranh giới cách ly runtime.

## 13. Related & Complementary Skills
dex-execution-sandbox-policies, dex-secretless-cicd-oidc, dex-api-authorization-matrix-tests

## 14. Realistic Usage Example
```powershell
# Kiểm tra trạng thái Pod Security Standards trên cụm Kubernetes
kubectl get ns --show-labels

# Kiểm tra runtime handler của pod đang chạy
kubectl get pod hardened-untrusted-runner -o jsonpath='{.spec.runtimeClassName}'
```
