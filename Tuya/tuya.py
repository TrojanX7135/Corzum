from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
from datetime import datetime, timedelta
from tuya_connector import (
    TuyaOpenAPI
)
import time as time_module


# Khởi tạo kết nối với API của Tuya
ACCESS_ID = "jgxfarjqssw7pwfmjqrm"
ACCESS_KEY = "e9a1f6b2dc3a402e9ec53a365e4b07d9"
API_ENDPOINT = "https://openapi.tuyaus.com"
MQ_ENDPOINT = "wss://mqe.tuyaus.com:8285/"
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()


# Hàm gọi API của Tuya để lấy tickey-id
def tuya_get_tickeyId(device_id):
    response = openapi.post(f'/v1.0/devices/{device_id}/door-lock/password-ticket', {
        'device_id': device_id,
    })
    return response


# Hàm xử lý mã hóa mật khẩu bằng tickey-id
def encode(device_id, password, access_secret):
    # Gọi hàm tuya_get_tickeyId để lấy ticket-id
    ticket_response = tuya_get_tickeyId(device_id)
    ticket_id = ticket_response['result']['ticket_id']
    ticket_key = ticket_response['result']['ticket_key']
    # Giải mã ticket-key để lấy khóa bí mật
    secret_key = unpad(AES.new(access_secret.encode('utf-8'), AES.MODE_ECB).decrypt(bytes.fromhex(ticket_key)), AES.block_size)
    # Mã hóa mật khẩu
    encrypted_password = AES.new(secret_key, AES.MODE_ECB).encrypt(pad(password.encode('utf-8'), AES.block_size)).hex()
    return encrypted_password, ticket_id


# Hàm gọi API của Tuya để đặt mật khẩu cho thiết bị khóa cửa
def tuya_set_lock_password(device_id, Name, password, effective_time, invalid_time):
    access_secret = ACCESS_KEY
    # Mã hóa mật khẩu bằng cách sử dụng ticket-key
    encrypted_password, ticket_id = encode(device_id, password, access_secret)
    # Gọi API đặt mật khẩu
    response = openapi.post(f'/v1.0/devices/{device_id}/door-lock/temp-password', {
        'device_id': device_id,
        'Name': Name,
        'password': encrypted_password,
        'effective_time': effective_time,
        'invalid_time': invalid_time,
        'password_type': 'ticket',
        'ticket_id': ticket_id,
    })
    return response


# Hàm gọi API của Tuya để cập nhật lại mật khẩu tạm thời
def tuya_update_lock_password(device_id, password_id, password, effective_time, invalid_time):
    access_secret = ACCESS_KEY
    # Mã hóa mật khẩu bằng cách sử dụng ticket-key
    encrypted_password, ticket_id = encode(device_id, password, access_secret)
    # Gọi API đặt lại mật khẩu 
    response = openapi.put(f'/v1.0/devices/{device_id}/door-lock/temp-passwords/{password_id}/modify-password', {
        'device_id': device_id,
        'password_id': password_id,
        'password': encrypted_password,
        'effective_time': effective_time,
        'invalid_time': invalid_time,
        'password_type': 'ticket',
        'ticket_id': ticket_id
    })
    return response


# Hàm gọi API của Tuya để xóa mật khẩu tạm thời trên device
def tuya_delete_lock_password(device_id, password_id):
    response = openapi.delete(f'/v1.0/devices/{device_id}/door-lock/temp-passwords/{password_id}', {
        'device_id': device_id,
        'password_id': password_id
    })
    return response


# Hàm gọi API của Tuya để lấy OTP
def tuya_set_lock_OTP(device_id):
    access_secret = ACCESS_KEY
    password = str(random.randint(1000000, 9999999))
    # Mã hóa mật khẩu bằng cách sử dụng ticket-key
    encrypted_password, ticket_id = encode(device_id, password, access_secret)
    # Định dạng thời gian theo chuẩn ISO 8601
    time_format = '%Y-%m-%dT%H:%M:%SZ'
    # Lấy thời điểm hiện tại
    now = datetime.utcnow()
    # Tính toán thời điểm hiệu lực của mật khẩu (thời điểm hiện tại)
    effective_time = now.strftime(time_format)
    # Tính toán thời điểm hết hiệu lực của mật khẩu (thời điểm hiện tại cộng thêm 1 phút)
    invalid_time = (now + timedelta(minutes=5)).strftime(time_format)
    # Gọi API đặt mật khẩu
    response = openapi.post(f'/v1.0/devices/{device_id}/door-lock/temp-password', {
        'device_id': device_id,
        'Name': 'OTP',
        'password': encrypted_password,
        'effective_time': effective_time,
        'invalid_time': invalid_time,
        'password_type': 'ticket',
        'ticket_id': ticket_id,
    })
    if response['success']:
        response['password'] = {'password': password}
    return response


# Hàm gọi API để lấy trạng thái của khóa tạm thời
def tuya_get_password_status(device_id, password_id):
    response = openapi.get(f'/v1.0/devices/{device_id}/door-lock/temp-password/{password_id}', {
        'device_id': device_id,
        'password_id': password_id
    })
    return response


# Hàm gọi API của Tuya để lấy trạng thái pin của khóa cửa
def tuya_get_lock_status(device_id):
    response = openapi.get(f'/v1.0/devices/{device_id}', {
        'device_id': device_id
    })
    return response


# Hàm gọi API để chụp ảnh
def tuya_capture_an_image(device_id):
    response = openapi.post(f'/v1.0/cameras/{device_id}/actions/capture', {
        'device_id': device_id
    })
    return response


# Hàm gọi API của Tuya để lấy nhật ký thiết bị
def tuya_get_device_logs_Tuya(devId):
    end_time = int(time_module.time() * 1000)
    start_time = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
    response = openapi.get(f'/v1.0/devices/{devId}/logs', {
        'device_id': devId,
        'type': '7',
        'start_time': start_time,
        'end_time': end_time
    })
    return response

# Hàm gọi API của Tuya để lấy nhật ký thiết bị 2
def tuya_get_device_logs_Tuya_2(devId, start_time, end_time):
    response = openapi.get(f'/v1.0/devices/{devId}/door-lock/open-logs', {
        'device_id': devId,
        'type': '7',
        'start_time': start_time,
        'end_time': end_time
    })
    return response


# Hàm gọi API của Tuya để lấy list device có trong Cloud
def tuya_get_list_device_inCloud():
    response = openapi.get(f'/v1.3/iot-03/devices')
    return response



