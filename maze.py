import pygame
import random
import sys

# ==========================================
# CONFIGURATION
# ==========================================
ROWS = 20
COLS = 25
CELL_SIZE = 30

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Building and Running Mazes")

clock = pygame.time.Clock()

# ==========================================
# MAZE REPRESENTATION
# ==========================================
# northWall[r][c]
# True  -> upper wall exists
# False -> upper wall removed
#
# eastWall[r][c]
# True  -> right wall exists
# False -> right wall removed
#
# Extra phantom boundaries:
# northWall[0][c] represents bottom edge
# eastWall[r][0] represents left edge
# ==========================================

northWall = [[True for _ in range(COLS)] for _ in range(ROWS + 1)]
eastWall = [[True for _ in range(COLS + 1)] for _ in range(ROWS)]

# Track visited cells
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Solver tracking
solverVisited = [[False for _ in range(COLS)] for _ in range(ROWS)]
deadEnds = [[False for _ in range(COLS)] for _ in range(ROWS)]


# ==========================================
# DRAW MAZE
# ==========================================
def draw_maze():

    screen.fill(GRAY)

    for r in range(ROWS):
        for c in range(COLS):

            x = c * CELL_SIZE
            y = r * CELL_SIZE

            # Draw visited cells
            if visited[r][c]:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

            # Draw dead-end cells
            if deadEnds[r][c]:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10)
                )

            # Top wall
            if northWall[r + 1][c]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x, y),
                    (x + CELL_SIZE, y),
                    2
                )

            # Bottom wall
            if northWall[r][c]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x, y + CELL_SIZE),
                    (x + CELL_SIZE, y + CELL_SIZE),
                    2
                )

            # Left wall
            if eastWall[r][c]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x, y),
                    (x, y + CELL_SIZE),
                    2
                )

            # Right wall
            if eastWall[r][c + 1]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x + CELL_SIZE, y),
                    (x + CELL_SIZE, y + CELL_SIZE),
                    2
                )


# ==========================================
# GET UNVISITED NEIGHBORS
# ==========================================
def get_unvisited_neighbors(r, c):

    neighbors = []

    directions = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1)    # right
    ]

    for dr, dc in directions:

        nr = r + dr
        nc = c + dc

        if 0 <= nr < ROWS and 0 <= nc < COLS:

            if not visited[nr][nc]:
                neighbors.append((nr, nc))

    return neighbors


# ==========================================
# REMOVE WALL BETWEEN CELLS
# ==========================================
def remove_wall(r1, c1, r2, c2):

    # Moving up
    if r2 < r1:
        northWall[r1 + 1][c1] = False

    # Moving down
    elif r2 > r1:
        northWall[r2 + 1][c2] = False

    # Moving left
    elif c2 < c1:
        eastWall[r1][c1] = False

    # Moving right
    elif c2 > c1:
        eastWall[r1][c1 + 1] = False


# ==========================================
# BONUS EXTRA WALL REMOVAL
# ==========================================
def add_random_cycle(r, c):

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    random.shuffle(directions)

    for dr, dc in directions:

        nr = r + dr
        nc = c + dc

        if 0 <= nr < ROWS and 0 <= nc < COLS:

            remove_wall(r, c, nr, nc)
            break


# ==========================================
# MAZE GENERATION
# DFS + STACK
# ==========================================
def generate_maze():

    stack = []

    current_r = random.randint(0, ROWS - 1)
    current_c = random.randint(0, COLS - 1)

    visited[current_r][current_c] = True

    total_cells = ROWS * COLS
    visited_count = 1

    while visited_count < total_cells:

        handle_events()

        neighbors = get_unvisited_neighbors(current_r, current_c)

        if neighbors:

            # Save current position
            stack.append((current_r, current_c))

            # Choose random neighbor
            nr, nc = random.choice(neighbors)

            # Eat through wall
            remove_wall(current_r, current_c, nr, nc)

            # Move mouse
            current_r = nr
            current_c = nc

            visited[current_r][current_c] = True

            visited_count += 1

            # Bonus cycles
            if random.randint(1, 20) == 1:
                add_random_cycle(current_r, current_c)

        elif stack:

            # Backtrack
            current_r, current_c = stack.pop()

        draw_maze()

        # Draw mouse
        mx = current_c * CELL_SIZE + CELL_SIZE // 2
        my = current_r * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(
            screen,
            GREEN,
            (mx, my),
            CELL_SIZE // 4
        )

        pygame.display.update()

        clock.tick(FPS)


# ==========================================
# GET AVAILABLE MOVES
# ==========================================
def get_available_moves(r, c):

    moves = []

    # UP
    if r > 0:
        if not northWall[r + 1][c]:
            moves.append((r - 1, c))

    # DOWN
    if r < ROWS - 1:
        if not northWall[r + 2][c]:
            moves.append((r + 1, c))

    # LEFT
    if c > 0:
        if not eastWall[r][c]:
            moves.append((r, c - 1))

    # RIGHT
    if c < COLS - 1:
        if not eastWall[r][c + 1]:
            moves.append((r, c + 1))

    return moves

# ==========================================
# SOLVE MAZE
# ==========================================
def solve_maze(start_r, start_c, end_r, end_c):

    stack = []

    current_r = start_r
    current_c = start_c

    solverVisited[current_r][current_c] = True

    running = True

    while running:

        handle_events()

        draw_maze()

        # Draw current mouse position
        mx = current_c * CELL_SIZE + CELL_SIZE // 2
        my = current_r * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(
            screen,
            RED,
            (mx, my),
            CELL_SIZE // 4
        )

        pygame.display.update()

        clock.tick(25)

        # Reached exit
        if (current_r, current_c) == (end_r, end_c):
            print("Maze solved!")
            return

        possible_moves = []

        for nr, nc in get_available_moves(current_r, current_c):

            if not solverVisited[nr][nc]:
                possible_moves.append((nr, nc))

        if possible_moves:

            stack.append((current_r, current_c))

            nr, nc = random.choice(possible_moves)

            current_r = nr
            current_c = nc

            solverVisited[current_r][current_c] = True

        elif stack:

            deadEnds[current_r][current_c] = True

            current_r, current_c = stack.pop()

        else:
            print("No solution found")
            return


# ==========================================
# HANDLE EVENTS
# ==========================================
def handle_events():

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# ==========================================
# MAIN
# ==========================================
def main():

    generate_maze()

    # Random edge start/end
    start_r = random.randint(0, ROWS - 1)
    start_c = 0

    end_r = random.randint(0, ROWS - 1)
    end_c = COLS - 1

    # Open left entrance
    eastWall[start_r][0] = False

    # Open right exit
    eastWall[end_r][COLS] = False

    pygame.time.delay(1000)

    solve_maze(start_r, start_c, end_r, end_c)

    while True:

        handle_events()

        draw_maze()

        # Draw start
        sx = start_c * CELL_SIZE + CELL_SIZE // 2
        sy = start_r * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(
            screen,
            GREEN,
            (sx, sy),
            CELL_SIZE // 4
        )

        # Draw end
        ex = end_c * CELL_SIZE + CELL_SIZE // 2
        ey = end_r * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(
            screen,
            RED,
            (ex, ey),
            CELL_SIZE // 4
        )

        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":
    main()