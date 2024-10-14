import json
import logging
from typing import List, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CheckovIssue(BaseModel):
    check_id: str
    file_path: str
    message: str = 'No message available'
    severity: Optional[str] = None
    guideline: Optional[str] = None
    result: str  # PASSED or FAILED
    line_number_start: Optional[int] = None
    line_number_end: Optional[int] = None

    def __repr__(self):
        """Custom repr method to display issue details."""
        severity_display = self.severity if self.severity else 'None'
        guideline_display = self.guideline if self.guideline else 'None'
        return (
            f"CheckovIssue(\n"
            f"  check_id='{self.check_id}',\n"
            f"  file_path='{self.file_path}',\n"
            f"  message='{self.message}',\n"
            f"  severity='{severity_display}',\n"
            f"  guideline='{guideline_display}',\n"
            f"  result='{self.result}',\n"
            f"  line_number_start={self.line_number_start},\n"
            f"  line_number_end={self.line_number_end}\n"
            f")"
        )


class CheckovSummary(BaseModel):
    passed: int
    failed: int
    skipped: int
    parsing_errors: int
    resource_count: int
    checkov_version: str


class CheckovResult(BaseModel):
    summary: Optional[CheckovSummary]
    failed_checks: List[CheckovIssue] = []
    passed_checks: List[CheckovIssue] = []

    @classmethod
    def from_raw_json(cls, raw_json):
        """
        Factory method to parse the relevant fields from the Checkov JSON.
        This focuses on failed and passed checks and includes summary data.
        """
        try:
            parsed_json = json.loads(raw_json)

            # Parse the failed and passed checks within the JSON structure
            failed_checks = cls._parse_checks(parsed_json.get('results', {}).get('failed_checks', []), "FAILED")
            passed_checks = cls._parse_checks(parsed_json.get('results', {}).get('passed_checks', []), "PASSED")

            # Parse summary details if available
            summary_data = parsed_json.get('summary', None)
            if summary_data:
                summary = CheckovSummary(**summary_data)
            else:
                summary = None

            return cls(
                failed_checks=failed_checks,
                passed_checks=passed_checks,
                summary=summary
            )

        except Exception as e:
            logger.error(f"Error parsing Checkov JSON: {e}")
            raise ValueError(f"Invalid Checkov result format: {e}")

    @staticmethod
    def _parse_checks(checks, result_type):
        """Helper method to parse passed or failed checks."""
        parsed_checks = []
        for check in checks:
            parsed_checks.append(CheckovIssue(
                check_id=check['check_id'],
                file_path=check['file_path'],
                message=check.get('check_name', 'No message available'),
                severity=check.get('severity'),
                guideline=check.get('guideline'),
                result=result_type,
                line_number_start=check.get('file_line_range', [None, None])[0],
                line_number_end=check.get('file_line_range', [None, None])[1]
            ))
        return parsed_checks

    def __repr__(self):
        """Custom repr method to display CheckovResult summary."""
        failed_checks_repr = "\n".join([repr(check) for check in self.failed_checks])
        passed_checks_repr = "\n".join([repr(check) for check in self.passed_checks])

        return (
            f"CheckovResult(\n"
            f"  Summary: {self.summary}\n"
            f"  Passed Checks: {len(self.passed_checks)}\n"
            f"  Failed Checks: {len(self.failed_checks)}\n"
            f"  Details of passed checks:\n{passed_checks_repr}\n"
            f"  Details of failed checks:\n{failed_checks_repr}\n"
            f")"
        )
