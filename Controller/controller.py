from Database.db import get_locks, setDb_lock_password, updateDb_lock_password, deleteDb_lock_password
from Models.models import Lock
from Tuya.tuya import set_tuya_password
from Tuya.tuya import get_tuya_tickeyId
from Tuya.tuya import delete_tuya_password
from Tuya.tuya import get_tuya_history

# Hàm lấy danh sách các khóa cửa từ cơ sở dữ liệu
def get_all_locks():
    return get_locks()


# Hàm lấy tickey-id cho mã hóa mật khẩu
def get_tickeyId(device_id):
    # Gọi API của Tuya để lấy TickeyId
    response = get_tuya_tickeyId(device_id)
    if response['success']:
        return f'Lấy TickeyId cho {device_id} thành công : {response["result"]}'
    else :
        return f'Lấy TickeyId cho {device_id} thất bại : {response["msg"]}'


# Hàm đặt mật khẩu cho khóa cửa    
def set_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id):
    # Gọi API của Tuya để đặt mật khẩu cho khóa cửa
    response = set_tuya_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id)
    if response['success']:
        # Thêm khóa cửa mới vào cơ sở dữ liệu
        setDb_lock_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id)
        return f'Đặt mật khẩu thành công cho khóa cửa {device_id} : {response["result"]}'
    else:
        return f'Đặt mật khẩu thất bại cho khóa cửa {device_id}: {response["msg"]}'


# Hàm thay đổi mật khẩu cho một khóa cửa
def update_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id):
    # Kiểm tra xem khóa cửa có tồn tại trong cơ sở dữ liệu hay không
    lock = Lock.get_lock(device_id)
    if not lock:
        return f'Không tìm thấy khóa cửa với id {device_id}'    
    # Gọi API của Tuya để xóa mật khẩu hiện tại
    delete_tuya_password(device_id)    
    # Gọi API của Tuya để đặt mật khẩu mới
    response = set_tuya_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id)
    if response['success']:
        # Cập nhật thông tin mật khẩu mới vào cơ sở dữ liệu
        updateDb_lock_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id)
        return f'Đổi mật khẩu thành công cho khóa cửa {device_id} : {response["result"]}'
    else:
        return f'Đổi mật khẩu thất bại cho khóa cửa {device_id}: {response["msg"]}'


# Hàm xóa mật khẩu tạm thời cho khóa cửa
def delete_password(device_id):
    # Gọi API của Tuya để xóa mật khẩu tạm thời
    response = delete_tuya_password(device_id)
    if response['success']:
        # Xóa thông tin mật khẩu khỏi cơ sở dữ liệu
        deleteDb_lock_password(device_id)
        return f'Xóa mật khẩu thành công cho khóa cửa {device_id} : {response["result"]}'
    else:
        return f'Xóa mật khẩu thất bại cho khóa cửa {device_id}: {response["msg"]}'

# Hàm lấy nhật ký hoạt động của khóa cửa
def history_lock(device_id):
    # Gọi API của Tuya để lấy lịch sử
    response = get_tuya_history(device_id)
    if response['success']:
        return f'Nhật ký hoạt động của khóa cửa {device_id} : {response["result"]}'
    else:
        return f'Không lấy được nhật ký hoạt động của khóa cửa {device_id} : {response["msg"]}'