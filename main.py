import time

import pygame

from screen_elements import PixelScreen, Clock, Score
from settings import GameSettings
from game_01 import GameController, Snake
from games.game_test import PlayerWalk

pygame.init()
pygame.mixer.init()  # для звука
screen = GameSettings.my_screen
pygame.display.set_caption(GameSettings.GAME_CAPTION)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# player = Player()
# all_sprites.add(player)


main_game = Snake(game_mode='traffic', game_speed=5)
test_game = PlayerWalk()


# pixel_screen = PixelScreen(game=main_game)
pixel_screen = PixelScreen(game=test_game)
my_clock = Clock(start_time=time.time(), mili_secs=False)
game_score_controller = Score((650, 120), width=20)
controller = GameController(game=test_game, score_controller=game_score_controller, game_clock=my_clock)

# Цикл игры
while GameSettings.running:

    # Держим цикл на правильной скорости
    clock.tick(GameSettings.FPS)
    # Ввод процесса (события)
    # controller.run(player)


    # Обновление

    all_sprites.update()
    # Рендеринг
    screen.fill(GameSettings.background_color)
    controller.run()
    # my_clock.show()
    test_game.run()
    pixel_screen.draw()
    # all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
