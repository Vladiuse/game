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


    def get_obj(self):
        return self.obj

    def get_pos(self):
        return list(self.obj[0])

    def move_obj(self):
        pass


class SnakeObj(GameObject):

    def __init__(self):
        super().__init__()
        self.obj = [[9, 3], [10, 3],[11, 3], [12, 3],[13, 3], [14, 3],]
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
            if x == -1:
                x = 9
            elif x == 10:
                x = 0
            elif y == -1:
                y = 19
            elif y == 20:
                y = 0
            self.obj.insert(0, [y, x])
            if not eat:
                self.tail = self.obj.pop()
            self.last_direction = self.direction

    def eat(self):
        self.obj.append(self.tail)


class SnakeFood(GameObject):

    def __init__(self, snake):
        super().__init__()
        self.obj = None
        self.pos = self.new_food(snake)

    def new_food(self, snake):
        y,x = snake.get_pos()
        while [y, x] in snake.get_obj():
            x = r.randint(0, 9)
            y = r.randint(0, 19)
        self.obj = [[y,x]]
        return self.obj
