import json
import logging

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from terraform_linter_tool.reporting.app_layout import create_sidebar
from terraform_linter_tool.reporting.callbacks import register_callbacks
from terraform_linter_tool.reporting.data_loader import \
    load_report  # Import the data loader

logger = logging.getLogger(__name__)


class DashDashboard:
    def __init__(self, report_path, base_directory, host='127.0.0.1', port=8050):
        """
        Initialize the Dash dashboard with given report and configurations.
        
        :param report_path: Path to the linting report JSON file
        :param base_directory: Base directory for the project
        :param host: Host address for the Dash server
        :param port: Port number for the Dash server
        """
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.SPACELAB],  # Use Bootstrap for theming
            suppress_callback_exceptions=True
        )
        self.base_directory = base_directory
        self.report_path = report_path
        self.linter_data = self.load_linter_data(report_path)  # Load and process report data
        self.host = host  # Customize host
        self.port = port  # Customize port

        # Build the app layout
        self.app.layout = self.create_app_layout()  # Use a new method to handle layout creation

        # Register callbacks
        register_callbacks(self.app, self.linter_data)

    def load_linter_data(self, report_path):
        """
        Load the linter data from the given report file.
        :param report_path: Path to the report JSON file
        :return: Parsed linter data as list or dict
        """
        try:
            linter_data = load_report(report_path)  # Call the function to load the report
            if not linter_data:
                logger.warning("No linting issues found in the report.")
            else:
                logger.info(f"Linter data loaded from {report_path}.")
            return linter_data
        except FileNotFoundError:
            logger.error(f"Report file not found at {report_path}. Exiting dashboard.")
            return None
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from report file: {report_path}")
            return None

    def should_run(self):
        """
        Check if the dashboard should run by verifying if there are linting issues to display.
        
        :return: True if there are linting issues, False otherwise
        """
        if isinstance(self.linter_data, list):
            return len(self.linter_data) > 0  # Return True if list contains linting issues

        if isinstance(self.linter_data, dict):
            return self.linter_data and any(self.linter_data.get("linters", {}).values())  # Check for linting issues

        return False  # Default case: no issues

    def create_app_layout(self):
        """
        Create the full layout of the app, including the sidebar and content area.
        """
        return dbc.Container([  # Use dbc.Container instead of html.Div for fluid layout
            dcc.Location(id="url"),  # Allows for navigation
            dbc.Row([
                dbc.Col(create_sidebar(self.linter_data), width=2),  # Sidebar navigation with linter data
                dbc.Col(html.Div(id="page-content"), width=10),  # Main content layout based on URL
            ])
        ], fluid=True)  # Use fluid argument for the container

    def run(self):
        """
        Run the Dash dashboard server if linting issues are found.
        """
        if not self.should_run():
            logger.info("No issues to display. Exiting dashboard.")
            return

        issue_count = len(self.linter_data) if isinstance(self.linter_data, list) else len(self.linter_data['linters'])
        logger.info(f"Starting dashboard with {issue_count} linter issues.")

        # Run the Dash server
        self.app.run_server(debug=True, host=self.host, port=self.port)