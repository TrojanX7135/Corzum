from bson.objectid import ObjectId
from datetime import datetime

from Database.db import home, room, device, device_passwords, device_logs
from Database.db import Db_set_home, Db_get_homes, Db_update_home, Db_delete_home
from Database.db import Db_set_room, Db_get_rooms, Db_get_rooms_withHome, Db_update_room, Db_delete_room
from Database.db import Db_set_device, Db_get_devices, Db_get_devices_withRoom, Db_update_device, Db_add_device_fromCloud ,Db_delete_device, Db_update_device_pin
from Database.db import Db_set_device_password, Db_get_device_passwords, Db_get_device_passwords_withDevice, Db_update_device_password, Db_update_device_password_status, Db_delete_device_password
from Database.db import Db_get_device_logs, Db_update_log

from Tuya.tuya import tuya_set_lock_password, tuya_update_lock_password, tuya_delete_lock_password
from Tuya.tuya import tuya_get_lock_status
from Tuya.tuya import tuya_set_lock_OTP
from Tuya.tuya import tuya_get_password_status
from Tuya.tuya import tuya_get_device_logs_Tuya
from Tuya.tuya import tuya_get_list_device_inCloud, tuya_update_device


# ______________________________________________[ HOME ] 
class Home:
    @staticmethod
    
    # Tạo Home
    def Model_set_home(Name, address):
        Db_set_home(Name, address)
        return f'OK'

    # Lấy Home
    def Model_get_homes():
        return Db_get_homes()

    # Cập nhật Home
    def Model_update_home(home_id, Name, address):
        find = home.find_one({'_id': ObjectId(home_id)})
        if not find:
            return f'Error: không tìm thấy home_id'
        else:
            Db_update_home(home_id, Name, address)
            return f'OK'
    
    # Xóa Home
    def Model_delete_home(home_id):
        find = home.find_one({'_id': ObjectId(home_id)})
        if not find:
            return f'Error: không tìm thấy home_id'
        else:
            Db_delete_home(home_id)
            return f'OK'  



# ______________________________________________[ ROOM ] 
class Room:
    @staticmethod
    
    # Tạo Room
    def Model_set_room(home_id, Name):
        # Kiểm tra xem home_id có tồn tại trong collection home hay không
        find = home.find_one({'_id': ObjectId(home_id)})
        if not find:
            return f'Error: không tìm thấy home_id'
        else:
            Db_set_room(home_id, Name)
            return f'OK'

    # Lấy Rooms
    def Model_get_rooms():
        return Db_get_rooms()
    
    # Lấy danh sách Room với Home
    def Model_get_rooms_withHome(home_id):
        find = home.find_one({'_id': ObjectId(home_id)})
        if not find:
            return f'Error: không tìm thấy home_id'
        else:
            return Db_get_rooms_withHome(home_id)


    # Cập nhật Room
    def Model_update_room(room_id, home_id, Name):
        find = room.find_one({'_id': ObjectId(room_id)})
        if not find:
            return f'Error: không tìm thấy room_id'
        find = home.find_one({'_id': ObjectId(home_id)})
        if not find:
            return f'Error: không tìm thấy home_id'
        else:
            Db_update_room(room_id, home_id, Name)
            return f'OK'
        
    # Xóa Room
    def Model_delete_room(room_id):
        find = room.find_one({'_id': ObjectId(room_id)})
        if not find:
            return f'Error: không tìm thấy room_id'
        else:
            Db_delete_room(room_id)
            return f'OK'  



# ______________________________________________[ DEVICE ] 
class Device:
    @staticmethod
    
    # Tạo Device
    def Model_set_device(device_id, room_id, type, name):
        # Kiểm tra xem home_id có tồn tại trong collection home hay không
        find = room.find_one({'_id': ObjectId(room_id)})
        if not find:
            return f'Error: không tìm thấy room_id'
        else:
            Db_set_device(device_id, room_id, type, name)
            return f'OK'

    # Lấy Devices đồng thời cập nhật trạng thái pin cho device
    def Model_get_devices():
        device_list = tuya_get_list_device_inCloud()
        properties = device_list['result']['list']
        for prop in properties:
            device_id = prop['id']
            type = prop['category_name']
            name = prop['name']
            time = prop['create_time']
            timestamp = datetime.fromtimestamp(time)
            createAt = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            Db_add_device_fromCloud(device_id, type, name, createAt)
            response = tuya_get_lock_status(device_id)
            if response['success']:
                for code in response["result"]["status"]:
                    # Kiểm tra xem code có phải là battery_state hay không
                    if code["code"] == "battery_state":
                        # Trả về giá trị của code battery_state
                        battery_state = code["value"]
                        Db_update_device_pin(device_id, battery_state)
            else:
                return f'Error : {response["msg"]}'
        return Db_get_devices()
    
    # Lấy danh sách Device với Room đồng thời cập nhật trạng thái pin cho device
    def Model_get_devices_withRoom(room_id):
        find = room.find_one({'_id': ObjectId(room_id)})
        if not find:
            return f'Error: không tìm thấy room_id'
        else:
            device_list = tuya_get_list_device_inCloud()
            properties = device_list['result']['list']
            for prop in properties:
                device_id = prop['id']
                type = prop['category_name']
                name = prop['name']
                time = prop['create_time']
                timestamp = datetime.fromtimestamp(time)
                createAt = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                Db_add_device_fromCloud(device_id, type, name, createAt)
                response = tuya_get_lock_status(device_id)
                if response['success']:
                    for code in response["result"]["status"]:
                        # Kiểm tra xem code có phải là battery_state hay không
                        if code["code"] == "battery_state":
                            # Trả về giá trị của code battery_state
                            battery_state = code["value"]
                            Db_update_device_pin(device_id, battery_state)
                else:
                    return f'Error : {response["msg"]}'
            return Db_get_devices_withRoom(room_id)

    # Cập nhật Device
    def Model_update_device(device_id, room_id, name):
        find_device = device.find_one({'device_id': device_id})
        find_room = room.find_one({'_id': ObjectId(room_id)})
        if not find_device:
            return f'Error: không tìm thấy device_id'
        if not find_room:
            return f'Error: không tìm thấy room_id'        
        else:
            try:
                tuya_update_device(device_id, name)
            except Exception as e:
                return f'Error: {e}'
            Db_update_device(device_id, room_id, name)
            return f'OK'
        
    # Xóa Device
    def Model_delete_device(device_id):
        find = device.find_one({'device_id': device_id})
        if not find:
            return f'Error: không tìm thấy device_id'
        else:
            Db_delete_device(device_id)
            return f'OK'  



# ______________________________________________[ PASSWORD ] 
class DevicePassword:
    @staticmethod
    
    # Tạo password 
    def Model_set_device_password(device_id, Name, password, effective_time, invalid_time):
        # Kiểm tra xem home_id có tồn tại trong collection home hay không
        find = device.find_one({'device_id': device_id})
        if not find:
            # Nếu không tồn tại, trả về lỗi
            return f'Error: không tìm thấy device_id'
        else:
            # Gọi API của Tuya để đặt mật khẩu cho khóa cửa
            response = tuya_set_lock_password(device_id, Name, password, effective_time, invalid_time)
            if response['success']:
                Db_set_device_password(device_id, Name, password, effective_time, invalid_time, password_id=response["result"])
                return f'OK: {response["result"]}'
            else:
                return f'Error: {response["msg"]}'

    # Tạo password OTP
    def Model_set_device_password_OTP(device_id):
        # Gọi API của tuya
        response = tuya_set_lock_OTP(device_id)
        if response['success']:
            # Trả về mật khẩu OTP
            return f'{response["result"]}, {response["password"]}'
        else:
            return f'Error: {response["msg"]}'

    # Lấy danh sách Passwords đồng thời cập nhật trạng thái password
    def Model_get_device_passwords():
        # Lấy danh sách các mật khẩu từ cơ sở dữ liệu
        passwords_data = Db_get_device_passwords()
        for password_data in passwords_data:
            # Lấy trạng thái của mật khẩu
            device_id = password_data['device_id']
            password_id = password_data['password_id']
            status = Model_get_status_device_password(device_id, password_id)
            # Cập nhật trạng thái của mật khẩu trong cơ sở dữ liệu
            Db_update_device_password_status(device_id, password_id, status)
        return Db_get_device_passwords()
    
    def Model_get_device_passwords_withDevice(device_id):
        find = device.find_one({'device_id': device_id})
        if not find:
            return f'Error: không tìm thấy device_id'
        else:
            # Lấy danh sách các mật khẩu từ cơ sở dữ liệu
            passwords_data = Db_get_device_passwords()
            for password_data in passwords_data:
                # Lấy trạng thái của mật khẩu
                device_id_2 = password_data['device_id']
                password_id = password_data['password_id']
                status = Model_get_status_device_password(device_id_2, password_id)
                # Cập nhật trạng thái của mật khẩu trong cơ sở dữ liệu
                Db_update_device_password_status(device_id_2, password_id, status)
            return Db_get_device_passwords_withDevice(device_id)
            

    # Cập nhật Device password
    def Model_update_device_password(device_id, password_id, password, effective_time, invalid_time):  
        find_devcie = device.find_one({'device_id': device_id})
        find_password = device_passwords.find_one({'password_id.id': password_id})
        if not find_devcie:
            return f'Error: không tìm thấy device'
        if not find_password:
            return f'Error: không tìm thấy password_id'
        else:
            # Gọi API của Tuya để đặt mật khẩu mới
            Db_update_device_password(device_id, password_id, password, effective_time, invalid_time)
            response = tuya_update_lock_password(device_id, password_id, password, effective_time, invalid_time)
            if response['success']:
                # Cập nhật thông tin mật khẩu mới vào cơ sở dữ liệu           
                return f'OK : {response["result"]}'
            else:
                return f'Error: {response["msg"]}'
            
    # Xóa password trên Cloud Tuya
    def Model_delete_device_password(device_id, password_id):
        find_devcie = device.find_one({'device_id': device_id})
        find_password = device_passwords.find_one({'password_id.id': password_id})
        if not find_devcie:
            return f'Error: không tìm thấy device'
        if not find_password:
            return f'Error: không tìm thấy password_id'
        else:
            # Gọi API của Tuya để xóa mật khẩu tạm thời
            response = tuya_delete_lock_password(device_id, password_id)
            if response['success']:
                # Xóa thông tin mật khẩu khỏi cơ sở dữ liệu
                return f'OK: {response["result"]}'
            else:
                return f'Error: {response["msg"]}'
            
    # Xóa password trong Db
    def Mode_delete_password_inDatabase(password_id):
        find = device_passwords.find_one({'password_id.id': password_id})
        if not find:
            return f'Error: không tìm thấy password_id'
        else:
            Db_delete_device_password(password_id)
            return f'OK' 

# Hàm lấy status Password từ tuya
def Model_get_status_device_password(device_id, password_id):
    # Gọi API của tuya để lấy trạng thái  
    response = tuya_get_password_status(device_id, password_id)
    if response['success']:
        # Trả về trạng thái mật khẩu
        return f'{response["result"]["phase"]}'
    else:
        return f'Error : {response["msg"]}' 



# ______________________________________________[ LOG ]
class DeviceLog:
    @staticmethod
    
    # Hàm Lấy Logs
    def Model_get_device_logs(devId):
        find_device = device.find_one({'device_id': devId})
        find_device_log = device_logs.find({'device_id': devId})
        if not find_device:
            return f'Error: không tìm thấy device'
        if not find_device_log:
            return f'Error: không tìm thấy logs của device'
        else:
            return Db_get_device_logs(devId)
        
    # Hàm cập nhật Logs
    def Model_update_device_logs():
        try:
            device_list = tuya_get_list_device_inCloud()
            properties = device_list['result']['list']
            for prop in properties:
                device_id = prop['id']
                Tuya_logs = tuya_get_device_logs_Tuya(device_id)
                properties_2 = Tuya_logs['result']['logs']
                for prop2 in properties_2:
                    if prop2['code'] != 'battery_state':
                        Action2 = prop2['code']
                        value2 = prop2['value']
                        time2 = prop2['event_time']
                        timestamp2 = datetime.fromtimestamp(time2/1000)
                        formatted_time2 = timestamp2.strftime('%Y-%m-%d %H:%M:%S')
                        Db_update_log(device_id, Action2, value2, formatted_time2)
            return f'OK'
        except Exception as e:
            return f'Error: {e}'       



# ______________________________________________[ TUYA Object ]
# Hàm lấy trạng thái pin của khóa cửa từ TUYA
def Model_get_device_status_pin(device_id):
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
        return f'Error : {response["msg"]}'
    
# Hàm lấy nhật ký thiết bị từ Tuya
def Model_get_device_logs_Tuya(device_id):
    # Gọi API của Tuya để lấy log
    response = tuya_get_device_logs_Tuya(device_id)
    if response['success']:
        return f'{response["result"]}'
    else:
        return f'Error : {response["msg"]}'
    
# Hàm lấy list device có trong Cloud Tuya
def Model_get_list_device_inCloud():
    response = tuya_get_list_device_inCloud()
    if response['success']:
        return f'{response["result"]}'
    else:
        return f'Error : {response["msg"]}'




