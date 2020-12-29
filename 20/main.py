import numpy as np
import regex as re
from copy import deepcopy
from pprint import pprint


class PuzzleSolver:
    def __init__(self, filename):
        with open(filename) as file:
            tiles = file.read().split('\n\n')

        self.tiles = {}
        for tile in tiles:
            rows = tile.split('\n')
            id = int(rows[0].split(' ')[1][:-1])
            edges = [  # east, north, west, south
                ''.join([x[-1] for x in rows[:-len(rows):-1]]),
                rows[1][::-1],
                ''.join([x[0] for x in rows[1:]]),
                rows[-1],
            ]
            self.tiles[id] = {
                "tile": rows[1:],
                "edges": edges
            }

        self.side = int(np.sqrt(len(self.tiles)))

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


    # All of this yanked from: https://github.com/zedrdave/advent_of_code/blob/master/2020/10/__main__.py

    @classmethod
    def get_match(cls, pieces, origin_tile, side):
        for tile in pieces:
            if tile in cls.transform(origin_tile):
                continue
            for transformed_tile in cls.transform(tile):
                if cls.edge(transformed_tile, (side + 2) % 4) == cls.edge(origin_tile, side):
                    return transformed_tile
        return 0

    @staticmethod
    def transform(p):
        for _ in range(4):
            yield p
            yield '\n'.join(l[::-1] for l in p.split('\n'))  # flip
            p = '\n'.join(''.join(l[::-1]) for l in zip(*p.split('\n')))

    @staticmethod
    def edge(p, i):
        return [p[:10],
                p[9::11],
                p[-10:],
                p[0::11]][i]

    def build_image(self):
        tiles = {}
        for key, value in self.tiles.items():
            self.tiles[key]['tile'] = '\n'.join(value['tile'])
            tiles[key] = self.tiles[key]['tile']

        tiles_list = tiles.values()

        corners = []
        for id, tile in tiles.items():
            unmatched_edges = 0
            for i in range(4):
                unmatched_edges += not self.get_match(tiles_list, tile, i)
            if unmatched_edges == 2:
                corners.append(id)

        corner_tile_id = corners[0]

        corner_tile = next(p for p in self.transform(tiles[corner_tile_id]) if (self.get_match(tiles_list, p, 2) and
                                                                                self.get_match(tiles_list, p, 3)))

        first_line = self.get_line(tiles_list, corner_tile, 2)

        image = []
        for tile in first_line:
            image.append(self.get_line(tiles_list, tile, 3))

        image = '\n'.join(''.join(item[i + 1:i + 9] for item in row[::-1]) for row in image for i in range(11, 99, 11))

        print(image)

        # awesome regex way of finding the monster

        spacing = '[.#\n]{77}'
        monster = f'#.{spacing+"#....#"*3}##{spacing}.#{"..#"*5}'

        for image_t in self.transform(image):
            m = len(re.findall(monster, image_t, overlapped=True))
            if m:
                print('Part2: ', sum(c == '#' for c in image_t) - 15*m)
                break

        ##################################################################

        print("\nVisualisation:")

        ##################################################################


        monster = '(.)#(.(?:.|\n){77})#(....)##(....)##(....)###((?:.|\n){77}.)#(..)#(..)#(..)#(..)#(..)#'
        show_monster = r'\1🐸\2🟢\3🟢🟢\4🟢🟢\5🟢🟢🟢\6🟢\7🟢\8🟢\9🟢\10🟢\11🟢'

        showing_monsters = re.sub(monster, show_monster, re.sub(monster, show_monster, image_t))
        print(showing_monsters.replace('.', '🟦').replace('#', '🟦'))
        print('Num #:', sum(c == '#' for c in showing_monsters))

    def get_line(self, pieces, p, orient):
        R = [p]
        for _ in range(self.side-1):
            R += [self.get_match(pieces, R[-1], orient)]
        return R


if __name__ == '__main__':
    ps = PuzzleSolver('input.txt')
    print(ps.build_image())

    #ps = PuzzleSolver('input.txt')
    #print(np.prod(list(int(n) for n in ps.find_corner_tiles())))
