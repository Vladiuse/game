class GameObject:

    FRAME = 1

    def __init__(self, pos=None, frame=10, out_of_screen=False):
        # self.pos = [0, 0] if pos is None else pos
        self.pos = [0, 0] if pos is None else pos
        self.obj = [self.pos]
        self.clean_hit_box = None
        self.frame = GameObject.FRAME
        self.direction = None
        self.last_direction = None
        self.out_of_screen = out_of_screen

    def __str__(self):
        return __class__.__name__

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.obj):
            # self.i = 0
            raise StopIteration
        pos = self.obj[self.i]
        self.i += 1
        return pos

    def get_obj(self):
        if self.out_of_screen:
            in_screen_obj = []
            for pos in self.obj:
                if self.is_pos_in_screen(pos):
                    in_screen_obj.append(pos)
            return in_screen_obj
        return self.obj

    def get_clean_hit_box(self):
        return self.clean_hit_box

    def get_pos(self):
        return self.pos
        # return list(self.obj[0])

    def move_obj_n_pos(self, direction, step=1):
        _y = 0
        _x = 0
        if direction == 'up':
            _y -= step
        elif direction == 'down':
            _y += step
        elif direction == 'right':
            _x += step
        elif direction == 'left':
            _x -= step
        new_obj = []
        for y, x in self.obj:
            new_obj.append((y + _y, x + _x))
        self.obj = new_obj
        # коректировка self.pos
        y,x = self.pos
        self.pos = y + _y, x + _x
        self.direction = self.last_direction = direction

    def get_obj_with_pos(self, pos=None):
        new_obj = []
        for y, x in self.obj:
            new_obj.append((y + self.pos[0], x + self.pos[1]))
        self.obj = new_obj

    def move_right(self):
        self.move_obj_n_pos('right', step=1)
        self.direction = self.last_direction = 'right'

    def move_left(self):
        self.move_obj_n_pos('left', step=1)
        self.direction = self.last_direction = 'left'

    def move_down(self):
        self.move_obj_n_pos('down', step=1)
        self.direction = self.last_direction = 'down'

    def move_up(self):
        self.move_obj_n_pos('up', step=1)
        self.direction = self.last_direction = 'up'

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

    @staticmethod
    def pos_mirror_effect(pos):
        y, x = pos
        if x == -1:
            x = 9
        elif x == 10:
            x = 0
        elif y == -1:
            y = 19
        elif y == 20:
            y = 0
        return y, x

    def pos_mirror_effect_obj(self):
        new_obj = []
        for y, x in self.obj:
            y, x = self.pos_mirror_effect((y, x))
            new_obj.append((y, x))
        self.obj = new_obj

    @staticmethod
    def is_pos_in_screen(pos):
        y, x = pos
        return y in range(20) and x in range(10)

    def out_screen_pos_x_in_obj(self):
        """Выходит ли обьект за границу по оси х"""
        for y,x in self:
            if x not in range(10):
                return x

    def is_obj_in_screen(self):
        for pos in self.obj:
            if not self.is_pos_in_screen(pos):
                return False
        return True
