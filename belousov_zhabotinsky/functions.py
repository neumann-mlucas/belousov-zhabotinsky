import numpy as np
from scipy.signal import convolve2d

from scipy.ndimage import laplace
from scipy.ndimage import gaussian_laplace
from scipy.ndimage.interpolation import rotate


def rotate_grid(grid, symmetry):
    """ Average rotate a given grid """

    rotation = 360 / symmetry
    out = np.mean(
        [
            rotate(grid, rotation * i, reshape=False, mode="wrap",)
            for i in range(symmetry)
        ],
        axis=0,
    )
    return out


def init_grid(size, symmetry):
    """ Initialize three two dimensional grids to represent the spacial
    distribution / concentration of the species A, B and C """

    dim, *shape = size

    # Applies rotate to get a symmetrical grid
    out = []
    for _ in range(dim):
        grid = np.random.random(shape)
        grid = rotate_grid(grid, symmetry)
        out.append(grid)
    out = np.stack(out)

    return out


def variable_coefficients(coefficients, size):
    """ Returns a grid of coeficent values """

    dim, height, width = size

    out = np.zeros(size)
    for i in range(dim):
        out[i] = coefficients[i]

    _, cv, ch = [i // 2 for i in size]

    px = (np.arange(height) - cv) * (2 * np.pi / height)
    py = (np.arange(width) - ch) * (2 * np.pi / width)

    x = px.reshape((height, 1))
    y = py.reshape((1, width))

    out[0] *= 1 + 0.4 * np.cos((x * y))

    return out


def add_perturbation(grid, size):
    """ Add a pertubation in the center of a given grid """

    dim, height, width = size
    cv, ch = [i // 2 for i in (height, width)]
    dv, dh = [i // 20 for i in (height, width)]

    perturbations = [(i + 2) ** -1 for i in range(dim)]

    out = grid * 0.05
    for n, p in enumerate(perturbations):
        out[n, cv - dv : cv + dv, ch - dh : ch + dh] = p

    # Ensure the species concentrations are kept within [0,1]
    np.clip(out, 0, 0.99, out)

    return out


def apply_convolution(grid, size):
    """ Calculates the local average concentration """

    kernel = np.ones((3, 3)) / 9

    out = np.zeros(size)
    for i in range(len(grid)):
        out[i] = convolve2d(grid[i], kernel, mode="same", boundary="wrap")

    return out


def apply_gaussian_laplacian(grid, size, coefficients=(1, 100)):
    """ Calculates the local diffusion """

    dim = size[0]
    out = np.zeros(size)
    for i in range(dim):
        out[i] = coefficients[i] * gaussian_laplace(grid[i], sigma=3, mode="wrap")

    return out


def apply_laplacian(grid, size, coefficients=(1, 100)):
    """ Calculates the local diffusion """

    dim = size[0]
    out = np.zeros(size)
    for i in range(dim):
        out[i] = coefficients[i] * laplace(grid[i], mode="wrap")

    return out


def calc_bz(grid, size, coefficients=(1, 1, 1)):
    """ Apply the Belousov-Zhabotinsky equations to a given grid (three species system) """

    a, b, c = coefficients

    out = np.zeros(size)

    out[0] = grid[0] * (a * grid[1] - c * grid[2])
    out[1] = grid[1] * (b * grid[2] - a * grid[0])
    out[2] = grid[2] * (c * grid[0] - b * grid[1])

    return out


def calc_ch(grid, size, coefficients=(0.5,)):
    """ Apply the Cahn-Hilliard to a given grid"""

    a, *_ = coefficients

    out = np.zeros(size)

    diff = apply_laplacian(grid, size, coefficients=(1,))
    out = grid ** 3 - grid - a * diff

    return out


def calc_fn(grid, size, coefficients=(-0.005, 10)):
    """ Apply the FitzHugh-Nagumo equations to a given grid"""

    a, b, *_ = coefficients

    out = np.zeros(size)

    out[0] = grid[0] - grid[0] ** 3 - grid[1] + a
    out[1] = b * (grid[0] - grid[1])

    return out


def calc_gs(grid, size, coefficients=(0.0374, 0.0584)):
    """ Apply the Gray-Scott equations to a given grid"""

    a, b, *_ = coefficients

    out = np.zeros(size)

    reaction = grid[0] * grid[1] * grid[1]

    out[0] = -reaction + a * (1 - grid[0])
    out[1] = +reaction - (a + b) * grid[1]

    return out


def update_bz(grid, size, coefficients):
    """Propagate the Beloousov-Zhabotinsky reaction equations for a given grid"""

    # Hard coded time step
    DT = 1.0

    # Get average local concentration
    out = apply_convolution(grid, size)
    # Update grid
    out += DT * calc_bz(out, size, coefficients)
    # Ensure the species concentrations are kept within [0,1]
    np.clip(out, 0, 0.99, out)

    return out


def update_bz_laplacian(grid, size, coefficients):
    """Propagate the Beloousov-Zhabotinsky reaction equations for a given grid (DOES NOT WORK)"""

    # Hard coded time step
    DT = 0.01

    # Get average local concentration
    diff = apply_laplacian(grid, size, coefficients=(0.1, 0.1, 0.1))
    dout = calc_bz(grid, size, coefficients)
    # Update grid
    out = grid + DT * (diff + dout)
    # Ensure the species concentrations are kept within [0,1]
    np.clip(out, 0, 0.99, out)

    return out


def update_ch(grid, size, coefficients):
    """Propagate the Cahn-Hiliard equations for a given grid"""

    # Hard coded time step
    DT = 0.05

    # Calculate diffusion and reaction term
    mi = calc_ch(grid, size, coefficients)
    dout = apply_gaussian_laplacian(mi, size, coefficients=(0.5,))
    # Update grid
    out = grid + DT * (dout)
    # Ensure the species concentrations are kept within [-1,1]
    np.clip(out, -0.99, 0.99, out)

    return out


def update_fn(grid, size, coefficients):
    """Propagate the FitzHugh-Nagumo equations for a given grid"""

    # Hard coded time step
    DT = 0.01

    # Calculate diffusion and reaction term
    diff = apply_gaussian_laplacian(grid, size, coefficients=(1, 100))
    dout = calc_fn(grid, size, coefficients)
    # Update grid
    out = grid + DT * (diff + dout)
    # Ensure the species concentrations are kept within [0,1]
    np.clip(out, 0, 0.99, out)

    return out


def update_gs(grid, size, coefficients):
    """Propagate the Gray-Scott equations for a given grid"""

    # Hard coded time step
    DT = 0.05

    # Calculate diffusion and reaction term
    diff = apply_laplacian(grid, size, coefficients=(0.16, 0.08))
    dout = calc_gs(grid, size, coefficients)
    # Update grid
    out = grid + DT * (diff + dout)
    # Ensure the species concentrations are kept within [0,1]
    np.clip(out, 0, 0.99, out)

    return out
