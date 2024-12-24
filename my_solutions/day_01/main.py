import sys; sys.path.insert(0, '..')
import heapq
import collections


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        list1, list2 = self.process_raw_input(raw_input)
        heapq.heapify(list1)
        heapq.heapify(list2)

        return sum(
            (abs(heapq.heappop(list1) - heapq.heappop(list2)) for _ in range(len(list1)))
        )


    def solve_part_2(self, raw_input: list[str]) -> int:
        list1, list2 = self.process_raw_input(raw_input)
        list2_counter = collections.Counter(list2)

        return sum((n * list2_counter[n] for n in list1))

    def process_raw_input(self, raw_input: list[str]) -> list[list[int]]:
        list1 : list[int] = []
        list2 : list[int] = []

        for line in raw_input:
            [number1, number2] = line.split()
            list1.append(int(number1))
            list2.append(int(number2))   

        return [list1, list2]