from fastapi import FastAPI, Form
from Controller.controller import Ctrl_set_home, Ctrl_get_homes, Ctrl_update_home
from Controller.controller import Ctrl_set_room, Ctrl_get_rooms, Ctrl_update_room
from Controller.controller import Ctrl_set_device, Ctrl_get_devices, Ctrl_update_device
from Controller.controller import Ctrl_set_device_password, Ctrl_set_device_password_OTP, Ctrl_get_device_passwords, Ctrl_update_device_password, Ctrl_delete_device_password 
from Controller.controller import Ctrl_get_device_logs

from Controller.controller import Ctrl_get_device_status_pin
from Controller.controller import Ctrl_capture_an_image
from Controller.controller import Ctrl_get_device_logs_Tuya, Ctrl_get_device_logs_Tuya_2
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
        Address: str = Form(...)
    ):
    result = Ctrl_update_home(home_id, Name, Address)
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

# Route PUT để cập nhật Room
@app.put('/update_room')
async def View_update_room(
        room_id: str = Form(...), 
        home_id: str = Form(...), 
        Name: str = Form(...)
    ):
    result = Ctrl_update_room(room_id, home_id, Name)
    return {'result': result}


# ______________________________________________[ DEVICE ]
# Route POST để tạo Device
@app.post('/set_device')
async def View_set_devce(
        id: str = Form(...),
        room_id: str = Form(...),
        type: str = Form(...),
    ):
    result = Ctrl_set_device(id, room_id ,type)
    return {'result': result}

# Route GET để lấy danh sách các Device
@app.get('/get_devices')
async def View_get_devices():
    result = Ctrl_get_devices()
    return {'result': result}

# Route PUT để cập nhật Device
@app.put('/update_device')
async def View_update_device(
        Db_device_id: str = Form(...), 
        room_id: str = Form(...), 
        type: str = Form(...)
    ):
    result = Ctrl_update_device(Db_device_id, room_id, type)
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

# Route GET để lấy danh sách các khóa cửa từ cơ sở dữ liệu
@app.get('/get_device_passwords')
async def View_get_device_passwords():
    result = Ctrl_get_device_passwords()
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

# Route DELETE để xóa mật khẩu tạm thời cho khóa cửa
@app.delete('/delete_device_password')
async def View_delete_device_password(
        device_id: str = Form(...),
        password_id: int = Form(...),
    ):
    result = Ctrl_delete_device_password(device_id, password_id)
    return {'result': result}



# ______________________________________________[ LOG ]
# Route POST để lấy log theo device
@app.post('/get_device_logs')
async def View_get_device_logs(
        devId: str = Form(...)
    ):
    result = Ctrl_get_device_logs(devId)
    return {'result':result}



# ______________________________________________[ API TUYA ]
# Route POST để lấy trạng thái pin của khóa cửa
@app.post('/get_status_pin')
async def View_get_device_status_pin(
        device_id: str = Form(...)
    ):
    result = Ctrl_get_device_status_pin(device_id)
    return {'result':result}


# Route POST để chụp ảnh
@app.post('/capture_an_image')
async def View_capture_an_image(
        device_id: str = Form(...)
    ):
    result = Ctrl_capture_an_image(device_id)
    return {'result': result}

# Route POST để lấy device logs từ Tuya
@app.post('/get_device_logs_Tuya')
async def View_get_device_logs_Tuya(
        device_id: str = Form(...), 
    ):
    result = Ctrl_get_device_logs_Tuya(device_id)
    return {'result': result}

# Route POST để lấy device logs từ Tuya 2
@app.post('/get_device_logs_Tuya_2')
async def View_get_device_logs_Tuya_2(
        devId: str = Form(...),
        start_time: int = Form(...),
        end_time: int = Form(...) 
    ):
    result = Ctrl_get_device_logs_Tuya_2(devId, start_time, end_time)
    return {'result': result}

# Route GET để lấy list device có trong Cloud Tuya
@app.get('/get_list_device_inCloud')
async def View_get_list_device_inCloud():
    result = Ctrl_get_list_device_inCloud
    return {'result': result} 


# Route POST để lấy trạng thái mật khẩu
# @app.post('/get_password_status')
# async def View_get_password_status(
#         device_id: str = Form(...),
#         password_id: int = Form(...)
#     ):
#     result = Ctrl_get_password_status(device_id, password_id)
#     return {'result':result}


