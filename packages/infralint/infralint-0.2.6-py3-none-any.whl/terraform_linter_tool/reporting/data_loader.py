# data_loader.py
import json
import logging

logger = logging.getLogger()


def load_report(report_path):
    """Load the linting report data from the report path."""
    linter_data = []
    try:
        with open(report_path, 'r') as file:
            report = json.load(file)
            for linter_name, linter_results in report.get('linters', {}).items():
                for issue in linter_results:
                    linter_data.append(issue)
        if not linter_data:
            logger.info("No linting issues found in the report.")
        logger.info(f"Linter data loaded: {linter_data[:5]}")  # Log the first 5 entries of the linter data
    except FileNotFoundError:
        logger.error(f"Report file not found at: {report_path}")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from report file: {report_path}")
    return linter_data