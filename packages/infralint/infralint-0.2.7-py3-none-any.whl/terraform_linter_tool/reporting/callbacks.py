import logging
import os

import dash
from dash import Input, Output, State, html

from terraform_linter_tool.reporting.app_layout import (render_home_page,
                                                        render_linter_page)

logger = logging.getLogger(__name__)


def register_callbacks(app, linter_data):
    """
    Register callbacks to handle modal functionality and dynamic content in the dashboard.
    """

    # Consolidated outputs to modal-body to avoid nonexistent object errors
    @app.callback(
        [
            Output('context-modal', 'is_open'),  # Controls if the modal is open or closed
            Output('modal-body', 'children'),  # Consolidating modal content into modal-body
            Output('linting-table', 'active_cell')  # Controls which cell in the table is active
        ],
        [
            Input('linting-table', 'active_cell'),  # Triggered when a cell is clicked in the table
            Input('close-modal', 'n_clicks')  # Triggered when the modal close button is clicked
        ],
        [
            State('linting-table', 'data'),  # Holds the data of the table to find details on the clicked row
            State('context-modal', 'is_open')  # Holds the current open/close state of the modal
        ],
        prevent_initial_call=True  # Ensure this callback does not fire when the page loads
    )
    def toggle_modal(active_cell, n_clicks_close, table_data, is_open):
        """
        Handle modal toggling and content updates based on the table's active cell and the close button.
        """
        try:
            # Log the input state at the start of the callback
            logger.info(f"toggle_modal called with active_cell={active_cell}, n_clicks_close={n_clicks_close}, is_open={is_open}")

            # Context tells us which input triggered the callback
            ctx = dash.callback_context
            logger.debug(f"callback_context: {ctx.triggered}")

            # Handle closing the modal
            if ctx.triggered and ctx.triggered[0]['prop_id'] == 'close-modal.n_clicks':
                logger.info("Modal close triggered.")
                return False, "", None  # Close the modal and reset contents

            # If a table cell is clicked, the 'active_cell' will have details about the clicked cell
            if active_cell:
                row_index = active_cell['row']  # Get the row that was clicked

                # Ensure the row index is within bounds of the table data
                if row_index < len(table_data):
                    linter_entry = table_data[row_index]  # Get the data for the clicked row
                    logger.debug(f"Linter entry selected: {linter_entry}")

                    # Extract the description, links, and context from the linter entry
                    description = linter_entry.get('Description', 'No details available.')
                    links = linter_entry.get('Links', [])

                    # Fix: Handle both single string and list of links
                    link_elements = []
                    if isinstance(links, str):  # If 'Links' is a single string
                        link_elements = [html.A(href=links, children=links, target="_blank", style={"wordWrap": "break-word", "display": "block"})]
                    elif isinstance(links, list):  # If 'Links' is a list of strings
                        link_elements = [
                            html.A(href=link, children=link, target="_blank", style={"wordWrap": "break-word", "display": "block"})
                            for link in links
                        ]
                    else:
                        # If there are no valid links, show a fallback message
                        link_elements = [html.P("No reference links available.", className="modal-no-links")]

                    # Handle special cases for Checkov linter and potential OpenAI integration
                    context = linter_entry.get('Context', '')
                    if 'Checkov' in linter_entry.get('Linter', '') and not context:
                        # Check if OpenAI API key is available in the environment
                        openai_key = os.getenv("OPENAI_API_KEY")
                        context_message = "Enable OpenAI for additional context." if not openai_key else "OpenAI context is enabled."
                        logger.info(f"OpenAI context handling: {context_message}")
                    else:
                        # Fallback if there's no specific context available
                        context_message = context if context else "No additional context available."

                    # Here is where you wrap the content into `modal_content` to pass into the modal body
                    modal_content = html.Div(
                        [
                            html.P(description, className="modal-description"),
                            html.Div(link_elements, className="modal-links"),
                            html.P(context_message, className="modal-context")
                        ],
                        className="modal-content-wrapper"  # Unique class for overall styling
                    )

                    # Open the modal and populate it with the selected row's details
                    logger.info("Opening modal with details.")
                    return True, modal_content, active_cell

                else:
                    logger.warning(f"Row index {row_index} out of bounds for table data.")

            # If no table cell is clicked or modal close is triggered, maintain the current modal state
            return is_open, "", active_cell

        except Exception as e:
            # Log any unhandled exceptions with detailed error info
            logger.error(f"An error occurred in toggle_modal: {str(e)}", exc_info=True)
            return is_open, html.P("An error occurred while fetching details.", className="error-message"), active_cell

    # Callback for pie chart clicks to update URL
    @app.callback(
        Output('url', 'pathname'),  # Output to update the URL
        [Input('pie-chart', 'clickData')]  # Input from pie chart click
    )
    def update_url_from_pie_click(click_data):
        if click_data:
            clicked_linter = click_data['points'][0]['label'].lower()
            logger.info(f"Pie chart clicked, navigating to {clicked_linter}")
            return f"/{clicked_linter}"
        return dash.no_update

    # Main page rendering based on the URL
    @app.callback(
        Output('page-content', 'children'),  # Content area where pages are rendered
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        try:
            logger.info(f"display_page called with pathname={pathname}")
            linter_name = pathname.strip("/").lower()

            available_linters = [linter.lower() for linter in set([entry['Linter'] for entry in linter_data])]
            logger.debug(f"Available linters: {available_linters}")
            if linter_name in available_linters:
                logger.info(f"Rendering page for linter: {linter_name}")
                return render_linter_page(linter_name, linter_data)

            logger.info("Rendering home page")
            return render_home_page(linter_data)

        except Exception as e:
            logger.error(f"An error occurred in display_page: {str(e)}", exc_info=True)
            return html.Div("Error occurred while rendering the page.")