from dash import html, dcc

# Define the sidebar component with icons
sidebar = html.Div([
    dcc.Link([
        html.Img(src="../assets/icons/dashboard.png", className="icon-image"),
    ], href="/dashboard", className="sidebar-item"),
    dcc.Link([
        html.Img(src="../assets/icons/search.png", className="icon-image"),
    ], href="/search", className="sidebar-item"),
    dcc.Link([
        html.Img(src="../assets/icons/settings.png", className="icon-image"),
    ], href="/settings", className="sidebar-item"),
    html.Hr(),  # Horizontal line for separation
    # Add additional sidebar items as needed
], className="sidebar")
