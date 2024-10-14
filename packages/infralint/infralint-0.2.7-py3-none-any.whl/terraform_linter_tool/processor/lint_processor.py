from abc import ABC, abstractmethod
from typing import Dict, List


class LinterProcessor(ABC):
    def __init__(self):
        self.linter_data = []

    @abstractmethod
    def process_data(self, linter_results: Dict) -> List[Dict]:
        """Process linter data and return the formatted result."""
        pass
