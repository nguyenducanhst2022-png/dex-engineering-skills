---
name: dex-media-content-ingest-moderation
description: Validate, inspect, and quarantine incoming media assets during ingest. Detect container-level malformations, verify audio/video codec integrity, and isolate malicious payloads.
---

# dex-media-content-ingest-moderation

## 1. Purpose & Scope
Kiểm định, rà soát và cách ly tự động các tệp đa phương tiện đầu vào trong pipeline nạp nội dung (Media Ingest Moderation Pipeline); phát hiện các dị tật ở tầng container (MP4 atom corruption, MKV header malformation), xác minh tính toàn vẹn của luồng âm thanh/hình ảnh, ngăn chặn các kỹ thuật chèn mã độc vào metadata (ID3/EXIF exploits) và cách ly an toàn các tệp nguy hiểm.

## 2. When to Use
- Khi tiếp nhận tệp video/âm thanh từ người dùng tải lên (UGC platforms, cloud storage).
- Khi xây dựng rào chắn an ninh trước khi đưa tệp vào cụm máy chủ giải mã và transcoding tập trung.
- Khi cần xác minh nhanh một tệp media có đúng là định dạng thực tế hay chỉ là tệp thực thi độc hại ngụy trang đổi đuôi mở rộng.

## 3. When NOT to Use
- Khi tệp media được sinh ra từ chính các máy chủ nội bộ đã được chứng thực chữ ký số an toàn.
- Khi kiểm duyệt nội dung hình ảnh nhạy cảm về mặt thị giác (sử dụng các mô hình Computer Vision Moderation chuyên dụng).

## 4. Prerequisites & Input Context
- **Công cụ kiểm tra:** MediaInfo CLI, FFprobe, hoặc thư viện `mutagen` / `exiftool` chạy trong sandbox cô lập.
- **Môi trường:** Container không có quyền root (unprivileged container) với giới hạn RAM và CPU chặt chẽ.

## 5. Core Concepts & Taxonomy
- **Magic Byte Validation:** Kiểm tra các byte nhận diện đầu tệp (ví dụ `ftypisom` trong MP4, `Eß£` trong MKV/WebM) thay vì tin tưởng phần mở rộng của tệp.
- **Container Bomb Protection:** Ngăn ngừa các tệp chứa cấu trúc đệ quy hoặc thông số kích thước ảo (như atom MP4 có kích thước 1000 Terabyte) gây sập parser.
- **Quarantine Isolation:** Di chuyển các tệp lỗi hoặc nghi ngờ vào vùng lưu trữ cách ly biệt lập, ngăn chặn việc kích hoạt tự động các worker tiếp theo.

## 6. Step-by-Step Execution Workflow
1. Tiếp nhận tệp và kiểm tra Magic Bytes ở 64 byte đầu tiên của tệp.
2. Chạy `ffprobe` với các cờ hạn chế quyền (`-v error -show_entries stream=codec_type,codec_name -of json`).
3. Quét sạch các trường siêu dữ liệu (metadata tags) để phát hiện ký tự điều khiển lạ hoặc chuỗi nghi ngờ SQL Injection / Command Injection.
4. Xác nhận sự tồn tại của ít nhất một luồng video hoặc audio hợp lệ có thời lượng lớn hơn 0.
5. Nếu phát hiện tệp hỏng hoặc có cấu trúc bất thường, đánh dấu trạng thái QUARANTINED và gửi thông báo kiểm toán.
6. Nếu tệp vượt qua toàn bộ các bài kiểm tra, chuyển tệp sang bucket chính để tiến hành transcoding.

## 7. Concrete Examples
### Script Python kiem tra va cach ly tep media doc hai / bi hong:
```python
import subprocess
import json
import os
import shutil

QUARANTINE_DIR = "/var/media/quarantine"
SAFE_DIR = "/var/media/processing"

def inspect_and_quarantine(file_path):
    # 1. Kiem tra dung luong co ban
    if os.path.getsize(file_path) == 0:
        return quarantine(file_path, "Empty file")
        
    # 2. Chay ffprobe trong sandbox bounded timeout 5s
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,format_name:stream=codec_type,codec_name,width,height",
        "-of", "json", file_path
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if proc.returncode != 0:
            return quarantine(file_path, f"Probe error: {proc.stderr[:100]}")
            
        data = json.loads(proc.stdout)
        streams = data.get("streams", [])
        if not streams:
            return quarantine(file_path, "No valid audio/video streams found")
            
        # Kiem tra kich thuoc hop le
        for s in streams:
            if s.get("codec_type") == "video":
                w, h = s.get("width", 0), s.get("height", 0)
                if w > 8192 or h > 8192:
                    return quarantine(file_path, f"Extreme dimensions: {w}x{h}")
                    
        # File an toan
        shutil.move(file_path, os.path.join(SAFE_DIR, os.path.basename(file_path)))
        print(f"File {file_path} PASSED inspection.")
        return True
    except subprocess.TimeoutExpired:
        return quarantine(file_path, "Parser timeout - potential zip/container bomb")

def quarantine(file_path, reason):
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    dest = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
    shutil.move(file_path, dest)
    print(f"[QUARANTINE] {file_path} isolated. Reason: {reason}")
    return False
```

## 8. Anti-Patterns & Common Traps
- **Trusting User-Supplied File Extensions:** Cho phép tệp `.mp4` đi thẳng vào pipeline transcoding mà không kiểm tra magic bytes khiến tệp script độc hại được thực thi.
- **Running Transcoders as Root:** Chạy FFmpeg bằng quyền root khiến kẻ tấn công có thể chiếm toàn quyền điều khiển máy chủ nếu khai thác được lỗ hổng parser.
- **Unbounded Processing Timeout:** Không đặt timeout khi phân tích cú pháp tệp khiến worker bị treo vĩnh viễn khi gặp các tệp lặp cấu trúc vô tận.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% tệp nạp vào phải vượt qua kiểm tra magic bytes và cấu trúc container hợp lệ.
- **QG-02**: Mọi tiến trình kiểm tra (probe) đều bị giới hạn thời gian thực thi tối đa 5 giây và RAM tối đa 512MB.
- **QG-03**: Các tệp bị lỗi hoặc vi phạm chính sách được cách ly tự động 100% không để lọt vào pipeline chính.

## 10. Security & Safety Boundaries
- Thực thi cơ chế phòng thủ chiều sâu (Defense-in-Depth); cô lập parser trong sandbox cgroups/seccomp không có kết nối mạng internet.

## 11. Platform Adapters
- **Runtimes**: FFprobe, MediaInfo, Python mutagen, Linux seccomp sandbox.

## 12. Deliverables & Output Artifacts
- Kịch bản điều phối kiểm duyệt nạp tệp (`ingest_moderator.py`).
- Báo cáo nhật ký cách ly tệp độc hại (`quarantine_audit.log`).

## 13. Related & Complementary Skills
dex-video-transcoding-ladders, dex-media-metadata-normalization

## 14. Realistic Usage Example
```bash
# Kiem tra nhanh container media bang mediainfo
mediainfo --Output=JSON suspicious_upload.bin
```
