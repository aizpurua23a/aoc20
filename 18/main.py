
class OperationNode:
    def __init__(self, left_str_list=None, operator='', right_str_list=None, result=None):
        self.left = None
        self.operator = ''
        self.right = None
        self.result = None

        if result is not None:
            self.result = result
            return

        self.populate_children_from_lists(left_str_list, operator, right_str_list)
        self.update_result()

    def update_result(self):
        if self.result:
            return

        if self.operator == '+':
            self.result = self.left.result + self.right.result
        elif self.operator == '*':
            self.result = self.left.result * self.right.result

    def populate_children_from_lists(self, left_list, operator, right_list):
        self.populate_child_from_list(which='left', str_list=left_list)
        self.operator = operator
        self.populate_child_from_list(which='right', str_list=right_list)

    def populate_child_from_list(self, which, str_list):
        str_list = self.remove_redundant_parentheses_if_needed(str_list)

        if len(str_list) == 1:
            self.create_simple_node(which, int(str_list[0]))
            return

        left, operator, right = self.get_left_operator_and_right_from_str_list(str_list)

        node = self.make_node_from_left_operator_right(left, operator, right)
        if which == 'left':
            self.left = node
        if which == 'right':
            self.right = node

    def remove_redundant_parentheses_if_needed(self, str_list):
        if str_list[-1] != ')':
            return str_list

        p_start = self.find_matching_parentheses_backwards(-1, str_list)
        if p_start == -len(str_list):
            return str_list[1:-1]
        return str_list

    def create_simple_node(self, which, value):
        if which == "left":
            self.left = self.make_node_from_result(result=value)
        elif which == "right":
            self.right = self.make_node_from_result(result=value)

    def operate(self):
        if self.result is not None:
            return self.result

        if isinstance(self.left, int):
            left = self.left
        if isinstance(self.left, self.__class__):
            left = self.left.operate()

        if isinstance(self.right, int):
            right = self.right
        if isinstance(self.right, self.__class__):
            right = self.right.operate()

        if self.operator == '+':
            return left + right
        elif self.operator == '*':
            return left * right

    @classmethod
    def get_left_operator_and_right_from_str_list(cls, str_list):
        index, right_element_list = cls.handle_right_element(str_list)
        operator = str_list[index]
        left_element_list = cls.handle_left_element(index, str_list)
        return left_element_list, operator, right_element_list

    @classmethod
    def handle_right_element(cls, str_list):
        index = -1
        if str_list[index] == ')':
            p_start = cls.find_matching_parentheses_backwards(index, str_list)
            right_list = str_list[p_start + 1:index]
            index = p_start - 1
        else:
            right_list = [str_list[index]]
            index -= 1

        return index, right_list

    @staticmethod
    def handle_left_element(index, str_list):
        return str_list[:index]

    @staticmethod
    def find_matching_parentheses_backwards(index, str_list):
        parentheses_depth_count = 0
        for i in range(index-1, -len(str_list)-1, -1):
            if str_list[i] == ')':
                parentheses_depth_count += 1
            if str_list[i] == '(':
                parentheses_depth_count += -1
            if parentheses_depth_count == -1:
                return i
        raise ValueError('Parenthesis does not end.')

    @staticmethod
    def make_node_from_result(result):
        return OperationNode(result=result)

    @staticmethod
    def make_node_from_left_operator_right(left, operator,right):
        return OperationNode(left_str_list=left, operator=operator, right_str_list=right)


class OperationNodeSum(OperationNode):
    @classmethod
    def handle_right_element(cls, str_list):
        index = -1

        if str_list[index] == ')':
            p_start = cls.find_matching_parentheses_backwards(index, str_list)
            p_start = cls.find_less_prevalent_operator(p_start, str_list)

            right_list = str_list[p_start+1:]
            index = p_start

        else:
            p_start = cls.find_less_prevalent_operator(index, str_list)
            right_list = str_list[p_start+1:]
            index = p_start

        return index, right_list

    @classmethod
    def find_less_prevalent_operator(cls, index, str_list):
        last_valid_mul = cls.get_last_occurrence_of_operator_at_surface_level('*', str_list[:index])
        last_valid_sum = cls.get_last_occurrence_of_operator_at_surface_level('+', str_list[:index])
        if last_valid_mul is not None:
            return index + last_valid_mul
        if last_valid_sum is not None:
            return index + last_valid_sum
        return index

    @staticmethod
    def get_last_occurrence_of_operator_at_surface_level(operator, str_list):
        depth = 0
        for index, element in enumerate(str_list[::-1]):
            if element == ')':
                depth += 1
            if element == '(':
                depth -= 1

            if depth == 0 and element == operator:
                return -1 - index
        return None

    @staticmethod
    def make_node_from_result(result):
        return OperationNodeSum(result=result)

    @staticmethod
    def make_node_from_left_operator_right(left, operator, right):
        return OperationNodeSum(left_str_list=left, operator=operator, right_str_list=right)


class MathHomework:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.read().splitlines()
        self.roots = []

        for line in data:
            op_list = [element for element in line if element != ' ']
            left, operator, right = self.get_left_operator_right_from_str_list([op for op in op_list])
            self.roots.append(self.make_operator_node(left, operator, right))

    def get_left_operator_right(self, op_list):
        return OperationNode.get_left_operator_and_right_from_str_list([op for op in op_list])

    def make_operator_node(self, left, operator, right):
        return OperationNode(left, operator, right)

    @staticmethod
    def get_left_operator_right_from_str_list(str_list):
        return OperationNode.get_left_operator_and_right_from_str_list(str_list)

    def operate(self):
        return sum(node.result for node in self.roots)


class MathHomeworkAdv(MathHomework):

    @staticmethod
    def get_left_operator_right_from_str_list(str_list):
        return OperationNodeSum.get_left_operator_and_right_from_str_list(str_list)

    def get_left_operator_right(self, op_list):
        return OperationNodeSum.get_left_operator_and_right_from_str_list([op for op in op_list])

    def make_operator_node(self, left, operator, right):
        return OperationNodeSum(left, operator, right)


if __name__ == '__main__':
    #mht = MathHomework('test_input.txt')
    #print(mht.operate())
    #mh = MathHomework('input.txt')
    #print(mh.operate())

    mhat = MathHomeworkAdv('debug.txt')
    print(mhat.operate())
    mha = MathHomeworkAdv('input.txt')
    print(mha.operate())
