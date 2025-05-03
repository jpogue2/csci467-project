import pandas as pd

# Load and parse data
df = pd.read_csv("space_mountain_with_holiday_weather_filled.csv")
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%y %H:%M:%S')
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
df['Time_Key'] = df['Time']  # to merge on time of day

# Start with Lag1, Lag2, Lag3
lags = []
for lag_day in [1, 2, 3]:
    lag_df = df[['Date', 'Time_Key', 'Wait Time']].copy()
    lag_df['Date'] = lag_df['Date'] + pd.Timedelta(days=lag_day)
    lag_df.rename(columns={'Wait Time': f'Lag{lag_day}_Wait_Time'}, inplace=True)
    df = pd.merge(df, lag_df, on=['Date', 'Time_Key'], how='left')
    lags.append(f'Lag{lag_day}_Wait_Time')

# Compute rolling mean from Lag1–Lag3
df['RollingMean_Lag3'] = df[lags].mean(axis=1)

# Drop rows with missing lag data
df.dropna(subset=lags + ['RollingMean_Lag3'], inplace=True)

# Reformat Date and cleanup
df['Date'] = df['Date'].dt.strftime('%m/%d/%y')
df.drop(columns=['Datetime', 'Time_Key'], inplace=True)

# Save to CSV
df.to_csv("space_mountain_with_holiday_weather_lag_suite.csv", index=False)
