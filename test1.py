from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

import asyncio


async def message_handler(message):
    print("the data in the message received was ")
    print(message.data)
    print("custom properties are")
    print(message.custom_properties)

async def sendmassge() :

    CONNECTION_STRING = "HostName=wonshub.azure-devices.net;DeviceId=maze;SharedAccessKey=wpIMrKDXJYx2s51+3DQQp2YcxxtJR6M5+/eb02vSexU="

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    await client.connect()


    message = Message("telemetry message")
    message.message_id = "message id"
    message.correlation_id = "correlation id"

    message.custom_properties["property"] = "property_value"
    await client.send_message(message)
    ###

    
    client.on_message_received = message_handler

