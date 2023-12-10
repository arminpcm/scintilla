import dash
from dash import html
from dash.dependencies import Input, Output
from dash import dcc

import dash_bootstrap_components as dbc  # Import Dash Bootstrap Components

from components.sidebar import sidebar
from components.menu import menu
from components.pages import pages

# Choose a dark blue theme
external_stylesheets = [dbc.themes.SLATE]  # Change to your preferred theme

# Initialize the Dash app with the chosen theme and Bootstrap CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, *external_stylesheets])

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Capture and parse URL
    html.Div([
        menu,
        html.Div([
            html.Div(sidebar, style={'flex': '0 0 auto'}),  # Make sidebar stick to the left
            html.Div(pages, id='pages'),
        ], style={'display': 'flex'}),
    ]),
])

# Callback to update the tab content dynamically
@app.callback(
    Output('tab-content', 'children'),
    [Input('url', 'pathname')]
)
def update_tab(pathname):
    if pathname == '/activity':
        return html.Div("Activity Page")
    elif pathname == '/events':
        return html.Div("Events Page")
    elif pathname == '/logs':
        return html.Div("Logs Page")
    elif pathname == '/maps':
        return html.Div("Maps Page")
    elif pathname == '/datasets':
        return html.Div("Datasets Page")
    else:
        return "Page not found"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
