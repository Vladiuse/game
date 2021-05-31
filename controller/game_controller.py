import time
from copy import deepcopy

import pygame

from settings import GameSettings
from games.game_preview import GamePreview
from games.snake import Snake
from screen_elements import Clock, Score, PixelScreen, SmallScreen, SpeedLevel, GameLevel
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
        self.speed_level = SpeedLevel((700, 500), width=25)
        self.game_level = GameLevel(start_point=(700, 650), width=25)
        # game modules
        self.game = GamePreview(controller=self)
        self.recorder = Recorder(controller=self, work=True)

        self.last_game = 0

    def chose_game(self, game_to_run):
        if game_to_run == 'default':
            self.game = GamePreview(controller=self, start_game_number=self.last_game)
        else:
            game = GamePreview.games_data[game_to_run]['game']
            game_mode = GamePreview.games_data[game_to_run]['game_mode']
            game_speed = self.speed_level.speed_level
            game_level = self.game_level.game_level
            print(game_speed, game_level)
            self.game = game(controller=self, game_mode=game_mode,
                             game_speed=game_speed, game_level=game_level)

    def run(self):
        self.game_clock.show(self.game.start_time)
        self.score_controller.show_score(self.game.score)
        self.key_controller()
        self.game.run()
        self.main_screen.draw()
        self.small_screen.draw()
        self.speed_level.show()
        self.game_level.show()

    def key_controller(self):
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                GameSettings.running = False
            elif event.type == pygame.KEYDOWN:
                # for Recorder
                if event.key == pygame.K_r:
                    print('Record')
                    self.recorder.start_end_record()
                elif event.key == pygame.K_w:
                    self.recorder.write_record()
                else:
                    self.game.game_key_controller(event.key)

    def get_screen_pic(self):
        screen = self.game.get_screen_pic()
        #  for Recorder
        if self.recorder.work:
            self.recorder.add_frame(screen)
        return screen

    def up_speed(self):
        self.speed_level.up_speed_level()

    def up_game_level(self):
        self.game_level.up_game_level()

    def get_small_screen_pic(self):
        return self.game.get_small_screen_pic()
