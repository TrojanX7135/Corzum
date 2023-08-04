from bson.objectid import ObjectId

from Database.db import home, room, device, device_passwords, device_logs
from Database.db import Db_set_home, Db_get_homes, Db_update_home, Db_delete_home
from Database.db import Db_set_room, Db_get_rooms, Db_update_room, Db_delete_room
from Database.db import Db_set_device, Db_get_devices, Db_update_device, Db_delete_device
from Database.db import Db_set_device_password, Db_get_device_passwords, Db_update_device_password, Db_update_device_password_status, Db_delete_device_password
from Database.db import Db_get_device_logs

from Tuya.tuya import tuya_set_lock_password, tuya_update_lock_password, tuya_delete_lock_password
from Tuya.tuya import tuya_get_lock_status
from Tuya.tuya import tuya_set_lock_OTP
from Tuya.tuya import tuya_get_password_status
from Tuya.tuya import tuya_capture_an_image
from Tuya.tuya import tuya_get_device_logs_Tuya, tuya_get_device_logs_Tuya_2
from Tuya.tuya import tuya_get_list_device_inCloud


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
    def Model_update_home(home_id, Name, Address):
        find = home.find_one({'_id': ObjectId(home_id)})
        if not find:
            return f'Error: không tìm thấy home_id'
        else:
            Db_update_home(home_id, Name, Address)
            return f'OK'



class Room:

    @staticmethod
    # Tạo Room
    def Model_set_room(home_id, Name):
        # Kiểm tra xem home_id có tồn tại trong collection home hay không
        find = home.find_one({'_id': home_id})
        if not find:
            return f'Error: không tìm thấy home_id'
        else:
            Db_set_room(home_id, Name)
            return f'OK'

    # Lấy Rooms
    def Model_get_rooms():
        return Db_get_rooms()

    # Cập nhật Home
    def Model_update_room(room_id, home_id, Name):
        find = room.find_one({'_id': ObjectId(room_id)})
        if not find:
            return f'Error: không tìm thấy room_id'
        else:
            Db_update_room(room_id, home_id, Name)
            return f'OK'



class Device:

    @staticmethod
    # Tạo Device
    def Model_set_device(device_id, room_id, type):
        # Kiểm tra xem home_id có tồn tại trong collection home hay không
        find = room.find_one({'_id': room_id})
        if not find:
            return f'Error: không tìm thấy room_id'
        else:
            Db_set_device(device_id, room_id, type)
            return f'OK'

    # Lấy Devices
    def Model_get_devices():
        return Db_get_devices()

    # Cập nhật Device
    def Model_update_device(Db_device_id, room_id, type):
        find = device.find_one({'_id': ObjectId(Db_device_id)})
        if not find:
            return f'Error: không tìm thấy device_id'
        else:
            Db_update_device(Db_device_id, room_id, type)
            return f'OK'



class DevicePassword:

    @staticmethod
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

    def Model_set_device_password_OTP(device_id):
        # Gọi API của tuya
        response = tuya_set_lock_OTP(device_id)
        if response['success']:
            # Trả về mật khẩu OTP
            return f'{response["result"]}, {response["password"]}'
        else:
            return f'Lấy OTP không thành công cho khóa {device_id} : {response["msg"]}'

    # Hàm lấy danh sách Passwords
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

    # Cập nhật Device password
    def Model_update_device_password(device_id, password_id, password, effective_time, invalid_time):  
        find_devcie = device.find_one({'device_id': device_id})
        find_password = device_passwords.find_one({'password_id.id': password_id})
        if not find_devcie:
            return f'ERROR: không tìm thấy device'
        if not find_password:
            return f'ERROR: không tìm thấy password_id'
        else:
            # Gọi API của Tuya để đặt mật khẩu mới
            Db_update_device_password(device_id, password_id, password, effective_time, invalid_time)
            response = tuya_update_lock_password(device_id, password_id, password, effective_time, invalid_time)
            if response['success']:
                # Cập nhật thông tin mật khẩu mới vào cơ sở dữ liệu           
                return f'Đổi mật khẩu thành công cho khóa cửa {device_id} : {response["result"]}'
            else:
                return f'Đổi mật khẩu thất bại cho khóa cửa {device_id}: {response["msg"]}'
            
    # Xóa password
    def Model_delete_device_password(device_id, password_id):
        find_devcie = device.find_one({'device_id': device_id})
        find_password = device_passwords.find_one({'password_id.id': password_id})
        if not find_devcie:
            return f'ERROR: không tìm thấy device'
        if not find_password:
            return f'ERROR: không tìm thấy password_id'
        else:
            # Gọi API của Tuya để xóa mật khẩu tạm thời
            response = tuya_delete_lock_password(device_id, password_id)
            if response['success']:
                # Xóa thông tin mật khẩu khỏi cơ sở dữ liệu
                return f'Xóa mật khẩu thành công cho khóa cửa {device_id} : {response["result"]}'
            else:
                return f'Xóa mật khẩu thất bại cho khóa cửa {device_id}: {response["msg"]}'

# Hàm lấy status Password từ tuya
def Model_get_status_device_password(device_id, password_id):
    # Gọi API của tuya để lấy trạng thái  
    response = tuya_get_password_status(device_id, password_id)
    if response['success']:
        # Trả về trạng thái mật khẩu
        return f'{response["result"]["phase"]}'
    else:
        return f'Error : {response["msg"]}' 



class DeviceLog:

    @staticmethod
    # Hàm Lấy Logs
    def Model_get_device_logs(devId):
        find_device_log = device_logs.find({'device_id': devId})
        if not find_device_log:
            return f'ERROR: không tìm thấy device'
        else:
            return Db_get_device_logs(devId)
        






#####################################
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
    
# Hàm chụp ảnh từ Tuya
def Model_capture_an_image(device_id):
    # Gọi API của Tuya để chụp ảnh
    response = tuya_capture_an_image(device_id)
    if response['success']:
        return f'{response["result"]}'
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
    
# Hàm lấy nhật ký thiết bị từ Tuya 2
def Model_get_device_logs_Tuya_2(devId, start_time, end_time):
    # Gọi API của Tuya để lấy log
    response = tuya_get_device_logs_Tuya_2(devId, start_time, end_time)
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




