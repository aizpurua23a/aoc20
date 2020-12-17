from copy import deepcopy
from time import time
import numpy as np



class Conway3D:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.read().splitlines()
        input_size = len(data[0])
        self.iterations = 6
        dim = input_size + self.iterations * 2

        self.initial_state = np.zeros((dim, dim, 1 + self.iterations * 2), dtype=bool)
        offset = self.iterations

        for x, row in enumerate(data):
            for y, cube in enumerate(row):
                if cube == '.':
                    self.initial_state[offset + x][offset + y][self.iterations + 1] = False
                    continue
                self.initial_state[offset + x][offset + y][self.iterations + 1] = True

    def evolve(self):
        old_state = self.initial_state.copy()
        for i in range(self.iterations):
            offset = self.iterations - i - 1
            new_state = deepcopy(old_state)

            from_index = max(0, offset)
            to_index = min(len(new_state), len(new_state)-offset+1)
            for x in range(from_index, to_index):

                to_index = min(len(new_state[x]), len(new_state[x]) - offset + 1)
                for y in range(from_index, to_index):

                    to_index = min(len(new_state[x][y]), len(new_state[x][y]) - offset + 1)
                    for z in range(from_index, to_index):

                        neighbors = self.count_neighbors((x, y, z), old_state)
                        if old_state[x][y][z]:
                            if neighbors not in (2, 3):
                                new_state[x][y][z] = 0
                                continue
                        if neighbors == 3:
                            new_state[x][y][z] = 1
            old_state = new_state
        return np.sum(new_state)

    def count_neighbors(self, coords, state):
        x, y, z = coords
        neighbors = 0
        loop_counter = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                for k in range(z-1, z+2):
                    loop_counter += 1
                    if i < 0 or i >= len(state):
                        continue
                    if j < 0 or j >= len(state[0]):
                        continue
                    if k < 0 or k >= len(state[0][0]):
                        continue
                    if i == x and j == y and k == z:
                        continue

                    neighbors += state[i][j][k]

        return neighbors


class Conway4D:
    def __init__(self, filename, iterations):
        with open(filename, 'r') as file:
            data = file.read().splitlines()
        input_size = len(data[0])
        self.iterations = iterations

        dim_1 = input_size + self.iterations * 2
        dim_2 = 1 + self.iterations * 2

        self.initial_state = np.zeros((dim_1, dim_1, dim_2, dim_2), dtype=bool)
        offset = self.iterations
        for x, row in enumerate(data):
            for y, cube in enumerate(row):
                if cube == '.':
                    self.initial_state[offset + x][offset + y][self.iterations][self.iterations] = False
                    continue
                self.initial_state[offset + x][offset + y][self.iterations][self.iterations] = True

    def evolve(self):
        old_state = self.initial_state.copy()
        t0 = 0
        for i in range(self.iterations):
            t0 = time()
            print('Iteration {} of {}'.format(i+1, self.iterations))

            new_state = deepcopy(old_state)
            offset = self.iterations - i - 1
            from_index = max(offset, 0)
            to_index = min(len(new_state), len(new_state) - offset + 1)
            for x in range(from_index, to_index):

                to_index = min(len(new_state[x]), len(new_state[x]) - offset + 1)
                for y in range(from_index, to_index):

                    to_index = min(len(new_state[x][y]), len(new_state[x][y]) - offset + 1)
                    for z in range(from_index, to_index):

                        to_index = min(len(new_state[x][y][z]), len(new_state[x][y][z]) - offset + 1)
                        for w in range(from_index, to_index):
                            neighbors = self.count_neighbors((x, y, z, w), old_state)

                            if old_state[x][y][z][w]:
                                if neighbors not in (2, 3):
                                    new_state[x][y][z][w] = False
                                    continue

                            if neighbors == 3:
                                new_state[x][y][z][w] = True

            old_state = new_state
            if t0:
                print('Done in {:0.2f} seconds.'.format(time() - t0))
        return np.sum(new_state)

    def count_neighbors(self, coords, state):
        x, y, z, w = coords
        neighbors = 0
        loop_counter = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                for k in range(z-1, z+2):
                    for m in range(w-1, w+2):
                        loop_counter += 1
                        if i < 0 or i >= len(state):
                            continue
                        if j < 0 or j >= len(state[0]):
                            continue
                        if k < 0 or k >= len(state[0][0]):
                            continue
                        if m < 0 or m >= len(state[0][0][0]):
                            continue
                        if i == x and j == y and k == z and m == w:
                            continue
                        neighbors += state[i][j][k][m]
        return neighbors


if __name__ == '__main__':
    #c3 = Conway3D('input.txt')
    #print(c3.evolve())
    c4 = Conway4D('input.txt', 6)
    print(c4.evolve())
