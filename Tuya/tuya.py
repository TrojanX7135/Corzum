from tuya_connector import TuyaOpenAPI

# Khởi tạo kết nối với API của Tuya
ACCESS_ID = "88rhdtkuvwuwvnf9sqfg"
ACCESS_KEY = "e3975867df94441195361e543bd45f85"
API_ENDPOINT = 'https://openapi.tuyaus.com'
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Hàm gọi API của Tuya để lấy tickey-id
def get_tuya_tickeyId(device_id):
    response = openapi.post(f'/v1.0/devices/{device_id}/door-lock/password-ticket', {
        'device_id': device_id,
    })
    return response

# Hàm gọi API của Tuya để đặt mật khẩu cho thiết bị khóa cửa
def set_tuya_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id):
    response = openapi.post(f'/v1.0/devices/{device_id}/door-lock/temp-password', {
        'device_id': device_id,
        'Name': Name,
        'password': password,
        'effective_time': effective_time,
        'invalid_time': invalid_time,
        'password_type': password_type,
        'ticket_id': ticket_id,
    })
    return response

# Hàm gọi API của Tuya để xóa mật khẩu tạm thời trên device
def delete_tuya_password(device_id):
    response = openapi.post(f'/v1.0/devices/{device_id}/door-lock/temp-passwords/rest-password', {
        'device_id': device_id
    })
    return response

# Hàm gọi API của Tuya để lấy nhật ký hoạt động của khóa cửa
def get_tuya_history(device_id):
    response = openapi.post(f'/v1.0/devices/{device_id}/door-lock/open-logs?page_no=1&page_size=20&start_time=1543213146&end_time=1543213546', {
        'device_id': device_id
    })
    return response


