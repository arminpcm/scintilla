from dash import html, dcc

# Define the sidebar component with icons
sidebar = html.Div([
    dcc.Link([
        html.Img(src="../assets/icons/activity.svg", className="sidebar-icon"),
    ], href="/activity", className="sidebar-item"),
    dcc.Link([
        html.Img(src="../assets/icons/event.svg", className="sidebar-icon"),
    ], href="/events", className="sidebar-item"),
    dcc.Link([
        html.Img(src="../assets/icons/log.svg", className="sidebar-icon"),
    ], href="/logs", className="sidebar-item"),
    dcc.Link([
        html.Img(src="../assets/icons/map.svg", className="sidebar-icon"),
    ], href="/maps", className="sidebar-item"),
    dcc.Link([
        html.Img(src="../assets/icons/dataset.svg", className="sidebar-icon"),
    ], href="/datasets", className="sidebar-item"),
], className="sidebar")
