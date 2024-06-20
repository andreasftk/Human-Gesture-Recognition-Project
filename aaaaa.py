import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Define folder paths
merged_folder = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/merged'
output_dir = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/segments'
os.makedirs(output_dir, exist_ok=True)

# Process each merged CSV file
for file_name in os.listdir(merged_folder):
    if file_name.endswith('Both.csv'):
        file_path = os.path.join(merged_folder, file_name)
        
        # Load the CSV file
        data = pd.read_csv(file_path)

        # Calculate the total energy (original code, not removed)
        data['energy'] = np.sum(
            data[['x-axis (deg/s)', 'y-axis (deg/s)', 'z-axis (deg/s)']].values**2 +
            data[['x-axis (g)', 'y-axis (g)', 'z-axis (g)']].values**2,
            axis=1
        )
        
        # Calculate the gradient vector magnitude of accelerometer axes
        grad_x = np.gradient(data['x-axis (g)'])
        grad_y = np.gradient(data['y-axis (g)'])
        grad_z = np.gradient(data['z-axis (g)'])
        data['acc_x_diff'] = grad_x

        # Convert acceleration from g to m/s²
        data['x-axis (m/s²)'] = data['x-axis (g)'] * 9.81
        data['y-axis (m/s²)'] = data['y-axis (g)'] * 9.81
        data['z-axis (m/s²)'] = data['z-axis (g)'] * 9.81

        # Assuming a uniform time interval, dt (in seconds)
        dt = 0.001  # Adjust this based on your actual time interval

        # Integrate acceleration to get speed using the trapezoidal rule
        data['speed_x'] = np.zeros(len(data))
        data['speed_y'] = np.zeros(len(data))
        data['speed_z'] = np.zeros(len(data))

        for i in range(1, len(data)):
            data['speed_x'] = np.cumsum((data['x-axis (m/s^2)'][:-1].values + data['x-axis (m/s^2)'][1:].values) / 2) * dt
            data.loc[i, 'speed_y'] =  0.5 * (data.loc[i, 'y-axis (g)'] + data.loc[i-1, 'y-axis (g)']) 
            data.loc[i, 'speed_z'] = 0.5 * (data.loc[i, 'z-axis (g)'] + data.loc[i-1, 'z-axis (g)']) 

        # Apply the threshold to classify the data
        threshold = 0.5  # This threshold can be adjusted as needed
        data['movement'] = data['acc_x_diff'].apply(lambda x: 1 if abs(x) > threshold else 0)

        # Save the updated dataframe to a new CSV file
        output_file_with_movement_path = os.path.join(output_dir, file_name.replace('Both.csv', 'WithMovement.csv'))
        data.to_csv(output_file_with_movement_path, index=False)

        # Hold values from 0 to 1854
        data_subset = data.iloc[:]

        # Function to get segments of movements excluding preceding zeros
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

        # Get movement segments without preceding zeros
        segments = get_movement_segments(data_subset['movement'])

        # Plot each axis of the gyroscope and accelerometer data
        fig, axes = plt.subplots(6, 1, figsize=(14, 18), sharex=True)

        axes[0].set_title('Gyroscope X-axis (deg/s) Over Time')
        axes[1].set_title('Gyroscope Y-axis (deg/s) Over Time')
        axes[2].set_title('Gyroscope Z-axis (deg/s) Over Time')
        axes[3].set_title('Accelerometer X-axis (g) Over Time')
        axes[4].set_title('Accelerometer Y-axis (g) Over Time')
        axes[5].set_title('Accelerometer Z-axis (g) Over Time')

        # Plot original data in light grey
        axes[0].plot(data_subset['x-axis (deg/s)'], color='lightgrey', label='Original Data')
        axes[1].plot(data_subset['y-axis (deg/s)'], color='lightgrey', label='Original Data')
        axes[2].plot(data_subset['z-axis (deg/s)'], color='lightgrey', label='Original Data')
        axes[3].plot(data_subset['x-axis (g)'], color='lightgrey', label='Original Data')
        axes[4].plot(data_subset['y-axis (g)'], color='lightgrey', label='Original Data')
        axes[5].plot(data_subset['z-axis (g)'], color='lightgrey', label='Original Data')

        # Define colors for plotting
        colors = plt.cm.get_cmap('tab20', len(segments))

        for i, (start, end) in enumerate(segments):
            color = colors(i)
            axes[0].plot(range(start, end), data_subset['x-axis (deg/s)'][start:end], color=color)
            axes[1].plot(range(start, end), data_subset['y-axis (deg/s)'][start:end], color=color)
            axes[2].plot(range(start, end), data_subset['z-axis (deg/s)'][start:end], color=color)
            axes[3].plot(range(start, end), data_subset['x-axis (g)'][start:end], color=color)
            axes[4].plot(range(start, end), data_subset['y-axis (g)'][start:end], color=color)
            axes[5].plot(range(start, end), data_subset['z-axis (g)'][start:end], color=color)

        for ax in axes:
            ax.grid(True)
            ax.legend()

        plt.tight_layout()
        plt.show()

        # Plot energy and gradient in a separate figure
        fig_energy_grad, ax_energy_grad = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        ax_energy_grad[0].set_title('Total Energy Over Time')
        ax_energy_grad[1].set_title('First-Order Differences of Accelerometer X-axis (g) Over Time')

        # Plot original data in light grey
        ax_energy_grad[0].plot(data_subset['energy'], color='lightgrey', label='Energy')
        ax_energy_grad[1].plot(data_subset['speed_x'], color='lightgrey', label='Gradient of X-axis (g)')

        for i, (start, end) in enumerate(segments):
            color = colors(i)
            ax_energy_grad[0].plot(range(start, end), data_subset['energy'][start:end], color=color)
            ax_energy_grad[1].plot(range(start, end), data_subset['speed_x'][start:end], color=color)

        for ax in ax_energy_grad:
            ax.grid(True)
            ax.legend()

        plt.tight_layout()
        plt.show()

        # Save each segment as a separate CSV
