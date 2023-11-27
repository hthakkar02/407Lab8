import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Read the CSV file into a DataFrame
df = pd.read_csv('../lab8-dataset/WALKING_AND_TURNING.csv', header=0,
                 usecols=["timestamp", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z", "mag_x", "mag_y",
                          "mag_z"])

print(df)
columns_to_smooth = ["accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z", "mag_x", "mag_y", "mag_z"]
for column in columns_to_smooth:
    df[column + "_smoothed"] = df[column].rolling(window=20, min_periods=1).mean()

plt.figure(figsize=(12, 6))

# Unsmoothed data
# plt.plot(df['gyro_x'], label='gyro_x (Unsmoothed)')
plt.plot(df['gyro_y'], label='gyro_y (Unsmoothed)')
plt.plot(df['gyro_z'], label='gyro_z (Unsmoothed)')

# plt.plot(df['gyro_x_smoothed'], label='gyro_x (Smoothed)')
plt.plot(df['gyro_y_smoothed'], label='gyro_y (Smoothed)')
plt.plot(df['gyro_z_smoothed'], label='gyro_z (Smoothed)')

plt.xlabel('Timestamp')
plt.ylabel('Gyroscope')
plt.title('Gyroscope Data')
plt.legend()
plt.savefig('gyroscope_plot.png')
