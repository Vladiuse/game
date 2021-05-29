from copy import deepcopy


class Recorder:

    def __init__(self, controller, on=False):
        self.controller = controller
        self.record = []
        self.snake_frames = []

    def add_screen_to_data(self, screen):
        sc = screen
        self.record.append(sc)

    def show_record(self):
        print(len(self.record))
        self.write_record()

    def write_record(self, mock_frames=None):

        if mock_frames:
            self.record = mock_frames
        # отрисовка буквы на каждый frame
        # for frame in self.record:
        #     for y,x in letter_A:
        #         frame[y][x] = 1
        with open('snake_prev_1.txt', 'w') as file:
            for frame in self.record:
                frame_to_write = ''
                for line in frame:
                    line = list(map(lambda x: str(x), line))
                    frame_to_write += ''.join(line)
                frame_to_write += '\n'
                file.write(frame_to_write)
            print('Write!!!')

    def read_prew(self):
        with open('snake_prev.txt') as snake_file:
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
        return frames

# if __name__ == '__main__':
# rec = Recorder(controller='1')
# snake_frames = rec.read_prew()
# rec.write_record(mock_frames=snake_frames)
# rec.read_prew()