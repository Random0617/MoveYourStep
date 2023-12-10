from Tile import Tile

import time
import math
import constants
import pygame

pygame.init()
font = pygame.font.Font(constants.TEXT_FONT, 20)
big_font = pygame.font.Font(constants.TEXT_FONT, 40)

def set_height_or_width(filename, k):
    input_file = open(filename, "r")
    sizes = input_file.readline().split(",")
    result = int(sizes[k])  # 0 for height, 1 for width
    input_file.close()
    return result


def reset_tiles(filename, width, height):
    # Get data for all tiles from the text file
    input_file = open(filename, "r")
    input_file.readline().split(",")
    input_file.readline()
    tiles = []
    for k in range(height):
        row = []
        row_stats = input_file.readline().split(",")
        print(row_stats)
        for i in range(width):
            new_tile = Tile(1, 0)  # Empty tile
            if "A" in row_stats[i]:  # Empty tile and starting tile
                new_tile.type = 0
            elif "-1" in row_stats[i]:  # Tile is an obstacle
                new_tile.type = -2
            elif "D" in row_stats[i]:  # Tile is a door
                new_tile.type = -1
                new_tile.value = int(row_stats[i][1:])
            elif "K" in row_stats[i]:  # Tile is a key
                new_tile.type = 2
                new_tile.value = int(row_stats[i][1:])
            elif "T" in row_stats[i]:  # Tile is Mr. Thanh (goal)
                new_tile.type = 3
            row.append(new_tile)
        tiles.append(row)
    input_file.close()
    return tiles


# Initializing surface
def draw_state(tiles, width, height):
    surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    TILE_WIDTH = math.floor(constants.SCREEN_WIDTH / width)
    TILE_HEIGHT = math.floor(constants.SCREEN_HEIGHT / height)
    for i in range(height):
        for k in range(width):
            text = font.render(str(tiles[i][k].value), True, constants.BLACK)
            color = constants.WHITE
            if tiles[i][k].type == -2:
                color = constants.GRAY
            elif tiles[i][k].type == -1:
                color = constants.ORANGE
            elif tiles[i][k].type == 0:
                color = constants.RED
            elif tiles[i][k].type == 2:
                color = constants.YELLOW
            elif tiles[i][k].type == 3:
                color = constants.BLUE
            pygame.draw.rect(surface, color,
                             pygame.Rect(TILE_WIDTH * k, TILE_HEIGHT * i + 2, TILE_WIDTH - 2, TILE_HEIGHT - 2))
            if tiles[i][k].type == -1 or tiles[i][k].type == 2:
                text_width = text.get_rect().width
                text_height = text.get_rect().height
                text_x = (TILE_WIDTH * k + TILE_WIDTH * (k + 1)) / 2 - text_width / 2
                text_y = (TILE_HEIGHT * i + TILE_HEIGHT * (i + 1)) / 2 - text_height / 2
                surface.blit(text, (text_x, text_y))
    pygame.display.flip()  # compulsory

def unlock_door(tiles, width, height, key_num):
    # Not relevant for level 1, but required to call draw_heatmap_path
    # Call this when the agent touches the key
    tiles_copy = tiles
    for i in range(height):
        for k in range(width):
            if tiles_copy[i][k].value == key_num:
                tiles_copy[i][k].value = 0
                tiles_copy[i][k].type = 1
    return tiles_copy

def draw_heatmap_state(heatmap_tiles, width, height):
    # Reference: https://www.color-hex.com/color-palette/55783
    surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    TILE_WIDTH = math.floor(constants.SCREEN_WIDTH / width)
    TILE_HEIGHT = math.floor(constants.SCREEN_HEIGHT / height)
    for i in range(height):
        for k in range(width):
            text = font.render(str(heatmap_tiles[i][k].value), True, constants.BLACK)
            color = constants.GRAY
            if heatmap_tiles[i][k].type == -2:
                color = constants.GRAY
            elif heatmap_tiles[i][k].type == -1:
                color = constants.ORANGE
            elif heatmap_tiles[i][k].type == 0:
                if heatmap_tiles[i][k].times_travelled == 0:
                    color = constants.RED
                else:
                    color = constants.PATH_COLORS[min(heatmap_tiles[i][k].times_travelled, len(constants.PATH_COLORS) - 1)]
            elif heatmap_tiles[i][k].type == 1:
                if heatmap_tiles[i][k].times_travelled == 0:
                    color = constants.WHITE
                else:
                    color = constants.PATH_COLORS[min(heatmap_tiles[i][k].times_travelled, len(constants.PATH_COLORS) - 1)]
            elif heatmap_tiles[i][k].type == 2:
                color = constants.YELLOW
            elif heatmap_tiles[i][k].type == 3:
                color = constants.BLUE
            pygame.draw.rect(surface, color,
                             pygame.Rect(TILE_WIDTH * k, TILE_HEIGHT * i + 2, TILE_WIDTH - 2, TILE_HEIGHT - 2))
            if heatmap_tiles[i][k].type == -1 or heatmap_tiles[i][k].type == 2:
                text_width = text.get_rect().width
                text_height = text.get_rect().height
                text_x = (TILE_WIDTH * k + TILE_WIDTH * (k + 1)) / 2 - text_width / 2
                text_y = (TILE_HEIGHT * i + TILE_HEIGHT * (i + 1)) / 2 - text_height / 2
                surface.blit(text, (text_x, text_y))


def draw_heatmap_path(tiles, path, width, height):
    # To draw a heatmap, a tile needs to have information about how many times it has been gone through.
    surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    TILE_WIDTH = math.floor(constants.SCREEN_WIDTH / width)
    TILE_HEIGHT = math.floor(constants.SCREEN_HEIGHT / height)

    class HeatmapTile:
        def __init__(self, type, value, times_travelled):
            self.type = type
            self.value = value
            self.times_travelled = times_travelled

    heatmap_tiles = []
    for i in range(height):
        row = []
        for k in range(width):
            heatmap_tile = HeatmapTile(tiles[i][k].type, tiles[i][k].value, 0)
            row.append(heatmap_tile)
        heatmap_tiles.append(row)
    if len(path) > 0:
        excluded_from_numbering = []
        for i in range(len(path)):
            time.sleep(0.2)
            heatmap_tiles[path[i][0]][path[i][1]].times_travelled += 1
            for k in range(i):
                if path[k][0] == path[i][0] and path[k][1] == path[i][1]:
                    excluded_from_numbering.append(k)
                    print("Appended " + str(k))
            if heatmap_tiles[path[i][0]][path[i][1]].type == 2:
                heatmap_tiles = unlock_door(heatmap_tiles, width, height, heatmap_tiles[path[i][0]][path[i][1]].value)
                tiles = unlock_door(tiles, width, height, heatmap_tiles[path[i][0]][path[i][1]].value)
            draw_heatmap_state(heatmap_tiles, width, height)
            for k in range(i + 1):
                if not (k in excluded_from_numbering):
                    text = font.render(str(k + 1), True, constants.BLACK)
                    text_width = text.get_rect().width
                    text_height = text.get_rect().height
                    text_x = (TILE_WIDTH * path[k][1] + TILE_WIDTH * (path[k][1] + 1)) / 2 - text_width / 2
                    text_y = (TILE_HEIGHT * path[k][0] + TILE_HEIGHT * (path[k][0] + 1)) / 2 - text_height / 2
                    surface.blit(text, (text_x, text_y))
            pygame.display.flip()
    else:
        draw_heatmap_state(heatmap_tiles, width, height)
        text = big_font.render("No solution was found.", True, constants.BLACK)
        text_width = text.get_rect().width
        text_height = text.get_rect().height
        text_x = constants.SCREEN_WIDTH / 2 - text_width / 2
        text_y = constants.SCREEN_HEIGHT / 2 - text_height / 2
        surface.blit(text, (text_x, text_y))
        pygame.display.flip()


def tile_available(tiles, tile_row, tile_col, height_limit, width_limit):
    if (0 <= tile_row < height_limit and 0 <= tile_col < width_limit
            and (tiles[tile_row][tile_col].type in [0, 1, 2, 3])):
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
            self.type = type  # int: 0, 1, -2, 3
            self.expanded = expanded  # bool
            self.added_to_queue = added_to_queue  # bool
            self.distance = distance  # int
            self.prev_cell = prev_cell  # two-element array showing coordinates

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
                BFS_tiles[top_left[0]][top_left[1]].prev_cell = [cur_x, cur_y]
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
                BFS_tiles[top_right[0]][top_right[1]].prev_cell = [cur_x, cur_y]
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
                BFS_tiles[bottom_left[0]][bottom_left[1]].distance = min(
                    BFS_tiles[bottom_left[0]][bottom_left[1]].distance,
                    BFS_tiles[cur_x][cur_y].distance + 1)
                BFS_tiles[bottom_left[0]][bottom_left[1]].prev_cell = [cur_x, cur_y]
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
                BFS_tiles[bottom_right[0]][bottom_right[1]].distance = min(
                    BFS_tiles[bottom_right[0]][bottom_right[1]].distance,
                    BFS_tiles[cur_x][cur_y].distance + 1)
                BFS_tiles[bottom_right[0]][bottom_right[1]].prev_cell = [cur_x, cur_y]
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
                BFS_tiles[top_middle[0]][top_middle[1]].prev_cell = [cur_x, cur_y]
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[top_middle[0]][top_middle[1]].distance:
                BFS_tiles[top_middle[0]][top_middle[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[top_middle[0]][top_middle[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, middle_right[0], middle_right[1], height_limit, width_limit)
                and BFS_tiles[middle_right[0]][middle_right[1]].expanded == False):
            if not BFS_tiles[middle_right[0]][middle_right[1]].added_to_queue:
                priority_queue.append(BFS_tiles[middle_right[0]][middle_right[1]])
                BFS_tiles[middle_right[0]][middle_right[1]].added_to_queue = True
                BFS_tiles[middle_right[0]][middle_right[1]].distance = min(
                    BFS_tiles[middle_right[0]][middle_right[1]].distance,
                    BFS_tiles[cur_x][cur_y].distance + 1)
                BFS_tiles[middle_right[0]][middle_right[1]].prev_cell = [cur_x, cur_y]
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[middle_right[0]][middle_right[1]].distance:
                BFS_tiles[middle_right[0]][middle_right[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[middle_right[0]][middle_right[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, bottom_middle[0], bottom_middle[1], height_limit, width_limit)
                and BFS_tiles[bottom_middle[0]][bottom_middle[1]].expanded == False):
            if not BFS_tiles[bottom_middle[0]][bottom_middle[1]].added_to_queue:
                priority_queue.append(BFS_tiles[bottom_middle[0]][bottom_middle[1]])
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].added_to_queue = True
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].distance = min(
                    BFS_tiles[bottom_middle[0]][bottom_middle[1]].distance,
                    BFS_tiles[cur_x][cur_y].distance + 1)
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].prev_cell = [cur_x, cur_y]
            if BFS_tiles[cur_x][cur_y].distance + 1 < BFS_tiles[bottom_middle[0]][bottom_middle[1]].distance:
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].distance = BFS_tiles[cur_x][cur_y].distance + 1
                BFS_tiles[bottom_middle[0]][bottom_middle[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(BFS_tiles, middle_left[0], middle_left[1], height_limit, width_limit)
                and BFS_tiles[middle_left[0]][middle_left[1]].expanded == False):
            if not BFS_tiles[middle_left[0]][middle_left[1]].added_to_queue:
                priority_queue.append(BFS_tiles[middle_left[0]][middle_left[1]])
                BFS_tiles[middle_left[0]][middle_left[1]].added_to_queue = True
                BFS_tiles[middle_left[0]][middle_left[1]].distance = min(
                    BFS_tiles[middle_left[0]][middle_left[1]].distance,
                    BFS_tiles[cur_x][cur_y].distance + 1)
                BFS_tiles[middle_left[0]][middle_left[1]].prev_cell = [cur_x, cur_y]
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
    solution = []
    if BFS_tiles[finishing_row][finishing_col].expanded:
        cur_x = finishing_row
        cur_y = finishing_col
        while not (cur_x == starting_row and cur_y == starting_col):
            solution.append([cur_x, cur_y])
            print("Add to solution: " + str(cur_x) + " " + str(cur_y))
            temp = BFS_tiles[cur_x][cur_y]
            cur_x = temp.prev_cell[0]
            cur_y = temp.prev_cell[1]
        solution.reverse()
    return solution


def level1_UCS(tiles, width, height):
    height_limit = height
    width_limit = width

    class UCS_Tile:
        def __init__(self, row, col, type, expanded, added_to_queue, distance, prev_cell):
            self.row = row
            self.col = col
            self.type = type  # int: 0, 1, -2, 3
            self.expanded = expanded  # bool
            self.added_to_queue = added_to_queue  # bool
            self.distance = distance  # int
            self.prev_cell = prev_cell  # two-element array showing coordinates

    UCS_tiles = []
    starting_row = -1
    starting_col = -1
    finishing_row = -1
    finishing_col = -1
    for i in range(height):
        row = []
        for k in range(width):
            UCStile = UCS_Tile(i, k, tiles[i][k].type, False, False, 999999, [-1, -1])
            row.append(UCStile)
            if tiles[i][k].type == 0:
                starting_row = i
                starting_col = k
            if tiles[i][k].type == 3:
                finishing_row = i
                finishing_col = k
        UCS_tiles.append(row)
    print(str(starting_row) + " " + str(starting_col))
    print(str(finishing_row) + " " + str(finishing_col))
    priority_queue = []
    priority_queue.append(UCS_tiles[starting_row][starting_col])
    UCS_tiles[starting_row][starting_col].added_to_queue = True
    UCS_tiles[starting_row][starting_col].distance = 0
    while len(priority_queue) > 0:
        # In this project, all moves have an equal cost.
        # The only difference between BFS and UCS is that BFS visits the node at front of the queue,
        # while UCS visits the unvisited node with the smallest known distance
        popped_index = -1
        smallest_known_distance = 999999
        for i in range(len(priority_queue)):
            if priority_queue[i].distance < smallest_known_distance:
                smallest_known_distance = priority_queue[i].distance
                popped_index = popped_index - popped_index + i
        visiting_cell = priority_queue[popped_index]
        UCS_tiles[visiting_cell.row][visiting_cell.col].expanded = True
        print("Set UCS_tiles[" + str(visiting_cell.row) + "][" + str(visiting_cell.col) + "] = True")
        priority_queue.pop(popped_index)
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
        if (tile_available(UCS_tiles, top_left[0], top_left[1], height_limit, width_limit)
                and UCS_tiles[top_left[0]][top_left[1]].expanded == False
                and (UCS_tiles[top_middle[0]][top_middle[1]].type == 0 or UCS_tiles[top_middle[0]][
                    top_middle[1]].type == 1)
                and (UCS_tiles[middle_left[0]][middle_left[1]].type == 0 or UCS_tiles[middle_left[0]][
                    middle_left[1]].type == 1)):
            if not UCS_tiles[top_left[0]][top_left[1]].added_to_queue:
                priority_queue.append(UCS_tiles[top_left[0]][top_left[1]])
                UCS_tiles[top_left[0]][top_left[1]].added_to_queue = True
                UCS_tiles[top_left[0]][top_left[1]].distance = min(UCS_tiles[top_left[0]][top_left[1]].distance,
                                                                   UCS_tiles[cur_x][cur_y].distance + 1)
                UCS_tiles[top_left[0]][top_left[1]].prev_cell = [cur_x, cur_y]
            if UCS_tiles[cur_x][cur_y].distance + 1 < UCS_tiles[top_left[0]][top_left[1]].distance:
                UCS_tiles[top_left[0]][top_left[1]].distance = UCS_tiles[cur_x][cur_y].distance + 1
                UCS_tiles[top_left[0]][top_left[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(UCS_tiles, top_right[0], top_right[1], height_limit, width_limit)
                and UCS_tiles[top_right[0]][top_right[1]].expanded == False
                and (UCS_tiles[top_middle[0]][top_middle[1]].type == 0 or UCS_tiles[top_middle[0]][
                    top_middle[1]].type == 1)
                and (UCS_tiles[middle_right[0]][middle_right[1]].type == 0 or UCS_tiles[middle_right[0]][
                    middle_right[1]].type == 1)):
            if not UCS_tiles[top_right[0]][top_right[1]].added_to_queue:
                priority_queue.append(UCS_tiles[top_right[0]][top_right[1]])
                UCS_tiles[top_right[0]][top_right[1]].added_to_queue = True
                UCS_tiles[top_right[0]][top_right[1]].distance = min(UCS_tiles[top_right[0]][top_right[1]].distance,
                                                                     UCS_tiles[cur_x][cur_y].distance + 1)
                UCS_tiles[top_right[0]][top_right[1]].prev_cell = [cur_x, cur_y]
            if UCS_tiles[cur_x][cur_y].distance + 1 < UCS_tiles[top_right[0]][top_right[1]].distance:
                UCS_tiles[top_right[0]][top_right[1]].distance = UCS_tiles[cur_x][cur_y].distance + 1
                UCS_tiles[top_right[0]][top_right[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(UCS_tiles, bottom_left[0], bottom_left[1], height_limit, width_limit)
                and UCS_tiles[bottom_left[0]][bottom_left[1]].expanded == False
                and (UCS_tiles[bottom_middle[0]][bottom_middle[1]].type == 0 or UCS_tiles[bottom_middle[0]][
                    bottom_middle[1]].type == 1)
                and (UCS_tiles[middle_left[0]][middle_left[1]].type == 0 or UCS_tiles[middle_left[0]][
                    middle_left[1]].type == 1)):
            if not UCS_tiles[bottom_left[0]][bottom_left[1]].added_to_queue:
                priority_queue.append(UCS_tiles[bottom_left[0]][bottom_left[1]])
                UCS_tiles[bottom_left[0]][bottom_left[1]].added_to_queue = True
                UCS_tiles[bottom_left[0]][bottom_left[1]].distance = min(
                    UCS_tiles[bottom_left[0]][bottom_left[1]].distance,
                    UCS_tiles[cur_x][cur_y].distance + 1)
                UCS_tiles[bottom_left[0]][bottom_left[1]].prev_cell = [cur_x, cur_y]
            if UCS_tiles[cur_x][cur_y].distance + 1 < UCS_tiles[bottom_left[0]][bottom_left[1]].distance:
                UCS_tiles[bottom_left[0]][bottom_left[1]].distance = UCS_tiles[cur_x][cur_y].distance + 1
                UCS_tiles[bottom_left[0]][bottom_left[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(UCS_tiles, bottom_right[0], bottom_right[1], height_limit, width_limit)
                and UCS_tiles[bottom_right[0]][bottom_right[1]].expanded == False
                and (UCS_tiles[bottom_middle[0]][bottom_middle[1]].type == 0 or UCS_tiles[bottom_middle[0]][
                    bottom_middle[1]].type == 1)
                and (UCS_tiles[middle_right[0]][middle_right[1]].type == 0 or UCS_tiles[middle_right[0]][
                    middle_right[1]].type == 1)):
            if not UCS_tiles[bottom_right[0]][bottom_right[1]].added_to_queue:
                priority_queue.append(UCS_tiles[bottom_right[0]][bottom_right[1]])
                UCS_tiles[bottom_right[0]][bottom_right[1]].added_to_queue = True
                UCS_tiles[bottom_right[0]][bottom_right[1]].distance = min(
                    UCS_tiles[bottom_right[0]][bottom_right[1]].distance,
                    UCS_tiles[cur_x][cur_y].distance + 1)
                UCS_tiles[bottom_right[0]][bottom_right[1]].prev_cell = [cur_x, cur_y]
            if UCS_tiles[cur_x][cur_y].distance + 1 < UCS_tiles[bottom_right[0]][bottom_right[1]].distance:
                UCS_tiles[bottom_right[0]][bottom_right[1]].distance = UCS_tiles[cur_x][cur_y].distance + 1
                UCS_tiles[bottom_right[0]][bottom_right[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(UCS_tiles, top_middle[0], top_middle[1], height_limit, width_limit)
                and UCS_tiles[top_middle[0]][top_middle[1]].expanded == False):
            if not UCS_tiles[top_middle[0]][top_middle[1]].added_to_queue:
                priority_queue.append(UCS_tiles[top_middle[0]][top_middle[1]])
                UCS_tiles[top_middle[0]][top_middle[1]].added_to_queue = True
                UCS_tiles[top_middle[0]][top_middle[1]].distance = min(UCS_tiles[top_middle[0]][top_middle[1]].distance,
                                                                       UCS_tiles[cur_x][cur_y].distance + 1)
                UCS_tiles[top_middle[0]][top_middle[1]].prev_cell = [cur_x, cur_y]
            if UCS_tiles[cur_x][cur_y].distance + 1 < UCS_tiles[top_middle[0]][top_middle[1]].distance:
                UCS_tiles[top_middle[0]][top_middle[1]].distance = UCS_tiles[cur_x][cur_y].distance + 1
                UCS_tiles[top_middle[0]][top_middle[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(UCS_tiles, middle_right[0], middle_right[1], height_limit, width_limit)
                and UCS_tiles[middle_right[0]][middle_right[1]].expanded == False):
            if not UCS_tiles[middle_right[0]][middle_right[1]].added_to_queue:
                priority_queue.append(UCS_tiles[middle_right[0]][middle_right[1]])
                UCS_tiles[middle_right[0]][middle_right[1]].added_to_queue = True
                UCS_tiles[middle_right[0]][middle_right[1]].distance = min(
                    UCS_tiles[middle_right[0]][middle_right[1]].distance,
                    UCS_tiles[cur_x][cur_y].distance + 1)
                UCS_tiles[middle_right[0]][middle_right[1]].prev_cell = [cur_x, cur_y]
            if UCS_tiles[cur_x][cur_y].distance + 1 < UCS_tiles[middle_right[0]][middle_right[1]].distance:
                UCS_tiles[middle_right[0]][middle_right[1]].distance = UCS_tiles[cur_x][cur_y].distance + 1
                UCS_tiles[middle_right[0]][middle_right[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(UCS_tiles, bottom_middle[0], bottom_middle[1], height_limit, width_limit)
                and UCS_tiles[bottom_middle[0]][bottom_middle[1]].expanded == False):
            if not UCS_tiles[bottom_middle[0]][bottom_middle[1]].added_to_queue:
                priority_queue.append(UCS_tiles[bottom_middle[0]][bottom_middle[1]])
                UCS_tiles[bottom_middle[0]][bottom_middle[1]].added_to_queue = True
                UCS_tiles[bottom_middle[0]][bottom_middle[1]].distance = min(
                    UCS_tiles[bottom_middle[0]][bottom_middle[1]].distance,
                    UCS_tiles[cur_x][cur_y].distance + 1)
                UCS_tiles[bottom_middle[0]][bottom_middle[1]].prev_cell = [cur_x, cur_y]
            if UCS_tiles[cur_x][cur_y].distance + 1 < UCS_tiles[bottom_middle[0]][bottom_middle[1]].distance:
                UCS_tiles[bottom_middle[0]][bottom_middle[1]].distance = UCS_tiles[cur_x][cur_y].distance + 1
                UCS_tiles[bottom_middle[0]][bottom_middle[1]].prev_cell = [cur_x, cur_y]

        if (tile_available(UCS_tiles, middle_left[0], middle_left[1], height_limit, width_limit)
                and UCS_tiles[middle_left[0]][middle_left[1]].expanded == False):
            if not UCS_tiles[middle_left[0]][middle_left[1]].added_to_queue:
                priority_queue.append(UCS_tiles[middle_left[0]][middle_left[1]])
                UCS_tiles[middle_left[0]][middle_left[1]].added_to_queue = True
                UCS_tiles[middle_left[0]][middle_left[1]].distance = min(
                    UCS_tiles[middle_left[0]][middle_left[1]].distance,
                    UCS_tiles[cur_x][cur_y].distance + 1)
                UCS_tiles[middle_left[0]][middle_left[1]].prev_cell = [cur_x, cur_y]
            if UCS_tiles[cur_x][cur_y].distance + 1 < UCS_tiles[middle_left[0]][middle_left[1]].distance:
                UCS_tiles[middle_left[0]][middle_left[1]].distance = UCS_tiles[cur_x][cur_y].distance + 1
                UCS_tiles[middle_left[0]][middle_left[1]].prev_cell = [cur_x, cur_y]
    print("Finishing row: " + str(finishing_row))
    print("Finishing col: " + str(finishing_col))
    print("Finishing cell has been expanded: " + str(UCS_tiles[finishing_row][finishing_col].expanded))
    for i in range(height):
        str_result = ""
        for k in range(width):
            if UCS_tiles[i][k].distance == 999999:
                str_result = str_result + "__ "
            elif UCS_tiles[i][k].distance < 10:
                str_result = str_result + "0" + str(UCS_tiles[i][k].distance) + " "
            else:
                str_result = str_result + str(UCS_tiles[i][k].distance) + " "
        print(str_result)
    solution = []
    if UCS_tiles[finishing_row][finishing_col].expanded:
        cur_x = finishing_row
        cur_y = finishing_col
        while not (cur_x == starting_row and cur_y == starting_col):
            solution.append([cur_x, cur_y])
            print("Add to solution: " + str(cur_x) + " " + str(cur_y))
            temp = UCS_tiles[cur_x][cur_y]
            cur_x = temp.prev_cell[0]
            cur_y = temp.prev_cell[1]
        solution.reverse()
    return solution

def level1_DFS(tiles, width, height):
    class DFS_Tile:
        def __init__(self, row, col, type, visited, prev_cell):
            self.row = row
            self.col = col
            self.type = type  # int: 0, 1, -2, 3
            self.visited = visited  # bool
            self.prev_cell = prev_cell

    DFS_Tiles = []
    starting_row = -1
    starting_col = -1
    finishing_row = -1
    finishing_col = -1
    for i in range(height):
        row = []
        for k in range(width):
            single_DFS_tile = DFS_Tile(i, k, tiles[i][k].type, False, [-1, -1])
            row.append(single_DFS_tile)
            if tiles[i][k].type == 0:
                starting_row = i
                starting_col = k
            if tiles[i][k].type == 3:
                finishing_row = i
                finishing_col = k
        DFS_Tiles.append(row)
    print(str(starting_row) + " " + str(starting_col))
    print(str(finishing_row) + " " + str(finishing_col))
    cur_x = starting_row
    cur_y = starting_col
    solution = [[cur_x, cur_y]]
    DFS_Tiles[cur_x][cur_y].visited = True
    while (len(solution) > 0 and
           not(solution[len(solution) - 1][0] == finishing_row and solution[len(solution) - 1][1] == finishing_col)):
        cur_x = solution[len(solution) - 1][0]
        cur_y = solution[len(solution) - 1][1]
        top_left = [cur_x - 1, cur_y - 1]
        top_middle = [cur_x - 1, cur_y]
        top_right = [cur_x - 1, cur_y + 1]
        middle_left = [cur_x, cur_y - 1]
        middle_right = [cur_x, cur_y + 1]
        bottom_left = [cur_x + 1, cur_y - 1]
        bottom_middle = [cur_x + 1, cur_y]
        bottom_right = [cur_x + 1, cur_y + 1]
        neighbors = [top_left, top_middle, top_right, middle_left, middle_right,
                     bottom_left, bottom_middle, bottom_right]
        index = 0

        while (index < len(neighbors) and
               ((not tile_available(DFS_Tiles, neighbors[index][0], neighbors[index][1], height, width))
                or (DFS_Tiles[neighbors[index][0]][neighbors[index][1]].visited == True)
               or (neighbors[index] == top_left and (not tile_available(DFS_Tiles, top_middle[0], top_middle[1], height, width)
                                                     or not tile_available(DFS_Tiles, middle_left[0], middle_left[1], height, width)))
               or (neighbors[index] == top_right and (not tile_available(DFS_Tiles, top_middle[0], top_middle[1], height, width)
                                                     or not tile_available(DFS_Tiles, middle_right[0], middle_right[1], height, width)))
               or (neighbors[index] == bottom_left and (not tile_available(DFS_Tiles, bottom_middle[0], bottom_middle[1], height, width)
                                                     or not tile_available(DFS_Tiles, middle_left[0], middle_left[1], height, width)))
               or (neighbors[index] == bottom_right and (not tile_available(DFS_Tiles, bottom_middle[0], bottom_middle[1], height, width)
                                                     or not tile_available(DFS_Tiles, middle_right[0], middle_right[1], height, width))))):
            index += 1
        if index == len(neighbors):
            solution.pop()
            print("Removed last element")
            print("DFS solution: " + str(solution))
        else:
            solution.append([neighbors[index][0], neighbors[index][1]])
            DFS_Tiles[neighbors[index][0]][neighbors[index][1]].visited = True
            print("Append element")
            print("DFS solution: " + str(solution))
    if len(solution) > 0:
        solution.pop(0)
    return solution

# def level1_DFS(tiles, width, height):
#     class DFS_Tile:
#         def __init__(self, row, col, type, visited, prev_cell):
#             self.row = row
#             self.col = col
#             self.type = type  # int: 0, 1, -2, 3
#             self.visited = visited  # bool
#             self.prev_cell = prev_cell  # two-element array showing coordinates

#     DFS_tiles = []
#     starting_row, starting_col, finishing_row, finishing_col = -1, -1, -1, -1

#     for i in range(height):
#         row = []
#         for k in range(width):
#             DFStile = DFS_Tile(i, k, tiles[i][k].type, False, [-1, -1])
#             row.append(DFStile)
#             if tiles[i][k].type == 0:
#                 starting_row, starting_col = i, k
#             if tiles[i][k].type == 3:
#                 finishing_row, finishing_col = i, k
#         DFS_tiles.append(row)

#     stack = [DFS_tiles[starting_row][starting_col]]
#     DFS_tiles[starting_row][starting_col].visited = True

#     while stack:
#         visiting_cell = stack.pop()
#         cur_x, cur_y = visiting_cell.row, visiting_cell.col

#         neighbors = [
#             [cur_x - 1, cur_y - 1], [cur_x - 1, cur_y], [cur_x - 1, cur_y + 1],
#             [cur_x, cur_y - 1], [cur_x, cur_y + 1],
#             [cur_x + 1, cur_y - 1], [cur_x + 1, cur_y], [cur_x + 1, cur_y + 1]
#         ]

#         for neighbor in neighbors:
#             n_row, n_col = neighbor
#             if 0 <= n_row < height and 0 <= n_col < width and not DFS_tiles[n_row][n_col].visited and tiles[n_row][n_col].type != -2:
#                 if (cur_x == n_row or cur_y == n_col) or (tiles[cur_x][n_col].type != -2 and tiles[n_row][cur_y].type != -2):
#                     stack.append(DFS_tiles[n_row][n_col])
#                     DFS_tiles[n_row][n_col].visited = True
#                     DFS_tiles[n_row][n_col].prev_cell = [cur_x, cur_y]

#     solution = []
#     if DFS_tiles[finishing_row][finishing_col].visited:
#         cur_x, cur_y = finishing_row, finishing_col
#         while not (cur_x == starting_row and cur_y == starting_col):
#             solution.append([cur_x, cur_y])
#             temp = DFS_tiles[cur_x][cur_y]
#             cur_x, cur_y = temp.prev_cell[0], temp.prev_cell[1]
#         solution.reverse()

#     return solution

def heuristic(cur_row, cur_col, dest_row, dest_col):
    return max(abs(dest_row - cur_row), abs(dest_col - cur_col))

def level1_Astar(tiles, width, height):
    class DFS_Tile:
        def __init__(self, row, col, type, visited, prev_cell):
            self.row = row
            self.col = col
            self.type = type  # int: 0, 1, -2, 3
            self.visited = visited  # bool
            self.prev_cell = prev_cell

    DFS_Tiles = []
    starting_row = -1
    starting_col = -1
    finishing_row = -1
    finishing_col = -1
    for i in range(height):
        row = []
        for k in range(width):
            single_DFS_tile = DFS_Tile(i, k, tiles[i][k].type, False, [-1, -1])
            row.append(single_DFS_tile)
            if tiles[i][k].type == 0:
                starting_row = i
                starting_col = k
            if tiles[i][k].type == 3:
                finishing_row = i
                finishing_col = k
        DFS_Tiles.append(row)
    print(str(starting_row) + " " + str(starting_col))
    print(str(finishing_row) + " " + str(finishing_col))
    cur_x = starting_row
    cur_y = starting_col
    solution = [[cur_x, cur_y]]
    DFS_Tiles[cur_x][cur_y].visited = True
    while (len(solution) > 0 and
           not(solution[len(solution) - 1][0] == finishing_row and solution[len(solution) - 1][1] == finishing_col)):
        cur_x = solution[len(solution) - 1][0]
        cur_y = solution[len(solution) - 1][1]
        top_left = [cur_x - 1, cur_y - 1]
        top_middle = [cur_x - 1, cur_y]
        top_right = [cur_x - 1, cur_y + 1]
        middle_left = [cur_x, cur_y - 1]
        middle_right = [cur_x, cur_y + 1]
        bottom_left = [cur_x + 1, cur_y - 1]
        bottom_middle = [cur_x + 1, cur_y]
        bottom_right = [cur_x + 1, cur_y + 1]
        neighbor_heuristic_distances = [[top_left, heuristic(top_left[0], top_left[1], finishing_row, finishing_col)],
                                        [top_middle, heuristic(top_middle[0], top_middle[1], finishing_row, finishing_col)],
                                        [top_right, heuristic(top_right[0], top_right[1], finishing_row, finishing_col)],
                                        [middle_left, heuristic(middle_left[0], middle_left[1], finishing_row, finishing_col)],
                                        [middle_right, heuristic(middle_right[0], middle_right[1], finishing_row, finishing_col)],
                                        [bottom_left, heuristic(bottom_left[0], bottom_left[1], finishing_row, finishing_col)],
                                        [bottom_middle, heuristic(bottom_middle[0], bottom_middle[1], finishing_row, finishing_col)],
                                        [bottom_right, heuristic(bottom_right[0], bottom_right[1], finishing_row, finishing_col)]]
        neighbor_heuristic_distances.sort(key=lambda x: x[1], reverse=False)
        neighbors = [neighbor_heuristic_distances[0][0],
                     neighbor_heuristic_distances[1][0],
                     neighbor_heuristic_distances[2][0],
                     neighbor_heuristic_distances[3][0],
                     neighbor_heuristic_distances[4][0],
                     neighbor_heuristic_distances[5][0],
                     neighbor_heuristic_distances[6][0],
                     neighbor_heuristic_distances[7][0]]
        index = 0

        while (index < len(neighbors) and
               ((not tile_available(DFS_Tiles, neighbors[index][0], neighbors[index][1], height, width))
                or (DFS_Tiles[neighbors[index][0]][neighbors[index][1]].visited == True)
               or (neighbors[index] == top_left and (not tile_available(DFS_Tiles, top_middle[0], top_middle[1], height, width)
                                                     or not tile_available(DFS_Tiles, middle_left[0], middle_left[1], height, width)))
               or (neighbors[index] == top_right and (not tile_available(DFS_Tiles, top_middle[0], top_middle[1], height, width)
                                                     or not tile_available(DFS_Tiles, middle_right[0], middle_right[1], height, width)))
               or (neighbors[index] == bottom_left and (not tile_available(DFS_Tiles, bottom_middle[0], bottom_middle[1], height, width)
                                                     or not tile_available(DFS_Tiles, middle_left[0], middle_left[1], height, width)))
               or (neighbors[index] == bottom_right and (not tile_available(DFS_Tiles, bottom_middle[0], bottom_middle[1], height, width)
                                                     or not tile_available(DFS_Tiles, middle_right[0], middle_right[1], height, width))))):
            index += 1
        if index == len(neighbors):
            solution.pop()
            print("Removed last element")
            print("DFS solution: " + str(solution))
        else:
            solution.append([neighbors[index][0], neighbors[index][1]])
            DFS_Tiles[neighbors[index][0]][neighbors[index][1]].visited = True
            print("Append element")
            print("DFS solution: " + str(solution))
    if len(solution) > 0:
        solution.pop(0)
    return solution

def print_level1_BFS(input_file):
    height = set_height_or_width(input_file, 0)
    width = set_height_or_width(input_file, 1)
    tiles = reset_tiles(input_file, width, height)
    draw_state(tiles, width, height)
    level1_BFSsolution = level1_BFS(tiles, width, height)
    draw_heatmap_path(tiles, level1_BFSsolution, width, height)

def print_level1_UCS(input_file):
    height = set_height_or_width(input_file, 0)
    width = set_height_or_width(input_file, 1)
    tiles = reset_tiles(input_file, width, height)
    draw_state(tiles, width, height)
    level1_UCSsolution = level1_UCS(tiles, width, height)
    draw_heatmap_path(tiles, level1_UCSsolution, width, height)

def print_level1_DFS(input_file):
    height = set_height_or_width(input_file, 0)
    width = set_height_or_width(input_file, 1)
    tiles = reset_tiles(input_file, width, height)
    draw_state(tiles, width, height)
    level1_DFSsolution = level1_DFS(tiles, width, height)
    draw_heatmap_path(tiles, level1_DFSsolution, width, height)

def print_level1_Astar(input_file):
    height = set_height_or_width(input_file, 0)
    width = set_height_or_width(input_file, 1)
    tiles = reset_tiles(input_file, width, height)
    draw_state(tiles, width, height)
    level1_Astar_solution = level1_Astar(tiles, width, height)
    draw_heatmap_path(tiles, level1_Astar_solution, width, height)