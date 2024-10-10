import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def visualize_path(grid, path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot barriers
    barrier_indices = np.argwhere(grid == 1)
    ax.scatter(barrier_indices[:, 0], barrier_indices[:, 1], barrier_indices[:, 2], c='red')
    
    # Plot path
    path = np.array(path)
    ax.plot(path[:, 0], path[:, 1], path[:, 2], color='blue')
    
    plt.show()
