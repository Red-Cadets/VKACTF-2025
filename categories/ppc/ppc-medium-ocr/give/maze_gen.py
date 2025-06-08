import random
import time
from PIL import Image, ImageDraw
from collections import deque
import io

class MazeCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = [True, True, True, True]

    def remove_walls(self, next_row, next_col):
        if next_row < self.row:
            self.walls[0] = False
        elif next_row > self.row:
            self.walls[2] = False
        if next_col < self.col:
            self.walls[3] = False
        elif next_col > self.col:
            self.walls[1] = False

class Maze:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid = [[MazeCell(i, j) for j in range(num_cols)] for i in range(num_rows)]
        self.entry_coor = (0, 0)
        self.exit_coor = (num_rows - 1, num_cols - 1)

    def find_neighbours(self, row, col):
        neighbours = []
        if row > 0 and not self.grid[row-1][col].visited:
            neighbours.append((row-1, col))
        if col < self.num_cols - 1 and not self.grid[row][col+1].visited:
            neighbours.append((row, col+1))
        if row < self.num_rows - 1 and not self.grid[row+1][col].visited:
            neighbours.append((row+1, col))
        if col > 0 and not self.grid[row][col-1].visited:
            neighbours.append((row, col-1))
        return neighbours

    def _validate_neighbours_generate(self, neighbours):
        if neighbours:
            return neighbours
        return None

def depth_first_recursive_backtracker(maze):

    corners = [(0, 0), (0, maze.num_cols - 1), (maze.num_rows - 1, 0), (maze.num_rows - 1, maze.num_cols - 1)]
    start_coor = random.choice(corners)
    k_curr, l_curr = start_coor
    maze.entry_coor = start_coor
    path = [(k_curr, l_curr)]
    maze.grid[k_curr][l_curr].visited = True
    visit_counter = 1
    visited_cells = list()


    start_time = time.time()

    while visit_counter < maze.num_rows * maze.num_cols:
        neighbour_indices = maze.find_neighbours(k_curr, l_curr)
        neighbour_indices = maze._validate_neighbours_generate(neighbour_indices)

        if neighbour_indices:
            visited_cells.append((k_curr, l_curr))
            k_next, l_next = random.choice(neighbour_indices)
            maze.grid[k_curr][l_curr].remove_walls(k_next, l_next)
            maze.grid[k_next][l_next].remove_walls(k_curr, l_curr)
            maze.grid[k_next][l_next].visited = True
            k_curr, l_curr = k_next, l_next
            path.append((k_curr, l_curr))
            visit_counter += 1
        elif visited_cells:
            k_curr, l_curr = visited_cells.pop()
            path.append((k_curr, l_curr))

    if maze.entry_coor == (0, 0):
        maze.exit_coor = (maze.num_rows - 1, maze.num_cols - 1)
    elif maze.entry_coor == (0, maze.num_cols - 1):
        maze.exit_coor = (maze.num_rows - 1, 0)
    elif maze.entry_coor == (maze.num_rows - 1, 0):
        maze.exit_coor = (0, maze.num_cols - 1)
    elif maze.entry_coor == (maze.num_rows - 1, maze.num_cols - 1):
        maze.exit_coor = (0, 0)

    maze.generation_path = path
    return path

def bfs_shortest_path(maze):
    start = maze.entry_coor
    end = maze.exit_coor
    queue = deque([(start, [])])
    visited = set()

    directions = {
        (-1, 0): 'w',
        (1, 0): 's',
        (0, -1): 'a',
        (0, 1): 'd'
    }

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            return path

        if (x, y) not in visited:
            visited.add((x, y))


            for dx, dy in directions.keys():
                nx, ny = x + dx, y + dy


                if 0 <= nx < maze.num_rows and 0 <= ny < maze.num_cols:
                    cell = maze.grid[x][y]
                    if directions[(dx, dy)] == 'w' and not cell.walls[0]:
                        queue.append(((nx, ny), path + ['w']))
                    elif directions[(dx, dy)] == 's' and not cell.walls[2]:
                        queue.append(((nx, ny), path + ['s']))
                    elif directions[(dx, dy)] == 'a' and not cell.walls[3]:
                        queue.append(((nx, ny), path + ['a']))
                    elif directions[(dx, dy)] == 'd' and not cell.walls[1]:
                        queue.append(((nx, ny), path + ['d']))
    return []

def gen_maze_image(maze, entry_img, exit_img):
    CELL = 50
    NEON = (255, 0, 0)
    cell_size = 50
    w = maze.num_cols * CELL + 2
    h = maze.num_rows * CELL + 2
    img  = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    horiz, vert = [], []
    for i in range(maze.num_rows):
        y = i * CELL
        for j in range(maze.num_cols):
            x = j * CELL
            walls = maze.grid[i][j].walls
            if walls[0]: horiz.append((x, y, x+CELL, y))
            if walls[2]: horiz.append((x, y+CELL, x+CELL, y+CELL))
            if walls[1]: vert .append((x+CELL, y, x+CELL, y+CELL))
            if walls[3]: vert .append((x, y, x, y+CELL))

    try:
        draw.lines(horiz, fill=NEON, width=2, joint=None)
        draw.lines(vert , fill=NEON, width=2, joint=None)
    except AttributeError:              
        for seg in horiz:
            draw.line(seg, fill=NEON, width=2)
        for seg in vert:
            draw.line(seg, fill=NEON, width=2)

    draw.line((w-1, 0, w-1, h), fill=NEON, width=2)
    draw.line((0, h-1, w,   h-1), fill=NEON, width=2)


    entry_image = Image.open(entry_img).resize((cell_size - 2, cell_size - 2))
    exit_image = Image.open(exit_img).resize((cell_size - 2, cell_size - 2))

    entry_row, entry_col = maze.entry_coor
    exit_row,  exit_col  = maze.exit_coor

    img.paste(entry_image, (entry_col * cell_size + 2, entry_row * cell_size + 2))
    img.paste(exit_image, (exit_col * cell_size + 2, exit_row * cell_size + 2))

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return img_io
