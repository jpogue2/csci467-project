import pandas as pd
import requests
from datetime import datetime
from tqdm import tqdm  # Add tqdm for progress bar

# Coordinates for Disneyland
LAT = 33.8121
LON = -117.9190
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Load your CSV
df = pd.read_csv("space_mountain_with_holiday_small.csv")
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%y %H:%M:%S')

# Extract unique dates for batching
df['DateOnly'] = df['Datetime'].dt.date
unique_dates = df['DateOnly'].unique()

# Dictionary to hold fetched weather data
weather_data = {}

# Fetch hourly weather for each date (with progress bar)
for date in tqdm(unique_dates, desc="Fetching weather data"):
    start = date.strftime("%Y-%m-%d")
    url = f"{BASE_URL}?latitude={LAT}&longitude={LON}&start_date={start}&end_date={start}&hourly=temperature_2m,precipitation&timezone=America%2FLos_Angeles"
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        hours = json_data['hourly']['time']
        temps = json_data['hourly']['temperature_2m']
        precs = json_data['hourly']['precipitation']
        for t, temp, prec in zip(hours, temps, precs):
            timestamp = datetime.fromisoformat(t)
            weather_data[timestamp] = {'Temperature': temp, 'Precipitation': prec}
    else:
        print(f"Failed to fetch weather for {start}")

# Add weather columns
df['Temperature'] = df['Datetime'].map(lambda dt: weather_data.get(dt, {}).get('Temperature'))
df['Precipitation'] = df['Datetime'].map(lambda dt: weather_data.get(dt, {}).get('Precipitation'))

# Save the augmented file
df.drop(columns=['DateOnly', 'Datetime'], inplace=True)
df.to_csv("space_mountain_with_holiday_weather_small.csv", index=False)
