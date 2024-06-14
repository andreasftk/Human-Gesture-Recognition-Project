

import pandas as pd
import matplotlib.pyplot as plt
import itertools
import os
import numpy as np


# Load the CSV file
file_path = 'C:/Users/andre/Downloads/updated_combined_accel_gyro_data_with_energy_and_corrected_movement.csv'
data = pd.read_csv(file_path)


# Calculate the total energy
data['energy'] = np.sum(
    data[['gyr_x (deg/s)', 'gyr_y (deg/s)', 'gyr_z (deg/s)']].values**2 +
    data[['acc_x (g)', 'acc_y (g)', 'acc_z (g)']].values**2,
    axis=1
)

# Apply the threshold to classify the data
threshold = 2000
data['movement'] = data['energy'].apply(lambda x: 1 if x > threshold else 0)

# Save the updated dataframe to a new CSV file
output_file_with_movement_path = 'G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/updated_combined_accel_gyro_data_with_energy_and_movement.csv'
data.to_csv(output_file_with_movement_path, index=False)


# Hold values from 0 to 1854
data_subset = data.iloc[:1854]

# Function to get segments of movements including preceding zeros
def get_movement_segments_with_zeros(movement_series):
    segments = []
    start_idx = None
    for i in range(1, len(movement_series)):
        if movement_series[i] == 1 and movement_series[i-1] == 0:
            start_idx = i
            # Include preceding zeros
            while start_idx > 0 and movement_series[start_idx-1] == 0:
                start_idx -= 1
        elif movement_series[i] == 0 and movement_series[i-1] == 1:
            if start_idx is not None:
                segments.append((start_idx, i))
            start_idx = None
    if start_idx is not None:
        segments.append((start_idx, len(movement_series)))
    return segments

# Get movement segments with preceding zeros
segments_with_zeros = get_movement_segments_with_zeros(data_subset['corrected_movement'])

# Define colors for plotting
colors = plt.cm.get_cmap('tab20', len(segments_with_zeros))

# Plot each axis of the gyroscope and accelerometer data with different colors for each movement segment
fig, axes = plt.subplots(6, 1, figsize=(14, 18), sharex=True)

axes[0].set_title('Gyroscope X-axis (deg/s) Over Time')
axes[1].set_title('Gyroscope Y-axis (deg/s) Over Time')
axes[2].set_title('Gyroscope Z-axis (deg/s) Over Time')
axes[3].set_title('Accelerometer X-axis (g) Over Time')
axes[4].set_title('Accelerometer Y-axis (g) Over Time')
axes[5].set_title('Accelerometer Z-axis (g) Over Time')

for i, (start, end) in enumerate(segments_with_zeros):
    color = colors(i)
    axes[0].plot(range(start, end), data_subset['gyr_x (deg/s)'][start:end], color=color)
    axes[1].plot(range(start, end), data_subset['gyr_y (deg/s)'][start:end], color=color)
    axes[2].plot(range(start, end), data_subset['gyr_z (deg/s)'][start:end], color=color)
    axes[3].plot(range(start, end), data_subset['acc_x (g)'][start:end], color=color)
    axes[4].plot(range(start, end), data_subset['acc_y (g)'][start:end], color=color)
    axes[5].plot(range(start, end), data_subset['acc_z (g)'][start:end], color=color)

for ax in axes:
    ax.grid(True)

plt.tight_layout()
plt.show()

# Create a directory to store the CSV files
output_dir = 'G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/'
os.makedirs(output_dir, exist_ok=True)

# Save each segment as a separate CSV file
for i, (start, end) in enumerate(segments_with_zeros):
    segment_data = data_subset.iloc[start:end]
    segment_file_path = os.path.join(output_dir, f'movement_segment_{i+1}.csv')
    segment_data.to_csv(segment_file_path, index=False)

print(f'Movement segments saved in directory: {output_dir}')


# Load the individual movement CSV files
movement_1 = pd.read_csv("G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/movement_segment_1.csv")
movement_2 = pd.read_csv("G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/movement_segment_2.csv")
movement_3 = pd.read_csv("G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/movement_segment_3.csv")
movement_4 = pd.read_csv("G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/movement_segment_4.csv")
movement_5 = pd.read_csv("G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/movement_segment_5.csv")
movement_6 = pd.read_csv("G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/movement_segment_6.csv")
movement_7 = pd.read_csv("G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/movement_segment_7.csv")
movement_8 = pd.read_csv("G:/Other computers/My Computer/8 Εξάμηνο\Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/segments/movement_segment_8.csv")

# List of movements
movements = [movement_1, movement_2, movement_3, movement_4, movement_5, movement_6, movement_7, movement_8]

# Function to plot the combined movements
def plot_combined_movement(data, movement):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 16), sharex=True)
    
    # Accelerometer data
    ax1.plot(data.index, data['acc_x (g)'], label='x-axis (g)', color='r')
    ax1.plot(data.index, data['acc_y (g)'], label='y-axis (g)', color='g')
    ax1.plot(data.index, data['acc_z (g)'], label='z-axis (g)', color='b')
    ax1.set_ylabel('Acceleration (g)')
    ax1.set_title(f'Accelerometer Data - {movement}')
    ax1.legend()
    
    # Gyroscope data
    ax2.plot(data.index, data['gyr_x (deg/s)'], label='x-axis (deg/s)', color='r')
    ax2.plot(data.index, data['gyr_y (deg/s)'], label='y-axis (deg/s)', color='g')
    ax2.plot(data.index, data['gyr_z (deg/s)'], label='z-axis (deg/s)', color='b')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Angular Velocity (deg/s)')
    ax2.set_title(f'Gyroscope Data - {movement}')
    ax2.legend()
    
    plt.show()

# Plot individual movement segments
# for i, movement in enumerate(movements, 1):
#     plot_combined_movement(movement, f'Movement Segment {i}')

# Create all possible combinations of the eight movements taken 3 at a time
movement_combinations = list(itertools.product(movements, repeat=3))

output_dir = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/data/class_A/'
# Combine and plot all movement combinations
for i, combination in enumerate(movement_combinations, 1):
    combined_data = pd.concat(combination, ignore_index=True)
    #combined_data = combined_data.drop(columns=['elapsed (s)'])
    #plot_combined_movement(combined_data, f'Combination {i}')
    combined_file_path = os.path.join(output_dir, f'data_A_{i}.csv')
    combined_data.to_csv(combined_file_path, index=False)

print(f'Combined movement data saved in directory: {output_dir}')

