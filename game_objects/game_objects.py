# def render_counter_param(n):
#     counter = 0
#
#     def render_counter(func):
#         def surrogate(*args, **kwargs):
#             nonlocal counter
#             counter += 1
#             print('DECOR', counter)
#             if counter == n:
#                 counter = 0
#                 return func(*args, **kwargs)
#
#         return surrogate
#
#     return render_counter
#
import random as r


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

    def activate(self, player):
        self.player = player
        self.get_bobm_with_pos()

    def bang(self, ):
        if self.player:
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
            for x in range(0,10):
                self.obj.append([y, x])
        self.clean_hit_box = []
        for y in range(0, self.y_line):
            for x in range(0,10):
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




    #
    #
    # def clean(self, in_end_func=None):
    #     if self.y_clean_pic != -21:
    #         if self.y_clean_pic >= 0:
    #             self.game_condition[self.y_clean_pic] = [1] * 10
    #         else:
    #             self.game_condition[abs(self.y_clean_pic + 1)] = [0] * 10
    #         self.y_clean_pic -= 1
    #     else:
    #         self.y_clean_pic = 19
