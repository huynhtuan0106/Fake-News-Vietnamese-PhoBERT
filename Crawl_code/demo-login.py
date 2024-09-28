import time
import pickle
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

# Chờ trang tải xong
time.sleep(5)  # Đợi 5 giây để trang tải xong

try:
    # Nhập tên đăng nhập
    username_field = browser.find_element(By.ID, "email")
    username_field.send_keys("0816162611")  
    
    # Nhập mật khẩu
    password_field = browser.find_element(By.ID, "pass")
    password_field.send_keys("HTuan0848122611.")  

    # Nhấn nút đăng nhập
    login_button = browser.find_element(By.NAME, "login")
    login_button.click()

    # Chờ một chút để đảm bảo việc đăng nhập hoàn tất
    time.sleep(20)  # Đợi 10 giây

    pickle.dump(browser.get_cookies(), open("my_cookie.pkl","wb"))

finally:
    # Đóng trình duyệt sau khi hoàn thành
    browser.close()
