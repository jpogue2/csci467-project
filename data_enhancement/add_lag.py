import pandas as pd

# Load and parse data
df = pd.read_csv("space_mountain_with_holiday_weather_filled.csv")
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%y %H:%M:%S')
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')

# Create a unique key for merging: just the time component
df['Time_Key'] = df['Time']

# Create a shifted version of the DataFrame by 1 day
df_lag = df[['Date', 'Time_Key', 'Wait Time']].copy()
df_lag['Date'] = df_lag['Date'] + pd.Timedelta(days=1)  # Shift forward one day
df_lag.rename(columns={'Wait Time': 'Lag_Wait_Time'}, inplace=True)

# Merge lagged wait time into original dataframe
df = pd.merge(df, df_lag, on=['Date', 'Time_Key'], how='left')

# Drop rows where lag is not available (i.e., no data for same time previous day)
df.dropna(subset=['Lag_Wait_Time'], inplace=True)

# Format Date column back to MM/DD/YY
df['Date'] = df['Date'].dt.strftime('%m/%d/%y')

# Save to CSV
df.drop(columns=['Datetime', 'Time_Key'], inplace=True)
df.to_csv("space_mountain_with_holiday_weather_lag.csv", index=False)
