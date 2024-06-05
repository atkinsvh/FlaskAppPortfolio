import os
import pandas as pd
import folium
from folium.plugins import HeatMap

def generate_heatmap(file_path):
    # Ensure the static directory exists
    static_dir = 'uploads'
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Read the CSV file
    data = pd.read_csv(file_path)

    # Check if 'latitude' and 'longitude' columns exist
    if 'latitude' in data.columns and 'longitude' in data.columns:
        df = data[['latitude', 'longitude']].dropna()

        locations = df.values.tolist()
        m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=6)
        HeatMap(locations).add_to(m)
        map_path = os.path.join(static_dir, 'heatmap.html')
        m.save(map_path)
    else:
        raise KeyError("The CSV file does not contain 'latitude' and 'longitude' columns.")
