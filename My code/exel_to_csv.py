import pandas as pd
import sys

# Đường dẫn tới file Excel gốc
excel_file_path = 'tonghop.xlsx'

# Đường dẫn tới file CSV mới sẽ lưu
csv_file_path = 'tonghop.csv'

# Đọc file Excel
df = pd.read_excel(excel_file_path)

# Lưu lại file CSV
df.to_csv(csv_file_path, index=False, encoding='utf-8')

# Thiết lập stdout để sử dụng encoding utf-8
sys.stdout.reconfigure(encoding='utf-8')

print(f"File đã được chuyển đổi và lưu lại với định dạng CSV tại: {csv_file_path}")
