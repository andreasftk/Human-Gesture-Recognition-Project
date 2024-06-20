import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import scipy.signal


folder = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/segments/'
file_name = 'KaresiouWear_2024-06-18T16.54.31.695_F5174DCC3C91_WithMovement.csv'
file_path = os.path.join(folder, file_name)
data = pd.read_csv(file_path)
data_subset = data.iloc[:].reset_index(drop=True)

def get_movement_segments(movement_series):
    segments = []
    start_idx = None
    for i in range(1, len(movement_series)):
        if movement_series[i] == 1 and movement_series[i-1] == 0:
            start_idx = i
        elif movement_series[i] == 0 and movement_series[i-1] == 1:
            if start_idx is not None:
                segments.append((start_idx, i))
            start_idx = None
    if start_idx is not None:
        segments.append((start_idx, len(movement_series)))
    return segments

segments = get_movement_segments(data_subset['movement'])

fig, axes = plt.subplots(7, 1, figsize=(14, 21), sharex=True)

axes[0].set_title('Gyroscope X-axis (deg/s) Over Time')
axes[1].set_title('Gyroscope Y-axis (deg/s) Over Time')
axes[2].set_title('Gyroscope Z-axis (deg/s) Over Time')
axes[3].set_title('Accelerometer X-axis (g) Over Time')
axes[4].set_title('Accelerometer Y-axis (g) Over Time')
axes[5].set_title('Accelerometer Z-axis (g) Over Time')
axes[6].set_title('Energy Over Time')

axes[0].plot(data_subset['x-axis (deg/s)'], color='lightgrey', label='Original Data')
axes[1].plot(data_subset['y-axis (deg/s)'], color='lightgrey', label='Original Data')
axes[2].plot(data_subset['z-axis (deg/s)'], color='lightgrey', label='Original Data')
axes[3].plot(data_subset['x-axis (g)'], color='lightgrey', label='Original Data')
axes[4].plot(data_subset['y-axis (g)'], color='lightgrey', label='Original Data')
axes[5].plot(data_subset['z-axis (g)'], color='lightgrey', label='Original Data')
axes[6].plot(data_subset['energy'], color='lightgrey', label='Original Data')

colors = plt.cm.get_cmap('tab20', len(segments))

for i, (start, end) in enumerate(segments):
    color = colors(i)
    axes[0].plot(range(start, end), data_subset['x-axis (deg/s)'][start:end], color=color)
    axes[1].plot(range(start, end), data_subset['y-axis (deg/s)'][start:end], color=color)
    axes[2].plot(range(start, end), data_subset['z-axis (deg/s)'][start:end], color=color)
    axes[3].plot(range(start, end), data_subset['x-axis (g)'][start:end], color=color)
    axes[4].plot(range(start, end), data_subset['y-axis (g)'][start:end], color=color)
    axes[5].plot(range(start, end), data_subset['z-axis (g)'][start:end], color=color)
    axes[6].plot(range(start, end), data_subset['energy'][start:end], color=color)

for ax in axes:
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.show()

output_dir = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/segments'


for i, (start, end) in enumerate(segments):
    segment_data = data_subset.iloc[start:end]
    segment_file_path = os.path.join(output_dir, f'{file_name.replace("WithMovement.csv", "")}segment_{i+1}.csv')
    segment_data.to_csv(segment_file_path, index=False)

print(f'Movement segments saved for file {file_name} in directory: {output_dir}')

plt.figure(figsize=(14, 6))
plt.plot(data_subset['energy'], color='black', label='Energy')
plt.title('Energy Over Time')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.grid(True)

for i, (start, end) in enumerate(segments):
    plt.axvspan(start, end, color=colors(i), alpha=0.3)

plt.legend()
plt.tight_layout()
plt.show()
