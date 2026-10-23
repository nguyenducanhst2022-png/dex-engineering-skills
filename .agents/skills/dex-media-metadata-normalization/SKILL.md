---
name: dex-media-metadata-normalization
description: Normalize, resolve, and deduplicate multimedia metadata across movies, series, anime, and manga. Handle multilingual titles, romanized naming schemes, and synchronize canonical external IDs.
---

# dex-media-metadata-normalization

## 1. Purpose & Scope
Chuẩn hóa, phân giải và hợp nhất dữ liệu siêu dữ liệu đa phương tiện (Media Metadata Normalization); xử lý các biến thể tiêu đề đa ngôn ngữ (chữ Hán/Kanji, Romaji phiên âm, tên tiếng Anh, tên phát hành tiếng Việt), loại bỏ dữ liệu trùng lặp (Deduplication) và liên kết đồng bộ các mã định danh chuẩn từ các kho dữ liệu quốc tế (TMDB, IMDb, AniList, MyAnimeList, MusicBrainz, Wikidata).

## 2. When to Use
- Khi xây dựng kho danh mục nội dung đa phương tiện tổng hợp (VOD streaming catalog, manga aggregator, digital library).
- Khi nhập khẩu dữ liệu từ nhiều nhà cung cấp khác nhau với các quy ước đặt tên và phân chia mùa/tập (Season/Episode) mâu thuẫn nhau.
- Khi cần ánh xạ thông minh các từ khóa tìm kiếm của người dùng sang thực thể chính tắc (Canonical Media Entity).

## 3. When NOT to Use
- Khi ứng dụng chỉ xử lý các tập tin nhị phân nội bộ mà không cần phân loại hoặc hiển thị thông tin tác phẩm ra người dùng.
- Khi dữ liệu đã được gán nhãn cứng bởi một cơ quan đăng ký duy nhất mà không có nguồn đối sánh bên ngoài.

## 4. Prerequisites & Input Context
- **Cơ sở dữ liệu:** PostgreSQL hỗ trợ extension `pg_trgm` (trigram matching) và `unaccent`.
- **Nguồn dữ liệu tham chiếu:** API Keys cho TMDB, AniList GraphQL, hoặc Wikidata SPARQL endpoint.

## 5. Core Concepts & Taxonomy
- **Fuzzy String Matching (Trigram Similarity):** Thuật toán so khớp chuỗi xấp xỉ giúp nhận diện các tiêu đề có sự sai lệch nhỏ về chính tả, dấu cách hoặc ký tự đặc biệt.
- **External ID Graph:** Bảng quan hệ liên kết một bản ghi nội bộ với nhiều mã khóa định danh bên ngoài (`tmdb_id`, `imdb_id`, `mal_id`, `anilist_id`).
- **Canonical Title Hierarchy:** Thứ tự ưu tiên xác định tên chính: Tên bản địa gốc (Native) -> Tên phiên âm quốc tế (Romaji) -> Tên tiếng Anh chính thức -> Danh sách bí danh (Aliases).

## 6. Step-by-Step Execution Workflow
1. Thu thập chuỗi siêu dữ liệu thô (tên phim, số mùa, số tập, năm phát hành, tên studio/tác giả).
2. Làm sạch chuỗi: loại bỏ thông tin tag kỹ thuật (ví dụ `[1080p]`, `[x265]`, `[Vietsub]`, `Dual Audio`).
3. Truy vấn tìm kiếm trên cơ sở dữ liệu tham chiếu (TMDB/AniList) bằng tiêu đề đã làm sạch và năm phát hành.
4. Đánh giá độ tin cậy của kết quả (Confidence Score): nếu Similarity >= 0.85, tự động gán mã liên kết; nếu từ 0.65 đến 0.84, đưa vào danh sách chờ nhân sự đối soát.
5. Chuẩn hóa cấu trúc đánh số tập và mùa theo định dạng SxxExx tiêu chuẩn.
6. Cập nhật thực thể canonical vào database kèm mốc thời gian kiểm chứng.

## 7. Concrete Examples
### Pipeline Python chuan hoa tieu de truyen/phim va trich xuat mua/tap:
```python
import re
from difflib import SequenceMatcher

def clean_media_title(raw_title):
    # Loai bo cac the nguon [1080p], (Batch), [Vietsub]
    cleaned = re.sub(r'\[.*?\]|\(.*?\)', '', raw_title)
    
    # Trich xuat mua va tap (VD: S02E15 hoac Season 2 Episode 15)
    season_match = re.search(r'(?:S|Season\s*)(\d+)', cleaned, re.IGNORECASE)
    episode_match = re.search(r'(?:E|Episode|Ep\s*)(\d+)', cleaned, re.IGNORECASE)
    
    season = int(season_match.group(1)) if season_match else 1
    episode = int(episode_match.group(1)) if episode_match else 1
    
    # Loai bo phan tap khoi ten chinh
    core_title = re.sub(r'(?:S\d+)?(?:E\d+)|(?:Season\s*\d+)?(?:Episode\s*\d+)', '', cleaned, flags=re.IGNORECASE)
    core_title = " ".join(core_title.split()).strip()
    
    return {"canonical_title": core_title, "season": season, "episode": episode}

def calculate_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

raw = "[SubsPlease] Frieren Beyond Journey's End - S01E28 [1080p] [Vietsub].mkv"
print(clean_media_title(raw))
# Output: {'canonical_title': "Frieren Beyond Journey's End -", 'season': 1, 'episode': 28}
```

## 8. Anti-Patterns & Common Traps
- **Destructive Stripping of Roman Numerals:** Xóa nhầm các ký tự số La Mã (như `II`, `III`) trong tên tác phẩm làm mất phân biệt giữa các phần tiếp theo.
- **Single Source Lock-in:** Chỉ phụ thuộc vào 1 API bên thứ ba (như TMDB); khi API đó đổi policy hoặc sập mạng, toàn bộ pipeline nhập liệu bị đình trệ.
- **Ignoring Unicode Normalization Form:** Không chuẩn hóa chuỗi về dạng NFC trước khi so sánh khiến các ký tự có dấu tổ hợp bị lệch mã hash.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tỷ lệ phân giải chính xác tiêu đề chuẩn (Disambiguation Precision) đạt trên 98% trên tập mẫu kiểm thử.
- **QG-02**: Không có bản ghi trùng lặp nào cùng chia sẻ chung một `tmdb_id` hoặc `imdb_id` trong danh mục chính tắc.
- **QG-03**: Tất cả các chuỗi văn bản lưu trữ đều được chuẩn hóa Unicode NFC.

## 10. Security & Safety Boundaries
- Giới hạn tần suất gọi API bên ngoài (Rate Limiting) và bảo vệ an toàn các API Key của bên cung cấp dịch vụ.

## 11. Platform Adapters
- **Runtimes**: Python, PostgreSQL pg_trgm, AniList GraphQL, TMDB v3 API, MusicBrainz API.

## 12. Deliverables & Output Artifacts
- Module chuẩn hóa chuỗi siêu dữ liệu (`metadata_normalizer.py`).
- Lược đồ CSDL quản lý bảng ánh xạ bí danh (`aliases_mapping_schema.sql`).

## 13. Related & Complementary Skills
dex-database-engineering, dex-media-content-ingest-moderation

## 14. Realistic Usage Example
```bash
# Chay test chuan hoa metadata tren bo test case mau
pytest tests/test_metadata_normalization.py -v
```
