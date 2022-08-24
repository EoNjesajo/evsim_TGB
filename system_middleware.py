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
    #database = SystemDatabase()
    
    method_list = {}

    agents = {}

    simulators = {}
    name = set()
    #mode = 'VIRTUAL_TIME'
    mode = "REAL_TIME"

    CONNECTION_STRING = "HostName=wonshub.azure-devices.net;DeviceId=maze;SharedAccessKey=wpIMrKDXJYx2s51+3DQQp2YcxxtJR6M5+/eb02vSexU="
    
    IOTHUB_CONNECTION_STRING = "HostName=wonshub.azure-devices.net;SharedAccessKeyName=serviceAndRegistryRead;SharedAccessKey=Hx96nI5ZXPKa4xRT80nAA5hpgmYzwxZzO7vwl8sMChw="
    DEVICE_ID = "maze"

    iothub_registry_manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)

    @staticmethod
    def setting(chat_id, user) :
        sim_name = user + '_sim'
        gm_name = user + '_gm'

        gm = Gamemanager(0, Infinite, gm_name, sim_name)
        agent = Agent(0, Infinite, user, sim_name, chat_id, 1, 1, SystemMiddleware.bot, gm.map)
        SystemMiddleware.agents[chat_id] = [agent, gm, user]


        SystemSimulator.register_engine(sim_name, SystemMiddleware.mode, 0.01) 
        SystemSimulator.get_engine(sim_name).insert_input_port("command")

        SystemSimulator.get_engine(sim_name).register_entity(SystemMiddleware.agents[chat_id][0]) #agent
        SystemSimulator.get_engine(sim_name).register_entity(SystemMiddleware.agents[chat_id][1]) #gm

        SystemSimulator.get_engine(sim_name).coupling_relation(None, "command", SystemMiddleware.agents[chat_id][0], "command")
        SystemSimulator.get_engine(sim_name).coupling_relation(SystemMiddleware.agents[chat_id][0], "gm", SystemMiddleware.agents[chat_id][1], "agent")
        SystemSimulator.get_engine(sim_name).coupling_relation(SystemMiddleware.agents[chat_id][1], "agent", SystemMiddleware.agents[chat_id][0], "gm")

    @staticmethod
    def start(chat_id, user):
        errortime = SystemErrorTime()
        errortime.start_time()
        if chat_id in SystemMiddleware.agents.keys() : 
            print("start error")
            errortime.time_interval()
            return ["게임이 이미 진행 중입니다."]
        elif user in SystemMiddleware.name:
            errortime.time_interval()
            return ["이미 존재하는 닉네임입니다."]
        else : 
            SystemMiddleware.name.add(user)
            exec("{} = Command_list()".format(user),globals())
            SystemMiddleware.setting(chat_id, user)
            #SystemMiddleware.database.register_user(chat_id, user)
            
#         return ["""미로 게임
# /logout : 게임을 종료합니다.
# /regame : 시작 지점으로 돌아갑니다.
# /map : 맵 리스트를 가져옵니다.
# /button : 이동 동작 리스트에 이동 동작을 추가하는 버튼을 출력합니다.
# /command 명령어 : 명령어에 따라 리스트에 이동 동작을 추가합니다.
# /location : 캐릭터의 현재 위치를 출력합니다.
# /list : 추가한 이동 동작 리스트를 출력합니다.
# /clear : 가장 마지막 이동 동작을 지웁니다.
# /reset : 이동 동작 리스트를 초기화합니다.
# /simulation : 추가한 이동 동작 리스트에 따라 동작을 수행합니다."""]
            SystemMiddleware.exec_non_block_send_message(chat_id, ["{}님이 게임을 시작했습니다.".format(user), 
            """미로 게임
/logout : 게임을 종료합니다.
/regame : 시작 지점으로 돌아갑니다.
/map : 맵 리스트를 가져옵니다.
/button : 이동 동작 리스트에 이동 동작을 추가하는 버튼을 출력합니다.
/command 명령어 : 명령어에 따라 리스트에 이동 동작을 추가합니다.
/location : 캐릭터의 현재 위치를 출력합니다.
/list : 추가한 이동 동작 리스트를 출력합니다.
/clear : 가장 마지막 이동 동작을 지웁니다.
/reset : 이동 동작 리스트를 초기화합니다.
/simulation : 추가한 이동 동작 리스트에 따라 동작을 수행합니다."""])
    @staticmethod
    def logout(chat_id):
        errortime = SystemErrorTime()
        errortime.start_time()
        if not chat_id in SystemMiddleware.agents.keys() :
            print("logout error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])
        user = SystemMiddleware.agents[chat_id][2]
        del SystemMiddleware.agents[chat_id]
        exec('del {}'.format(user),globals())
        SystemMiddleware.name.remove(user)
        SystemSimulator.remove_engine(user + '_sim')
        
        SystemMiddleware.exec_non_block_send_message(chat_id, ["{}님이 게임을 종료했습니다.".format(user)])
        
    @staticmethod
    def regame(chat_id):
        errortime = SystemErrorTime()
        errortime.start_time()
        if not chat_id in SystemMiddleware.agents.keys() :
            print("regame error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])

        else : 
            user = SystemMiddleware.agents[chat_id][2]
            SystemMiddleware.agents[chat_id][0].ix = 1
            SystemMiddleware.agents[chat_id][0].iy = 1
            for i in ['R','L','F','B'] :
                globals()[user].turn(i,'')
            exec("{}.cm_list.clear()".format(user))
            #SystemMiddleware.database.is_regame(chat_id)
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임을 다시 시작합니다."])

    @staticmethod
    def contest(chat_id) :     
        errortime = SystemErrorTime()
        errortime.start_time()
        user = SystemMiddleware.agents[chat_id][2]
        if not chat_id in SystemMiddleware.agents.keys() :
            print("contest error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])
        SystemMiddleware.agents[chat_id][1].set_map('contest')
        SystemMiddleware.agents[chat_id][0].change_map(1,1,SystemMiddleware.agents[chat_id][1].map)
        for i in ['R','L','F','B'] :
            globals()[user].turn(i,'')
        exec("{}.cm_list.clear()".format(user))
        SystemMiddleware.exec_non_block_send_message(chat_id, ["대회 맵으로 설정되었습니다."])

    
    @staticmethod
    def button(chat_id, data):
        user = SystemMiddleware.agents[chat_id][2]
        if data in ['B','L','R','F'] :
            exec('{}.{}()'.format(user, data))
            #SystemMiddleware.database.enter_command(chat_id, "button {}".format(data))
            return '명령이 추가되었습니다.'
        elif data in ['1','2','3','4','5','6','7','8'] :
            SystemMiddleware.agents[chat_id][1].set_map(data)
            SystemMiddleware.agents[chat_id][0].change_map(1,1,SystemMiddleware.agents[chat_id][1].map)
            SystemMiddleware.agents[chat_id][0].ix = 1
            SystemMiddleware.agents[chat_id][0].iy = 1
            for i in ['R','L','F','B'] :
                globals()[user].turn(i,'')
            exec("{}.cm_list.clear()".format(user))
            return '맵이 변경되었습니다.'
        else :
            exec(data)
            #SystemMiddleware.database.enter_command(chat_id, data, "Command success")
            return "다음의 명령을 추가합니다. : {} ".format(data)

    @staticmethod
    def command(chat_id , command_list):
        errortime = SystemErrorTime()
        errortime.start_time()
        if not chat_id in SystemMiddleware.agents.keys() :
            print("command error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])
        try : 
            com = command_list[0]
        except :
            SystemMiddleware.exec_non_block_send_message(chat_id, ["명령을 입력해주세요."])
        else :
            for i in range(1,len(command_list)):
                com = com + ' '+ command_list[i]
            try :
                exec(com)
            except Exception :
                #SystemMiddleware.database.enter_command(chat_id, com, "Error")
                print("command error")
                errortime.time_interval()
                SystemMiddleware.exec_non_block_send_message(chat_id, ["잘못된 명령입니다."])
            else :
                #SystemMiddleware.database.enter_command(chat_id, com, "Command success")
                #next_com = SystemMiddleware.next_command(chat_id, command_list)
                SystemMiddleware.exec_non_block_send_message(chat_id, ["다음의 명령을 추가합니다. : {} ".format(com)])

    @staticmethod
    def list(chat_id):
        errortime = SystemErrorTime()
        errortime.start_time()
        if not chat_id in SystemMiddleware.agents.keys() :
            print("list error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])

        user = SystemMiddleware.agents[chat_id][2]
        exec("command = {}.cm_list".format(user), None, locals())
        SystemMiddleware.exec_non_block_send_message(chat_id, ["[{}]".format(locals()['command'])])

    @staticmethod
    def location(chat_id):
        errortime = SystemErrorTime()
        errortime.start_time()
        if not chat_id in SystemMiddleware.agents.keys() :
            print("location error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])
        agent = SystemMiddleware.agents[chat_id][0]
        size = len(agent.map)
        map =  copy.deepcopy(agent.map)
        Fog = [[8 for col in range(size)] for row in range(size)]
        for j in range(agent.ix-1, agent.ix+2):
            for i in range(agent.iy-1, agent.iy+2):
                Fog[i][j] = map[i][j]
        Fog[agent.iy][agent.ix] = 5

        tags = {'map' : Fog}
        twin = SystemMiddleware.iothub_registry_manager.get_twin(SystemMiddleware.DEVICE_ID)
        twin_patch = Twin(tags=tags, properties= TwinProperties(desired={'power_level' : 1}))
        twin = SystemMiddleware.iothub_registry_manager.update_twin(SystemMiddleware.DEVICE_ID, twin_patch, twin.etag)
        
        #return Fog

        #SystemMiddleware.exec_non_block_send_photo(chat_id,visualize_map(chat_id, Fog))

    
    @staticmethod
    def reset(chat_id):
        errortime = SystemErrorTime()
        errortime.start_time()
        if not chat_id in SystemMiddleware.agents.keys() :
            print("reset error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])
        user = SystemMiddleware.agents[chat_id][2]
        exec("{}.cm_list.clear()".format(user))
        SystemMiddleware.exec_non_block_send_message(chat_id, ["명령 초기화 완료"])

    @staticmethod
    def clear(chat_id):
        errortime = SystemErrorTime()
        errortime.start_time()
        if not chat_id in SystemMiddleware.agents.keys() :
            print("clear error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])
        user = SystemMiddleware.agents[chat_id][2]
        exec("del {}.cm_list[len({}.cm_list)-1]".format(user, user))
        SystemMiddleware.exec_non_block_send_message(chat_id, ["명령 지우기 완료"])

    @staticmethod
    def simulation(chat_id):
        errortime = SystemErrorTime()
        errortime.start_time()
        if not chat_id in SystemMiddleware.agents.keys() :
            print("simulation error")
            errortime.time_interval()
            SystemMiddleware.exec_non_block_send_message(chat_id, ["게임이 시작되지 않았습니다."])
        sims = []
        id_list = []

        # if len(commend) > 0 :
        #     if commend[0] == 'all' :
        #         id_list = list(SystemMiddleware.agents.keys())
        # else :
        id_list.append(chat_id)

        for id in id_list:
            user = SystemMiddleware.agents[id][2]
            sims.append(user+'_sim')
            agent = SystemMiddleware.agents[id][0]
            if globals()[user].get_blk('R') != None:
                agent.set_ifMove('R', globals()[user].get_blk('R')) # R이 막혀있을때 이동할 방향 셋팅
            if globals()[user].get_blk('L') != None:
                agent.set_ifMove('L', globals()[user].get_blk('L')) # L이 막혀있을때 이동할 방향 셋팅
            if globals()[user].get_blk('F') != None:
                agent.set_ifMove('F', globals()[user].get_blk('F')) # F이 막혀있을때 이동할 방향 셋팅
            if globals()[user].get_blk('B') != None:
                agent.set_ifMove('B', globals()[user].get_blk('B')) # B이 막혀있을때 이동할 방향 셋팅
            exec("command = {}.get_command()".format(user),None,locals())
            SystemSimulator.get_engine(user+'_sim').insert_external_event("command", locals()["command"])
            
        if SystemMiddleware.mode == "VIRTUAL_TIME":
            SystemSimulator.exec_non_block_simulate(sims)
        else : 
            SystemSimulator.exec_non_block_simulate(sims, len(locals()["command"])*1.2)
        print('test')
        Fog = SystemMiddleware.location(chat_id)
        return Fog
        


    @staticmethod
    def next_command(chat_id, input):
        current_com = []
        next_com = []

        game_record = pd.read_csv('/home/wons/evsim_chat/game_record.csv')

        game_record = game_record[game_record['Result'] == 'Command success']
        game_record = game_record[game_record['Chat_ID'] == chat_id]
        game_record = game_record[game_record['Agent'] == SystemMiddleware.agents[chat_id][2]]

        command = list(game_record.Command.values)
        for i in ['button R', 'button L', 'button F', 'button B'] :
            command = [word for word in command if word != i]
    
        for i in command :
            current_com.append([x for x in i.replace('\n','').split(' ') if x!=''])

        for i in range(len(current_com)) : 
            if input == current_com[i]:
                try :
                    next_com.append(current_com[i+1])
                except :
                    pass
        return next_com

    @staticmethod
    def find_command(game_record, id_try, chat_id, arrive_time, try_num) :
        user = game_record[game_record['Chat_ID'] == chat_id]
        user_command =list(user.Command.values)
        user_time = list(user.Try_Time.values)

        index = None
        arrive_time = datetime.strptime(arrive_time, '%Y-%m-%d %H:%M:%S')
        commands = []
        while(True):
            if str(arrive_time) in user_time :
                index = user_time.index(str(arrive_time))
                break
            arrive_time = arrive_time + timedelta(seconds=-1)
        for i in range(index-try_num+1, index+1):
            commands.append(user_command[i].replace(id_try[chat_id][2],'name'))

        return commands
    
    @staticmethod
    def levenshtein(seq1, seq2):
        size_x = len(seq1) + 1   
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y)) 
        for x in range(size_x): 
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y

        for x in range(1, size_x):  
            for y in range(1, size_y):  
                if seq1[x-1] == seq2[y-1]:  
                    matrix [x,y] = min(matrix[x-1, y] + 1, matrix[x-1, y-1], matrix[x, y-1] + 1 )
                else:
                    matrix [x,y] = min(matrix[x-1,y] + 1, matrix[x-1,y-1] + 1, matrix[x,y-1] + 1)
        return (matrix[size_x - 1, size_y - 1])  
            
    @staticmethod
    def check_cheater():
        ranking = pd.read_csv('/home/wons/evsim_chat/ranking_record.csv')
        game = pd.read_csv('/home/wons/evsim_chat/game_record.csv')
        cheaters = {}
        id_try = {}

        for chat_id in list(set(ranking.Chat_ID.values)) :
            user = ranking[ranking['Chat_ID'] == chat_id]
            try_min = 100
            min_time = None
            name = None
            try_num = list(user.Try.values)
            agent = list(user.Agent.values)
            arrive_time = list(user.Arrive_Time.values)
            for i in range(len(user.Try.values)) :
                if try_min > try_num[i] :
                    try_min = try_num[i] 
                    min_time = arrive_time[i]
                    name = agent[i]
            id_try[chat_id] = [try_min, min_time, name]

        for chat_id in id_try.keys() :
            suspect = ranking[ranking['Chat_ID'] != chat_id]
            suspect = suspect[suspect['Try'] == id_try[chat_id][0]]
            suspect_agents = list(suspect.Agent.values)
            suspect_ids = list(suspect.Chat_ID.values)
            suspect_times = list(suspect.Arrive_Time.values)

            cheater=[]

            user_command = SystemMiddleware.find_command(game, id_try, chat_id,id_try[chat_id][1],id_try[chat_id][0])

            for i in range(len(suspect_ids)):
                suspect_command = SystemMiddleware.find_command(game, id_try,suspect_ids[i],suspect_times[i],id_try[chat_id][0])
                cost = 0
                total = 0
                for j in range(len(user_command)):
                    cost += SystemMiddleware.levenshtein(user_command[j],suspect_command[j])
                    total += len(user_command)
                rate = 1-cost/total
                if 0.8 < rate :
                    #cheater += suspect_agents[i] + ", "
                    if id_try[suspect_ids[i]][0]==id_try[chat_id][0] and not suspect_agents[i] in cheater :
                        cheater.append(suspect_agents[i])
                
            cheaters['{}[{}]'.format(id_try[chat_id][2],id_try[chat_id][0])] = cheater
        
        text_list = []

        for user, cheater in cheaters.items():
            if len(cheater) !=0 :
                text_list.append(user + " : " + str(cheater))
        
        return text_list

##추가
    @staticmethod
    def set_method():
        SystemMiddleware.method_list = {
            'start' : SystemMiddleware.start,
            'logout' : SystemMiddleware.logout,
            'regame' : SystemMiddleware.regame,
            'contest' : SystemMiddleware.contest,
            'button' : SystemMiddleware.button,
            'location' : SystemMiddleware.location,
            'list' : SystemMiddleware.list,
            'clear' : SystemMiddleware.clear,
            'reset' : SystemMiddleware.reset,
            'simulation' : SystemMiddleware.simulation, 
            'check_cheater' : SystemMiddleware.check_cheater
        }

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
        # if message[0] == 'location' or message[0] == 'simulation': 
        #     tags = {'map' : text}
        #     twin = SystemMiddleware.iothub_registry_manager.get_twin(SystemMiddleware.DEVICE_ID)
        #     twin_patch = Twin(tags=tags, properties= TwinProperties(desired={'power_level' : 1}))
        #     twin = SystemMiddleware.iothub_registry_manager.update_twin(SystemMiddleware.DEVICE_ID, twin_patch, twin.etag)
        # else :
        #     tags = {'recent_messages' : text}

    


    @staticmethod
    def receive_message(message):
        command = vars(message)['data'].decode('utf-8').split()
        chat_id = vars(message)['message_id']
        
        SystemMiddleware.handler(chat_id = int(chat_id), message = command)

        

    @staticmethod 
    def send_message(chat_id, text):
        SystemMiddleware.bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    def send_photo(chat_id, path):
        SystemMiddleware.bot.send_photo(chat_id, open(path,'rb'))

    @staticmethod
    def exec_non_block_send_message(chat_id, text_list):
        for text in text_list : 
            p = Thread(target=SystemMiddleware.send_message, args=(chat_id, text))
            p.start()

    @staticmethod
    def exec_non_block_send_photo(chat_id, path):
        p = Thread(target=SystemMiddleware.send_photo, args=(chat_id, path))
        p.start()