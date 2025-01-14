from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import pandas as pd

dash.register_page(__name__, path='/artist-migration')

# TODO: create a new csv that is transformed using the following code patch and just load it here (more efficient)
df = pd.read_csv('data/artvis.csv', sep=';')
df[['e.latitude', 'e.longitude']] = df[['e.latitude', 'e.longitude']].apply(pd.to_numeric, errors='coerce')
df = df.dropna(subset=['e.latitude', 'e.longitude', 'e.startdate'])
df = df[df['e.city'] != '-']
df[['e.latitude', 'e.longitude']] = df[['e.latitude', 'e.longitude']].astype(float)

df = df[df["a.birthplace"] != df["a.deathplace"]]
df = df[(df["a.birthplace"] != "\\N") & (df["a.deathplace"] != "\\N")]
data = df.groupby(['a.birthplace', 'a.deathplace']).size().reset_index(name='count')
data = data.sort_values(by = "count", ascending = False)
print(data)

location_counts = df.groupby(['a.birthplace', 'a.deathplace']).size().reset_index(name='count')

# fig = px.scatter_mapbox(
#     location_counts, lat="e.latitude", lon="e.longitude", 
#     size="count",
#     zoom=4, height=700,
#     mapbox_style="carto-positron",
# )

fig = px.line_map(
    location_counts,
    lat = "e.latitude",
    lon = "e.longitude",
    width = "count"
)

layout = html.Div([
    # html.H3("ArtVis Map Visualization"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='map',
                figure=fig,
            ),
        ], width=7),
        dbc.Col([
            dbc.Card(id='info-card-2', style={"height": "700px", "overflowY": "auto"})  
        ], width=5)
    ], style={"height": "700"})
], className='m-3')
 
@callback(
    Output('info-card-2', 'children'),
    Input('map', 'clickData'),
)
def display_info(clickData):
    if clickData is None:
        return dbc.CardBody("Click on a marker for more information about the location.")

    lat = clickData['points'][0]['lat']
    lon = clickData['points'][0]['lon']
    
    filtered_df = df[(df['e.latitude'] == lat) & (df['e.longitude'] == lon)]
    num_artists = filtered_df.shape[0]
    city = filtered_df['e.city'].iloc[0]

    yearly_counts = filtered_df.groupby('e.startdate').size().reset_index(name='row_count')

    timeline_fig = px.line(yearly_counts, x='e.startdate', y='row_count', markers=True,
                  title=f'Number of artists that exhibited in {city} by year.',
                  labels={'e.startdate': 'Year', 'row_count': 'Artists'})
    timeline_fig.update_layout(xaxis=dict(dtick=1))
    
    venue_counts = filtered_df['e.venue'].value_counts().nlargest(5).reset_index()
    venue_counts.columns = ['Venue', 'Occurrences']  # Rename columns for clarity
    venue_counts = venue_counts.sort_values(by='Occurrences', ascending=True)
    top_venues_fig = px.bar(
        venue_counts,
        x='Occurrences',
        y='Venue',
        title='Top 10 Venues by number of Artists hosted',
        labels={'Occurrences': 'Num Artists hosted', 'Venue': 'Venue'},
        orientation='h'
    )

    top_venues_fig.update_layout(
        xaxis_title='Num Artists hosted',
        yaxis_title='Venue',
    )

    card_content = [
        dbc.CardHeader(city),
        dbc.CardBody([
            html.P(f"In total, {num_artists} exhibited in {city}"),
            dcc.Graph(figure=timeline_fig),
            dcc.Graph(figure=top_venues_fig)
        ])
    ]
    
    return card_content