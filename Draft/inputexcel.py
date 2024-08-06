import pandas as pd
import json
import random
import sys

# Đặt mã hóa cho stdout để xử lý ký tự đặc biệt
sys.stdout.reconfigure(encoding='utf-8')

# Dữ liệu cần nhập vào
data = {
    "Ngày": "30/07/2024",
    "Link": "https://www.facebook.com/yenbao",
    "Tiêu đề": "Ngạc nhiên: Nhiều trường học bị đóng cửa vì lý do chưa rõ!",
    "Số lượt thích": 45,
    "Số lượt chia sẻ": 80,
    "Số bình luận": 450,
    "Link bài đăng": "https://www.facebook.com/yenbao/posts/1300000000000000?ref=embed_post",
    "Bình luận": [
        {"comment_id": "c1", "author": "Nguyễn Lan", "content": "@Duy Tân, tin này có đáng tin không? 😠"},
        {"comment_id": "c2", "author": "Duy Tân", "content": "Bài này không có cơ sở! @Bảo Anh cần kiểm tra!"}, 
        {"comment_id": "c3", "author": "Bảo Anh", "content": "Sao tin này lại như vậy? 😠 @Hà Anh cần thông tin chính thức!"}, 
        {"comment_id": "c4", "author": "Hà Anh", "content": "A Di Đà Phật, sao lại có tin này? 😢 @Tú Anh xác minh!"}, 
        {"comment_id": "c5", "author": "Tú Anh", "content": "Bài này làm tôi lo quá! 😭 @Ngọc Trinh cần kiểm tra!"}, 
        {"comment_id": "c6", "author": "Ngọc Trinh", "content": "Chờ thông báo chính thức, đừng tin bài này! @Thúy Hằng!"}, 
        {"comment_id": "c7", "author": "Thúy Hằng", "content": "Tin này không tin được! @Như Quỳnh cần thông tin chính xác!"}, 
        {"comment_id": "c8", "author": "Như Quỳnh", "content": "Bài này có đáng tin không? @Trí Đức cần xác minh!"}, 
        {"comment_id": "c9", "author": "Trí Đức", "content": "Bài này sao lại như vậy? 😡 @Bảo Ngọc kiểm tra!"}, 
        {"comment_id": "c10", "author": "Bảo Ngọc", "content": "Tin giả, đừng tin nhé! @Duy Tân cần thông tin rõ!"}
    ]
}



# Tạo DataFrame từ dữ liệu
df = pd.DataFrame([data])

# Đường dẫn tệp Excel
output_file = "gptfake.xlsx"

# Kiểm tra nếu tệp đã tồn tại và ghi thêm dữ liệu
try:
    existing_df = pd.read_excel(output_file)
    df = pd.concat([existing_df, df], ignore_index=True)
except FileNotFoundError:
    pass

df.to_excel(output_file, index=False)

print(f"Dữ liệu đã được thêm vào tệp {output_file}.")
