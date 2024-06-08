import pandas as pd

def merge_sensors_data(accelerometer_file, gyroscope_file, output_file):
    # Load the CSV files
    accelerometer_df = pd.read_csv(accelerometer_file)
    gyroscope_df = pd.read_csv(gyroscope_file)
    
    # Merge dataframes on elapsed time
    merged_df = pd.merge_asof(accelerometer_df, gyroscope_df, on='elapsed (s)', direction='nearest', suffixes=('_accel', '_gyro'))
    
    # Select relevant columns
    merged_df = merged_df[['elapsed (s)', 'x-axis (g)', 'y-axis (g)', 'z-axis (g)', 'x-axis (deg/s)', 'y-axis (deg/s)', 'z-axis (deg/s)']]
    
    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_file, index=False)

# Define file paths
accelerometer_file = 'C:/Users/andre/Downloads/KaresiouWear_2024-06-08T21.06.27.834_F5174DCC3C91_Accelerometer.csv'
gyroscope_file = 'C:/Users/andre/Downloads/KaresiouWear_2024-06-08T21.06.27.834_F5174DCC3C91_Gyroscope.csv'
output_file = 'C:/Users/andre/Downloads/merged_sensors_data2.csv'

# Call the function
merge_sensors_data(accelerometer_file, gyroscope_file, output_file)
