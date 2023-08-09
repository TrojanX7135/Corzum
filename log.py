import logging
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
    TUYA_LOGGER,
)
from datetime import datetime
import json
from Database.db import Db_set_device_logs
from Database.db import Db_update_device_pin
from Database.db import Db_update_log
from Tuya.tuya import tuya_get_device_logs_Tuya, tuya_get_list_device_inCloud


#tham số Tuya project
ACCESS_ID = "jgxfarjqssw7pwfmjqrm"
ACCESS_KEY = "e9a1f6b2dc3a402e9ec53a365e4b07d9"
API_ENDPOINT = "https://openapi.tuyaus.com"
MQ_ENDPOINT = "wss://mqe.tuyaus.com:8285/"

class employee:
    def __init__(self):
        self.infomations = information()

class information:
    def __init__(self):
        self.Device_Id = ""
        self.Product_Key= ""
        self.Battery_state=""
        self.Action=""
        self.Time=""


def callback(text):
    data = json.loads(text) # chuyển đổi thông điệp từ chuỗi JSON sang đối tượng Python
    devId = data["bizData"]["devId"]
    print(f"devId: {devId}")
    time = data["bizData"]["properties"][0]["time"]
    timestamp = datetime.fromtimestamp(time/1000)
    formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    properties = data["bizData"]["properties"]
    for prop in properties:
        if prop["code"] == "battery_state":
            battery_state = prop["value"]
            print(f"battery_state: {battery_state}")
        if prop["code"] != "battery_state":
            Action = prop["code"]
            value = prop["value"]
            print(f"Action : {Action} : {value}")
            Db_set_device_logs(devId, Action, value, formatted_time)
    print(f"time: {formatted_time}")
    print("==========================================================")
    Db_update_device_pin(devId, battery_state)



# Enable debug log
# TUYA_LOGGER.setLevel(logging.DEBUG)

# Init openapi and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()
# Mỗi lần chạy server sẽ gọi cập nhật logs
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
    print('<<< updated logs >>>') 
except Exception as e:
    print(f'Error: {e}')
print('__________________________________________________________')
print('')      
    

# Init Message Queue
open_pulsar = TuyaOpenPulsar(
    ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.PROD
)

# Add Message Queue listener
open_pulsar.add_message_listener(callback)


# Start Message Queue
open_pulsar.start()

input()
# Stop Message Queue
open_pulsar.stop()
