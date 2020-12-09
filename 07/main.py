from pprint import pprint


class BagNode:
    def __init__(self, name, amount, rules):
        self.name = name
        self.amount = amount
        self.children = self.make_children_from_rule([rule[name] for rule in rules if [*rule][0] == name][0], rules)

    def make_children_from_rule(self, rule, rules):
        return [BagNode(key, rule[key], rules) for key in rule]

    def get_bag_amount(self):
        return (sum(child.get_bag_amount() for child in self.children)+1) * self.amount


class BagRules:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            rules = file.read().split('\n')
        self.rules = self._get_rules_list_from_rules(rules)

    def ex_07_01(self):
        valid_bags = [False]*len(self.rules)
        valid_bags_running_list = ['shiny gold']
        added_bags = 1
        while added_bags:
            added_bags = 0
            for index, rule in enumerate(self.rules):
                if any(valid_bag in list(bag_rules.keys()) for valid_bag in valid_bags_running_list for bag_rules in rule.values()):
                    added_bags += not(valid_bags[index])
                    valid_bags[index] = True
                    valid_bags_running_list.append([*self.rules[index]][0])
        return valid_bags

    def ex_07_02(self):
        root = BagNode('shiny gold', 1, self.rules)
        return root.get_bag_amount()-1

    @staticmethod
    def _get_rules_list_from_rules(rules):
        rules_list = []
        for rule in rules:
            bag, contents = rule.split(' contain ')
            bag = bag[:-5]  # removing " bags"
            contents = contents[:-1]  # removing the last period.
            contents = contents.split(', ')
            parsed_contents = {}
            for content in contents:
                if content == "no other bags":
                    break
                elif content[0] == '1':
                    parsed_contents[content[2:-4]] = 1
                else:
                    parsed_contents[content[2:-5]] = int(content[0])
            rules_list.append({bag: parsed_contents})
        return rules_list


def ex_07_01():
    pass


if __name__ == '__main__':
    bg = BagRules('test_input2.txt')
    pprint(sum(bg.ex_07_01()))

    bg2 = BagRules('input.txt')
    bg2.ex_07_02()
