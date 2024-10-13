import curses
import random
import sys

# Initialize the puzzle
def init_puzzle(size):
    numbers = list(range(1, size*size)) + [0]
    random.shuffle(numbers)
    return [numbers[i:i+size] for i in range(0, len(numbers), size)]

# Draw the puzzle on the screen
def draw_puzzle(stdscr, puzzle, size):
    for i in range(size):
        for j in range(size):
            if puzzle[i][j] == 0:
                stdscr.addstr(i*2, j*4, "    ")
            else:
                stdscr.addstr(i*2, j*4, f" {puzzle[i][j]:2d} ")
    stdscr.addstr(size*2 + 1, 0, "Use arrow keys to move tiles. Press 'q' to quit.")
    stdscr.refresh()

# Find the position of the empty tile
def find_empty(puzzle):
    return next((i, j) for i, row in enumerate(puzzle) for j, val in enumerate(row) if val == 0)

# Check if the puzzle is solved
def is_solved(puzzle):
    flattened = [num for row in puzzle for num in row]
    return flattened == list(range(1, len(flattened))) + [0]

# Get the grid size from the user
def get_size_input(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter grid size (3-6), or press Enter for default (4): ")
    stdscr.refresh()
    curses.echo()
    size = 4
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            return None
        elif key == ord('\n'):
            break
        elif 51 <= key <= 54:
            size = key - 48
            break
    curses.noecho()
    return size

# Celebrate the win
def celebrate_win(stdscr, size):
    stdscr.clear()
    stdscr.addstr(size + 2, 0, "Congratulations! You solved the puzzle!")
    stdscr.refresh()
    stdscr.getch()

# Main game function
def main(stdscr):
    curses.curs_set(0)
    
    size = get_size_input(stdscr)
    if size is None:
        return

    puzzle = init_puzzle(size)
    
    while True:
        stdscr.clear()
        draw_puzzle(stdscr, puzzle, size)
        
        if is_solved(puzzle):
            celebrate_win(stdscr, size)
            break
        
        key = stdscr.getch()
        if key == ord('q'):
            break
        
        y, x = find_empty(puzzle)
        if key == curses.KEY_UP and y < size - 1:
            puzzle[y][x], puzzle[y+1][x] = puzzle[y+1][x], puzzle[y][x]
        elif key == curses.KEY_DOWN and y > 0:
            puzzle[y][x], puzzle[y-1][x] = puzzle[y-1][x], puzzle[y][x]
        elif key == curses.KEY_LEFT and x < size - 1:
            puzzle[y][x], puzzle[y][x+1] = puzzle[y][x+1], puzzle[y][x]
        elif key == curses.KEY_RIGHT and x > 0:
            puzzle[y][x], puzzle[y][x-1] = puzzle[y][x-1], puzzle[y][x]

# Make sure main is defined at the module level
if __name__ == "__main__":
    curses.wrapper(main)
