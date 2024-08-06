import pandas as pd

# Đường dẫn tới file Excel của bạn
file_path = 'url.xlsx'

# Đọc file Excel
df = pd.read_excel(file_path)

# Giả sử các URL nằm trong cột đầu tiên, bạn có thể thay đổi tên cột tương ứng nếu cần
urls = df.iloc[:, 0].tolist()

# In ra các URL để kiểm tra
for url in urls:
    print(url)