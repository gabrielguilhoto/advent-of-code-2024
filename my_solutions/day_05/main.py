import sys; sys.path.insert(0, '..')
import re
import collections
from typing import Deque

OrderingRule = tuple[int, int]
Update = list[int]

class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        page_ordering_rules, updates = self.process_raw_input(raw_input)

        return sum(
            self.get_middle_page_number(update)
            for update in updates
            if self.does_update_match_page_ordering_rules(update, page_ordering_rules)
        )

    def solve_part_2(self, raw_input: list[str]) -> int:
        page_ordering_rules, updates = self.process_raw_input(raw_input)
        result = 0

        for update in updates:
            if self.does_update_match_page_ordering_rules(update, page_ordering_rules):
                continue
            
            pages_in_update = set(update)
            filtered_rules = self.filter_page_ordering_rules_in_update(pages_in_update, page_ordering_rules)
            topological_indexes = self.get_topological_indexes(filtered_rules, pages_in_update)
            result += self.get_middle_page_number(self.correct_update_to_topological_order(update, topological_indexes))
        
        return result

    def process_raw_input(self, raw_input: list[str]) -> tuple[list[OrderingRule], list[Update]]:
        page_ordering_rules : list[OrderingRule] = []
        updates : list[Update] = []
        
        for line in raw_input:
            ordering_match = re.match('(\d+)\|(\d+)', line)
            if ordering_match:
                page_ordering_rules.append((int(ordering_match.group(1)), int(ordering_match.group(2))))
            elif line:
                updates.append([int(n) for n in line.split(",")])
        
        return page_ordering_rules, updates
    
    def does_update_match_page_ordering_rules(self, update: Update, page_ordering_rules: list[OrderingRule]) -> bool:
        page_number_index = {
            page_number: index
            for index, page_number in enumerate(update)
        }
        for rule in page_ordering_rules:
            if rule[0] not in page_number_index or rule[1] not in page_number_index:
                continue
            if page_number_index[rule[0]] > page_number_index[rule[1]]:
                return False
        return True
    
    def get_middle_page_number(self, update: Update) -> int:
        if len(update) % 2 == 0:
            raise ValueError("Update length must be odd")
        
        return update[len(update) // 2]
    
    def filter_page_ordering_rules_in_update(self, pages_in_update: set[int], page_ordering_rules: list[OrderingRule]) -> list[OrderingRule]:
        return [
            rule
            for rule in page_ordering_rules
            if rule[0] in pages_in_update and rule[1] in pages_in_update
        ]
    
    def get_topological_indexes(self, page_ordering_rules: list[OrderingRule], pages_to_consider: set[int]) -> dict[int, int]:
        topological_sort : list[int] = []
        indegrees = self.calculate_indegrees(page_ordering_rules, pages_to_consider)
        adjacency_lists = self.get_adjacency_lists(page_ordering_rules)

        queue : Deque[int] = collections.deque()

        for v, indegree in indegrees.items():
            if indegree == 0:
                queue.append(v)
        
        while queue:
            v = queue.popleft()
            topological_sort.append(v)
            for w in adjacency_lists[v]:
                indegrees[w] -= 1
                if indegrees[w] == 0:
                    queue.append(w)
        
        if len(topological_sort) != len(pages_to_consider):
            raise ValueError("Topological sort could not be found")

        return {
            page_number: index
            for index, page_number in enumerate(topological_sort)
        }

    def get_adjacency_lists(self, page_ordering_rules: list[OrderingRule]) -> dict[int, list[int]]:
        adjacency_lists : dict[int, list[int]] = collections.defaultdict(list)
        for v, w in page_ordering_rules:
            adjacency_lists[v].append(w)
        return adjacency_lists

    def calculate_indegrees(self, page_ordering_rules: list[OrderingRule], pages_to_consider: set[int]) -> dict[int, int]:
        indegrees = {v: 0 for v in pages_to_consider}
        for _, v in page_ordering_rules:
            indegrees[v] += 1
        return indegrees

    def correct_update_to_topological_order(self, update: Update, topological_indexes: dict[int, int]) -> Update:
        return sorted(update, key=lambda page_number: topological_indexes[page_number])