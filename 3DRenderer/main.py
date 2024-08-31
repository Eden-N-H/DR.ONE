from object_3d import *
from camera import *
from projection import *
import pygame as pg
from generate_grid import *

class SoftwareRender:
    def __init__(self):
        pg.init() # Initialize pygame
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900 # Determine RES -> width/height of pygame window
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2 # calc half width/height -> center of screen
        self.FPS = 60 # set target FPS
        self.screen = pg.display.set_mode(self.RES) # creates main window
        self.clock = pg.time.Clock() # set the clock
        self.create_objects() # Create 3d object

    def create_objects(self):
        self.camera = Camera(self, [-5, 6, -55]) # creates a camera at a specified point in 3d space
        self.projection = Projection(self) # create instance of projection class
        self.object = self.get_object_from_file('3DRenderer/3DResources/cube.obj') # specifies obj file location
        self.object.rotate_y(-math.pi / 4) # applies a rotation to object to orient correctly in regard to screen

    def get_object_from_file(self, filename): # function reads data from obj file to render faces and vertexes.
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '): # retrieve vertex data
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'): # retrieve face data
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self): # renders the current frame on screen
        self.screen.fill(pg.Color('darkslategray')) # colors the entire screen
        self.object.draw() # draws the object

    def run(self): # updates and renders the scene continuously while handling input
        while True:
            self.draw() # update the screen
            self.camera.control() # handle user inputs for camera control, updates camera pos if necessary.
            [exit() for i in pg.event.get() if i.type == pg.QUIT] # exits if quit event occurs
            pg.display.set_caption(str(self.clock.get_fps())) # sets name of window to fps
            pg.display.flip() # updates screen with rendering done in current frame (swaps back with front buffer)
            self.clock.tick(self.FPS) # runs at specified frame rate


if __name__ == '__main__': # render and then run
    app = SoftwareRender()
    app.run()