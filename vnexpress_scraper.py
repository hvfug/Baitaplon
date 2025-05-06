import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time

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

def scrape_vnexpress_congnghe(pages=5):
    base_url = 'https://vnexpress.net/cong-nghe-p'
    articles = []

    for page in range(1, pages + 1):
        url = base_url + str(page)
        print(f'Đang lấy dữ liệu từ trang: {url}')
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.content, 'html.parser')

        items = soup.find_all('article', class_='item-news')
        for item in items:
            try:
                title_tag = item.find('h3', class_='title-news')
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']
                description_tag = item.find('p', class_='description')
                description = description_tag.get_text(strip=True) if description_tag else ''
                img_tag = item.find('img')
                img_url = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else (img_tag['src'] if img_tag else '')

                content = get_article_details(link)

                articles.append({
                    'Tiêu đề': title,
                    'Mô tả': description,
                    'Hình ảnh': img_url,
                    'Nội dung': content,
                    'Link bài viết': link
                })

                time.sleep(1)

            except Exception as e:
                print(f'Lỗi xử lý bài viết: {e}')
                continue

    df = pd.DataFrame(articles)
    df.to_csv('vnexpress_congnghe.csv', index=False, encoding='utf-8-sig')
    print('✅ Đã lưu dữ liệu vào vnexpress_congnghe.csv')

# Lên lịch chạy tự động mỗi ngày lúc 6h sáng
schedule.every().day.at("14:31").do(scrape_vnexpress_congnghe, pages=5)

print("⏰ Đang chờ đến 6h sáng mỗi ngày để chạy scraper...")

while True:
    schedule.run_pending()
    time.sleep(60)
