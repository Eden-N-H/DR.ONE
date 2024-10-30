import heapq
import numpy as np

def a_star_3d(grid, step):
    waypoints = grid.waypoints
    start = grid.start
    end = grid.end

    # Start with the current position at the start point
    current_position = start
    full_path = []

    # Visit each waypoint in order
    for waypoint in waypoints:
        path_to_waypoint = find_path(current_position, waypoint, grid, step)
        if path_to_waypoint is None:
            return None  # No path found to waypoint
        full_path.extend(path_to_waypoint[:-1])  # Exclude the current position, add all but the last point
        current_position = waypoint

    # Finally, find the path from the last waypoint to the end
    path_to_end = find_path(current_position, end, grid, step)
    if path_to_end is None:
        return None  # No path found to end
    full_path.extend(path_to_end)

    return full_path

def find_path(start, end, grid, step):
    frontier = []
    heapq.heappush(frontier, (0, start))
    cost_so_far = {start: 0}
    came_from = {start: None}

    while frontier:
        _, current_node = heapq.heappop(frontier)

        if current_node == end:
            break

        for neighbor in get_neighbors_3d(current_node, grid, step):
            if grid.is_collision(neighbor):
                continue

            new_cost = cost_so_far[current_node] + 1  # Assuming uniform movement cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current_node

    return reconstruct_path(came_from, start, end)

# Simplified neighbor function for a 5x5x5 grid
def get_neighbors_3d(node, grid, step):
    x, y, z = node
    neighbors = []
    for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
        neighbor = (x + dx, y + dy, z + dz)
        if all(0 <= n < 5 for n in neighbor):  # Ensure neighbor is within grid bounds
            neighbors.append(neighbor)
    return neighbors

def heuristic(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def reconstruct_path(came_from, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return None  # No path found
    path.append(start)
    path.reverse()
    return path
