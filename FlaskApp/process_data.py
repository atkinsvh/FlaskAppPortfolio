import os
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from geopy.geocoders import OpenCage

def process_data(file_path):
    # Ensure the static directory exists
    static_dir = 'app/static'
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Read the CSV file
    data = pd.read_csv(file_path)

    # Debugging information to understand the CSV structure
    print("CSV Columns:", data.columns)

    # Check if 'Date' and 'Amount' columns exist
    if 'Date' in data.columns and 'Amount' in data.columns:
        # Assuming the CSV has 'Date' and 'Amount' columns
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date')

        # Example of processing: calculating monthly totals
        monthly_data = data.resample('M').sum()

        # Plotting the data
        plt.figure(figsize=(10, 6))
        monthly_data['Amount'].plot(kind='bar')
        plt.title('Monthly Transaction Amounts')
        plt.xlabel('Month')
        plt.ylabel('Total Amount')
        graph_path = os.path.join(static_dir, 'transactions_graph.png')
        plt.savefig(graph_path)
        plt.close()

        return graph_path
    else:
        raise KeyError("The CSV file does not contain 'Date' and 'Amount' columns.")

def generate_heatmap(file_path):
    # Ensure the static directory exists
    static_dir = 'app/static'
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    # Read the API key from the file
    with open('/home/neurolady/GeoCodingApi.txt', 'r') as file:
        api_key = file.read().strip()
    
    def get_lat_long(city, state, api_key):
        geolocator = OpenCage(api_key)
        location = geolocator.geocode(f"{city}, {state}")
        if location:
            return location.latitude, location.longitude
        else:
            return None

    # Read the CSV file
    data = pd.read_csv(file_path)
    df = pd.DataFrame(columns=['breed', 'name', 'price', 'city', 'state', 'Latitude', 'Longitude'])

    for index, row in data.iterrows():
        breed = row['breed']
        name = row['name']
        price = row['price']
        try:
            city, state = row['location'].split(',')
        except ValueError as e:
            print(f"Error splitting location '{row['location']}': {e}")
            continue

        coordinates = get_lat_long(city.strip(), state.strip(), api_key)
        if coordinates:
            df = df.append({
                'breed': breed, 'name': name, 'price': price, 
                'city': city.strip(), 'state': state.strip(), 
                'Latitude': coordinates[0], 
                'Longitude': coordinates[1]
            }, ignore_index=True)
        else:
            print(f"Could not find coordinates for '{city.strip()}, {state.strip()}'")

    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    locations = df[['Latitude', 'Longitude']].values.tolist()
    m = folium.Map(location=[40.0, -80.0], zoom_start=6)
    HeatMap(locations).add_to(m)
    map_path = os.path.join(static_dir, 'heatmap.html')
    m.save(map_path)
