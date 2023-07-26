from Database.db import Db_get_locks, Db_set_lock_password, Db_update_lock_password, Db_delete_lock_password
from Models.models import Lock
from Tuya.tuya import tuya_set_lock_password
from Tuya.tuya import tuya_update_lock_password
from Tuya.tuya import tuya_delete_lock_password
from Tuya.tuya import tuya_get_lock_history
from Tuya.tuya import tuya_get_lock_status
from Tuya.tuya import tuya_set_lock_OTP
from Tuya.tuya import tuya_get_password_status

# Hàm lấy danh sách các khóa cửa từ cơ sở dữ liệu
def Ctrl_get_locks():
    return Db_get_locks()


# Hàm đặt mật khẩu cho khóa cửa    
def Ctrl_set_lock_password(device_id, Name, password, effective_time, invalid_time):
    # Gọi API của Tuya để đặt mật khẩu cho khóa cửa
    response = tuya_set_lock_password(device_id, Name, password, effective_time, invalid_time)
    if response['success']:
        # Thêm khóa cửa mới vào cơ sở dữ liệu
        Db_set_lock_password(device_id, Name, password, effective_time, invalid_time, password_id=response["result"])
        return f'Đặt mật khẩu thành công cho khóa cửa {device_id} : {response["result"]}'
    else:
        return f'Đặt mật khẩu thất bại cho khóa cửa {device_id}: {response["msg"]}'


# Hàm thay đổi mật khẩu cho một khóa cửa
def Ctrl_update_lock_password(device_id, password_id, password, effective_time, invalid_time):  
    # Gọi API của Tuya để đặt mật khẩu mới
    response = tuya_update_lock_password(device_id, password_id, password, effective_time, invalid_time)
    if response['success']:
        # Cập nhật thông tin mật khẩu mới vào cơ sở dữ liệu
        Db_update_lock_password(device_id, password_id, password, effective_time, invalid_time)
        return f'Đổi mật khẩu thành công cho khóa cửa {device_id} : {response["result"]}'
    else:
        return f'Đổi mật khẩu thất bại cho khóa cửa {device_id}: {response["msg"]}'


# Hàm xóa mật khẩu tạm thời cho khóa cửa
def Ctrl_delete_lock_password(device_id, password_id):
    # Gọi API của Tuya để xóa mật khẩu tạm thời
    response = tuya_delete_lock_password(device_id, password_id)
    if response['success']:
        # Xóa thông tin mật khẩu khỏi cơ sở dữ liệu
        Db_delete_lock_password(device_id, password_id)
        return f'Xóa mật khẩu thành công cho khóa cửa {device_id} : {response["result"]}'
    else:
        return f'Xóa mật khẩu thất bại cho khóa cửa {device_id}: {response["msg"]}'


# Hàm lấy nhật ký hoạt động của khóa cửa
def Ctrl_get_lock_history(device_id, page_no, page_size, start_time, end_time):
    # Gọi API của Tuya để lấy lịch sử
    response = tuya_get_lock_history(device_id, page_no, page_size, start_time, end_time)
    if response['success']:
        return f'{response["result"]}'
    else:
        return f'Không lấy được nhật ký hoạt động của khóa cửa {device_id} : {response["msg"]}'
    

# Hàm lấy trạng thái của khóa cửa
def Ctrl_get_lock_status(device_id):
    # Gọi API của Tuya để lấy trạng thái
    response = tuya_get_lock_status(device_id)
    if response['success']:
        # Duyệt qua danh sách các code trong trường status
        for code in response["result"]["status"]:
            # Kiểm tra xem code có phải là battery_state hay không
            if code["code"] == "battery_state":
                # Trả về giá trị của code battery_state
                return f'{code["value"]}'
    else:
        return f'Không lấy được trạng thái pin của khóa cửa {device_id} : {response["msg"]}'


# Hàm tạo mật khẩu OTP cho khóa cửa
def Ctrl_set_lock_OTP(device_id):
    # Gọi API của tuya
    response = tuya_set_lock_OTP(device_id)
    if response['success']:
        # Trả về mật khẩu OTP
        # return response['password']
        return f'{response["result"]}, {response["password"]}'
    else:
        return f'Lấy OTP không thành công cho khóa {device_id} : {response["msg"]}'
    

# Hàm lấy trạng thái password tạm thời
def Ctrl_get_password_status(device_id, password_id):
    # Gọi API của tuya để lấy trạng thái  
    response = tuya_get_password_status(device_id, password_id)
    if response['success']:
        # Trả về tarng5 thái mật khẩu
        return f'{response["result"]["phase"]}'
    else:
        return f'Lấy trạng thái mật khẩu không thành công: {response["msg"]}' 

    



