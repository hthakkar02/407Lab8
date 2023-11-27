import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# read in cols
columns_to_use = ['timestamp', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z']
data = pd.read_csv('../lab8-dataset/TURNING.csv', header=0, usecols=columns_to_use)

# Plot the accelerometer data (both smoothed and unsmoothed)
plt.figure(figsize=(12, 6))

# Unsmoothed data
plt.plot(data['accel_x'], label='accel_x (Unsmoothed)')
plt.plot(data['accel_y'], label='accel_y (Unsmoothed)')
plt.plot(data['accel_z'], label='accel_z (Unsmoothed)')

# Smoothed data
data['smooth_accel_x'] = data['accel_x'].rolling(window=5).mean()
data['smooth_accel_y'] = data['accel_y'].rolling(window=5).mean()
data['smooth_accel_z'] = data['accel_z'].rolling(window=5).mean()

plt.plot(data['smooth_accel_x'], label='accel_x (Smoothed)')
plt.plot(data['smooth_accel_y'], label='accel_y (Smoothed)')
plt.plot(data['smooth_accel_z'], label='accel_z (Smoothed)')

plt.xlabel('Timestamp')
plt.ylabel('Acceleration')
plt.title('Accelerometer Data')
plt.legend()
plt.savefig('accelerometer_plot.png')
plt.show()

# Plot the magnetometer data (both smoothed and unsmoothed)
plt.figure(figsize=(12, 6))

# Unsmoothed data
plt.plot(data['mag_x'], label='mag_x (Unsmoothed)')
plt.plot(data['mag_y'], label='mag_y (Unsmoothed)')
plt.plot(data['mag_z'], label='mag_z (Unsmoothed)')

# Smoothed data
data['smooth_mag_x'] = data['mag_x'].rolling(window=5).mean()
data['smooth_mag_y'] = data['mag_y'].rolling(window=5).mean()
data['smooth_mag_z'] = data['mag_z'].rolling(window=5).mean()

plt.plot(data['smooth_mag_x'], label='mag_x (Smoothed)')
plt.plot(data['smooth_mag_y'], label='mag_y (Smoothed)')
plt.plot(data['smooth_mag_z'], label='mag_z (Smoothed)')

plt.xlabel('Timestamp')
plt.ylabel('Magnetometer')
plt.title('Magnetometer Data')
plt.legend()
plt.savefig('magnetometer_plot.png')
plt.show()

# Plot the gyroscope data (both smoothed and unsmoothed)
plt.figure(figsize=(12, 6))

# Unsmoothed data
plt.plot(data['gyro_x'], label='gyro_x (Unsmoothed)')
plt.plot(data['gyro_y'], label='gyro_y (Unsmoothed)')
plt.plot(data['gyro_z'], label='gyro_z (Unsmoothed)')

# Smoothed data
data['smooth_gyro_x'] = data['gyro_x'].rolling(window=5).mean()
data['smooth_gyro_y'] = data['gyro_y'].rolling(window=5).mean()
data['smooth_gyro_z'] = data['gyro_z'].rolling(window=5).mean()

plt.plot(data['smooth_gyro_x'], label='gyro_x (Smoothed)')
plt.plot(data['smooth_gyro_y'], label='gyro_y (Smoothed)')
plt.plot(data['smooth_gyro_z'], label='gyro_z (Smoothed)')

plt.xlabel('Timestamp')
plt.ylabel('Gyroscope')
plt.title('Gyroscope Data')
plt.legend()
plt.savefig('gyroscope_plot.png')
plt.show()
# Detect 90-degree turns
# Calculate thresholds based on quantiles of smoothed data
quantile_accel = .7 # Adjust these quantile values as needed
quantile_gyro = .7
quantile_mag = .73

threshold_accel = data['smooth_accel_x'].quantile(quantile_accel)
threshold_gyro = data['smooth_gyro_x'].quantile(quantile_gyro)
threshold_mag = data['smooth_mag_x'].quantile(quantile_mag)

for index in range(len(data) - 2):
    # Calculate changes in accelerometer data
    delta_accel_x = data.at[index + 1, 'smooth_accel_x'] - data.at[index, 'smooth_accel_x']
    delta_accel_y = data.at[index + 1, 'smooth_accel_y'] - data.at[index, 'smooth_accel_y']
    delta_accel_z = data.at[index + 1, 'smooth_accel_z'] - data.at[index, 'smooth_accel_z']
    magnitude_accel = np.sqrt(delta_accel_x ** 2 + delta_accel_y ** 2 + delta_accel_z ** 2)

    # Calculate changes in gyroscope data
    delta_gyro_x = data.at[index + 1, 'smooth_gyro_x'] - data.at[index, 'smooth_gyro_x']
    delta_gyro_y = data.at[index + 1, 'smooth_gyro_y'] - data.at[index, 'smooth_gyro_y']
    delta_gyro_z = data.at[index + 1, 'smooth_gyro_z'] - data.at[index, 'smooth_gyro_z']
    magnitude_gyro = np.sqrt(delta_gyro_x ** 2 + delta_gyro_y ** 2 + delta_gyro_z ** 2)

    # Calculate changes in magnetometer data
    delta_mag_x = data.at[index + 1, 'smooth_mag_x'] - data.at[index, 'smooth_mag_x']
    delta_mag_y = data.at[index + 1, 'smooth_mag_y'] - data.at[index, 'smooth_mag_y']
    delta_mag_z = data.at[index + 1, 'smooth_mag_z'] - data.at[index, 'smooth_mag_z']
    magnitude_mag = np.sqrt(delta_mag_x ** 2 + delta_mag_y ** 2 + delta_mag_z ** 2)

    # Check if any of the magnitudes exceed the thresholds
    if magnitude_accel > threshold_accel and magnitude_gyro > threshold_gyro and magnitude_mag > threshold_mag:
        print(f"Potential 90-degree turn detected at time {data.at[index, 'timestamp']}")
