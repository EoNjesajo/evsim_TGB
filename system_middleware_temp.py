import copy


from telegram.ext import Updater

from system_simulator import SystemSimulator
#from system_database import SystemDatabase
from Agent import Agent
from Game_manager import *
from command_list import *
from system_errortime import SystemErrorTime
import pandas as pd
from datetime import datetime, timedelta

from threading import Thread

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult


class SystemMiddleware():

    updater = Updater( token='5270412803:AAHU6RCPczvA_lBW1lgiVvFKcZiSABysGvs', use_context=True )  
    bot = updater.bot

    simulator = SystemSimulator()
    
    method_list = {}

    agents = {}

    simulators = {}
    name = set()
    mode = "REAL_TIME" #'VIRTUAL_TIME'

    CONNECTION_STRING = "HostName=wonshub.azure-devices.net;DeviceId=maze;SharedAccessKey=wpIMrKDXJYx2s51+3DQQp2YcxxtJR6M5+/eb02vSexU="
    
    IOTHUB_CONNECTION_STRING = "HostName=wonshub.azure-devices.net;SharedAccessKeyName=serviceAndRegistryRead;SharedAccessKey=Hx96nI5ZXPKa4xRT80nAA5hpgmYzwxZzO7vwl8sMChw="
    DEVICE_ID = "maze"

    iothub_registry_manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)


    @staticmethod
    def receive_message(message):
        command = vars(message)['data'].decode('utf-8').split()
        chat_id = vars(message)['message_id']
        
        SystemMiddleware.handler(chat_id = int(chat_id), message = command)

    @staticmethod
    def handler(chat_id=None, message=None):
        try : 
            method = SystemMiddleware.method_list[message[0]]
            if message[0]=='start':
                text = method(chat_id, message[1])
            else :
                if chat_id in SystemMiddleware.agents.keys():
                    text = method(chat_id)
        except :
            if chat_id in SystemMiddleware.agents.keys():
                method = SystemMiddleware.command
                text = method(chat_id, message)