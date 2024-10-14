import os
from typing import Dict, List

from terraform_linter_tool.models.checkov_model import CheckovIssue
from terraform_linter_tool.processor.ai_processor import \
    AIProcessor  # Import the AIProcessor
from terraform_linter_tool.processor.lint_processor import LinterProcessor


class CheckovProcessor(LinterProcessor):
    def __init__(self):
        # Initialize AIProcessor if OpenAI key is set
        self.ai_processor = None
        if os.getenv("OPENAI_API_KEY"):
            self.ai_processor = AIProcessor()

    def process_data(self, linter_results: Dict) -> List[Dict]:
        """Process Checkov results and append AI-generated severity/context for CRITICAL or HIGH severity."""
        data = []
        for issue in linter_results.get('failed_checks', []):
            checkov_issue = CheckovIssue(
                check_id=issue.get("check_id"),
                message=issue.get("message"),
                result=issue.get("result", "FAILED"),
                file_path=issue.get("file_path"),
                line_number_start=issue.get("line_number_start"),
                line_number_end=issue.get("line_number_end"),
                severity=issue.get("severity"),
                guideline=issue.get("guideline")
            )

            # Step 1: Collect the initial linter result
            issue_data = {
                'Linter': 'Checkov',
                'File': checkov_issue.file_path,
                'Line': checkov_issue.line_number_start,
                'Description': checkov_issue.message,
                'Severity': checkov_issue.severity.upper() if checkov_issue.severity else "UNKNOWN",
                'Context': "",  # Context to be potentially updated by AIProcessor
                'Links': [checkov_issue.guideline] if checkov_issue.guideline else []
            }

            # Step 2: Use AIProcessor to update severity and context if applicable
            if self.ai_processor:
                issue_data = self.ai_processor.process_linter_issue(issue_data)

            # Step 3: Append the processed data to the list
            data.append(issue_data)

        return data
