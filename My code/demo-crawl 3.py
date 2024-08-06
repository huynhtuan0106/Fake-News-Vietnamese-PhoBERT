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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
        time.sleep(30)  # Đợi một chút để trang tải xong

# Thu thập dữ liệu từ các bài viết
def collect_posts(browser, target_count):
    collected_posts = []
    scroll_attempts = 0
    while len(collected_posts) < target_count:
        # Cuộn trang và tải thêm bài viết nếu cần
        scroll_page(browser, 1)
        posts = browser.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')
        
        for post in posts:
            if len(collected_posts) >= target_count:
                break

            try:
                # Kiểm tra và click vào phần tử "xem thêm"
                try:
                    more_elements = post.find_elements(By.XPATH, './/span[contains(text(),"Xem thêm")]')
                    for more_element in more_elements:
                        # Cuộn đến phần tử nếu cần thiết
                        browser.execute_script("arguments[0].scrollIntoView(true);", more_element)
                        time.sleep(1)  # Đợi phần tử hiển thị
                        more_element.click()
                        print("Clicked 'Xem thêm'")
                        time.sleep(3)  # Đợi nội dung thêm được tải
                        break
                except Exception as e:
                    print("Error clicking 'Xem thêm':", str(e).encode('utf-8', errors='replace').decode('utf-8'))

                # Thu thập nội dung bài viết từ CSS selector của nội dung
                content_elements = post.find_elements(By.CSS_SELECTOR, '.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h')
                contents = [element.text for element in content_elements]
                content = " ".join(contents) if contents else "No content"
                
                collected_posts.append({
                    "content": content,
                })
                
                # In ra thông tin bài viết để kiểm tra
                print(f"Post collected: Content: {content}")

            except Exception as e:
                print("Error:", str(e).encode('utf-8', errors='replace').decode('utf-8'))

        scroll_attempts += 1
        if scroll_attempts > 10:  # Cảnh báo nếu không tìm thấy thêm bài viết
            print("Warning: Too many scroll attempts, might be missing posts.")
            break

    return collected_posts

# Lấy 20 bài viết
target_count = 20
posts_data = collect_posts(browser, target_count)

# Đóng trình duyệt
browser.quit()

# Lưu dữ liệu vào file (ví dụ JSON)
output_file = "k14vn_posts.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=4)

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



