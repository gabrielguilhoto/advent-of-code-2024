import sys; sys.path.insert(0, '..')
from typing import Literal
import collections

Position = tuple[int, int]
Direction = Literal["up", "down", "left", "right"]

moves_by_direction : dict[Direction, Position] = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}

class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, map: list[str]) -> int:
        guard_position, obstacle_positions = self.get_positions_from_map(map)
        return len(self.simulate_guard_patrol(guard_position, obstacle_positions, len(map), len(map[0])))

    def solve_part_2(self, map: list[str]) -> int:
        guard_position, obstacle_positions = self.get_positions_from_map(map)
        positions_in_guard_path = self.simulate_guard_patrol(guard_position, obstacle_positions, len(map), len(map[0]))

        obstruction_possibilities = 0
        for (i, j) in positions_in_guard_path - {guard_position}:
            try:
                self.simulate_guard_patrol(guard_position, obstacle_positions | {(i, j)}, len(map), len(map[0]))
            except CycleDetected:
                obstruction_possibilities += 1
        
        return obstruction_possibilities

    def get_positions_from_map(self, map: list[str]) -> tuple[Position, set[Position]]:
        obstacle_positions : set[Position] = set()
        guard_position = None

        for i, line in enumerate(map):
            for j, char in enumerate(line):
                if char == "#":
                    obstacle_positions.add((i, j))
                elif char == "^":
                    guard_position = (i, j)

        assert guard_position is not None
        return guard_position, obstacle_positions
    
    def simulate_guard_patrol(self, guard_position: Position, obstacle_positions: set[Position], N: int, M: int) -> set[Position]:
        guard_direction : Direction = "up"
        (i, j) = guard_position
        visited_positions : set[Position] = set()
        directions_when_position_is_visited : dict[Position, set[Direction]] = collections.defaultdict(set)

        while 0 <= i < N and 0 <= j < M:
            visited_positions.add((i, j))
            if guard_direction in directions_when_position_is_visited[(i, j)]:
                raise CycleDetected()
            directions_when_position_is_visited[(i, j)].add(guard_direction)

            next_position = (i + moves_by_direction[guard_direction][0], j + moves_by_direction[guard_direction][1])
            if next_position in obstacle_positions:
                guard_direction = self.turn_right_90_degrees(guard_direction)
            else:
                i, j = next_position
        
        return visited_positions

    def turn_right_90_degrees(self, direction: Direction) -> Direction:
        if direction == "up":
            return "right"
        if direction == "right":
            return "down"
        if direction == "down":
            return "left"
        if direction == "left":
            return "up"
        
class CycleDetected(Exception):
    pass