

class TreeFinder(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.data = file.read().split('\n')

        self.lane_depth = len(self.data)
        self.lane_width = len(self.data[0])

    def ex_03_1(self):
        print(self.get_tree_count_given_side_and_down(3, 1))

    def ex_03_2(self):
        inputs = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        results = [self.get_tree_count_given_side_and_down(side, down) for (side, down) in inputs]
        prod = 1
        for result in results:
            prod *= result

        print(prod)

    def get_tree_count_given_side_and_down(self, side_increment, down_increment):
        tree_count = 0
        side_position = side_increment
        depth = down_increment
        while depth < self.lane_depth:
            tree_count += 1 if self.data[depth][side_position] == "#" else 0

            depth += down_increment
            side_position += side_increment

            if side_position >= self.lane_width:
                side_position -= self.lane_width
        print('Side: {}, Down: {}, Trees {}'.format(side_increment, down_increment, tree_count))

        return tree_count


if __name__ == '__main__':
    tf = TreeFinder('input.txt')
    tf.ex_03_1()
    tf.ex_03_2()
