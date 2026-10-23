---
name: dex-desktop-gpu-inference-fallback
description: Integrate desktop GPU AI inference engines (DirectML, ONNX Runtime, CUDA, Vulkan). Detect hardware capabilities and manage seamless fallback to optimized multi-threaded CPU paths.
---

# dex-desktop-gpu-inference-fallback

## 1. Purpose & Scope
Tích hợp và tối ưu hóa suy luận mô hình trí tuệ nhân tạo tăng tốc phần cứng (Desktop GPU Inference) cho ứng dụng máy tính cá nhân; cấu hình các Execution Providers tiên tiến (DirectML cho card đồ họa AMD/Intel/NVIDIA trên Windows, ONNX Runtime, Vulkan, TensorRT); tự động nhận diện năng lực thiết bị (Adapter Enumeration qua DirectX/DXGI) và xây dựng đường dự phòng chuyển tiếp mượt mà (Seamless CPU Fallback) sang tập lệnh CPU đa luồng (OpenVINO, AVX2/AVX-512) khi thiết bị không đủ VRAM hoặc thiếu driver phù hợp.

## 2. When to Use
- Khi tích hợp các mô hình nơ-ron cục bộ (Local LLM, Whisper Audio Transcription, Object Detection, Background Removal) vào ứng dụng desktop.
- Khi ứng dụng bị sập với lỗi Out of Device Memory (VRAM Exhaustion) trên các máy tính sử dụng card đồ họa tích hợp (iGPU).
- Khi cần phần mềm chạy được trên 100% thiết bị của người dùng bất kể có card đồ họa rời hay không.

## 3. When NOT to Use
- Khi gọi các mô hình AI thông qua Cloud API (OpenAI, Anthropic, Gemini) nơi việc suy luận diễn ra trên máy chủ từ xa.
- Khi khối lượng suy luận quá nhỏ (<1ms) mà chi phí sao chép dữ liệu từ CPU sang GPU (PCIe transfer overhead) lớn hơn thời gian tính toán.

## 4. Prerequisites & Input Context
- **Hệ điều hành:** Windows 10/11 x64, DirectX 12 Agility SDK.
- **Thư viện AI:** ONNX Runtime (`onnxruntime-directml`), DirectML SDK, hoặc llama.cpp.

## 5. Core Concepts & Taxonomy
- **DirectML (DirectX Machine Learning):** API tăng tốc học máy cấp thấp của Microsoft hoạt động trên mọi card đồ họa tương thích DirectX 12 của Intel, AMD, NVIDIA và Qualcomm.
- **VRAM Budget Management:** Kiểm tra dung lượng bộ nhớ video khả dụng trước khi nạp mô hình; nếu mô hình yêu cầu 4GB VRAM nhưng máy chỉ còn 1.5GB, lập tức kích hoạt đường CPU Fallback.
- **Execution Provider Priority Chain:** Chuỗi ưu tiên nạp backend: DirectML GPU -> OpenVINO NPU/CPU -> Multithreaded AVX2 CPU.

## 6. Step-by-Step Execution Workflow
1. Sử dụng DXGI API (`IDXGIFactory6::EnumAdapterByGpuPreference`) để liệt kê tất cả card đồ họa có trên hệ thống.
2. Kiểm tra dung lượng bộ nhớ video chuyên dụng (`DedicatedVideoMemory`) và phiên bản tính năng DirectX 12 (`D3D_FEATURE_LEVEL_12_0`).
3. Thử nghiệm khởi tạo ONNX Runtime InferenceSession với DirectML Execution Provider trong khối kiểm soát ngoại lệ.
4. Nếu khởi tạo thất bại (thiếu driver, không đủ VRAM), ghi log cảnh báo và chuyển sang CPU Execution Provider với các cờ tối ưu hóa luồng (`intra_op_num_threads`).
5. Thực hiện suy luận thử nghiệm trên một tensor nhỏ (Warm-up Inference) để biên dịch shader đồ họa trước khi xử lý dữ liệu thật.
6. Theo dõi mức tiêu thụ bộ nhớ và giải phóng tài nguyên session khi người dùng đóng tính năng.

## 7. Concrete Examples
### Khoi tao ONNX Runtime linh hoat ho tro DirectML GPU va CPU Fallback trong C++:
```cpp
#include <onnxruntime_cxx_api.h>
#include <dml_provider_factory.h>
#include <dxgi1_6.h>
#include <iostream>
#include <memory>

std::unique_ptr<Ort::Session> create_inference_session(Ort::Env& env, const wchar_t* model_path) {
    Ort::SessionOptions session_options;
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

    bool gpu_initialized = false;

    // 1. Thu nghiem khoi tao DirectML GPU Backend
    try {
        // ID device 0 la GPU chinh
        OrtStatus* status = OrtSessionOptionsAppendExecutionProvider_DML(session_options, 0);
        if (status == nullptr) {
            auto session = std::make_unique<Ort::Session>(env, model_path, session_options);
            std::cout << "[AI ENGINE] Hardware Acceleration enabled via DirectML (GPU)." << std::endl;
            gpu_initialized = true;
            return session;
        }
    } catch (const std::exception& ex) {
        std::cerr << "[WARN] DirectML GPU init failed: " << ex.what() << ". Falling back to CPU..." << std::endl;
    }

    // 2. Fallback sang CPU da luong neu GPU that bai
    if (!gpu_initialized) {
        Ort::SessionOptions cpu_options;
        cpu_options.SetIntraOpNumThreads(4); // 4 luong CPU
        cpu_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
        auto session = std::make_unique<Ort::Session>(env, model_path, cpu_options);
        std::cout << "[AI ENGINE] Running on Portable Optimized CPU Fallback." << std::endl;
        return session;
    }
    return nullptr;
}
```

## 8. Anti-Patterns & Common Traps
- **Unbounded GPU Memory Allocation:** Cố ép mô hình lớn 8GB vào card iGPU chia sẻ RAM hệ thống khiến toàn bộ máy tính bị đứng hình (TDR - Timeout Detection and Recovery).
- **Hardcoded CUDA Dependency:** Chỉ hỗ trợ CUDA khiến 100% người dùng sử dụng card đồ họa AMD Radeon hoặc Intel Arc không thể sử dụng tính năng AI.
- **Freezing UI Thread on Warm-up:** Chạy lượt suy luận warm-up đầu tiên trên Main Thread làm giao diện bị đơ 3-5 giây trong khi DirectML biên dịch pipeline state objects.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tự động nhận diện GPU và kích hoạt DirectML thành công trên các phần cứng có hỗ trợ DirectX 12.
- **QG-02**: Tự động chuyển đổi sang CPU Fallback an toàn 100% khi chạy trên môi trường không có GPU hoặc khi GPU bị lỗi bộ nhớ.
- **QG-03**: Kết quả đầu ra của mô hình giữa chế độ GPU và chế độ CPU hoàn toàn đồng nhất về mặt toán học.

## 10. Security & Safety Boundaries
- Quét kiểm tra tệp mô hình ONNX trước khi nạp; ngăn ngừa các mô hình chứa cấu trúc đồ thị độc hại (Model Serialization Exploits).

## 11. Platform Adapters
- **Runtimes**: ONNX Runtime DirectML, DirectX 12 / DXGI, PyTorch DirectML, OpenVINO CPU.

## 12. Deliverables & Output Artifacts
- Lớp quản lý bộ máy suy luận AI đa nền tảng (`desktop_ai_engine.cpp` / `inference.rs`).
- Báo cáo đo kiểm hiệu năng suy luận so sánh giữa GPU và CPU fallback.

## 13. Related & Complementary Skills
dex-native-simd-dispatch, dex-windows-app-crash-dumps, dex-windows-app-startup-profiling

## 14. Realistic Usage Example
```powershell
# Kiem tra danh sach card do hoa DirectX tren may tinh bang dxdiag
dxdiag /t dxdiag_report.txt; Select-String "Card name:" dxdiag_report.txt
```
