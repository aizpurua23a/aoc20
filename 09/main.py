
class PreambleNumbers:
    def __init__(self, filename, preamble_length):
        with open(filename, 'r') as file:
            self.number_list = list(int(number) for number in file.read().split('\n'))

        self.preamble_length = preamble_length

    def find_first_violation(self):
        for index, number in enumerate(self.number_list):
            if index >= self.preamble_length:
                if not self.is_number_sum_of_two_elements_in_list(number, self.number_list[(index-self.preamble_length):index]):
                    return index, number

    def is_number_sum_of_two_elements_in_list(self, number, list):
        for element in list:
            if number-element in list:
                return True
        return False

    def find_set_that_adds_to_number_in_list(self, number, num_list):
        # we discard adding 2 numbers because that's the definition of the target number
        len_set = 3
        len_list = len(num_list)
        while len_set <= len_list:
            index = 0
            while index <= len_list-len_set:
                if sum(num_list[index:index + len_set]) == number:
                    return num_list[index:index + len_set]
                index += 1
            len_set += 1
        return []


if __name__ == '__main__':
    pn = PreambleNumbers("input.txt", 25)
    index, number = pn.find_first_violation()
    print(index, number)
    num_list = pn.find_set_that_adds_to_number_in_list(number, pn.number_list[:index])
    print(num_list)
    print(min(num_list) + max(num_list))