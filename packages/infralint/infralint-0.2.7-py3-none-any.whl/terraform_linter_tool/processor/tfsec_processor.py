from typing import Dict, List

from terraform_linter_tool.models.tfsec_model import TFSecResult
from terraform_linter_tool.processor.lint_processor import LinterProcessor

# terraform_linter_tool/processor/tfsec_processor.py


class TFSecProcessor(LinterProcessor):
    def __init__(self, base_directory=None):
        self.base_directory = base_directory

    def process_data(self, linter_results: Dict) -> List[Dict]:
        """Process TFSec results and append to linter_data."""
        data = []
        for result in linter_results.get('results', []):
            tfsec_result = TFSecResult.parse_obj(result)
            data.append({
                'Linter': 'TFSec',
                'File': tfsec_result.get_file_path(self.base_directory),
                'Line': tfsec_result.location.start_line,
                'Description': tfsec_result.rule_description,
                'Severity': tfsec_result.severity.upper(),
                'Links': tfsec_result.links
            })
        return data
