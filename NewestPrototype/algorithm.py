import pygame
from queue import PriorityQueue
def aStarAlgorithm(draw, grid, start, end, waypoints):
    """
    Implements the A* pathfinding algorithm in a grid.
    Args:
        draw: Function to update the visual display (e.g., Pygame drawing function).
        grid: The grid of nodes (spots) representing the environment.
        start: The starting node in the grid.
        end: The goal node in the grid.
        waypoints: (Optional) List of waypoint nodes to pass through (not used in the core logic).
    """

    # Step counter used to keep track of the order in which nodes are added to the open_set (tie-breaker)
    count = 0

    # Priority queue (min-heap) to store nodes to explore, ordered by f_score (estimated total cost).
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # Start node is added with priority 0

    # Dictionary to track the most efficient path (which node each node came from)
    came_from = {}

    # Dictionary to store the cost from start to each node (g_score), initialized to infinity
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0  # The cost to reach the start node is 0

    # Dictionary to store the estimated total cost (g + heuristic h) from start to goal for each node
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())  # Initialize f_score of start node with heuristic to the goal

    # A set to track nodes that are in the open_set (for quick lookup)
    open_set_hash = {start}

    # Main A* algorithm loop: continues until there are no nodes left to explore
    while not open_set.empty():
        # Handle Pygame events (like quitting the application)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the node in open_set with the lowest f_score (priority queue guarantees this)
        current = open_set.get()[2]  # The node is at index 2 of the tuple (f_score, count, node)
        open_set_hash.remove(current)  # Remove current node from the hash set

        # If the current node is the goal (end), reconstruct and return the path
        if current == end:
            reconstruct_path(came_from, end, draw)  # Call a function to visualize the path
            end.make_end()  # Mark the end node visually
            return True  # Path has been found, so exit the function

        # Explore the neighbors of the current node
        for neighbor in current.neighbors:
            # Calculate the tentative g_score for the neighbor
            # Assumes all edge costs between nodes are equal (hence +1 for moving to a neighbor)
            temp_g_score = g_score[current] + 1

            # If the tentative g_score is better (lower) than the current g_score for the neighbor:
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current  # Record the best path to this neighbor
                g_score[neighbor] = temp_g_score  # Update g_score for the neighbor

                # Update f_score (g + heuristic h) for the neighbor
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                # If the neighbor hasn't been added to the open_set before, add it
                if neighbor not in open_set_hash:
                    count += 1  # Increment the count (used as a tie-breaker for equal f_score)
                    open_set.put((f_score[neighbor], count, neighbor))  # Add neighbor to the open_set
                    open_set_hash.add(neighbor)  # Also add neighbor to the hash set for fast lookup

                    # Optionally update the display to show the neighbor as open (part of the frontier)
                    neighbor.make_open()

        # Call the draw function to update the visual representation (e.g., Pygame window)
        draw()

        # Optionally mark the current node as closed (explored and no longer part of the frontier)
        if current != start:
            pass
            # current.make_closed()  # Toggle to view closed nodes in a different color

    # If we exit the loop, no path was found
    return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        #####print(current) Add a way of printing/retrieving the pos for each grid that makes up the reconstructed path.
        current = came_from[current]
        if not current.is_start():  # Ensure start block isn't modified
            current.make_path()
        draw()

def thetaStarAlgorithm(draw, grid, start, end, waypoints):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            # reconstruct_path(came_from, end, draw)
            reconstruct_path(came_from, current, draw)  # Theta* alg.
            end.make_end()
            return True

        for neighbor in get_neighbors(current, grid):  # Theta* alg.
            if neighbor.is_barrier():
                continue

            tentative_g_score = g_score[current] + h(current.get_pos(), neighbor.get_pos())

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() # toggle to view colors
        draw()

        if current != start:
            pass
            # current.make_closed() # toggle to view colors

    return False

def thetaStarAlgorithm(draw, grid, start, end, waypoints):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            # reconstruct_path(came_from, end, draw)
            reconstruct_path(came_from, current, draw)  # Theta* alg.
            end.make_end()
            return True

        for neighbor in get_neighbors(current, grid):  # Theta* alg.
            if neighbor.is_barrier():
                continue

            tentative_g_score = g_score[current] + h(current.get_pos(), neighbor.get_pos())

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() # toggle to view colors
        draw()

        if current != start:
            pass
            # current.make_closed() # toggle to view colors

    return False

def thetaStarAlgorithmNoDiagonals(draw, grid, start, end, waypoints):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, current, draw)  # Theta* path reconstruction
            end.make_end()
            return True

        for neighbor in get_neighbors(current, grid):  # Theta* neighbor checking
            if neighbor.is_barrier():
                continue

            # Ensure that the movement is only horizontal or vertical
            current_pos = current.get_pos()
            neighbor_pos = neighbor.get_pos()
            if abs(current_pos[0] - neighbor_pos[0]) + abs(current_pos[1] - neighbor_pos[1]) != 1:
                # Skip diagonal neighbors
                continue

            tentative_g_score = g_score[current] + h(current.get_pos(), neighbor.get_pos())

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # Toggle to view colors
        draw()

        if current != start:
            pass
            # current.make_closed()  # Toggle to view colors

    return False


def get_neighbors(current, grid):  # For theta* alg.
    neighbors = []
    row, col = current.get_pos()
    rows, cols = len(grid), len(grid[0])

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_row, new_col = row + i, col + j
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbor = grid[new_row][new_col]
                if not neighbor.is_barrier():
                    neighbors.append(neighbor)

    return neighbors



def dijkstraAlgorithm(draw, grid, start, end, waypoints):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

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
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() # toggle to view colors

        draw()

def aStarJPS(draw, grid, start, end, waypoints):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
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

        # Implement Jump Point Search logic here
        jump_points = get_jump_points(current, grid, start, end)

        for neighbor in jump_points:
            temp_g_score = g_score[current] + distance(current, neighbor)

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
            pass
            # current.make_closed()

    return False

def get_jump_points(current, grid, start, end):
    """
    This function identifies jump points by 'jumping' over nodes in a straight line
    and finding nodes that could alter the path (forced neighbors).
    In a grid with no barriers, this will behave similarly to A* by visiting all nodes.
    """
    jump_points = []

    # Example: Check straight lines and diagonal directions for valid jump points
    # Add neighbors normally if no forced neighbor (e.g., barrier) exists.
    for neighbor in current.neighbors:
        # In the absence of barriers, we don't perform JPS optimization
        # Just return all neighbors, acting like regular A*
        jump_points.append(neighbor)

    return jump_points

def distance(p1, p2):
    """Calculate the distance between two points."""
    x1, y1 = p1.get_pos()
    x2, y2 = p2.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)
