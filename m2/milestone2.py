import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../lab8-dataset/WALKING.csv', header=0, usecols=['timestamp', 'accel_x', 'accel_y', 'accel_z'])
df['timestamp'] = df['timestamp'] * 1e-9

columns_to_smooth = ['accel_x', 'accel_y', 'accel_z']
for column in columns_to_smooth:
    df[column + "_smoothed"] = df[column].rolling(window=20, min_periods=1).mean()

    df.plot(x='timestamp', y=[column, column + "_smoothed"], label=[f'{column} (Raw)', f'{column} (Smoothed)'])
    plt.title(f'{column} - Raw vs Smoothed')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Value (m/s^2)')
    plt.legend()
    plt.savefig(f'{column}_plot.png')

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
