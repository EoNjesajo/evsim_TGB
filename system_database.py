import pymysql
from datetime import datetime
import numpy as np

class SystemDatabase():
    _user = {} #쳇아이디 : [이름, 현재 트라이 횟수, 현재 에러 횟수, 전체 트라이 횟수, 전체 에러 횟수]
    
    @staticmethod
    def register_user(chat_id, name):
        SystemDatabase._user[chat_id] = [name, 0, 0, 0, 0]

    @staticmethod
    def is_regame(chat_id) : 
        for i in range(1,3) :
            SystemDatabase._user[chat_id][i] = 0

    @staticmethod
    def enter_command(chat_id, command, code="Command success"):
        for i in range(1,5) : #1,3 / 2,4
            if i%2 == 0 and code == "Error" :
                SystemDatabase._user[chat_id][i] += 1
            elif i%2 != 0 : 
                SystemDatabase._user[chat_id][i] += 1
        conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')
        try:
            with conn.cursor() as cur:
                sql = 'INSERT INTO game_record (Agent, Chat_ID, Try_Time, Command, Result, Try, Error, Entire_Try, Entire_Error) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cur.execute(sql, ({SystemDatabase._user[chat_id][0]}, {chat_id}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {command}, {code}, 
                    {SystemDatabase._user[chat_id][1]},{SystemDatabase._user[chat_id][2]},{SystemDatabase._user[chat_id][3]},{SystemDatabase._user[chat_id][4]}))
            conn.commit() # 쿼리 실행 후에는 commit 시켜주기 - 데이터베이스에 반영
        finally:
            conn.close() # 사용 후 닫아주기

    @staticmethod
    def is_stopped(chat_id, map, x, y):
        map[y][x] = 5
        now_map = "{}".format(np.array(map))

        conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')
        try:
            with conn.cursor() as cur:
                sql = 'INSERT INTO map_record (Chat_ID, Try_Time, Map) VALUES(%s, %s, %s)'
                cur.execute(sql, ({chat_id}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {now_map}))
            conn.commit()
        finally:
            conn.close() 

    @staticmethod
    def is_arrived(chat_id):
        conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')
        try:
            with conn.cursor() as cur:
                sql = 'INSERT INTO ranking_record (Chat_ID, Agent, Arrive_Time, Try, Error) VALUES(%s, %s, %s, %s, %s)'
                cur.execute(sql, ({chat_id}, {SystemDatabase._user[chat_id][0]}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {SystemDatabase._user[chat_id][1]}, {SystemDatabase._user[chat_id][2]}))
                                        
                conn.commit() # 쿼리 실행 후에는 commit 시켜주기 - 데이터베이스에 반영
        finally:
                conn.close() # 사용 후 닫아주기

    

        

    
    