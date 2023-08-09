from fastapi import FastAPI, Form
from Controller.controller import Ctrl_set_home, Ctrl_get_homes, Ctrl_update_home, Ctrl_delete_home
from Controller.controller import Ctrl_set_room, Ctrl_get_rooms, Ctrl_get_rooms_withHome, Ctrl_update_room, Ctrl_delete_room
from Controller.controller import Ctrl_set_device, Ctrl_get_devices, Ctrl_get_devices_withRoom, Ctrl_update_device, Ctrl_delete_device
from Controller.controller import Ctrl_set_device_password, Ctrl_set_device_password_OTP, Ctrl_get_device_passwords, Ctrl_get_device_passwods_withDevice, Ctrl_update_device_password, Ctrl_delete_device_password, Ctrl_delete_password_inDatabase 
from Controller.controller import Ctrl_get_device_logs, Ctrl_update_device_logs

from Controller.controller import Ctrl_get_device_status_pin
from Controller.controller import Ctrl_get_device_logs_Tuya
from Controller.controller import Ctrl_get_list_device_inCloud

app = FastAPI()


# ______________________________________________[ HOME ]
# Route POST để tạo Home
@app.post('/set_home')
async def View_set_home(
        Name: str = Form(...),
        address: str = Form(...)
    ):
    result = Ctrl_set_home(Name, address)
    return {'result': result}

# Route GET để lấy danh sách các Home
@app.get('/get_homes')
async def View_get_homes():
    result = Ctrl_get_homes()
    return {'result': result}

# Route PUT để cập nhật home
@app.put('/update_home')
async def View_update_home(
        home_id: str = Form(...),
        Name: str = Form(...),
        address: str = Form(...)
    ):
    result = Ctrl_update_home(home_id, Name, address)
    return {'result': result}

# Route DELETE để xóa home
@app.delete('/delete_home')
async def View_delete_home(
        home_id: str = Form(...)
    ):
    result = Ctrl_delete_home(home_id)
    return {'result': result}



# ______________________________________________[ ROOM ]
# Route POST để tạo Room
@app.post('/set_room')
async def View_set_room(
        home_id: str = Form(...),
        Name: str = Form(...),
    ):
    result = Ctrl_set_room(home_id ,Name)
    return {'result': result}

# Route GET để lấy danh sách các Room
@app.get('/get_rooms')
async def View_get_rooms():
    result = Ctrl_get_rooms()
    return {'result': result}

# Route POST để lấy danh sách các Room theo Home
@app.post('/get_rooms_withHome')
async def View_get_rooms_withHome(
       home_id: str = Form(...) 
    ):
    result = Ctrl_get_rooms_withHome(home_id)
    return {'result': result}

# Route PUT để cập nhật Room
@app.put('/update_room')
async def View_update_room(
        room_id: str = Form(...), 
        home_id: str = Form(...), 
        Name: str = Form(...)
    ):
    result = Ctrl_update_room(room_id, home_id, Name)
    return {'result': result}

# Route DELETE để xóa Room
@app.delete('/delete_room')
async def View_delete_room(
        room_id: str = Form(...)
    ):
    result = Ctrl_delete_room(room_id)
    return {'result': result}


# ______________________________________________[ DEVICE ]
# Route POST để tạo Device
# Không cần tạo device vì khi GET device device sẽ được tự động thêm

# Route GET để lấy danh sách các Device
@app.get('/get_devices')
async def View_get_devices():
    result = Ctrl_get_devices()
    return {'result': result}

# Route POST để lấy danh sách các Devices theo Room
@app.post('/get_devices_withRoom')
async def View_get_devices_withRoom(
       room_id: str = Form(...) 
    ):
    result = Ctrl_get_devices_withRoom(room_id)
    return {'result': result}

# Route PUT để cập nhật Device
@app.put('/update_device')
async def View_update_device(
        device_id: str = Form(...), 
        room_id: str = Form(...), 
        name: str = Form(...)
    ):
    result = Ctrl_update_device(device_id, room_id, name)
    return {'result': result}

# Route DELETE để xóa Device
@app.delete('/delete_device')
async def View_delete_device(
        device_id: str = Form(...)
    ):
    result = Ctrl_delete_device(device_id)
    return {'result': result}



# ______________________________________________[ PASSWORD ]
# Route POST để đặt mật khẩu cho khóa cửa
@app.post('/set_device_password')
#lock_id ở đây là deviceID
async def View_set_lock_password(
        device_id: str = Form(...),
        Name: str = Form(...),
        password: str = Form(...),
        effective_time: int = Form(...),
        invalid_time: int = Form(...)
    ):
    result = Ctrl_set_device_password(device_id, Name, password, effective_time, invalid_time)
    return {'result': result}

# Route POST để lấy mật khẩu OTP
@app.post('/set_OTP')
async def View_set_device_password_OTP(
        device_id: str = Form(...)
    ):
    result = Ctrl_set_device_password_OTP(device_id)
    return {'result':result}

# Route GET để lấy danh sách password
@app.get('/get_device_passwords')
async def View_get_device_passwords():
    result = Ctrl_get_device_passwords()
    return {'result': result}

# Route POST để lấy danh sách Password theo Device
@app.post('/get_device_passwods_withDevice')
async def View_get_device_passwods_withDevice(
       device_id: str = Form(...) 
    ):
    result = Ctrl_get_device_passwods_withDevice(device_id)
    return {'result': result}

# Route PUT để thay đổi mật khẩu cho một khóa cửa
@app.put('/update_device_password')
async def View_update_device_password(
        device_id: str = Form(...),
        password_id: int = Form(...),
        password: str = Form(...),
        effective_time: int = Form(...),
        invalid_time: int = Form(...)
    ):
    result = Ctrl_update_device_password(device_id, password_id, password, effective_time, invalid_time)
    return {'result': result}

# Route DELETE để xóa mật khẩu tạm thời cho khóa cửa trong Cloud Tuya
@app.delete('/delete_device_password_inCloudTuya')
async def View_delete_device_password(
        device_id: str = Form(...),
        password_id: int = Form(...),
    ):
    result = Ctrl_delete_device_password(device_id, password_id)
    return {'result': result}

# Route DELETE để xóa Password trong Database
@app.delete('/delete_device_password_inDatabase')
async def View_delete_password_inDatabase(
        password_id: int = Form(...)
    ):
    result = Ctrl_delete_password_inDatabase(password_id)
    return {'result': result}



# ______________________________________________[ LOG ]
# Route POST để lấy log theo device
@app.post('/get_device_logs')
async def View_get_device_logs(
        device_id: str = Form(...)
    ):
    result = Ctrl_get_device_logs(device_id)
    return {'result':result}

# Route PUT để cập nhật logs
@app.put('/update_device_logs')
async def View_update_device_logs():
    result = Ctrl_update_device_logs()
    return {'result':result}




# ______________________________________________[ API TUYA ]
# Route POST để lấy trạng thái pin của khóa cửa
@app.post('/get_status_pin')
async def View_get_device_status_pin(
        device_id: str = Form(...)
    ):
    result = Ctrl_get_device_status_pin(device_id)
    return {'result':result}


# # Route POST để lấy device logs từ Tuya
# @app.post('/get_device_logs_Tuya')
# async def View_get_device_logs_Tuya(
#         device_id: str = Form(...), 
#     ):
#     result = Ctrl_get_device_logs_Tuya(device_id)
#     return {'result': result}


# # Route GET để lấy list device có trong Cloud Tuya
# @app.post('/get_list_device_inCloud')
# async def View_get_list_device_inCloud():
#     result = Ctrl_get_list_device_inCloud()
#     return {'result': result} 


# Route POST để lấy trạng thái mật khẩu
# @app.post('/get_password_status')
# async def View_get_password_status(
#         device_id: str = Form(...),
#         password_id: int = Form(...)
#     ):
#     result = Ctrl_get_password_status(device_id, password_id)
#     return {'result':result}


