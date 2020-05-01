#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation

from .functions import *
from .render import parse_args


def update_im(grid):

    im = ax.imshow(grid[0], animated=True)

    return [im]


def gen_ims(grid, steps=1000):

    # faster
    step_size = args.step_size
    size = args.size
    coefficients = args.coefficients

    ims = []
    for frame in range(steps):
        for _ in range(step_size):
            grid = args.update_grid(grid, size, coefficients)
        im = update_im(grid)
        ims.append(im)

    return ims


if __name__ == "__main__":

    SIZE = 256
    args = parse_args()
    args.size = (args.dim, SIZE, SIZE)

    # Initialize screen and grid
    grid = init_grid(args.size, args.symmetry)
    if args.variable_coefficients:
        coefficients = variable_coefficients(args.coefficients, args.size)
    if args.add_perturbation:
        grid = add_perturbation(grid, args.size)

    fig, ax = plt.subplots()

    ax.set_xticks(ticks=[])
    ax.set_yticks(ticks=[])

    ims = gen_ims(grid, steps=100)
    animated = ArtistAnimation(fig, ims, interval=10, blit=True)

    plt.show()
