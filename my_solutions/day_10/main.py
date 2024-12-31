import collections

Position = tuple[int, int]
Map = list[list[int]]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        map = self.parse_raw_input(raw_input)
        return sum(
            self.get_trailhead_score_via_bfs(map, i, j)
            for i, row in enumerate(map)
            for j, height in enumerate(row)
            if height == 0
        )

    def solve_part_2(self, raw_input: list[str]) -> int:
        map = self.parse_raw_input(raw_input)
        return sum(
            self.count_trails_beggining_at(map, i, j)
            for i, row in enumerate(map)
            for j, height in enumerate(row)
            if height == 0
        )

    def parse_raw_input(self, raw_input: list[str]) -> Map:
        return [[int(n) for n in line] for line in raw_input]

    def get_trailhead_score_via_dfs(self, map: Map, i: int, j: int, visited: set[Position]) -> int:
        visited.add((i, j))
        if map[i][j] == 9:
            return 1

        score = 0
        for i_n, j_n in self.get_neighbors(map, i, j):
            if (i_n, j_n) not in visited:
                score += self.get_trailhead_score_via_dfs(map, i_n, j_n, visited)
        return score

    def get_trailhead_score_via_bfs(self, map: Map, i: int, j: int) -> int:
        discovered = {(i, j)}
        queue = collections.deque([(i, j)])
        score = 0

        while queue:
            (i_q, j_q) = queue.popleft()

            if map[i_q][j_q] == 9:
                score += 1
                continue

            for i_n, j_n in self.get_neighbors(map, i_q, j_q):
                if (i_n, j_n) not in discovered:
                    discovered.add((i_n, j_n))
                    queue.append((i_n, j_n))

        return score

    def count_trails_beggining_at(self, map: Map, i: int, j: int) -> int:
        if map[i][j] == 9:
            return 1

        return sum(
            self.count_trails_beggining_at(map, i_n, j_n)
            for (i_n, j_n) in self.get_neighbors(map, i, j)
        )

    def get_neighbors(self, map: Map, i: int, j: int) -> list[Position]:
        return [
            (i_n, j_n)
            for (i_n, j_n) in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            if 0 <= i_n < len(map) and 0 <= j_n < len(map[0]) and map[i_n][j_n] == map[i][j] + 1
        ]
