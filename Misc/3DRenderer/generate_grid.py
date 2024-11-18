import os


def create_3d_grid(directory, filename, grid_size, spacing, colored_cubes):
    """
    Create an OBJ file for the 3D grid
    :param filename: The name of the file to save the OBJ data. (use 'cube.obj'
    :param grid_size: The number of lines along each axis (X, Y, Z).
    :param spacing: The distance between grid lines.
    :param colored_cubes: Dictionary of cube positions and colors, e.g., {(0, 0, 0): 'red', (1, 1, 1): 'blue'}
    """

    grid_size = grid_size + 1

    if not os.path.exists(directory):
        os.makedirs(directory)

    obj_path = os.path.join(directory, filename)
    mtl_filename = filename.replace('.obj', '.mtl')
    mtl_path = os.path.join(directory, mtl_filename)

    with open(mtl_path, 'w') as mtl_file: # open mtl file for writing
        mtl_file.write("# Material Library\n")
        for color_name in set(colored_cubes.values()): # iterates through colors ad writes material definitions to file
            mtl_file.write(f"newmtl {color_name}\n")
            mtl_file.write(f"Ka 1.0 1.0 1.0\n")
            mtl_file.write(f"Kd {color_name} {color_name} {color_name}\n")
            mtl_file.write(f"Ks 0.0 0.0 0.0\n")

    with open(obj_path, 'w') as file: # open obj file for writing -> adds a comment and link to mtl file
        file.write("# 3D Grid\n")
        file.write(f"mtllib {mtl_filename}\n")

        # generates vertices for each cube in the frid using specified params
        for x in range(grid_size):
            for y in range(grid_size):
                for z in range(grid_size):
                    file.write(f"v {x * spacing} {y * spacing} {z * spacing}\n")

        def write_face(v1, v2, v3, v4, color): # writes face to obj with specified color
            file.write(f"usemtl {color}\n")
            file.write(f"f {v1} {v2} {v3} {v4}\n")

        def index(x, y, z): # calculates a 1 based index -> used to reference vertices when creating faces
            return x * grid_size * grid_size + y * grid_size + z + 1

        # iterates through each cube and gets color -> default if not specified
        for x in range(grid_size - 1):
            for y in range(grid_size - 1):
                for z in range(grid_size - 1):
                    color = colored_cubes.get((x, y, z), 'default')
                    v1 = index(x, y, z)
                    v2 = index(x + 1, y, z)
                    v3 = index(x + 1, y + 1, z)
                    v4 = index(x, y + 1, z)
                    write_face(v1, v2, v3, v4, color)

                    # Top face
                    v5 = index(x, y, z + 1)
                    v6 = index(x + 1, y, z + 1)
                    v7 = index(x + 1, y + 1, z + 1)
                    v8 = index(x, y + 1, z + 1)
                    write_face(v5, v6, v7, v8, color)

                    # Sides
                    write_face(v1, v2, v6, v5, color)
                    write_face(v2, v3, v7, v6, color)
                    write_face(v3, v4, v8, v7, color)
                    write_face(v4, v1, v5, v8, color)

    print(f"3D grid OBJ file '{filename}' created successfully.")

colored_cubes = {(0, 0, 0): 'red', (1, 1, 1): 'blue'}
create_3d_grid('3DResources', 'cube.obj', grid_size=5, spacing=2.0, colored_cubes=colored_cubes)

