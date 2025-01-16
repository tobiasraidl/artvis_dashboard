import pandas as pd

df = pd.read_csv('data/artvis_processed.csv')
df = df.dropna(subset=['birthLon', 'birthLat', 'deathLon', 'deathLat'])
df.to_csv('data/preprocess_artvis_processed.csv', index=False)
