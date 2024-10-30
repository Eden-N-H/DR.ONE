import numpy as np

class Grid:
    def __init__(self, size, step=1):
        self.size = size  # Store the size as a tuple (x_size, y_size, z_size)
        self.step = step
        self.grid = np.zeros((size[0], size[1], size[2]))  # Initialize a 5x5x5 grid
        self.barriers = []  # Store barriers as coordinate tuples

        # Initialize start, waypoints, and end as None
        self.start = None
        self.waypoints = []
        self.end = None

    def add_barrier(self, x, y, z):
        self.barriers.append((x, y, z))

    def add_waypoint(self, x, y, z):
        self.waypoints.append((x, y, z))

    def is_collision(self, position):
        # Check if the given position is in the list of barriers
        return position in self.barriers
