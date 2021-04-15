import time

import pygame


class PlayerWalk:

    def __init__(self):
        self.game_status = True
        self.game_condition = []
        self.start_game()
        self.score = 0
        self.start_time = time.time()
        self.player = Player((5, 18))

    def get_screen_pic(self):
        """Передает экрану (он запрашивает эту функцию)
        состояние игры"""
        return self.game_condition

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())

    def run(self):
        if self.game_status:
            self.render_pic()

    def game_key_controller(self, key):
        """Меняет флаг направление движения -
        изменение на противоположное не проходит"""
        self.player.move(key)

    def clear_screen(self):
        self.game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())

    def render_pic(self):
        self.clear_screen()
        for y, x in self.player.get_obj():
            self.game_condition[y][x] = 1


class Player:

    def __init__(self, start_point):
        self.x, self.y = start_point

    def get_obj(self):
        obj = []
        elements = (self.y, self.x),(self.y + 1, self.x),(self.y + 1, self.x - 1), (self.y + 1, self.x + 1)
        for y, x in elements:
            if y in range(0, 20) and x in range(0, 10):
                obj.append([y, x])
        return obj

    def move(self, key):
        if key == pygame.K_LEFT:
            if self.x != 0:
                self.x -= 1
        elif key == pygame.K_RIGHT:
            if self.x != 9:
                self.x += 1
        # elif key == pygame.K_UP:
        #     self.y -= 1
        # elif key == pygame.K_DOWN:
        #     self.y += 1
