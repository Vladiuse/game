class GameObject:

    def __init__(self, pos=None):
        self.pos = [0, 0] if pos is None else pos
        self.obj = []

    def get_obj(self):
        return self.obj


class SnakeObj(GameObject):

    def __init__(self):
        super().__init__()
        self.obj = [[9, 5], [10, 5]]
        self.pos = self.obj[0]
        self.direction = None
        self.last_direction = None


class SnakeFood(GameObject):

    def __init__(self, pos):
        super().__init__(pos=pos)
        self.obj = [self.pos]
