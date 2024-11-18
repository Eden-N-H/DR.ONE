import pygame
import numpy as np
from math import *

'''
Use 'x', 'y', 'z' to rotate

'''

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)  # Green color for highlighted cubes

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D Cube Projection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 30  # Adjusted scale for zoom out
circle_pos = [WIDTH / 2, HEIGHT / 2]  # x, y

# Initialize rotation angles
angle_x = 0
angle_y = 0
angle_z = 0

# Initialize Pygame
pygame.init()


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

    # Draw faces first
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
        # Draw edges on top of faces
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

# Variables to track key states
keys_pressed = {'x': False, 'y': False, 'z': False}

# Define the color of the specified small cubes
highlighted_cubes = [
    (1, 1, 1),  # Example positions of the small cubes to highlight
    (2, 2, 2),
    (3, 3, 3)
]

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_x:
                keys_pressed['x'] = True
            elif event.key == pygame.K_y:
                keys_pressed['y'] = True
            elif event.key == pygame.K_z:
                keys_pressed['z'] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                keys_pressed['x'] = False
            elif event.key == pygame.K_y:
                keys_pressed['y'] = False
            elif event.key == pygame.K_z:
                keys_pressed['z'] = False

    # Update rotation angles based on key states
    rotation_speed = 0.02
    if keys_pressed['x']:
        angle_x += rotation_speed  # Adjust rotation speed
    if keys_pressed['y']:
        angle_y += rotation_speed  # Adjust rotation speed
    if keys_pressed['z']:
        angle_z += rotation_speed  # Adjust rotation speed

    # Update rotation matrices based on key presses
    rotation_z = np.matrix([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)],
    ])

    screen.fill(WHITE)

    cube_size = 2
    spacing = 0  # No spacing to ensure cubes are joined
    grid_size = 5  # Number of smaller cubes along each axis

    # Draw the large cube made of smaller cubes
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):
                offset_x = (x - grid_size // 2) * cube_size
                offset_y = (y - grid_size // 2) * cube_size
                offset_z = (z - grid_size // 2) * cube_size
                vertices = create_cube_vertices(cube_size)
                vertices = [v + np.array([offset_x, offset_y, offset_z]) for v in vertices]

                # Set color for faces and edges
                face_color = HIGHLIGHT_COLOR if (x, y, z) in highlighted_cubes else None
                edge_color = BLACK if (x, y, z) in highlighted_cubes else None

                draw_cube_faces(vertices, face_color)

    # Draw all edges on top of faces
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):
                offset_x = (x - grid_size // 2) * cube_size
                offset_y = (y - grid_size // 2) * cube_size
                offset_z = (z - grid_size // 2) * cube_size
                vertices = create_cube_vertices(cube_size)
                vertices = [v + np.array([offset_x, offset_y, offset_z]) for v in vertices]
                edge_color = BLACK if (x, y, z) in highlighted_cubes else None
                draw_cube_edges(vertices, edge_color)

    pygame.display.update()
