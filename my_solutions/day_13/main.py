import re
import typing

Coordinates = tuple[int, int]


class Machine(typing.TypedDict):
    a_button: Coordinates
    b_button: Coordinates
    prize: Coordinates


INPUT_REGEX = r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)"""


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        machines = self.process_raw_input(raw_input)
        return self.tokens_to_win_machines(machines)

    def solve_part_2(self, raw_input: list[str]) -> int:
        machines = self.process_raw_input(raw_input, 10000000000000)
        return self.tokens_to_win_machines(machines)

    def process_raw_input(self, raw_input: list[str], prize_offset: int = 0) -> list[Machine]:
        machines: list[Machine] = []
        for raw_machine in raw_input:
            match = re.match(INPUT_REGEX, raw_machine)
            if match:
                machines.append(
                    {
                        "a_button": (int(match.group(1)), int(match.group(2))),
                        "b_button": (int(match.group(3)), int(match.group(4))),
                        "prize": (
                            int(match.group(5)) + prize_offset,
                            int(match.group(6)) + prize_offset,
                        ),
                    }
                )
        return machines

    def tokens_to_win_machines(self, machines: list[Machine]) -> int:
        total_tokens = 0

        for machine in machines:
            machine_tokens = self.tokens_to_win_machine(machine)
            if machine_tokens is not None:
                total_tokens += machine_tokens

        return total_tokens

    def tokens_to_win_machine(self, machine: Machine) -> int | None:
        (x_p, y_p) = machine["prize"]
        (x_a, y_a) = machine["a_button"]
        (x_b, y_b) = machine["b_button"]

        system_solution = self.solve_integer_linear_system(x_a, x_b, x_p, y_a, y_b, y_p)
        if system_solution:
            (A, B) = system_solution
            return 3 * A + B
        return None

    def solve_integer_linear_system(
        self, a1: int, b1: int, c1: int, a2: int, b2: int, c2: int
    ) -> tuple[int, int] | None:
        determinant = a1 * b2 - a2 * b1

        if determinant == 0:
            if c1 * b2 == c2 * b1:
                raise ValueError("Infinite solutions")
            return None

        A = (c1 * b2 - c2 * b1) / determinant
        B = (a1 * c2 - a2 * c1) / determinant

        if A.is_integer() and B.is_integer():
            return int(A), int(B)

        return None
