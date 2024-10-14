import importlib.resources as resources  # Use importlib.resources for resource handling
import json
import logging
import os
import shutil
from typing import Dict

import click

from terraform_linter_tool.config import ensure_config_exists, load_config
from terraform_linter_tool.lint_factory import \
    LinterFactory  # Import the new LinterFactory
from terraform_linter_tool.reporting.dashboard import DashDashboard
from terraform_linter_tool.utils.linter_checker import check_linter_installed
from terraform_linter_tool.utils.report_generator import generate_report
from terraform_linter_tool.utils.terraform_utils import \
    validate_terraform_directory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_SOURCE = 'src/terraform_linter_tool/resources/config.yaml'
DEFAULT_CONFIG_DEST = os.path.expanduser('~/.infralint/config.yaml')


@click.group(help="""
Infralint is a tool for linting, security scanning, and reporting on infrastructure code.

Usage:

    infralint run <directory> [OPTIONS]
    infralint export-config

Commands:
    run            Run the linters on the specified directory and generate a report.
    export-config  Export the default configuration to ~/.infralint/config.yaml.

Run 'infralint run --help' for more details on the available options.
""")
def cli():
    """CLI group for Infralint."""
    pass


@cli.command(help="""
Run multiple Terraform linters and generate a report. By default, it will
launch the Dash dashboard after the report is generated.

Example:

    infralint run ./terraform_directory --output json:./reports/report.json

Options:
    directory     The path to the directory containing Terraform files.
    --config      Path to the configuration file (optional).
    --output      Specify the output format (json or html) and path (optional).
    --no-dash     Do not run the dashboard after linting.
""")
@click.argument('directory', type=click.Path(exists=True), default='.')
@click.option('--config', type=click.Path(exists=True), help="Path to the configuration file.")
@click.option('--output', type=str, help="Specify output format (json or html) and path.")
@click.option('--no-dash', is_flag=True, help="Do not run the dashboard after linting.")
def run(directory, config, output, no_dash):
    """
    Run multiple Terraform linters and generate a report. By default, it will
    launch the Dash dashboard after the report is generated.
    """

    # Ensure the config exists
    logger.debug(f"Config file path received: {config}")
    if not config:
        config = ensure_config_exists()
        logger.debug(f"Using default config: {config}")
    # Load the config data
    try:
        config_data = load_config(config)
        logger.debug(f"Config data loaded: {config_data}")
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return

    # Handle output format and path if provided
    if output:
        try:
            output_format, output_path = output.split(':')
            if validate_output_format(output_format):
                config_data['output']['format'] = output_format
                config_data['output']['save_to'] = output_path
            else:
                logger.error("Invalid output format specified.")
                return
        except ValueError:
            logger.error(f"Invalid output format argument: {output}")
            return

    # Validate and run linters
    logger.debug(f"Validating directory: {directory}")
    if not validate_terraform_directory(directory):
        logger.error(f"Invalid Terraform directory: {directory}")
        return

    logger.info(f"Validated directory: {directory}")
    report_path = run_linters_and_generate_report(config_data, directory)
    logger.info(f"Report generated at: {report_path}")

    # Only skip Dash if the user specified `--no-dash`
    if not no_dash:
        base_directory = os.path.abspath(directory)
        logger.info(f"Starting the Dash app with report from: {report_path}")
        dashboard = DashDashboard(report_path=report_path, base_directory=base_directory)
        dashboard.run()


@cli.command(help="""
Export the default configuration to ~/.infralint/config.yaml.
This command creates the necessary folder and copies the default configuration template.
""")
def export_config():
    """Export default config to ~/.infralint/config.yaml."""
    config_dir = os.path.dirname(DEFAULT_CONFIG_DEST)

    # Create the directory if it does not exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        logger.info(f"Created directory: {config_dir}")

    # Copy the default config using importlib.resources to access the resource
    if not os.path.exists(DEFAULT_CONFIG_DEST):
        try:
            # Use importlib.resources to get the path to the bundled config.yaml
            with resources.files('terraform_linter_tool.resources').joinpath('config.yaml').open('rb') as fsrc:
                with open(DEFAULT_CONFIG_DEST, 'wb') as fdst:
                    shutil.copyfileobj(fsrc, fdst)

            logger.info(f"Config file exported to: {DEFAULT_CONFIG_DEST}")
        except Exception as e:
            logger.error(f"Failed to export config file: {e}")
    else:
        logger.info(f"Config file already exists at: {DEFAULT_CONFIG_DEST}")


def validate_output_format(output_format):
    if output_format not in ['json', 'html']:
        logger.error(f"Invalid output format: {output_format}. Supported formats: json, html.")
        return False
    return True


def run_linter(linter_name, LinterClass, directory: str):
    """
    Runs the specified linter and returns raw results or error messages.
    """
    logger.debug(f"Checking if {linter_name} is installed...")
    if check_linter_installed(linter_name):
        logger.info(f"Running {linter_name} on directory: {directory}")
        linter_instance = LinterClass()
        try:
            return linter_instance.run(directory)  # Pass the correct directory path
        except Exception as e:
            logger.error(f"Failed to run {linter_name}: {e}")
            return {'error': f"Failed to run {linter_name}: {e}"}
    else:
        logger.error(f"{linter_name} is not installed.")
        return {'error': f'{linter_name} is not installed'}


def run_linters_and_generate_report(config: Dict, directory: str) -> str:
    """
    Runs all configured linters, generates, and saves reports.
    :param config: The configuration for the linters and output settings.
    :param directory: The directory to run the linters on.
    :return: The path where the report is saved.
    """
    results = {'summary': {'directory': directory, 'linted_files': 0}, 'linters': {}}

    # Calculate base directory once
    base_directory = os.path.abspath(directory)

    # Get the enabled linters dynamically from the factory
    linters = LinterFactory.get_enabled_linters(config)

    for linter_name, LinterClass, ResultModel, ProcessorClass in linters:
        logger.debug(f"Running linter {linter_name} for directory {directory}")
        raw_result = run_linter(linter_name, LinterClass, directory)

        # Log the raw result for debugging purposes
        logger.debug(f"Raw result from {linter_name}: {raw_result}")

        # If raw_result is a string, parse it as JSON
        if isinstance(raw_result, str):
            try:
                parsed_json_result = json.loads(raw_result)  # Renaming for clarity
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from {linter_name}: {e}")
                results['linters'][linter_name] = {'error': f"Failed to parse JSON: {e}"}
                continue

        # Log the parsed result for further inspection
        logger.debug(f"Parsed JSON result for {linter_name}: {parsed_json_result}")
        
        # Process the linter result using the model
        if 'error' not in parsed_json_result:
            try:
                # Validate the result model and convert it to a structured format
                parsed_result = ResultModel.from_raw_json(json.dumps(parsed_json_result))  # Using the appropriate model
                logger.debug(f"Parsed result for {linter_name}: {parsed_result}")
                # Pass base_directory if the processor needs it
                if 'base_directory' in ProcessorClass.__init__.__code__.co_varnames:
                    processor = ProcessorClass(base_directory=base_directory)
                else:
                    processor = ProcessorClass()
                # Process the result
                processed_result = processor.process_data(parsed_result.dict())
                # Save the processed result in the results dictionary
                results['linters'][linter_name] = processed_result
                results['summary']['linted_files'] += 1  # type: ignore

            except ValueError as e:
                logger.error(f"Failed to process {linter_name} output: {e}")
                results['linters'][linter_name] = {'error': f'Failed to process {linter_name} output: {e}'}
        else:
            logger.error(f"{linter_name} returned an error: {parsed_json_result['error']}")
            results['linters'][linter_name] = {'error': parsed_json_result['error']}

    # Check if results contain any linter data before generating the report
    if not results['linters']:
        logger.warning("No linter results available, skipping report generation.")
        return ""
    # Generate the report
    logger.info("Generating the report based on linter results.")
    generate_report(results, config['output'])
    # Log the final structure of the report for debugging
    logger.debug(f"Final results: {results}")
    return config['output']['save_to']  # type: ignore


# The main function, which will be called when this script is run directly
def main():
    cli()


if __name__ == "__main__":
    main()