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
    if pathname == '/dashboard':
        return html.Div("Dashboard Page")
    elif pathname == '/search':
        return html.Div("Search Page")
    elif pathname == '/settings':
        return html.Div("Settings Page")
    else:
        return "Page not found"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
