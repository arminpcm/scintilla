from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime

from modules.pantheon.app import dash_app as app

# Read the parquet file
df = pd.read_parquet("data/logs/extracted/manifest.parquet")

# Convert nanoseconds since epoch to datetime
df['start_time'] = pd.to_datetime(df['start_time'], unit='ns')

# Define the color dictionary
colors = {
    'background': 'rgb(22, 63, 83)',
    'text': 'rgb(154, 154, 154)'
}

# Layout of the app
layout = html.Div([
    dcc.Graph(id='line-chart'),
    # dash_table.DataTable(
    #     id='data-table',
    #     columns=[{'name': col, 'id': col} for col in df.columns],
    #     data=df.to_dict('records'),
    # )
])

# Callback to update the line chart based on user interactions
@app.callback(
    Output('line-chart', 'figure'),
    [Input('line-chart', 'relayoutData')]
)
def update_chart(relayout_data):
    # Check if the user has zoomed in
    # Reload the manifest
    df = pd.read_parquet("data/logs/extracted/manifest.parquet")
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ns')

    if relayout_data and 'xaxis.range[0]' in relayout_data:
        print(relayout_data['xaxis.range[0]'])
        start_date = pd.to_datetime(relayout_data['xaxis.range[0]'])
        end_date = pd.to_datetime(relayout_data['xaxis.range[1]'])

        # Filter the data based on the selected date range
        filtered_df = df[(df['start_time'] >= start_date) & (df['start_time'] <= end_date)]

        # Group by day and count the number of logs
        grouped_df = filtered_df.groupby(filtered_df['start_time'].dt.date).size().reset_index(name='log_count')

        # Create a line chart
        figure = {
            'data': [
                {'x': grouped_df['start_time'], 'y': grouped_df['log_count'], 'type': 'line', 'name': 'Logs'},
            ],
            'layout': {
                'title': 'Logs Over Time',
                'xaxis': {
                    'title': 'Date',
                },
                'yaxis': {
                    'title': 'Number of Logs',
                },
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            },
        }
    else:
        # If no zoom, show the entire dataset
        grouped_df = df.groupby(df['start_time'].dt.date).size().reset_index(name='log_count')

        figure = {
            'data': [
                {'x': grouped_df['start_time'], 'y': grouped_df['log_count'], 'type': 'line', 'name': 'Logs'},
            ],
            'layout': {
                'title': 'Logs Over Time',
                'xaxis': {
                    'title': 'Date',
                },
                'yaxis': {
                    'title': 'Number of Logs',
                },
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            },
        }

    return figure
