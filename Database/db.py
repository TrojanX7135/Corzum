from pymongo import MongoClient

# Khởi tạo kết nối với cơ sở dữ liệu MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
locks = db['locks']

# Hàm lấy danh sách các khóa cửa từ cơ sở dữ liệu
def get_locks():
    result = []
    for lock in locks.find():
        result.append({
            'device_id': lock['device_id'],
            'Name': lock['Name'],
            'password': lock['password'],
            'effective_time': lock['effective_time'],
            'invalid_time': lock['invalid_time'],
            'password_type': lock['password_type'],
            'ticket_id': lock['ticket_id']
        })
    return result

# Hàm thêm một khóa cửa mới vào cơ sở dữ liệu
def setDb_lock_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id):
    lock_data = {
        'device_id': device_id,
        'Name': Name,
        'password': password,
        'effective_time': effective_time,
        'invalid_time': invalid_time,
        'password_type': password_type,
        'ticket_id': ticket_id,
    }
    locks.insert_one(lock_data)

# Hàm cập nhật mật khẩu cho một khóa cửa trong cơ sở dữ liệu
def updateDb_lock_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id):
    locks.update_one({'device_id': device_id}, {'$set': {
    'Name': Name,
    'password': password,
    'effective_time': effective_time,
    'invalid_time': invalid_time,
    'password_type': password_type,
    'ticket_id': ticket_id,
}})
    
# Hàm xóa mật khẩu cho một khóa cửa
def deleteDb_lock_password(device_id):
    locks.delete_one({'device_id': device_id})



