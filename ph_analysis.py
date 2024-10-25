# script by Rebecca Fokkink (s4604431)
# python code to clean up data file on pH measurements

# import some packages
import pandas as pd
import numpy as np

# load the file
ph_data = pd.read_csv('data.csv')

# Split 'plot_ID' into separate columns: field_code, grassland_type, and restoration_measure
ph_data[['field_code', 'grassland_type', 'restoration_measure', 'plot_number']] = ph_data['Plot_ID'].str.split('_', expand=True)

# Select only the columns you need
ph_data = ph_data[['field_code', 'plot_number', 'grassland_type', 'restoration_measure', 'Depth', 'pH']]

# Save the modified DataFrame to a new CSV file
#ph_data.to_csv('modified_data.csv', index=False)

# Display the first few rows to verify
print(ph_data.head())