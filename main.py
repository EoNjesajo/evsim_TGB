import time
from azure.iot.device import IoTHubDeviceClient
from system_middleware import *
import sys

CONNECTION_STRING = "HostName=wonshub.azure-devices.net;DeviceId=maze;SharedAccessKey=SxpLYy/45qe50l9C3ZoKoL7kSpBCqDrH7LfbeH/Tvb4="

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

SystemMiddleware.set_method()

while True : 
    try:
        # 메시지 핸들러를 클라이언트에 연결
        client.on_message_received = SystemMiddleware.receive_message
        while True:
            time.sleep(1000)
    except :
        sys.exit(0)
    # finally:
    #     client.shutdown()
