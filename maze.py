import pygame
import sys
import random

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
GREEN = (0, 255, 0)


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

        self.visited = False

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.visited:
            pygame.draw.rect(screen, (220, 220, 220), (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)

        if self.walls['right']:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

        if self.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)

        if self.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)


grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]


def get_neighbors(cell):
    neighbors = []

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in directions:
        nr = cell.row + dr
        nc = cell.col + dc

        if 0 <= nr < ROWS and 0 <= nc < COLS:
            neighbor = grid[nr][nc]

            if not neighbor.visited:
                neighbors.append(neighbor)

    return neighbors


current = grid[0][0]
current.visited = True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw()

    neighbors = get_neighbors(current)

    if neighbors:
        current = random.choice(neighbors)
        current.visited = True

    x = current.col * CELL_SIZE + CELL_SIZE // 2
    y = current.row * CELL_SIZE + CELL_SIZE // 2

    pygame.draw.circle(screen, GREEN, (x, y), CELL_SIZE // 4)

    pygame.display.update()
    clock.tick(10)