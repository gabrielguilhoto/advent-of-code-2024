import heapq
import typing

Map = list[str]
Position = tuple[int, int]
Direction = typing.Literal["east", "south", "west", "north"]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, map: Map) -> int | float:
        return self.find_best_path_score(map)

    def solve_part_2(self, raw_input): ...

    def find_best_path_score(self, map: Map) -> int | float:
        start = self.find_start_position(map)
        queue: list[tuple[int, Position, Direction]] = [(0, start, "east")]
        score_on = {(start, "east"): 0}
        visited: set[tuple[Position, Direction]] = set()

        while queue:
            (score, position, direction) = heapq.heappop(queue)
            if (position, direction) in visited:
                continue
            visited.add((position, direction))

            (i, j) = position
            if map[i][j] == "E":
                return score

            for neighbor in self.get_neighbors(map, position, direction):
                (position, direction, additional_score) = neighbor
                new_score = score + additional_score
                if (position, direction) not in score_on or new_score < score_on[
                    (position, direction)
                ]:
                    heapq.heappush(queue, (new_score, position, direction))
                    score_on[(position, direction)] = new_score

        return float("inf")

    def find_start_position(self, map: Map) -> Position:
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == "S":
                    return (i, j)

        raise ValueError("Start position not found")

    def get_neighbors(
        self, map: Map, position: Position, direction: Direction
    ) -> list[tuple[Position, Direction, int]]:
        neighbors: list[tuple[Position, Direction, int]] = []

        (i_n, j_n) = self.get_position_by_moving(position, direction)
        if 0 <= i_n < len(map) and 0 <= j_n < len(map[i_n]) and map[i_n][j_n] != "#":
            neighbors.append(((i_n, j_n), direction, 1))

        for neigh_direction in self.get_directions_by_turning_90_degrees(direction):
            neighbors.append((position, neigh_direction, 1000))

        return neighbors

    def get_position_by_moving(self, position: Position, direction: Direction) -> Position:
        (i, j) = position

        match direction:
            case "east":
                return (i, j + 1)
            case "south":
                return (i + 1, j)
            case "west":
                return (i, j - 1)
            case "north":
                return (i - 1, j)

    def get_directions_by_turning_90_degrees(self, direction: Direction) -> set[Direction]:
        match direction:
            case "east" | "west":
                return {"north", "south"}
            case "north" | "south":
                return {"west", "east"}
