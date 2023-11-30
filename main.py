from Tile import Tile

height = 0
width = 0

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

'''
a = "K321"
b = "K415"
print((int)(a[1:]) + (int)(b[1:]))
'''