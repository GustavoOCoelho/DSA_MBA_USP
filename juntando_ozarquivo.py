import pandas as pd
import glob

# Specify the path to the directory containing the CSV files
path = '/Users/gustavooliveiracoelho/hello/estados/'

# Use glob to match the pattern for all CSV files in the directory
all_files = glob.glob(path + "*.csv")

# Initialize an empty list to hold the DataFrames
dfs = []

# Loop over the list of files and read each file into a DataFrame, then append to the list
for filename in all_files:
    df = pd.read_csv(filename)
    dfs.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('RREO_COMBINADO_estados.csv', index=False)