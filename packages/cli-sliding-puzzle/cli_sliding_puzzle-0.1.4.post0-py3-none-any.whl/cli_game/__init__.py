from .game import main
from ._version import __version__

def run_game():
    import curses
    return curses.wrapper(main)
