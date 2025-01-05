import functools


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input: str) -> int:
        stones = self.process_raw_input(raw_input)
        return sum(self.becomes_how_many_stones_after_k_blinks(stone, 25) for stone in stones)

    def solve_part_2(self, raw_input: str) -> int:
        stones = self.process_raw_input(raw_input)
        return sum(self.becomes_how_many_stones_after_k_blinks(stone, 75) for stone in stones)

    def process_raw_input(self, raw_input: str) -> list[int]:
        return [int(n) for n in raw_input.split(" ")]

    @functools.cache
    def becomes_how_many_stones_after_k_blinks(self, stone: int, k: int) -> int:
        if k == 0:
            return 1

        stones_after_1_blink = self.change_stone(stone)
        return sum(
            self.becomes_how_many_stones_after_k_blinks(new_stone, k - 1)
            for new_stone in stones_after_1_blink
        )

    def change_stone(self, stone: int) -> list[int]:
        if stone == 0:
            return [1]

        stone_as_str = str(stone)
        N = len(stone_as_str)
        if N % 2 == 0:
            return [int(stone_as_str[: N // 2]), int(stone_as_str[N // 2 :])]

        return [stone * 2024]
