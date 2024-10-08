import pygame
import time
import math
from queue import PriorityQueue

# Define game window
WIDTH = 800
MENU_WIDTH = 200
WIN = pygame.display.set_mode((WIDTH + MENU_WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding (3.0)")

pygame.font.init()

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
DARKGREY = (50, 50, 50)
TURQUOISE = (64, 224, 208)

# Define button states
SELECT_NONE = 0
SELECT_START = 1
SELECT_END = 2
SELECT_BARRIER = 3
SELECT_WAYPOINT = 4

selected_type = SELECT_NONE

# Define buttons' positions and sizes
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 50
START_BUTTON_POS = (WIDTH + 10, 50)
END_BUTTON_POS = (WIDTH + 10, 120)
BARRIER_BUTTON_POS = (WIDTH + 10, 190)
WAYPOINT_BUTTON_POS = (WIDTH + 10, 260)
SLIDER_POS = (WIDTH + 10, 380)  # Position for the slider

waypoints = []

grid_size = 20  # Default grid size


# Class spot represents a single tile/square on the grid.
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_waypoint(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED  # Mark the spot as closed

    def make_open(self):
        self.color = GREEN  # Mark the spot as open

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_waypoint(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)  # Clear the screen with white
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)  # Draw grid lines
    draw_side_menu(win)


def draw_button(win, pos, text, color):
    pygame.draw.rect(win, color, (*pos, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    win.blit(text_surface, (pos[0] + 10, pos[1] + 10))


def draw_slider(win, pos, value, min_val=10, max_val=50):
    pygame.draw.rect(win, DARKGREY, (*pos, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"Grid Size: {value}", True, WHITE)
    win.blit(text_surface, (pos[0] + 10, pos[1] + 10))

    # Slider bar
    pygame.draw.rect(win, GREY, (pos[0] + 10, pos[1] + 60, BUTTON_WIDTH - 20, 10))
    # Slider knob
    knob_x = int(pos[0] + 10 + ((value - min_val) / (max_val - min_val)) * (BUTTON_WIDTH - 20))
    pygame.draw.circle(win, WHITE, (knob_x, pos[1] + 65), 10)


def draw_side_menu(win):
    startCol = GREY
    endCol = GREY
    barCol = GREY
    waypointCol = GREY

    if selected_type == SELECT_START:
        startCol = DARKGREY
    if selected_type == SELECT_END:
        endCol = DARKGREY
    if selected_type == SELECT_BARRIER:
        barCol = DARKGREY
    if selected_type == SELECT_WAYPOINT:
        waypointCol = DARKGREY

    draw_button(win, START_BUTTON_POS, "Start", startCol)
    draw_button(win, END_BUTTON_POS, "End", endCol)
    draw_button(win, BARRIER_BUTTON_POS, "Barrier", barCol)
    draw_button(win, WAYPOINT_BUTTON_POS, "Waypoint", waypointCol)

    draw_slider(win, SLIDER_POS, grid_size)  # Draw the slider

    pygame.draw.line(win, GREY, (WIDTH, 0), (WIDTH, 800), 1)


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def handle_slider_input(pos, slider_pos, current_value, min_val=10, max_val=50):
    slider_x, slider_y = slider_pos
    if slider_x <= pos[0] <= slider_x + BUTTON_WIDTH and slider_y <= pos[1] <= slider_y + 60:
        # Calculate new slider value
        new_value = min_val + ((pos[0] - slider_x) / BUTTON_WIDTH) * (max_val - min_val)
        return int(new_value)
    return current_value

def algorithm(draw, grid, start, end):
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

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    # neighbor.make_open()
        draw()

        if current != start:
            pass
            # current.make_closed()

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


def handle_slider_input(pos, slider_pos, current_value, min_val=10, max_val=50):
    slider_x, slider_y = slider_pos
    if slider_x <= pos[0] <= slider_x + BUTTON_WIDTH and slider_y <= pos[1] <= slider_y + 60:
        # Calculate new slider value
        new_value = min_val + ((pos[0] - slider_x) / (BUTTON_WIDTH - 20)) * (max_val - min_val)
        return int(new_value)
    return current_value

def main(win, width):
    global selected_type
    global waypoints
    global grid_size

    ROWS = grid_size
    grid = make_grid(ROWS, width)
    start = None
    end = None

    mouse_pressed = False
    slider_pos = SLIDER_POS
    slider_rect = pygame.Rect(slider_pos[0], slider_pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)  # Define the slider area

    run = True
    while run:
        draw(win, grid, ROWS, width)  # Draw grid and spots
        draw_side_menu(win)  # Draw the side menu with the slider
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pressed = True
                    pos = pygame.mouse.get_pos()
                    if slider_rect.collidepoint(pos):
                        grid_size = handle_slider_input(pos, slider_pos, grid_size)
                        ROWS = int(grid_size)
                        grid = make_grid(ROWS, width)
                    elif START_BUTTON_POS[0] <= pos[0] <= START_BUTTON_POS[0] + BUTTON_WIDTH and START_BUTTON_POS[1] <= pos[1] <= START_BUTTON_POS[1] + BUTTON_HEIGHT:
                        selected_type = SELECT_START
                    elif END_BUTTON_POS[0] <= pos[0] <= END_BUTTON_POS[0] + BUTTON_WIDTH and END_BUTTON_POS[1] <= pos[1] <= END_BUTTON_POS[1] + BUTTON_HEIGHT:
                        selected_type = SELECT_END
                    elif BARRIER_BUTTON_POS[0] <= pos[0] <= BARRIER_BUTTON_POS[0] + BUTTON_WIDTH and BARRIER_BUTTON_POS[1] <= pos[1] <= BARRIER_BUTTON_POS[1] + BUTTON_HEIGHT:
                        selected_type = SELECT_BARRIER
                    elif WAYPOINT_BUTTON_POS[0] <= pos[0] <= WAYPOINT_BUTTON_POS[0] + BUTTON_WIDTH and WAYPOINT_BUTTON_POS[1] <= pos[1] <= WAYPOINT_BUTTON_POS[1] + BUTTON_HEIGHT:
                        selected_type = SELECT_WAYPOINT
                    else:
                        if pos[0] < WIDTH:
                            row, col = get_clicked_pos(pos, ROWS, width)
                            spot = grid[row][col]
                            if selected_type == SELECT_START:
                                if start:
                                    start.reset()
                                start = spot
                                start.make_start()
                            elif selected_type == SELECT_END:
                                if end:
                                    end.reset()
                                end = spot
                                end.make_end()
                            elif selected_type == SELECT_BARRIER:
                                if spot != start and spot != end:
                                    spot.make_barrier()
                            elif selected_type == SELECT_WAYPOINT:
                                if spot not in waypoints:
                                    spot.make_waypoint()
                                    waypoints.append(spot)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed = False

            if pygame.mouse.get_pressed()[0]:
                if mouse_pressed:
                    pos = pygame.mouse.get_pos()
                    if slider_rect.collidepoint(pos):
                        grid_size = handle_slider_input(pos, slider_pos, grid_size)
                        ROWS = int(grid_size)
                        grid = make_grid(ROWS, width)
                    elif pos[0] < WIDTH:
                        row, col = get_clicked_pos(pos, ROWS, width)
                        spot = grid[row][col]
                        if selected_type == SELECT_START:
                            if start:
                                start.reset()
                            start = spot
                            start.make_start()
                        elif selected_type == SELECT_END:
                            if end:
                                end.reset()
                            end = spot
                            end.make_end()
                        elif selected_type == SELECT_BARRIER:
                            if spot != start and spot != end:
                                spot.make_barrier()
                        elif selected_type == SELECT_WAYPOINT:
                            if spot not in waypoints:
                                spot.make_waypoint()
                                waypoints.append(spot)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    startTime = time.time()
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    endTime = time.time()
                    print("Processing time: " + str(endTime - startTime) + "s")

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    waypoints = []

                if event.key == pygame.K_ESCAPE:
                    run = False

    pygame.quit()






main(WIN, WIDTH)
