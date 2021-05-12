import pygame

from game_objects import Car, RoadBorder
from .default_game_class import Game


class Race(Game):
    """Letter F"""

    def __init__(self, controller, game_mode=None):
        super().__init__(controller=controller, game_mode=game_mode)
        self.player_car = Car(pos=(16, 2))
        self.player = self.player_car
        self.road = RoadBorder()
        self.car = Car(pos=(-2, 2), out_of_screen=True)
        self.game_objects = [self.player_car, self.road, self.car]
        self.start_game()

    def start_game(self):
        super().start_game()

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
            self.road.move()
            self.render(*self.game_objects)
        else:
            self.end_game()
