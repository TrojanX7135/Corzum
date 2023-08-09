from Models.models import Home, Room, Device, DevicePassword, DeviceLog
from Models.models import Model_get_device_status_pin, Model_get_device_logs_Tuya, Model_get_list_device_inCloud



# ______________________________________________[ HOME ] 
# Hàm tạo Home
def Ctrl_set_home(Name, address):
    try:
        return Home.Model_set_home(Name, address)
    except Exception as e:
        return f'Error: {e}'

# Hàm lấy danh sách các Home
def Ctrl_get_homes():
    return Home.Model_get_homes()

# Hàm cập nhật Home
def Ctrl_update_home(home_id, Name, address):
    try:
        return Home.Model_update_home(home_id, Name, address)
    except Exception as e:
        return f'Error: {e}'
    
# Hàm xóa Home
def Ctrl_delete_home(home_id):
    try:
        return Home.Model_delete_home(home_id)
    except Exception as e:
        return f'Error: {e}'



# ______________________________________________[ ROOM ] 
# Hàm tạo Room
def Ctrl_set_room(home_id, Name):
    try:
        return Room.Model_set_room(home_id, Name)
    except Exception as e:
        return f'Error: {e}'
    
# Hàm lấy danh sách các Room
def Ctrl_get_rooms():
    return Room.Model_get_rooms()

# Hàm lấy danh sách các Room dựa vào Home
def Ctrl_get_rooms_withHome(home_id):
    try:
        return Room.Model_get_rooms_withHome(home_id)
    except Exception as e:
        return f'Error: {e}'

# Hàm cập nhật Room
def Ctrl_update_room(room_id, home_id, Name):
    try:
        return Room.Model_update_room(room_id, home_id, Name)
    except Exception as e:
        return f'Error: {e}'
    
# Hàm xóa Room
def Ctrl_delete_room(room_id):
    try:
        return Room.Model_delete_room(room_id)
    except Exception as e:
        return f'Error: {e}'   



# ______________________________________________[ DEVICE ] 
# Hàm tạo device
def Ctrl_set_device(device_id, room_id, type, name):
    try:
        return Device.Model_set_device(device_id, room_id, type, name)
    except Exception as e:
        return f'Error: {e}' 

# Hàm lấy danh sách các Device 
def Ctrl_get_devices():
    return Device.Model_get_devices()

# Hàm lấy danh sách các Device dựa vào Room
def Ctrl_get_devices_withRoom(room_id):
    try:
        return Device.Model_get_devices_withRoom(room_id)
    except Exception as e:
        return f'Error: {e}'

# Hàm cập nhật Device
def Ctrl_update_device(device_id, room_id, name):
    try:
        return Device.Model_update_device(device_id, room_id, name)
    except Exception as e:
        return f'Error: {e}'
    
# Hàm xóa Device
def Ctrl_delete_device(device_id):
    try:
        return Device.Model_delete_device(device_id)
    except Exception as e:
        return f'Error: {e}'  



# ______________________________________________[ PASSWORD ] 
# Hàm đặt mật khẩu cho khóa cửa    
def Ctrl_set_device_password(device_id, Name, password, effective_time, invalid_time):
    try:
        return DevicePassword.Model_set_device_password(device_id, Name, password, effective_time, invalid_time)
    except Exception as e:
        return f'Error: {e}'

# Hàm tạo mật khẩu OTP cho khóa cửa
def Ctrl_set_device_password_OTP(device_id):
    try:
        return DevicePassword.Model_set_device_password_OTP(device_id)
    except Exception as e:
        return f'Error: {e}'          

# Hàm lấy danh sách Passwords
def Ctrl_get_device_passwords():
        return DevicePassword.Model_get_device_passwords()
    
# Hàm lấy danh sách Passwords dựa vào Device
def Ctrl_get_device_passwods_withDevice(device_id):
    try:
        return DevicePassword.Model_get_device_passwords_withDevice(device_id)
    except Exception as e:
        return f'Error: {e}'

# Hàm thay đổi mật khẩu cho một khóa cửa
def Ctrl_update_device_password(device_id, password_id, password, effective_time, invalid_time):  
    try:
        return DevicePassword.Model_update_device_password(device_id, password_id, password, effective_time, invalid_time)
    except Exception as e:
        return f'Error: {e}' 

# Hàm xóa mật khẩu tạm thời cho khóa cửa trên Cloud Tuay
def Ctrl_delete_device_password(device_id, password_id):
    try:
        return DevicePassword.Model_delete_device_password(device_id, password_id)
    except Exception as e:
        return f'Error: {e}'
    
# Hàm xóa password trong Db
def Ctrl_delete_password_inDatabase(password_id):
    try:
        return DevicePassword.Mode_delete_password_inDatabase(password_id)
    except Exception as e:
        return f'Error: {e}'  
        


# ______________________________________________[ LOG ]
# Hàm lấy log
def Ctrl_get_device_logs(devId):
    try:
        return DeviceLog.Model_get_device_logs(devId)
    except Exception as e:
        return f'Error: {e}'

# Hàm cập nhật logs    
def Ctrl_update_device_logs():
    try:
        return DeviceLog.Model_update_device_logs()
    except Exception as e:
        return f'Error: {e}'
    



# ______________________________________________[ API TUYA ]
# Hàm lấy trạng thái pin 
def Ctrl_get_device_status_pin(devId):
    try:
        return Model_get_device_status_pin(devId)
    except Exception as e:
        return f'Error: {e}'
    
# Hàm lấy logs device của Tuya
def Ctrl_get_device_logs_Tuya(device_id):
    try:
        return Model_get_device_logs_Tuya(device_id)
    except Exception as e:
        return f'Error: {e}'
    
# Hàm xử lý lấy list device có trong Cloud Tuya
def Ctrl_get_list_device_inCloud():
    try:
        return Model_get_list_device_inCloud()
    except Exception as e:
        return f'Error: {e}'


    



    



