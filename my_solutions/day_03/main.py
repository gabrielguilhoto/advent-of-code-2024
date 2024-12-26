import sys; sys.path.insert(0, '..')
import re
from typing import TypedDict, Literal, cast

class MulInstruction(TypedDict):
    type: Literal["mul"]
    a: int
    b: int

class DoOrDontInstruction(TypedDict):
    type: Literal["do", "don't"]
    
Instruction = MulInstruction | DoOrDontInstruction


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input: str) -> int:
        return sum(
            instr["a"] * instr["b"]
            for instr in self.find_instructions(raw_input)
            if instr["type"] == "mul"
        )

    def solve_part_2(self, raw_input: str) -> int:
        instructions = self.find_instructions(raw_input)
        should_multiply = True
        result = 0
        
        for instruction in instructions:
            if instruction["type"] == "do":
                should_multiply = True
            elif instruction["type"] == "don't":
                should_multiply = False
            elif instruction["type"] == "mul" and should_multiply:
                result += instruction["a"] * instruction["b"]
        
        return result

    
    def find_instructions(self, raw_input: str) -> list[Instruction]:
        matches = re.finditer('(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))', raw_input)

        def match_to_instruction(match: re.Match[str]) -> Instruction:
            if match.group(0).startswith("mul"):
                return {
                    "type": "mul",
                    "a": int(match.group(2)),
                    "b": int(match.group(3))
                }
            else:
                return { "type": cast(Literal["do", "don't"], match.group(0)[:-2]) }
        
        return [match_to_instruction(match) for match in matches]

        
        
   