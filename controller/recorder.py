from copy import deepcopy


class Recorder:

    def __init__(self, controller, work=False):
        self.controller = controller
        self.frames = []
        self.work = work
        self.record = False

    def start_end_record(self):
        self.record = True if self.record is False else False

    def add_frame(self, frame):
        if self.record:
            frame = tuple(frame)
            self.frames.append(frame)

    def write_record(self):
        letter_G = ((2, 6), (2, 5), (2, 4), (3, 3), (4, 3), (5, 3), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (4, 5))
        letter = letter_G
        with open('prev_draw.txt', 'w') as file:
            for frame in self.frames:
                frame = list(frame)
                # clean half
                for y in range(10):
                    for x in range(10):
                        frame[y][x] = 0
                # add letter on frame
                for y,x in letter:
                    frame[y][x] = 1
                #
                frame_to_write = ''
                for line in frame:
                    line = list(map(lambda x: str(x), line))
                    frame_to_write += ''.join(line)
                frame_to_write += '\n'
                file.write(frame_to_write)
            print('Write!!!')

    # def read_prew(self):
    #     with open('snake_prev.txt') as snake_file:
    #         frames = []
    #         for file_line in snake_file:
    #             file_line = file_line[:-1]
    #             frame = []
    #             frame_line = []
    #             for char in file_line:
    #                 frame_line.append(int(char))
    #                 if len(frame_line) == 10:
    #                     frame.append(deepcopy(frame_line))
    #                     frame_line.clear()
    #             frames.append(deepcopy(frame))
    #     return frames

# if __name__ == '__main__':
# rec = Recorder(controller='1')
# snake_frames = rec.read_prew()
# rec.write_record(mock_frames=snake_frames)
# rec.read_prew()