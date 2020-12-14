import math
from sympy.ntheory.modular import crt
from time import time


class BusWait:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.departure_from = int(file.readline().split('\n')[0])
            self.bus_times = set(file.read().split(','))
            self.bus_times.remove('x')
            self.bus_times = set(map(int, self.bus_times))
            pass

    def calculate_first_possible_departure(self):
        wait_times = []
        for time in self.bus_times:
            mul = math.ceil(self.departure_from/time)
            wait_times.append((time, time*mul - self.departure_from))
        min_wait_time = min(wait_times, key=lambda x: x[1])
        return min_wait_time[0] * min_wait_time[1]


class BusTimeTable:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            _ = file.readline()
            bus_times = list(file.read().split(','))
            self.bus_ids = []
            for index, time in enumerate(bus_times):
                if time != 'x':
                    self.bus_ids.append((index, int(time)))

    def chinese_remainder(self):
        bus_id_mod_result = {bus[1]: (bus[1] - bus[0]) % bus[1] for bus in self.bus_ids}
        return crt(bus_id_mod_result.keys(), bus_id_mod_result.values())[0]


if __name__ == '__main__':
    btt = BusTimeTable('input.txt')
    print(btt.chinese_remainder())
