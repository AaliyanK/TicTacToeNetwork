import os
import pygame


letterx = pygame.image.load(os.path.join('x.png'))
lettero = pygame.image.load(os.path.join('o.png'))


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 200), (600, 200)),  # first horizontal line
                           ((0, 400), (600, 400)),  # second horizontal line
                           ((200, 0), (200, 600)),  # first vertical line
                           ((400, 0), (400, 600))]  # second vertical line

        # creating a 2D 3 by 3 range with list comprehension
        # outputs a list representing the three rows of the grid
        self.grid = [[0 for x in range(3)]
                     for y in range(3)]  # x and y come from here
        # boolean used to switch the players, wont change the matrix we've created.
        self.switch_player = True

        # searching the direction to identify when a row/col is complete
        #                      N      NW      W      SW    S    SE      E     NE
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0),
                            (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False  # to close the game once someone wins

    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)
            # surface is defined in tic.py, its the place where we draw
            # next is the color
            # the starting is line[0] - (0,200) to 600,200
            # ending is line[1] for the second horizontal line
            # 2 is the thickness
        for y in range(len(self.grid)):  # goes all 3 lists that are output
            # goes through the innerlist - all the elements
            for x in range(len(self.grid[y])):
                # if you read an element with an X then display the X pic (blit)
                if self.get_cell_value(x, y) == 'X':
                    surface.blit(letterx, (x*200, y*200))
                elif self.get_cell_value(x, y) == 'O':
                    surface.blit(lettero, (x*200, y*200))

    def get_cell_value(self, x, y):
        # reads the grid thats produced in the "output" and uses it to do actions
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        # to prevent overwriting the x/o on the table
        if self.get_cell_value(x, y) == 0:
            self.set_cell_value(x, y, player)
            self.check_grid(x, y, player)

    def is_within_bounds(self, x, y):  # to avoid a list error
        # returns a boolean if all the conditions are true/false
        return x >= 0 and x < 3 and y >= 0 and y < 3

    def check_grid(self, x, y, player):  # crazy algorithm, hard to explain LOL
        count = 1
        # returns the tuples (0,1) ... (dirx,diry)
        for index, (dirx, diry) in enumerate(self.search_dirs):
            if self.is_within_bounds(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                count += 1
                xx = x+dirx
                yy = y+diry
                if self.is_within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    if count == 3:
                        break
                if count < 3:  # what this is doing is that its checking all the values around the input value, if there is a possible "x" in any direction, it will evaluate to true, proving that a possible three-in a row is possible
                    new_dir = 0  # algorithm basically searches for 3 in a row
                    if index == 0:
                        new_dir = self.search_dirs[4]  # N to S
                    elif index == 1:
                        new_dir = self.search_dirs[5]  # NW to SE
                    elif index == 2:
                        new_dir = self.search_dirs[6]  # W TO E
                    elif index == 3:
                        # SW TO NE #checks diagonals!!
                        new_dir = self.search_dirs[7]
                    elif index == 4:
                        new_dir = self.search_dirs[0]  # S TO N
                    elif index == 5:
                        new_dir = self.search_dirs[1]  # SE TO NW
                    elif index == 6:
                        new_dir = self.search_dirs[2]  # E TO W
                    elif index == 7:
                        new_dir = self.search_dirs[3]  # NE TO SW

                    if self.is_within_bounds(x+new_dir[0], y+new_dir[1])\
                            and self.get_cell_value(x+new_dir[0], y+new_dir[1]) == player:
                        count += 1
                        if count == 3:  # THE COUNT IS COUNTING THE NUMBER OF SUCCESSIVE THREE IN A ROW VALUES
                            break
                    else:
                        count = 1
        if count == 3:  # we have a full row/col
            print(player, 'wins!')
            self.game_over = True  # to end game
        else:
            self.game_over = self.is_grid_full()  # a false or true will return

    def is_grid_full(self):
        for row in self.grid:
            for value in row:
                if value == 0:  # means that we still have a free cell
                    return False
        return True

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                # resets the board to 0, all cells will be 0
                self.set_cell_value(x, y, 0)

    def print_grid(self):
        for row in self.grid:
            print(row)
