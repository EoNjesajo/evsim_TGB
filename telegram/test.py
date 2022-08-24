import time
from azure.iot.device import IoTHubDeviceClient
from system_bot import *
import sys

def receive_message(message):
        command = vars(message)['data'].decode('utf-8').split()
        chat_id = vars(message)['message_id']

#CONNECTION_STRING = "HostName=wonshub.azure-devices.net;DeviceId=maze;SharedAccessKey=wpIMrKDXJYx2s51+3DQQp2YcxxtJR6M5+/eb02vSexU="
CONNECTION_STRING = "HostName=wonshub.azure-devices.net;DeviceId=telegram;SharedAccessKey=iP1LHbNB4r1f/Ec7L75EzmuyBjBinIqVFuwPdBZkKuA="
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
while True : 
    try:
        # 메시지 핸들러를 클라이언트에 연결
        client.on_message_received = receive_message
        while True:
            time.sleep(1000)
    except :
        sys.exit(0)
    # finally:
    #     client.shutdown()