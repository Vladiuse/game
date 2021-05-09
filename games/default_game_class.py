import time

from settings import GameSettings


class Game:

    def __init__(self, controller, game_mode=None):
        self.controller = controller
        self.game_condition = []
        self.game_status = True
        self.start_time = time.time()
        self.score = 0
        self.game_speed = 5
        self.lives = 3
        self.fps = GameSettings.FPS
        self.game_mode = game_mode
        self.blink_count = 20

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        self.get_null_screen()

    def restart_game(self):
        pass

    def get_null_screen(self):
        """Получить чистый экран"""
        self.game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())

    def get_screen_pic(self):
        """get frame of game"""
        return self.game_condition

    def run(self):
        """Основной цикл игры"""
        pass

    def end_game(self):
        self.game_status = False

    def render(self, *args):
        self.get_null_screen()
        for obj in args:
            for y, x in obj.get_obj():
                self.game_condition[y][x] = 1

    def collisions(self):
        pass

    def blink_elems(self, *args):
        """Add blink effect on elements"""
        self.blink_count -= 1
        for elem in args:
            for y, x in elem:
                if self.blink_count > 10:
                    self.game_condition[y][x] = 0
                else:
                    self.game_condition[y][x] = 1
                if self.blink_count == 0:
                    self.blink_count = 20
