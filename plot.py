import pandas as pd
import matplotlib.pyplot as plt
import itertools

# Load the individual movement CSV files
movement_1 = pd.read_csv("C:/Users/andre/Downloads/movement_1.csv")
movement_2 = pd.read_csv("C:/Users/andre/Downloads/movement_2.csv")
movement_3 = pd.read_csv("C:/Users/andre/Downloads/movement_3.csv")

# Create all possible combinations of the three movements
movements = [movement_1, movement_2, movement_3]
movement_combinations = list(itertools.product(movements, repeat=3))

# Function to plot the combined movements
def plot_combined_movement(data, movement):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 16), sharex=True)
    
    # Accelerometer data
    ax1.plot(data.index, data['x-axis (g)'], label='x-axis (g)', color='r')
    ax1.plot(data.index, data['y-axis (g)'], label='y-axis (g)', color='g')
    ax1.plot(data.index, data['z-axis (g)'], label='z-axis (g)', color='b')
    ax1.set_ylabel('Acceleration (g)')
    ax1.set_title(f'Accelerometer Data - Combined Movement {movement}')
    ax1.legend()
    
    # Gyroscope data
    ax2.plot(data.index, data['x-axis (deg/s)'], label='x-axis (deg/s)', color='r')
    ax2.plot(data.index, data['y-axis (deg/s)'], label='y-axis (deg/s)', color='g')
    ax2.plot(data.index, data['z-axis (deg/s)'], label='z-axis (deg/s)', color='b')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Angular Velocity (deg/s)')
    ax2.set_title(f'Gyroscope Data - Combined Movement {movement}')
    ax2.legend()
    
    plt.show()

# Combine and plot all movement combinations
for i, combination in enumerate(movement_combinations, 1):
    combined_data = pd.concat(combination, ignore_index=True)
    combined_data = combined_data.drop(columns=['elapsed (s)'])
    plot_combined_movement(combined_data, f'Combination {i}')
