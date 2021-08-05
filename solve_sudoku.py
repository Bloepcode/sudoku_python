# A python implementation of algoritm X


import copy
from colorama import Fore, Back, Style

backtracks = 0


def generate_board(grid):
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


def find_next_cell_to_fill(grid):
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


def is_valid(grid, i, j, e):
    """
    Check if e on position i, j is valid
    """

    row_ok = all([e != grid[i][x] for x in range(0, 9)])
    if row_ok:
        column_ok = all([e != grid[x][j] for x in range(0, 9)])
        if column_ok:
            # Finding top-left x, y co-ordinates of section that contains i, j
            sec_top_x, sec_top_y = 3 * (i//3), 3 * (j//3)
            for x in range(sec_top_x, sec_top_x+3):
                for y in range(sec_top_y, sec_top_y+3):
                    if grid[x][y] == e:
                        return False

            return True

    return False


def solve_sudoku(grid, i=0, j=0):
    """
    Fills in the missing squares by brute-forcing the sudoku.
    """

    global backtracks

    # Find next grid cell to fill
    i, j = find_next_cell_to_fill(grid)

    if i == -1:
        return True

    for e in range(1, 10):
        # Try different values in i, j position
        if is_valid(grid, i, j, e):
            grid[i][j] = e
            if solve_sudoku(grid, i, j) != False:
                return grid

            backtracks += 1

            grid[i][j] = 0

    return False


def get_board():
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
    orig_grid = get_board()
    print(f"[ {Fore.GREEN}1{Style.RESET_ALL} ]")
    print(f"[ {Fore.YELLOW}0{Style.RESET_ALL} ] Solving Sudoku.", end="\r")
    grid = solve_sudoku(copy.deepcopy(orig_grid))

    with open("out.txt", "w") as f:
        if grid != False:
            print(f"[ {Fore.GREEN}1{Style.RESET_ALL} ]")
            print("Successfully solved the sudoku, output is in out.txt!")
            f.write("\nOriginal:\n")
            f.write(generate_board(orig_grid))

            f.write("\n\nSolved:\n")
            f.write(generate_board(grid))

            f.write("\nBacktracks: {}\n".format(backtracks))
        else:
            print(f"[ {Fore.RED}x{Style.RESET_ALL} ]")
            print("Could not solve this sudoku!")
            f.write("Could not solve sudoku!")
