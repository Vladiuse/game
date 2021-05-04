import time
import time

import pygame

from games.draw_line import PlayerWalk
from games.snake import Snake
from games.game_default import GamePreview
from screen_elements import Clock, Score, PixelScreen
from settings import GameSettings

screen = GameSettings.my_screen


class GameController:
    """Отслеживает нажимаемые клаиши
     - передает их в игру"""

    def __init__(self):
        self.game = GamePreview(controller=self)
        # self.chose_game(game)
        self.score_controller = Score((650, 120), width=20)
        self.game_clock = Clock(start_time=time.time(), mili_secs=False)
        self.main_screen = PixelScreen(controller=self)

    def chose_game(self, game):
        if game == 'default':
            self.game = GamePreview(controller=self)
        else:
            game = GamePreview.games_data[game]['game']
            self.game = game(controller=self)
        # elif game == 'snake':
        #     self.game = Snake(controller=self)
        # elif game == 'walk':
        #     self.game = PlayerWalk(controller=self)

    def run(self):
        self.game_clock.show(self.game.start_time)
        self.score_controller.show_score(self.game.score)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                GameSettings.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.game_key_controller(event.key)
        self.game.run()
        self.main_screen.draw()

    def get_screen_pic(self):
        return self.game.get_screen_pic()


