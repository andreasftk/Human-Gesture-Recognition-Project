import os
import pandas as pd
import matplotlib.pyplot as plt

import os
import pandas as pd

def merge_csv_files(accel_folder, gyro_folder, output_folder):
    try:
        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)
        
        # List all files in the accelerometer and gyroscope folders
        accel_files = [f for f in os.listdir(accel_folder) if f.endswith('Accelerometer.csv')]
        gyro_files = [f for f in os.listdir(gyro_folder) if f.endswith('Gyroscope.csv')]
        
        if not accel_files:
            print("No accelerometer files found.")
        if not gyro_files:
            print("No gyroscope files found.")
        
        for accel_file in accel_files:
            # Find the corresponding gyroscope file
            file_prefix = accel_file.replace('Accelerometer.csv', '')
            gyro_file = file_prefix + 'Gyroscope.csv'
            
            if gyro_file in gyro_files:
                try:
                    # Read accelerometer and gyroscope data
                    accel_df = pd.read_csv(os.path.join(accel_folder, accel_file))
                    gyro_df = pd.read_csv(os.path.join(gyro_folder, gyro_file))
                    
                    # Merge the two dataframes on the common columns 'epoc (ms)' and 'timestamp (+0300)'
                    merged_df = pd.merge(
                        accel_df, 
                        gyro_df,
                        left_index=True, right_index=True
                    
                    )
                    columns_to_drop = ['epoc (ms)_x', 'timestamp (+0300)_x', 'elapsed (s)_x', 
                                       'epoc (ms)_y', 'timestamp (+0300)_y', 'elapsed (s)_y']
                    merged_df.drop(columns=columns_to_drop, inplace=True)
                    
                    # Save the merged dataframe to a new CSV file in the output folder
                    output_file_path = os.path.join(output_folder, file_prefix + 'Both.csv')
                    merged_df.to_csv(output_file_path, index=False)
                    print(f'Merged file saved: {output_file_path}')
                except Exception as e:
                    print(f"Error processing files {accel_file} and {gyro_file}: {e}")
            else:
                print(f"Corresponding gyroscope file for {accel_file} not found.")
    except Exception as e:
        print(f"Error in merging files: {e}")

# Define folder paths
accel_folder = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/accelerometer'
gyro_folder = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/gyroscope'
output_folder = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/merged'

# Call the function to merge CSV files
merge_csv_files(accel_folder, gyro_folder, output_folder)


def plot_merged_files(merged_folder):
    # List all files in the merged folder
    merged_files = [f for f in os.listdir(merged_folder) if f.endswith('Both.csv')]
    
    for merged_file in merged_files:
        file_path = os.path.join(merged_folder, merged_file)
        try:
            # Read the merged CSV file
            merged_df = pd.read_csv(file_path)
            
             # Create subplots for accelerometer and gyroscope data
            fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
            
            # Plot accelerometer data
            axs[0].plot(merged_df['x-axis (g)'], label='Accelerometer X-axis')
            axs[0].plot(merged_df['y-axis (g)'], label='Accelerometer Y-axis')
            axs[0].plot(merged_df['z-axis (g)'], label='Accelerometer Z-axis')
            axs[0].set_title(f'Accelerometer Data: {merged_file}')
            axs[0].set_ylabel('Acceleration (g)')
            axs[0].legend()
            
            # Plot gyroscope data
            axs[1].plot(merged_df['x-axis (deg/s)'], label='Gyroscope X-axis')
            axs[1].plot(merged_df['y-axis (deg/s)'], label='Gyroscope Y-axis')
            axs[1].plot(merged_df['z-axis (deg/s)'], label='Gyroscope Z-axis')
            axs[1].set_title(f'Gyroscope Data: {merged_file}')
            axs[1].set_xlabel('Sample')
            axs[1].set_ylabel('Angular Velocity (deg/s)')
            axs[1].legend()
            
            # Adjust layout to prevent overlap
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error reading or plotting the file {merged_file}: {e}")

# Define the merged folder path
merged_folder = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/merged'

# Call the function to plot the data from all merged files
plot_merged_files(merged_folder)


def plot_merged_file(file_path):
    # Read the merged CSV file
    try:
        merged_df = pd.read_csv(file_path)
        
        # Plot accelerometer data
        plt.figure(figsize=(10, 6))
        plt.plot(merged_df['x-axis (g)'], label='Accelerometer X-axis')
        plt.plot(merged_df['y-axis (g)'], label='Accelerometer Y-axis')
        plt.plot(merged_df['z-axis (g)'], label='Accelerometer Z-axis')
        plt.title('Accelerometer Data')
        plt.xlabel('Sample')
        plt.ylabel('Acceleration (g)')
        plt.legend()
        plt.show()
        
        # Plot gyroscope data
        plt.figure(figsize=(10, 6))
        plt.plot(merged_df['x-axis (deg/s)'], label='Gyroscope X-axis')
        plt.plot(merged_df['y-axis (deg/s)'], label='Gyroscope Y-axis')
        plt.plot(merged_df['z-axis (deg/s)'], label='Gyroscope Z-axis')
        plt.title('Gyroscope Data')
        plt.xlabel('Sample')
        plt.ylabel('Angular Velocity (deg/s)')
        plt.legend()
        plt.show()
        
    except Exception as e:
        print(f"Error reading or plotting the file: {e}")

# Define the merged file path
merged_file_path = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/merged/sampleBoth.csv'

# Call the function to plot the data
# plot_merged_file(merged_file_path)
