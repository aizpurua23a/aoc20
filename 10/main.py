from numpy import prod
from itertools import product


class Jolter:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.data = list(map(int, file.read().splitlines()))
        self.data = [0] + self.data + [max(self.data) + 3]
        self.data.sort()

        self.sub_arrays = self.three_jolt_splitter(self.data)
        self.sub_array_max_length = max([len(array) for array in self.sub_arrays])

        self.valid_converter_combinations = {
            1: 1,
            2: 1,
        }
        for array_length in range(3, self.sub_array_max_length + 1):
            self.valid_converter_combinations[array_length] = \
                self.get_valid_combinations_in_array_of_length(array_length)

        # Generated Manually
            # self.valid_converter_combinations = {
            # 1: 1,
            # 2: 1,
            # 3: 2,
            # 4: 4,
            # 5: 7  # given 5 consecutive elements, we cannot remove the middle 3 at the same time.
        # }

    @staticmethod
    def get_valid_combinations_in_array_of_length(n):
        prods = list(''.join(element) for element in product('01', repeat=n-2))
        valid_combinations = len(prods)
        if n-2 >= 3:
            for element in prods:
                if '000' in element:  # No three consecutive elements can be removed at the same time.
                    valid_combinations -= 1

        return valid_combinations

    @staticmethod
    def three_jolt_splitter(data):
        sub_arrays = []
        first_index = 0
        for index in range(0, len(data) - 1):
            if data[index + 1] - data[index] == 3:
                sub_arrays.append(data[first_index:index+1].copy())
                first_index = index + 1
        sub_arrays.append([data[-1]])
        return sub_arrays

    def day_10_1(self):
        one_jolt_difs = 0
        three_jolt_difs = 1
        for index in range(0, len(self.data) - 1):
            if self.data[index + 1] - self.data[index] == 1:
                one_jolt_difs += 1
            if self.data[index + 1] - self.data[index] == 3:
                three_jolt_difs += 1

        return one_jolt_difs * three_jolt_difs

    def day_10_2(self):
        return prod([self.valid_converter_combinations[len(array)] for array in self.sub_arrays])


if __name__ == '__main__':
    j = Jolter('input.txt')
    print(j.day_10_1())
    print(j.day_10_2())
