import collections

Position = tuple[int, int]
AntennaPositionsByFrequency = dict[str, list[Position]]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        antenna_positions_by_frequency = self.process_raw_input(raw_input)
        return sum(
            1
            for i in range(len(raw_input))
            for j in range(len(raw_input[i]))
            if self.does_position_have_antinode(
                (i, j), antenna_positions_by_frequency, should_check_distance=True
            )
        )

    def solve_part_2(self, raw_input: list[str]) -> int:
        antenna_positions_by_frequency = self.process_raw_input(raw_input)
        return sum(
            1
            for i in range(len(raw_input))
            for j in range(len(raw_input[i]))
            if self.does_position_have_antinode(
                (i, j), antenna_positions_by_frequency, should_check_distance=False
            )
        )

    def process_raw_input(self, raw_input: list[str]) -> AntennaPositionsByFrequency:
        antenna_positions_by_frequency: AntennaPositionsByFrequency = collections.defaultdict(list)

        for i, line in enumerate(raw_input):
            for j, char in enumerate(line):
                if char != ".":
                    antenna_positions_by_frequency[char].append((i, j))

        return antenna_positions_by_frequency

    def does_position_have_antinode(
        self,
        position: Position,
        antenna_positions_by_frequency: AntennaPositionsByFrequency,
        should_check_distance: bool,
    ) -> bool:
        for positions in antenna_positions_by_frequency.values():
            for p1 in range(len(positions)):
                for p2 in range(p1 + 1, len(positions)):
                    if not self.are_points_in_line(position, positions[p1], positions[p2]):
                        continue

                    if not should_check_distance:
                        return True

                    d1 = self.get_distance(position, positions[p1])
                    d2 = self.get_distance(position, positions[p2])
                    if d1 == d2 * 2 or d2 == d1 * 2:
                        return True
        return False

    def are_points_in_line(self, a: Position, b: Position, c: Position) -> bool:
        return a[1] * (b[0] - c[0]) + b[1] * (c[0] - a[0]) + c[1] * (a[0] - b[0]) == 0

    def get_distance(self, a: Position, b: Position) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
