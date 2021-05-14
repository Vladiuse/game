import random as r

import pygame

from game_objects import Car, RoadBorder
from .default_game_class import Game


class Race(Game):
    FRAME = 5
    SCORE = 100
    """Letter F"""

    def __init__(self, controller, game_mode=None):
        super().__init__(controller=controller, game_mode=game_mode)
        self.player_car = Car(pos=(16, 2))
        self.player = self.player_car
        self.road = RoadBorder()
        self.cars = []
        self.game_objects = [self.player_car, self.road]
        self.road_map = None
        self.get_road_map()
        self.frame = 1
        self.start_game()

    def start_game(self):
        super().start_game()

    def restart_game(self):
        self.lives -= 1
        self.game_status = True
        self.player_car = Car(pos=(16, 2))
        self.player = self.player_car
        self.road = RoadBorder()
        self.cars = []
        self.game_objects = [self.player_car, self.road]
        self.road_map = None
        self.get_road_map()
        self.frame = 1
        self.start_game()

    def get_road_map(self):
        cars = ['car_l', 'car_r']
        road_map = [r.choice(cars), 0, 0, 0]
        last_car = road_map[0]
        while len(road_map) < 500:
            car = r.choice(cars)
            if last_car != car:
                between = [0] * r.randint(5, 6)
            else:
                between = [0] * r.randint(1, 4)
            last_car = car
            road_map.extend(between)
            road_map.extend([car, 0, 0, 0])
        self.road_map = road_map


    def get_random_cars(self):
        self.frame -= 1
        if self.frame == 0:
            try:
                road_obj = self.road_map[0]
            except IndexError:
                self.get_road_map()
                road_obj = self.road_map[0]
            if road_obj == 'car_r':
                self.cars.append(Car(pos=(-4, 2), out_of_screen=True))
            elif road_obj == 'car_l':
                self.cars.append(Car(pos=(-4, 5), out_of_screen=True))
            self.road_map.pop(0)
            self.frame = Race.FRAME

    def del_out_screen_cars(self):
        cars_in_screen = []
        for car in self.cars:
            y,x = car.get_pos()
            if y < 19:
                cars_in_screen.append(car)
        if len(self.cars) > len(cars_in_screen):
            self.add_score()
        self.cars = cars_in_screen

    def collisions(self):
        for car in self.cars:
            if self.array_collision(self.player, car):
                self.game_status = False
                self.bomb.activate(player=self.player)
                self.game_objects.extend(self.cars)
                self.game_objects.append(self.bomb)

    def run(self):
        if self.game_status:
            if not self.pause:
                self.collisions()
                self.road.move()
                self.get_random_cars()
                self.del_out_screen_cars()
                for car in self.cars:
                    car.move(direction='down')
            self.render(*self.game_objects, *self.cars)
        else:
            self.end_game()

    def game_key_controller(self, key):
        super().game_key_controller(key=key)
        if key == pygame.K_LEFT:
            self.player_car.move_left()
        elif key == pygame.K_RIGHT:
            self.player_car.move_right()

    def add_score(self):
        self.score += Race.SCORE

    # def collisions(self):
    #     for pos in self.player.get_obj():
    #         for car in self.cars:
    #             if pos in car.get_obj():
    #                 self.game_status = False
    #                 self.bomb.activate(player=self.player)
    #                 self.game_objects.extend(self.cars)
    #                 self.game_objects.append(self.bomb)
