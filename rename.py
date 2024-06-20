import os

# Define the base directory
base_dir = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/segments_renamed'

# Define the folder pattern
folder_pattern = 'data_D_'

# Initialize a counter for the new file names
counter = 1

# Iterate through the folders
for i in range(1, 7):  # Assuming there are 6 folders as in the example
    folder_name = f"{folder_pattern}{i}(row)"
    folder_path = os.path.join(base_dir, folder_name)
    
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate through the files in the folder
        for file_name in os.listdir(folder_path):
            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)
            
            # Check if the file is a CSV and does not end with '_WithMovement.csv'
            if file_name.endswith('.csv') and not file_name.endswith('_WithMovement.csv'):
                # Create the new file name
                new_file_name = f"data_D_{counter}.csv"
                new_file_path = os.path.join(folder_path, new_file_name)
                
                # Rename the file
                os.rename(file_path, new_file_path)
                
                # Increment the counter
                counter += 1

print("Files have been renamed successfully.")
