from pprint import pprint


def get_instruction_list(filename):
    with open(filename, 'r') as file:
        return list((line.split(' ')[0], int(line.split(' ')[1])) for line in file.read().split('\n'))



class HandHeldComputer:
    def __init__(self, instructions):
        self.instructions = instructions.copy()
        self.accumulator = 0
        self.index = 0
        self.executed_instructions = [False]*len(self.instructions)

    def run(self):
        repeated_instruction = False
        while not repeated_instruction:

            # success case for part 2
            if self.index == len(self.instructions):
                return False, True, self.accumulator

            # success case for part 1
            if self.executed_instructions[self.index]:
                return True, False, self.accumulator

            self.executed_instructions[self.index] = True

            if self.instructions[self.index][0] == 'acc':
                self.accumulator += self.instructions[self.index][1]

            if self.instructions[self.index][0] == 'jmp':
                self.index += self.instructions[self.index][1]
                continue

            # ignoring nop

            self.index += 1


def part2_wrapper(instructions):
    for index, instruction in enumerate(instructions):
        iteration_instructions = instructions.copy()
        if instruction[0] == 'jmp':
            iteration_instructions[index] = ('nop', instruction[1])

        if instruction[0] == 'nop':
            iteration_instructions[index] = ('jmp', instruction[1])

        hcc = HandHeldComputer(iteration_instructions)
        _, success, acc = hcc.run()

        if success:
            return acc


if __name__ == '__main__':
    instructions = get_instruction_list('input.txt')
    hhc = HandHeldComputer(instructions)
    pprint(hhc.run())

    pprint(part2_wrapper(instructions))

