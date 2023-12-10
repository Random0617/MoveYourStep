import pygame
import time
import level1
import level2

def main():
    '''
    # START OF HEATMAP EXAMPLE
    input_file = "input1-level2.txt"
    height = level1.set_height_or_width(input_file, 0)
    width = level1.set_height_or_width(input_file, 1)
    tiles = level1.reset_tiles(input_file, width, height)
    level1.draw_state(tiles, width, height)
    # Path: coordinates of the cells gone traveled through (not including starting cell), in the correct order
    example_path = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10], [2, 10], [3, 10],
                    [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], [10, 10], [11, 10], [12, 10], [12, 9],
                    [12, 8], [12, 7], [11, 7], [10, 7], [9, 7], [9, 8], [9, 9], [9, 10], [8, 10], [7, 10], [6, 10],
                    [6, 11], [6, 12], [6, 13], [7, 13], [8, 13], [9, 13], [9, 12], [9, 11], [9, 10], [8, 10], [7, 10],
                    [6, 10], [5, 10], [5, 9], [5, 8], [5, 7], [5, 6], [6, 6], [7, 6], [8, 6], [9, 6], [9, 7], [9, 8],
                    [9, 9], [9, 10], [8, 10], [7, 10], [6, 10], [5, 10], [5, 11]]
    # Call level1.draw_heatmap_path to color the solution path (in the same form as example_path)
    # The instructor requires that the path be shown step-by-step with different colors for cells visited multiple times
    level1.draw_heatmap_path(tiles, example_path, width, height)
    time.sleep(2)
    # END OF HEATMAP EXAMPLE (please comment out this block of code when you start testing level 2)
    '''
    input_files = ["input1-level1.txt", "input2-level1.txt", "input3-level1.txt",
                   "input4-level1.txt", "input5-level1.txt"]
    for i in range(len(input_files)):
        input_file = input_files[i]
        level1.print_level1_BFS(input_file)
        time.sleep(3)
        level1.print_level1_UCS(input_file)
        time.sleep(3)
        level1.print_level1_DFS(input_file)
        time.sleep(3)
    input_files = ["input1-level2.txt", "input2-level2.txt", "input3-level2.txt",
                   "input4-level2.txt", "input5-level2.txt", "input6-level2.txt"]
    for i in range(len(input_files)):
        input_file = input_files[i]
        level2.print_level2_BFS(input_file)
        time.sleep(3)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


main()
