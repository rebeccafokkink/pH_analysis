# script by Rebecca Fokkink (s4604431)
# python code to clean up data file on pH measurements

# import some packages
import pandas as pd

# load the file
ph_data = pd.read_csv('data.csv')

# Split 'plot_ID' into separate columns: field_code, grassland_type, and restoration_measure
ph_data[['field_code', 'grassland_type', 'restoration_measure', 'plot_number']] = ph_data['Plot_ID'].str.split('_', expand=True)

# Select only the columns you need
ph_data = ph_data[['field_code', 'plot_number', 'grassland_type', 'restoration_measure', 'depth', 'pH']]

# Define a function to generate site_IDs based on field_code and restoration_measure
def generate_site_id(row):
    # Use original 'restoration_measure' values in site_ID to preserve original data
    return f"{row['field_code']}_{row['restoration_measure']}"

# Apply the function to create the initial 'site_ID' column
ph_data['site_ID'] = ph_data.apply(generate_site_id, axis=1)

# Standardize the 'restoration_measure' column to 'TG' for both TG and TG2
ph_data['restoration_measure'] = ph_data['restoration_measure'].replace('TG2', 'TG')

# - For dry grasslands ('H'), group both 'T' and 'TG' as 'T' in 'restoration_measure' column
ph_data.loc[(ph_data['grassland_type'] == 'H') & (ph_data['restoration_measure'] == 'TG'), 'restoration_measure'] = 'T'

# Filter out rows where 'restoration_measure' is 'M'
ph_data = ph_data[ph_data['restoration_measure'] != 'M']

# Save the updated DataFrame to a new CSV file
ph_data.to_csv('updated_dataset.csv', index=False)