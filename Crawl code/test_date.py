from datetime import datetime


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

