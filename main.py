import time

import pygame

from screen_elements import PixelScreen, Clock
from settings import GameSettings

pygame.init()
pygame.mixer.init()  # для звука
screen = GameSettings.my_screen
pygame.display.set_caption(GameSettings.GAME_CAPTION)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# player = Player()
# all_sprites.add(player)

# Цикл игры
running = True


def get_screen_pic(to_line, to_col):
    pixels_screen = []
    for _ in range(0, 20):
        line = []
        for pixel in range(0, 10):
            line.append(0)
        pixels_screen.append(line)
    pixels_screen[to_line][to_col] = 1
    return pixels_screen


to_show = get_screen_pic(5, 8)
pixel_screen = PixelScreen(screen=screen, start_point=(250, 25), pixel_size=33, pixel_between=1.12, controller=to_show)
my_clock = Clock(screen=screen, start_time=time.time(), mili_secs=False, start_point=(650, 40), width=20)

while running:

    # Держим цикл на правильной скорости
    clock.tick(GameSettings.FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     print('DOWN')
        #     player.last_key(event.key)

    # Обновление

    # all_sprites.update()
    # Рендеринг
    screen.fill(GameSettings.background_color)
    my_clock.show()

    # all_sprites.draw(screen)
    pixel_screen.draw()
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
