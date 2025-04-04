import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import math

# parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("--file", dest = 'filepath', type=str, required=True, help="Path to the input file (csv)")
args = parser.parse_args()

# read input file
filepath = args.filepath
df = pd.read_csv(filepath)

# ------ SPLITTING DATASET ------
# train on 2014 (December), 2015, 2016, 2017, 2018, 2019, 2022 (excluding COVID years)
# test on 2023, 2024, 2025 (January - March)
train_years = ['14', '15', '16', '17', '18', '19', '22']
test_years = ['23', '24', '25']

df['Year'] = df['Date'].apply(lambda x: x.split('/')[-1])  # Extract year as a string
train_df = df[df['Year'].isin(train_years)]  # Filter rows where Year is in train_years
test_df = df[df['Year'].isin(test_years)]  # Filter rows where Year is in train_years

print("Train set shape: {}".format(train_df.shape))
print("Test set shape: {}".format(test_df.shape))

# ------ TRAINING ------
# getting unique day and time values for training model
week_day_list = np.unique(train_df['Day of Week'])
time_list = np.unique(train_df['Time of Day'])

# getting averages across time of day per week day
avg_vals = {}
for day in week_day_list:
    for time in time_list:
        avg = (train_df[(train_df['Day of Week'] == day) & (train_df['Time of Day'] == time)]['Wait Time'].mean())
        avg_vals[(day, time)] = avg

# removing NaN values
avg_vals = {k: int(v) for k, v in avg_vals.items() if not math.isnan(v)}

print("Training completed.")
# plotting results of training statistical model
# TODO: add titles and fix graph
plt.bar(range(len(avg_vals)), list(avg_vals.values()), align='center')
plt.xticks(range(len(avg_vals)), list(avg_vals.keys()))
plt.show()

# ------ TESTING ------
# getting the actual values for the test set
y_test_actual = test_df['Wait Time'].values
y_pred = []

for index, row in test_df.iterrows():
    day = row['Day of Week']
    time = row['Time of Day']
    if (day, time) in avg_vals:
        # if the day and time is in the training set, use the average value
        y_pred.append(avg_vals[(day, time)])
    else:
        y_pred.append(np.nan)

# replacing nan values with mean of the training set
y_pred = [int(x) if not math.isnan(x) else int(np.mean(list(avg_vals.values()))) for x in y_pred]

# # calculating RMSE
rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred))
print("RMSE: {}".format(rmse))

# plotting results of testing statistical model
plt.plot(y_test_actual, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.title('Statistical Model Predictions vs Actual')
plt.xlabel('Time')
plt.ylabel('Wait Time')
plt.legend()
plt.show()
