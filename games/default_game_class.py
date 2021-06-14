import time

import pygame

from game_objects import Bomb, Curtain
from settings import GameSettings


class Game:
    """Main game object"""
    FRAME = 30
    # START_FRAME = 30

    def __init__(self, controller, game_mode=None, game_speed=1):
        self.controller = controller
        self.frame = self.__class__.FRAME
        self.game_condition = []
        self.small_screen_condition = []
        self.game_status = True
        self.game_objects = []
        self.start_time = time.time()
        self.score = 0
        self.game_speed = game_speed
        self.lives = 3
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
        self.frame = self.__class__.FRAME

    def restart_game(self):
        pass

    def get_null_screen(self):
        """Get clean screen"""
        self.game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for _ in range(20):
        # while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())

    def get_null_small_screen(self):
        """Get clean small screen"""
        self.small_screen_condition.clear()
        line = [0, 0, 0, 0]
        while len(self.small_screen_condition) != 4:
            self.small_screen_condition.append(line.copy())

    def get_screen_pic(self):
        """get frame of game"""
        return self.game_condition

    def get_small_screen_pic(self):
        """Get small screen frame"""
        return self.small_screen_condition

    def game_key_controller(self, key):
        """Меняет флаг направление движения -
        изменение на противоположное не проходит"""
        if key == pygame.K_ESCAPE:
            self.controller.chose_game('default')
        if key == pygame.K_p:
            self.pause_game()
        # if key == pygame.K_x:
        #     self.game_status = False

    def run(self):
        """Main cycle of game"""
        pass

    def collisions(self):
        pass

    def render(self, *args):
        """Draw objects on game screen"""
        self.get_null_screen()
        for obj in args:
            if obj.get_clean_hit_box():
                for y, x in obj.get_clean_hit_box():
                    self.game_condition[y][x] = 0
            if obj.get_obj():
                for y, x in obj.get_obj():
                    self.game_condition[y][x] = 1

    def get_small_screen_condition(self):
        """Draw objects on small screen"""
        self.get_null_small_screen()
        dic_lives = {
            1: [[3, 0], ],
            2: [[3, 0], [2, 0], ],
            3: [[3, 0], [2, 0], [1, 0], ],
            4: [[3, 0], [2, 0], [1, 0], [0, 0], ],
        }
        if self.lives:
            if isinstance(self.lives, int):
                for y, x in dic_lives[self.lives]:
                    self.small_screen_condition[y][x] = 1
            else:
                shape = self.lives['shape']
                rotation = self.lives['rotation']
                for y, x in shape[rotation]:
                    self.small_screen_condition[y][x] = 1
                self.correct_small_screen_pic()

    def correct_small_screen_pic(self):
        # while sum(self.small_screen_condition[-1]) == 0:
        #     last = self.small_screen_condition.pop()
        #     self.small_screen_condition.insert(0, last)
        if sum(self.small_screen_condition[-1]) == 0:
            last = self.small_screen_condition.pop()
            self.small_screen_condition.insert(0, last)
        if sum(self.small_screen_condition[-1]) == 0:
            last = self.small_screen_condition.pop()
            self.small_screen_condition.insert(0, last)
        if sum(line[0] for line in self.small_screen_condition) == 0:
            for line in self.small_screen_condition:
                last = line.pop(0)
                line.insert(5, last)

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

    # def curtain_clean_effect(self, in_end_func=None):
    #     if self.y_clean_pic != -21:
    #         if self.y_clean_pic >= 0:
    #             self.game_condition[self.y_clean_pic] = [1] * 10
    #         else:
    #             self.game_condition[abs(self.y_clean_pic + 1)] = [0] * 10
    #         self.y_clean_pic -= 1
    #     else:
    #         self.y_clean_pic = 19
    #         if in_end_func:
    #             in_end_func()

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

    @staticmethod
    def array_collision(obj_1, obj_2):
        for pos in obj_1:
            if pos in obj_2:
                return True
        return False

    # def get_small_screen_condition(self):
    #     small_screen = [
    #         [[0, 0], [0, 0], [0, 0], [0, 0]],
    #         [[0, 0], [0, 0], [0, 0], [0, 0]],
    #         [[0, 0], [0, 0], [0, 0], [0, 0]],
    #         [[0, 0], [0, 0], [0, 0], [0, 0]],
    #     ]
    #     dic_lives = {
    #         1: [[3, 0], ],
    #         2: [[3, 0], [2, 0], ],
    #         3: [[3, 0], [2, 0], [1, 0], ],
    #         4: [[3, 0], [2, 0], [1, 0], [0, 0], ],
    #     }
    #     if self.lives:
    #         if isinstance(self.lives, int):
    #             # print(dic_lives[self.lives])
    #             for y, x in dic_lives[self.lives]:
    #                 small_screen[y][x] = 1
    #         else:
    #             shape = self.lives['shape']
    #             rotation = self.lives['rotation']
    #             for y, x in shape[rotation]:
    #                 small_screen[y][x] = 1
    #     self.small_screen_condition = small_screen
