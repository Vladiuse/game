import time

import pygame

from games.draw_line import PlayerWalk
from games.snake import Snake


class GamePreview:
    """Превью доступных игр"""

    games = ['snake', 'walk', 'center']
    games_data = {
        'snake': {
            'preview': [[8, 5], [7, 5], [6, 5], [0, 0]], 'game': Snake
        },
        'walk': {
            'preview': [[18, 5], [19, 5], [19, 6], [19, 4]], 'game': PlayerWalk
        },
        'center': {
            'preview': [[0, 0], [0, 9], [19, 0], [19, 9]], 'game': None
        }
    }

    def __init__(self, controller):
        self.__game_condition = []
        self.game_number = 0
        self.start_game()
        self.start_time = time.time()
        self.score = 0
        self.controller = controller

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.__game_condition) != 20:
            self.__game_condition.append(line.copy())
        self.draw_game()

    def get_screen_pic(self):
        """Передает экрану (он запрашивает эту функцию)
        состояние игры"""
        return self.__game_condition

    def clear_screen(self):
        self.__game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.__game_condition) != 20:
            self.__game_condition.append(line.copy())

    def render(self):
        self.clear_screen()
        self.draw_game()

    def draw_game(self):
        game_name = GamePreview.games[self.game_number]
        game_data = GamePreview.games_data[game_name]['preview']
        for y, x in game_data:
            self.__game_condition[y][x] = 1

    def run(self):
        self.render()
        pass

    def game_key_controller(self, key):
        if key == pygame.K_LEFT:
            self.game_number -= 1
        elif key == pygame.K_RIGHT:
            self.game_number += 1
        elif self.game_number == -1:
            self.game_number = len(GamePreview.games) - 1
        self.game_number %= len(GamePreview.games)
        if key == pygame.K_SPACE:
            game = GamePreview.games[self.game_number]
            if game != 'center':  # игра заглушка
                self.controller.chose_game(game)
            else:
                'Выбранная игра пока не доступна!!!'
