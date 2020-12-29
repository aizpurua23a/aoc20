# All credit is due to https://www.reddit.com/r/adventofcode/comments/kimluc/2020_day_23_solutions/ggsc9sm?utm_source=share&utm_medium=web2x&context=3
# Using a list indexed by ids with pointers to other ids.

class Cup:
    def __init__(self, cup_id, max_id, min_id):
        self.cup_id = cup_id
        self.previous_id = max_id if cup_id == min_id else cup_id - 1
        self.next_id = min_id if cup_id == max_id else cup_id + 1

    def __repr__(self):
        return 'Node ID: {}'.format(self.cup_id)


class CupGame:
    def __init__(self, cup_input, max_value=None, part1=False):
        if max_value is None:
            max_value = max(int(x) for x in cup_input)

        self.max_value = max_value
        self.cups = [Cup(i, 1, max_value) for i in range(1, max_value + 1)]

        for i in range(1, len(cup_input) - 1):
            current_cup = self.get_cup_by_label(int(cup_input[i]))
            current_cup.previous_id = int(cup_input[i - 1])
            current_cup.next_id = int(cup_input[i + 1])

        if part1:
            first_cup = self.get_cup_by_label(int(cup_input[0]))
            first_cup.previous_id = int(cup_input[-1])
            first_cup.next_id = int(cup_input[1])
            last_cup = self.get_cup_by_label(int(cup_input[-1]))
            last_cup.previous_id = int(cup_input[-2])
            last_cup.next_id = int(cup_input[0])
        else:
            first_cup = self.get_cup_by_label(int(cup_input[0]))
            first_cup.previous_id = max_value
            first_cup.next_id = int(cup_input[1])
            last_cup = self.get_cup_by_label(int(cup_input[-1]))
            last_cup.previous_id = int(cup_input[-2])
            last_cup.next_id = len(cup_input) + 1
            self.get_cup_by_label(max_value).next_id = int(cup_input[0])

        self.first_id = int(cup_input[0])

    def get_cup_by_label(self, label):
        return self.cups[label-1]

    def play(self, moves):
        old_head = self.first_id
        move = 0

        while move < moves:
            if move % 1000000 == 0:
                print('Move: {} million'.format(move//1000000))

            # initial disposition:
            # old_head -- slice-head -- # -- slice-tail -- old_tail -- ... -- new_head -- new_tail -- ...

            # new disposition:
            # old_head -- old_tail -- ... -- new_head -- slice-head -- # -- slice-tail -- new_tail -- ...

            slice_head = self.get_cup_by_label(old_head).next_id
            slice_mid = self.get_cup_by_label(slice_head).next_id
            slice_tail = self.get_cup_by_label(slice_mid).next_id
            old_tail = self.get_cup_by_label(slice_tail).next_id
            new_head, new_tail = self.get_new_head_and_tail(old_head, (slice_head, slice_mid, slice_tail))


            # stiching in the new order
            self.get_cup_by_label(old_head).next_id = old_tail
            self.get_cup_by_label(old_tail).previous_id = old_head

            self.get_cup_by_label(new_head).next_id = slice_head
            self.get_cup_by_label(slice_head).previous_id = new_head

            self.get_cup_by_label(slice_tail).next_id = new_tail
            self.get_cup_by_label(new_tail).previous_id = slice_tail

            old_head = self.get_cup_by_label(old_head).next_id
            move += 1


    def get_new_head_and_tail(self, old_head, slice_ids):
        candidate_id = old_head - 1
        while candidate_id <= 0 or candidate_id in slice_ids:
            candidate_id += -1

            if candidate_id <= 0:
                candidate_id = self.max_value

        new_head = candidate_id
        new_tail = self.get_cup_by_label(new_head).next_id

        return new_head, new_tail

    def print_full_loop(self):
        cup = self.cups[0]
        while True:
            print(cup.cup_id, end='')
            cup = self.get_cup_by_label(cup.next_id)
            if cup.cup_id == self.cups[0].cup_id:
                break
        print()

    def print_first_three_elements(self):
        print(self.cups[0].cup_id)
        print(self.get_cup_by_label(self.cups[0].next_id).cup_id)
        print(self.get_cup_by_label(self.get_cup_by_label(self.cups[0].next_id).next_id).cup_id)

    def part_2_sol(self):
        return self.get_cup_by_label(self.cups[0].next_id).cup_id * \
               self.get_cup_by_label(self.get_cup_by_label(self.cups[0].next_id).next_id).cup_id

    @classmethod
    def part1(cls):
        cg = CupGame('523764819', part1=True)
        cg.play(100)
        cg.print_full_loop()

    @classmethod
    def part2(cls):
        cg = CupGame('523764819', max_value=1000000)
        cg.play(10000000)
        cg.print_first_three_elements()
        print(cg.part_2_sol())


if __name__ == '__main__':
    CupGame.part1()
    CupGame.part2()
