import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.components import Navbar
import sys, os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
server = app.server # when ran as a server


app.layout = html.Div(
    [
        dcc.Store(id='config-store'),
        Navbar(),
        dash.page_container
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
