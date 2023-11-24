import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#read in cols
columns_to_use = ['timestamp', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z']
data = pd.read_csv('../lab8-dataset/TURNING.csv', header=0, usecols=columns_to_use)

# Plot the accelerometer data
plt.figure(figsize=(12, 6))

# Assuming 'accel_x', 'accel_y', 'accel_z' are the columns for accelerometer data
plt.plot(data['accel_x'], label='accel_x')
plt.plot(data['accel_y'], label='accel_y')
plt.plot(data['accel_z'], label='accel_z')

plt.xlabel('Timestamp')
plt.ylabel('Acceleration')
plt.title('Accelerometer Data')
plt.legend()
plt.savefig('accelerometer_plot.png')


# Plot the magnetometer data
plt.figure(figsize=(12, 6))

# Assuming 'mag_x', 'mag_y', 'mag_z' are the columns for magnetometer data
plt.plot(data['mag_x'], label='mag_x')
plt.plot(data['mag_y'], label='mag_y')
plt.plot(data['mag_z'], label='mag_z')

plt.xlabel('Timestamp')
plt.ylabel('Magnetometer')
plt.title('Magnetometer Data')
plt.legend()
plt.savefig('magnetometer_plot.png')
plt.show()

# Plot the gyroscope data
plt.figure(figsize=(12, 6))

# Assuming 'gyro_x', 'gyro_y', 'gyro_z' are the columns for gyroscope data
plt.plot(data['gyro_x'], label='gyro_x')
plt.plot(data['gyro_y'], label='gyro_y')
plt.plot(data['gyro_z'], label='gyro_z')

plt.xlabel('Timestamp')
plt.ylabel('Gyroscope')
plt.title('Gyroscope Data')
plt.legend()
plt.savefig('gyroscope_plot.png')
plt.show()






# Smooth the data if necessary (e.g., using rolling mean or other smoothing techniques)
# Example: Smoothing accelerometer data for 'accel_x', 'accel_y', 'accel_z'
data['smooth_accel_x'] = data['accel_x'].rolling(window=5).mean()
data['smooth_accel_y'] = data['accel_y'].rolling(window=5).mean()
data['smooth_accel_z'] = data['accel_z'].rolling(window=5).mean()

# Detect 90-degree turns
# Example: Checking for turns based on changes in accelerometer data
# You might need to adjust the threshold and criteria based on your data
threshold = .75  # Adjust this threshold as needed

for index in range(1, len(data) - 1):
    # Calculate differences between consecutive values
    delta_x = data.at[index + 1, 'smooth_accel_x'] - data.at[index, 'smooth_accel_x']
    delta_y = data.at[index + 1, 'smooth_accel_y'] - data.at[index, 'smooth_accel_y']
    delta_z = data.at[index + 1, 'smooth_accel_z'] - data.at[index, 'smooth_accel_z']

    # Calculate the magnitude of the change
    magnitude = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)

    # Check if magnitude exceeds the threshold
    if magnitude > threshold:
        print(f"Potential 90-degree turn detected at index {index}")
