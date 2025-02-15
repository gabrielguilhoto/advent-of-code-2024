import collections
import math
import re
import typing


class Robot(typing.TypedDict):
    position: tuple[int, int]
    velocity: tuple[int, int]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        W, T = (11, 7) if len(raw_input) == 12 else (101, 103)
        robots = self.process_raw_input(raw_input)

        self.simulate(robots, 100, W, T)
        return math.prod(self.count_robots_in_quadrants(robots, W, T))

    def solve_part_2(self, raw_input: list[str]) -> int:
        W, T = (101, 103)
        robots = self.process_raw_input(raw_input)

        i = 0
        while True:
            max_robot_streak = self.get_max_robot_streak(robots, W, T)
            if max_robot_streak >= 10:
                print(f"==== {i} ====")
                self.print_robots(robots, W, T)
                return i

            self.simulate(robots, 1, W, T)
            i += 1

    def process_raw_input(self, raw_input: list[str]) -> list[Robot]:
        robots: list[Robot] = []
        for line in raw_input:
            match = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
            if match:
                robots.append(
                    {
                        "position": (int(match.group(1)), int(match.group(2))),
                        "velocity": (int(match.group(3)), int(match.group(4))),
                    }
                )
            else:
                raise ValueError("Invalid input")
        return robots

    def simulate(self, robots: list[Robot], seconds: int, W: int, T: int):
        for _ in range(seconds):
            for robot in robots:
                (x, y) = robot["position"]
                (v_x, v_y) = robot["velocity"]
                robot["position"] = ((x + v_x) % W, (y + v_y) % T)

    def count_robots_in_quadrants(self, robots: list[Robot], W: int, T: int) -> list[int]:
        robots_per_quadrant = [0, 0, 0, 0]

        for robot in robots:
            (x, y) = robot["position"]
            quadrant = self.get_position_quadrant(x, y, W, T)
            if quadrant is not None:
                robots_per_quadrant[quadrant] += 1

        return robots_per_quadrant

    def get_position_quadrant(self, x: int, y: int, W: int, T: int) -> int | None:
        if x < W // 2:
            if y < T // 2:
                return 0
            if y > T // 2:
                return 1
        if x > W // 2:
            if y < T // 2:
                return 2
            if y > T // 2:
                return 3
        return None

    def get_max_robot_streak(self, robots: list[Robot], W: int, T: int):
        positions_with_robots = set(robot["position"] for robot in robots)
        max_robot_streak = 0
        curr_robot_streak = 0

        for y in range(T):
            curr_robot_streak = 0
            for x in range(W):
                if (x, y) in positions_with_robots:
                    curr_robot_streak += 1
                    max_robot_streak = max(max_robot_streak, curr_robot_streak)
                else:
                    curr_robot_streak = 0

        return max_robot_streak

    def print_robots(self, robots: list[Robot], W: int, T: int):
        robots_by_position: dict[tuple[int, int], int] = collections.defaultdict(int)
        for robot in robots:
            robots_by_position[robot["position"]] += 1

        for y in range(T):
            for x in range(W):
                print(robots_by_position[(x, y)] or ".", end="")
            print()
