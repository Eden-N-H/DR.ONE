import pygame
import numpy as np
from math import *
from queue import PriorityQueue
import random

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)  # Green color for highlighted cubes
PURPLE = (128, 0, 128)
TURQUOISE = (64, 224, 208)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)  # Added color for the start cube

# Pygame setup
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D Cube Projection with Pathfinding")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 30  # Adjusted scale for zoom out
circle_pos = [WIDTH / 2, HEIGHT / 2]  # x, y

# Initialize Pygame
pygame.init()

# 3D rotation matrices
angle_x = 0
angle_y = 0
angle_z = 0

def create_cube_vertices(size):
    half_size = size / 2
    return [
        np.array([-half_size, -half_size, half_size]),
        np.array([half_size, -half_size, half_size]),
        np.array([half_size, half_size, half_size]),
        np.array([-half_size, half_size, half_size]),
        np.array([-half_size, -half_size, -half_size]),
        np.array([half_size, -half_size, -half_size]),
        np.array([half_size, half_size, -half_size]),
        np.array([-half_size, half_size, -half_size])
    ]

def draw_cube_faces(vertices, color):
    faces = [
        [0, 1, 2, 3],  # Front face
        [4, 5, 6, 7],  # Back face
        [0, 1, 5, 4],  # Bottom face
        [2, 3, 7, 6],  # Top face
        [0, 3, 7, 4],  # Left face
        [1, 2, 6, 5]  # Right face
    ]

    for face in faces:
        projected_face = []
        for index in face:
            rotated2d = np.dot(rotation_z, vertices[index].reshape((3, 1)))
            rotated2d = np.dot(rotation_y, rotated2d)
            rotated2d = np.dot(rotation_x, rotated2d)
            projected2d = np.dot(projection_matrix, rotated2d)
            x = int(projected2d[0, 0].item() * scale) + circle_pos[0]
            y = int(projected2d[1, 0].item() * scale) + circle_pos[1]
            projected_face.append([x, y])

        if color:
            pygame.draw.polygon(screen, color, projected_face)

def draw_cube_edges(vertices, color):
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
        (0, 4), (1, 5), (2, 6), (3, 7)  # Connecting edges
    ]

    if color:  # Only draw edges if color is provided
        for edge in edges:
            start, end = edge
            rotated2d_start = np.dot(rotation_z, vertices[start].reshape((3, 1)))
            rotated2d_start = np.dot(rotation_y, rotated2d_start)
            rotated2d_start = np.dot(rotation_x, rotated2d_start)
            projected2d_start = np.dot(projection_matrix, rotated2d_start)
            x_start = int(projected2d_start[0, 0].item() * scale) + circle_pos[0]
            y_start = int(projected2d_start[1, 0].item() * scale) + circle_pos[1]

            rotated2d_end = np.dot(rotation_z, vertices[end].reshape((3, 1)))
            rotated2d_end = np.dot(rotation_y, rotated2d_end)
            rotated2d_end = np.dot(rotation_x, rotated2d_end)
            projected2d_end = np.dot(projection_matrix, rotated2d_end)
            x_end = int(projected2d_end[0, 0].item() * scale) + circle_pos[0]
            y_end = int(projected2d_end[1, 0].item() * scale) + circle_pos[1]

            pygame.draw.line(screen, color, (x_start, y_start), (x_end, y_end), 1)  # Draw edges with specified color

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

clock = pygame.time.Clock()

# 3D pathfinding grid setup
class Spot:
    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.x, self.y, self.z

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self):
        vertices = create_cube_vertices(self.size)
        offset_x = (self.x - grid_size // 2) * self.size
        offset_y = (self.y - grid_size // 2) * self.size
        offset_z = (self.z - grid_size // 2) * self.size
        vertices = [v + np.array([offset_x, offset_y, offset_z]) for v in vertices]
        draw_cube_faces(vertices, self.color)
        if self.color == BLACK or self.color == HIGHLIGHT_COLOR:
            draw_cube_edges(vertices, BLACK)

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        for d in directions:
            x, y, z = self.x + d[0], self.y + d[1], self.z + d[2]
            if 0 <= x < grid_size and 0 <= y < grid_size and 0 <= z < grid_size:
                neighbor = grid[x][y][z]
                if not neighbor.is_barrier():
                    self.neighbors.append(neighbor)

def h(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for col in row for spot in col}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for col in row for spot in col}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(size):
    grid = [[[Spot(x, y, z, cube_size) for z in range(size)] for y in range(size)] for x in range(size)]
    return grid

def randomize_grid(grid):
    empty_spots = [grid[x][y][z] for x in range(grid_size) for y in range(grid_size) for z in range(grid_size)]
    start = random.choice(empty_spots)
    start.make_start()
    empty_spots.remove(start)

    end = random.choice(empty_spots)
    end.make_end()
    empty_spots.remove(end)

    barriers = random.sample(empty_spots, 5)
    for barrier in barriers:
        barrier.make_barrier()

    return start, end

def main():
    global rotation_x, rotation_y, rotation_z, projection_matrix, circle_pos, scale, grid_size, cube_size
    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)],
    ])

    rotation_y = np.matrix([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)],
    ])

    rotation_z = np.matrix([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1],
    ])

    projection_matrix = np.matrix([
        [1, 0, 0],
        [0, 1, 0]
    ])

    grid_size = 10
    cube_size = 2
    grid = make_grid(grid_size)

    start, end = randomize_grid(grid)

    run = True
    while run:
        clock.tick(60)
        screen.fill(WHITE)

        # Draw the 3D grid
        for x in range(grid_size):
            for y in range(grid_size):
                for z in range(grid_size):
                    spot = grid[x][y][z]
                    spot.draw()

        pygame.display.flip()  # Use flip() to update the entire display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Draw once before pathfinding starts
                    pygame.display.flip()
                    draw_text(screen, "Solving...", (10, 10))
                    pygame.display.flip()  # Ensure the "Solving..." message is shown

                    for x in range(grid_size):
                        for y in range(grid_size):
                            for z in range(grid_size):
                                spot = grid[x][y][z]
                                spot.update_neighbors(grid)

                    algorithm(lambda: draw(screen, grid, grid_size, WIDTH), grid, start, end)

                if event.key == pygame.K_c:
                    grid = make_grid(grid_size)
                    start, end = randomize_grid(grid)

    pygame.quit()


def draw_text(surface, text, position, color=BLACK):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

main()
