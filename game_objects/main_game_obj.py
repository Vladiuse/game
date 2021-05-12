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

    def move_obj(self, direction, step=1):
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
        for y,x in self.obj:
            new_obj.append((y + _y, x + _x))
        self.obj = new_obj


    @staticmethod
    def pos_mirror_effect(pos):
        y,x = pos
        if x == -1:
            x = 9
        elif x == 10:
            x = 0
        elif y == -1:
            y = 19
        elif y == 20:
            y = 0
        return y, x