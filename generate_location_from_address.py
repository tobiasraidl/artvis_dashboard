from geopy.geocoders import Nominatim
import pandas as pd

app = Nominatim(user_agent="tutorial")

df = pd.read_csv('data/artvis.csv', sep=';')
df[['e.latitude', 'e.longitude']] = df[['e.latitude', 'e.longitude']].apply(pd.to_numeric, errors='coerce')
df = df.dropna(subset=['e.latitude', 'e.longitude', 'e.startdate'])
df = df[df['e.city'] != '-']
df[['e.latitude', 'e.longitude']] = df[['e.latitude', 'e.longitude']].astype(float)
df = df[df["a.birthplace"] != df["a.deathplace"]]
df = df[(df["a.birthplace"] != "\\N") & (df["a.deathplace"] != "\\N")]

cache = {}
for i, (index, row) in enumerate(df.iterrows()):
    # Process birthplace
    birthplace = row['a.birthplace']
    if birthplace in cache:
        birth_location = cache[birthplace]
    else:
        location = app.geocode(birthplace)
        birth_location = location.raw if location else None
        cache[birthplace] = birth_location

    df.at[index, 'birthLon'] = birth_location["lon"] if birth_location else None
    df.at[index, 'birthLat'] = birth_location["lat"] if birth_location else None

    # Process deathplace
    deathplace = row['a.deathplace']
    if deathplace in cache:
        death_location = cache[deathplace]
    else:
        location = app.geocode(deathplace)
        death_location = location.raw if location else None
        cache[deathplace] = death_location

    df.at[index, 'deathLon'] = death_location["lon"] if death_location else None
    df.at[index, 'deathLat'] = death_location["lat"] if death_location else None
    
    if i == 100:
        break

df.to_csv("data/artvis_processed.csv", index=False)
