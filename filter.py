
import pandas as pd
import numpy as np

# Load full lag feature dataset
df = pd.read_csv("space_mountain_with_holiday_weather_lag_suite.csv")

# One-hot encode Day of Week
df = pd.get_dummies(df, columns=['Day of Week'], drop_first=True)

# Extract year
df['Year'] = df['Date'].apply(lambda x: x.split('/')[-1])

# Filter to entries after park opens
df = df[df['Time of Day'] >= 450]

# Select top features based on previous Lasso results
top_features = ['Date', 'Time', 'Wait Time', 'Year',
                'Lag1_Wait_Time', 'Lag2_Wait_Time', 'Temperature',
                'Month', 'Time of Day', 'Day of Week_Saturday']

# Drop unused columns and keep only selected
df_simplified = df[top_features]

# Save to CSV
df_simplified.to_csv("space_mountain_simplified.csv", index=False)

print("Saved simplified dataset to space_mountain_simplified.csv")
