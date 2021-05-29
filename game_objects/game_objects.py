import random as r

import pygame

from .main_game_obj import GameObject


class SnakeObj(GameObject):

    def __init__(self):
        super().__init__()
        self.obj = [[9, 3], [10, 3], [11, 3], [12, 3], [13, 3], [14, 3], ]
        # self.pos = self.obj[0].copy()
        self.direction = None
        self.last_direction = None
        self.tail = None

    # @render_counter_param(FRAME_C)
    def move(self, eat=False):

        if self.direction:  # need for 'step' mode
            (y, x) = self.get_pos()
            if self.direction == 'UP':
                y -= 1
            elif self.direction == 'DOWN':
                y += 1
            elif self.direction == 'LEFT':
                x -= 1
            elif self.direction == 'RIGHT':
                x += 1
            y, x = self.pos_mirror_effect((y, x))
            self.obj.insert(0, [y, x])
            if not eat:
                self.tail = self.obj.pop()
            self.last_direction = self.direction

    def eat(self):
        self.obj.append(self.tail)

    def get_name(self):
        return 'SnakeObj'

    def get_pos(self):
        return list(self.obj[0])


class SnakeFood(GameObject):

    def __init__(self, snake):
        super().__init__()
        self.obj = None
        self.pos = self.new_food(snake)

    def new_food(self, snake):
        y, x = snake.get_pos()
        while [y, x] in snake.get_obj():
            x = r.randint(0, 9)
            y = r.randint(0, 19)
        self.obj = [[y, x]]
        return self.obj

    def get_pos(self):
        return list(self.obj[0])


class Bomb(GameObject):
    BOMB_1 = [[0, 0], [0, 3], [1, 1], [1, 2], [2, 1], [2, 2], [3, 0], [3, 3]]
    BOMB_2 = [[0, 1], [0, 2], [1, 0], [1, 3], [2, 0], [2, 3], [3, 1], [3, 2]]

    def __init__(self):
        super().__init__()
        self.player = None
        self.pos = None
        self.obj = None
        self.frames = 10
        self.bang_count = 5
        self.bomb_frame_1 = []
        self.bomb_frame_2 = []
        self.end = True

    def activate(self, player):
        self.player = player
        self.get_bobm_with_pos()
        self.end = False

    def bang(self, ):
        if not self.end:
            self.frames -= 1
            if self.frames > 5:
                self.obj = self.bomb_frame_1
                self.clean_hit_box = self.bomb_frame_2
            else:
                self.obj = self.bomb_frame_2
                self.clean_hit_box = self.bomb_frame_1
            if self.frames == 0:
                self.frames = 10
                self.bang_count -= 1
            if not self.bang_count:
                self.end = True
                self.set_to_default()
                return False
            return True

    def set_to_default(self):
        self.bang_count = 5
        self.frames = 10
        self.pos = None
        self.player = None
        self.bomb_frame_1 = []
        self.bomb_frame_2 = []

    def get_bobm_with_pos(self):
        self.pos = self.player.get_pos()
        y, x = self.pos
        if y == 0:
            y = 1
        if y > 17:
            y = 17
        if x == 0:
            x = 1
        if x > 7:
            x = 7
        y -= 1
        x -= 1
        for _y, _x in Bomb.BOMB_1:
            self.bomb_frame_1.append([_y + y, _x + x])
        for _y, _x in Bomb.BOMB_2:
            self.bomb_frame_2.append([_y + y, _x + x])
        self.obj = self.bomb_frame_1
        self.clean_hit_box = self.bomb_frame_2


class Curtain(GameObject):

    def __init__(self):
        super().__init__()
        self.y_line = 19
        self.obj = []
        self.clean_hit_box = []
        self.direction = 'UP'
        self.end = False

    def clean(self):
        self.obj = []
        for y in range(self.y_line, 20):
            for x in range(0, 10):
                self.obj.append([y, x])
        self.clean_hit_box = []
        for y in range(0, self.y_line):
            for x in range(0, 10):
                self.clean_hit_box.append([y, x])
        if self.direction == 'UP':
            self.y_line -= 1
        else:
            self.y_line += 1
        if self.y_line == -1:
            self.direction = 'DOWN'
            self.y_line += 1
        if self.y_line == 20:
            self.end = True

    def set_to_default(self):
        self.y_line = 19
        self.obj = []
        self.clean_hit_box = []
        self.direction = 'UP'
        self.end = False


class Turret(GameObject):

    def __init__(self, start_point):
        super().__init__()
        self.x, self.y = start_point

    def __str__(self):
        return 'Player'

    def get_obj(self):
        obj = []
        elements = (self.y, self.x), (self.y + 1, self.x), (self.y + 1, self.x - 1), (self.y + 1, self.x + 1)
        for y, x in elements:
            if y in range(0, 20) and x in range(0, 10):
                obj.append([y, x])
        return obj

    def move(self, key):
        if key == pygame.K_LEFT:
            if self.x != 0:
                self.x -= 1
        elif key == pygame.K_RIGHT:
            if self.x != 9:
                self.x += 1

    def get_position(self):
        return self.y, self.x

    def get_pos(self):
        return self.y, self.x


class Wall(GameObject):
    counter_for_new_line = 30 * 5

    def __init__(self, start_line_count=3, auto_line_add=True, direction=None, out_of_screen=False):
        super().__init__(out_of_screen=out_of_screen)
        self.obj = []
        self.counter_for_new_line = Wall.counter_for_new_line
        self.auto_line_add = auto_line_add
        self.direction = direction
        self.__init_wall(start_line_count)

    def __str__(self):
        return str(self.obj)

    def __init_wall(self, start_line_count):
        for y in range(start_line_count):
            #  for recorder
            # y += 10
            self.__add_line(y)
        if self.direction == 'down':
            self.obj.extend((20, x) for x in range(10))
        elif self.direction == 'up':
            self.obj.extend((-1, x) for x in range(10))
            # self.obj.extend((9, x) for x in range(10))
        # self.add_brick((0,1))

    def clean_wall(self):
        self.obj = []

    def __add_line(self, line_y_pos):
        y = line_y_pos
        line = []
        for x in range(10):
            pos = (y, x)
            if r.randint(0, 1):
                line.append(pos)
        if len(line) == 10:
            line.pop(r.randint(0, 9))
        if line:
            self.obj.extend(line)
        else:
            self.__add_line(line_y_pos)

    def _get_down(self):
        top = 0
        for y, x in self.obj:
            if y > top:
                top = y
        return top

    def get_top(self):
        top = 1000
        for y, x in self.obj:
            if y < top:
                top = y
        return top

    # def get_obj(self):
    # need to turel
    #     if self.auto_line_add:
    #         self.auto_line_adder()
    #         self._check_line()
    #     return self.obj

    def act(self):
        self.test_wall_check_lines()
        if self.auto_line_add:
            self.auto_line_adder()

    def auto_line_adder(self):
        self.counter_for_new_line -= 1
        if self.counter_for_new_line == 0:
            self.counter_for_new_line = Wall.counter_for_new_line
            self.__move_lines(line_y_pos=-1, direction='down')
            self.__add_line(line_y_pos=0)

    def drop_brick(self, brick_pos):
        """Удаление елемента из массива"""
        self.obj.remove(brick_pos)

    def add_brick(self, brick_pos):
        """Добавление елемента к массиву"""
        if brick_pos in self.obj:
            print('IN!!!')
        self.obj.append(brick_pos)

    def add_array(self, array):
        for brick in array:
            self.add_brick(brick)

    def test_wall_check_lines(self):
        lines_to_del = self._check_line_new()
        if lines_to_del:
            self.del_lines(lines_to_del)
            self.correct_array(lines_to_del)

    def _check_line_new(self):
        dic = {}
        for y, x in self.obj:
            if y not in dic:
                dic.update({y: 1})
            else:
                dic[y] += 1
        if 10 in dic.values():
            lines_to_del = []
            for y, x in dic.items():
                if x == 10 and y in range(20):
                    lines_to_del.append(y)
            return lines_to_del

    def del_lines(self, lines: list):
        if len(self.obj) != len(set(self.obj)):
            print('SET TO == ARRAY')
        for y_line in lines:
            self.obj = list((y, x) for y, x in self.obj if y != y_line)

    def correct_array(self, y_line_del):
        if self.direction == 'down':
            coof = 1
        else:
            # self.direction == 'up'
            coof = -1
        y_line_del.sort()
        for y_line_to_del in y_line_del:
            new_obj = []
            for y, x in self.obj:
                if self.direction == 'down':
                    if y < y_line_to_del:
                        # y, x = y + 1, x
                        y, x = y + coof, x
                else:
                    if y > y_line_to_del:
                        # y, x = y + 1, x
                        y, x = y + coof, x
                new_obj.append((y, x))
            self.obj = new_obj

    def __move_lines(self, line_y_pos, direction):
        """смещает блоки ниже указаной - ЗАМЕНИТЬ!!!"""
        if direction == 'up':
            direction = -1
        elif direction == 'down':
            direction = 1
        new_obj = []
        for y, x in self.obj:
            if y > line_y_pos:
                new_brick = (y + direction, x)
                new_obj.append(new_brick)
            else:
                new_obj.append((y, x))
        self.obj = new_obj

    # def _check_line(self):
    #     self._check_line_new()
    #     """Проверяет нет ли заполненных строк"""
    #     lines = set([y for y, x in self.obj])
    #     for line in lines:
    #         line_counter = 0
    #         for y, x in self.obj:
    #             if y == line:
    #                 line_counter += 1
    #         if line_counter == 10:
    #             self._del_line_and_down_rest(line)

    # def _del_line_and_down_rest(self, line_y_pos):
    #     self.obj = list(filter(lambda pos: pos[0] != line_y_pos, self.obj))
    #     # self.__move_lines(line_y_pos, direction=-1)
    #     self.__move_lines(line_y_pos, direction='up')
    #


class Bullet(GameObject):
    number = 0

    def __init__(self, start_point, direction=None):
        super().__init__()
        self.x = start_point[1]
        self.y = start_point[0]
        self.direction = 'UP' if direction is None else direction
        self.counter = 0
        self.counter = 15
        self.obj = ((self.y, self.x),)
        self.number = Bullet.number
        Bullet.number += 1

    def __str__(self):
        return 'Bullet'

    def move(self):
        if self.direction == 'UP':
            self.y -= 1
        self.obj = ((self.y, self.x),)

    def get_pos(self):
        return self.y, self.x

    def get_obj(self):
        return ((self.y, self.x),)


class Car(GameObject):
    FRAME = 5
    schema = (0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (3, 0), (3, 1), (3, 2),
    left = (16, 2)
    right = (16, 5)

    def __init__(self, out_of_screen=False, pos=(16, 3), ):
        super().__init__(out_of_screen=out_of_screen)
        self.frame = 1
        self.pos = pos
        self.obj = None
        self.get_car_with_pos()
        self.side_position = 'left'

    def get_car_with_pos(self):
        new_car = []
        for y, x in Car.schema:
            new_car.append((y + self.pos[0], x + self.pos[1]))
        self.obj = new_car

    def move(self, direction):
        self.frame -= 1
        if self.frame == 0:
            self.move_obj_n_pos(direction=direction)
            self.frame = Car.FRAME

    #
    # def move_to(self, pos):
    #     self.pos = pos
    #     self.get_car_with_pos()

    def move_right(self):
        if self.side_position != 'right':
            self.move_obj_n_pos('right', step=3)
            self.side_position = 'right'

    def move_left(self):
        if self.side_position != 'left':
            self.move_obj_n_pos('left', step=3)
        self.side_position = 'left'

    def get_pos(self):
        return list(self.obj[0])


class RoadBorder(GameObject):
    schema = [(18, 0), (17, 0), (13, 0), (12, 0),
              (8, 0), (7, 0), (3, 0), (3, 9), (7, 9),
              (8, 9), (12, 9), (13, 9), (17, 9), (18, 9),
              (2, 0), (2, 9), (16, 0), (11, 0), (6, 0),
              (1, 0), (1, 9), (6, 9), (11, 9), (16, 9)]

    def __init__(self):
        super().__init__()
        self.obj = RoadBorder.schema

    def move(self):
        self.frame -= 1
        if self.frame == 0:
            self.move_obj_n_pos(direction='down')
            self.frame = 10
            self.pos_mirror_effect_obj()


class Cursor(GameObject):

    def __init__(self, pos):
        super().__init__()
        self.obj = [pos]
        self.pos = self.obj[0]

    def move(self, direction):
        self.move_obj_n_pos(direction=direction, )
        self.obj = [self.pos_mirror_effect(self.obj[0])]

    def get_pos(self):
        return self.obj[0]


class Brick(GameObject):

    Turret = {
        0: ((2, 0), (2, 1), (1, 1), (2, 2)),
        1: ((0, 0), (1, 0), (2, 0), (1, 1)),
        2: ((0, 0), (0, 1), (1, 1), (0, 2)),
        3: ((1, 1), (0, 2), (1, 2), (2, 2)),
    }
    Big_line = {
        0: ((0, 1), (1, 1), (2, 1), (3, 1)),
        1: ((3, 0), (3, 1), (3, 2), (3, 3))
    }
    Cube = {
        0: ((0, 0), (1, 0), (1, 1), (0, 1)),
    }

    S_right = {
        0: ((1, 1), (1, 2), (2, 1), (2, 0)),
        1: ((0, 0), (1, 0), (1, 1), (2, 1)),
    }
    S_left = {
        0: ((1, 0), (1, 1), (2, 1), (2, 2)),
        1: ((0, 1), (1, 1), (1, 0), (2, 0)),
    }
    L_left = {
        0: ((0, 0), (1, 0), (2, 0), (2, 1)),
        1: ((1, 0), (0, 0), (0, 1), (0, 2)),
        2: ((0, 1), (0, 2), (1, 2), (2, 2)),
        3: ((1, 2), (2, 2), (2, 1), (2, 0)),
    }

    L_incorect = {
        0: ((2, 0), (1, 0), (0, 0), (0, 1)),
        1: ((0, 0), (0, 1), (0, 2), (1, 2)),
        2: ((0, 2), (1, 2), (2, 2), (2, 1)),
        3: ((2, 2), (2, 1), (2, 0), (1, 0)),
    }

    # Small_line = {
    #     0: ((1, 0), (1, 1),),
    #     1: ((0, 0), (1, 0),),
    # }
    # turret_1 = ((2, 0), (2, 1), (1, 1), (2, 2))
    # turret_2 = ((0, 0), (1, 0), (2, 0), (1, 1))
    # turret_3 = ((0, 0), (0, 1), (1, 1), (0, 2))
    # turret_4 = ((1, 1), (0, 2), (1, 2), (2, 2))
    # shapes = [turret_1,turret_2, turret_3, turret_4]

    shapes = [Turret, Big_line, Cube, S_right, S_left, L_left, L_incorect]
    FRAME = 12

    def __init__(self, pos, shape=None, rotation=0):
        super().__init__()
        # if shape is None:
        #     shape = r.choice(shapes)
        self.direction = 'down'
        self.last_direction = 'down'
        self.shape = shape
        self.shape_number = rotation
        self.pos = pos
        self.obj = shape[rotation]
        self.out_of_screen = True
        self.frame = Brick.FRAME
        self.get_obj_with_pos()

    def rotate(self):
        self.shape_number += 1
        print(self.shape_number)
        if self.shape_number == len(self.shape):
            self.shape_number = 0
        self.obj = self.shape[self.shape_number]

        self.get_obj_with_pos()

    def rotate_back(self):
        self.shape_number -= 1
        if self.shape_number == -1:
            self.shape_number = len(self.shape) - 1
        self.obj = self.shape[self.shape_number]

        self.get_obj_with_pos()

    def move_back(self):
        print('move back')
        direction_inversion = {
            'right': 'left',
            'left': 'right',
            'down': 'up',
            'up': 'down',
        }
        direction = direction_inversion[self.last_direction]
        self.move_obj_n_pos(direction, step=1)

    def auto_move(self):
        self.frame -= 1
        if self.frame == 0:
            self.move_down()
            self.frame = Brick.FRAME

    def move_right(self):
        self.move_obj_n_pos('right', step=1)

    def move_left(self):
        self.move_obj_n_pos('left', step=1)

    def move_down(self):
        self.move_obj_n_pos('down', step=1)

    def move_up(self):
        self.move_obj_n_pos('up', step=1)
