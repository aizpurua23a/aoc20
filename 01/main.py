def ex_01():
    #num_list = [1721, 979, 366, 299, 675, 1456]
    with open('input.txt', 'r') as file:
        num_list = [int(x) for x in file.read().split('\n')]

    for first_num in num_list:
        for second_num in num_list:
            for third_num in num_list:
                if first_num != second_num != third_num:
                    if first_num + second_num + third_num == 2020:
                        print(first_num * second_num * third_num)


if __name__ == '__main__':
    ex_01()
