import time

from settings import GameSettings


class Game:

    def __init__(self, controller, game_mode=None):
        self.controller = controller
        self.game_condition = []
        self.small_screen_condition = []
        self.game_status = True
        self.start_time = time.time()
        self.score = 0
        self.game_speed = 5
        self.lives = 2
        self.fps = GameSettings.FPS
        self.game_mode = game_mode
        self.blink_count = 6
        self.y_clean_pic = 19

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        # self.get_null_screen()
        self.get_small_screen_condition()

    def restart_game(self):
        print('restart_game default')
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
        if self.lives == 0:
            self.controller.chose_game('default')
        else:
            self.curtain_clean_effect()

    def curtain_clean_effect(self, in_end=None):
        if self.y_clean_pic != -21:
            if self.y_clean_pic >= 0:
                self.game_condition[self.y_clean_pic] = [1] * 10
            else:
                self.game_condition[abs(self.y_clean_pic + 1)] = [0] * 10
            self.y_clean_pic -= 1
        else:
            self.y_clean_pic = 19
            self.restart_game()







    def render(self, *args):
        self.get_null_screen()
        for obj in args:
            for y, x in obj.get_obj():
                self.game_condition[y][x] = 1

    def collisions(self):
        pass

    def blink_elems(self, *args):
        """Add blink effect on elements or objects"""
        self.blink_count -= 1
        for elem in args:
            for y, x in elem:
                if self.blink_count > 3:
                    self.game_condition[y][x] = 0
                else:
                    self.game_condition[y][x] = 1
                if self.blink_count == 0:
                    self.blink_count = 6

    def get_small_screen_condition(self):
        small_screen = [
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0]],
        ]
        dic_lives = {
            1: [[3, 0], ],
            2: [[3, 0], [2, 0], ],
            3: [[3, 0], [2, 0], [1, 0], ],
            4: [[3, 0], [2, 0], [1, 0], [0, 0], ],
        }
        if self.lives:
            # print(dic_lives[self.lives])
            for y, x in dic_lives[self.lives]:
                small_screen[y][x] = 1
        self.small_screen_condition = small_screen


    def get_small_screen_pic(self):
        return self.small_screen_condition