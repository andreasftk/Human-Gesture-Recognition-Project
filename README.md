Brief descriptions of each file:

1. **merge_csv.py**
   * **Purpose:** Merges separate `_Gyroscope.csv` and `_Accelerometer.csv` files into a single file named `Both.csv`.
   * **Usage:** Run this script first to consolidate data from gyroscope and accelerometer sensors.
2. **data_segmentation.py**
   * **Purpose:** Segments the `Both.csv` file into movement and no-movement categories.
   * **Usage:** Execute this script after `merge_csv.py` to categorize the merged data based on movement. Select one of the csv files from the previous step and find the best threshold to seperate the movement from the non movement. This process needs to be executed for each `Both.csv` file.
3. **aiot_data_engineering.ipynb**
   * **Purpose:** Notebook for filtering and windowing the segmented data.
   * **Usage:** Use this notebook to apply filters and create temporal windows for further analysis.
4. **aiot_dataset_creation.ipynb**
   * **Purpose:** Notebook for storing processed data into a database.
   * **Usage:** Execute this notebook to save the preprocessed data into a database for easy access and management.
5. **aiot_project.ipynb**
   * **Purpose:** Notebook for data preparation and building a neural network model.
   * **Usage:** This notebook covers data preprocessing steps and the development of a neural network model tailored for the IoT project.

### Setup Instructions

* **Environment Setup:** Ensure Python 3.x environment with necessary libraries (pandas, numpy) installed.
* **Notebook Execution:** Open Jupyter notebooks (`aiot_data_engineering.ipynb`, `aiot_dataset_creation.ipynb`, `aiot_project.ipynb`) in JupyterLab or Jupyter Notebook and execute cells sequentially.

### Notes

* Modify file paths of the files used inside the python code.
* Ensure dependencies are installed before running any scripts or notebooks.
