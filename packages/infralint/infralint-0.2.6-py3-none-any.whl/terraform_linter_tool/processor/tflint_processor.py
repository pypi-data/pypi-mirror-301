from typing import Dict, List

from terraform_linter_tool.models.tflint_model import TFLintIssue
from terraform_linter_tool.processor.lint_processor import LinterProcessor


class TFLintProcessor(LinterProcessor):
    def process_data(self, linter_results: Dict) -> List[Dict]:
        """Process TFLint results and append to linter_data."""
        data = []
        for issue in linter_results.get('issues', []):
            tflint_issue = TFLintIssue.parse_obj(issue)
            data.append({
                'Linter': 'TFLint',
                'File': tflint_issue.get_file_path(),
                'Line': tflint_issue.range.start['line'],
                'Description': tflint_issue.message,
                'Severity': tflint_issue.rule.severity.upper(),
                'Links': [tflint_issue.rule.link] if tflint_issue.rule.link else []
            })
        return data
