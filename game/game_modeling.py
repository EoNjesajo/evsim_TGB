from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.

class Object(Draggable):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            scale = (.07, .07, .1),
            texture = 'white_cube',
            color = color.random_color(),
            highlight_color = color.lime,
        )

class Wall(Entity):
    def __init__(self, position=(0,0,0), **kwargs):
        super().__init__(
            parent = scene,
            position = position,
            scale = (.1, .1, .1),
            color = color.white,
            model = 'cube',
            texture = 'white_cube',
        )    
        for key, value in kwargs.items():
            setattr(self, key, value)

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            scale = (.1, .1, .1),
            origin = (-.5,.5),
            model = 'cube',
            texture = 'white_cube',
            color = color.white,
            highlight_color = color.lime,
            on_click = self.click
        )


    # def input(self, key):
    #     if self.hovered:
    #         if key == 'left mouse down':
    #             object = Object(position=self.position + mouse.normal)
    def click(self):
        # if self.hovered:
        #     if key == 'left mouse down':
        object = Object(position=self.position + mouse.normal/10)
    
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

            for c in self.children:
                if c == object:
                    continue

                if c.x == object.x and c.y == object.y:
                    print('swap positions')
                    c.position = object.org_pos

        object.drag = drag
        object.drop = drop
    
            # if key == 'right mouse down':
            #     destroy(self)
                # voxel = Voxel(position=self.position + mouse.normal)

    # def click(self) :
    #     voxel = Voxel(position=self.position + mouse.normal)


for y in range(-5,5):
    for x in range(-5,5):
        voxel = Voxel(position=(x/10,y/10,0))

for y in range(-6,5):
    for z in range(5):
        wall = Wall(position=(5/10,y/10,-z/10))

for x in range(-6,6):
    for z in range(5):
        wall = Wall(position=(x/10,5/10,-z/10))

for x in range(-6,6):
    wall = Wall(position=(x/10,-6/10,0))
for y in range(-6,6):
    wall = Wall(position=(-6/10,y/10,0))

# def input(key):
#     if key == 'left mouse down':
#         hit_info = raycast(camera.world_position)
#         if hit_info.hit:
#             Voxel(position=hit_info.entity.position + hit_info.normal)

ec = EditorCamera(rotation=(-52,44,50), world_position=(.05,.05,0),target_z=-2, rotation_speed = 0)
# ec.enabled = False
# def input(key):
#     if key == 'scroll up' or 'scroll down':
#         print(ec.rotation)

app.run()