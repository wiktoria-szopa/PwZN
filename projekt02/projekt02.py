import argparse
import numpy as np
import random
from PIL import Image
import os
from tqdm import tqdm


# kazda pare spinow liczyc raz, co robi sie przy duzej becie i malej becie

#
# parser = argparse.ArgumentParser()
# parser.add_argument('n', type=int, help='rozmiar boków siatki')
# parser.add_argument('J', type=float, help='wartość całki wymiany')
# parser.add_argument('beta', type=float, help='parametr związany z temperaturą')
# parser.add_argument('B', type=float, help='wartość pola B')
# # makrokroków, czyli ile razy losujemy tyle spinow ile jest lacznie w siatce, czyli
# # majac np n=2, to 2 kroki to byloby losowanie 8 razybo 4 to calkowita ilosc spinow, a 2*4=8
# parser.add_argument('step_number', type=int, help='liczba kroków symulacji')
# parser.add_argument('rho', type=float, help='początkowa gęstość spinów w górę', default=0.5)
# parser.add_argument('--pictures', '-p', help='nazwa folderu z generowanymi obrazkami')
# parser.add_argument('--animate', '-a', help='nazwa pliku z animacją')
# parser.add_argument('--magnetisation', '-m', help='nazwa pliku z magnetyzacją')
# args = parser.parse_args()

def generate_grid(n, rho):
    return np.random.choice([1, -1], size=(n, n), p=[rho, 1 - rho])


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


def calculate_magnetisation(grid, fileout, n):
    magnetisation = np.sum(grid) / n ** 2
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


def create_animation(image_filenames, output_filename='animation.gif', duration=100, loop=0):
    images = [Image.open(filename) for filename in image_filenames]
    images[0].save(output_filename, save_all=True, append_images=images[1:], duration=duration, loop=loop)


def simulate(n, J, beta, B, step_number, rho, pictures=None, animate=None, magnetisation=None):
    grid = generate_grid(n, rho)
    pictures_tmp = 'pics'
    image_filenames = []
    for macrostep in tqdm(range(step_number)):
        for step in range(n ** 2):
            grid = change_one_spin(n, grid, J, B, beta)
            if magnetisation:
                calculate_magnetisation(grid, magnetisation, n)
            if pictures:
                if not os.path.exists(pictures):
                    os.makedirs(pictures)
                image_filename = f'{pictures}/grid_image{macrostep}_{step}.png'
                grid_to_image(grid, filename=image_filename)
                image_filenames.append(image_filename)

            if animate and not pictures:
                if not os.path.exists(pictures_tmp):
                    os.makedirs(pictures_tmp)
                image_filename = f'pics/grid_image{macrostep}_{step}.png'
                grid_to_image(grid, filename=image_filename)
                image_filenames.append(image_filename)

    if animate and pictures:
        create_animation(image_filenames, output_filename=animate)

    if animate and not pictures:
        create_animation(image_filenames, output_filename=animate)
        for filename in image_filenames:
            os.remove(filename)
        os.rmdir(pictures_tmp)


simulate(20, 1, 0.00000000000000001, 1, 10, 0.5, animate='animation.gif', magnetisation='magnetisation.txt')
