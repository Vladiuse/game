import pygame

from game_objects import Tank
from .default_game_class import Game


class Tanks(Game):
    """Clean work game"""

    def __init__(self, controller, game_mode, game_speed, game_level):
        super().__init__(controller, game_mode=game_mode, game_speed=game_speed)
        self.player = Tank((17, 3), model='player', direction='up')
        # self.enemy = Tank((0, 0), model='enemy', direction='down')
        self.enemys = []
        self.bullets = []
        self.shoot_timer = 240
        # self.lives = 3
        self.add_enemy_tanks()
        self.start_game()

    def start_game(self):
        super().start_game()


    def restart_game(self):
        self.lives -= 1
        self.player = Tank((17, 3), model='player', direction='up')
        # self.enemy = Tank((0, 0), model='enemy', direction='down')
        self.enemys = []
        self.bullets = []
        self.shoot_timer = 240
        self.game_status = True
        self.add_enemy_tanks()
        self.start_game()



    def run(self):
        if self.game_status:
            if not self.pause:
                self.collisions()
                self.tanks_auto_shoot()
                for bullet in self.bullets:
                    bullet.move()
                self.del_bullets_out_screen()
                self.render(*self.enemys, *self.bullets, self.player)
        else:
            self.end_game()

    def add_enemy_tanks(self):
        positions = (0,0), (0, 7)
        directions = ('down', 'left')
        for p,d in zip(positions, directions):
            self.enemys.append(Tank(start_pos=p, model='enemy', direction=d))


    def tanks_auto_shoot(self):
        for tank in self.enemys:
            bullet = tank.auto_shot()
            if bullet:
                self.bullets.append(bullet)


    def del_bullets_out_screen(self):
        for bullet_id, bullet in enumerate(self.bullets):
            if not bullet.is_obj_in_screen():
                self.bullets.pop(bullet_id)

    def collisions(self):
        all_tanks = [self.player, *self.enemys]
        for tank in all_tanks:
            for bullet in self.bullets:
                if self.array_collision(tank, bullet):
                    print('COLOOO')
                    if tank.model != bullet.type:
                        if tank.model == 'player':
                            pass # end game
                            print('PLAYER KILLLED')
                            self.game_status = False
                            self.bomb.activate(player=self.player)
                            self.game_objects.append(self.bomb)
                        else:
                            tank.live = bullet.live = False
        alive_enemys = []
        for tank in self.enemys:
            if tank.live:
                alive_enemys.append(tank)
        bullets = []
        for bullet in self.bullets:
            if bullet.live:
                bullets.append(bullet)
        self.bullets = bullets
        self.enemys = alive_enemys


    def game_key_controller(self, key):
        super().game_key_controller(key=key)
        if key == pygame.K_UP:
            if self.player.direction == 'up':
                self.player.move_up()
            else:
                self.player.rotate('up')
        elif key == pygame.K_DOWN:
            if self.player.direction == 'down':
                self.player.move_down()
            else:
                self.player.rotate('down')
        elif key == pygame.K_LEFT:
            if self.player.direction == 'left':
                self.player.move_left()
            else:
                self.player.rotate('left')
        elif key == pygame.K_RIGHT:
            if self.player.direction == 'right':
                self.player.move_right()
            else:
                self.player.rotate('right')
        if not self.player.is_obj_in_screen():
            self.player.move_back()
        if key == pygame.K_SPACE:
            player_bullet = self.player.shot()
            self.bullets.append(player_bullet)
