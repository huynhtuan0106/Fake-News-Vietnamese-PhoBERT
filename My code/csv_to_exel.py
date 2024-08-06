import pandas as pd

# Đường dẫn tới file CSV và file XLSX
csv_file_path = 'demofake.csv'
xlsx_file_path = 'bhjbhjhbhkjbhkjg.xlsx'

# Đọc file CSV với encoding đúng
df = pd.read_csv(csv_file_path, encoding='utf-8')  # Bạn có thể thay 'utf-8' bằng encoding khác nếu cần

# Ghi dữ liệu vào file XLSX
df.to_excel(xlsx_file_path, index=False, encoding='utf-8')
