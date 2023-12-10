from dash import html
import dash_core_components as dcc

PANTHEON_LOGO = "../assets/icons/pantheon.png"

search_bar = html.Div(
    [
        dcc.Input(type="search", placeholder="Search", className="search-box"),
        html.Button("Search", className="search-button", n_clicks=0),
    ],
    className="search-bar",
    style={'margin': 'auto', 'width': '25%'}  # Center the search_bar horizontally
)

menu = html.Div(
    [
        html.Div(
            [
                html.Img(src=PANTHEON_LOGO, height="45px", style={'paddingLeft': '10px'}),
            ],
            className="logo-row",
        ),
        search_bar,
    ],
    className="custom-menu",
    style={'textAlign': 'center'},  # Center the menu content
)
