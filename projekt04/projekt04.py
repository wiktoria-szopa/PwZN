import argparse
import numpy as np
import random
from PIL import Image
import os
from tqdm import tqdm
import numba
import time

@numba.njit
def generate_grid(n, rho):
    grid = np.empty((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(n):
            grid[i, j] = 1 if random.random() < rho else -1
    return grid

@numba.njit
def calculate_hamiltonian(grid, J, B):
    H = 0
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            s_ij = grid[i, j]

            s_right = grid[i, (j + 1) % cols]
            s_down = grid[(i + 1) % rows, j]
            s_left = grid[i, (j - 1) % cols]
            s_up = grid[(i - 1) % rows, j]

            H -= J * s_ij * (s_right + s_down + s_left + s_up)
    H = H / 2
    H -= B * np.sum(grid)
    return H

@numba.njit
def change_one_spin(n, grid, J, B, beta):
    E0 = calculate_hamiltonian(grid, J, B)

    i = random.randint(0, n - 1)
    j = random.randint(0, n - 1)
    grid[i, j] = -grid[i, j]

    E1 = calculate_hamiltonian(grid, J, B)
    dE = E1 - E0
    if dE < 0:
        return grid
    elif random.random() < np.exp(-beta * dE):
        return grid

    grid[i, j] = -grid[i, j]
    return grid

@numba.njit
def calculate_magnetisation(grid, n):
    return np.sum(grid) / n ** 2

def write_magnetisation(magnetisation, fileout):
    with open(fileout, 'a') as f:
        f.write(f'{magnetisation}\n')

def grid_to_image(grid, cell_size=10, filename='grid_image.png'):
    n, m = grid.shape
    image = Image.new('RGB', (m * cell_size, n * cell_size), color='white')
    pixels = image.load()

    for i in range(n):
        for j in range(m):
            color = (0, 0, 0) if grid[i, j] == -1 else (255, 255, 255)
            for x in range(cell_size):
                for y in range(cell_size):
                    pixels[j * cell_size + x, i * cell_size + y] = color

    image.save(filename)

def create_animation(image_filenames, output_filename='animation.gif', duration=500, loop=0):
    images = [Image.open(filename) for filename in image_filenames]
    images[0].save(output_filename, save_all=True, append_images=images[1:], duration=duration, loop=loop)

def simulate(n, J, beta, B, step_number, rho, pictures=None, animate=None, magnetisation=None):
    grid = generate_grid(n, rho)
    pictures_tmp = 'pics'
    image_filenames = []
    s = time.time()
    for macrostep in tqdm(range(step_number)):
        for step in range(n ** 2):
            grid = change_one_spin(n, grid, J, B, beta)
            if magnetisation:
                mag = calculate_magnetisation(grid, n)
                write_magnetisation(mag, magnetisation)
        if pictures:
            if not os.path.exists(pictures):
                os.makedirs(pictures)
            image_filename = f'{pictures}/grid_image{macrostep}.png'
            grid_to_image(grid, filename=image_filename)
            image_filenames.append(image_filename)

        if animate and not pictures:
            if not os.path.exists(pictures_tmp):
                os.makedirs(pictures_tmp)
            image_filename = f'pics/grid_image{macrostep}.png'
            grid_to_image(grid, filename=image_filename)
            image_filenames.append(image_filename)

    if animate and pictures:
        create_animation(image_filenames, output_filename=animate)

    if animate and not pictures:
        create_animation(image_filenames, output_filename=animate)
        for filename in image_filenames:
            os.remove(filename)
        os.rmdir(pictures_tmp)
    print('czas petli: ',time.time()-s)

start_time = time.time()
simulate(20, 1, 1, 1, 4, 0.5, animate='animation.gif', magnetisation='magnetisation.txt')
end_time = time.time()

print(f'Czas wykonania: {end_time - start_time} s')
# bez numby ~8s
# z numba ~5s, gdyby było więcej kroków to różnica byłaby większa, sama petla jest giga szybka

# czas petli z numba 2.7s, bez to te okolo 7s, w tym projekcie jeszcze sie chyba wczytuje wszystko itp




