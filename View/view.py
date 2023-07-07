from fastapi import FastAPI, Form
from Controller.controller import get_all_locks
from Controller.controller import update_password
from Controller.controller import set_password
from Controller.controller import get_tickeyId
from Controller.controller import delete_password
from Controller.controller import history_lock

app = FastAPI()

# Route GET để lấy danh sách các khóa cửa từ cơ sở dữ liệu
@app.get('/get_locks')
async def get_locks():
    result = get_all_locks()
    return result

# Route POST để lấy tickeyId
@app.post('/get_tickeyId')
async def get_lock_tickeyId(device_id: str = Form(...)):
    result = get_tickeyId(device_id)
    return {'result': result}

# Route POST để đặt mật khẩu cho khóa cửa
@app.post('/set_password')
#lock_id ở đây là deviceID
async def set_lock_password(
        device_id: str = Form(...),
        Name: str = Form(...),
        password: str = Form(...),
        effective_time: int = Form(...),
        invalid_time: int = Form(...),
        password_type: str = Form(...),
        ticket_id: str = Form(...),
    ):
    result = set_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id)
    return {'result': result}

# Route PUT để thay đổi mật khẩu cho một khóa cửa
@app.put('/update_password')
async def update_lock_password(
        device_id: str = Form(...),
        Name: str = Form(...),
        password: str = Form(...),
        effective_time: int = Form(...),
        invalid_time: int = Form(...),
        password_type: str = Form(...),
        ticket_id: str = Form(...),
    ):
    result = update_password(device_id, Name, password, effective_time, invalid_time, password_type, ticket_id)
    return {'result': result}

# Route DELETE để xóa mật khẩu tạm thời cho khóa cửa
@app.delete('/delete_password')
async def delete_lock_password(device_id: str = Form(...)):
    result = delete_password(device_id)
    return {'result': result}

# Route GET để lấy nhật ký hoạt động của khóa cửa
@app.post('/get_history')
async def get_history_lock(device_id: str = Form(...)):
    result = history_lock(device_id)
    return {'result': result}


