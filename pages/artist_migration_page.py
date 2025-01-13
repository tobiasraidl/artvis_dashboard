from dash import html, dcc
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/artist-migration')

layout = dbc.Container([
    html.H3("Test Artist Migration Page")
])