import logging
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
    TUYA_LOGGER,
)
from datetime import datetime
import json
import sqlite3


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

# #hàm lọc dữ liệu event,status
# def filter(value):
#     lst=[]
#     deviceId=value["devId"]
#     lst.append(deviceId)
#     productkey=value["productKey"]
#     lst.append(productkey)
#     code_battery=value["status"][0]["value"]
#     lst.append(code_battery)
#     code_action=value["status"][1]['code']
#     lst.append(code_action)
#     t = value["status"][1]['t']
#     timestamp=datetime.fromtimestamp(t/1000)
#     #print(timestamp)
#     lst.append(str(timestamp))
#     print(lst)
#     return lst

# def callback(text):
#     data = json.loads(text)  # chuyen tin nhan tu dang string sang dict
#     print(data)
#     obj1 = employee()
#     #create_database("Lock")
#     if filter(data)[0]:
#         obj1.infomations.Device_id=filter(data)[0]
#     if filter(data)[1]:
#         obj1.infomations.Product_Key=filter(data)[1]
#     if filter(data)[2]:
#         obj1.infomations.Battery_state=filter(data)[2]
#     if filter(data)[3]:
#         obj1.infomations.Action=filter(data)[3]
#     if filter(data)[4]:
#         obj1.infomations.Time=filter(data)[4]
#     #insert_database("Lock",obj1.infomations)

#     print(f"Device ID: {obj1.infomations.Device_id}")
#     print(f"Product Key: {obj1.infomations.Product_Key}")
#     print(f"Battery State: {obj1.infomations.Battery_state}")
#     print(f"Action: {obj1.infomations.Action}")
#     print(f"Time: {obj1.infomations.Time}")

def callback(text):
    data = json.loads(text) # chuyển đổi thông điệp từ chuỗi JSON sang đối tượng Python
    devId = data["bizData"]["devId"]
    battery_state = data["bizData"]["properties"][0]["code"]
    value = data["bizData"]["properties"][0]["value"]
    print(f"devId: {devId}")
    print(f"battery_state: {battery_state}")
    print(f"value: {value}")
    # phần còn lại của hàm callback



# Enable debug log
# TUYA_LOGGER.setLevel(logging.DEBUG)

# Init openapi and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Init Message Queue
open_pulsar = TuyaOpenPulsar(
    ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.TEST
)

# Add Message Queue listener
open_pulsar.add_message_listener(callback)

# open_pulsar.add_message_listener(lambda msg: callback(msg))
print()

# Start Message Queue
open_pulsar.start()

input()
# Stop Message Queue
open_pulsar.stop()
