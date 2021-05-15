import time
from copy import deepcopy

import pygame

from games.game_preview import GamePreview
from games.snake import Snake
from screen_elements import Clock, Score, PixelScreen, SmallScreen
from settings import GameSettings
from .recorder import Recorder

screen = GameSettings.my_screen


class GameController:
    """Отслеживает нажимаемые клаиши
     - передает их в игру"""

    def __init__(self):
        # Screen elements
        self.score_controller = Score((700, 120), width=20)
        self.game_clock = Clock(start_time=time.time(), mili_secs=False)
        self.main_screen = PixelScreen(controller=self)
        self.small_screen = SmallScreen(controller=self)
        # game modules
        self.game = GamePreview(controller=self)
        self.recorder = Recorder(controller=self)

        self.last_game = 0

    def chose_game(self, game_to_run):
        if game_to_run == 'default':
            self.game = GamePreview(controller=self, start_game_number=self.last_game)
        else:
            game = GamePreview.games_data[game_to_run]['game']
            game_mode = GamePreview.games_data[game_to_run]['game_mode']
            self.game = game(controller=self, game_mode=game_mode)

    def run(self):
        self.game_clock.show(self.game.start_time)
        self.score_controller.show_score(self.game.score)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                GameSettings.running = False
            # # for Recorder
            elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_r:
                #         print('Record')
                #         self.recorder.show_record()
                self.game.game_key_controller(event.key)
        self.game.run()
        self.main_screen.draw()
        self.small_screen.draw()

    def get_screen_pic(self):
        """For Recorder"""
        if isinstance(self.game, Snake):
            screen = self.game.get_screen_pic()
            screen = deepcopy(screen)
            self.recorder.add_screen_to_data(screen)
        return self.game.get_screen_pic()

    def get_small_screen_pic(self):
        return self.game.get_small_screen_pic()


# class Recorder:
#
#     def __init__(self, controller, on=False):
#         self.controller = controller
#         self.record = []
#         self.snake_frames = []
#
#     def add_screen_to_data(self, screen):
#         sc = screen
#         self.record.append(sc)
#
#     def show_record(self):
#         print(len(self.record))
#         self.write_record()
#
#     def write_record(self, mock_frames=None):
#
#         if mock_frames:
#             self.record = mock_frames
#         # отрисовка буквы на каждый frame
#         # for frame in self.record:
#         #     for y,x in letter_A:
#         #         frame[y][x] = 1
#         with open('snake_prev_1.txt', 'w') as file:
#             for frame in self.record:
#                 frame_to_write = ''
#                 for line in frame:
#                     line = list(map(lambda x: str(x), line))
#                     frame_to_write += ''.join(line)
#                 frame_to_write += '\n'
#                 file.write(frame_to_write)
#             print('Write!!!')
#
#     def read_prew(self):
#         with open('snake_prev.txt') as snake_file:
#             frames = []
#             for file_line in snake_file:
#                 file_line = file_line[:-1]
#                 frame = []
#                 frame_line = []
#                 for char in file_line:
#                     frame_line.append(int(char))
#                     if len(frame_line) == 10:
#                         frame.append(deepcopy(frame_line))
#                         frame_line.clear()
#                 frames.append(deepcopy(frame))
#         return frames
        # print(frames)
        # print(len(frames))

# if __name__ == '__main__':
# rec = Recorder(controller='1')
# snake_frames = rec.read_prew()
# rec.write_record(mock_frames=snake_frames)
# rec.read_prew()
