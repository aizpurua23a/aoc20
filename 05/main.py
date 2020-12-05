from pprint import pprint


class SeatFinder(object):
    def __init__(self, file):
        self.example_seats = [
            "FBFBBFFRLR",
            "BFFFBBFRRR",
            "FFFBBBFRRR",
            "BBFFBBFRLL"
        ]

        with open(file, 'r') as file:
            self.seats = file.read().split('\n')

        self.seat_ids = [self.get_int_from_seat_str(seat) for seat in self.seats]
        self.seat_ids.sort()

    def get_highest_id_of_seat_list(self):
        return max(self.get_id_of_seat(seat) for seat in self.seats)

    def get_id_of_seat(self, seat):
        row, column = self.get_row_and_column_of_seat(seat)
        return row * 8 + column

    def get_row_and_column_of_seat(self, seat):
        row = self.get_row_from_seat_7_chars(seat[:7])
        column = self.get_column_from_seat_3_chars(seat[-3:])
        return row, column

    def get_row_from_seat_7_chars(self, seat_row_str):
        sum = 0
        for index, char in enumerate(seat_row_str):
            power = len(seat_row_str) - index - 1
            charnum = 1 if char == "B" else 0
            sum += charnum * pow(2, power)
        return sum

    def get_column_from_seat_3_chars(self, seat_col_str):
        sum = 0
        for index, char in enumerate(seat_col_str):
            power = len(seat_col_str) - index - 1
            charnum = 1 if char == "R" else 0
            sum += charnum * pow(2, power)
        return sum

    def get_int_from_seat_str(self, seat_str):
        sum = 0
        for index, char in enumerate(seat_str):
            power = len(seat_str) - index - 1
            charnum = 0
            if char == "R" or char == "B":
                charnum = 1
            sum += charnum * pow(2, power)
        return sum

    def find_missing_id(self):

        potential_ids = []
        for index, id in enumerate(self.seat_ids):
            if index == 0:
                continue
            if id != self.seat_ids[index-1] + 1:
                potential_ids.append(id-1)

        return potential_ids


if __name__ == '__main__':
    sf = SeatFinder('input.txt')
    pprint(sf.seat_ids)
    pprint(sf.find_missing_id())
