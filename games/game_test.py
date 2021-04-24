import time

import pygame


class Counter:

    @staticmethod
    def render_counter_param(n):
        counter = 0

        def render_counter(func):
            def surrogate(*args, **kwargs):
                nonlocal counter
                counter += 1
                if counter == n:
                    counter = 0
                    return func(*args, **kwargs)

            return surrogate

        return render_counter


def render_counter_param(n):
    counter = 0

    def render_counter(func):
        def surrogate(*args, **kwargs):
            nonlocal counter
            counter += 1
            if counter == n:
                counter = 0
                return func(*args, **kwargs)

        return surrogate

    return render_counter


class PlayerWalk:

    max_bullet_count = 3

    def __init__(self):
        self.game_status = True
        self.__game_condition = []
        self.start_game()
        self.score = 0
        self.start_time = time.time()
        self.player = Player((5, 18))
        self.bullets = []
        self.wall = Wall((0,0))


    def get_screen_pic(self):
        """Передает экрану (он запрашивает эту функцию)
        состояние игры"""
        return self.__game_condition

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.__game_condition) != 20:
            self.__game_condition.append(line.copy())

    def run(self):
        if self.game_status:
            for bullet in self.bullets:
                bullet.move()
            self.render_pic()

    def game_key_controller(self, key):
        if key == pygame.K_UP:
            self.create_bullet()
        else:
            self.player.move(key)

    def create_bullet(self):
        if len(self.bullets) != PlayerWalk.max_bullet_count:
            y, x = self.player.get_position()
            bullet = Bullet((y - 1, x))
            self.bullets.append(bullet)

    def clear_screen(self):
        self.__game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.__game_condition) != 20:
            self.__game_condition.append(line.copy())

    def render_pic(self):
        self.collision()
        self.clear_screen()
        self.draw_player()
        self.draw_bullet()
        self.draw_wall()

    def draw_player(self):
        for y, x in self.player.get_obj():
            self.__game_condition[y][x] = 1

    def draw_bullet(self):
        if self.bullets:
            self.check_bullet_in_screen()
            for bullet in self.bullets:
                y,x = bullet.get_obj()
                self.__game_condition[y][x] = 1


    def check_bullet_in_screen(self):
        """Удаление пуль вышедших за экран"""
        for bullet_id, bullet in enumerate(self.bullets):
            y, x = bullet.get_obj()
            if y == -1:
                self.bullets.pop(bullet_id)

    def collision(self):
        """Уладения блока от пули"""
        wall = self.wall.get_obj()
        if self.bullets:
            for bullet_id, bullet in enumerate(self.bullets):
                y, x = bullet.get_obj()
                if (y, x) in wall:
                    self.wall.drop_brick((y, x))
                    self.bullets.pop(bullet_id)
                    self.score += 1

    # def collision(self):
    #     if self.bullets:
    #         for bullet_id, bullet in enumerate(self.bullets):
    #             y, x = bullet.get_obj()
    #             if (y, x) in self.wall.get_obj():
    #                 self.wall.add_brick((y + 1, x))
    #                 self.bullets.pop(bullet_id)
    #                 self.score += 1


    def draw_wall(self):
        for y,x in self.wall.get_obj():
            self.__game_condition[y][x] = 1



class Player:

    def __init__(self, start_point):
        self.x, self.y = start_point

    def get_obj(self):
        obj = []
        elements = (self.y, self.x), (self.y + 1, self.x), (self.y + 1, self.x - 1), (self.y + 1, self.x + 1)
        for y, x in elements:
            if y in range(0, 20) and x in range(0, 10):
                obj.append([y, x])
        return obj

    def move(self, key):
        if key == pygame.K_LEFT:
            if self.x != 0:
                self.x -= 1
        elif key == pygame.K_RIGHT:
            if self.x != 9:
                self.x += 1

    def get_position(self):
        return self.y, self.x

class Wall:

    def __init__(self, start_point):
        self.x = start_point[1]
        self.y = start_point[0]
        self.obj = self.__init_wall()

    def get_obj(self):
        return self.obj

    def __init_wall(self):
        wall = []
        for y in range(3):
            for x in range(10):
                pos = (y, x)
                wall.append(pos)
        return wall

    def drop_brick(self, brick_pos):
        self.obj.remove(brick_pos)

    def add_brick(self, brick_pos):
        self.obj.append(brick_pos)




class Bullet:

    def __init__(self, start_point, direction=None):
        self.x = start_point[1]
        self.y = start_point[0]
        self.direction = 'UP' if direction is None else direction
        self.counter = 0
        self.counter = 15

    def __str__(self):
        # return str(self.y) + ' - ' + str(self.x)
        return f'Bullet: y:{self.y} x:{self.x}'

    # @Counter.render_counter_param(30)
    def move(self):
        if self.direction == 'UP':
            self.y -= 1

    def get_obj(self):
        return self.y, self.x
