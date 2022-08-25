from telegram.ext import Updater, Filters, MessageHandler
from telegram import ChatAction
from telegram import InlineKeyboardButton as bt
from telegram import InlineKeyboardMarkup as mu

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.device import IoTHubDeviceClient

from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult


from threading import Thread

import sys
import time

class SystemBot():
    updater = Updater( token='5270412803:AAHU6RCPczvA_lBW1lgiVvFKcZiSABysGvs', use_context=True )  
    bot = updater.bot
    dispatcher = updater.dispatcher

    HUB_CONNECTION_STRING = "HostName=wonshub.azure-devices.net;SharedAccessKeyName=serviceAndRegistryRead;SharedAccessKey=Hx96nI5ZXPKa4xRT80nAA5hpgmYzwxZzO7vwl8sMChw="
    DEVICE_ID = "maze"

    iothub_registry_manager = IoTHubRegistryManager(HUB_CONNECTION_STRING)


    method_list = {}

    @staticmethod
    def send_message_to_cloud(chat_id, message):
        try:
            if message in SystemBot.method_list.keys() :
                SystemBot.method_list[message](chat_id, message)
            registry_manager = IoTHubRegistryManager(SystemBot.HUB_CONNECTION_STRING)
            props={}
            props.update(messageId = chat_id)
            registry_manager.send_c2d_message(SystemBot.DEVICE_ID, message, properties=props)
            query_spec = QuerySpecification(query="SELECT tags FROM devices WHERE is_defined(tags.map)")
            query_result = SystemBot.iothub_registry_manager.query_iot_hub(query_spec, None, 100)
            for twin in query_result.items:
                data_dic  = eval(str(twin))
            if message == 'location' or message == 'simulation':
                SystemBot.exec_non_block_send_photo(chat_id,visualize_map(chat_id, data_dic['tags']['map']))
            # else : 
            #     SystemBot.exec_non_block_send_message(chat_id, data_dic['tags']['recent_messages'])

        except Exception as ex:
            print ( "Unexpected error {0}" % ex )
            return
        except KeyboardInterrupt:
            print ( "IoT Hub C2D Messaging service stopped" )


    @staticmethod
    def handler(update, context):
        chat_id = str(update.effective_chat.id)
        message = update.message.text
        SystemBot.send_message_to_cloud(chat_id, message)

    @staticmethod
    def map_button_task(chat_id, message):
        task_buttons = [
            [
            bt( '1', callback_data='1' )
            , bt( '2', callback_data='2' )
        ],  [
            bt( '3', callback_data='3' )
            , bt( '4', callback_data='4' )
        ],  [
            bt( '5', callback_data='5' )
            , bt( '6', callback_data='6' )
        ],  [
            bt( '7', callback_data='7' )
            , bt( '8', callback_data='8' )
        ]  ]
        reply_markup = mu( task_buttons )
        
        SystemBot.bot.send_message(
            chat_id=chat_id
            , text='맵을 선택해주세요.'
            , reply_markup=reply_markup
        )

    @staticmethod
    def command_button_task(chat_id, message):
        task_buttons = [
            [
            bt( 'Back', callback_data='B' )
        ],  [
            bt( 'Left', callback_data='L' )
            , bt( 'Right', callback_data='R' )
        ],  [
            bt( 'Front', callback_data='F' )
  
        ]]
        reply_markup = mu( task_buttons )
        
        SystemBot.bot.send_message(
            chat_id=chat_id
            , text='작업을 선택해주세요.'
            , reply_markup=reply_markup
        )
    
    @staticmethod
    def button(update, context):
        chat_id = update.effective_user.id
        query = update.callback_query
        message = 'button ' + query.data
        print(message)
        
        SystemBot.bot.send_chat_action(
            chat_id=chat_id
            , action=ChatAction.TYPING
        )
        SystemBot.send_message(chat_id, message)

    @staticmethod 
    def send_message(chat_id, text):
        SystemBot.bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    def send_photo(chat_id, path):
        SystemBot.bot.send_photo(chat_id, open(path,'rb'))

    @staticmethod
    def exec_non_block_send_message(chat_id, text_list):
        for text in text_list : 
            p = Thread(target=SystemBot.send_message, args=(chat_id, text))
            p.start()

    @staticmethod
    def exec_non_block_send_photo(chat_id, path):
        p = Thread(target=SystemBot.send_photo, args=(chat_id, path))
        p.start()

    @staticmethod
    def get_updater():
        SystemBot.method_list = {
            'map' : SystemBot.map_button_task,
            'button' : SystemBot.command_button_task,
        }
 

        handler = MessageHandler(Filters.text, SystemBot.handler)
        SystemBot.dispatcher.add_handler(handler)

        return SystemBot.updater

