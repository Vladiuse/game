import pygame
import random as r
import time

WIDTH = 480
HEIGHT = 360
FPS = 30

class Player(pygame.sprite.Sprite):

    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        pygame.draw.ellipse(screen, GREEN,
                            (10, 50, 280, 100))
        self.rect.x += 5
        if self.rect.x > WIDTH:
            self.rect.x = 0
#
# class Figure:
#
#     def __init__(self):


pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)







player = Player()
all_sprites.add(player)
pygame.draw.circle(screen, BLACK, (100, 200), 30,10)
# Цикл игры
running = True

x = 100
y = 100
start = time.time()
count = 0
while running:

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Обновление

    # all_sprites.update()


    # Рендеринг
    count += 1
    # end = time.time()
    # print(f'count is {count}, time is {round(end-start)}')
    screen.fill(WHITE)
    pygame.draw.circle(screen, GREEN,(x, y), 20)

    x += 5
    if x > 300:
        x = 50
        y += 50

    # all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()