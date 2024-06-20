import os
import shutil

# Define the base directory and the new directory
base_dir = 'G:/Other computers/My Computer/8 Εξάμηνο/Αλγοριθμικές Θεμελιώσεις Δικτύων Αισθητήρων/Human Gesture Recognition Project/raw_data/segments_renamed'
new_dir = os.path.join(base_dir, 'class_B')

# Create the new directory if it doesn't exist
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

# Define the folder pattern
folder_pattern = 'data_B_'

# Iterate through the folders
for i in range(1, 7):  # Assuming there are 6 folders as in the example
    folder_name = f"{folder_pattern}{i}(mp)"
    folder_path = os.path.join(base_dir, folder_name)
    
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate through the files in the folder
        for file_name in os.listdir(folder_path):
            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)
            
            # Check if the file is a CSV
            if file_name.endswith('.csv'):
                # Construct the new file path
                new_file_path = os.path.join(new_dir, file_name)
                
                # Move the file to the new directory
                shutil.move(file_path, new_file_path)

print("Files have been moved to the class_A folder successfully.")
