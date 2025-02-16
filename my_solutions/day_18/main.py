import collections

Position = tuple[int, int]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int | float:
        byte_positions = self.process_raw_input(raw_input)
        is_test = len(byte_positions) == 25
        N = 7 if is_test else 71
        bytes_to_fall = 12 if is_test else 1024

        return self.find_shortest_path_steps(set(byte_positions[:bytes_to_fall]), N)

    def solve_part_2(self, raw_input: list[str]) -> Position | None:
        byte_positions = self.process_raw_input(raw_input)
        is_test = len(byte_positions) == 25
        N = 7 if is_test else 71

        return self.find_byte_that_prevents_exist(byte_positions, N)

    def process_raw_input(self, raw_input: list[str]) -> list[Position]:
        result: list[Position] = []
        for line in raw_input:
            (x, y) = line.split(",")
            result.append((int(x), int(y)))
        return result

    def find_byte_that_prevents_exist(
        self, byte_positions: list[Position], N: int
    ) -> Position | None:
        left = 0
        right = len(byte_positions) - 1

        mid = (left + right) // 2
        lowest_blocking_index: int | None = None

        while left <= right:
            steps = self.find_shortest_path_steps(set(byte_positions[: mid + 1]), N)

            if steps == float("inf"):
                lowest_blocking_index = mid
                right = mid - 1
            else:
                left = mid + 1

            mid = (left + right) // 2

        return byte_positions[lowest_blocking_index] if lowest_blocking_index is not None else None

    def find_shortest_path_steps(self, byte_positions: set[Position], N: int) -> int | float:
        queue = collections.deque([((0, 0), 0)])
        discovered = {(0, 0)}

        while queue:
            (x, y), dist = queue.popleft()
            if (x, y) == (N - 1, N - 1):
                return dist

            for neighbor in self.get_neighbors(x, y, byte_positions, N):
                if neighbor not in discovered:
                    discovered.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return float("inf")

    def get_neighbors(
        self, x: int, y: int, byte_positions: set[Position], N: int
    ) -> list[Position]:
        return [
            (x_n, y_n)
            for (x_n, y_n) in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if 0 <= x_n < N and 0 <= y_n < N and (x_n, y_n) not in byte_positions
        ]
