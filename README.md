# VNExpress News Scraper

## 📌 Mô tả
Dự án tự động thu thập tin tức từ mục **Công nghệ** trên trang [VNExpress.net](https://vnexpress.net/cong-nghe) và lưu vào file CSV. Script sẽ tự động chạy mỗi ngày lúc **6h sáng** để thu thập dữ liệu mới.

---

## 🧩 Yêu cầu cài đặt

1. **Clone repository**
    ```bash
    git clone https://github.com/hvfug/Baitaplon.git
    cd Baitaplon
    ```

2. **Cài đặt các thư viện cần thiết**
    - Sử dụng `pip` để cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirementss.txt
    ```

---

## 🚀 Cách chạy

### Chạy thủ công
Nếu bạn muốn chạy script ngay lập tức mà không đợi đến 6h sáng:
```bash
python vnexpress_scraper.py
