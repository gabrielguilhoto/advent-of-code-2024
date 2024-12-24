import sys; sys.path.insert(0, '..')


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        reports = self.process_raw_input(raw_input)
        report_safeness = [
            self.is_report_safe(report, is_increasing=True)
            or self.is_report_safe(report, is_increasing=False)
            for report in reports
        ]
        return len([safe for safe in report_safeness if safe])

    def solve_part_2(self, raw_input: list[str]) -> int:
        reports = self.process_raw_input(raw_input)
        report_safeness = [
            self.is_report_safe(report, is_increasing=True, with_dampener=True)
            or self.is_report_safe(report, is_increasing=False, with_dampener=True)
            or self.is_report_safe(report[1:], is_increasing=True, with_dampener=False)
            or self.is_report_safe(report[1:], is_increasing=False, with_dampener=False)
            for report in reports
        ]
        return len([safe for safe in report_safeness if safe])

    def process_raw_input(self, raw_input: list[str]) -> list[list[int]]:
        return [[int(x) for x in line.split()] for line in raw_input]
    
    def is_report_safe(self, report: list[int], is_increasing: bool, with_dampener: bool = False) -> bool:
        last_number = report[0]
        dampener_uses_left = 1 if with_dampener else 0

        for number in report[1:]:
            if not self.is_number_safe(number, last_number, is_increasing):
                if dampener_uses_left:
                    dampener_uses_left -= 1
                    continue

                return False
            
            last_number = number
            
        return True
    
    def is_number_safe(self, number: int, last_number: int, is_increasing: bool) -> bool:
        if is_increasing and number < last_number:
            return False
        
        if not is_increasing and number > last_number:
            return False

        difference = abs(number - last_number)
        if difference < 1 or difference > 3:
            return False
        
        return True