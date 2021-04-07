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
        # self.start_point = (100, 100)
        x = self.start_point[0]
        y = self.start_point[1]
        coof = self.width/20

        polygon_coors_1 = self.get_polygon_coords((x, y), horizontal=True)
        # polygon_coors_2 = (45, 155) # (50 +- 5)
        polygon_coors_2 = (x - coof*11, y + coof*11)
        polygon_coors_2 = self.get_polygon_coords(polygon_coors_2)
        polygon_coors_3 = (455, 155)
        polygon_coors_3 = (x + self.height - coof*9, y + coof*11)
        polygon_coors_3 = self.get_polygon_coords(polygon_coors_3)
        polygon_coors_4 = (510, 100)
        polygon_coors_4 = (x + self.height + coof*2, 100)
        polygon_coors_4 = self.get_polygon_coords(polygon_coors_4, horizontal=True)

        polygon_coors_6 = (45, 565)
        polygon_coors_6 = (x - coof*11, y + self.height + coof*13)
        polygon_coors_6 = self.get_polygon_coords(polygon_coors_6)
        polygon_coors_7 = (455, 565)
        polygon_coors_7 = (x + self.height - coof*9, y + self.height + coof*13)
        polygon_coors_7 = self.get_polygon_coords(polygon_coors_7)
        polygon_coors_8 = (920, 100)
        polygon_coors_8 = (x + self.height*2 + coof*4, y)
        polygon_coors_8 = self.get_polygon_coords(polygon_coors_8, horizontal=True)



        pygame.draw.polygon(self.screen, WHITE,polygon_coors_1)
        pygame.draw.polygon(self.screen, WHITE,polygon_coors_2)
        pygame.draw.polygon(self.screen, WHITE,polygon_coors_3)
        pygame.draw.polygon(self.screen, WHITE,polygon_coors_4)

        pygame.draw.polygon(self.screen, WHITE,polygon_coors_6)
        pygame.draw.polygon(self.screen, WHITE,polygon_coors_7)
        pygame.draw.polygon(self.screen, WHITE,polygon_coors_8)


    def get_polygon_coords(self, start_point, horizontal=False):
        x = start_point[0]
        y = start_point[1]
        percent = self.height * self.percent / 2
        polygon_coors = ((x, y + percent), (x + self.width / 2, y), (x + self.width, y + percent),
                         (x + self.width, y + self.height - percent), (x + self.width / 2, y + self.height),
                         (x, y + self.height - percent))
        if horizontal:
            new = []
            for (x,y) in polygon_coors:
                new.append((y, x))
            return new
        return polygon_coors
