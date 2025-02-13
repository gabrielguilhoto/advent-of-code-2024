import typing

Map = list[str]
Position = tuple[int, int]

Direction = typing.Literal["up", "down", "left", "right"]
PositionAndDirection = tuple[int, int, Direction]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, map: Map) -> int:
        visited: set[Position] = set()
        price = 0

        for i in range(len(map)):
            for j in range(len(map[i])):
                if (i, j) not in visited:
                    area, perimeter, _ = self.find_region_area_perimeter_and_borders(
                        map, (i, j), visited
                    )
                    price += area * perimeter

        return price

    def solve_part_2(self, map: Map) -> int:
        visited: set[Position] = set()
        price = 0

        for i in range(len(map)):
            for j in range(len(map[i])):
                if (i, j) not in visited:
                    area, _, region_borders = self.find_region_area_perimeter_and_borders(
                        map, (i, j), visited
                    )
                    sides = self.count_sides_from_borders(region_borders)
                    price += area * sides

        return price

    def find_region_area_perimeter_and_borders(
        self, map: Map, position: Position, visited: set[Position]
    ) -> tuple[int, int, set[PositionAndDirection]]:
        visited.add(position)
        neighbors_in_region, borders = self.get_neighbors_and_borders(map, position)

        area = 1
        perimeter = len(borders)

        for neighbor in neighbors_in_region:
            if neighbor not in visited:
                neighboring_area, neighboring_perimeter, neighbor_borders = (
                    self.find_region_area_perimeter_and_borders(map, neighbor, visited)
                )
                area += neighboring_area
                perimeter += neighboring_perimeter
                borders |= neighbor_borders

        return area, perimeter, borders

    def get_neighbors_and_borders(
        self, map: Map, position: Position
    ) -> tuple[set[Position], set[PositionAndDirection]]:
        (i, j) = position

        all_neighbors: set[PositionAndDirection] = {
            (i, j + 1, "right"),
            (i, j - 1, "left"),
            (i + 1, j, "down"),
            (i - 1, j, "up"),
        }
        neighbors_in_region: set[PositionAndDirection] = {
            (i_n, j_n, direction)
            for (i_n, j_n, direction) in all_neighbors
            if 0 <= i_n < len(map) and 0 <= j_n < len(map[i_n]) and map[i][j] == map[i_n][j_n]
        }
        borders = all_neighbors - neighbors_in_region
        neighbors_in_region_without_direction = {
            (i_n, j_n) for (i_n, j_n, _) in neighbors_in_region
        }

        return neighbors_in_region_without_direction, borders

    def count_sides_from_borders(self, borders: set[PositionAndDirection]) -> int:
        borders_by_direction: dict[Direction, list[Position]] = {
            "right": [],
            "left": [],
            "up": [],
            "down": [],
        }
        for i, j, direction in borders:
            borders_by_direction[direction].append(
                (i, j) if direction in {"up", "down"} else (j, i)
            )

        sides = 0
        for direction, direction_borders in borders_by_direction.items():
            direction_borders.sort()
            prev_i, prev_j = None, None

            for i, j in direction_borders:
                if i != prev_i or j - 1 != prev_j:
                    sides += 1
                prev_i, prev_j = i, j

        return sides
