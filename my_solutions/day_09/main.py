Blocks = list[int | None]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input: str) -> int:
        blocks = self.parse_raw_input(raw_input)
        self.compact_blocks_for_part_1(blocks)

        return self.calculate_checksum(blocks)

    def solve_part_2(self, raw_input: str) -> int:
        blocks = self.parse_raw_input(raw_input)
        self.compact_blocks_for_part_2(blocks)
        
        return self.calculate_checksum(blocks)

    def parse_raw_input(self, raw_input: str) -> Blocks:
        blocks: Blocks = []
        for i, char in enumerate(raw_input):
            id = i // 2 if i % 2 == 0 else None
            blocks.extend([id] * int(char))
        return blocks

    def compact_blocks_for_part_1(self, blocks: Blocks):
        i = 0
        j = len(blocks) - 1

        while i < j:
            if blocks[j] is None:
                j -= 1
                continue

            while blocks[i] is not None:
                i += 1
                if i >= j:
                    break

            blocks[i], blocks[j] = blocks[j], blocks[i]
            j -= 1

    def compact_blocks_for_part_2(self, blocks: Blocks):
        j = len(blocks) - 1

        while j >= 0:
            file_start, file_end, file_id = self.find_next_file_to_move(blocks, j)
            j = file_start - 1
            size = file_end - file_start + 1

            position_to_move = self.find_place_to_move_file(blocks, j, size)
            if position_to_move is not None:
                for i in range(size):
                    blocks[position_to_move + i] = file_id
                    blocks[file_start + i] = None

    def find_next_file_to_move(self, blocks: Blocks, max_index: int) -> tuple[int, int, int]:
        j = max_index
        while blocks[j] is None:
            j -= 1
        file_end = j
        file_id = blocks[j]
        assert file_id is not None

        while blocks[j] == file_id:
            j -= 1
        file_start = j + 1

        return file_start, file_end, file_id

    def find_place_to_move_file(self, blocks: Blocks, max_index: int, size: int) -> int | None:
        for i in range(max_index + 1):
            if blocks[i] is not None:
                continue
            start_i = i
            while i < start_i + size and i < len(blocks) and blocks[i] is None:
                i += 1
            if i == start_i + size:
                return start_i

        return None

    def calculate_checksum(self, blocks: Blocks) -> int:
        return sum([i * block if block is not None else 0 for i, block in enumerate(blocks)])

    def print_blocks(self, blocks: Blocks):
        for block in blocks:
            print(block if block is not None else ".", end="")
        print()
