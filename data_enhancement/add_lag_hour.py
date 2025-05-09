import pandas as pd

# Load CSV
df = pd.read_csv("space_mountain_with_holiday_weather_lag_suite.csv")

# Convert Date and Time to a single datetime column for accurate time shifting
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format="%m/%d/%y %H:%M:%S")

# Sort by datetime to ensure correct lag computation
df = df.sort_values('Datetime')

# Group by each day to avoid crossing over dates
df['Wait_Time_30min_Ago'] = df.groupby(df['Date'])['Wait Time'].shift(1)
df['Wait_Time_60min_Ago'] = df.groupby(df['Date'])['Wait Time'].shift(2)

df['Wait_Time_30min_Ago'] = df['Wait_Time_30min_Ago'].fillna(df['Lag1_Wait_Time'])
df['Wait_Time_60min_Ago'] = df['Wait_Time_60min_Ago'].fillna(df['RollingMean_Lag3'])

df = df.drop(columns=['Datetime'], errors='ignore')

# Save updated CSV
df.to_csv("space_mountain_with_holiday_weather_lag_new.csv", index=False)

print("✅ Added Wait_Time_30min_Ago and Wait_Time_60min_Ago.")
