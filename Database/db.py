from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# Khởi tạo kết nối với cơ sở dữ liệu MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
home = db['home']
room = db['room']
device = db['device']
device_passwords = db['device_passwords']
device_logs = db['device_logs']



# ______________________________________________[ HOME ]  
# Hàm thêm một Home mới vào cơ sở dữ liệu
def Db_set_home(Name, address):
    time = datetime.now()
    createAt = time.strftime('%Y-%m-%d %H:%M:%S')
    home_data = {
        'Name': Name,
        'address': address,
        'createAt': createAt
    }
    home.insert_one(home_data)

# Hàm lấy thông tin home
def Db_get_homes():
    homes = home.find()
    result = []
    for home_data in homes:
        result.append({
            'Name': home_data['Name'],
            'address': home_data['address'],
            'createAt': home_data['createAt']
        })
    return result

# Hàm update Home
def Db_update_home(home_id, Name, Address):
    home.update_one({'_id': ObjectId(home_id)}, {'$set': {
        'Name': Name,
        'address': Address,
    }})
    
# Hàm xóa Home
def Db_delete_home(home_id):
    home.delete_one({'_id': ObjectId(home_id)})
    room.delete_many({'home_id': home_id})   



# ______________________________________________[ ROOM ]
# Hàm thêm một Room
def Db_set_room(home_id, Name):
    time = datetime.now()
    createAt = time.strftime('%Y-%m-%d %H:%M:%S')
    room_data = {
        'home_id': home_id,
        'Name': Name,
        'createAt': createAt
    }
    room.insert_one(room_data)

# Hàm lấy thông tin Room
def Db_get_rooms():
    rooms = room.find()
    result = []
    for room_data in rooms:
        result.append({
            'home_id': room_data['home_id'],
            'Name': room_data['Name'],
            'createAt': room_data['createAt']
        })
    return result

# Hàm update Room
def Db_update_room(room_id, home_id, Name):
    room.update_one({'_id': ObjectId(room_id)}, {'$set': {
        'home_id': home_id,
        'Name': Name,
    }})
    
# Hàm xóa Room    
def Db_delete_room(room_id):
    room.delete_one({'_id': room_id})
    device.delete_many({'room_id': room_id,})



# ______________________________________________[ DEVICE ]
# Hàm thêm một Device
def Db_set_device(device_id, room_id, type):
    time = datetime.now()
    createAt = time.strftime('%Y-%m-%d %H:%M:%S')
    device_data = {
        'device_id': device_id,
        'room_id': room_id,
        'type': type,
        'createAt': createAt
    }
    device.insert_one(device_data)

# Hàm lấy thông tin Device
def Db_get_devices():
    devices = device.find()
    result = []
    for device_data in devices:
        result.append({
            'device_id': device_data['device_id'],
            'room_id': device_data['room_id'],
            'type': device_data['type'],
            'createAt': device_data['createAt']
        })
    return result

# Hàm update Device
def Db_update_device(Db_device_id, room_id, type):
    device.update_one({'_id': Db_device_id}, {'$set': {
        'room_id': room_id,
        'type': type,
    }})

# Hàm cập nhật pin cho Device
def Db_update_device_pin(devId, battery_state):
    device.update_one({'device_id': devId}, {'$set': {
        'battery_state': battery_state
    }})

# Hàm xóa Device   
def Db_delete_device(room_id):
    room.delete_one({'_id': room_id})
    device.delete_many({'room_id': room_id,})      



# ______________________________________________[ PASSWORD ]
# Hàm thêm Passwords
def Db_set_device_password(device_id, Name, password, effective_time, invalid_time, password_id):
    effective_time_str = datetime.fromtimestamp(effective_time).strftime('%Y-%m-%d %H:%M:%S')
    invalid_time_str = datetime.fromtimestamp(invalid_time).strftime('%Y-%m-%d %H:%M:%S')
    device_passwords_data = {
        'password_id': password_id,
        'device_id': device_id,
        'Name': Name,
        'password': password,
        'effective_time': effective_time_str,
        'invalid_time': invalid_time_str,
        'password_type': 'ticket',
        'status': '...'
    }
    device_passwords.insert_one(device_passwords_data)

# Hàm lấy thông tin Password
def Db_get_device_passwords():
    result = []
    for device_password in device_passwords.find():
        result.append({
            'device_id': device_password['device_id'],
            'Name': device_password['Name'],
            'password': device_password['password'],
            'effective_time': device_password['effective_time'],
            'invalid_time': device_password['invalid_time'],
            'password_type': device_password['password_type'],
            'password_id': device_password['password_id']['id'],
            'status': device_password['status']
        })
    return result

# Hàm update trạng thái Password
def Db_update_device_password_status(device_id, password_id, status):
    device_passwords.update_one(
        {'device_id': device_id, 'password_id.id': password_id},
        {'$set': {'status': status}}
    )

# Hàm cập nhật Password Db
def Db_update_device_password(device_id, password_id, password, effective_time, invalid_time):
    effective_time_str = datetime.fromtimestamp(effective_time).strftime('%Y-%m-%d %H:%M:%S')
    invalid_time_str = datetime.fromtimestamp(invalid_time).strftime('%Y-%m-%d %H:%M:%S')
    device_passwords.update_one({'device_id': device_id, 'password_id.id': password_id}, {'$set': {
        'password': password,
        'effective_time': effective_time_str,
        'invalid_time': invalid_time_str,
        'password_type': 'ticket',
    }})

# Hàm xóa Passord Db
def Db_delete_device_password(device_id, password_id):
    device_passwords.delete_one({'device_id': device_id, 'password_id.id': password_id})



# ______________________________________________[ LOG ]
# Hàm lưu log vào cơ sở dữ liệu
def Db_set_device_logs(devId, Action, value, formatted_time): 
    device_logs_data = {
        'device_id': devId,
        'action': Action,
        'value': value,
        'time': formatted_time
    }
    device_logs.insert_one(device_logs_data)

# Hàm lấy log theo từng device
def Db_get_device_logs(devId):
    logs = device_logs.find({'device_id': devId})
    result = []
    for log_data in logs:
        result.append({
            'device_id': log_data['device_id'],
            'action': log_data['action'],
            'value': log_data['value'],
            'time': log_data['time']
        })
    return result

# Hàm cập nhật logs bị miss
def Db_update_log(devId, Action, value, time):
    device_logs.update_many(  
        {'device_id': devId, 'time': time},
        {'$set': {
            'device_id': devId,
            'action': Action,
            'value': value,
            'time': time 
        }}, upsert=True
    ) 



    


   




