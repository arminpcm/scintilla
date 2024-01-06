from dash import html
from dash.dependencies import Input, Output
from dash import dcc

from modules.pantheon.app import dash_app as app
from modules.pantheon.components.sidebar import sidebar
from modules.pantheon.components.menu import menu
from modules.pantheon.components.pages.activity import layout as activity_layout


pages = html.Div([
    html.Div(id='canvas-content')
], className="canvas")  # Move the entire div to the left


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

# Callback to update the canvas content dynamically
@app.callback(
    Output('canvas-content', 'children'),
    [Input('url', 'pathname')]
)
def change_page(pathname):
    if pathname == '/activity':
        return activity_layout
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
