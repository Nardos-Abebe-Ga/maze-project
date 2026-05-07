# Full Python Code – Maze Generator and Solver


import pygame
import random
import sys

# =========================
# CONFIGURATION
# =========================
ROWS = 20
COLS = 25
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator and Solver")
clock = pygame.time.Clock()


# =========================
# CELL CLASS
# =========================
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        # All walls initially exist
        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True
        }

        self.visited = False
        self.solution_visited = False
        self.dead_end = False

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        # Background
        if self.visited:
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

        # Dead-end cells during solving
        if self.dead_end:
            pygame.draw.rect(screen, BLUE, (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10))

        # Draw walls
        if self.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)

        if self.walls['right']:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

        if self.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)

        if self.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)


# =========================
# CREATE GRID
# =========================
grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]


# =========================
# HELPER FUNCTIONS
# =========================
def get_neighbors(cell):
    neighbors = []

    directions = [
        (-1, 0, 'top', 'bottom'),
        (1, 0, 'bottom', 'top'),
        (0, -1, 'left', 'right'),
        (0, 1, 'right', 'left')
    ]

    for dr, dc, wall, opposite_wall in directions:
        nr = cell.row + dr
        nc = cell.col + dc

        if 0 <= nr < ROWS and 0 <= nc < COLS:
            neighbor = grid[nr][nc]

            if not neighbor.visited:
                neighbors.append((neighbor, wall, opposite_wall))

    return neighbors


def remove_walls(current, next_cell, wall, opposite_wall):
    current.walls[wall] = False
    next_cell.walls[opposite_wall] = False


# =========================
# MAZE GENERATION
# DFS + STACK
# =========================
def generate_maze():
    stack = []

    current = grid[0][0]
    current.visited = True

    total_cells = ROWS * COLS
    visited_count = 1

    while visited_count < total_cells:
        handle_events()

        neighbors = get_neighbors(current)

        if neighbors:
            next_cell, wall, opposite_wall = random.choice(neighbors)

            stack.append(current)

            remove_walls(current, next_cell, wall, opposite_wall)

            current = next_cell
            current.visited = True
            visited_count += 1

            # Bonus: randomly remove extra wall to create cycles
            if random.randint(1, 20) == 1:
                add_random_cycle(current)

        elif stack:
            current = stack.pop()

        draw_maze()

        # Draw current generation position
        x = current.col * CELL_SIZE + CELL_SIZE // 2
        y = current.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, GREEN, (x, y), CELL_SIZE // 4)

        pygame.display.update()
        clock.tick(FPS)


# =========================
# BONUS CYCLES
# =========================
def add_random_cycle(cell):
    directions = [
        (-1, 0, 'top', 'bottom'),
        (1, 0, 'bottom', 'top'),
        (0, -1, 'left', 'right'),
        (0, 1, 'right', 'left')
    ]

    random.shuffle(directions)

    for dr, dc, wall, opposite_wall in directions:
        nr = cell.row + dr
        nc = cell.col + dc

        if 0 <= nr < ROWS and 0 <= nc < COLS:
            neighbor = grid[nr][nc]

            # Remove wall only if wall exists
            if cell.walls[wall]:
                cell.walls[wall] = False
                neighbor.walls[opposite_wall] = False
                break


# =========================
# DRAW MAZE
# =========================
def draw_maze():
    screen.fill(GRAY)

    for row in grid:
        for cell in row:
            cell.draw()


# =========================
# GET AVAILABLE MOVES
# =========================
def get_available_moves(cell):
    moves = []

    r = cell.row
    c = cell.col

    if not cell.walls['top'] and r > 0:
        moves.append(grid[r - 1][c])

    if not cell.walls['bottom'] and r < ROWS - 1:
        moves.append(grid[r + 1][c])

    if not cell.walls['left'] and c > 0:
        moves.append(grid[r][c - 1])

    if not cell.walls['right'] and c < COLS - 1:
        moves.append(grid[r][c + 1])

    return moves


# =========================
# SOLVE MAZE
# BACKTRACKING + STACK
# =========================
def solve_maze(start, end):
    stack = []

    current = start
    current.solution_visited = True

    while current != end:
        handle_events()

        draw_maze()

        # Draw current mouse position
        x = current.col * CELL_SIZE + CELL_SIZE // 2
        y = current.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, RED, (x, y), CELL_SIZE // 4)

        pygame.display.update()
        clock.tick(25)

        possible_moves = [
            cell for cell in get_available_moves(current)
            if not cell.solution_visited
        ]

        if possible_moves:
            stack.append(current)

            next_cell = random.choice(possible_moves)
            next_cell.solution_visited = True

            current = next_cell

        elif stack:
            current.dead_end = True
            current = stack.pop()

        else:
            print("No solution found")
            return

    # Draw final solution position
    draw_maze()

    x = end.col * CELL_SIZE + CELL_SIZE // 2
    y = end.row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, RED, (x, y), CELL_SIZE // 3)

    pygame.display.update()

    print("Maze solved!")


# =========================
# EVENT HANDLING
# =========================
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# =========================
# MAIN PROGRAM
# =========================
def main():
    generate_maze()

    # Random start and end positions
    start = grid[random.randint(0, ROWS - 1)][0]
    end = grid[random.randint(0, ROWS - 1)][COLS - 1]

    # Open maze entrances
    start.walls['left'] = False
    end.walls['right'] = False

    pygame.time.delay(1000)

    solve_maze(start, end)

    # Keep window open
    while True:
        handle_events()
        draw_maze()

        # Draw start
        sx = start.col * CELL_SIZE + CELL_SIZE // 2
        sy = start.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, GREEN, (sx, sy), CELL_SIZE // 4)

        # Draw end
        ex = end.col * CELL_SIZE + CELL_SIZE // 2
        ey = end.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, RED, (ex, ey), CELL_SIZE // 4)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
