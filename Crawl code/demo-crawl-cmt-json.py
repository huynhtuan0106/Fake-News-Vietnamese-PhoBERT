import time
import pickle
import sys
import io
import json
import re
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
# Nếu bạn muốn xem giao diện của trình duyệt, hãy loại bỏ dòng sau
# chrome_options.add_argument("--headless")

# Khởi tạo dịch vụ với ChromeDriver
service = Service(ChromeDriverManager().install())

# Khởi tạo trình duyệt Chrome với dịch vụ và các tùy chọn đã cấu hình
browser = webdriver.Chrome(service=service, options=chrome_options)


# Điều hướng đến trang đăng nhập của Facebook
browser.get("https://www.facebook.com")

# Load cookie từ file
cookies = pickle.load(open("Crawl code/my_cookie.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

# Refresh trình duyệt
browser.get("https://www.facebook.com")


# Hàm cuộn trang
def scroll_page(browser, num_scrolls):
    for _ in range(num_scrolls):
        # Cuộn xuống cuối trang
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)  # Đợi một chút để trang tải xong


def change_date(original_datetime_str):
    # Tách phần ngày giờ từ chuỗi ban đầu
    date_str = original_datetime_str.split("lúc")[0].strip()
    time_str = original_datetime_str.split("lúc")[1].strip()

    # Chuyển đổi các từ tiếng Việt sang dạng số và loại bỏ từ không cần thiết
    date_str = date_str.replace("Thứ Ba, ", "")\
                    .replace("Thứ Hai, ", "")\
                    .replace("Thứ Tư, ", "")\
                    .replace("Thứ Năm, ", "")\
                    .replace("Thứ Sáu, ", "")\
                    .replace("Thứ Bảy, ", "")\
                    .replace("Chủ Nhật, ", "")\
                    .replace("Tháng 1", "01")\
                    .replace("Tháng 2", "02")\
                    .replace("Tháng 3", "03")\
                    .replace("Tháng 4", "04")\
                    .replace("Tháng 5", "05")\
                    .replace("Tháng 6", "06")\
                    .replace("Tháng 7", "07")\
                    .replace("Tháng 8", "08")\
                    .replace("Tháng 9", "09")\
                    .replace("Tháng 10", "10")\
                    .replace("Tháng 11", "11")\
                    .replace("Tháng 12", "12")

    # Loại bỏ dấu phẩy thừa
    date_str = date_str.replace(",", "")

    # Chuyển đổi chuỗi thành đối tượng datetime
    date_time_obj = datetime.strptime(date_str, "%d %m %Y")

    # Kết hợp ngày và giờ thành định dạng mới
    new_datetime_str = date_time_obj.strftime("%d/%m/%Y") + " " + time_str

    return new_datetime_str


def crawl_comment(link): 
    # Mở bài post
    browser.get(link)
    time.sleep(5)

    # Like
    #like_count = WebDriverWait(browser, 7).until(
    #    EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span'))
    #)
    #browser.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", like_count)

    # Sử dụng biểu thức chính quy để tìm số
    #match = re.search(r'\d+', like_count.text)

    # Nếu tìm thấy số, in số đó
    #if match:
    #    number = match.group()
        #print("Lượt like: ", number) 

    # Click vào bình luận
    try:
        show_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[2]/div[2]/div')

        # Cuộn đến phần tử để đảm bảo nó nằm trong khung nhìn của trang
        browser.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", show_button)
        time.sleep(3) 
        show_button.click()
        time.sleep(3)

        # Click vào "Xem tất cả bình luận"
        all_button = WebDriverWait(browser, 4).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[3]/div[1]'))
        )
        time.sleep(2)
        all_button.click()
        time.sleep(4)
    except:
        pass

    # Share
    #try:    
    #    share = WebDriverWait(browser, 4).until(
    #        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[3]/span/div/div/div[1]/span'))
    #    )

        #print("Lượt chia sẻ: ", share.text)

    #    share_count = share.text
    #except: 
        #share_count = 0


    # Cuộn trang để hiển thị bình luận
    scroll_page(browser,10)

    # Lấy các bình luận
    div_cmt = browser.find_elements(By.XPATH,'//div[contains(@aria-label, "Bình luận")]')
    #print(f'Tổng số bình luận: {len(div_cmt)}')

    # Danh sách chứa các bình luận
    comments = []

    for i, cmt in enumerate(div_cmt):
        try:
            try:
                poster = cmt.find_element(By.CSS_SELECTOR, '.x3nfvp2').text
            except Exception:
                poster = "Clone"
            
            content = cmt.find_element(By.CSS_SELECTOR, ".xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs").text
            
            if content.strip():  # Chỉ thêm bình luận nếu có nội dung
                comment = {
                    "comment_id": f"c{i+1}",
                    "author": poster,
                    "content": content
                }
                comments.append(comment)
        except Exception as e:
            pass  # Bỏ qua bình luận bị lỗi nội dung

    # Lưu vào tệp JSON
    with open("comment.json", "w", encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)

    # Cuộn lên đầu trang
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)  # Đợi một chút để thấy hiệu ứng cuộn

    # Lấy content bài đăng
    try:
        content = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]/div[1]/div/div'))
        )
        #print (content.text)
        content_ne = content.text
    except:
        content_ne = "None"


    try: 
        # Tìm đối tượng cần di chuyển chuột tới
        element_to_hover_over = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[2]/div/div[2]/span/div/span[1]/span/a/span')

        # Tạo đối tượng ActionChains
        actions = ActionChains(browser)

        # Di chuyển chuột đến đối tượng
        actions.move_to_element(element_to_hover_over).perform()

        # Đợi một chút để đối tượng hiển thị
        time.sleep(3)  # Có thể điều chỉnh thời gian chờ này

        # Lấy ngày đăng
        ngay = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/span'))
        )
        
        ngaydang = change_date(ngay.text)
    
    except:
        ngaydang = "None"

    try:
        # Lấy ID người đăng
        poster = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[2]/div/div[1]/span/h2/span[1]/a/strong/span'))
        )
        poster.click()
        time.sleep(5)
        current_url = browser.current_url
        #print(f"URL hiện tại: {current_url}")
    except:
        current_url = "None"

    # Đường dẫn tới file Excel gốc
    excel_file_path = 'Data/Draft/ketqua.xlsx'

    # Đọc file Excel
    df = pd.read_excel(excel_file_path)

    comments_str = json.dumps(comments, ensure_ascii=False, indent=4)

    # Dữ liệu mới muốn thêm vào (dạng từ điển), bỏ trống một số cột
    new_data = {
        'content': content_ne,
        'author_id': current_url,
        #'like': number,
        #'shares_count': share_count,
        #'comments_count': len(div_cmt),
        'comment_list': comments_str,
        'link': link,
        'date' : ngaydang,
        'label': 0,
        # Thêm các cột khác nếu có
    }


    # Chuyển dữ liệu mới thành DataFrame
    new_row = pd.DataFrame([new_data])

    # Thêm dữ liệu mới vào DataFrame hiện tại
    df = pd.concat([df, new_row], ignore_index=True)

    # Lưu lại file Excel với dữ liệu đã thêm
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

    print(f"Đã thêm dữ liệu vào file Excel tại: {excel_file_path}")


# Đường dẫn tới file Excel của bạn
file_path = 'Data/Draft/url.xlsx'

# Đọc file Excel
df = pd.read_excel(file_path)

# Giả sử các URL nằm trong cột đầu tiên, bạn có thể thay đổi tên cột tương ứng nếu cần
urls = df.iloc[:, 0].tolist()

# In ra các URL để kiểm tra
for url in urls:
    print(url)
    crawl_comment(url)

#crawl_comment("https://www.facebook.com/vietnamnet.vn/posts/514422874302211?ref=embed_post")
#crawl_comment("https://www.facebook.com/vietnamnet.vn/posts/513946274349871?ref=embed_post")
#crawl_comment("https://www.facebook.com/vietnamnet.vn/posts/514325794311919?ref=embed_post")
#crawl_comment("https://www.facebook.com/vietnamnet.vn/posts/514358750975290?ref=embed_post")
#crawl_comment("https://www.facebook.com/vietnamnet.vn/posts/514399610971204?ref=embed_post")

browser.quit()


# Đọc nội dung JSON từ tệp và lưu vào CSV
#with open("comment.json", "r", encoding='utf-8') as f:
    #comments = json.load(f)

# Sử dụng pandas để chuyển đổi JSON thành DataFrame và lưu vào CSV
#df = pd.DataFrame(comments)
#df.to_csv("comments.csv", index=False, encoding='utf-8-sig')