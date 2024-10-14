import logging

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format

logger = logging.getLogger()


def create_sidebar(linter_data):
    """Create a sidebar for navigating between linters with a logo, title, and home icon."""
    enabled_linters = list(set([entry['Linter'] for entry in linter_data]))
    links = [dbc.NavLink(linter, href=f"/{linter.lower()}", active="exact") for linter in enabled_linters]

    return html.Div(
        [
            # Logo and Title Container
            html.Div(
                [
                    html.Img(src="/assets/logo.webp", className="logo", style={
                        "width": "50px",
                        "height": "50px",
                        "borderRadius": "50%",
                        "padding": "10px",
                        "backgroundColor": "#F0F4F8",
                        "boxShadow": "0px 2px 8px rgba(0, 0, 0, 0.1)"
                    }),
                    html.H2("InfraLint", className="sidebar-title", style={
                        "fontSize": "22px",
                        "fontWeight": "bold",
                        "color": "#2D3748",
                        "marginLeft": "10px",
                        "letterSpacing": "0.5px"
                    })
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "padding": "20px 0"
                }
            ),
            
            # Use the downloaded home-solid.svg for the Home icon
            html.Div(
                dbc.NavLink(
                    html.Img(src="/assets/home-solid.svg", style={
                        "width": "30px",  # Adjust the size of the icon as needed
                        "height": "30px",
                    }),  # Local SVG home icon
                    href="/",
                    className="home-link",
                    style={
                        "display": "block",
                        "textAlign": "center",
                        "marginBottom": "20px",
                        "padding": "10px"
                    }
                )
            ),
            html.Hr(),  # Horizontal line to separate home from the linter links
            
            # Navigation links for Linters
            dbc.Nav(links, vertical=True, pills=True),
        ],
        className="sidebar",  # Custom class for sidebar
    )


# Content layout
def create_content_layout():
    """Create the content area where data will be displayed."""
    return html.Div(id="page-content", className="content")


def create_app_layout(linter_data):
    return dbc.Container([
        dbc.Row([
            # Sidebar - make it collapsible and responsive
            dbc.Col(
                create_sidebar(linter_data),
                xs=12, sm=12, md=3, lg=2, className="sidebar-wrapper"
            ),
            # Content area
            dbc.Col(
                create_content_layout(),
                xs=12, sm=12, md=9, lg=10, className="content-wrapper"
            ),
        ], className="g-0"),  # Zero spacing between rows and columns
    ], fluid=True)


def render_home_page(linter_data):
    """Render a summary page with a pie chart of total issues from all linters."""
    df = pd.DataFrame(linter_data)
    issue_counts = df.groupby('Linter').size().reset_index(name='Count')

    # Create pie chart for issue distribution
    fig = px.pie(
        issue_counts,
        names='Linter',
        values='Count',
        title="Overview of Linter Issues",
        hole=0.3,  # Donut style
        color_discrete_sequence=["#1f77b4", "#2ca02c", "#ff7f0e"]
    )

    # Center the title and improve responsiveness
    fig.update_layout(
        title_x=0.5,
        title_font=dict(size=22, family="Open Sans, sans-serif", color="rgb(42, 63, 95)"),
        margin=dict(t=50),  # Adjust top margin
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5
        ),  # Make legend horizontal for smaller screens
    )

    return html.Div([
        dcc.Graph(id='pie-chart', figure=fig, style={"width": "100%", "height": "auto"}),  # Responsive width/height
        html.H2("Select a section of the chart to explore specific issues.", className="summary-text", style={
            "textAlign": "center",
            "fontSize": "18px",
            "color": "#333",
            "marginTop": "20px"
        }),
        # Footer content
        html.Footer(
            html.Div(
                [
                    html.Span("darrenrabbitt.com | All rights reserved | v1.2.5", className="footer-text")
                ],
                className="footer-container"
            ),
            style={
                "marginTop": "40px",  # Adds some spacing between the content and footer
                "padding": "10px 0",  # Padding for footer
                "backgroundColor": "#f8f9fa",  # Light background color for the footer
                "textAlign": "center",  # Center-align the footer text
                "color": "#333",  # Text color
                "fontSize": "14px"  # Font size for the footer text
            }
        )
    ])


def render_linter_page(linter_name, linter_data):
    """Render the page for a specific linter with concise table and modal for details."""
    
    # Convert linter_name to lowercase for case-insensitive comparison
    linter_name_lower = linter_name.lower()
    
    # Log the linter name and the available linters for debugging
    available_linters = [entry['Linter'].lower() for entry in linter_data]
    logger.debug(f"Requested linter: {linter_name_lower}, Available linters: {available_linters}")
    
    # Filter linter data based on the selected linter name (case-insensitive)
    filtered_data = [d for d in linter_data if d['Linter'].lower() == linter_name_lower]
    logger.debug(f"Filtered data for {linter_name_lower}: {filtered_data}")
    
    # Ensure that the filtered data has content
    if len(filtered_data) == 0:
        logger.warning(f"No data found for {linter_name_lower} in the report.")
        return html.P(f"No data for {linter_name_lower}.")

    # Create DataFrame from the filtered linter data
    df = pd.DataFrame(filtered_data)

    # Ensure that DataFrame contains the necessary columns
    if df.empty or 'Description' not in df.columns:
        logger.error(f"DataFrame for {linter_name_lower} is empty or missing critical fields.")
        return html.P(f"No data for {linter_name_lower} or missing fields in the report.")
    else:
        logger.info(f"DataFrame for {linter_name_lower} created with {len(df)} rows.")
        logger.debug(f"DataFrame contents:\n{df.head()}")

    # Fill NaN/None values to avoid rendering issues
    df = df.fillna('')

    # Convert the 'Links' column to a string or markdown
    if 'Links' in df.columns:
        df['Links'] = df['Links'].apply(lambda links: ', '.join(links) if isinstance(links, list) else str(links))

    # Sort by Severity in descending order and log the sorted DataFrame
    severity_order = {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 1}
    df['SeveritySort'] = df['Severity'].map(severity_order)
    df = df.sort_values(by='SeveritySort', ascending=False).drop(columns=['SeveritySort'])

    logger.debug(f"Sorted DataFrame for {linter_name_lower}:\n{df.head()}")

    # Define the columns without "View"
    columns = [
        {"name": "File", "id": "File"},
        {"name": "Line", "id": "Line", "type": "numeric", "format": Format(group=False)},
        {"name": "Severity", "id": "Severity"},
        {"name": "Description", "id": "Description"},
        {"name": "Links", "id": "Links"},
    ]

    # Table component without the View column and radio buttons
    table = dash_table.DataTable(
        id='linting-table',
        columns=columns,
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'left',
            'padding': '12px',
            'maxWidth': '220px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    )

    # Pie chart for issue severity distribution
    fig = px.pie(df, names='Severity', title=f'{linter_name_lower.capitalize()} Severity Distribution')

    # Modal for showing detailed description and guidelines
    modal = dbc.Modal(
        [
            dbc.ModalHeader("Details"),
            dbc.ModalBody(id="modal-body"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ml-auto", n_clicks=0)
            ),
        ],
        id="context-modal",
        size="lg",
        is_open=False,
    )

    # Log the successful rendering of the page
    logger.info(f"Rendering page for {linter_name_lower} with {len(df)} issues.")

    return html.Div([
        html.H2(f"{linter_name_lower.capitalize()} Linting Results", className="linter-header"),
        table,
        dcc.Graph(figure=fig),
        modal
    ])
