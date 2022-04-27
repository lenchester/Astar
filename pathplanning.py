from queue import PriorityQueue
from grid import *
from field import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 500
ROWS = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()



def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def reconstruct_path(grid, came_from, current):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw(screen, grid, ROWS, WIDTH)



def astar(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {field: float("inf") for row in grid.fieldlist for field in row}
    g_score[start] = 0
    f_score = {field: float("inf") for row in grid.get_fieldlist for field in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}  # stores everything what open_set stores

    while not open_set.empty():
        current = open_set.get()[2]  # only node
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(grid, came_from, end)
            end.make_end()
            return True

        for neighbour in current.neighbors:
            if not neighbour.is_barrier():
                temp_neighbour_g_score = g_score[current] + 1  # g(s) + c(s, s')
                if temp_neighbour_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_neighbour_g_score
                    f_score[neighbour] = temp_neighbour_g_score + h(neighbour.get_pos(), end.get_pos())
                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.make_open()
        draw(screen, grid, ROWS, WIDTH)

        if current != start:
            current.make_closed()
    return False


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid.get_fieldlist:
        for spot in row:
            spot.draw(win)

    grid.draw_grid(win, rows, width)
    pygame.display.update()


def main(win, width):
    grid = Grid(ROWS, WIDTH)
    start = grid.fieldlist[0][19]
    end = grid.fieldlist[19][0]
    start.make_start()
    end.make_end()

    done = False
    found = False

    while not done:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if not found:
                for row in grid.fieldlist:
                    for spot in row:
                        spot.set_neighbors(grid)

                found = astar(grid, start, end)

    pygame.quit()


main(screen, 500)
