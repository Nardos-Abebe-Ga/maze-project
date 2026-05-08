Maze Generator and Solver

This project generates and solves a random rectangular maze using Python and Pygame.

The maze generation uses a Depth First Search (DFS) algorithm with a stack-based backtracking system. A virtual “mouse” moves through the maze, randomly selecting unvisited neighboring cells and removing walls to create valid paths.

The maze solver also uses a stack-based backtracking approach. A red dot represents the mouse searching for the exit, while blue cells indicate dead ends that were explored and abandoned.

The program visually demonstrates:

Dynamic maze generation

Recursive backtracking

Stack data structure usage

Maze traversal and solving

Randomized path creation

Bonus functionality includes random cycle creation by occasionally removing extra walls.