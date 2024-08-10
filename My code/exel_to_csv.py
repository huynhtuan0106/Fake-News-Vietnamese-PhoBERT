import pandas as pd
import sys

# Đường dẫn tới file Excel gốc
excel_file_path = 'Data/real.xlsx'

# Đường dẫn tới file CSV mới sẽ lưu
csv_file_path = 'Data/real.csv'

# Đọc file Excel
try:
    df = pd.read_excel(excel_file_path)
except Exception as e:
    print(f"Không thể đọc file Excel: {e}")
    sys.exit(1)

# Lưu lại file CSV với encoding UTF-8 để hỗ trợ tiếng Việt
try:
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
except Exception as e:
    print(f"Không thể lưu file CSV: {e}")
    sys.exit(1)

# Thiết lập stdout để sử dụng encoding utf-8
sys.stdout.reconfigure(encoding='utf-8')

print(f"File đã được chuyển đổi và lưu lại với định dạng CSV tại: {csv_file_path}")
