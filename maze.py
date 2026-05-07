import pygame
import sys

pygame.init()

ROWS = 20
COLS = 25
CELL_SIZE = 30

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True
        }

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)

        if self.walls['right']:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

        if self.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)

        if self.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)


grid = []

for row in range(ROWS):
    row_cells = []

    for col in range(COLS):
        row_cells.append(Cell(row, col))

    grid.append(row_cells)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw()

    pygame.display.update()
    clock.tick(60)