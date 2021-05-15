from .default_game_class import Game


class SomeGame(Game):
    """Clean work game"""

    def __init__(self, controller, game_mode):
        super().__init__(controller, game_mode=game_mode)
        self.start_game()

    def start_game(self):
        super().start_game()

    def restart_game(self):
        pass

    def run(self):
        if self.game_status:
            if not self.pause:
                pass
                # self.render(*self.game_objects)
        else:
            self.end_game()

    def collisions(self):
        pass

    def game_key_controller(self, key):
        super().game_key_controller(key=key)


