from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/artist-migration')

# TODO: create a new csv that is transformed using the following code patch and just load it here (more efficient)
df = pd.read_csv('data/migration.csv')
df = df.dropna(subset=['birthLon', 'birthLat', 'deathLon', 'deathLat'])
# print(df.info())
# df[['birthLon', 'birthLat', 'deathLon', 'deathLat']] = df[['birthLon', 'birthLat', 'deathLon', 'deathLat']].apply(pd.to_numeric, errors='coerce')

# df = df[df["a.birthplace"] != df["a.deathplace"]]
# df = df[(df["a.birthplace"] != "\\N") & (df["a.deathplace"] != "\\N")]
df_one_row_per_artist =  df.drop_duplicates(subset=['a.id'])
df_grouped_by_death_birth_places = df_one_row_per_artist.groupby(['a.birthplace', 'a.deathplace', 'birthLon', 'birthLat', 'deathLon', 'deathLat']).size().reset_index(name='count')
data = df_grouped_by_death_birth_places.sort_values(by = "count", ascending = False)

# print(data)


# Create the figure
def create_figure():
    fig = go.Figure()

    for index, row in data.iterrows():
        fig.add_trace(go.Scattergeo(
            lon = [row["birthLon"], row["deathLon"]],
            lat = [row["deathLat"], row["deathLat"]],
            mode = 'lines',
            line = dict(width = row["count"], color="blue"),
            name = f"{row['a.birthplace']} to {row['a.deathplace']}"
        ))

    fig.update_layout(
        # title_text = 'World Map with Arrows',
        showlegend = False,
        geo = dict(
            projection_type = 'natural earth',
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
        width=1000,
        height=500,
    )
    
    return fig

layout = html.Div([
    # html.H3("ArtVis Map Visualization"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='map',
                figure=create_figure(),
            ),
        ], width=7),
        dbc.Col([
            dbc.Card(id='info-card-2', style={"height": "700px", "overflowY": "auto"})  
        ], width=5)
    ], style={"height": "700"})
], className='m-3')
 