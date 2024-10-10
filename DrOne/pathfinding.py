# pathfinding.py

import heapq
import numpy as np
import math

def a_star_3d(grid, start, end, step=0.1, object_size=(0.5, 0.5, 0.5)):
    frontier = []
    heapq.heappush(frontier, (0, start))
    cost_so_far = {start: 0}
    came_from = {start: None}

    while frontier:
        current_priority, current_node = heapq.heappop(frontier)

        if current_node == end:
            break

        for neighbor in get_neighbors_3d(current_node, grid, step):
            # Convert the floating-point coordinates to grid indices
            ix, iy, iz = int(neighbor[0] / step), int(neighbor[1] / step), int(neighbor[2] / step)

            # Ensure the indices are valid for the grid size
            if ix < 0 or iy < 0 or iz < 0 or ix >= int(grid.size[0]/step) or iy >= int(grid.size[1]/step) or iz >= int(grid.size[2]/step):
                continue

            # Check for collision with barriers using object dimensions
            if grid.is_collision(neighbor, object_size):
                continue

            new_cost = cost_so_far[current_node] + calculate_movement_cost(current_node, neighbor, came_from)

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current_node

    return reconstruct_path(came_from, start, end)

# Get neighboring cells, now moves are step-sized (0.1)
def get_neighbors_3d(node, grid, step):
    x, y, z = node
    neighbors = []
    for dx in [-step, 0, step]:
        for dy in [-step, 0, step]:
            for dz in [-step, 0, step]:
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                neighbor = (round(x + dx, 1), round(y + dy, 1), round(z + dz, 1))
                ix = int(neighbor[0] / step)
                iy = int(neighbor[1] / step)
                iz = int(neighbor[2] / step)
                if 0 <= ix < int(grid.size[0]/step) and 0 <= iy < int(grid.size[1]/step) and 0 <= iz < int(grid.size[2]/step):
                    neighbors.append(neighbor)
    return neighbors

# Movement cost with degree-based calculation
def calculate_movement_cost(current_node, next_node, came_from):
    distance = np.linalg.norm(np.array(current_node) - np.array(next_node))
    if came_from[current_node] is None:
        return distance
    previous_node = came_from[current_node]
    angle_change = calculate_angular_change(previous_node, current_node, next_node)
    angle_penalty_weight = 0.1  # Tweakable weight
    return distance + (angle_penalty_weight * angle_change)

def calculate_angular_change(prev, current, next):
    vec1 = np.array(current) - np.array(prev)
    vec2 = np.array(next) - np.array(current)
    norm_vec1 = vec1 / np.linalg.norm(vec1)
    norm_vec2 = vec2 / np.linalg.norm(vec2)
    dot_product = np.dot(norm_vec1, norm_vec2)
    dot_product = np.clip(dot_product, -1.0, 1.0)
    angle_radians = np.arccos(dot_product)
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees

def heuristic(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def reconstruct_path(came_from, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
