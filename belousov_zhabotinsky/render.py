#!/usr/bin/python

import curses
import argparse

from .functions import *


def parse_args():

    COEFFICIENTS = (1.0, 1.0, 1.0)
    COLORS = np.random.choice(6, 10) + 1  # valid range is 1-7
    ASCIIS = list(map(lambda x: " .:?!@~¨*&+"[x], np.random.choice(10, 10)))

    # ASCIIS = (" ", ".", " ", ":", "*", "*", "#", "#", "@", "@")
    # COLORS = (1, 1, 2, 2, 2, 3, 3, 3, 7, 1)

    # COLORS = (1, 2, 3, 4, 1, 2, 3, 4, 1, 2)
    # ASCIIS = list(map(str, range(10)))

    parser = argparse.ArgumentParser(
        prog="belousov-zhabotinsky",
        description="""The python package you never knew you needed! Now you
        can appreciate all the glory of the Belousov-Zhabotinsky reaction from
        the comfort of your console window with a state of the art ASCII art
        rendering. Your life will never be the same!""",
        epilog="""You can exit
        the program by pressing any key, but using the Ctrl key can cause the
        terminal to bug. For bug report or more information:
        https://github.com/neumann-mlucas/belousov-zhabotinsky""",
    )
    parser.add_argument(
        "-a",
        "--asciis",
        action="store",
        default=ASCIIS,
        nargs=10,
        help="""10 ASCII characters to be use in the rendering. Each point in
        the screen has a value between 0 and 1, and each ASCII character used
        as an input represents a range of values (e.g. 0.0-0.1, 0.1-0.2 etc)""",
    )
    parser.add_argument(
        "-b",
        "--background",
        action="store",
        default=0,
        type=int,
        help="""Background color [int 0-7]. 0:black, 1:red, 2:green, 3:yellow,
        4:blue, 5:magenta, 6:cyan, and 7:white""",
    )
    parser.add_argument(
        "-c",
        "--colors",
        action="store",
        default=COLORS,
        nargs=10,
        type=int,
        help="""10 numbers in the [0-7] range for mapping colors to the ASCII
        characters. 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta,
        6:cyan, and 7:white""",
    )
    parser.add_argument(
        "-coef",
        "--coefficients",
        action="store",
        default=COEFFICIENTS,
        nargs=3,
        type=float,
        help="""Values for alpha, beta and gamma -- changes the reaction's
        behavior. Default is alpha=1.0, beta=1.0, gamma=1.0""",
    )
    parser.add_argument(
        "-s",
        "--symmetry",
        action="store",
        default=1,
        type=int,
        help="""Symmetric mode, generates a n-fold symmetric grid""",
    )
    parser.add_argument(
        "-ch",
        "--cahn-hillard",
        action="store_true",
        default=False,
        help="""Use the Cahn-Hillard equations""",
    )
    parser.add_argument(
        "-gs",
        "--gray-scott",
        action="store_true",
        default=False,
        help="""Use the Gray-Scott equations""",
    )
    parser.add_argument(
        "-p",
        "--add-perturbation",
        action="store_true",
        default=False,
        help="""Add a perturbation to the uncial grid""",
    )
    parser.add_argument(
        "-fn",
        "--fitzhugh-nagumo",
        action="store_true",
        default=False,
        help="""Use the FitzHugh-Nagumo equations (Turing patterns)""",
    )
    parser.add_argument(
        "-vc",
        "--variable-coefficients",
        action="store_true",
        default=False,
        help="""Make coefficients variable within the grid [TESTING]""",
    )
    args = parser.parse_args()

    # I NEED TO THINK IN A BETTER WAY OF DOING THIS
    if args.fitzhugh_nagumo:
        args.update_grid = update_fn
        args.dim = 2
        args.step_size = 10
        if args.coefficients == COEFFICIENTS:
            args.coefficients = (-0.005, 10)
    elif args.cahn_hillard:
        args.update_grid = update_ch
        args.dim = 1
        args.step_size = 50
        if args.coefficients == COEFFICIENTS:
            args.coefficients = (0.05,)
    elif args.gray_scott:
        args.update_grid = update_gs
        args.dim = 2
        args.step_size = 50
        args.add_perturbation = True
        if args.coefficients == COEFFICIENTS:
            args.coefficients = (0.0374, 0.0584)
    else:
        args.update_grid = update_bz
        args.dim = 3
        args.step_size = 1

    args.coefficients = args.coefficients[: args.dim]

    return args


def init_screen(args):
    """ Set ncurses screen and returns the screen object """

    screen = curses.initscr()
    curses.curs_set(0)

    curses.start_color()
    curses.init_pair(1, 1, args.background)
    curses.init_pair(2, 2, args.background)
    curses.init_pair(3, 3, args.background)
    curses.init_pair(4, 4, args.background)
    curses.init_pair(5, 5, args.background)
    curses.init_pair(6, 6, args.background)
    curses.init_pair(7, 7, args.background)

    screen.clear()

    return screen


def render(args):
    """ Initializes grid then update and render it ad infinitum """

    # Local variables are faster than objects attributes
    asciis = args.asciis
    colors = args.colors
    coefficients = args.coefficients
    step_size = args.step_size
    update_grid = args.update_grid

    # Initialize screen and grid
    screen = init_screen(args)
    height, width = screen.getmaxyx()
    size = (args.dim, height, width)
    grid = init_grid(size, args.symmetry)

    if args.variable_coefficients:
        coefficients = variable_coefficients(coefficients, size)
    if args.add_perturbation:
        grid = add_perturbation(grid, size)

    # Error on addstr(height, width)
    grid_idxs = [(i, j) for i in range(height) for j in range(width)]
    grid_idxs.pop()

    while True:

        # Update grid (some equations are 'slower' than others)
        for _ in range(step_size):
            grid = update_grid(grid, size, coefficients)

        # Update screen
        for line, column in grid_idxs:

            # Array values are floats, indexes are ints
            idx = int(grid[0, line, column] * 10)

            # Get current char and calculate new char
            now_char = screen.inch(line, column) | curses.A_CHARTEXT
            new_char = asciis[idx]

            # Update only if char has changed
            if now_char != new_char:
                new_color = curses.color_pair(colors[idx]) | curses.A_BOLD
                screen.addstr(
                    line, column, new_char, new_color,
                )
            else:
                continue

        screen.refresh()
        screen.timeout(25)

        # Ends rendering
        if screen.getch() != -1:
            curses.endwin()
            break


def main():
    args = parse_args()
    render(args)


if __name__ == "__main__":
    main()
