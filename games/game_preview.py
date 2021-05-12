import time
from copy import deepcopy

import pygame

from games.snake import Snake, SnakeCopy
from games.turret_tetris import TurretTetris
from .default_game_class import Game

letter_A = [[6, 3], [5, 3], [4, 3], [3, 3],
            [4, 4], [2, 4],
            [4, 5], [2, 5],
            [6, 6], [5, 6], [4, 6], [3, 6],
            ]

letter_B = ([6, 3], [5, 3], [4, 3], [3, 3], [2, 3],
            [6, 4], [2, 4], [4, 4],
            [6, 5], [2, 5], [4, 5],
            [5, 6], [3, 6],
            )

letter_C = ([5, 3], [4, 3], [3, 3],
            [6, 4], [6, 5], [6, 6],
            [2, 4], [2, 5], [2, 6],
            )

letter_D = ([6, 3], [5, 3], [4, 3], [3, 3], [2, 3],
            [6, 4], [2, 4],
            [6, 5], [2, 5],
            [5, 6], [4, 6], [3, 6],
            )

letter_E = ([6, 3], [5, 3], [4, 3], [3, 3], [2, 3],
            [6, 4], [2, 4], [4, 4],
            [6, 5], [2, 5], [4, 5],
            [6, 6], [2, 6],
            )


class GamePreview(Game):
    """Превью доступных игр"""

    games = ['snake', 'turret_tetris', 'turret_tetris_2',  'game_d', 'center',]
    games_data = {
        'snake': {
            'preview': 'game_previews/snake_prev_1.txt', 'game': Snake, 'game_mode': 'traffic',
        },
        'turret_tetris': {
            'preview': letter_B, 'game': TurretTetris, 'game_mode': 'build',
        },
        'turret_tetris_2': {
            'preview': letter_C, 'game': TurretTetris, 'game_mode': 'destroy',
        },
        'game_d': {
            'preview': letter_D, 'game': SnakeCopy, 'game_mode': 'traffic',
        },
        'center': {
            'preview': letter_E, 'game': None, 'game_mode': None,
        },
    }

    def __init__(self, controller):
        super().__init__(controller=controller)
        self.__game_condition = []
        self.game_number = 0
        self.start_time = time.time()
        self.score = 0
        self.frames = None
        self.frame_count = 0
        self.game_status = True
        self.lives = 1
        self.start_game()

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
        if isinstance(game_data, tuple):
            for y, x in game_data:
                self.__game_condition[y][x] = 1
        else:
            self.frames = self.read_snake_prev(game_data)
            frame = self.frames[self.frame_count]
            self.frame_count += 1
            if self.frame_count > len(self.frames) - 1:
                self.frame_count = 0
            self.__game_condition = frame
            # return frame

    def run(self):
        self.render()

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
                print('Выбранная игра пока не доступна!!!')

    def read_snake_prev(self, file_name):
        with open(file_name) as snake_file:
            frames = []
            for file_line in snake_file:
                file_line = file_line[:-1]
                frame = []
                frame_line = []
                for char in file_line:
                    frame_line.append(int(char))
                    if len(frame_line) == 10:
                        frame.append(deepcopy(frame_line))
                        frame_line.clear()
                frames.append(deepcopy(frame))
        return frames
