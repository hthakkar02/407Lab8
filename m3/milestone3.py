import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# read in cols
columns_to_use = ['timestamp', 'gyro_x', 'gyro_y', 'gyro_z']
data = pd.read_csv('../lab8-dataset/TURNING.csv', header=0, usecols=columns_to_use)

data['timestamp'] = data['timestamp'] * 1e-9

# Plot the gyroscope data (both smoothed and unsmoothed)
plt.figure(figsize=(12, 6))

# Unsmoothed data
plt.plot(data['gyro_x'], label='gyro_x (Unsmoothed)')
plt.plot(data['gyro_y'], label='gyro_y (Unsmoothed)')
plt.plot(data['gyro_z'], label='gyro_z (Unsmoothed)')

# Smoothed data
data['smooth_gyro_x'] = data['gyro_x'].rolling(window=20).mean()
data['smooth_gyro_y'] = data['gyro_y'].rolling(window=20).mean()
data['smooth_gyro_z'] = data['gyro_z'].rolling(window=20).mean()

plt.plot(data['smooth_gyro_x'], label='gyro_x (Smoothed)')
plt.plot(data['smooth_gyro_y'], label='gyro_y (Smoothed)')
plt.plot(data['smooth_gyro_z'], label='gyro_z (Smoothed)')

plt.xlabel('Timestamp')
plt.ylabel('Gyroscope')
plt.title('Gyroscope Data')
plt.legend()
plt.savefig('gyroscope_plot.png')

plt.figure(figsize=(12, 6))

# Integrate gyroscope readings with respect to time
data['time_seconds'] = data['timestamp']
data['integral_smooth_gyro_x'] = np.cumsum(data['smooth_gyro_x'] * (data['time_seconds'].diff().fillna(0)))
data['integral_smooth_gyro_y'] = np.cumsum(data['smooth_gyro_y'] * (data['time_seconds'].diff().fillna(0)))
data['integral_smooth_gyro_z'] = np.cumsum(data['smooth_gyro_z'] * (data['time_seconds'].diff().fillna(0)))

plt.plot(data['integral_smooth_gyro_x'], label='Integral gyro_x (Smoothed)')
plt.plot(data['integral_smooth_gyro_y'], label='Integral gyro_y (Smoothed)')
plt.plot(data['integral_smooth_gyro_z'], label='Integral gyro_z (Smoothed)')

plt.xlabel('Timestamp')
plt.ylabel('Integrated Gyroscope')
plt.title('Integrated Gyroscope Data')
plt.legend()
plt.savefig('integrated_gyroscope_plot.png')

threshold_gyro = 1.5
data['magnitude_integrated_gyro'] = np.sqrt(data['integral_smooth_gyro_x']**2 +
                                            data['integral_smooth_gyro_y']**2 +
                                            data['integral_smooth_gyro_z']**2)
data['magnitude_integrated_gyro'].replace([np.inf, -np.inf, np.nan], 0, inplace=True)
data['division_result'] = (data['magnitude_integrated_gyro'] // threshold_gyro)

plt.figure(figsize=(12, 6))
plt.plot(data['integral_smooth_gyro_x'], label='Integral gyro_x (Smoothed)')
plt.plot(data['integral_smooth_gyro_y'], label='Integral gyro_y (Smoothed)')
plt.plot(data['integral_smooth_gyro_z'], label='Integral gyro_z (Smoothed)')

# Plot vertical dotted lines at indexes where change is detected
prev_value = 0
legend_added = False
total_turns = 0
for index, row in data.iterrows():
    current_value = row['division_result']
    if current_value != prev_value:
        total_turns+=1
        if current_value > prev_value:
            print(f"A 90 degree turn counterclockwise was made")
        else:
            print(f"A 90 degree turn clockwise was made")
        plt.axvline(x=index, color='r', linestyle='--', label='Change' if not legend_added else '')
        prev_value = current_value
        legend_added = True

plt.xlabel('Timestamp')
plt.ylabel('Integrated Gyroscope')
plt.title('Integrated Gyroscope Data')
plt.legend()
plt.savefig('integrated_gyroscope_plot_with_lines.png')
print(f"A total of {total_turns} 90 degree turns were made.")
