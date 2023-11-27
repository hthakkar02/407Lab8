import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('../lab8-dataset/WALKING_AND_TURNING.csv', header=0,
                 usecols=["timestamp", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"], index_col=None,
                 names=["timestamp", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"])

columns_to_smooth = ["accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"]
for column in columns_to_smooth:
    df[column + "_smoothed"] = df[column].rolling(window=20, min_periods=1).mean()

df['timestamp'] = df['timestamp'] * 1e-9

df['time_seconds'] = df['timestamp']
df['integral_smooth_gyro_x'] = np.cumsum(df['gyro_x_smoothed'] * (df['time_seconds'].diff().fillna(0)))
df['integral_smooth_gyro_y'] = np.cumsum(df['gyro_y_smoothed'] * (df['time_seconds'].diff().fillna(0)))
df['integral_smooth_gyro_z'] = np.cumsum(df['gyro_z_smoothed'] * (df['time_seconds'].diff().fillna(0)))

plt.figure(figsize=(12, 6))

plt.plot(df['gyro_x'], label='gyro_x (Unsmoothed)')
plt.plot(df['gyro_y'], label='gyro_y (Unsmoothed)')
plt.plot(df['gyro_z'], label='gyro_z (Unsmoothed)')

plt.plot(df['gyro_x_smoothed'], label='gyro_x (Smoothed)')
plt.plot(df['gyro_y_smoothed'], label='gyro_y (Smoothed)')
plt.plot(df['gyro_z_smoothed'], label='gyro_z (Smoothed)')

plt.xlabel('Timestamp')
plt.ylabel('Gyroscope')
plt.title('Gyroscope Data')
plt.legend()
plt.savefig('gyroscope_plot.png')

plt.figure(figsize=(12, 6))

plt.plot(df['integral_smooth_gyro_x'], label='Integral gyro_x (Smoothed)')
plt.plot(df['integral_smooth_gyro_y'], label='Integral gyro_y (Smoothed)')
plt.plot(df['integral_smooth_gyro_z'], label='Integral gyro_z (Smoothed)')

plt.xlabel('Timestamp')
plt.ylabel('Integrated Gyroscope')
plt.title('Integrated Gyroscope Data')
plt.legend()
plt.savefig('integrated_gyroscope_plot.png')

df['accel_magnitude'] = (df['accel_x_smoothed'] ** 2 + df['accel_y_smoothed'] ** 2 + df['accel_z_smoothed'] ** 2) ** 0.5
threshold = df['accel_magnitude'].quantile(0.70)

plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['accel_magnitude'], label='Accel_magnitude')
plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
plt.title('Accel_magnitude vs Timestamp')
plt.xlabel('Timestamp (s)')
plt.ylabel('Magnitude (m/s^2)')
plt.legend()
plt.savefig(f'accel_magnitude_plot.png')

above_threshold = False
step_count = 0
for value in df['accel_magnitude']:
    if value > threshold and not above_threshold:
        above_threshold = True
    elif value < threshold and above_threshold:
        above_threshold = False
        step_count += 1

print(f"Number of steps: {step_count}")

threshold_gyro = .75
df['magnitude_integrated_gyro'] = np.sqrt(df['integral_smooth_gyro_x'] ** 2 +
                                          df['integral_smooth_gyro_y'] ** 2 +
                                          df['integral_smooth_gyro_z'] ** 2)
df['magnitude_integrated_gyro'].replace([np.inf, -np.inf, np.nan], 0, inplace=True)
df['division_result'] = (df['magnitude_integrated_gyro'] // threshold_gyro)

plt.figure(figsize=(12, 6))
plt.plot(df['integral_smooth_gyro_x'], label='Integral gyro_x (Smoothed)')
plt.plot(df['integral_smooth_gyro_y'], label='Integral gyro_y (Smoothed)')
plt.plot(df['integral_smooth_gyro_z'], label='Integral gyro_z (Smoothed)')

prev_value = 0
legend_added = False
total_turns = 0
timestamps = []
above_threshold = False
step_count = 0
prev_step_count = 0
line_lengths = []
for index, row in df.iterrows():
    current_value = row['division_result']
    value = row['accel_magnitude']
    if value > threshold and not above_threshold:
        above_threshold = True
    elif value < threshold and above_threshold:
        above_threshold = False
        step_count += 1
    if current_value != prev_value:
        total_turns += 1
        timestamps.append(row['timestamp'])
        if current_value > prev_value:
            print(f"A 45 degree turn counterclockwise was made at timestamp: {row['timestamp']} steps up to this turn: "
                  f"{step_count - prev_step_count}")
        else:
            print(f"A 45 degree turn clockwise was made at timestamp: {row['timestamp']} steps up to this turn: "
                  f"{step_count - prev_step_count}")
        line_lengths.append(step_count - prev_step_count)
        plt.axvline(x=index, color='r', linestyle='--', label='Change' if not legend_added else '')
        prev_value = current_value
        legend_added = True
        prev_step_count = step_count

plt.xlabel('Timestamp')
plt.ylabel('Integrated Gyroscope')
plt.title('Integrated Gyroscope Data')
plt.legend()
plt.savefig('integrated_gyroscope_plot_with_lines.png')
print(f"A total of {total_turns} 90 degree turns were made.")


def calculate_coordinates(x, y, line_length, line_angle):
    angle_rad = np.radians(line_angle)
    new_x = x + line_length * np.cos(angle_rad)
    new_y = y + line_length * np.sin(angle_rad)
    return new_x, new_y


data = {'Length': line_lengths,
        'Angle': [90]+([45] * (len(line_lengths) - 1))}

df = pd.DataFrame(data)

start_x, start_y = 0, 0
accumulated_angle = 0

fig, ax = plt.subplots()

ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)

ax.set_xlim([-max(line_lengths)*2, max(line_lengths)*2])
ax.set_ylim([-max(line_lengths)*2, max(line_lengths)*2])

lines = []

for index, row in df.iterrows():
    length = row['Length']
    angle = row['Angle']
    accumulated_angle += angle

    end_x, end_y = calculate_coordinates(start_x, start_y, length, accumulated_angle)
    line = ax.plot([start_x, end_x], [start_y, end_y], marker='o')[0]
    lines.append(line)
    start_x, start_y = end_x, end_y
ax.set_aspect('equal', adjustable='box')
ax.legend(lines, [f'Length: {length} meters' for length in line_lengths])
plt.grid(True)
plt.xlabel('X-axis (Meters)')
plt.ylabel('Y-axis (Meters)')
plt.title('Coordinate Plane in meters to plot path')
plt.savefig('walking_trajectory_plot.png')
