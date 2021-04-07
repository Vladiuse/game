import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Element:

    def __init__(self, screen, start_point, width, height, percent):
        self.screen = screen
        self.start_point = start_point
        self.width = width
        self.height = height
        self.percent = percent

    def draw(self):
        poligon_coors = self.get_poligon_coords(self.start_point)
        # new = []
        # for i in poligon_coors:
        #     rez = (i[1], i[0])
        #     new.append(rez)

        pygame.draw.polygon(self.screen, WHITE,
                            poligon_coors)

    def get_poligon_coords(self, start_point):
        x = start_point[0]
        y = start_point[1]
        percent = self.height * self.percent / 2
        poligon_coors = ((x, y + percent), (x + self.width / 2, y), (x + self.width, y + percent),
                         (x + self.width, y + self.height - percent), (x + self.width / 2, y + self.height),
                         (x, y + self.height - percent))
        return poligon_coors
