import numpy as np
import random
from PIL import Image
import os
from tqdm import tqdm
import shutil


class Ising:
    def __init__(self, n, J, beta, B, step_number, rho, pictures=None, animate=None, magnetisation=None):
        self.n = n
        self.J = J
        self.beta = beta
        self.B = B
        self.step_number = step_number
        self.rho = rho
        self.pictures = pictures
        self.animate = animate
        self.magnetisation = magnetisation
        self.grid = self.generate_grid()
        self.pictures_tmp = 'pics'
        self.image_filenames = []

    def generate_grid(self):
        return np.random.choice([1, -1], size=(self.n, self.n), p=[self.rho, 1 - self.rho])

    def calculate_hamiltonian(self):
        H = 0
        rows, cols = self.grid.shape
        for i in range(rows):
            for j in range(cols):
                s_ij = self.grid[i, j]

                s_right = self.grid[i, (j + 1) % cols]
                s_down = self.grid[(i + 1) % rows, j]
                s_left = self.grid[i, (j - 1) % cols]
                s_up = self.grid[(i - 1) % rows, j]

                H -= self.J * s_ij * (s_right + s_down + s_left + s_up)
        H = H / 2
        H -= self.B * np.sum(self.grid)
        return H

    def change_one_spin(self):
        E0 = self.calculate_hamiltonian()

        i = random.randint(0, self.n - 1)
        j = random.randint(0, self.n - 1)
        self.grid[i, j] = -self.grid[i, j]

        E1 = self.calculate_hamiltonian()
        dE = E1 - E0
        if dE < 0:
            return self.grid
        elif random.random() < np.exp(-self.beta * dE):
            return self.grid

        self.grid[i, j] = -self.grid[i, j]
        return self.grid

    def calculate_magnetisation(self):
        magnetisation = np.sum(self.grid) / self.n ** 2
        with open(self.magnetisation, 'a') as f:
            f.write(f'{magnetisation}\n')

    def grid_to_image(self, filename, cell_size=10):
        n, m = self.grid.shape
        image = Image.new('RGB', (m * cell_size, n * cell_size), color='white')
        pixels = image.load()

        for i in range(n):
            for j in range(m):
                color = (0, 0, 0) if self.grid[i, j] == -1 else (255, 255, 255)
                for x in range(cell_size):
                    for y in range(cell_size):
                        pixels[j * cell_size + x, i * cell_size + y] = color

        image.save(filename)

    def create_animation(self, duration=500, loop=0):
        images = [Image.open(filename) for filename in self.image_filenames]
        images[0].save(self.animate, save_all=True, append_images=images[1:], duration=duration, loop=loop)

    def simulate(self):
        grid = self.generate_grid()
        pictures_tmp = 'pics'
        for macrostep in tqdm(range(self.step_number)):
            for step in range(self.n ** 2):
                grid = self.change_one_spin()
                if self.magnetisation:
                    self.calculate_magnetisation()
            if self.pictures:
                if not os.path.exists(self.pictures):
                    os.makedirs(self.pictures)
                image_filename = f'{self.pictures}/grid_image{macrostep}.png'
                self.grid_to_image(filename=image_filename)
                self.image_filenames.append(image_filename)

            if self.animate and not self.pictures:
                if not os.path.exists(pictures_tmp):
                    os.makedirs(pictures_tmp)
                image_filename = f'pics/grid_image{macrostep}.png'
                self.grid_to_image(filename=image_filename)
                self.image_filenames.append(image_filename)

        if self.animate and self.pictures:
            self.create_animation()

        if self.animate and not self.pictures:
            self.create_animation()
            for filename in self.image_filenames:
                os.remove(filename)
            shutil.rmtree(pictures_tmp)

# optymalniej liczyc energie oraz robic animacje co makro, a nie mikro krok
