import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def merge_sensor_data(accelerometer_csv, gyroscope_csv, output_csv):
    # Load the CSV files
    accelerometer_data = pd.read_csv(accelerometer_csv)
    gyroscope_data = pd.read_csv(gyroscope_csv)
    
    # Merge the dataframes on 'elapsed (s)' column
    merged_data = pd.merge(accelerometer_data, gyroscope_data, on='elapsed (s)', suffixes=('_accel', '_gyro'))
    
    # Select relevant columns
    merged_data = merged_data[['elapsed (s)', 'x-axis (g)', 'y-axis (g)', 'z-axis (g)', 
                               'x-axis (deg/s)', 'y-axis (deg/s)', 'z-axis (deg/s)']]
    
    # Save the merged dataframe to a new CSV file
    merged_data.to_csv(output_csv, index=False)

    return merged_data

# Define file paths
accelerometer_csv = 'C:/Users/andre/Downloads/KaresiouWear_2024-06-08T21.36.41.634_F5174DCC3C91_Accelerometer.csv'
gyroscope_csv = 'C:/Users/andre/Downloads/KaresiouWear_2024-06-08T21.36.41.634_F5174DCC3C91_Gyroscope.csv'
output_csv = 'C:/Users/andre/Downloads/merged_sensor_data.csv'

# Merge the data and save to a new CSV
merged_data = merge_sensor_data(accelerometer_csv, gyroscope_csv, output_csv)

# Display the first few rows of the merged dataframe
print(merged_data.head())

def plot_sensor_data(merged_data):
    # Plot accelerometer data
    plt.figure(figsize=(14, 7))
    plt.subplot(2, 1, 1)
    plt.plot(merged_data['elapsed (s)'], merged_data['x-axis (g)'], label='X-axis (g)')
    plt.plot(merged_data['elapsed (s)'], merged_data['y-axis (g)'], label='Y-axis (g)')
    plt.plot(merged_data['elapsed (s)'], merged_data['z-axis (g)'], label='Z-axis (g)')
    plt.title('Accelerometer Data')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.legend()
    plt.grid(True)

    # Plot gyroscope data
    plt.subplot(2, 1, 2)
    plt.plot(merged_data['elapsed (s)'], merged_data['x-axis (deg/s)'], label='X-axis (deg/s)')
    plt.plot(merged_data['elapsed (s)'], merged_data['y-axis (deg/s)'], label='Y-axis (deg/s)')
    plt.plot(merged_data['elapsed (s)'], merged_data['z-axis (deg/s)'], label='Z-axis (deg/s)')
    plt.title('Gyroscope Data')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Angular Velocity (deg/s)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Plot the merged sensor data
plot_sensor_data(merged_data)

# Filter the data to hold the signal from 28.3 to 42.5 seconds
filtered_data = merged_data[(merged_data['elapsed (s)'] >= 28.3) & (merged_data['elapsed (s)'] <= 42.5)]

# Plot the filtered sensor data
plot_sensor_data(filtered_data)

# Calculate the energy for each time instance
filtered_data.loc[:, 'energy'] = (
    (filtered_data['x-axis (g)'] ** 2 + filtered_data['y-axis (g)'] ** 2 + filtered_data['z-axis (g)'] ** 2) +
    (filtered_data['x-axis (deg/s)'] ** 2 + filtered_data['y-axis (deg/s)'] ** 2 + filtered_data['z-axis (deg/s)'] ** 2)
)

# Plot the energy waveform
plt.figure(figsize=(14, 5))
plt.plot(filtered_data['elapsed (s)'], filtered_data['energy'], label='Energy')
plt.title('Energy Waveform')
plt.xlabel('Elapsed Time (s)')
plt.ylabel('Energy')
plt.legend()
plt.grid(True)
plt.show()

# Define the threshold and minimum duration in seconds
threshold = 2000
min_duration = 0.25  # in seconds
sample_rate = 100  # samples per second

# Calculate the minimum number of samples for the duration
min_samples = int(min_duration * sample_rate)

# Label the data based on the threshold
filtered_data.loc[:, 'label'] = (filtered_data['energy'] > threshold).astype(int)

# Segment the data with the new condition
movement_segments = []
current_segment = []

for _, row in filtered_data.iterrows():
    if row['label'] == 1:
        current_segment.append(row)
    else:
        if len(current_segment) >= min_samples:
            movement_segments.append(pd.DataFrame(current_segment))
        current_segment = []

# If the last segment is non-empty and meets the duration condition, append it as well
if len(current_segment) >= min_samples:
    movement_segments.append(pd.DataFrame(current_segment))

# Save each segment as a new CSV file
segment_files = []
for i, segment in enumerate(movement_segments):
    segment_file = f'C:/Users/andre/Downloads/movement_segment_{i + 1}.csv'
    segment.to_csv(segment_file, index=False)
    segment_files.append(segment_file)

# Display the file paths of the saved segments
print(segment_files)

# Filter the data to keep the signal from 28.352 to 38.757 seconds
final_filtered_data = merged_data[(merged_data['elapsed (s)'] >= 28.352) & (merged_data['elapsed (s)'] <= 38.757)]

def plot_accelerometer_data(data):
    plt.figure(figsize=(14, 7))
    plt.plot(data['elapsed (s)'], data['x-axis (g)'], label='X-axis (g)')
    plt.plot(data['elapsed (s)'], data['y-axis (g)'], label='Y-axis (g)')
    plt.plot(data['elapsed (s)'], data['z-axis (g)'], label='Z-axis (g)')
    plt.title('Accelerometer Data')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_gyroscope_data(data):
    plt.figure(figsize=(14, 7))
    plt.plot(data['elapsed (s)'], data['x-axis (deg/s)'], label='X-axis (deg/s)')
    plt.plot(data['elapsed (s)'], data['y-axis (deg/s)'], label='Y-axis (deg/s)')
    plt.plot(data['elapsed (s)'], data['z-axis (deg/s)'], label='Z-axis (deg/s)')
    plt.title('Gyroscope Data')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Angular Velocity (deg/s)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the accelerometer data
plot_accelerometer_data(final_filtered_data)

# Plot the gyroscope data
plot_gyroscope_data(final_filtered_data)

def generate_synthetic_movements(final_filtered_data, num_movements):
    synthetic_data = []

    for _ in range(num_movements):
        for segment in final_filtered_data:
            synthetic_segment = segment.copy()

            # Introduce small random variations to the data
            synthetic_segment['x-axis (g)'] += np.random.normal(0, 0.01, size=len(segment))
            synthetic_segment['y-axis (g)'] += np.random.normal(0, 0.01, size=len(segment))
            synthetic_segment['z-axis (g)'] += np.random.normal(0, 0.01, size=len(segment))
            synthetic_segment['x-axis (deg/s)'] += np.random.normal(0, 1, size=len(segment))
            synthetic_segment['y-axis (deg/s)'] += np.random.normal(0, 1, size=len(segment))
            synthetic_segment['z-axis (deg/s)'] += np.random.normal(0, 1, size=len(segment))
            
            synthetic_data.append(synthetic_segment)

    return pd.concat(synthetic_data, ignore_index=True)

# Manually identified movement segments
movement_periods = [
    (29, 32),
    (33, 36),
    (37, 38.5)
]

# Filter the data to keep the signal from 28.352 to 38.757 seconds
filtered_data = final_filtered_data[(final_filtered_data['elapsed (s)'] >= 28.352) & (final_filtered_data['elapsed (s)'] <= 38.757)]

manual_movement_segments = []

for start, end in movement_periods:
    segment = filtered_data[(filtered_data['elapsed (s)'] >= start) & (filtered_data['elapsed (s)'] <= end)]
    manual_movement_segments.append(segment)

# Generate the extended time series with 400 movements
num_movements_to_generate = 4
extended_synthetic_data = generate_synthetic_movements(manual_movement_segments, num_movements_to_generate)

# Adjust the time to maintain continuity
time_offset = 0
time_offset = 0
sample_rate = 100  # samples per second
synthetic_data = []
for i in range(num_movements_to_generate):
    for segment in manual_movement_segments:
        synthetic_segment = segment.copy()
        synthetic_segment['elapsed (s)'] += time_offset
        synthetic_data.append(synthetic_segment)
        time_offset = synthetic_segment['elapsed (s)'].iloc[-1] + 1 / sample_rate

extended_synthetic_data = pd.concat(synthetic_data, ignore_index=True)

# Save the extended synthetic dataset to a CSV file
extended_synthetic_data.to_csv('extended_synthetic_movements.csv', index=False)

# Plot the synthetic accelerometer data
plot_accelerometer_data(extended_synthetic_data)

# Plot the synthetic gyroscope data
plot_gyroscope_data(extended_synthetic_data)
