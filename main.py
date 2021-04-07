import pygame
import random as r

WIDTH = 480
HEIGHT = 360
FPS = 30

pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление

    # Рендеринг
    screen.fill(WHITE)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()