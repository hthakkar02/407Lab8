import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../lab8-dataset/ACCELERATION.csv', header=0)
df.plot(x='timestamp', y=['acceleration', 'noisyacceleration'], kind='line', figsize=(10, 6),
        title='Acceleration vs Noisy Acceleration')
plt.xlabel('Timestamp (seconds)')
plt.ylabel('Acceleration (m/s^2)')
plt.savefig('acceleration_plot.png')

df['speed'] = df['acceleration'].cumsum()
df['noisyspeed'] = df['noisyacceleration'].cumsum()

df.plot(x='timestamp', y=['speed', 'noisyspeed'], kind='line', figsize=(10, 6), title='Speed vs Timestamp')
plt.xlabel('Timestamp (seconds)')
plt.ylabel('Speed (m/s)')
plt.savefig('speed_plot.png')

df['distance'] = df['speed'].cumsum()
df['noisydistance'] = df['noisyspeed'].cumsum()

df.plot(x='timestamp', y=['distance', 'noisydistance'], kind='line', figsize=(10, 6), title='Distance vs Timestamp')
plt.xlabel('Timestamp (seconds)')
plt.ylabel('Distance (m)')
plt.savefig('distance_plot.png')

actual_distance = df['distance'].iloc[-1]
noisy_distance = df['noisydistance'].iloc[-1]

print(f"Final Distance (Actual Acceleration): {actual_distance} meters")
print(f"Final Distance (Noisy Acceleration): {noisy_distance} meters")
print(f"Difference between the Distances (Noisy Distance - Actual Distance): {noisy_distance - actual_distance} meters")
