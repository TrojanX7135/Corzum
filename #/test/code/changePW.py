from fastapi import FastAPI, Form
from pymongo import MongoClient
from tuya_connector import TuyaOpenAPI

app = FastAPI()

# Khởi tạo kết nối với cơ sở dữ liệu MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
locks = db['locks']

# Khởi tạo kết nối với API của Tuya
ACCESS_ID = 'sgxwf8d4rq7qyvpk3dgc'
ACCESS_KEY = 'p1688376465608hsvkgk'
API_ENDPOINT = 'https://openapi.tuyaus.com'
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

def change_password(lock_id, new_password):
    # Tìm kiếm tài liệu tương ứng trong bộ sưu tập locks
    lock = locks.find_one({'lock_id': lock_id})
    if not lock:
        return f'Không tìm thấy khóa cửa với id {lock_id}'

    # Cập nhật mật khẩu trong cơ sở dữ liệu
    locks.update_one({'lock_id': lock_id}, {'$set': {'password': new_password}})

    # Gọi API của Tuya để thay đổi mật khẩu trên thiết bị khóa cửa
    response = openapi.post(f'/v1.0/devices/{lock_id}/door-lock/password', {
        'password': new_password,
        'password_type': lock['password_type']
    })
    if response['success']:
        return f'Đổi mật khẩu thành công cho khóa cửa {lock_id}'
    else:
        return f'Đổi mật khẩu thất bại cho khóa cửa {lock_id}: {response["msg"]}'

@app.get('/')
async def get_locks():
    result = []
    for lock in locks.find():
        result.append({
            'lock_id': lock['lock_id'],
            'password': lock['password']
        })
    return result

@app.post('/')
async def update_password(lock_id: str = Form(...), new_password: str = Form(...)):
    result = change_password(lock_id, new_password)
    return {'result': result}
