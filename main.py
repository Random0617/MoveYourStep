from Tile import Tile
import pygame
import time
import math

# Initializing constants (global variables)
WHITE = (255, 255, 255)  # empty tile (except starting tile)
RED = (255, 0, 0)  # starting tile
GRAY = (128, 128, 128)  # obstacle tile
YELLOW = (255, 255, 0)  # key tile
ORANGE = (255, 127, 0)  # door tile
BLUE = (0, 0, 255)  # finish tile
BLACK = (0, 0, 0)  # text color

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

pygame.init()
font = pygame.font.Font("HighlandGothicFLF.ttf", 20)

def set_height_or_width(filename, k):
    input_file = open(filename, "r")
    sizes = input_file.readline().split(",")
    result = int(sizes[k])  # 0 for height, 1 for width
    input_file.close()
    return result


def reset_tiles(filename, width, height):
    # Get data for all tiles from the text file
    input_file = open(filename, "r")
    sizes = input_file.readline().split(",")
    print(str(height) + " " + str(width))
    floor = input_file.readline()
    print(floor)
    tiles = []
    for k in range(height):
        row = []
        row_stats = input_file.readline().split(",")
        print(row_stats)
        for i in row_stats:
            new_tile = Tile(1, 0)  # Empty tile
            if "A" in i:  # Empty tile and starting tile
                new_tile.type = 0
            elif "-1" in i:  # Tile is an obstacle
                new_tile.type = -2
            elif "D" in i:  # Tile is a door
                new_tile.type = -1
                new_tile.value = int(i[1:])
            elif "K" in i:  # Tile is a key
                new_tile.type = 2
                new_tile.value = int(i[1:])
            elif "T" in i:  # Tile is Mr. Thanh (goal)
                new_tile.type = 3
            row.append(new_tile)
        for i in row:
            print(str(i.type) + " " + str(i.value))
        tiles.append(row)
    input_file.close()
    return tiles

# Initializing surface
def draw_state(tiles, width, height):
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    TILE_WIDTH = math.floor(SCREEN_WIDTH / width)
    TILE_HEIGHT = math.floor(SCREEN_HEIGHT / height)
    for i in range(height):
        for k in range(width):
            text = font.render(str(tiles[i][k].value), True, BLACK)
            color = WHITE
            if tiles[i][k].type == -2:
                color = GRAY
            elif tiles[i][k].type == -1:
                color = ORANGE
            elif tiles[i][k].type == 0:
                color = RED
            elif tiles[i][k].type == 2:
                color = YELLOW
            elif tiles[i][k].type == 3:
                color = BLUE
            pygame.draw.rect(surface, color,
                             pygame.Rect(TILE_WIDTH * k, TILE_HEIGHT * i + 2, TILE_WIDTH - 2, TILE_HEIGHT - 2))
            if tiles[i][k].type == -1 or tiles[i][k].type == 2:
                text_width = text.get_rect().width
                text_height = text.get_rect().height
                text_x = (TILE_WIDTH * k + TILE_WIDTH * (k + 1)) / 2 - text_width / 2
                text_y = (TILE_HEIGHT * i + TILE_HEIGHT * (i + 1)) / 2 - text_height / 2
                surface.blit(text, (text_x, text_y))
    pygame.display.flip()  # compulsory


def draw_path(tiles, path, width, height):
    draw_state(tiles, width, height)
    for i in range(len(path)):
        time.sleep(0.1)
        tiles[path[i][0]][path[i][1]].type = 0
        draw_state(tiles, width, height)

def tile_available(tiles, tile_row, tile_col, height_limit, width_limit):
    if (0 <= tile_row < height_limit and 0 <= tile_col < width_limit
            and (tiles[tile_row][tile_col].type in [0, 1, 3])):
        return 1
    else:
        return 0

def level1_BFS(tiles, width, height):
    height_limit = height
    width_limit = width
    class BFS_Tile:
        def __init__(self, row, col, type, expanded, added_to_queue, distance, prev_cell):
            self.row = row
            self.col = col
            self.type = type # int: 0, 1, -2, 3
            self.expanded = expanded # bool
            self.added_to_queue = added_to_queue # bool
            self.distance = distance # int
            self.prev_cell = prev_cell # two-element array showing coordinates

    BFS_tiles = []
    starting_row = -1
    starting_col = -1
    finishing_row = -1
    finishing_col = -1
    for i in range(height):
        row = []
        for k in range(width):
            BFStile = BFS_Tile(i, k, tiles[i][k].type, False, False, 999999, [-1, -1])
            row.append(BFStile)
            if tiles[i][k].type == 0:
                starting_row = i
                starting_col = k
            if tiles[i][k].type == 3:
                finishing_row = i
                finishing_col = k
        BFS_tiles.append(row)
    print(str(starting_row) + " " + str(starting_col))
    print(str(finishing_row) + " " + str(finishing_col))
    priority_queue = []
    priority_queue.append(BFS_tiles[starting_row][starting_col])
    BFS_tiles[starting_row][starting_col].added_to_queue = True
    BFS_tiles[starting_row][starting_col].distance = 0
    while len(priority_queue) > 0:
        visiting_cell = priority_queue[0]
        BFS_tiles[visiting_cell.row][visiting_cell.col].expanded = True
        print("Set BFS_tiles[" + str(visiting_cell.row) + "][" + str(visiting_cell.col) + "] = True")
        priority_queue.pop(0)
        cur_x = visiting_cell.row
        cur_y = visiting_cell.col
        print("Start adding neighbors for " + str(cur_x) + ", " + str(cur_y))
        top_left = [cur_x - 1, cur_y - 1]
        top_middle = [cur_x - 1, cur_y]
        top_right = [cur_x - 1, cur_y + 1]
        middle_left = [cur_x, cur_y - 1]
        middle_right = [cur_x, cur_y + 1]
        bottom_left = [cur_x + 1, cur_y - 1]
        bottom_middle = [cur_x + 1, cur_y]
        bottom_right = [cur_x + 1, cur_y + 1]
        neighbors = [top_left, top_middle, top_right, middle_left, middle_right, bottom_left, bottom_middle, bottom_right]
        # If a neighbor is available (not out of bounds) and has not been added to queue before
        '''
        for i in range(len(neighbors)):
            if (tile_available(BFS_tiles, neighbors[i][0], neighbors[i][1], height_limit, width_limit) and
                    BFS_tiles[neighbors[i][0]][neighbors[i][1]].added_to_queue == False):
                priority_queue.append(BFS_tiles[neighbors[i][0]][neighbors[i][1]])
                BFS_tiles[neighbors[i][0]][neighbors[i][1]].added_to_queue = True
                print("Add to queue: " + str(neighbors[i][0]) + ", " + str(neighbors[i][1]))
        '''
        if (tile_available(BFS_tiles, top_left[0], top_left[1], height_limit, width_limit)
                and BFS_tiles[top_left[0]][top_left[1]].expanded == False
                and (BFS_tiles[top_middle[0]][top_middle[1]].type == 0 or BFS_tiles[top_middle[0]][
                    top_middle[1]].type == 1)
                and (BFS_tiles[middle_left[0]][middle_left[1]].type == 0 or BFS_tiles[middle_left[0]][
                    middle_left[1]].type == 1)):
            if not BFS_tiles[top_left[0]][top_left[1]].added_to_queue:
                priority_queue.append(BFS_tiles[top_left[0]][top_left[1]])
                BFS_tiles[top_left[0]][top_left[1]].added_to_queue = True
                BFS_tiles[top_left[0]][top_left[1]].distance = min(BFS_tiles[top_left[0]][top_left[1]].distance,
                                                                   BFS_tiles[cur_x][cur_y].distance + 1)
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[top_left[0]][top_left[1]].distance:
                BFS_tiles[top_left[0]][top_left[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[top_left[0]][top_left[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, top_right[0], top_right[1], height_limit, width_limit)
                and BFS_tiles[top_right[0]][top_right[1]].expanded == False
                and (BFS_tiles[top_middle[0]][top_middle[1]].type == 0 or BFS_tiles[top_middle[0]][
                    top_middle[1]].type == 1)
                and (BFS_tiles[middle_right[0]][middle_right[1]].type == 0 or BFS_tiles[middle_right[0]][
                    middle_right[1]].type == 1)):
            if not BFS_tiles[top_right[0]][top_right[1]].added_to_queue:
                priority_queue.append(BFS_tiles[top_right[0]][top_right[1]])
                BFS_tiles[top_right[0]][top_right[1]].added_to_queue = True
                BFS_tiles[top_right[0]][top_right[1]].distance = min(BFS_tiles[top_right[0]][top_right[1]].distance,
                                                                   BFS_tiles[cur_x][cur_y].distance + 1)
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[top_right[0]][top_right[1]].distance:
                BFS_tiles[top_right[0]][top_right[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[top_right[0]][top_right[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, bottom_left[0], bottom_left[1], height_limit, width_limit)
                and BFS_tiles[bottom_left[0]][bottom_left[1]].expanded == False
                and (BFS_tiles[bottom_middle[0]][bottom_middle[1]].type == 0 or BFS_tiles[bottom_middle[0]][
                    bottom_middle[1]].type == 1)
                and (BFS_tiles[middle_left[0]][middle_left[1]].type == 0 or BFS_tiles[middle_left[0]][
                    middle_left[1]].type == 1)):
            if not BFS_tiles[bottom_left[0]][bottom_left[1]].added_to_queue:
                priority_queue.append(BFS_tiles[bottom_left[0]][bottom_left[1]])
                BFS_tiles[bottom_left[0]][bottom_left[1]].added_to_queue = True
                BFS_tiles[bottom_left[0]][bottom_left[1]].distance = min(BFS_tiles[bottom_left[0]][bottom_left[1]].distance,
                                                                   BFS_tiles[cur_x][cur_y].distance + 1)
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[bottom_left[0]][bottom_left[1]].distance:
                BFS_tiles[bottom_left[0]][bottom_left[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[bottom_left[0]][bottom_left[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, bottom_right[0], bottom_right[1], height_limit, width_limit)
                and BFS_tiles[bottom_right[0]][bottom_right[1]].expanded == False
                and (BFS_tiles[bottom_middle[0]][bottom_middle[1]].type == 0 or BFS_tiles[bottom_middle[0]][
                    bottom_middle[1]].type == 1)
                and (BFS_tiles[middle_right[0]][middle_right[1]].type == 0 or BFS_tiles[middle_right[0]][
                    middle_right[1]].type == 1)):
            if not BFS_tiles[bottom_right[0]][bottom_right[1]].added_to_queue:
                priority_queue.append(BFS_tiles[bottom_right[0]][bottom_right[1]])
                BFS_tiles[bottom_right[0]][bottom_right[1]].added_to_queue = True
                BFS_tiles[bottom_right[0]][bottom_right[1]].distance = min(BFS_tiles[bottom_right[0]][bottom_right[1]].distance,
                                                                   BFS_tiles[cur_x][cur_y].distance + 1)
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[bottom_right[0]][bottom_right[1]].distance:
                BFS_tiles[bottom_right[0]][bottom_right[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[bottom_right[0]][bottom_right[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, top_middle[0], top_middle[1], height_limit, width_limit)
                and BFS_tiles[top_middle[0]][top_middle[1]].expanded == False):
            if not BFS_tiles[top_middle[0]][top_middle[1]].added_to_queue:
                priority_queue.append(BFS_tiles[top_middle[0]][top_middle[1]])
                BFS_tiles[top_middle[0]][top_middle[1]].added_to_queue = True
                BFS_tiles[top_middle[0]][top_middle[1]].distance = min(BFS_tiles[top_middle[0]][top_middle[1]].distance,
                                                                   BFS_tiles[cur_x][cur_y].distance + 1)
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[top_middle[0]][top_middle[1]].distance:
                BFS_tiles[top_middle[0]][top_middle[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[top_middle[0]][top_middle[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, middle_right[0], middle_right[1], height_limit, width_limit)
                and BFS_tiles[middle_right[0]][middle_right[1]].expanded == False):
            if not BFS_tiles[middle_right[0]][middle_right[1]].added_to_queue:
                priority_queue.append(BFS_tiles[middle_right[0]][middle_right[1]])
                BFS_tiles[middle_right[0]][middle_right[1]].added_to_queue = True
                BFS_tiles[middle_right[0]][middle_right[1]].distance = min(BFS_tiles[middle_right[0]][middle_right[1]].distance,
                                                                   BFS_tiles[cur_x][cur_y].distance + 1)
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[middle_right[0]][middle_right[1]].distance:
                BFS_tiles[middle_right[0]][middle_right[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[middle_right[0]][middle_right[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, bottom_middle[0], bottom_middle[1], height_limit, width_limit)
                and BFS_tiles[bottom_middle[0]][bottom_middle[1]].expanded == False):
            if not BFS_tiles[bottom_middle[0]][bottom_middle[1]].added_to_queue:
                priority_queue.append(BFS_tiles[bottom_middle[0]][bottom_middle[1]])
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].added_to_queue = True
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].distance = min(BFS_tiles[bottom_middle[0]][bottom_middle[1]].distance,
                                                                   BFS_tiles[cur_x][cur_y].distance + 1)
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[bottom_middle[0]][bottom_middle[1]].distance:
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, middle_left[0], middle_left[1], height_limit, width_limit)
                and BFS_tiles[middle_left[0]][middle_left[1]].expanded == False):
            if not BFS_tiles[middle_left[0]][middle_left[1]].added_to_queue:
                priority_queue.append(BFS_tiles[middle_left[0]][middle_left[1]])
                BFS_tiles[middle_left[0]][middle_left[1]].added_to_queue = True
                BFS_tiles[middle_left[0]][middle_left[1]].distance = min(BFS_tiles[middle_left[0]][middle_left[1]].distance,
                                                                   BFS_tiles[cur_x][cur_y].distance + 1)
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[middle_left[0]][middle_left[1]].distance:
                BFS_tiles[middle_left[0]][middle_left[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[middle_left[0]][middle_left[1]].prev_cell = [cur_x, cur_y]
    print("Finishing row: " + str(finishing_row))
    print("Finishing col: " + str(finishing_col))
    print("Finishing cell has been expanded: " + str(BFS_tiles[finishing_row][finishing_col].expanded))
    for i in range(height):
        str_result = ""
        for k in range(width):
            if BFS_tiles[i][k].distance == 999999:
                str_result = str_result + "__ "
            elif BFS_tiles[i][k].distance < 10:
                str_result = str_result + "0" + str(BFS_tiles[i][k].distance) + " "
            else:
                str_result = str_result + str(BFS_tiles[i][k].distance) + " "
        print(str_result)
    return 0
def main():
    input_file = "input1-level1.txt"
    height = set_height_or_width(input_file, 0)
    width = set_height_or_width(input_file, 1)
    tiles = reset_tiles(input_file, width, height)
    draw_state(tiles, width, height)
    level1_BFS(tiles, width, height)
    '''
    # Path: coordinates of the cells gone traveled through, in the correct order
    example_path = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10],
                    [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10],
                    [10, 10], [11, 10], [12, 10], [12, 9], [12, 8], [12, 7]]
    # Call draw_path to color the solution path (in the same form as example_path)
    # The instructor requires that the path be shown step-by-step
    draw_path(tiles, example_path, width, height)
    '''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


main()
