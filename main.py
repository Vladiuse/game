import time

import pygame

from screen_elements import PixelScreen, Clock
from settings import GameSettings
from game_01 import Player, GameController, PixelWalk

pygame.init()
pygame.mixer.init()  # для звука
screen = GameSettings.my_screen
pygame.display.set_caption(GameSettings.GAME_CAPTION)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# player = Player()
# all_sprites.add(player)


main_game = PixelWalk(game_mode='step')


pixel_screen = PixelScreen(game=main_game)
my_clock = Clock(start_time=time.time(), mili_secs=False, start_point=(650, 40), width=20)
controller = GameController(main_game)
# Цикл игры
while GameSettings.running:

    # Держим цикл на правильной скорости
    clock.tick(GameSettings.FPS)
    # Ввод процесса (события)
    # controller.run(player)
    controller.run()

    # Обновление

    all_sprites.update()
    # Рендеринг
    screen.fill(GameSettings.background_color)
    my_clock.show()
    main_game.run()
    pixel_screen.draw()
    # all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
