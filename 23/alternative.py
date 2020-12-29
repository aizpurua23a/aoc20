# copied from: https://topaz.github.io/paste/#XQAAAQA4FQAAAAAAAAA0m0pnuFI8c/sCZpj3cAYdgFEf51b2rvztXwo281DNqZlFhr3jD2Jc8fPt5xuNAXhIVN1hxxJ6JhBim1u2qm6ADGlqxvK/LgQbrmiD2WSgGsdd0IV1EhiLnBlFp3IPjVPU4oHBwnBBlWVe1kmRFH5fbBiLOeWKwwK6NmfBW97JjjqrZI4I80ZZ0p/C6p/o1CNhU8QsBmzc5O1C+YXbM0JyiPLs7l0FWUusl3tSHNPBSB08SfqaL5Q2/HY91duj9XSSJPsgn6uPEQTTOLzdanbn7zNvtlB51CEGcVo77f9u1uULAFgnkt7+DumpgDcSshA/nzxHNg2APKeMXlHOnLXfcWtLl7XWI+uBiBe3MO68nc8RpGKmeQjXRYqI6dzdHTPSW1rEOiINCiS0R9QZRD70mD0UVhCA52Tlpci2IbHPORpFzr9c8x3FkavvUPmhiOtG9gInoPus0uBuKOeEHMmsZmq/DdpftjqAk4Esa6j6N926M7/LDQCQ01kqycRt+d3AggOULRxL/H8+ZR+6d2JhCrfM/hQXvyXajvevMlOWpB6q2ydtkYejzRj+Naeaxd++0Y4Gg1hIBzyRULpFAsE3kKe1ik5UoNILWv0GQoE5aQ7xa/1gmAbQnrJUCHQlkAoi51PmyAXdAtElZ/r3v0Kri7CA394mjsslPsq81ROjr69h/D8Lvgr1myhOYX/fLmGr0arA12Pf09+i1ajlYZIIV40iZehCF/F0YYc059OXTZlRl4MDaNbRWp9cCDO4CjYhuOtP60BEz6lkcH3Y4FfltzE6yuqxnxX13knAAQ9GMIutMb/OA1wTLg8PGTXgxwGj5B4TomQoBvuT+HDj5FjMjoYkqoYwGetZmr+IFL1CTpimpOj1AKYG2FH8b8dC/ezZgZX+YyJYO4ZF+WRNVI6dJg7rzwXZasQI/oIjLTVPoOY0Uz9NP1xkq8PM48O7lchEH2tXZ0595AToWI12O1Dsn7NLZ4xzJwQCeMen6kQAL3owCGt5Bm/+/d+jBGu+bACHy3n28fFVUGLD9WnSKxmRUZV52MmpLEP4aT5sY25/S5C5cCixJA8ih/j4Mi5DseJ7od9GNMXz/Aa50cf8oOeSvWTz/WZ1FgOy2FrQj9SbCNrQ2EX9KHnRL9W/TMUFdKKOh68asz/vLd2jdKUv5P+dG3DCu9GeDxndN9fLunMm5ucgZeb7gm+kuzxqgwN8AtNExj5kPfoG/syb9qimdlT1aTCTloNOvlVbqrWgEa5cZoRPajcT4WLthkCMFGau4TYQLqoPOEBsmnsU0+1aG1JwgFX8skigIcvcvdm1TH3+IK9RCKiud7zljQWv3/1bHqvT73kij2bAvm8T1aAYWe0qjnkQkzJgefMhUc4yt/l9TbVEsunTkLXKCEpj5qWOI4XIkslObnUHZ883hPt1d1ZZl9EGykcv8igpE7rFLED4vUvDk2Ys3OHKp6shF44RZuJ05yoUBWg0AkIX5vV5LAz1R8tel1Bd7jbDPBQZGgUzELlinpIfBZOJCEawuSCB1T7yKyfOP7zvRpd5KuziHW7/zOYdTW6Sn/HjUZx1e449MrBrVCEeVsVczZCl7LsUFV9D3BAFOhLQJxbotZCiTePYi1P0LFuCB2S6A1czIff1JnYe7kqR1sywIaiNLpjxa57RdsEOFsKmTZNeYvI+1Ejnm3UVFetOOCHjHhiQDxn/9PTFBQ==

import time
from typing import Union


class Cup:

    def __init__(self, label: int, min_label: int, max_label: int):
        self.label = label
        self.previous = max_label if label == min_label else label - 1
        self.next = min_label if label == max_label else label + 1


def run_script(filepath: str) -> Union[int, str, float, bool]:
    with open(filepath, "r") as f:
        raw_data = f.read()
    return main_function(raw_data)


def main_function(raw_data: str) -> Union[int, str, float, bool]:
    start_time = time.time()

    result = your_script(raw_data)

    elapsed_time = time.time() - start_time
    print(f"Time elapsed : {elapsed_time}s")
    return result


def your_script(raw_data: str) -> Union[int, str, float, bool]:
    """
    Time to code! Write your code here to solve today's problem
    """
    cups = initialize_cups(9, raw_data, True)
    current_cup_label = int(raw_data[0])
    perform_game(cups, current_cup_label, 100)
    print(f"Result Part 1 : {prepare_result_1(cups)}")
    cups = initialize_cups(1000000, raw_data, False)
    current_cup_label = int(raw_data[0])
    perform_game(cups, current_cup_label, 10000000)
    print(f"Result Part 2 : {prepare_result_2(cups)}")


def perform_game(cups: list, current_cup_label: int, turns: int) -> None:
    max_label = len(cups)
    for i in range(turns):
        # print(f"\nRound {i+1}")
        # pretty_print_cups(cups, 10)
        # print(f"Current cup : {current_cup_label}")
        selected_cups_labels = select_cups(cups, current_cup_label)
        # print(f"Selected : {selected_cups_labels}")
        destination_label = choose_destination(current_cup_label, selected_cups_labels, max_label)
        # print(f"Destination : {destination_label}")
        perform_transformation(cups, current_cup_label, selected_cups_labels, destination_label)
        current_cup_label = get_labeled_cup(cups, current_cup_label).next


def select_cups(cups: list, current_cup_label: int) -> list:
    selected_cups_labels = []
    current_cup = get_labeled_cup(cups, current_cup_label)
    for i in range(3):
        current_cup = get_labeled_cup(cups, current_cup.next)
        selected_cups_labels.append(current_cup.label)
    return selected_cups_labels


def choose_destination(current_cup_label: int, selected_cups_labels: list, max_label: int) -> int:
    destination_label = current_cup_label - 1
    while destination_label in selected_cups_labels or destination_label <= 0:
        destination_label -= 1
        if destination_label <= 0:
            destination_label = max_label
    return destination_label


def perform_transformation(cups: list, current_cup_label: int, selected_cups_labels: list,
                           destination_label: int) -> None:
    # Remove the selected cups
    last_selected_cup = get_labeled_cup(cups, selected_cups_labels[-1])
    get_labeled_cup(cups, current_cup_label).next = last_selected_cup.next
    get_labeled_cup(cups, last_selected_cup.next).previous = current_cup_label
    # Insert the selected cups
    destination_cup = get_labeled_cup(cups, destination_label)
    destination_neighbor_label = destination_cup.next
    destination_cup.next = selected_cups_labels[0]
    get_labeled_cup(cups, selected_cups_labels[0]).previous = destination_label
    last_selected_cup.next = destination_neighbor_label
    get_labeled_cup(cups, destination_neighbor_label).previous = selected_cups_labels[-1]


def initialize_cups(count: int, raw_data: str, part1: bool) -> list:
    cups = [Cup(i, 1, count) for i in range(1, count + 1)]
    for i in range(1, len(raw_data) - 1):
        current_cup = get_labeled_cup(cups, int(raw_data[i]))
        current_cup.previous = int(raw_data[i - 1])
        current_cup.next = int(raw_data[i + 1])
    if part1:
        first_cup = get_labeled_cup(cups, int(raw_data[0]))
        first_cup.previous = int(raw_data[-1])
        first_cup.next = int(raw_data[1])
        last_cup = get_labeled_cup(cups, int(raw_data[-1]))
        last_cup.previous = int(raw_data[-2])
        last_cup.next = int(raw_data[0])
    else:
        first_cup = get_labeled_cup(cups, int(raw_data[0]))
        first_cup.previous = count
        first_cup.next = int(raw_data[1])
        last_cup = get_labeled_cup(cups, int(raw_data[-1]))
        last_cup.previous = int(raw_data[-2])
        last_cup.next = len(raw_data) + 1
        get_labeled_cup(cups, count).next = int(raw_data[0])
    return cups


def pretty_print_cups(cups: list, count: int) -> None:
    labels = [str(cups[0].label)]
    current_cup = get_labeled_cup(cups, cups[0].next)
    i = 1
    while not current_cup == cups[0] and i < count:
        labels.append(str(current_cup.label))
        current_cup = get_labeled_cup(cups, current_cup.next)
        i += 1
    print("Cups : " + ", ".join(labels))


def prepare_result_1(cups: list) -> str:
    labels = []
    current_cup = get_labeled_cup(cups, cups[0].next)
    while not current_cup == cups[0]:
        labels.append(str(current_cup.label))
        current_cup = get_labeled_cup(cups, current_cup.next)
    return "".join(labels)


def prepare_result_2(cups: list) -> str:
    current_label = 1
    total = 1
    for i in range(2):
        current_label = get_labeled_cup(cups, current_label).next
        total *= current_label
    return total


def get_labeled_cup(cups: list, label: int) -> Cup:
    return cups[label - 1]


if __name__ == "__main__":
    print(run_script("input.txt"))