import pandas as pd

# Load the original CSV
df = pd.read_csv("space_mountain_with_holiday_weather.csv")

# Parse Date and Datetime columns
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%y %H:%M:%S')
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')

# Forward and backward fill temperature and precipitation within each day
df['Temperature'] = df.groupby(df['Date'])['Temperature'].transform(lambda x: x.ffill().bfill())
df['Precipitation'] = df.groupby(df['Date'])['Precipitation'].transform(lambda x: x.ffill().bfill())

# Add flag for originally missing weather data
df['Weather_Missing'] = df[['Temperature', 'Precipitation']].isna().any(axis=1).astype(int)

# Drop rows where weather is still missing
df.dropna(subset=['Temperature', 'Precipitation'], inplace=True)

# Convert Date back to MM/DD/YY format for consistency
df['Date'] = df['Date'].dt.strftime('%m/%d/%y')

df.drop(columns=['Datetime', 'Weather_Missing'], inplace=True)

# Save to new CSV
df.to_csv("space_mountain_with_holiday_weather_filled.csv", index=False)
