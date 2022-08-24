from system_bot import *

#게임활용의 수업, 운영

# System Simulpythator Initialization

#시스템시뮬레이터 객체 생성

# 텔레그램 봇 이름 : maze_game_romm(@maze_guide_bot)

updater = SystemBot.get_updater()

updater.start_polling()
updater.idle()
