import time
import pickle
import sys
import io
import json
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cấu hình các tùy chọn cho Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
# chrome_options.add_argument("--headless")

# Khởi tạo dịch vụ với ChromeDriver
service = Service(ChromeDriverManager().install())

# Khởi tạo trình duyệt Chrome với dịch vụ và các tùy chọn đã cấu hình
browser = webdriver.Chrome(service=service, options=chrome_options)


# Điều hướng đến trang đăng nhập của Facebook
browser.get("https://www.facebook.com")
time.sleep(10)

# Load cookie từ file
cookies = pickle.load(open("Crawl_code/my_cookie_2.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

# Refresh trình duyệt
browser.get("https://www.facebook.com")


# Hàm cuộn trang
def scroll_page(browser, num_scrolls):
    for _ in range(num_scrolls):
        # Cuộn xuống cuối trang
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # Đợi một chút để trang tải xong


def crawl_comment(link):
    # Mở bài post
    browser.get(link)
    time.sleep(5)

    # Click vào bình luận
    try:
        show_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[2]/div[2]/div')
        browser.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", show_button)
        time.sleep(3)
        show_button.click()
        time.sleep(3)

        # Click vào "Xem tất cả bình luận"
        all_button = WebDriverWait(browser, 4).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[3]/div[1]'))
        )
        time.sleep(2)
        all_button.click()
        time.sleep(4)
    except:
        pass

    # Cuộn trang để hiển thị bình luận
    scroll_page(browser, 10)

    # Lấy các bình luận
    div_cmt = browser.find_elements(By.XPATH, '//div[contains(@aria-label, "Bình luận")]')

    # Danh sách chứa các bình luận
    comments = []

    for i, cmt in enumerate(div_cmt):
        try:
            poster = cmt.find_element(By.CSS_SELECTOR, '.x3nfvp2').text if cmt.find_element(By.CSS_SELECTOR, '.x3nfvp2') else "Clone"
            content = cmt.find_element(By.CSS_SELECTOR, ".xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs").text

            if content.strip():  # Chỉ thêm bình luận nếu có nội dung
                comments.append(content)
        except Exception:
            pass

    # Tạo DataFrame từ danh sách các bình luận và lưu vào file Excel
    df = pd.DataFrame({"Comment": comments})
    df.to_excel("cmt2.xlsx", index=False)

# Ví dụ sử dụng hàm
crawl_comment("https://www.facebook.com/LangOfficial.vn/posts/pfbid028j7CuANMRpwfe87GXMTjyaKbTiBnHLS7S3TQi6XpJZHTMn5ksHvRpyNzbiDRkC44l?rdid=Zrzgn0mtoYOh8NZQ#")



browser.quit()
