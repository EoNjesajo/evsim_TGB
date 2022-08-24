
import telegram
from telegram.ext import Updater
from telegram import ChatAction
from telegram.ext import CommandHandler,  CallbackQueryHandler
from telegram import InlineKeyboardButton as bt
from telegram import InlineKeyboardMarkup as mu

class Bot():
    updater = Updater( token='5270412803:AAHU6RCPczvA_lBW1lgiVvFKcZiSABysGvs', use_context=True )  
    dispatcher = updater.dispatcher

    def __init__(self):
        self.method_list = {
            'button' : self.button_task,
        }


    def button_task(self, update, context):
        chat_id = update.effective_chat.id
        task_buttons = [
            [
            bt( '1번 항목', callback_data='1' )
        ],  [
            bt( '2번 항목', callback_data='2' )
        ],  [
            bt( '3번 항목', callback_data='3' )
        ],  [
            bt( '4번 항목', callback_data='3' )
        ]
        ]
        reply_markup = mu( task_buttons )
        
        context.bot.send_message(
            chat_id=chat_id
            , text='작업을 선택해주세요.'
            , reply_markup=reply_markup
        )
    
    def behavior(self, data):
        if data == '1' :
            return '1번 수행'
        elif data == '2' :
            return '2번 수행'
        elif data == '3' :
            return '3번 수행'
        elif data == '4' :
            return '4번 수행'
    

    def button(self, update, context):
        chat_id = update.effective_user.id
        query = update.callback_query
        data = query.data
        
        context.bot.send_chat_action(
            chat_id=chat_id
            , action=ChatAction.TYPING
        )
        text = self.behavior(data)

        context.bot.edit_message_text(
            text=text
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
    
 
    def get_updater(self):
        for name in self.method_list.keys():
            self.dispatcher.add_handler(CommandHandler(name, self.method_list[name]))

        button_callback_handler = CallbackQueryHandler(self.button)  
        self.dispatcher.add_handler( button_callback_handler )
        return self.updater

game_bot = Bot()

updater = game_bot.get_updater()

updater.start_polling()
updater.idle()