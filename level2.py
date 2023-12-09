import time

import level1

def customized_level1_BFS(tiles, width, height, starting_row, starting_col, finishing_row, finishing_col):
    height_limit = height
    width_limit = width

    class BFS_Tile:
        def __init__(self, row, col, type, value, expanded, added_to_queue, distance, prev_cell):
            self.row = row
            self.col = col
            self.type = type  # int: 0, 1, -2, 3
            self.value = value
            self.expanded = expanded  # bool
            self.added_to_queue = added_to_queue  # bool
            self.distance = distance  # int
            self.prev_cell = prev_cell  # two-element array showing coordinates

    BFS_tiles = []
    for i in range(height):
        row = []
        for k in range(width):
            BFStile = BFS_Tile(i, k, tiles[i][k].type, tiles[i][k].value, False, False, 999999, [-1, -1])
            row.append(BFStile)
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
        if (level1.tile_available(BFS_tiles, top_left[0], top_left[1], height_limit, width_limit)
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

        if (level1.tile_available(BFS_tiles, top_right[0], top_right[1], height_limit, width_limit)
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

        if (level1.tile_available(BFS_tiles, bottom_left[0], bottom_left[1], height_limit, width_limit)
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

        if (level1.tile_available(BFS_tiles, bottom_right[0], bottom_right[1], height_limit, width_limit)
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

        if (level1.tile_available(BFS_tiles, top_middle[0], top_middle[1], height_limit, width_limit)
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

        if (level1.tile_available(BFS_tiles, middle_right[0], middle_right[1], height_limit, width_limit)
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

        if (level1.tile_available(BFS_tiles, bottom_middle[0], bottom_middle[1], height_limit, width_limit)
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

        if (level1.tile_available(BFS_tiles, middle_left[0], middle_left[1], height_limit, width_limit)
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


def get_starting_cell(tiles, width, height):
    starting_row = -1
    starting_col = -1
    for i in range(height):
        for k in range(width):
            if tiles[i][k].type == 0:
                starting_row = i
                starting_col = k
    cell = [starting_row, starting_col]
    return cell


def simplified_BFS(tiles, width, height):
    height_limit = height
    width_limit = width

    class BFS_tile_simplified:
        def __init__(self, row, col, type, value, expanded, added_to_queue):
            self.row = row
            self.col = col
            self.type = type  # int: -2, -1, 0, 1, 2, 3
            self.value = value
            self.expanded = expanded  # bool
            self.added_to_queue = added_to_queue  # bool

    class Key:
        def __init__(self, row, col, type, value):
            self.row = row
            self.col = col
            self.type = type  # 2 (key) or 3 (finish)
            self.value = value

    BFS_simplified_tiles = []
    starting_row = -1
    starting_col = -1
    finishing_row = -1
    finishing_col = -1
    for i in range(height):
        row = []
        for k in range(width):
            BFStile = BFS_tile_simplified(i, k, tiles[i][k].type, tiles[i][k].value, False, False)
            row.append(BFStile)
            if tiles[i][k].type == 0:
                starting_row = i
                starting_col = k
            if tiles[i][k].type == 3:
                finishing_row = i
                finishing_col = k
        BFS_simplified_tiles.append(row)
    print(str(starting_row) + " " + str(starting_col))
    print(str(finishing_row) + " " + str(finishing_col))
    priority_queue = []
    collected_keys = []
    priority_queue.append(BFS_simplified_tiles[starting_row][starting_col])
    BFS_simplified_tiles[starting_row][starting_col].added_to_queue = True
    while len(priority_queue) > 0:
        visiting_cell = priority_queue[0]
        cur_x = visiting_cell.row
        cur_y = visiting_cell.col
        BFS_simplified_tiles[cur_x][cur_y].expanded = True
        print("Set BFS_simplified_tiles[" + str(cur_x) + "][" + str(cur_y) + "] = True")
        if BFS_simplified_tiles[cur_x][cur_y].type in [2, 3]:
            key = Key(cur_x, cur_y, BFS_simplified_tiles[cur_x][cur_y].type, BFS_simplified_tiles[cur_x][cur_y].value)
            collected_keys.append(key)
        priority_queue.pop(0)
        print("Start adding neighbors for " + str(cur_x) + ", " + str(cur_y))
        top_left = [cur_x - 1, cur_y - 1]
        top_middle = [cur_x - 1, cur_y]
        top_right = [cur_x - 1, cur_y + 1]
        middle_left = [cur_x, cur_y - 1]
        middle_right = [cur_x, cur_y + 1]
        bottom_left = [cur_x + 1, cur_y - 1]
        bottom_middle = [cur_x + 1, cur_y]
        bottom_right = [cur_x + 1, cur_y + 1]
        if (level1.tile_available(BFS_simplified_tiles, top_left[0], top_left[1], height_limit, width_limit)
                and BFS_simplified_tiles[top_left[0]][top_left[1]].expanded == False
                and BFS_simplified_tiles[top_middle[0]][top_middle[1]].type in [0, 1, 2, 3]
                and BFS_simplified_tiles[middle_left[0]][middle_left[1]].type in [0, 1, 2, 3]):
            if not BFS_simplified_tiles[top_left[0]][top_left[1]].added_to_queue:
                priority_queue.append(BFS_simplified_tiles[top_left[0]][top_left[1]])
                BFS_simplified_tiles[top_left[0]][top_left[1]].added_to_queue = True

        if (level1.tile_available(BFS_simplified_tiles, top_right[0], top_right[1], height_limit, width_limit)
                and BFS_simplified_tiles[top_right[0]][top_right[1]].expanded == False
                and BFS_simplified_tiles[top_middle[0]][top_middle[1]].type in [0, 1, 2, 3]
                and BFS_simplified_tiles[middle_right[0]][middle_right[1]].type in [0, 1, 2, 3]):
            if not BFS_simplified_tiles[top_right[0]][top_right[1]].added_to_queue:
                priority_queue.append(BFS_simplified_tiles[top_right[0]][top_right[1]])
                BFS_simplified_tiles[top_right[0]][top_right[1]].added_to_queue = True

        if (level1.tile_available(BFS_simplified_tiles, bottom_left[0], bottom_left[1], height_limit, width_limit)
                and BFS_simplified_tiles[bottom_left[0]][bottom_left[1]].expanded == False
                and BFS_simplified_tiles[bottom_middle[0]][bottom_middle[1]].type in [0, 1, 2, 3]
                and BFS_simplified_tiles[middle_left[0]][middle_left[1]].type in [0, 1, 2, 3]):
            if not BFS_simplified_tiles[bottom_left[0]][bottom_left[1]].added_to_queue:
                priority_queue.append(BFS_simplified_tiles[bottom_left[0]][bottom_left[1]])
                BFS_simplified_tiles[bottom_left[0]][bottom_left[1]].added_to_queue = True

        if (level1.tile_available(BFS_simplified_tiles, bottom_right[0], bottom_right[1], height_limit, width_limit)
                and BFS_simplified_tiles[bottom_right[0]][bottom_right[1]].expanded == False
                and BFS_simplified_tiles[bottom_middle[0]][bottom_middle[1]].type in [0, 1, 2, 3]
                and BFS_simplified_tiles[middle_right[0]][middle_right[1]].type in [0, 1, 2, 3]):
            if not BFS_simplified_tiles[bottom_right[0]][bottom_right[1]].added_to_queue:
                priority_queue.append(BFS_simplified_tiles[bottom_right[0]][bottom_right[1]])
                BFS_simplified_tiles[bottom_right[0]][bottom_right[1]].added_to_queue = True

        if (level1.tile_available(BFS_simplified_tiles, top_middle[0], top_middle[1], height_limit, width_limit)
                and BFS_simplified_tiles[top_middle[0]][top_middle[1]].expanded == False):
            if not BFS_simplified_tiles[top_middle[0]][top_middle[1]].added_to_queue:
                priority_queue.append(BFS_simplified_tiles[top_middle[0]][top_middle[1]])
                BFS_simplified_tiles[top_middle[0]][top_middle[1]].added_to_queue = True

        if (level1.tile_available(BFS_simplified_tiles, middle_right[0], middle_right[1], height_limit, width_limit)
                and BFS_simplified_tiles[middle_right[0]][middle_right[1]].expanded == False):
            if not BFS_simplified_tiles[middle_right[0]][middle_right[1]].added_to_queue:
                priority_queue.append(BFS_simplified_tiles[middle_right[0]][middle_right[1]])
                BFS_simplified_tiles[middle_right[0]][middle_right[1]].added_to_queue = True

        if (level1.tile_available(BFS_simplified_tiles, bottom_middle[0], bottom_middle[1], height_limit, width_limit)
                and BFS_simplified_tiles[bottom_middle[0]][bottom_middle[1]].expanded == False):
            if not BFS_simplified_tiles[bottom_middle[0]][bottom_middle[1]].added_to_queue:
                priority_queue.append(BFS_simplified_tiles[bottom_middle[0]][bottom_middle[1]])
                BFS_simplified_tiles[bottom_middle[0]][bottom_middle[1]].added_to_queue = True

        if (level1.tile_available(BFS_simplified_tiles, middle_left[0], middle_left[1], height_limit, width_limit)
                and BFS_simplified_tiles[middle_left[0]][middle_left[1]].expanded == False):
            if not BFS_simplified_tiles[middle_left[0]][middle_left[1]].added_to_queue:
                priority_queue.append(BFS_simplified_tiles[middle_left[0]][middle_left[1]])
                BFS_simplified_tiles[middle_left[0]][middle_left[1]].added_to_queue = True
    print("Finishing row: " + str(finishing_row))
    print("Finishing col: " + str(finishing_col))
    print("Finishing cell has been expanded: " + str(BFS_simplified_tiles[finishing_row][finishing_col].expanded))
    for i in range(height):
        str_result = ""
        for k in range(width):
            if BFS_simplified_tiles[i][k].expanded:
                str_result += "_ "
            else:
                str_result += "X "
        print(str_result)
    return collected_keys


def found_finish(keys):
    for i in range(len(keys)):
        if keys[i].value == 0:
            return True
    return False


def print_level2_BFS(input_file):
    height = level1.set_height_or_width(input_file, 0)
    width = level1.set_height_or_width(input_file, 1)
    tiles = level1.reset_tiles(input_file, width, height)
    keys = simplified_BFS(tiles, width, height)
    stacked_keys = []
    found_key_solution = False
    if found_finish(keys):
        found_key_solution = not found_key_solution
        for i in range(len(keys)):
            stacked_keys.append(keys[i])
    while len(keys) > 0 and not found_finish(keys):
        keys = simplified_BFS(tiles, width, height)
        key_string = "Keys collected this round:"
        for i in range(len(keys)):
            stacked_keys.append(keys[i])
            tiles = level1.unlock_door(tiles, width, height, keys[i].value)
            key_string = key_string + " " + str(keys[i].value)
        print(key_string)
        stacked_key_string = "All keys collected:"
        for i in range(len(stacked_keys)):
            stacked_key_string = stacked_key_string + " " + str(stacked_keys[i].value)
        print(stacked_key_string)
        if found_finish(keys):
            found_key_solution = not found_key_solution
    if found_key_solution:
        print("A solution exists.")
        while stacked_keys[len(stacked_keys) - 1].value != 0:
            stacked_keys.pop()
        tiles = level1.reset_tiles(input_file, width, height)
        checkpoints = [get_starting_cell(tiles, width, height)]
        for i in range(len(stacked_keys)):
            checkpoints.append([stacked_keys[i].row, stacked_keys[i].col, stacked_keys[i].value])
        print("Checkpoints: " + str(checkpoints))
        random_solution = []
        for i in range(len(checkpoints) - 1):
            if i == 0:
                tiles = level1.reset_tiles(input_file, width, height)
            else:
                tiles = level1.unlock_door(tiles, width, height, checkpoints[i][2])
            path = customized_level1_BFS(tiles, width, height, checkpoints[i][0], checkpoints[i][1],
                                         checkpoints[i + 1][0], checkpoints[i + 1][1])
            print(checkpoints[0], checkpoints[1])
            print("Path: " + str(path))
            for k in range(len(path)):
                random_solution.append(path[k])
        tiles = level1.reset_tiles(input_file, width, height)
        level1.draw_state(tiles, width, height)
        time.sleep(0.2)
        level1.draw_heatmap_path(tiles, random_solution, width, height)
    else:
        print("No solution was found.")
        tiles = level1.reset_tiles(input_file, width, height)
        random_solution = []
        level1.draw_heatmap_path(tiles, random_solution, width, height)