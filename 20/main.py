import numpy as np


class PuzzleSolver:
    def __init__(self, filename):
        with open(filename) as file:
            tiles = file.read().split('\n\n')

        self.tiles = {}
        for tile in tiles:
            rows = tile.split('\n')
            id = int(rows[0].split(' ')[1][:-1])
            edges = [  # east, north, west, south
                ''.join([x[-1] for x in rows[1:]]),
                rows[1],
                ''.join([x[0] for x in rows[1:]]),
                rows[-1],
            ]
            self.tiles[id] = {
                "tile": rows[1:],
                "edges": edges
            }

    def find_corner_tiles(self):
        corner_tiles = []

        for id, tile in self.tiles.items():
            matched_edges = 0
            for edge in tile.get('edges'):
                if self.does_edge_match_other_tiles(id, edge):
                    matched_edges += 1

            if matched_edges == 2:
                corner_tiles.append(id)

        return corner_tiles

    def does_edge_match_other_tiles(self, origin_id, edge):
        for id, tile in self.tiles.items():
            if id == origin_id:
                continue

            for candidate_edge in tile.get('edges'):
                if edge == candidate_edge or edge == candidate_edge[::-1]:
                    return True
        return False

    def build_image(self):
        n = len(self.tiles)
        side = int(np.sqrt(n))

        id, flipped, rotated = self.find_first_corner()


        #find image size
        #find corner
        #fill first row

        #fill subsequent rows

    def find_first_corner(self):

        matched_edges = [False] * 4
        first_corner_id = None
        for id, tile in self.tiles.items():
            matched_edges = [False] * 4
            for index, edge in enumerate(tile.get('edges')):
                if self.does_edge_match_other_tiles(id, edge):
                    matched_edges[index] = True

            if sum(matched_edges) == 2:
                first_corner_id = id
                break

        edges = self.tiles[first_corner_id]

        if matched_edges == [False, True, True, False]:
            rotated = 0
        if matched_edges == [True, True, False, False]:
            rotated = 1
        if matched_edges == [True, False, False, True]:
            rotated = 2
        if matched_edges == [False, False, True, True]:
            rotated = 3

        return first_corner_id, False, rotated

    @staticmethod
    def rotate_tile(tile, amount):
        new_tile = {}
        for i in range(amount):
            new_tile['tile'] = list(zip(*tile['tile'][::-1]))[::-1]
            tile = new_tile

        return tile



if __name__ == '__main__':
    ps = PuzzleSolver('test_input.txt')
    print(np.prod(list(int(n) for n in ps.find_corner_tiles())))

    ps = PuzzleSolver('input.txt')
    print(np.prod(list(int(n) for n in ps.find_corner_tiles())))
