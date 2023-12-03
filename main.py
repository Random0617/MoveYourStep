from Tile import Tile
import pygame
import time
import math

height = 0
width = 0

# Get data for all tiles from the text file
input_file = open("input1-level2.txt", "r")
sizes = input_file.readline().split(",")
height = int(sizes[0])
width = int(sizes[1])
print(str(height) + " " + str(width))
floor = input_file.readline()
print(floor)

tiles = []

for k in range(height):
    row = []
    row_stats = input_file.readline().split(",")
    print(row_stats)
    for i in row_stats:
        new_tile = Tile(0, 0, 999) # Empty tile
        if "A" in i: # Empty tile and starting tile
            new_tile.distance = 0
        elif "-1" in i: # Tile is an obstacle
            new_tile.type = -1
        elif "K" in i: # Tile is a key
            new_tile.type = 2
            new_tile.value = (int)(i[1:])
        elif "D" in i: # Tile is a door
            new_tile.type = 3
            new_tile.value = (int)(i[1:])
        elif "T" in i: # Tile is Mr. Thanh (goal)
            new_tile.type = 4
        row.append(new_tile)
    for i in row:
        print(str(i.type) + " " + str(i.value) + " " + str(i.distance))
    tiles.append(row)

pygame.init()

# Initializing constants
WHITE = (255, 255, 255) # empty tile (except starting tile)
RED = (255, 0, 0) # starting tile
GRAY = (128, 128, 128) # obstacle tile
YELLOW = (255, 255, 0) # key tile
ORANGE = (255, 127, 0) # door tile
BLUE = (0, 0, 255) # finish tile
BLACK = (0, 0, 0) # text color

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

TILE_WIDTH = math.floor(SCREEN_WIDTH / width)
TILE_HEIGHT = math.floor(SCREEN_HEIGHT / height)

font = pygame.font.Font("HighlandGothicFLF.ttf", 20)

# Initializing surface
def draw_state(tiles):
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    for i in range(height):
        for k in range(width):
            text = font.render(str(tiles[i][k].value), True, BLACK)
            color = WHITE
            if tiles[i][k].distance == 0:
                color = RED
            elif tiles[i][k].type == -1:
                color = GRAY
            elif tiles[i][k].type == 2:
                color = YELLOW
            elif tiles[i][k].type == 3:
                color = ORANGE
            elif tiles[i][k].type == 4:
                color = BLUE
            pygame.draw.rect(surface, color, pygame.Rect(TILE_WIDTH * k, TILE_HEIGHT * i + 2, TILE_WIDTH - 2, TILE_HEIGHT - 2))
            if tiles[i][k].type == 2 or tiles[i][k].type == 3:
                text_width = text.get_rect().width
                text_height = text.get_rect().height
                text_x = (TILE_WIDTH * k + TILE_WIDTH * (k + 1)) / 2 - text_width / 2
                text_y = (TILE_HEIGHT * i + TILE_HEIGHT * (i + 1)) / 2 - text_height / 2
                surface.blit(text, (text_x, text_y))
    pygame.display.flip() # compulsory

def draw_path(tile_state, path):
    draw_state(tiles)
    for i in range(len(path)):
        time.sleep(0.1)
        tiles[path[i][0]][path[i][1]].distance = 0
        draw_state(tiles)

# Path: coordinates of the cells gone traveled through, in the correct order
example_path = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10],
                [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10],
                [10, 10], [11, 10], [12, 10], [12, 9], [12, 8], [12, 7]]
# Call draw_path to color the solution path (in the same form as example_path)
# The instructor requires that the path be shown step-by-step
draw_path(tiles, example_path)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()