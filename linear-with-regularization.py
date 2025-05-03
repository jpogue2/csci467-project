# %%
import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import math
import random 
from sklearn.linear_model import Ridge, Lasso

# %%
# Load dataset
df = pd.read_csv("space_mountain_with_holiday_weather_lag_new.csv")

# One-hot encode categorical features
df = pd.get_dummies(df, columns=['Day of Week']) 

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

# getting datasets
def get_X_y(dataframe):
    y = dataframe['Wait Time'].values
    X = dataframe.drop(columns=['Wait Time', 'Date', 'Time', 'Year'])
    return X, y

X_train, y_train = get_X_y(train_df)
X_dev, y_dev = get_X_y(dev_df)
X_test, y_test = get_X_y(test_df)

# %%
ridge = Ridge(alpha=1.0)
lasso = Lasso(alpha=1.0, max_iter=10000)

ridge.fit(X_train, y_train)
lasso.fit(X_train, y_train)

# Predictions
ridge_pred = ridge.predict(X_test)
lasso_pred = lasso.predict(X_test)

# RMSE
ridge_rmse = np.sqrt(mean_squared_error(y_test, ridge_pred))
lasso_rmse = np.sqrt(mean_squared_error(y_test, lasso_pred))

print(f"Ridge RMSE: {ridge_rmse:.2f}")
print(f"Lasso RMSE: {lasso_rmse:.2f}")

# %%
print("Ridge RMSE by alpha:")
for alpha in [0.01, 0.1, 1.0, 10.0, 100.0]:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train, y_train)
    pred = ridge.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    print(f"  alpha={alpha:<6}: RMSE = {rmse:.2f}")

# %%
print("Lasso RMSE by alpha:")
for alpha in [0.01, 0.1, 1.0, 10.0]:
    lasso = Lasso(alpha=alpha, max_iter=10000)
    lasso.fit(X_train, y_train)
    pred = lasso.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    print(f"  alpha={alpha:<6}: RMSE = {rmse:.2f}")

# %%
lasso_best = Lasso(alpha=1.0, max_iter=10000)
lasso_best.fit(X_train, y_train)

# Display non-zero feature coefficients
coef_df = pd.DataFrame({
    "Feature": X_train.columns,
    "Coefficient": lasso_best.coef_
})
print(coef_df[coef_df["Coefficient"] != 0].sort_values(by="Coefficient", key=abs, ascending=False))



