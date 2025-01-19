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
# print(df_one_row_per_artist)
df_grouped_by_death_birth_places = df_one_row_per_artist.groupby(['a.birthplace', 'a.deathplace', 'birthLon', 'birthLat', 'deathLon', 'deathLat']).size().reset_index(name='count')
artist_migration_grouped_with_counts = df_grouped_by_death_birth_places.sort_values(by = "count", ascending = False)

# print(data)


# Create the figure
def create_figure(data):
    fig = go.Figure()

    for index, row in data.iterrows():
        fig.add_trace(go.Scattergeo(
            lon = [row["birthLon"], row["deathLon"]],
            lat = [row["birthLat"], row["deathLat"]],
            mode = 'lines',
            line = dict(width = row["count"] * 3, color = '#354a6e'),
            opacity = 0.3,
            text = f"{row['a.birthplace']} to {row['a.deathplace']}",
            hoverinfo="text"
        ))

        fig.add_trace(go.Scattergeo(
            lon=[row["deathLon"]],
            lat=[row["deathLat"]],
            mode='markers',
            marker=dict(
                size=7, 
                color='#3dba4b',
                opacity=0.8,
                symbol='circle'
            ),
            hoverinfo="skip"
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
        width=1900,
        height=700,
    )
    
    return fig

layout = html.Div([
    # html.H3("ArtVis Map Visualization"),
    dbc.Row([
            html.Label('Set the year an artist needs to have been alive to be displayed:'),
            dcc.Slider(1700, 2000, 25, value=1825, id='slider', marks={year: str(year) for year in range(1700, 2001, 25)}),
            dbc.Spinner(dcc.Graph(
                id='map',
                figure={},
            )),
    ], style={"height": "700"}, className="justify-content-center")
], className='m-3')
 
 
@callback(
    Output('map', 'figure'),
    Input('slider', 'value'))
def update_output(value):
    filtered_df = df_one_row_per_artist[(df_one_row_per_artist['birthyear'] <= value) & 
                 ((df_one_row_per_artist['deathyear'].isna()) | (df_one_row_per_artist['deathyear'] >= value))]
    
    filtered_grouped_df = filtered_df.groupby(['a.birthplace', 'a.deathplace', 'birthLon', 'birthLat', 'deathLon', 'deathLat']).size().reset_index(name='count')
    # artist_migration_grouped_with_counts = filtered_grouped_df.sort_values(by = "count", ascending = False)
    
    fig = create_figure(filtered_grouped_df)
    return fig