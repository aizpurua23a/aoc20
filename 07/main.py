from pprint import pprint


class BagRules:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            rules = file.read().split('\n')
        self.rules = self._get_rules_dict_from_rules(rules)

    def ex_07_01(self):
        valid_bags = [False]*len(self.rules)

        new_valid_bags_found = True
        valid_bags_running_list = ['shiny gold']
        while new_valid_bags_found:
            initial_valid_bags_count = sum(valid_bags)
            for key:value in enumerate(self.rules):
                if any(valid_bag in allowed_bags
                       for valid_bag in valid_bags_running_list
                       for allowed_bags in rule.keys()):
                    valid_bags[index] = True
                    valid_bags_running_list.append(self.rules.keys()[index])
            final_valid_bags_count = sum(valid_bags)
            new_valid_bags_found = final_valid_bags_count > initial_valid_bags_count

        return valid_bags


    @staticmethod
    def _get_rules_dict_from_rules( rules):
        rules_dict = {}
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

            rules_dict[bag] = parsed_contents
        return rules_dict


def ex_07_01():
    pass


if __name__ == '__main__':
    bg = BagRules('test_input.txt')
    pprint(bg.ex_07_01())
