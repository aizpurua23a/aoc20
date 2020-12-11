from pprint import pprint
from copy import deepcopy
from collections import Counter


class Seats:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.seats = [[character for character in row] for row in file.read().splitlines()]

    def is_seat_occupied(self, i, j, inc_i, inc_j, option):
        if inc_i == inc_j == 0:
            return False
        x = i + inc_i
        y = j + inc_j
        while 0 <= x <= len(self.seats)-1 and 0 <= y <= len(self.seats[0])-1:
            # option 1
            if option == 1:
                return self.seats[x][y] == '#'

            # option 2
            if self.seats[x][y] == '#':
                return True
            if self.seats[x][y] == 'L':
                return False
            x += inc_i
            y += inc_j
        return False

    def calculate_next_step(self, option):
        new_state = deepcopy(self.seats)
        for row_index, row in enumerate(self.seats):
            for column_index, seat in enumerate(row):
                occupied_count = 0
                for increment_row in [-1, 0, 1]:
                    for increment_col in [-1, 0, 1]:
                        occupied_count += self.is_seat_occupied(row_index, column_index, increment_row, increment_col, option)
                if occupied_count == 0 and seat == 'L':
                    new_state[row_index][column_index] = '#'
                if occupied_count >= 3 + option and seat == '#':
                    new_state[row_index][column_index] = 'L'

        changed = new_state != self.seats
        return changed, new_state

    def iterate_until_stable(self, option):
        changed = True
        while changed:
            changed, self.seats = self.calculate_next_step(option)
        return self.seats


if __name__ == '__main__':
    s1 = Seats('input.txt')
    s2 = Seats('input.txt')
    pprint(sum([Counter(row)['#'] for row in s1.iterate_until_stable(1)]))
    pprint(sum([Counter(row)['#'] for row in s2.iterate_until_stable(2)]))
