from .default_game_class import Game
from game_objects import Car
import pygame

class Race(Game):

    """Letter F"""

    def __init__(self, controller, game_mode=None):
        super().__init__(controller=controller, game_mode=game_mode)
        self.player_car = Car(pos=(16,2))
        self.player = self.player_car
        self.game_objects = [self.player_car]

    def start_game(self):
        super().start_game()
        pass

    def restart_game(self):
        pass

    def game_key_controller(self, key):
        super().game_key_controller(key=key)
        if key == pygame.K_LEFT:
            self.player_car.move_left()
        elif key == pygame.K_RIGHT:
            self.player_car.move_right()
        pass

    def run(self):
        if self.game_status:
            self.render(*self.game_objects)
        else:
            self.end_game()



