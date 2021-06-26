from copy import deepcopy

import pygame

from games import Snake, TurretTetris, Race, DrawObjects, Tetris, Tanks
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

letter_F = ([6, 3], [5, 3], [4, 3], [3, 3], [2, 3],
            [2, 4], [4, 4],
            [2, 5], [4, 5],
            [2, 6],
            )

letter_G = ((2, 6), (2, 5), (2, 4), (3, 3), (4, 3), (5, 3), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (4, 5))

tanks_schema = ((18, 0), (19, 0), (18, 1), (17, 1), (18, 2), (19, 2), (14, 1), (14, 4), (15, 4),
                (16, 4), (16, 5), (15, 5), (14, 5), (15, 6), (10, 8), (10, 7), (11, 7), (12, 7), (12, 8), (11, 6))


class GamePreview(Game):
    """Превью доступных игр"""

    games = ['snake', 'turret_tetris', 'race', 'tetris', 'tanks', 'turret_tetris_2', 'draw', ]
    games_data = {
        'snake': {
            'preview': 'game_previews/snake_prev_1.txt',
            'game': Snake,
            'game_mode': 'traffic',
        },
        'turret_tetris': {
            'preview': 'game_previews/turret_prev.txt',
            'game': TurretTetris,
            'game_mode': 'build',
        },
        'turret_tetris_2': {
            'preview': 'game_previews/prev_turret_destroy.txt',
            'game': TurretTetris,
            'game_mode': 'destroy',
        },
        'tanks': {
            'preview': (*letter_E, *tanks_schema),
            'game': Tanks,
            'game_mode': None,
        },
        'draw': {
            'preview': 'game_previews/prev_draw.txt',
            'game': DrawObjects,
            'game_mode': None,
        },
        'race': {
            'preview': 'game_previews/prev_car.txt',
            'game': Race,
            'game_mode': 'traffic',
        },
        'tetris': {
            'preview': 'game_previews/prev_tetris.txt',
            'game': Tetris,
            'game_mode': None,
        },
    }

    def __init__(self, controller, start_game_number=0):
        super().__init__(controller=controller)
        self.game_number = start_game_number
        self.score = 0
        self.frames = {}
        self.frame_count = 0
        self.lives = 0
        self.start_game()

    def draw_game(self):
        game_name = GamePreview.games[self.game_number]
        game_preview = GamePreview.games_data[game_name]['preview']
        if isinstance(game_preview, tuple):
            for y, x in game_preview:
                self.game_condition[y][x] = 1
        else:
            if game_name not in self.frames.keys():
                self.frames[game_name] = self.read_prev_from_file(game_preview)
            frame = self.frames[game_name][self.frame_count].copy()
            self.frame_count += 1
            if self.frame_count > len(self.frames[game_name]) - 1:
                self.frame_count = 0
            self.game_condition = frame

    def run(self):
        self.get_null_screen()
        self.draw_game()

    def game_key_controller(self, key):
        # chose game
        if key == pygame.K_LEFT:
            self.game_number -= 1
            self.frame_count = 0
        elif key == pygame.K_RIGHT:
            self.game_number += 1
            self.frame_count = 0
        elif self.game_number == -1:
            self.game_number = len(GamePreview.games) - 1
        self.game_number %= len(GamePreview.games)
        # level and speed
        if key == pygame.K_UP:
            self.controller.up_speed()
        if key == pygame.K_DOWN:
            self.controller.up_game_level()
        #  start game
        if key == pygame.K_SPACE:
            game = GamePreview.games[self.game_number]
            if GamePreview.games_data[game]['game'] is not None:
                self.controller.last_game = self.game_number
                self.controller.chose_game(game)
            else:
                print('!!!Выбранная игра пока не доступна!!!')

    @staticmethod
    def read_prev_from_file(file_name):
        print(f'Read file {file_name}')
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

    # def start_game(self):
    #     """Иницилизация стартового состояния игры"""
    #     super().start_game()
    # line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # while len(self.game_condition) != 20:
    #     self.game_condition.append(line.copy())
    # self.draw_game()

    # def get_screen_pic(self):
    #     """Передает экрану (он запрашивает эту функцию)
    #     состояние игры"""
    #     return self.game_condition
    #
    # def get_null_screen(self):
    #     self.game_condition.clear()
    #     line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #     while len(self.game_condition) != 20:
    #         self.game_condition.append(line.copy())

    # def render(self):
    #     self.get_null_screen()
    #     self.draw_game()
