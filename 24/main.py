import numpy as np

class HexTiling:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.read().splitlines()

        self.moves_list = [self.str_to_moves_list(line) for line in data]
        pass

    def flip_all_list(self):
        flipped = []
        for move in self.moves_list:
            x = sum(i for i, _ in move)
            y = sum(j for _, j in move)
            if (x, y) in flipped:
                flipped.remove((x, y))
            else:
                flipped.append((x, y))

        return flipped

    def game_of_hex_life(self, moves):
        board = np.zeros((60, 60), int)
        initial_flipped_tiles = self.flip_all_list()

        for move in initial_flipped_tiles:
            board[30+move[0]][30+move[1]] = 1

        move = 0
        while move < moves:
            board = self.update_board_with_conway_hex_rules(board)
            board = self.expand_board_if_needed(board)

            if (move+1) % 10 == 0:
                print(np.sum(board))
            move += 1

        return board

    @staticmethod
    def expand_board_if_needed(board):
        one_in_edges = False
        if 1 in board[0] or 1 in board[-1]:
            one_in_edges = True
        if 1 in [x[0] for x in board] or 1 in [x[-1] for x in board]:
            one_in_edges = True

        if not one_in_edges:
            return board

        board = np.pad(board, ((2, 2), (2, 2)), mode='constant', constant_values=0)
        return board


    @classmethod
    def update_board_with_conway_hex_rules(cls, board):
        new_board = board.copy()
        for row_index, row in enumerate(board):
            for col_index, elem in enumerate(row):
                flipped_neighbors = cls.count_flipped_neighbors(row_index, col_index, board)
                if elem == 1 and flipped_neighbors not in (1, 2):
                    new_board[row_index][col_index] = 0
                elif elem == 0 and flipped_neighbors == 2:
                    new_board[row_index][col_index] = 1

        return new_board

    @staticmethod
    def count_flipped_neighbors(row_index, col_index, board):
        count = 0
        if row_index == 19:
            a = 1

        if row_index < len(board)-1:
            count += board[row_index + 1][col_index]
            if col_index > 0:
                count += board[row_index + 1][col_index - 1]

        if row_index > 0:
            count += board[row_index - 1][col_index]
            if col_index < len(board[0])-1:
                count += board[row_index - 1][col_index + 1]

        if col_index > 0:
            count += board[row_index][col_index - 1]

        if col_index < len(board[0])-1:
            count += board[row_index][col_index+1]

        # +1 +1 and -1 -1 are NOT neighbors in this hexgrid

        return count

    @staticmethod
    def str_to_moves_list(moves_str):
        moves_list = []
        index = 0
        while index < len(moves_str):
            if moves_str[index:index+2] == 'ne':
                moves_list.append((0, 1))
                index += 2

            elif moves_str[index] == 'e':
                moves_list.append((1, 0))
                index += 1

            elif moves_str[index:index + 2] == 'se':
                moves_list.append((1, -1))
                index += 2

            elif moves_str[index:index + 2] == 'sw':
                moves_list.append((0, -1))
                index += 2

            elif moves_str[index] == 'w':
                moves_list.append((-1, 0))
                index += 1

            elif moves_str[index:index + 2] == 'nw':
                moves_list.append((-1, 1))
                index += 2

        return moves_list


if __name__ == '__main__':
    ht = HexTiling('input.txt')
    ht.game_of_hex_life(100)
