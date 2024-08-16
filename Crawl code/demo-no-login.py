import time
import pickle
import os
import json
import sys
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Cấu hình các tùy chọn cho Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
# Nếu bạn muốn xem giao diện của trình duyệt, hãy loại bỏ dòng sau
# chrome_options.add_argument("--headless")

# Khởi tạo dịch vụ với ChromeDriver
service = Service(ChromeDriverManager().install())

# Khởi tạo trình duyệt Chrome với dịch vụ và các tùy chọn đã cấu hình
browser = webdriver.Chrome(service=service, options=chrome_options)

# Điều hướng đến trang đăng nhập của Facebook
browser.get("https://www.facebook.com")

# Load cookie từ file
cookies = pickle.load(open("my demo/my_cookie.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

# Refresh trình duyệt
browser.get("https://www.facebook.com")

# Truy cập vào trang fanpage K14vn
fanpage_url = "https://www.facebook.com/K14vn"
browser.get(fanpage_url)
time.sleep(5)  # Đợi một chút để trang tải xong

# Hàm cuộn trang
def scroll_page(browser, num_scrolls):
    for _ in range(num_scrolls):
        # Cuộn xuống cuối trang
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Đợi một chút để trang tải xong

# Cuộn trang 5 lần để tải thêm các bài viết
scroll_page(browser, 5)

# Thu thập dữ liệu từ các bài viết
posts = browser.find_elements(By.XPATH, "//div[@data-pagelet='MainFeed']//div[@role='article']")
print(f"Found {len(posts)} posts")  # In ra số lượng bài viết tìm thấy

data = []

for post in posts:
    try:
        # Thu thập tiêu đề bài viết
        title_element = post.find_element(By.XPATH, ".//h2")
        title = title_element.text if title_element else "No title"
        
        # Thu thập nội dung bài viết
        content_element = post.find_element(By.XPATH, ".//div[@data-ad-preview='message']")
        content = content_element.text if content_element else "No content"
        
        # Thu thập số lượt thích
        likes_element = post.find_element(By.XPATH, ".//span[contains(text(), 'likes')]")
        likes = likes_element.text if likes_element else "0 likes"
        
        # Thu thập số lượt chia sẻ
        shares_element = post.find_element(By.XPATH, ".//span[contains(text(), 'shares')]")
        shares = shares_element.text if shares_element else "0 shares"
        
        # Thu thập số lượt bình luận
        comments_element = post.find_element(By.XPATH, ".//span[contains(text(), 'comments')]")
        comments = comments_element.text if comments_element else "0 comments"
        
        # Thêm dữ liệu vào danh sách
        data.append({
            "title": title,
            "content": content,
            "likes": likes,
            "shares": shares,
            "comments": comments
        })
        # In ra thông tin bài viết để kiểm tra
        print(f"Post collected: Title: {title}, Content: {content}, Likes: {likes}, Shares: {shares}, Comments: {comments}")
    except Exception as e:
        print("Error:", e)

# Đóng trình duyệt
browser.quit()

# Lưu dữ liệu vào file (ví dụ JSON)
output_file = "k14vn_posts.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Thiết lập lại đầu ra tiêu chuẩn để sử dụng mã hóa UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# In ra kích thước và nội dung file
file_size = os.path.getsize(output_file)
print(f"Kích thước file: {file_size} bytes")

with open(output_file, "r", encoding="utf-8") as f:
    content = json.load(f)
    print("Nội dung file:")
    print(json.dumps(content, ensure_ascii=False, indent=4))

print("Done")
