from dash import html, dcc

PANTHEON_LOGO = "../assets/icons/pantheonlogo.png"

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
                html.Img(src=PANTHEON_LOGO, height="30px", style={'paddingLeft': '10px'}),
            ],
            className="logo-row",
        ),
        search_bar,
        dcc.Link([
            html.Img(src="../assets/icons/user.svg", className="menu-icon"),
        ], href="/user", className="menu-item"),
        dcc.Link([
            html.Img(src="../assets/icons/setting.svg", className="menu-icon"),
        ], href="/settings", className="menu-item"),    
    ],
    className="custom-menu",
    style={'textAlign': 'center'},  # Center the menu content
)
