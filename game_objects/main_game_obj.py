class GameObject:

    def __init__(self, pos=None, frame=10, out_of_screen=False):
        self.pos = [0, 0] if pos is None else pos
        self.obj = [self.pos]
        self.clean_hit_box = None
        self.frame = frame
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

    def get_obj_with_pos(self, pos=None):
        new_obj = []
        for y, x in self.obj:
            new_obj.append((y + self.pos[0], x + self.pos[1]))
        self.obj = new_obj

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
        return y in range(0, 20) and x in range(0, 10)

    def out_screen_pos_x_in_obj(self):
        for y,x in self:
            if x not in range(10):
                return True

