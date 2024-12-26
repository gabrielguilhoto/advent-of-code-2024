import sys; sys.path.insert(0, '..')

class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        xmas_count = 0

        for i in range(len(raw_input)):
            for j in range(len(raw_input[i])):
                if raw_input[i][j] == "X":
                    xmas_count += self.countXmasFrom(i, j, raw_input)

        return xmas_count

    def solve_part_2(self, raw_input: list[str]) -> int:
        xmas_count = 0

        for i in range(len(raw_input)):
            for j in range(len(raw_input[i])):
                xmas_count += 1 if self.isThereAnXShapedMasCenteredIn(i, j, raw_input) else 0

        return xmas_count

    def countXmasFrom(self, i_s: int, j_s: int, grid: list[str]) -> int:
        possible_steps = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        xmas_count = 0

        for step_i, step_j in possible_steps:
            if self.isThereAnXmas(i_s, j_s, step_i, step_j, grid):
                xmas_count += 1
        
        return xmas_count


    def isThereAnXmas(self, i_s: int, j_s: int, step_i: int, step_j: int, grid: list[str]) -> bool:
        last_i = i_s + step_i * 3
        last_j = j_s + step_j * 3
        if not (0 <= last_i < len(grid) and 0 <= last_j < len(grid[0])):
            return False
        
        return (
            grid[i_s][j_s] == "X"
            and grid[i_s + step_i][j_s + step_j] == "M"
            and grid[i_s + step_i * 2][j_s + step_j * 2] == "A"
            and grid[i_s + step_i * 3][j_s + step_j * 3] == "S"
        )

    def isThereAnXShapedMasCenteredIn(self, i: int, j: int, grid: list[str]) -> bool:
        if grid[i][j] != "A" or i - 1 < 0 or i + 1 >= len(grid) or j - 1 < 0 or j + 1 >= len(grid[i]):
            return False
        
        is_there_a_left_mas = (
            (grid[i - 1][j - 1] == "M" and grid[i + 1][j + 1] == "S")
            or (grid[i - 1][j - 1] == "S" and grid[i + 1][j + 1] == "M")
        )
        is_there_a_right_mas = (
            (grid[i - 1][j + 1] == "M" and grid[i + 1][j - 1] == "S")
            or (grid[i - 1][j + 1] == "S" and grid[i + 1][j - 1] == "M")
        )

        return is_there_a_left_mas and is_there_a_right_mas