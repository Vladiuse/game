import time
from copy import deepcopy
import pygame

from games.draw_line import PlayerWalk
from games.snake import Snake


class GamePreview:
    """Превью доступных игр"""

    games = ['snake', 'walk', 'center']
    games_data = {
        'snake': {
            #  'preview': [[8, 5], [7, 5], [6, 5], [0, 0]], 'game': Snake
            'preview': 'snake_prew.txt', 'game': Snake
        },
        'walk': {
            'preview': ([18, 5], [19, 5], [19, 6], [19, 4]), 'game': PlayerWalk
        },
        'center': {
            'preview': ([0, 0], [0, 9], [19, 0], [19, 9]), 'game': None
        }
    }

    def __init__(self, controller):
        self.__game_condition = []
        self.game_number = 0
        self.start_time = time.time()
        self.score = 0
        self.controller = controller
        self.frames = None
        self.frame_count = 0
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
            self.frames = self.read_snake_prew(game_data)
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


    def read_snake_prew(self, file_name):
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
        # print(frames)
        # print(len(frames))

