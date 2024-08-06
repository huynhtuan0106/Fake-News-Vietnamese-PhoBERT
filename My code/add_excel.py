import pandas as pd

# Đường dẫn tới file Excel gốc
excel_file_path = 'test.xlsx'

# Đọc file Excel
df = pd.read_excel(excel_file_path)

# Dữ liệu mới muốn thêm vào (dạng từ điển), bỏ trống một số cột
new_data = {
    'like': 1,
    'shares_count': 1,
    'comments_count': 1,
    'comment_list': 1,
    'link': 1,
    # Thêm các cột khác nếu có
}

# Chuyển dữ liệu mới thành DataFrame
new_row = pd.DataFrame([new_data])

# Thêm dữ liệu mới vào DataFrame hiện tại
df = pd.concat([df, new_row], ignore_index=True)

# Lưu lại file Excel với dữ liệu đã thêm
df.to_excel(excel_file_path, index=False, engine='openpyxl')

# Sử dụng mã hóa hệ thống để in
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print(f"Đã thêm dữ liệu vào file Excel tại: {excel_file_path}")
