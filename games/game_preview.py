from copy import deepcopy

import pygame

from games import Snake, TurretTetris, Race, DrawObjects, Tetris
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

turret_schema_B = [(19, 5), (19, 6), (18, 6), (19, 7), (10, 0), (10, 1),
                   (10, 3), (10, 4), (10, 5), (10, 8), (10, 9),
                   (11, 9), (11, 7), (11, 6), (11, 5), (11, 4), (11, 3),
                   (11, 1), (11, 2), (12, 0), (12, 1), (12, 3),
                   (12, 5), (16, 6), (12, 6), (13, 6), (14, 6), (12, 7), (12, 9)]

letter_C = ([5, 3], [4, 3], [3, 3],
            [6, 4], [6, 5], [6, 6],
            [2, 4], [2, 5], [2, 6],
            )
turret_schema_C = [(19, 4), (19, 3), (18, 4), (19, 5), (16, 4),
                   (10, 0), (10, 1), (10, 3), (10, 5), (10, 4),
                   (11, 5), (11, 4), (10, 6), (11, 7), (10, 8),
                   (11, 9), (12, 3), (12, 2), (11, 1), (12, 0),
                   (12, 6), (12, 8), (12, 9)]

letter_D = ([6, 3], [5, 3], [4, 3], [3, 3], [2, 3],
            [6, 4], [2, 4],
            [6, 5], [2, 5],
            [5, 6], [4, 6], [3, 6],
            )

snake_schema = [(17, 5), (16, 5), (15, 5), (15, 4), (15, 1), (15, 3), (17, 6)]

letter_E = ([6, 3], [5, 3], [4, 3], [3, 3], [2, 3],
            [6, 4], [2, 4], [4, 4],
            [6, 5], [2, 5], [4, 5],
            [6, 6], [2, 6],
            )
draw_schema = [(11, 1), (11, 2), (12, 1), (12, 2),
               (11, 8), (11, 7), (12, 7), (12, 8),
               (13, 6), (13, 3), (14, 4), (14, 5),
               (15, 5), (15, 4), (16, 3), (16, 6),
               (17, 7), (17, 2), (17, 1), (18, 1),
               (18, 2), (18, 7), (17, 8), (18, 8)]

letter_F = ([6, 3], [5, 3], [4, 3], [3, 3], [2, 3],
            [2, 4], [4, 4],
            [2, 5], [4, 5],
            [2, 6],
            )
car_schema = ((18, 0), (17, 0), (16, 0), (13, 0), (12, 0), (11, 0), (11, 9),
              (12, 9), (13, 9), (16, 9), (17, 9), (18, 9), (19, 2), (19, 3),
              (19, 4), (18, 3), (17, 2), (17, 3), (17, 4), (16, 3), (14, 5),
              (14, 6), (14, 7), (13, 6), (12, 6), (12, 5), (12, 7), (11, 6))

tetris = ((19, 0), (19, 1), (19, 2), (19, 3), (18, 3), (18, 2), (18, 1),
          (17, 1), (17, 2), (19, 4), (18, 5), (19, 5), (19, 6), (18, 6),
          (18, 7), (19, 7), (19, 8), (15, 3), (15, 4), (16, 4), (14, 3),
          (19, 9), (18, 9), (17, 9), (2, 5), (2, 4), (2, 3), (2, 6), (2, 7),
          (2, 2), (3, 4), (3, 5), (4, 5), (4, 4), (5, 4), (5, 5), (6, 5),
          (6, 4), (3, 3), (3, 2), (3, 7), (3, 6), (7, 5), (7, 4))


class GamePreview(Game):
    """Превью доступных игр"""

    games = ['snake', 'turret_tetris', 'race',  'tetris','turret_tetris_2', 'draw', ]
    games_data = {
        'snake': {
            'preview': 'game_previews/snake_prev_1.txt', 'game': Snake, 'game_mode': 'traffic',
        },
        # 'turret_tetris': {
        #     'preview': (*letter_B, *turret_schema_B), 'game': TurretTetris, 'game_mode': 'build',
        # },
        'turret_tetris': {
            'preview': 'game_previews/turret_prev.txt', 'game': TurretTetris, 'game_mode': 'build',
        },
        'turret_tetris_2': {
            'preview': (*letter_C, *turret_schema_C), 'game': TurretTetris, 'game_mode': 'destroy',
        },

        'draw': {
            'preview': (*letter_D, *draw_schema), 'game': DrawObjects, 'game_mode': None,
        },
        # 'race': {
        #     'preview': (*letter_E, *car_schema), 'game': Race, 'game_mode': 'traffic',
        # },
        'race': {
            'preview': 'game_previews/prev_car.txt', 'game': Race, 'game_mode': 'traffic',
        },
        'tetris': {
            'preview': 'game_previews/prev_tetris.txt', 'game': Tetris, 'game_mode': None,
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
        game_data = GamePreview.games_data[game_name]['preview']
        if isinstance(game_data, tuple):
            for y, x in game_data:
                self.game_condition[y][x] = 1
        else:
            if game_name not in self.frames.keys():
                self.frames[game_name] = self.read_prev_from_file(game_data)
            frame = self.frames[game_name][self.frame_count].copy()
            self.frame_count += 1
            if self.frame_count > len(self.frames[game_name]) - 1:
                self.frame_count = 0
            self.game_condition = frame
            # return frame

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
                print('Выбранная игра пока не доступна!!!')

    def read_prev_from_file(self, file_name):
        print('Read file')
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
