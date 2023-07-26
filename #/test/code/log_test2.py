from tuya_connector import (
	TuyaOpenAPI,
	TuyaOpenPulsar,
	TuyaCloudPulsarTopic,
)

ACCESS_ID = "jgxfarjqssw7pwfmjqrm"
ACCESS_KEY = "e9a1f6b2dc3a402e9ec53a365e4b07d9"
API_ENDPOINT = "https://openapi.tuyaus.com"
MQ_ENDPOINT = "wss://mqe.tuyaus.com:8285/"
# ACCESS_ID = "88rhdtkuvwuwvnf9sqfg"
# ACCESS_KEY = "e3975867df94441195361e543bd45f85"
# API_ENDPOINT = "https://openapi.tuyaus.com"
# MQ_ENDPOINT = "wss://mqe.tuyaus.com:8285/"

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()
print("Connected to Tuya OpenAPI successfully")

# Call any API from Tuya
response = openapi.get("/v1.0/statistics-datas-survey", dict())

# Init Message Queue
open_pulsar = TuyaOpenPulsar(
	ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.TEST
)
# Add Message Queue listener
open_pulsar.add_message_listener(lambda msg: print(f"---\nexample receive: {msg}"))

# Start Message Queue
open_pulsar.start()
print("Connected to Tuya Message Queue successfully")

input()
# Stop Message Queue
open_pulsar.stop()