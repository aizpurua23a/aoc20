
class MemGame:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.starting_numbers = [int(num) for num in file.read().split(',')]
        self.num_dict = {}
        for index in range(len(self.starting_numbers)-1):
            self.num_dict[self.starting_numbers[index]] = index

    def play(self, limit):
        last_number = self.starting_numbers[-1]
        for i in range(len(self.starting_numbers), limit):
            if self.num_dict.get(last_number) is None:
                number = 0
            else:
                number = i - self.num_dict[last_number] - 1
            self.num_dict[last_number] = i - 1
            last_number = number
        return last_number


if __name__ == '__main__':
    mg = MemGame('test_input.txt')
    print(mg.play(2020))
    mg = MemGame('test_input.txt')
    print(mg.play(30000000))
