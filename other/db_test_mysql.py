import pymysql

# # DATABASE 생성
# conn = pymysql.connect(
#     host='wonsdb', user='root', password='rlarlaths1#')

# try:
#     with conn.cursor() as cur:
#         sql = "CREATE DATABASE record_db"
#         cur.execute(sql)
#     conn.commit()
# finally:
#     conn.close()

# -----------------------------------------------------------------------

# # TABLE 생성
# conn = pymysql.connect(
#     host='wonsdb', user='root', password='rlarlaths1#', db='record_db')

# try:
#     with conn.cursor() as cur:
#         sql1 = """
#         CREATE TABLE game_record (
#             ID INT AUTO_INCREMENT PRIMARY KEY,
#             Agent TEXT NOT NULL,
#             Chat_ID BIGINT(10) NOT NULL,
#             Command TEXT NOT NULL,
#             Try_Time TEXT NOT NULL,
#             Result TEXT NOT NULL,
#             Try BIGINT(5) NOT NULL,
#             Error BIGINT(5) NOT NULL,
#             Entire_Try BIGINT(5) NOT NULL,
#             Entire_Error BIGINT(5) NOT NULL
#         )
#         """
#         sql2 = """
#         CREATE TABLE map_record (
#             ID INT AUTO_INCREMENT PRIMARY KEY,
#             Chat_ID BIGINT(10) NOT NULL,
#             Try_Time TEXT NOT NULL,
#             Map TEXT NOT NULL 
#         )
#         """
#         cur.execute(sql1)
#         cur.execute(sql2)
#         sql3 = """
#         CREATE TABLE ranking_record(
#             Chat_ID BIGINT(10) NOT NULL,
#             Agent TEXT NOT NULL,       
#             Arrive_Time TEXT NOT NULL,
#             Try BIGINT(5) NOT NULL,
#             Error BIGINT(5) NOT NULL
#         )
#         """
#         cur.execute(sql3)
#     conn.commit()
# finally:
#     conn.close()

# -----------------------------------------------------------------------

# # TABLE 삭제
# conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')

# try:
#     with conn.cursor() as cur:
#         sql1 = 'DROP TABLE game_record'
#         sql2 = 'DROP TABLE map_record'
#         sql3 = 'DROP TABLE ranking_record'
#         cur.execute(sql1)
#         cur.execute(sql2)
#         cur.execute(sql3)
#     conn.commit()
# finally:
#     conn.close()

# -----------------------------------------------------------------------

# # /command 결과 테이블 출력
# conn = pymysql.connect(host="wonsdb", user="root", password="rlarlaths1#", db="record_db")

# cur = conn.cursor()

# cur.execute("SELECT * FROM game_record")

# row = cur.fetchall()
# print(row)

# conn.close()

# -----------------------------------------------------------------------

# # /simulation 결과 테이블 출력
# conn = pymysql.connect(host="wonsdb", user="root", password="rlarlaths1#", db="record_db")

# cur = conn.cursor()

# cur.execute("SELECT * FROM map_record")
# row = cur.fetchall()
# print(row)

# conn.close()

# -----------------------------------------------------------------------

# # Chat_ID별로 시도한 횟수

# conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')

# try:
#     with conn.cursor() as cur:
#         sql = 'SELECT Chat_ID, Agent, COUNT(*) FROM game_record GROUP BY Agent ORDER BY Chat_ID'
#         cur.execute(sql)
        
#         # 튜플 추출
#         for row in cur.fetchall():
#             print(row)

#     conn.commit()
# finally:
#     conn.close()

# -----------------------------------------------------------------------

# # Chat_ID당 시도 횟수

# conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')

# try:
#     with conn.cursor() as cur:
#         sql = 'SELECT DISTINCT Chat_ID, COUNT(Chat_ID) FROM game_record GROUP BY Chat_ID ORDER BY COUNT(Chat_ID) DESC'
#         cur.execute(sql)
        
#         # 튜플 추출
#         for row in cur.fetchall():
#             print(row)

#     conn.commit()
# finally:
#     conn.close()

# -----------------------------------------------------------------------

# # Chat_ID당 시뮬레이션 횟수

# conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')

# try:
#     with conn.cursor() as cur:
#         sql = 'SELECT DISTINCT Chat_ID, COUNT(Chat_ID) FROM map_record GROUP BY Chat_ID ORDER BY Chat_ID'
#         cur.execute(sql)
        
#         # 튜플 추출
#         for row in cur.fetchall():
#             print(row)

#     conn.commit()
# finally:
#     conn.close()

# -----------------------------------------------------------------------

# 에이전트 이름 확인용

# conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')

# try:
#     with conn.cursor() as cur:
#         sql = 'SELECT Chat_ID, Agent, Try_Time FROM game_record WHERE Chat_ID = 5100300114'
#         cur.execute(sql)
        
#         # 튜플 추출
#         for row in cur.fetchall():
#             print(row)

#     conn.commit()
# finally:
#     conn.close()



# CSV로 추출 

conn = pymysql.connect(host='wonsdb', user='root', password='rlarlaths1#', db='record_db')

try:
    with conn.cursor() as cur:
        sql = 'SELECT Chat_ID, Agent, Try_Time FROM game_record WHERE Chat_ID = 5100300114'
        cur.execute(sql)
        
        # 튜플 추출
        for row in cur.fetchall():
            print(row)

    conn.commit()
finally:
    conn.close()