class TicketValidator:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
        rules, my_ticket, nearby_tickets = data.split('\n\n')

        self.rules = {}
        for rule in rules.split('\n'):
            self.rules[rule.split(': ')[0]] = [tuple(int(limit) for limit in num_range.split('-'))
                                               for num_range in rule.split(': ')[1].split(' or ')]
        self.my_ticket = [int(num) for num in my_ticket.split('\n')[1].split(',')]
        self.nearby_tickets = [[int(num) for num in ticket.split(',')] for ticket in nearby_tickets.split('\n')[1:]]
        self.valid_tickets = self.get_valid_tickets()
        self.fields = self.decide_field_correlation(self.parse_tickets_for_rule_validity())

    def find_all_invalid_numbers_in_nearby_tickets(self):
        invalid_numbers = []
        for nearby_ticket in self.nearby_tickets:
            for num in nearby_ticket:
                if not any(any(self.is_num_in_range(num, num_range) for num_range in rule)
                           for rule in self.rules.values()):
                    invalid_numbers.append(num)
        return invalid_numbers

    def get_valid_tickets(self):
        valid_tickets = []
        for nearby_ticket in self.nearby_tickets:
            if all(any(self.field_fulfills_rule(num, rule) for rule in self.rules.values()) for num in nearby_ticket):
                valid_tickets.append(nearby_ticket)
        return valid_tickets

    def parse_tickets_for_rule_validity(self):
        can_rule_be_applied_to_field = {rule: [True]*len(self.valid_tickets[0]) for rule in self.rules}
        for ticket in self.valid_tickets:
            for field_index, field in enumerate(ticket):
                for rule in self.rules:
                    if not self.field_fulfills_rule(field, self.rules[rule]):
                        can_rule_be_applied_to_field[rule][field_index] = False

        return can_rule_be_applied_to_field

    def decide_field_correlation(self, rule_fulfillment_dict):
        self.fields = ['']*len(self.rules)
        finished = False
        while not finished:
            for field in rule_fulfillment_dict:
                if sum(rule_fulfillment_dict[field]) == 1:

                    index = rule_fulfillment_dict[field].index(True)
                    self.fields[index] = field
                    rule_fulfillment_dict = self.remove_element_from_rfd(rule_fulfillment_dict, index, field)

                    if len(rule_fulfillment_dict) == 1:
                        last_field = list(rule_fulfillment_dict.keys())[0]
                        if sum(rule_fulfillment_dict[last_field]) != 1:
                            raise ValueError('Something is wrong in field decision. '
                                             'Too may possibilities for last field.')
                        index = rule_fulfillment_dict[last_field].index(True)
                        self.fields[index] = field
                        finished = True
        return self.fields

    def get_departure_mul(self):
        prod = 1
        for index, field in enumerate(self.fields):
            if 'departure ' in field:
                prod *= self.my_ticket[index]
        return prod

    @staticmethod
    def remove_element_from_rfd(rfd, index, field_to_remove):
        shorter_rfd = rfd.copy()
        for field, rfv in rfd.items():
            rfv[index] = False
            shorter_rfd[field] = rfv

        shorter_rfd.pop(field_to_remove)
        return shorter_rfd

    def field_fulfills_rule(self, num, rule):
        return self.is_num_in_range(num, rule[0]) or self.is_num_in_range(num, rule[1])

    @staticmethod
    def is_num_in_range(num, range_tuple):
        return range_tuple[0] <= num <= range_tuple[1]


if __name__ == '__main__':
    tv = TicketValidator('input.txt')
    rfd = tv.parse_tickets_for_rule_validity()
    print(tv.find_all_invalid_numbers_in_nearby_tickets())
    print(tv.decide_field_correlation(rfd))
    print(tv.get_departure_mul())
