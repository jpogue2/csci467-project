import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import math
from sklearn.linear_model import LinearRegression
import random 

# parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("--file", dest = 'filepath', type=str, required=True, help="Path to the input file (csv)")
args = parser.parse_args()

# read input file
filepath = args.filepath
df = pd.read_csv(filepath)

# one hot encode the Day of Week column
# drop_first=True is used to avoid multicollinearity (dummy variable trap)
df = pd.get_dummies(df, columns=['Day of Week'], drop_first=True) 

# ------ SPLITTING DATASET ------
# train on 2014 (December), 2015, 2016, 2017, 2018, 2019, 2022 (excluding COVID years)
# validation on 2023
# test on 2024, 2025 (January - March)
# years = ['15', '16', '17', '18', '19', '22', '23', '24']
# train_years = random.sample(years, 6)
# train_years.append('14')
# test_years = [item for item in years if item not in train_years]
# test_years.append('25')

train_years = ['14', '15', '16', '17', '18', '19', '22']
test_years = ['23', '24', '25']

df['Year'] = df['Date'].apply(lambda x: x.split('/')[-1])  # extract year as a string
train_df = df[df['Year'].isin(train_years)]
test_df = df[df['Year'].isin(test_years)]

print("Train set shape: {}".format(train_df.shape))
print("Test set shape: {}".format(test_df.shape))

# getting datasets
y_train = train_df['Wait Time'].values
X_train = train_df.drop(columns=['Wait Time', 'Date', 'Time', 'Year'])
y_test = test_df['Wait Time'].values
X_test = test_df.drop(columns=['Wait Time', 'Date', 'Time', 'Year'])

# print(X_train.columns)


# create linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("RMSE: {}".format(rmse))

# ------ PLOTTING ------
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.show()
