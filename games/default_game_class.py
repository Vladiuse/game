import time
import pygame
from game_objects import Bomb, Curtain
from settings import GameSettings



class Game:

    def __init__(self, controller, game_mode=None):
        self.controller = controller
        self.game_condition = []
        self.small_screen_condition = []
        self.game_status = True
        self.game_objects = []
        self.start_time = time.time()
        self.score = 0
        self.game_speed = 5
        self.lives = 2
        self.fps = GameSettings.FPS
        self.game_mode = game_mode
        self.blink_count = 6
        self.pause = False
        self.turret = None
        self.bomb = Bomb()
        self.curtain = Curtain()


    def start_game(self):
        """Иницилизация стартового состояния игры"""
        self.get_null_screen()
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

    def pause_game(self):
        self.pause = False if self.pause else True

    def end_game(self):
        if not self.bomb.end:
            self.bomb.bang()
            self.render(*self.game_objects)
        else:
            self.curtain.clean()
            self.render(self.curtain)
            if self.curtain.end:
                self.curtain.set_to_default()
                if self.lives == 0:
                    self.controller.chose_game('default')
                else:
                    self.restart_game()


    def curtain_clean_effect(self, in_end_func=None):
        if self.y_clean_pic != -21:
            if self.y_clean_pic >= 0:
                self.game_condition[self.y_clean_pic] = [1] * 10
            else:
                self.game_condition[abs(self.y_clean_pic + 1)] = [0] * 10
            self.y_clean_pic -= 1
        else:
            self.y_clean_pic = 19
            if in_end_func:
                in_end_func()

    def render(self, *args):
        self.get_null_screen()
        for obj in args:
            if obj.get_clean_hit_box():
                for y, x in obj.get_clean_hit_box():
                    self.game_condition[y][x] = 0
            if obj.get_obj():
                for y, x in obj.get_obj():
                    self.game_condition[y][x] = 1

    def game_key_controller(self, key):
        """Меняет флаг направление движения -
        изменение на противоположное не проходит"""
        if key == pygame.K_ESCAPE:
            self.controller.chose_game('default')
        if key == pygame.K_p:
            self.pause_game()
        # if key == pygame.K_x:
        #     self.game_status = False



    def collisions(self):
        pass

    def blink_effect(self, *args):
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
