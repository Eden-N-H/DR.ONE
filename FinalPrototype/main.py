import tkinter as tk
from grid import Grid
from pathfinding import a_star_3d
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time  # Import the time module for measuring processing time

class Main():
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = Grid(grid_size, step=1)
        self.processing_time_label = None  # Placeholder for the processing time label

    def draw_initial_grid(self, canvas):
        grid = self.grid
        fig = canvas.figure
        fig.clf()  # Clear any previous plot data
        ax = fig.add_subplot(111, projection='3d')

        # Plot all valid grid points as light grey dots for visualization
        x_vals, y_vals, z_vals = zip(*[(x, y, z) for x in range(5) for y in range(5) for z in range(5)])
        ax.scatter(x_vals, y_vals, z_vals, c='lightgrey', marker='o', s=10, label="Grid Points")

        # Plot barriers as red points
        if grid.barriers:
            bx, by, bz = zip(*grid.barriers)
            ax.scatter(bx, by, bz, c='red', marker='o', s=50, label="Barriers")

        # Plot start, waypoint, and end points
        if grid.start:
            ax.scatter(*grid.start, c='green', marker='x', s=100, label="Start")
        if grid.waypoints:
            for point in grid.waypoints:
                ax.scatter(*point, c='yellow', marker='x', s=100, label="Waypoint")
        if grid.end:
            ax.scatter(*grid.end, c='magenta', marker='x', s=100, label="End")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("3D Pathfinding")
        ax.legend()

        # Set ticks to show only whole numbers (0, 1, 2, 3, 4)
        ax.set_xticks(range(5))
        ax.set_yticks(range(5))
        ax.set_zticks(range(5))

        canvas.draw_idle()

    def update_path_on_grid(self, canvas, path):
        self.draw_initial_grid(canvas)
        fig = canvas.figure
        ax = fig.axes[0]  # Get the current axis
        if path:
            path_coords = list(zip(*path))
            ax.plot(path_coords[0], path_coords[1], path_coords[2], c='b', label="Path")
        canvas.draw_idle()

    def write_path_to_file(self, path):
        # Create or overwrite a file called 'path_vectors.txt'
        with open("path_vectors.txt", "w") as f:
            for i in range(len(path) - 1):
                # Calculate the vector from current point to the next
                vector = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1], path[i + 1][2] - path[i][2])
                f.write(f"{vector}\n")  # Write the vector to the file

    def generate_path_and_display(self, canvas):
        if not self.grid.start or not self.grid.end:
            print("Please ensure start and end points are defined.")
            return

        start_time = time.time()  # Start the timer
        final_path = a_star_3d(self.grid, step=1)
        end_time = time.time()  # End the timer

        processing_time = end_time - start_time  # Calculate processing time

        if final_path:
            self.update_path_on_grid(canvas, final_path)
            # Display processing time
            self.show_processing_time(processing_time)

            # Write the path to file
            self.write_path_to_file(final_path)
        else:
            print("No path found.")

    def show_processing_time(self, processing_time):
        if self.processing_time_label is None:
            self.processing_time_label = tk.Label(text=f"Processing Time: {processing_time:.4f} seconds")
            self.processing_time_label.pack(side=tk.TOP, pady=5)
        else:
            self.processing_time_label.config(text=f"Processing Time: {processing_time:.4f} seconds")

    def add_point(self, point_type, canvas):
        try:
            x, y, z = int(self.x_entry.get()), int(self.y_entry.get()), int(self.z_entry.get())
            if 0 <= x < 5 and 0 <= y < 5 and 0 <= z < 5:
                # Check for existing points
                if (x, y, z) == self.grid.start:
                    print("A Start point already exists at this location.")
                    return
                if (x, y, z) == self.grid.end:
                    print("An End point already exists at this location.")
                    return
                if (x, y, z) in self.grid.barriers:
                    print("A Barrier already exists at this location.")
                    return
                if (x, y, z) in self.grid.waypoints:
                    print("A Waypoint already exists at this location.")
                    return

                # Add point logic
                if point_type in ["Start", "End"]:
                    self.grid.path = []  # Reset path on start/end change
                if point_type == "Barrier":
                    self.grid.add_barrier(x, y, z)
                elif point_type == "Start":
                    if self.grid.end == (x, y, z):
                        print("Start point cannot overlap with end point.")
                        return
                    self.grid.start = (x, y, z)
                elif point_type == "End":
                    if self.grid.start == (x, y, z):
                        print("End point cannot overlap with start point.")
                        return
                    self.grid.end = (x, y, z)
                elif point_type == "Waypoint":
                    self.grid.waypoints.append((x, y, z))

                print(f"{point_type} point added at ({x}, {y}, {z})")
                self.draw_initial_grid(canvas)
            else:
                print(f"{x, y, z} Out of range.")
        except ValueError:
            print("Invalid input for coordinates. Please enter whole numeric values less than 5.")

    def clear_grid(self, canvas):
        self.grid.barriers.clear()
        self.grid.start = None
        self.grid.end = None
        self.grid.waypoints.clear()
        print("All points cleared.")
        self.draw_initial_grid(canvas)

    def addExample(self, canvas):
        # Using add_point method to add barriers, start, and end points
        barriers = [(1, 1, 1), (0, 2, 1), (2, 0, 1), (3, 1, 0), (1, 3, 3), (4, 4, 0), (1, 0, 4), (3, 3, 1)]
        for barrier in barriers:
            self.grid.add_barrier(*barrier)

        self.grid.add_waypoint(4, 1, 4)

        # Set the start and end points
        self.grid.start = (3, 3, 3)
        self.grid.end = (0, 0, 0)

        # Draw the updated grid
        self.draw_initial_grid(canvas)

    def main(self):
        root = tk.Tk()
        root.title("3D Pathfinding")

        fig = plt.Figure()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, pady=10)

        # Create a LabelFrame for adding points
        add_point_frame = tk.LabelFrame(control_frame, text="Add a Point", padx=10, pady=10)
        add_point_frame.pack(side=tk.RIGHT, padx=20)

        point_type_label = tk.Label(add_point_frame, text="Select Point Type:")
        point_type_label.grid(row=0, column=0, padx=5, pady=5)
        point_type_var = tk.StringVar(value="Barrier")
        point_type_menu = tk.OptionMenu(add_point_frame, point_type_var, "Start", "End", "Waypoint", "Barrier")
        point_type_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_point_frame, text="X:").grid(row=1, column=0, padx=5, pady=5)
        self.x_entry = tk.Entry(add_point_frame, width=5)
        self.x_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_point_frame, text="Y:").grid(row=2, column=0, padx=5, pady=5)
        self.y_entry = tk.Entry(add_point_frame, width=5)
        self.y_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_point_frame, text="Z:").grid(row=3, column=0, padx=5, pady=5)
        self.z_entry = tk.Entry(add_point_frame, width=5)
        self.z_entry.grid(row=3, column=1, padx=5, pady=5)

        add_button = tk.Button(add_point_frame, text="Add Point", command=lambda: self.add_point(point_type_var.get(), canvas))
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(control_frame)
        button_frame.pack(side=tk.LEFT, padx=20)


        clear_button = tk.Button(button_frame, text="Clear All", command=lambda: self.clear_grid(canvas))
        clear_button.grid(row=0, column=0, pady=5, sticky=tk.W)

        btn_add_example = tk.Button(button_frame, text="Add Example Points", command=lambda: self.addExample(canvas))
        btn_add_example.grid(row=1, column=0, pady=5, sticky=tk.W)

        btn_generate = tk.Button(button_frame, text="Generate Path",
                                 command=lambda: self.generate_path_and_display(canvas))
        btn_generate.grid(row=2, column=0, pady=5, sticky=tk.W)

        self.draw_initial_grid(canvas)

        root.mainloop()

if __name__ == "__main__":
    m = Main((5, 5, 5))
    m.main()
