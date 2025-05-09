import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
import concurrent.futures

# Bước 1: Định nghĩa URL gốc của chuyên mục
BASE_URL = 'https://vnexpress.net/khoa-hoc-cong-nghe-p'

# Bước 2: Hàm lấy chi tiết nội dung bài viết
def get_article_details(article_url):
    try:
        res = requests.get(article_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.content, 'html.parser')

        content_div = soup.find('div', class_='fck_detail')
        if content_div:
            paragraphs = content_div.find_all('p')
            content = '\n'.join(p.get_text(strip=True) for p in paragraphs)
            return content
        return ''
    except Exception as e:
        print(f"Lỗi khi lấy chi tiết bài viết: {e}")
        return ''

# Bước 3: Hàm lấy tất cả các trang với tối ưu hiệu suất
def get_all_pages():
    articles = []
    page = 1

    while True:
        url = f'{BASE_URL}{page}'
        print(f'Đang lấy dữ liệu từ trang: {url}')
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.content, 'html.parser')

            items = soup.find_all('article', class_='item-news')
            if not items:
                break

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(get_article_details, item.find('a')['href']) for item in items if item.find('a')]
                contents = [future.result() for future in concurrent.futures.as_completed(futures)]

            for item, content in zip(items, contents):
                title_tag = item.find('h3', class_='title-news')
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']
                description_tag = item.find('p', class_='description')
                description = description_tag.get_text(strip=True) if description_tag else ''
                img_tag = item.find('img')
                img_url = img_tag.get('data-src', '') if img_tag else ''

                articles.append({
                    'Tiêu đề': title,
                    'Mô tả': description,
                    'Hình ảnh': img_url,
                    'Nội dung': content,
                    'Link bài viết': link
                })

        except Exception as e:
            print(f'Lỗi xử lý trang {page}: {e}')

        page += 1

    return articles

# Bước 4: Lưu dữ liệu vào file CSV
def save_to_csv(articles):
    df = pd.DataFrame(articles)
    df.to_csv('vnexpress_congnghe.csv', index=False, encoding='utf-8-sig')
    print('✅ Đã lưu dữ liệu vào vnexpress_congnghe.csv')

# Bước 5: Định nghĩa lịch chạy tự động hàng ngày
schedule.every().day.at("14:32").do(lambda: save_to_csv(get_all_pages()))

print("⏰ Đang chờ đến 06:00 mỗi ngày để chạy scraper...")

while True:
    schedule.run_pending()
    time.sleep(60)
