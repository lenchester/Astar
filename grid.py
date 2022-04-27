import pygame

from field import *


class Grid:
    def __init__(self, rows, width):
        self.fieldlist = []
        gap = width // rows
        for i in range(rows):
            self.fieldlist.append([])
            for j in range(rows):
                spot = Field(i, j, gap, rows)
                if (i == 9 and j > 9) or (3 < i < 10 and j == 10) or (i == 16 and j < 10):
                    spot.make_barrier()

                self.fieldlist[i].append(spot)

    def draw_grid(self, win, rows, width):
        for y in range(rows):
            for x in range(rows):
                rect = pygame.Rect(x*(width//rows), y*(width//rows),width//rows, width//rows )
                pygame.draw.rect(win, BLACK, rect, 1)

    @property
    def get_fieldlist(self):
        return self.fieldlist
