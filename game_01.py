import time
import time
from copy import deepcopy
import pygame

from games.draw_line import PlayerWalk
from games.snake import Snake
from games.game_default import GamePreview
from screen_elements import Clock, Score, PixelScreen
from settings import GameSettings

screen = GameSettings.my_screen


class GameController:
    """Отслеживает нажимаемые клаиши
     - передает их в игру"""

    def __init__(self):
        self.game = GamePreview(controller=self)
        # self.chose_game(game)
        self.score_controller = Score((650, 120), width=20)
        self.game_clock = Clock(start_time=time.time(), mili_secs=False)
        self.main_screen = PixelScreen(controller=self)
        self.recorder = Recorder(controller=self)

    def chose_game(self, game):
        if game == 'default':
            self.game = GamePreview(controller=self)
        else:
            game = GamePreview.games_data[game]['game']
            self.game = game(controller=self)
        # elif game == 'snake':
        #     self.game = Snake(controller=self)
        # elif game == 'walk':
        #     self.game = PlayerWalk(controller=self)

    def run(self):
        self.game_clock.show(self.game.start_time)
        self.score_controller.show_score(self.game.score)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                GameSettings.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print('Record')
                    self.recorder.show_record()
                self.game.game_key_controller(event.key)
        self.game.run()
        self.main_screen.draw()

    def get_screen_pic(self):
        if isinstance(self.game, Snake):
            screen = self.game.get_screen_pic()
            screen = deepcopy(screen)
            self.recorder.add_screen_to_data(screen)
        return self.game.get_screen_pic()


class Recorder:

    def __init__(self, controller):
        self.controller = controller
        self.record = []
        self.snake_frames = []

    def add_screen_to_data(self, screen):
        sc = screen
        self.record.append(sc)

    def show_record(self):
        print(len(self.record))
        self.write_record()

    def write_record(self):
        with open('snake_prew.txt', 'w') as file:
            for frame in self.record:
                frame_to_write = ''
                for line in frame:
                    line = list(map(lambda x: str(x), line))
                    frame_to_write += ''.join(line)
                frame_to_write += '\n'

                file.write(frame_to_write)
            print('Write!!!')

    def read_prew(self):
        with open('snake_prew.txt') as snake_file:
            frames = []
            for file_line in snake_file:
                file_line = file_line[:-1]
                frame = []
                frame_line = []
                for char in file_line:
                    frame_line.append(int(char))
                    if len(frame_line) == 10:
                        frame.append(deepcopy(frame_line))
                        frame_line.clear()
                frames.append(deepcopy(frame))
        # print(frames)
        # print(len(frames))

# rec = Recorder(controller='1')
# rec.read_prew()









