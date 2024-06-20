import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import scipy.signal

def apply_filter(arr, order=4, wn=0.04, filter_type="lowpass") -> np.ndarray:
    fbd_filter = scipy.signal.butter(N=order, Wn=wn, btype=filter_type, output="sos")
    filtered_signal = scipy.signal.sosfiltfilt(sos=fbd_filter, x=arr, padlen=0)
    return filtered_signal

def normalize_and_recalibrate(data):
    for axis in ['x-axis (deg/s)', 'y-axis (deg/s)', 'z-axis (deg/s)', 'x-axis (g)', 'y-axis (g)', 'z-axis (g)']:
        data[axis] = (data[axis] - data[axis].min()) / (data[axis].max() - data[axis].min())
    return data

def normalize(data):
    return (data - data.min()) / (data.max() - data.min())

def quantize(data, num_levels):
    bins = np.linspace(0, 1, num_levels + 1)
    quantized_data = np.digitize(data, bins) - 1
    quantized_data = quantized_data / (num_levels - 1)
    return quantized_data

folder = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/merged'
output_dir = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/segments'
os.makedirs(output_dir, exist_ok=True)

sampling_rate = 100
cutoff_frequency = 4
normalized_cutoff_frequency = cutoff_frequency / (0.5 * sampling_rate)

file_name = 'KaresiouWear_2024-06-16T18.17.54.637_F5174DCC3C91_Both.csv'
file_path = os.path.join(folder, file_name)

data = pd.read_csv(file_path)
data1 = pd.read_csv(file_path)

data['x-axis (deg/s)'] = apply_filter(data['x-axis (deg/s)'].values, order=4, wn=normalized_cutoff_frequency, filter_type='lowpass')
data['y-axis (deg/s)'] = apply_filter(data['y-axis (deg/s)'].values, order=4, wn=normalized_cutoff_frequency, filter_type='lowpass')
data['z-axis (deg/s)'] = apply_filter(data['z-axis (deg/s)'].values, order=4, wn=normalized_cutoff_frequency, filter_type='lowpass')
data['x-axis (g)'] = apply_filter(data['x-axis (g)'].values, order=4, wn=normalized_cutoff_frequency, filter_type='lowpass')
data['y-axis (g)'] = apply_filter(data['y-axis (g)'].values, order=4, wn=normalized_cutoff_frequency, filter_type='lowpass')
data['z-axis (g)'] = apply_filter(data['z-axis (g)'].values, order=4, wn=normalized_cutoff_frequency, filter_type='lowpass')

data = normalize_and_recalibrate(data)

data1['energy'] = np.sum(
    data[['x-axis (deg/s)', 'y-axis (deg/s)', 'z-axis (deg/s)']].values**2 +
    data[['x-axis (g)', 'y-axis (g)', 'z-axis (g)']].values**2,
    axis=1
)

data['energy'] = data1['energy']
data['energy'] = apply_filter(data['energy'].values, order=4, wn=normalized_cutoff_frequency, filter_type='lowpass')
data['energy'] = normalize(data['energy'].values)

threshold = 2.0
def classify_movement(row):
    if row['energy'] < 0.35 and row['energy'] > 0.10: 
        if row['y-axis (g)'] < 0.16 and row['y-axis (g)'] > 0.0: 
            return 0
        else:
            return 1
    else:
        return 1

data1['movement'] = data.apply(classify_movement, axis=1)
data['movement'] = data1['movement']

output_file_with_movement_path = os.path.join(output_dir, file_name.replace('Both.csv', 'WithMovement.csv'))
data.to_csv(output_file_with_movement_path, index=False)

data_subset = data.iloc[:].reset_index(drop=True)

def get_movement_segments(movement_series):
    segments = []
    start_idx = None
    
    for i in range(len(movement_series)):
        if movement_series[i] == 1:
            if start_idx is None:
                start_idx = i
        else:
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

for i, (start, end) in enumerate(segments):
    segment_data = data_subset.iloc[start:end]
    segment_file_path = os.path.join(output_dir, f'{file_name.replace("Both.csv", "")}segment_{i+1}.csv')
    segment_data.to_csv(segment_file_path, index=False)

print(f'Movement segments saved for file {file_name} in directory: {output_dir}')

# plt.figure(figsize=(14, 6))
# plt.plot(data_subset['energy'], color='black', label='Energy')
# plt.title('Energy Over Time')
# plt.xlabel('Time')
# plt.ylabel('Energy')
# plt.grid(True)

for i, (start, end) in enumerate(segments):
    plt.axvspan(start, end, color=colors(i), alpha=0.3)

plt.legend()
plt.tight_layout()
plt.show()
