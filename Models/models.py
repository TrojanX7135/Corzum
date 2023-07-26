from Database.db import locks

class Lock:
    # Khởi tạo đối tượng Lock"
    def __init__(self, device_id):
        self.device_id = device_id

    # Hàm lấy thông tin của một khóa cửa từ cơ sở dữ liệu
    @staticmethod
    def get_lock(device_id):
        lock_data = locks.find_one({'device_id': device_id})
        if not lock_data:
            return None
        return Lock(
            lock_data['device_id'], 
            lock_data['Name'],
            lock_data['password'],
            lock_data['effective_time'],
            lock_data['invalid_time'],
            lock_data['password_type'],
            lock_data['password_id'],
        )
