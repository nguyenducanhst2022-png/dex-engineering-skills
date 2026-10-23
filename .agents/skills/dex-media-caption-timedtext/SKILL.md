---
name: dex-media-caption-timedtext
description: Process, convert, validate, and synchronize timed-text caption formats (WebVTT, TTML, SRT). Detect cue collision overlaps, enforce WCAG accessibility standards, and support multi-language tracks.
---

# dex-media-caption-timedtext

## 1. Purpose & Scope
Xử lý, chuyển đổi, xác thực cú pháp và đồng bộ hóa các định dạng phụ đề và văn bản theo thời gian (Timed Text: WebVTT, TTML, SubRip SRT); phát hiện và tự động sửa các lỗi va chạm mốc thời gian (overlapping cues), bảo đảm tuân thủ tiêu chuẩn tiếp cận tiếp cận người khuyết tật (WCAG 2.1 AA / FCC closed captioning rules), và quản lý đa ngôn ngữ trong luồng phát trực tuyến HLS/DASH.

## 2. When to Use
- Khi nhập kho và phân phối phụ đề đa ngôn ngữ cho phim, khóa học trực tuyến hoặc chương trình truyền hình.
- Khi chuyển đổi kho phụ đề định dạng cũ (.srt, .scc) sang chuẩn web hiện đại (.vtt) tương thích HTML5 `<track>`.
- Khi phụ đề hiển thị sai lệch mốc thời gian (lệch khẩu hình) hoặc 2 câu thoại đè chồng lên nhau trên màn hình.

## 3. When NOT to Use
- Khi xử lý văn bản tài liệu tĩnh (PDF, DOCX) không gắn liền với trục thời gian của media.
- Khi tạo phụ đề tự động bằng mô hình AI Speech-to-Text (sử dụng các skill về Speech Recognition).

## 4. Prerequisites & Input Context
- **Tệp phụ đề:** Tệp văn bản định dạng `.vtt`, `.srt`, hoặc `.ttml`.
- **Công cụ kiểm tra:** Python `webvtt-py`, `pycaption`, hoặc bộ validator W3C Timed Text.

## 5. Core Concepts & Taxonomy
- **Cue Payload Formatting:** Cú pháp đánh dấu trong WebVTT bao gồm mốc bắt đầu `-->` mốc kết thúc, cùng các chỉ thị căn vị trí (line, position, align, size).
- **Drift Synchronization:** Hiện tượng phụ đề bị trôi dần về cuối phim do sự không khớp giữa tốc độ khung hình (23.976 fps drop-frame vs 24 fps true).
- **WCAG Captioning Standards:** Quy tắc hiển thị tối đa 2 dòng văn bản trên màn hình cùng một lúc, không vượt quá 37 ký tự mỗi dòng và tốc độ đọc tối ưu 160–180 từ/phút.

## 6. Step-by-Step Execution Workflow
1. Phân tích cú pháp tệp phụ đề và kiểm tra dòng tiêu đề bắt buộc (`WEBVTT` header ở dòng đầu tiên).
2. Kiểm tra tính tăng dần đơn điệu của trục thời gian: `start_time < end_time` và `start_time[n] >= start_time[n-1]`.
3. Phát hiện các đoạn cue bị chồng lấn thời gian vô lý và tách biệt thành các dòng riêng biệt.
4. Làm sạch các thẻ HTML không an toàn hoặc ký tự mã hóa Unicode lỗi thời.
5. Đóng gói phụ đề vào HLS Master Playlist dưới dạng thẻ `#EXT-X-MEDIA:TYPE=SUBTITLES` với mã ngôn ngữ chuẩn ISO 639-1/2.
6. Kiểm thử việc hiển thị trên trình phát HTML5 và khẳng định không có lỗi lệch khung.

## 7. Concrete Examples
### Script Python xác thực và làm sạch tệp phụ đề WebVTT:
```python
import webvtt

def validate_and_clean_vtt(input_path, output_path):
    vtt = webvtt.read(input_path)
    cleaned_cues = []
    
    prev_end = "00:00:00.000"
    for idx, cue in enumerate(vtt):
        # 1. Kiem tra thoi gian bat dau phai nho hon thoi gian ket thuc
        assert cue.start < cue.end, f"Invalid duration at cue {idx}: {cue.start} -> {cue.end}"
        
        # 2. Canh bao va sua neu co va cham chong lan
        if cue.start < prev_end:
            print(f"[WARN] Overlapping cue detected at {cue.start}, adjusting...")
            cue.start = prev_end
            
        # 3. Kiem tra so dong khong vuot qua 2 dong
        lines = [line.strip() for line in cue.text.split('\n') if line.strip()]
        if len(lines) > 2:
            print(f"[WARN] Cue {idx} has {len(lines)} lines, collapsing to 2 lines.")
            cue.text = " ".join(lines[:-1]) + "\n" + lines[-1]
            
        prev_end = cue.end
        cleaned_cues.append(cue)
        
    vtt.save(output_path)
    print(f"Validated {len(cleaned_cues)} cues successfully.")

validate_and_clean_vtt("subs_raw.vtt", "subs_clean.vtt")
```

## 8. Anti-Patterns & Common Traps
- **Missing WEBVTT Header:** Lưu tệp chỉ có các mốc giờ mà thiếu chữ `WEBVTT` ở đầu tệp khiến trình duyệt Safari từ chối tải phụ đề hoàn toàn.
- **Comma vs Period Millisecond Delimiters:** Dùng dấu phẩy `,` (kiểu SRT `00:01:20,500`) thay vì dấu chấm `.` (kiểu WebVTT `00:01:20.500`) trong tệp VTT.
- **Excessive Text Density:** Nhét cả đoạn văn bản 4 dòng dài dằng dặc che kín màn hình video gây cản trở tầm nhìn của người xem.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tệp phụ đề vượt qua kiểm tra cú pháp WebVTT/TTML với 0 lỗi biên dịch.
- **QG-02**: Không có mốc thời gian âm hoặc va chạm thời gian giữa các câu thoại đơn âm.
- **QG-03**: Định danh ngôn ngữ tuân thủ chính xác mã chuẩn quốc tế (ví dụ: `en`, `vi`, `ja`).

## 10. Security & Safety Boundaries
- Lọc sạch các thẻ script nguy hiểm (`<script>`, `onerror=`) chèn trong nội dung phụ đề trước khi render vào DOM (XSS prevention).

## 11. Platform Adapters
- **Runtimes**: WebVTT, pycaption, Subtitle Edit CLI, FFmpeg subtitles filter.

## 12. Deliverables & Output Artifacts
- Tệp phụ đề WebVTT chuẩn hóa (`captions_standard.vtt`).
- Báo cáo lỗi va chạm và cảnh báo khả năng tiếp cận WCAG.

## 13. Related & Complementary Skills
dex-video-transcoding-ladders, dex-streaming-manifest-validation

## 14. Realistic Usage Example
```bash
# Chuyen doi tu phu de SRT sang WebVTT chuan bang ffmpeg
ffmpeg -y -i subtitles.srt -c:s webvtt subtitles.vtt
```
