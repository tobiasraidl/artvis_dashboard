import googlemaps
import pandas as pd
import csv
import time

# Initialize Google Maps client
gmaps = googlemaps.Client(key='ASK_ALEX_FOR_API_KEY')

df = pd.read_csv('data/artvis.csv', sep=';')
df[['e.latitude', 'e.longitude']] = df[['e.latitude', 'e.longitude']].apply(pd.to_numeric, errors='coerce')
df = df.dropna(subset=['e.latitude', 'e.longitude', 'e.startdate'])
df = df[df['e.city'] != '-']
df[['e.latitude', 'e.longitude']] = df[['e.latitude', 'e.longitude']].astype(float)
df = df[df["a.birthplace"] != df["a.deathplace"]]
df = df[(df["a.birthplace"] != "\\N") & (df["a.deathplace"] != "\\N")]

unique_places = set(df["a.birthplace"]) | set(df["a.deathplace"])

cache = {}
i = 1
for place in unique_places:
    print(f"Row: {i}")
    try:
        geocode_result = gmaps.geocode(place)
        cache[place] = geocode_result[0]['geometry']['location'] if geocode_result else None
    except Exception as e:
        print(f"Error geocoding {place}: {e}")
        with open("data/location_cache.csv", "w", newline="") as f:
            w = csv.DictWriter(f, cache.keys())
            w.writeheader()
            w.writerow(cache)
    i += 1
    time.sleep(0.1)  # To avoid hitting the rate limit

for index, row in df.iterrows():
    # Process birthplace
    birthplace = row['a.birthplace']
    birth_location = cache.get(birthplace)
    df.at[index, 'birthLon'] = birth_location['lng'] if birth_location else None
    df.at[index, 'birthLat'] = birth_location['lat'] if birth_location else None

    # Process deathplace
    deathplace = row['a.deathplace']
    death_location = cache.get(deathplace)
    df.at[index, 'deathLon'] = death_location['lng'] if death_location else None
    df.at[index, 'deathLat'] = death_location['lat'] if death_location else None

df.to_csv("data/artvis_processed.csv", index=False)
print("Geocoding completed and data saved.")
