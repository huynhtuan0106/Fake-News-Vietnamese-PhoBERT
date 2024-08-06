import pandas as pd
import sys

# Đường dẫn tới file CSV gốc
csv_file_path = 'demofake.csv'

# Đường dẫn tới file Excel mới sẽ lưu
excel_file_path = 'GBHK.xlsx'

# Thử các encoding khác
try:
    df = pd.read_csv(csv_file_path, encoding='utf-16')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(csv_file_path, encoding='cp1252')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, encoding='cp1252')

# Lưu lại file Excel
df.to_excel(excel_file_path, index=False, engine='openpyxl')

# Thiết lập stdout để sử dụng encoding utf-8
sys.stdout.reconfigure(encoding='utf-8')

print(f"File đã được chuyển đổi và lưu lại với định dạng Excel tại: {excel_file_path}")
