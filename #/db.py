from pymongo import MongoClient
from datetime import datetime

# Khởi tạo kết nối với cơ sở dữ liệu MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
device = db['device']
locks = db['locks']

def Db_get_locks():
    result = []
    for device_data in device.find():
        if 'locks' in device_data:
            for lock in device_data['locks']:
                result.append({
                    'device_id': device_data['_id'],
                    'Name': lock['Name'],
                    'password': lock['password'],
                    'effective_time': lock['effective_time'],
                    'invalid_time': lock['invalid_time'],
                    'password_type': lock['password_type'],
                    'password_id': lock['password_id']
                })
    return result

# Hàm thêm một khóa cửa mới vào cơ sở dữ liệu
def Db_set_lock_password(device_id, Name, password, effective_time, invalid_time, password_id):
    effective_time_str = datetime.fromtimestamp(effective_time).strftime('%Y-%m-%d %H:%M:%S')
    invalid_time_str = datetime.fromtimestamp(invalid_time).strftime('%Y-%m-%d %H:%M:%S')
    lock_data = {
        'device_id': device_id,
        'Name': Name,
        'password': password,
        'effective_time': effective_time_str,
        'invalid_time': invalid_time_str,
        'password_type': 'ticket',
        'password_id': password_id
    }
    device.update_one({'_id': device_id}, {'$set': {'_id': device_id}, '$push': {'locks': lock_data}}, upsert=True)

# Hàm lưu log vào cơ sở dữ liệu
def Db_set_logs(devId, Action, value, formatted_time): 
    record_data = {
        'device_id': devId,
        'action': Action,
        'action.value': value,
        'time': formatted_time
    }
    device.update_one({'_id': devId}, {'$set': {'_id': devId}, '$push': {'record': record_data}}, upsert=True)

# Hàm cập nhật mật khẩu cho một khóa cửa trong cơ sở dữ liệu
def Db_update_lock_password(device_id, password_id, password, effective_time, invalid_time):
    effective_time_str = datetime.fromtimestamp(effective_time).strftime('%Y-%m-%d %H:%M:%S')
    invalid_time_str = datetime.fromtimestamp(invalid_time).strftime('%Y-%m-%d %H:%M:%S')
    device.update_one({'_id': device_id, 'locks.password_id.id': password_id}, {'$set': {
        'locks.$.password': password,
        'locks.$.effective_time': effective_time_str,
        'locks.$.invalid_time': invalid_time_str,
        'locks.$.password_type': 'ticket',
    }})
    
# Hàm xóa mật khẩu cho một khóa cửa
def Db_delete_lock_password(device_id, password_id):
    device.update_one({'_id': device_id}, {'$pull': {'locks': {'password_id.id': password_id}}})



