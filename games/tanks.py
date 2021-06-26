from .default_game_class import Game
from game_objects import Tank
import pygame


class Tanks(Game):
    """Clean work game"""

    def __init__(self, controller, game_mode, game_speed, game_level):
        super().__init__(controller, game_mode=game_mode, game_speed=game_speed)
        self.player = Tank((17,3), model='player',direction='up')
        self.game_objects = [self.player]
        self.bullets = []
        self.start_game()

    def start_game(self):
        super().start_game()

    def restart_game(self):
        pass

    def run(self):
        if self.game_status:
            if not self.pause:
                # print(len(self.bullets))
                for bullet in self.bullets:
                    bullet.move()
                self.del_bullets_out_screen()
                self.render(*self.game_objects, *self.bullets)
        else:
            self.end_game()

    def del_bullets_out_screen(self):
        for bullet_id, bullet in enumerate(self.bullets):
            if not bullet.is_obj_in_screen():
                self.bullets.pop(bullet_id)



    def collisions(self):
        pass

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






