import pandas as pd
import holidays

# Load CSV
df = pd.read_csv("space_mountain.csv")

# Convert to datetime
df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%y")

# Generate US holidays from 2014–2025
us_holidays = holidays.US(years=range(2014, 2026))
holiday_dates = set(us_holidays.keys())

# Add Is_Holiday using .dt.date
df['Is_Holiday'] = df['Date'].dt.date.isin(holiday_dates)

# Add Is_Holiday_Adjacency (day before or after a holiday)
adjacent_dates = set()
for h in holiday_dates:
    adjacent_dates.add(h - pd.Timedelta(days=1))
    adjacent_dates.add(h + pd.Timedelta(days=1))

adjacent_only = adjacent_dates - holiday_dates
df['Is_Holiday_Adjacency'] = df['Date'].dt.date.isin(adjacent_only)

# Reformat Date column to MM/DD/YY
df['Date'] = df['Date'].dt.strftime("%m/%d/%y")

# Save updated CSV
df.to_csv("space_mountain_with_holiday.csv", index=False)

print("✅ Added 'Is_Holiday' and 'Is_Holiday_Adjacency' columns with MM/DD/YY date formatting.")
