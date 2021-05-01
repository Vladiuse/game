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


# class Player(pygame.sprite.Sprite):
#
#     def __init__(self):
#         # pygame.sprite.Sprite.__init__(self)
#         super().__init__()
#         self.image = pygame.Surface((50, 50))
#         self.image.fill(Colors.GREEN)
#         self.rect = self.image.get_rect()
#         self.rect.center = (800, 500)
#         self.direction = None
#         self.speed = 10
#
#     def update(self):
#
#         if self.rect.x < 0:
#             self.rect.x = GameSettings.SCREEN_WIDTH
#         if self.rect.x > GameSettings.SCREEN_WIDTH:
#             self.rect.x = 0
#         if self.rect.y < 0:
#             self.rect.y = GameSettings.SCREEN_HEIGHT
#         if self.rect.y > GameSettings.SCREEN_HEIGHT:
#             self.rect.y = 0
#         if self.direction is None:
#             pass
#         if self.direction == 'LEFT':
#             self.rect.x -= self.speed
#         if self.direction == 'RIGHT':
#             self.rect.x += self.speed
#         if self.direction == 'UP':
#             self.rect.y -= self.speed
#         if self.direction == 'DOWN':
#             self.rect.y += self.speed
#
#     def last_key(self, key):
#         if key == pygame.K_LEFT:
#             self.direction = 'LEFT'
#         if key == pygame.K_RIGHT:
#             self.direction = 'RIGHT'
#         if key == pygame.K_UP:
#             self.direction = 'UP'
#         if key == pygame.K_DOWN:
#             self.direction = 'DOWN'
