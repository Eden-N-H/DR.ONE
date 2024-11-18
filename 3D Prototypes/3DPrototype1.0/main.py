from grid import Grid
from pathfinding import a_star_3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def draw_3d_path(path, barriers, start, waypoint, end):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the barriers as red points
    if barriers:
        barrier_coords = list(zip(*barriers))
        ax.scatter(barrier_coords[0], barrier_coords[1], barrier_coords[2], c='r', marker='o', label="Barriers")

    # Plot the path as a blue line
    if path:
        path_coords = list(zip(*path))
        ax.plot(path_coords[0], path_coords[1], path_coords[2], c='b', label="Path")

    # Plot the start, waypoint, and end points
    ax.scatter(start[0], start[1], start[2], c='g', marker='x', s=100, label="Start")
    ax.scatter(waypoint[0], waypoint[1], waypoint[2], c='y', marker='x', s=100, label="Waypoint")
    ax.scatter(end[0], end[1], end[2], c='m', marker='x', s=100, label="End")

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Path Visualization')

    # Show the legend
    ax.legend()

    # Save the plot to a file
    plt.savefig("3d_path_plot.png")  # Saves the figure as a PNG file

    # Display the plot
    plt.show()


def main():
    # Define grid size in floating-point steps
    grid_size = (10.0, 10.0, 10.0)
    grid = Grid(grid_size, step=0.1)

    # Add barriers at floating-point coordinates
    grid.add_barrier(3.0, 3.0, 3.0)
    grid.add_barrier(4.0, 4.0, 4.0)
    
    # Set start, waypoint, and end points with floating-point precision
    start = (0.0, 0.0, 0.0)
    waypoint = (6.1, 6.3, 5.3)  # The waypoint to include in the path
    end = (9.9, 9.9, 9.9)

    # Object size is 0.5 x 0.5 x 0.5
    object_size = (0.5, 0.5, 0.5)

    # First path: from start to waypoint
    path_to_waypoint = a_star_3d(grid, start, waypoint, step=0.1, object_size=object_size)
    
    # Second path: from waypoint to end
    path_from_waypoint = a_star_3d(grid, waypoint, end, step=0.1, object_size=object_size)

    # Combine the two paths, removing duplicate waypoint
    if path_to_waypoint and path_from_waypoint:
        final_path = path_to_waypoint[:-1] + path_from_waypoint  # Avoid duplicating the waypoint
    else:
        final_path = None

    # Output the final path and graph it
    if final_path:
        print(f"Final path found: {final_path}")
        print(f"Path length: {len(final_path)}")
        # Write the path and length to a text file
        with open("path_output_with_waypoint.txt", "w") as file:
            file.write(f"Final path found: {final_path}\n")
            file.write(f"Path length: {len(final_path)}\n")

        # Draw the 3D path
        draw_3d_path(final_path, grid.barriers, start, waypoint, end)
    else:
        print("No path found")
        # Write failure message to file
        with open("path_output_with_waypoint.txt", "w") as file:
            file.write("No path found\n")

if __name__ == "__main__":
    main()
