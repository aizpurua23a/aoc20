def ex_02_a():
    with open("input.txt", "r") as file:
        lines = file.read().split('\n')
    sum_valid = 0

    for line in lines:
        config, word = line.split(':')

        reps, letter = config.split(' ')
        min_reps, max_reps = (int(x) for x in reps.split('-'))

        word = word.split(' ')[1]

        ocur = word.count(letter)
        if min_reps <= ocur <= max_reps:
            sum_valid += 1

    print(sum_valid)


def ex_02_b():
    with open("input.txt", "r") as file:
        lines = file.read().split('\n')
    sum_valid = 0

    for line in lines:
        config, word = line.split(':')

        pos, letter = config.split(' ')
        first_pos, second_pos = (int(x) for x in pos.split('-'))

        word = word.split(' ')[1]

        if word[first_pos-1] == letter or word[second_pos-1] == letter:
            sum_valid += 1

        if word[first_pos-1] == letter and word[second_pos-1] == letter:
            sum_valid -= 1

    print(sum_valid)


if __name__ == '__main__':
    ex_02_a()
    ex_02_b()
