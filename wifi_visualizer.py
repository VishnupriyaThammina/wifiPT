import pandas as pd
from dash import Dash, dcc, html, dash_table
import plotly.express as px
import argparse
import sys

# Parse command line argument for CSV file
parser = argparse.ArgumentParser(description="Visualize Airodump-ng CSV output")
parser.add_argument('--csv', '-c', required=True, help='Path to the airodump-ng CSV file')
args = parser.parse_args()

CSV_FILE = args.csv

try:
    # Read CSV and find separator row (empty line)
    df = pd.read_csv(CSV_FILE, skip_blank_lines=False)
    sep_idx = df[df.isnull().all(axis=1)].index[0]

    df_aps = pd.read_csv(CSV_FILE, nrows=sep_idx)
    df_clients = pd.read_csv(CSV_FILE, skiprows=sep_idx + 2)

    df_aps.columns = df_aps.columns.str.strip()
    df_clients.columns = df_clients.columns.str.strip()
except Exception as e:
    print(f"Error reading CSV file: {e}")
    sys.exit(1)

app = Dash(__name__)
app.title = "Airodump-ng CSV Visualizer"

app.layout = html.Div([
    html.H1("Airodump-ng CSV Visualizer"),

    html.H2("Access Points"),
    dash_table.DataTable(
        data=df_aps.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_aps.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        filter_action='native',
        sort_action='native'
    ),

    dcc.Graph(
        id='ap-signal',
        figure=px.scatter(
            df_aps, x='Channel', y='Power',
            hover_data=['BSSID', 'ESSID'],
            title='Access Points: Signal Strength by Channel'
        )
    ),

    html.H2("Clients"),
    dash_table.DataTable(
        data=df_clients.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_clients.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        filter_action='native',
        sort_action='native'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
