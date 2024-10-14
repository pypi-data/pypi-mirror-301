# linter_factory.py
from typing import Dict, Tuple, Type

# Import your linters, models, and processors
from terraform_linter_tool.linters.checkov import CheckovLinter
from terraform_linter_tool.linters.tflint import TFLintLinter
from terraform_linter_tool.linters.tfsec import TFSecLinter
from terraform_linter_tool.models.checkov_model import CheckovResult
from terraform_linter_tool.models.tflint_model import TFLintResult
from terraform_linter_tool.models.tfsec_model import TFSecReport
from terraform_linter_tool.processor.checkov_processor import CheckovProcessor
from terraform_linter_tool.processor.tflint_processor import TFLintProcessor
from terraform_linter_tool.processor.tfsec_processor import TFSecProcessor


class LinterFactory:
    """
    Factory class to dynamically return the appropriate Linter, Model, and Processor
    based on configuration.
    """

    # Define a mapping between linter names and their classes
    LINTER_MAP: Dict[str, Tuple[Type, Type, Type]] = {
        'tflint': (TFLintLinter, TFLintResult, TFLintProcessor),
        'tfsec': (TFSecLinter, TFSecReport, TFSecProcessor),
        'checkov': (CheckovLinter, CheckovResult, CheckovProcessor)
    }

    @staticmethod
    def get_enabled_linters(config: Dict) -> list:
        """
        Dynamically get the list of enabled linters based on the config.
        :param config: The configuration dictionary.
        :return: A list of tuples containing the linter name, LinterClass, ResultModel, and ProcessorClass.
        """
        enabled_linters = []
        for linter_name, (LinterClass, ResultModel, ProcessorClass) in LinterFactory.LINTER_MAP.items():
            if config['linters'].get(linter_name, {}).get('enabled', False):
                enabled_linters.append((linter_name, LinterClass, ResultModel, ProcessorClass))
        return enabled_linters
