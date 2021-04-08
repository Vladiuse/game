import pygame
from models import Element, Clock
import time
WIDTH = 1200
HEIGHT = 800
FPS = 30


class Player(pygame.sprite.Sprite):

    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        pygame.draw.ellipse(screen, GREEN,
                            (10, 50, 280, 100))
        self.rect.x += 5
        if self.rect.x > WIDTH:
            self.rect.x = 0




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

# Цикл игры
running = True



my_clock = Clock(screen=screen, start_time=time.time(), mili_secs=True,start_point=(300, 300), width=80)
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
    screen.fill(BLACK)
    my_clock.show()


    # poligon.draw()


    # all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
