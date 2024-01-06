import dash

import dash_bootstrap_components as dbc  # Import Dash Bootstrap Components

# Choose a dark blue theme
external_stylesheets = ["../assets/style.css"]  # Change to your preferred theme

# Initialize the Dash app with the chosen theme and Bootstrap CSS
dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, *external_stylesheets], suppress_callback_exceptions=True)
