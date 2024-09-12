import pygame
import sys
import pygame_gui
from spot import *
from algorithm import *
import time

pygame.init()
pygame.font.init()

font = pygame.font.SysFont(None, 36)

WIDTH, HEIGHT = 1280, 720 #Screen size
GRID_WIDTH = 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder_4.0")

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color("#000000"))

MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))

CLOCK = pygame.time.Clock()

GRID_SIZE = 20

SELECT_NONE = 0
SELECT_START = 1
SELECT_END = 2
SELECT_BARRIER = 3
SELECT_WAYPOINT = 4

selected_type = SELECT_NONE


SIZE_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 100), (400, 50)), manager=MANAGER, object_id="#main_text_entry")
START_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 200), (100, 50)), text="Start", manager=MANAGER)
END_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 300), (100, 50)), text="End", manager=MANAGER)
BARRIER_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 400), (100, 50)), text="Barrier", manager=MANAGER)
CALCULATE_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 500), (100, 50)), text="Calculate", manager=MANAGER)
CLEAR_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000, 500), (100, 50)), text="Clear", manager=MANAGER)

def make_grid(rows, width):
    grid = []
    gap = width / rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width / rows
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

    pygame.draw.line(win, GREY, (GRID_WIDTH, 0), (GRID_WIDTH, 720), 1)

def draw(win, grid, rows, width):
    win.fill(WHITE)  # Clear the screen with white
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)  # Draw grid lines

    grid_text = font.render(f"Grid size: " +  str(GRID_SIZE), True, BLACK)
    SCREEN.blit(grid_text, (800, 50))

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def adjustSelect(button):
    buttons = [START_BUTTON, END_BUTTON, BARRIER_BUTTON, CALCULATE_BUTTON]
    button.select()
    for b in buttons:
        if b != button:
            b.unselect()




def main():
    global GRID_SIZE
    grid = make_grid(GRID_SIZE, GRID_WIDTH)
    start = None
    end = None
    mouse_pressed = False
    processing_time = None

    global selected_type


    while True:
        UI_REFRESH_RATE = CLOCK.tick(60)/1000

        MANAGER.update(UI_REFRESH_RATE)

        SCREEN.blit(background, (0, 0))
        draw(SCREEN, grid, GRID_SIZE, GRID_WIDTH)  # Draw the grid
        MANAGER.draw_ui(SCREEN)

        if processing_time is not None:
            # Render the processing time as text and display it on the screen
            time_text = font.render(f"Processing time: {processing_time:.2f}s", True, (255, 0, 0))
            SCREEN.blit(time_text, (800, 600))  # Position it at (800, 600), adjust as needed

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                GRID_SIZE = int(event.text)
                grid = make_grid(GRID_SIZE, GRID_WIDTH)

            # Handle button input
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == START_BUTTON:
                    selected_type = SELECT_START
                    adjustSelect(START_BUTTON)
                elif event.ui_element == END_BUTTON:
                    selected_type = SELECT_END
                    adjustSelect(END_BUTTON)
                elif event.ui_element == BARRIER_BUTTON:
                    selected_type = SELECT_BARRIER
                    adjustSelect(BARRIER_BUTTON)
                elif event.ui_element == CLEAR_BUTTON:


                    start = None
                    end = None
                    grid = make_grid(GRID_SIZE, GRID_WIDTH)
                elif event.ui_element == CALCULATE_BUTTON and start and end:


                    startTime = time.time()
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(SCREEN, grid, GRID_SIZE, GRID_WIDTH), grid, start, end)
                    endTime = time.time()
                    processing_time = endTime - startTime
                    # print("Processing time: " + str(processing_time) + "s")


            # Mouse click events for selecting grid cells
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pressed = True
                    pos = pygame.mouse.get_pos()
                    if pos[0] < GRID_WIDTH:  # Only allow interaction within the grid
                        row, col = get_clicked_pos(pos, GRID_SIZE, GRID_WIDTH)
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

                elif event.button == 3:
                    mouse_pressed = True
                    pos = pygame.mouse.get_pos()
                    if pos[0] < GRID_WIDTH:  # Only allow interaction within the grid
                        row, col = get_clicked_pos(pos, GRID_SIZE, GRID_WIDTH)
                        spot = grid[row][col]
                        spot.reset()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed = False


            if pygame.mouse.get_pressed()[0]:
                if mouse_pressed:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < GRID_WIDTH:
                        row, col = get_clicked_pos(pos, GRID_SIZE, GRID_WIDTH)
                        spot = grid[row][col]
                        if selected_type == SELECT_BARRIER:
                            if spot != start and spot != end:
                                spot.make_barrier()

            # Pass the event to pygame_gui
            MANAGER.process_events(event)



main()
