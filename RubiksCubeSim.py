from ursina import *


class RubiksCube:

    def __init__(self):

        self.cubes = []
        self.history = []
        self.trigger = True
        self.history_index = 0
        self.cubes_left = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.cubes_down = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.cubes_front = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.cubes_back = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.cubes_right = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.cubes_up = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.cubes_m = {Vec3(0, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.cubes_e = {Vec3(x, 0, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.cubes_s = {Vec3(x, y, 0) for x in range(-1, 2) for y in range(-1, 2)}

        self.dict_cubes = {
            'l': self.cubes_left,
            'r': self.cubes_right,
            'u': self.cubes_up,
            'd': self.cubes_down,
            'f': self.cubes_front,
            'b': self.cubes_back,
            'm': self.cubes_m,
            'e': self.cubes_e,
            's': self.cubes_s
        }

        self.dict_axis = {
            'l': 'rotation_x',
            'r': 'rotation_x',
            'm': 'rotation_x',
            'u': 'rotation_y',
            'd': 'rotation_y',
            'e': 'rotation_y',
            'f': 'rotation_z',
            'b': 'rotation_z',
            's': 'rotation_z'
        }

        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    self.cubes.append(Entity(model='models/custom_cube.obj', texture='textures/rubik_texture.png',
                                             position=(x, y, z)))

        self.cubes[12].texture = 'textures/front.png'
        self.cubes[4].texture = 'textures/left.png'
        self.cubes[14].texture = 'textures/back.png'
        self.cubes[22].texture = 'textures/right.png'
        self.cubes[10].texture = 'textures/down.png'
        self.cubes[16].texture = 'textures/up.png'

    def delete_parent(self):
        for cube in self.cubes:
            if cube.parent == self.cubes[13]:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot

    def attach_parent(self, face):
        buf = self.dict_cubes[face]

        self.cubes[13].rotation = 0
        for cube in self.cubes:
            if cube.position in buf:
                cube.parent = self.cubes[13]

    def cube_rotation(self, name, angle=0):

        self.trigger = False
        self.delete_parent()
        self.attach_parent(name)
        if held_keys['shift'] and angle == 0:
            angle = -90
        elif angle == 0:
            angle = 90

        self.add_move(name, -angle)

        if name in 'lrm':
            self.cubes[13].animate(self.dict_axis[name], self.cubes[13].rotation_x + angle, duration=.2)
        if name in 'ude':
            self.cubes[13].animate(self.dict_axis[name], self.cubes[13].rotation_y + angle, duration=.2)
        if name in 'fbs':
            self.cubes[13].animate(self.dict_axis[name], self.cubes[13].rotation_z + angle, duration=.2)

        invoke(self.change_trigger, delay=0.31)

    def add_move(self, name, angle):
        self.history.append((name, angle))
        self.history_index += 1

    def undo(self):
        if len(self.history) > 0 and self.history_index > 0:
            self.cube_rotation(self.history[self.history_index - 1][0], self.history[self.history_index - 1][1])
            self.history.pop()
            self.history_index -= 2

    def redo(self):
        if self.history_index < len(self.history):
            self.cube_rotation(self.history[self.history_index][0], -self.history[self.history_index][1])
            self.history.pop()

    def delete_moves(self):
        x = len(self.history) - self.history_index
        for i in range(x):
            self.history.pop()

    def change_trigger(self):
        self.trigger = True


def input(key):
    if key in 'lrufbdmes' and game.trigger:
        if game.history_index < len(game.history):
            game.delete_moves()
        game.cube_rotation(key)

    if key == 'h' and game.trigger:
        if held_keys['shift']:
            game.redo()
        else:
            game.undo()

    if key == 'space' and game.trigger:
        for i in range(1):
            if game.history_index < len(game.history):
                game.delete_moves()
            x = random.choice('lrufbdmes')
            game.cube_rotation(x)


if __name__ == '__main__':
    app = Ursina()
    game = RubiksCube()
    window.borderless = False
    window.exit_button.visible = False
    EditorCamera()
    txt = Text(text='U - Up\n'
                    'D - Down\n'
                    'L - Left\n'
                    'R - Right\n'
                    'F - Front\n'
                    'B - Back\n'
                    'M - the layer between L and R\n'
                    'E - the layer between U and D\n'
                    'S - the layer between F and B\n'
                    'SHIFT + KEY - move backwards\n'
                    'H - undo\n'
                    'SHIFT + H - redo\n'
                    'SPACE - random move'
               , x=-0.75, y=0.4)

    app.run()
