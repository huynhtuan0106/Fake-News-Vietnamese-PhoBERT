import time
import pickle
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

# Mở bài post
browser.get("https://www.facebook.com/K14vn/posts/898637162297284?ref=embed_post")
time.sleep(10)

# Hàm cuộn trang
def scroll_page(browser, num_scrolls):
    for _ in range(num_scrolls):
        # Cuộn xuống cuối trang
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # Đợi một chút để trang tải xong

# Cuộn trang xuống để phần tử nằm trong khung nhìn
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Click vào bình luận
show_button = WebDriverWait(browser, 20).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[2]/div[2]/div'))
)
# Cuộn đến phần tử để đảm bảo nó nằm trong khung nhìn của trang
browser.execute_script("arguments[0].scrollIntoView();", show_button)
time.sleep(5) 
show_button.click()
time.sleep(5)

# Click vào "Xem tất cả bình luận"
all_button = WebDriverWait(browser, 20).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[3]/div[1]'))
)
time.sleep(5)
all_button.click()
time.sleep(15)

# Cuộn trang để hiển thị bình luận
scroll_page(browser,2)

# Lấy các bình luận
div_cmt = browser.find_elements(By.XPATH,'//div[contains(@aria-label, "Bình luận")]')
print(len(div_cmt))

for i, cmt in enumerate(div_cmt):
    try:
        poster = cmt.find_element(By.CSS_SELECTOR, '.x3nfvp2')
        content = cmt.find_element(By.CSS_SELECTOR, ".xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs")
        print(f'Poster {i+1}: {poster.text}')
        print(f'Content {i+1}: {content.text}')
    except Exception as e:
        print(f'Poster {i+1}: Clone')
        print(f'Content {i+1}: Lỗi')
    
browser.quit()


