
from ursina import *
from system_game import *

EditorCamera.input = None

app = Ursina()
ec = EditorCamera(rotation=(-52,44,50), world_position=(.05,.05,0),target_z=-2, rotation_speed = 0, zoom_speed = 0)
info = Infomation_Scene()
room = Room_scene()
Button_UI.set_button_ui()
room.login_window()

def chage_scene():
    if room.enabled :
        room.enabled = False
        info.enabled = True
        info.maze_update(room.chat_id)
        ec.enabled = False
    else :
        room.enabled = True
        info.enabled = False
        ec.enabled = True


Button_UI.append_button(color = color.gray, method = chage_scene)

app.run()


