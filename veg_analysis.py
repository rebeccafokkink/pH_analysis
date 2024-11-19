# script by Rebecca Fokkink (s4604431)
# python code to clean up data file from vegetation survey

# import some packages
import pandas as pd
import numpy as np

# load the file
veg_data = pd.read_csv('veg_data.csv')

# Remove all spaces within the 'plot_id' column
veg_data['plot_id'] = veg_data['plot_id'].str.replace(' ', '', regex=False)

# Group by 'plot_id' and count unique species in 'gen_sp' for each plot
species_richness = veg_data.groupby('plot_id')['gen_sp'].nunique()

# Map this richness value back to the original dataframe by plot_number
veg_data['species_richness'] = veg_data['plot_id'].map(species_richness)

# Split 'plot_id' into separate columns: field_code, grassland_type, and restoration_measure
veg_data[['field_code', 'grassland_type', 'restoration_measure', 'plot_number']] = veg_data['plot_id'].str.split('_', expand=True)

# Define a function to generate site_IDs based on field_code and restoration_measure
def generate_site_id(row):
    # Use original 'restoration_measure' values in site_ID to preserve original data
    return f"{row['field_code']}_{row['restoration_measure']}_{row['plot_number']}"

# Apply the function to create the initial 'site_ID' column
veg_data['site_ID'] = veg_data.apply(generate_site_id, axis=1)

# Standardize the 'restoration_measure' column to 'TG' for both TG and TG2
veg_data['restoration_measure'] = veg_data['restoration_measure'].replace('TG2', 'TG')

# - For dry grasslands ('H'), group both 'T' and 'TG' as 'T' in 'restoration_measure' column
veg_data.loc[(veg_data['grassland_type'] == 'H') & (veg_data['restoration_measure'] == 'TG'), 'restoration_measure'] = 'T'

# Filter out rows where 'restoration_measure' is 'M'
veg_data = veg_data[veg_data['restoration_measure'] != 'M']

# Create a dictionary to map cover categories to percentages
cover_mapping = {
    'r': 2.5,
    '+': 2.5,
    '1': 2.5,
    '2m': 2.5,
    '2a': 8.5,
    '2b': 19,
    '3': 37.5,
    '4': 62.5,
    '5': 87.5
}

# Apply the mapping to create a new 'cover_%' column with values as integers
veg_data['cover_%'] = veg_data['cover'].map(cover_mapping).astype(int)

# Define the function to calculate Shannon-Wiener index
def shannon_wiener_index(group):
    # Calculate the total cover for each plot (site_id)
    total_cover = group['cover_%'].sum()

    # Calculate the proportion of each species' cover relative to the total cover
    proportions = group['cover_%'] / total_cover

    # Calculate the Shannon-Wiener index: H' = -Σ (p_i * ln(p_i))
    shannon_index = - (proportions * proportions.apply(np.log)).sum()

    return shannon_index

# Calculate Shannon-Wiener index for each site_ID
shannon_results = veg_data.groupby('site_ID').apply(shannon_wiener_index).reset_index(name='shannon_index').round(2)

# Merge the results back to the original dataset
veg_data = pd.merge(veg_data, shannon_results, on='site_ID', how='left')

# Select only the columns you need
veg_data = veg_data[['site_ID', 'grassland_type', 'restoration_measure', 'species_richness', 'shannon_index']]

# Group by plot-level identifiers and keep one row per unique plot
veg_data = veg_data.groupby(
    ['site_ID', 'grassland_type', 'restoration_measure'], as_index=False
).agg({
    'species_richness': 'first',  # Retain the first value for species richness
    'shannon_index': 'first'     # Retain the first value for Shannon index
})


# Save the updated DataFrame to a new CSV file
veg_data.to_csv('updated_veg_data.csv', index=False)