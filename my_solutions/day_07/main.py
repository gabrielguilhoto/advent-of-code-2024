import sys; sys.path.insert(0, '..')
from typing import Literal

Equation = tuple[int, list[int]]
Operator = Literal["+", "*", "||"]

class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        equations = self.process_raw_input(raw_input)
        return sum(
            equation[0]
            for equation in equations
            if self.can_equation_be_true(equation, ["+", "*"], [])
        )

    def solve_part_2(self, raw_input: list[str]) -> int:
        equations = self.process_raw_input(raw_input)
        return sum(
            equation[0]
            for equation in equations
            if self.can_equation_be_true(equation, ["+", "*", "||"], [])
        )

    def process_raw_input(self, raw_input: list[str]) -> list[Equation]:
        result : list[Equation] = []

        for line in raw_input:
            [test_value, numbers] = line.split(":")
            result.append((int(test_value), [int(n) for n in numbers.split()]))

        return result

    def can_equation_be_true(self, equation: Equation, operators: list[Operator], partial_solution: list[Operator]) -> bool:
        if len(partial_solution) == len(equation[1]) - 1:
            return self.are_operators_correct(equation, partial_solution)
        
        for operator in operators:
            partial_solution.append(operator)

            result = self.can_equation_be_true(equation, operators, partial_solution)
            if result: return result

            partial_solution.pop()
        
        return False


    def are_operators_correct(self, equation: Equation, operators: list[Operator]) -> bool:
        test_value, numbers = equation
        result = numbers[0]

        for i, number in enumerate(numbers[1:]):
            if operators[i] == "+":
                result += number
            elif operators[i] == "*":
                result *= number
            elif operators[i] == "||":
                result = int(str(result) + str(number))
        
        return result == test_value