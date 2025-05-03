# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor


# %%
# read input file
filepath = "space_mountain_with_holiday_weather_lag_suite.csv"
df = pd.read_csv(filepath)


# %%
# one hot encode the Day of Week column
df = pd.get_dummies(df, columns=['Day of Week']) 


# %%
# ------ SPLITTING DATASET ------
train_years = ['14', '15', '16', '17', '18', '19', '22']
dev_years = ['23']
test_years = ['24', '25']

df['Year'] = df['Date'].apply(lambda x: x.split('/')[-1])  # Extract year as a string
df = df[df['Time of Day'] >= 450]
df['Time_sq'] = df['Time of Day'] ** 2
df['Time_sin'] = np.sin(2 * np.pi * df['Time of Day'] / 1440)
df['Time_cos'] = np.cos(2 * np.pi * df['Time of Day'] / 1440)

train_df = df[df['Year'].isin(train_years)]
dev_df = df[df['Year'].isin(dev_years)]
test_df = df[df['Year'].isin(test_years)]

print("Train size:", train_df.shape)
print("Dev size:", dev_df.shape)
print("Test size:", test_df.shape)

# %%
# getting datasets
def get_X_y(dataframe):
    y = dataframe['Wait Time'].values
    X = dataframe.drop(columns=['Wait Time', 'Date', 'Time', 'Year'])
    return X, y

X_train, y_train = get_X_y(train_df)
X_dev, y_dev = get_X_y(dev_df)
X_test, y_test = get_X_y(test_df)


# %%
model = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# %%
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("XGBoost RMSE: {:.2f}".format(rmse))


# %%
errors = y_pred - y_test
plt.figure(figsize=(8, 4))
plt.hist(errors, bins=30, edgecolor='black')
plt.title("Distribution of Prediction Errors (XGBoost)")
plt.xlabel("Prediction Error (Predicted - Actual)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()



