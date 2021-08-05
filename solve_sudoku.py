# A python implementation of algoritm X


import copy
from colorama import Fore, Back, Style

backtracks = 0


def generateBoard(grid):
    """
    Generates a user friendly board in text to save to a file or print to the console.
    """

    text = ""

    for x in range(0, 11):
        if x == 3 or x == 7 or x == 11:
            text += "---------+-----------+----------\n"
        else:
            line = ""
            for y in range(0, 11):
                if y == 3 or y == 7 or y == 11:
                    line += "|  "
                else:

                    y_min = 0
                    x_min = 0

                    if y < 3:
                        y_min = 0
                    elif y < 7:
                        y_min = 1
                    else:
                        y_min = 2

                    if x < 3:
                        x_min = 0
                    elif x < 7:
                        x_min = 1
                    else:
                        x_min = 2

                    line += str(grid[x-x_min][y-y_min]) + "  "
            text += line + "\n"

    return text


def findNextCellToFill(grid):
    """
    Find next empty cell to fill on the Sudoku grid.
    """

    # Look for an unfilled grid location
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y

    return -1, -1

# Check if the setting (i, j) square to e is valid


def isValid(grid, i, j, e):
    """
    Check if e on position i, j is valid
    """

    rowOk = all([e != grid[i][x] for x in range(0, 9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(0, 9)])
        if columnOk:
            # Finding top-left x, y co-ordinates of section that contains i, j
            secTopX, secTopY = 3 * (i//3), 3 * (j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if grid[x][y] == e:
                        return False

            return True

    return False


def solveSudoku(grid, i=0, j=0):
    """
    Fills in the missing squares by brute-forcing the sudoku.
    """

    global backtracks

    # Find next grid cell to fill
    i, j = findNextCellToFill(grid)

    if i == -1:
        return True

    for e in range(1, 10):
        # Try different values in i, j position
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j) != False:
                return grid

            backtracks += 1

            grid[i][j] = 0

    return False


def getBoard():
    """
    Get the sudoku from the in.txt file.
    """

    with open("in.txt", "r") as f:
        grid = []
        lines = f.readlines()
        for line in lines:
            row = []
            for x in range(0, 9):
                row.append(int(line[x*2]))
            grid.append(row)

    return grid


# Start the program
if __name__ == "__main__":
    print(
        f"[ {Fore.YELLOW}0{Style.RESET_ALL} ] Getting sudoku from in.txt.", end="\r")
    orig_grid = getBoard()
    print(f"[ {Fore.GREEN}1{Style.RESET_ALL} ]")
    print(f"[ {Fore.YELLOW}0{Style.RESET_ALL} ] Solving Sudoku.", end="\r")
    grid = solveSudoku(copy.deepcopy(orig_grid))

    with open("out.txt", "w") as f:
        if grid != False:
            print(f"[ {Fore.GREEN}1{Style.RESET_ALL} ]")
            print("Successfully solved the sudoku, output is in out.txt!")
            f.write("\nOriginal:\n")
            f.write(generateBoard(orig_grid))

            f.write("\n\nSolved:\n")
            f.write(generateBoard(grid))

            f.write("\nBacktracks: {}\n".format(backtracks))
        else:
            print(f"[ {Fore.RED}x{Style.RESET_ALL} ]")
            print("Could not solve this sudoku!")
            f.write("Could not solve sudoku!")
