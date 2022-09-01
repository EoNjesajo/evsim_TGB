from ursina import *
import copy
# from game_bot2 import *
from system_bot import *

from azure.iot.hub import IoTHubRegistryManager

class Button_UI() :
    button_ui = None
    @staticmethod
    def set_button_ui():
        Button_UI.button_ui = Entity(
            parent = camera.ui,
            model = Quad(radius=.015),
            texture = 'white_cube',
            texture_scale = (3,1),
            scale = (.3, .1),
            origin = (-.5, .5),
            position = (-.7,-.3),
            color = color.color(0,0,.1,.9),
            enabled = False
        )
    @staticmethod
    def find_free_spot():
        for y in range(1):
            for x in range(3):
                grid_positions = [(int(e.x*Button_UI.button_ui.texture_scale[0]), int(e.y*Button_UI.button_ui.texture_scale[1])) for e in Button_UI.button_ui.children]
                if not (x,-y) in grid_positions:
                    return x, y
    @staticmethod
    def append_button(color, method, x=0, y=0):
        x, y = Button_UI.find_free_spot()
        button = Button(
            parent = Button_UI.button_ui,
            model = 'quad',
            text = '+',
            color = color,
            scale_x = 1/Button_UI.button_ui.texture_scale[0],
            scale_y = 1/Button_UI.button_ui.texture_scale[1],
            origin = (-.5,.5),
            x = x * 1/Button_UI.button_ui.texture_scale[0],
            y = -y * 1/Button_UI.button_ui.texture_scale[1],
            z = -.5,
            # tooltip = Tooltip('Add item'),
            on_click = method
            )

    



class Room_scene(Entity):
    def __init__(self):
        super().__init__(
            parent = scene
        )
        self.CONNECTION_STRING = "HostName=wonshub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=oy2TdFWu/6Phfu32UfZwzG5GXU4yNNm+cRL6xOXIpjU="
        self.DEVICE_ID = "maze"
        self.bg = Entity(parent = self)
        self.fg = Entity(parent = self)
    class Block(Entity):
        def __init__(self, position=(0,0,0), **kwargs):
            super().__init__(
                position = position,
                scale = (.1, .1, .1),
                model = 'cube',
                texture = 'white_cube',
                color = color.white,
            )
            for key, value in kwargs.items():
                setattr(self, key, value)
    class Object(Draggable):
        def __init__(self, position=(0,0,0), parent = scene, **kwargs):
            super().__init__(
                parent = parent,
                position = position,
                model = 'cube',
                scale = (.07, .07, .1),
                texture = 'white_cube',
                color = color.random_color(),
                highlight_color = color.lime,
            )
            for key, value in kwargs.items():
                setattr(self, key, value)

    def iothub_messaging_sample_run(self, message):
        try:
            registry_manager = IoTHubRegistryManager(self.CONNECTION_STRING)
            props={}
            props.update(messageId = str(self.chat_id))

            registry_manager.send_c2d_message(self.DEVICE_ID, message, properties=props)

        except Exception as ex:
            print ( "Unexpected error {0}" % ex )
            return
        except KeyboardInterrupt:
            print ( "IoT Hub C2D Messaging service sample stopped" )


    
    def set_room(self, chat_id, name):
        self.chat_id = int(chat_id)
        self.name = name
        # SystemBot.handler(chat_id = self.chat_id, message = ['start', self.name], sp = False)
        self.iothub_messaging_sample_run('start {}'.format(self.name))
    
        for y in range(-5,5):
            for x in range(-5,5):
                block = self.Block(parent=self.bg, position=(x/10,y/10,0))
        for i in range(-5,5):
            for z in range(5):
                wall = self.Block(parent=self.bg, position=(i/10,5/10,-z/10), color = color.gray)
                wall = self.Block(parent=self.bg, position=(5/10,i/10,-z/10), color = color.gray)
   

    def find_free_spot(self):
        for y in range(4,-5,-1):
            for x in range(-5,4):
                grid_positions = [(int(e.x*10), int(e.y*10)) for e in self.fg.children] #e.x*self.texture_scale[0]
                if not (x,y) in grid_positions:
                    return x, y
    def append(self, text, x=0, y=0):
        if len(self.fg.children) >= 8*8:
            error_message = Text('<red>Inventory is full!', origin=(0,-1.5), x=-.5, scale=2)
            destroy(error_message, delay=1)
            return
        x, y = self.find_free_spot()
        def add_button() : 
            self.iothub_messaging_sample_run(text)
        object = self.Object(position=(x/10,y/10,-1/10), parent=self.fg, on_double_click = add_button, tooltip = Tooltip(text))
        def drag():
            object.org_pos = (object.x, object.y)
            object.z=-1/10
        def drop():
            object.x = round((object.x + (object.scale_x/2)) * 10) / 10
            object.y = round((object.y + (object.scale_y/2)) * 10) / 10
            object.z=-1/10
            if object.x < -0.5 or object.x >= 0.5 or object.y < -0.5 or object.y >= 0.5:
                object.position = (object.org_pos)
                return

            for c in self.fg.children:
                if c == object:
                    continue

                if c.x == object.x and c.y == object.y:
                    c.position = object.org_pos

        object.drag = drag
        object.drop = drop

    
    def login_window(self) :
        def login():
            def add_method():
                self.add_window()
            self.set_room(login_panel.content[1].text,login_panel.content[3].text)
            Button_UI.button_ui.enabled = True
            Button_UI.append_button(color = color.red, method = add_method)
            destroy(login_panel)
        login_panel = WindowPanel(
            title='Login',
            content=(
                Text('Chat_id:'),
                InputField(name='id_field'),
                Text('Name:'),
                InputField(name='name_field'),
                Button(text='login', color=color.azure,on_click = login),
                ),
                popup=True,
                enabled=True
            )
    def add_window(self) :
        def add():
            self.append(add_panel.content[1].text)
            destroy(add_panel)
        add_panel = WindowPanel(
            title='add object',
            content=(
                Text('command:'),
                InputField(name='command'),
                Button(text='add', color=color.azure,on_click = add),
                ),
                popup=False,
                enabled=True
            )

class Infomation_Scene(Entity):

    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = Quad(radius=.015),
            texture = 'white_cube',
            texture_scale = (8,8),
            scale = (0.8, 0.8),
            origin = (-.5, 5),
            position = (-.3,.4),
            color = color.color(0,0,.1,.9),
            enabled = False
        )
    def maze_update(self,chat_id):
        map = SystemBot.location(chat_id = chat_id, message = ['location'])
        self.iothub_messaging_sample_run('location')
        size = len(map)
        for i in range(0,size):
            for j in range(0,size):
                if map[i][j] == 1 :
                    et_color = color.black
                elif map[i][j] == 5 :
                    et_color = color.red
                elif map[i][j] == 3 :
                    et_color = color.blue
                elif map[i][j] == 8 :
                    et_color = color.gray
                else :
                    et_color = color.white

                entity = Entity(
                    parent = self,
                    model = 'cube',
                    color = et_color,
                    scale_x = 1/self.texture_scale[0],
                    scale_y = 1/self.texture_scale[1],
                    origin = (-.5,.5),
                    x = j * 1/self.texture_scale[0],
                    y = -i * 1/self.texture_scale[1],
                    z = -.5,
                )


        


