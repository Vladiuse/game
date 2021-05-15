# Lets have some fun ;)
import pygame

from controller import GameController
from settings import GameSettings

pygame.init()
pygame.mixer.init()  # для звука
screen = GameSettings.my_screen
pygame.display.set_caption(GameSettings.GAME_CAPTION)
clock = pygame.time.Clock()

controller = GameController()

if __name__ == '__main__':
    while GameSettings.running:
        clock.tick(GameSettings.FPS)
        screen.fill(GameSettings.background_color)
        controller.run()
        pygame.display.flip()

    pygame.quit()
