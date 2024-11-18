# grid_system.py

import numpy as np

class Grid:
    def __init__(self, size, step=0.1):
        self.size = size  # Store the size as a tuple (x_size, y_size, z_size)
        self.step = step
        self.grid = np.zeros((int(size[0]/step), int(size[1]/step), int(size[2]/step)))
        self.barriers = []  # Store barriers as floating-point coordinates
    
    def add_barrier(self, x, y, z):
        self.barriers.append((x, y, z))
    
    def is_collision(self, position, object_size=(0.5, 0.5, 0.5)):
        object_radius_x = object_size[0] / 2.0
        object_radius_y = object_size[1] / 2.0
        object_radius_z = object_size[2] / 2.0
        for barrier in self.barriers:
            if self.is_within_boundary(position, barrier, object_radius_x, object_radius_y, object_radius_z):
                return True
        return False
    
    def is_within_boundary(self, position, barrier, radius_x, radius_y, radius_z):
        px, py, pz = position
        bx, by, bz = barrier
        if (abs(px - bx) <= radius_x + 0.5 and
            abs(py - by) <= radius_y + 0.5 and
            abs(pz - bz) <= radius_z + 0.5):
            return True
        return False
