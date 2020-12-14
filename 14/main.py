class BitMask1:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.read().splitlines()

        self.instructions = []
        for line in data:
            if line[:4] == 'mask':
                mask = line.split(' = ')[1]
                mask = {35-index: int(value) for (index, value) in enumerate(mask) if value != 'X'}
                self.instructions.append(("mask", mask))

            if line[:3] == 'mem':
                lh, rh = line.split(' = ')
                index = int(lh.split('[')[1][:-1])
                value = int(rh)
                self.instructions.append(('mem', index, value))
        self.memory = [0] * (max(instruction[1] for instruction in self.instructions if instruction[0] == 'mem') + 1)

    def run_instructions(self):
        for instruction in self.instructions:
            if instruction[0] == "mask":
                self.mask = instruction[1]
            if instruction[0] == "mem":
                self.memory[instruction[1]] = self.apply_mask_to_value(instruction[2])
        return sum(self.memory)

    def apply_mask_to_value(self, value):
        result = value
        for k, m in self.mask.items():
            result |= (m << k)

        return result


class BitMask2:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.read().splitlines()

        self.instructions = []
        for line in data:
            if line[:4] == 'mask':
                mask = line.split(' = ')[1]
                self.instructions.append(("mask", mask))

            if line[:3] == 'mem':
                lh, rh = line.split(' = ')
                index = int(lh.split('[')[1][:-1])
                value = int(rh)
                self.instructions.append(('mem', index, value))
        self.memory = []

    def run_instructions(self):
        for index, instruction in enumerate(self.instructions):
            if index % 10 == 0:
                print('Instruction: {}'.format(index))

            if instruction[0] == "mask":
                self.mask = instruction[1]

            if instruction[0] == "mem":
                addresses_set = self.get_array_of_all_possible_addresses(instruction[1])
                self.update_memory(instruction[2], addresses_set)
        return sum(x[0] * len(x[1]) for x in self.memory)

    def update_memory(self, value, new_addresses):
        for new_address in new_addresses:
            for used_memory in self.memory:
                used_memory[1].discard(new_address)
        self.memory.append((value, new_addresses))

    def get_array_of_all_possible_addresses(self, address):
        and_mask = self.bin_to_int(self.mask.replace('X', '0'))
        new_address = address | and_mask
        possible_addresses = {new_address}

        for index, char in enumerate(self.mask):
            if char == "X":
                new_addresses = set()
                for p_addr in possible_addresses:
                    new_addresses.add(self.set_bit(p_addr, len(self.mask) - index - 1))
                    new_addresses.add(self.clear_bit(p_addr, len(self.mask) - index - 1))
                possible_addresses.update(new_addresses)
        return possible_addresses

    def set_bit(self, num, offset):
        mask = 1 << offset
        return num | mask

    def clear_bit(self, num, offset):
        mask = ~(1 << offset)
        return num & mask

    def bin_to_int(self, num):
        sum = 0
        for index, element in enumerate(num):
            if element == '1':
                sum += 2**(len(num) - index - 1)
        return sum


if __name__ == '__main__':
    bm = BitMask2('input.txt')
    print(bm.run_instructions())
