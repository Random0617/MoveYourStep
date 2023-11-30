from Tile import Tile
import pygame
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

# Initializing constants
WHITE = (255, 255, 255) # empty tile (except starting tile)
RED = (255, 0, 0) # starting tile
GRAY = (128, 128, 128) # obstacle tile
YELLOW = (255, 255, 0) # key tile
ORANGE = (255, 127, 0) # door tile
BLUE = (0, 0, 255) # finish tile

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

TILE_WIDTH = math.floor(SCREEN_WIDTH / width)
TILE_HEIGHT = math.floor(SCREEN_HEIGHT / height)

# Initializing surface
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

for i in range(height):
    for k in range(width):
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

# Drawing Rectangle
pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()