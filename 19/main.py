class RuleNode:
    def __init__(self, index, rule_dict):
        self.length = None
        self.character = None
        self.sub_rules = []

        rule = rule_dict[index]
        if isinstance(rule[0], str):
            self.character = rule[0]
            self.length = len(rule)
            return

        self.sub_rules = self.get_rules_from_rule_and_list(rule, rule_dict)
        self.fill_lengths()

    def fill_lengths(self):
        self.length = self.fill_lengths_from_children()

    def does_string_fulfill_rule(self, message):
        return self.does_string_fulfill_simple_rule(message)

    @staticmethod
    def get_rules_from_rule_and_list(rule, rule_dict):
        sub_rules = []
        for and_list_index, and_list in enumerate(rule):  # ONE of these lists must be fulfilled
            and_rules = []
            for list_index, rule_index in enumerate(and_list):
                and_rules.append(RuleNode(rule_index, rule_dict))
            sub_rules.append(and_rules)

        return sub_rules

    def fill_lengths_from_children(self):
        if self.length:
            return self.length
        lengths_of_or_sub_rules = [sum(and_sub_rule.length for and_sub_rule in or_sub_rule)
                                   for or_sub_rule in self.sub_rules]
        if not all(length == lengths_of_or_sub_rules[0] for length in lengths_of_or_sub_rules):
            raise ValueError('Not all lengths are equal; this is weird.')
        return lengths_of_or_sub_rules[0]

    def does_string_fulfill_simple_rule(self, message):
        if self.character:
            return self.character == message
        if len(message) != self.length:
            return False
        for or_rule in self.sub_rules:
            index = 0
            all_and_rules = True
            for and_rule in or_rule:
                if not and_rule.does_string_fulfill_rule(message[index:index+and_rule.length]):
                    all_and_rules = False
                    break
                index = index + and_rule.length
            if all_and_rules:
                return True
        return False


class RuleNodeRecurssion(RuleNode):  # Pending integrating with super
    def __init__(self, index, rule_dict):
        self.length = None
        self.character = None
        self.sub_rules = []
        self.special_rule = None

        if index == 0:
            self.special_rule = 0
            self.sub_rules = self.get_rules_from_rule_and_list([[42, 31]], rule_dict)
            self.fill_lengths()
            return

        super().__init__(index, rule_dict)

    def fill_lengths(self):
        if self.special_rule == 0:  # In special rules, the length attribute acts as the factor by which the length must
            self.length = self.sub_rules[0][0].length
            return
        self.length = self.fill_lengths_from_children()

    def does_string_fulfill_rule(self, message):
        if self.special_rule == 0:
            return self.check_rule_0(message)
        return self.does_string_fulfill_simple_rule(message)

    def check_rule_0(self, message):
        node_rule_42 = self.sub_rules[0][0]
        node_rule_31 = self.sub_rules[0][1]
        if not len(message) % self.length == 0:
            return False

        if len(message) % (self.length * 2):
            n = (len(message) // self.length) // 2
        else:
            n = (len(message) // self.length - 1) // 2

        for i in range(1, n + 1):
            cut_off_index = - node_rule_31.length * i
            msg1 = message[:cut_off_index]
            msg2 = message[cut_off_index:]

            m = self.length
            msg_list_42 = [msg1[j:j + m] for j in range(0, len(msg1), m)]
            msg_list_31 = [msg2[j:j + m] for j in range(0, len(msg2), m)]

            if (all(node_rule_42.does_string_fulfill_rule(msg) for msg in msg_list_42) and
                    all(node_rule_31.does_string_fulfill_rule(msg) for msg in msg_list_31)):
                return True
        return False


class MessageValidator:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            rules_str, messages = file.read().split('\n\n')
        self.root_node = self.get_root_node(self.process_rules(rules_str))
        self.message_list = messages.split('\n')

    def process_rules(self, rules_str):
        rules = [(int(rule.split(': ')[0]), rule.split(': ')[1]) for rule in rules_str.splitlines()]
        rules.sort(key=lambda x: x[0])
        return {rule[0]: rule[1] for rule in rules}

    def get_root_node(self, rules_list):
        rules_dict = {}
        for index, rule in rules_list.items():

            if "|" in rule:
                rules_dict[index] = [[int(and_rule) for and_rule in or_rule.strip().split(' ')]
                                     for or_rule_index, or_rule in enumerate(rule.split('|'))]

            elif '"' in rule:
                rules_dict[index] = rule[1]

            else:
                and_rules = [[int(and_rule) for and_rule in rule.strip().split(' ')]]
                rules_dict[index] = and_rules

        return self.make_node(0, rules_dict)

    def make_node(self, index, rules):
        return RuleNode(index, rules)

    def count_valid_messages(self):
        return sum(self.root_node.does_string_fulfill_rule(message) for message in self.message_list)


class MessageValidatorRecursion(MessageValidator):
    def make_node(self, index, rules):
        return RuleNodeRecurssion(index, rules)


if __name__ == '__main__':
    mv = MessageValidator('test_input2.txt')
    print(mv.count_valid_messages())

    mvr = MessageValidatorRecursion('test_input2.txt')
    print(mvr.count_valid_messages())
