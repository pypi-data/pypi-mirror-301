import json
import logging
import os
import shutil
import subprocess  # nosec B404 - subprocess used safely with trusted input
from typing import Dict, List

from terraform_linter_tool.linters.base_linter import BaseLinter
from terraform_linter_tool.models.checkov_model import CheckovIssue
from terraform_linter_tool.utils.linter_checker import check_linter_installed

logger = logging.getLogger(__name__)


class CheckovLinter(BaseLinter):
    def __init__(self, framework='terraform'):
        """
        Initialize CheckovLinter with a default framework, which can be overridden via config.
        :param framework: Infrastructure code framework to scan (e.g., 'terraform', 'cloudformation').
        """
        self.framework = framework

    def run(self, path):
        """
        Run Checkov on the provided directory path and return raw JSON result.

        :param path: Directory path to lint with Checkov.
        :return: Raw JSON string output from Checkov.
        """
        logger.debug(f"Received path for Checkov: {path}")

        # Ensure Checkov is installed
        if not check_linter_installed('checkov'):
            logger.error("Checkov is not installed. Please install it before running the linter.")
            return {'error': 'Checkov is not installed'}

        # Resolve the full path of the checkov executable
        checkov_path = shutil.which('checkov')
        if checkov_path is None:
            logger.error("Could not find Checkov executable in PATH.")
            return {'error': 'Checkov is not installed or not found in PATH'}

        # Ensure the path is absolute
        abs_path = os.path.abspath(path)
        logger.debug(f"Absolute path for Checkov: {abs_path}")

        # Check if the directory exists
        if not os.path.isdir(abs_path):
            logger.error(f"Provided directory does not exist: {abs_path}")
            return {'error': f'Provided directory does not exist: {abs_path}'}

        logger.info(f"Running Checkov on directory: {abs_path} with framework: {self.framework}")

        try:
            # Build the command using a list
            cmd = [checkov_path, '-d', abs_path, '--output', 'json', '--framework', self.framework]

            # Using subprocess.run safely with trusted inputs, hence suppressed with nosec
            result = subprocess.run(  # nosec B603
                cmd,
                capture_output=True, text=True, cwd=abs_path, check=False
            )

            # Handle cases where Checkov fails or returns errors
            if result.returncode != 0:
                logger.debug(f"Checkov stderr: {result.stderr}")
                if result.stdout:
                    logger.info("Checkov produced output despite the error. Returning the raw JSON output...")
                    logger.info(f"Checkov stdout: {result.stdout}")
                    return result.stdout.strip()
                else:
                    return {'error': f'Checkov failed with return code {result.returncode} and no output.'}

            output = result.stdout.strip()
            if not output:
                logger.warning(f"Checkov did not return any output for directory: {abs_path}")
                return {'error': 'No output from Checkov'}

            return output  # Return raw JSON string

        # Justify subprocess usage here; suppress Bandit warnings since input is trusted
        except subprocess.CalledProcessError as e:  # nosec
            logger.error(f"Subprocess error occurred while running Checkov: {e}")
            return {'error': f'Unexpected error: {str(e)}'}

        except Exception as e:
            logger.error(f"Unexpected error occurred while running Checkov: {e}")
            return {'error': f'Unexpected error: {str(e)}'}

    def _parse_checkov_result(self, raw_output: str) -> Dict[str, List[CheckovIssue]]:
        """
        Parse the Checkov output and convert it into a structured format.
        :param raw_output: Raw JSON string output from Checkov.
        :return: Parsed result containing failed and passed checks.
        """
        try:
            checkov_data = json.loads(raw_output)
            logger.debug(f"Parsed Checkov JSON data: {checkov_data}")

            # Extract results from the Checkov JSON output
            results = checkov_data.get('results', {})
            failed_checks = results.get('failed_checks', [])
            passed_checks = results.get('passed_checks', [])

            if not failed_checks and not passed_checks:
                logger.warning("No failed or passed checks found in Checkov output.")

            # Parse the failed and passed checks into structured CheckovIssue objects
            parsed_result = {
                "failed_checks": self._parse_checks(failed_checks, "FAILED"),
                "passed_checks": self._parse_checks(passed_checks, "PASSED"),
            }

            return parsed_result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Checkov output: {e}")
            return {"failed_checks": [], "passed_checks": []}

    def _parse_checks(self, checks: List[Dict], result: str) -> List[CheckovIssue]:
        """
        Helper method to parse Checkov checks into a list of CheckovIssue objects.
        :param checks: List of check dictionaries from the Checkov output.
        :param result: Result type ('PASSED' or 'FAILED') to associate with each check.
        :return: List of CheckovIssue objects.
        """
        parsed_issues = []
        for check in checks:
            check_id = check.get('check_id') or ""  # Ensure check_id is not None
            file_path = check.get('file_path') or ""  # Ensure file_path is not None

            # Create CheckovIssue object with validated data
            parsed_issues.append(
                CheckovIssue(
                    check_id=check_id,
                    result=result,
                    file_path=file_path,
                    severity=check.get('severity'),
                    guideline=check.get('guideline'),
                )
            )
        return parsed_issues