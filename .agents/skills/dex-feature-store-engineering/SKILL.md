---
name: dex-feature-store-engineering
description: Architect enterprise feature stores (Feast, Hopsworks) with dual online/offline storage synchronization, point-in-time correct join queries, feature definitions as code, and latency SLA guarantees. Use when scaling machine learning models across recommendation, fraud, and prediction systems.
---

# dex-feature-store-engineering

## 1. Purpose & Scope
Thiết kế kiến trúc kho lưu trữ đặc trưng học máy (Feature Store) chuẩn doanh nghiệp sử dụng Feast hoặc Hopsworks; đồng bộ hóa dữ liệu giữa hai tầng lưu trữ trực tuyến (Online Store có độ trễ mili-giây) và ngoại tuyến (Offline Store phục vụ huấn luyện mô hình theo lô); đảm bảo tính chính xác theo thời điểm lịch sử (Point-in-Time Correctness / As-Of Joins) và quản lý đặc trưng dưới dạng mã nguồn (Features as Code).

## 2. When to Use
- Khi các mô hình học máy (Gợi ý sản phẩm, phát hiện gian lận) bị lỗi rò rỉ dữ liệu tương lai (Data Leakage) trong quá trình huấn luyện.
- Khi các kỹ sư AI phải viết lại các câu lệnh tính toán đặc trưng phức tạp lặp đi lặp lại giữa môi trường train và môi trường serve (Train/Serve Skew).
- Khi cần phục vụ các đặc trưng người dùng trong thời gian thực (<10ms) cho các mô hình suy luận trực tiếp.

## 3. When NOT to Use
- Khi tổ chức chỉ có một mô hình học máy duy nhất chạy báo cáo định kỳ mỗi tháng.
- Khi lưu trữ các bảng dữ liệu quan hệ nghiệp vụ thông thường không phục vụ huấn luyện AI.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kho dữ liệu ngoại tuyến (BigQuery, Snowflake hoặc Parquet trên S3), kho dữ liệu trực tuyến độ trễ thấp (Redis hoặc DynamoDB), công cụ Feast SDK.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Point-in-Time Correctness:** Khi huấn luyện mô hình với sự kiện xảy ra ngày 1/1, chỉ được lấy các đặc trưng của người dùng tại đúng thời điểm ngày 1/1, không được lấy số liệu của ngày hôm nay.
- **Train/Serve Skew Elimination:** Định nghĩa logic tính toán đặc trưng một lần duy nhất, đảm bảo giá trị đưa vào mô hình lúc chạy thật khớp hoàn toàn với lúc học.
- **Dual-Storage Architecture:** Offline Store (Parquet/SQL) tối ưu cho việc đọc hàng triệu bản ghi, Online Store (Redis) tối ưu cho việc tra cứu theo khóa đơn lẻ (Key-value lookup).

## 6. Step-by-Step Execution Workflow
1. Định nghĩa thực thể (`Entity`) và các tập đặc trưng (`FeatureView`) bằng mã nguồn Python.
2. Thực thi lệnh `feast apply` để đồng bộ cấu hình vào sổ cái lưu trữ lược đồ đặc trưng.
3. Xây dựng đường ống đồng bộ định kỳ (`feast materialize`) đẩy các đặc trưng mới nhất từ kho offline sang Redis.
4. Sử dụng hàm `get_historical_features` để thực hiện phép nối thời gian chính xác (As-Of Join) cho tập huấn luyện.
5. Gọi hàm `get_online_features` từ dịch vụ API suy luận với thời gian phản hồi dưới 10ms.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Feast Feature View Definition as Code
from datetime import timedelta
from feast import Entity, Field, FeatureView, FileSource
from feast.types import Float32, Int64

user_entity = Entity(name="user_id", join_keys=["user_id"])

user_stats_view = FeatureView(
    name="user_transaction_stats",
    entities=[user_entity],
    ttl=timedelta(days=30),
    schema=[
        Field(name="avg_daily_spend_30d", dtype=Float32),
        Field(name="failed_logins_24h", dtype=Int64),
    ],
    online=True,
    source=FileSource(
        path="data/user_stats.parquet",
        timestamp_field="event_timestamp",
        created_timestamp_column="created_timestamp"
    )
)
```

## 8. Anti-Patterns & Common Traps
- Nối dữ liệu huấn luyện bằng lệnh SQL `LEFT JOIN` thông thường trên khóa chính mà không có điều kiện thời gian, dẫn đến mô hình 'nhìn thấy trước tương lai' và đạt điểm cao giả tạo lúc train.
- Tính toán đặc trưng ở tầng frontend rồi truyền vào API suy luận, khiến hacker có thể sửa đổi đặc trưng để qua mặt mô hình.
- Để dữ liệu trong Online Store bị lỗi thời do quên lập lịch tiến trình `materialize`.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Độ trễ tra cứu đặc trưng trực tuyến qua Redis duy trì P99 dưới 10ms dưới tải 1,000 req/s.
- QG-02: 100% các tập dữ liệu huấn luyện được tạo ra tuân thủ nghiêm ngặt tính đúng đắn theo thời điểm (Point-in-time correctness).
- QG-03: Không có sự trôi lệch giá trị (Zero Drift) giữa đặc trưng lúc huấn luyện và lúc suy luận thực tế.

## 10. Security & Safety Boundaries
- Áp dụng phân quyền truy cập đặc trưng theo vai trò; mã hóa dữ liệu nhạy cảm lưu trữ trong Redis cache.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Kho mã nguồn định nghĩa đặc trưng `feature_definitions.py`.
1. Quy trình tự động hóa nạp và đồng bộ đặc trưng `feast-sync-pipeline.yml`.

## 13. Related & Complementary Skills
- [`dex-machine-learning-data-drift`](.agents/skills/dex-machine-learning-data-drift/SKILL.md)
- [`dex-data-pipelines`](.agents/skills/dex-data-pipelines/SKILL.md)
- [`dex-data-pipelines`](.agents/skills/dex-data-pipelines/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Mô hình gợi ý sản phẩm thương mại điện tử đạt độ chính xác 95% trong phòng thí nghiệm nhưng khi đưa lên production thì doanh số không tăng. Kỹ sư kích hoạt `dex-feature-store-engineering`, phát hiện việc nối dữ liệu cũ bị rò rỉ dữ liệu mua hàng tương lai. Tái cấu trúc bằng Feast với Point-in-time join và Redis online store, giúp mô hình phản ánh năng lực thực tế và tăng 18% tỷ lệ chuyển đổi thật.
