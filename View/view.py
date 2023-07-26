from fastapi import FastAPI, Form
from Controller.controller import Ctrl_get_locks
from Controller.controller import Ctrl_set_lock_password
from Controller.controller import Ctrl_update_lock_password
from Controller.controller import Ctrl_delete_lock_password
from Controller.controller import Ctrl_get_lock_history
from Controller.controller import Ctrl_get_lock_status
from Controller.controller import Ctrl_set_lock_OTP
from Controller.controller import Ctrl_get_password_status

app = FastAPI()

# Route GET để lấy danh sách các khóa cửa từ cơ sở dữ liệu
@app.get('/get_locks')
async def View_get_locks():
    result = Ctrl_get_locks()
    return {'result': result}


# Route POST để đặt mật khẩu cho khóa cửa
@app.post('/set_password')
#lock_id ở đây là deviceID
async def View_set_lock_password(
        device_id: str = Form(...),
        Name: str = Form(...),
        password: str = Form(...),
        effective_time: int = Form(...),
        invalid_time: int = Form(...)
    ):
    result = Ctrl_set_lock_password(device_id, Name, password, effective_time, invalid_time)
    return {'result': result}


# Route PUT để thay đổi mật khẩu cho một khóa cửa
@app.put('/update_password')
async def View_update_lock_password(
        device_id: str = Form(...),
        password_id: int = Form(...),
        password: str = Form(...),
        effective_time: int = Form(...),
        invalid_time: int = Form(...)
    ):
    result = Ctrl_update_lock_password(device_id, password_id, password, effective_time, invalid_time)
    return {'result': result}


# Route DELETE để xóa mật khẩu tạm thời cho khóa cửa
@app.delete('/delete_password')
async def View_delete_lock_password(
        device_id: str = Form(...),
        password_id: int = Form(...),
    ):
    result = Ctrl_delete_lock_password(device_id, password_id)
    return {'result': result}


# Route POST để lấy nhật ký hoạt động của khóa cửa
@app.post('/get_history')
async def View_get_lock_history(
        device_id: str = Form(...),
        page_no: int = Form(...),
        page_size: int = Form(...),
        start_time: int = Form(...),
        end_time: int = Form(...)
    ):
    result = Ctrl_get_lock_history(device_id, page_no, page_size, start_time, end_time)
    return {'result': result}


# Route POST để lấy trạng thái của khóa cửa
@app.post('/get_status')
async def View_get_lock_status(
        device_id: str = Form(...)
    ):
    result = Ctrl_get_lock_status(device_id)
    return {'result':result}


# Route POST để lấy mật khẩu OTP
@app.post('/set_OTP')
async def View_set_lock_OTP(
        device_id: str = Form(...)
    ):
    result = Ctrl_set_lock_OTP(device_id)
    return {'result':result}


# Route POST để lấy trạng thái mật khẩu
@app.post('/get_password_status')
async def View_get_password_status(
        device_id: str = Form(...),
        password_id: int = Form(...)
    ):
    result = Ctrl_get_password_status(device_id, password_id)
    return {'result':result}
