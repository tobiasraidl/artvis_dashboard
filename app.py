import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# TODO: create a new csv that is transformed using the following code patch and just load it here (more efficient)
df = pd.read_csv('data/artvis.csv', sep=';')
df[['e.latitude', 'e.longitude']] = df[['e.latitude', 'e.longitude']].apply(pd.to_numeric, errors='coerce')
df = df.dropna(subset=['e.latitude', 'e.longitude', 'e.startdate'])
df = df[df['e.city'] != '-']
df[['e.latitude', 'e.longitude']] = df[['e.latitude', 'e.longitude']].astype(float)

location_counts = df.groupby(['e.latitude', 'e.longitude']).size().reset_index(name='count')

fig = px.scatter_mapbox(
    location_counts, lat="e.latitude", lon="e.longitude", 
    size="count",
    zoom=4, height=600,
    mapbox_style="carto-positron",
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("ArtVis Map Visualization"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='map',
                figure=fig
            ),
        ], width=6),
        dbc.Col([
            dbc.Card(id='info-card', style={'height': '100%'})  
        ], width=6)
    ])
], className='m-3')

@app.callback(
    Output('info-card', 'children'),
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

if __name__ == '__main__':
    app.run_server(debug=True)
