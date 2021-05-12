import random as r

import pygame


class GameObject:

    def __init__(self, pos=None):
        self.pos = [0, 0] if pos is None else pos
        self.obj = [self.pos]
        self.clean_hit_box = None

    def __str__(self):
        return __class__.__name__

    def get_obj(self):
        return self.obj

    def get_clean_hit_box(self):
        return self.clean_hit_box

    def get_pos(self):
        return list(self.obj[0])

    def move_obj(self):
        pass

    @staticmethod
    def pos_mirror_effect(y, x):
        if x == -1:
            x = 9
        elif x == 10:
            x = 0
        elif y == -1:
            y = 19
        elif y == 20:
            y = 0
        return y, x


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
            y, x = self.pos_mirror_effect(y, x)
            self.obj.insert(0, [y, x])
            if not eat:
                self.tail = self.obj.pop()
            self.last_direction = self.direction

    def eat(self):
        self.obj.append(self.tail)

    def get_name(self):
        return 'SnakeObj'


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


class Bomb(GameObject):
    BOMB_1 = [[0, 0], [0, 3], [1, 1], [1, 2], [2, 1], [2, 2], [3, 0], [3, 3]]
    BOMB_2 = [[0, 1], [0, 2], [1, 0], [1, 3], [2, 0], [2, 3], [3, 1], [3, 2]]

    def __init__(self):
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

    def __init__(self, start_line_count=3):
        super().__init__()
        self.obj = []
        self.__init_wall(start_line_count)
        self.counter_for_new_line = Wall.counter_for_new_line

    def __str__(self):
        return 'Wall'

    def __init_wall(self, start_line_count):
        for y in range(start_line_count):
            self.__add_line(y)

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

    def _get_top(self):
        top = 0
        for y, x in self.obj:
            if y > top:
                top = y
        return top

    def get_obj(self):
        self.auto_line_adder()
        self._check_line()
        return self.obj

    def auto_line_adder(self):
        self.counter_for_new_line -= 1
        if self.counter_for_new_line == 0:
            self.counter_for_new_line = Wall.counter_for_new_line
            self.__move_lines(line_y_pos=-1, direction=1)
            self.__add_line(line_y_pos=0)

    def drop_brick(self, brick_pos):
        self.obj.remove(brick_pos)

    def add_brick(self, brick_pos):
        self.obj.append(brick_pos)

    def _check_line(self):
        """Проверяет нет ли заполненных строк"""
        lines = set([y for y, x in self.obj])
        for line in lines:
            line_counter = 0
            for y, x in self.obj:
                if y == line:
                    line_counter += 1
            if line_counter == 10:
                # self._check_line_new(f'start - {line}')
                self._del_line_and_down_rest(line)
                # self._check_line_new('end')

    def _check_line_new(self, info):
        dic = {}
        for y, x in self.obj:
            if y not in dic:
                dic.update({y:1})
            else:
                dic[y] += 1
        print(dic, info)

    def _del_line_and_down_rest(self, line_y_pos):
        self.obj = list(filter(lambda pos: pos[0] != line_y_pos, self.obj))
        self.__move_lines(line_y_pos, direction=-1)

    def __move_lines(self, line_y_pos, direction=1):
        """смещает блоки ниже указаной"""
        new_obj = []
        for y, x in self.obj:
            if y > line_y_pos:
                new_brick = (y + direction, x)
                new_obj.append(new_brick)
            else:
                new_obj.append((y, x))
        self.obj = new_obj


class Bullet(GameObject):

    def __init__(self, start_point, direction=None):
        super().__init__()
        self.x = start_point[1]
        self.y = start_point[0]
        self.direction = 'UP' if direction is None else direction
        self.counter = 0
        self.counter = 15
        self.obj = [[self.y, self.x]]

    def __str__(self):
        return 'Bullet'

    def move(self):
        if self.direction == 'UP':
            self.y -= 1

    def get_pos(self):
        return self.y, self.x

    def get_obj(self):
        return [[self.y, self.x]]
