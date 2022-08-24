from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
from maze import *



#왼쪽 상단 부터 (0,0)  F: 아래쪽 , R:오른쪽, B:위쪽, L : 왼쪽


class Gamemanager(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.set_name(engine_name)
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("agent")

        self.insert_output_port("gm")
        self.map = get_map("None")

    def ext_trans(self, port, msg):
        msg_list = []
        if port == "agent":  #에이전트에게 명령어 와 현재 위치를 받는다.
            print(f"[Gm][in] received")
            self.cancel_rescheduling()
            data = msg.retrieve()
            msg_list = data[0]
            aX = msg_list[0]
            aY = msg_list[1]
            print(f"[Gm] aX:{aX} aY:{aY}") # 현재 위치 출력
            self.Data = self.map_data(aX, aY) # 상하좌우 맵데이터 저장
            self._cur_state = "MOVE"

    def output(self):
        msg = SysMessage(self.get_name,
                         "agent")  #에이전트의 현재 위치를 기준으로 상하좌우 의 맵데이터를 보낸다
        msg.insert(self.Data)
        print(f"[Gm][out]{self.Data}") # 딕셔너리 형태로 출력
        return msg

    def int_trans(self):
        if self._cur_state == "MOVE":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"

    def map_data(self, j, i):

        map_data = {
            'R': self.map[i][j + 1],
            'L': self.map[i][j - 1],
            'F': self.map[i + 1][j],
            'B': self.map[i - 1][j]
        }
        return map_data

    def set_map(self, name):
        self.map = get_map(name)
