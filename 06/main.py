from pprint import pprint


class AnswerCounter():
    def __init__(self, filename='input.txt'):
        with open(filename, 'r') as file:
            self.data = [group for group in file.read().split('\n\n')]
        self.union_set_list = [set(group.replace('\n', '')) for group in self.data]
        self.intersection_set_list = []
        for group in self.data:
            split_group = group.split('\n')
            answers_intersection = set(split_group[0])
            [answers_intersection.intersection_update(set(member)) for member in split_group]
            self.intersection_set_list.append(answers_intersection)

    def get_sum_of_union_lens(self):
        return sum(len(group) for group in self.union_set_list)

    def get_sum_of_intersection_lens(self):
        return sum(len(group) for group in self.intersection_set_list)


if __name__ == '__main__':
    ac = AnswerCounter("input.txt")
    pprint(ac.get_sum_of_union_lens())
    pprint(ac.get_sum_of_intersection_lens())
