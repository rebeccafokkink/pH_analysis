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
ph_data = ph_data[['field_code', 'plot_number', 'grassland_type', 'restoration_measure', 'depth', 'pH']]

# Define a function to generate site_IDs based on field_code and restoration_measure
def generate_site_id(row):
    if row['restoration_measure'] == 'TG':
        return f"{row['field_code']}_TG"
    elif row['restoration_measure'] == 'TG2':
        return f"{row['field_code']}_TG2"
    else:
        return f"{row['field_code']}_{row['restoration_measure']}"

# Apply the function to create a new 'site_ID' column
ph_data['site_ID'] = ph_data.apply(generate_site_id, axis=1)

# Standardize the 'restoration_measure' column to 'TG' for both TG and TG2
ph_data['restoration_measure'] = ph_data['restoration_measure'].replace('TG2', 'TG')

# Save the updated DataFrame to a new CSV file
ph_data.to_csv('updated_dataset.csv', index=False)