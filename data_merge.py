# script by Rebecca Fokkink (s4604431)
# python code to merge pH data with vegetation data

# import some packages
import pandas as pd

# load the files
vegetation_df = pd.read_csv('updated_veg_data.csv')
ph_df = pd.read_csv('updated_ph_data.csv')

# merge the two dataframes
merged_df = pd.merge(vegetation_df, ph_df, on=['site_ID', 'grassland_type', 'restoration_measure'], how='inner')

# Save the updated DataFrame to a new CSV file
merged_df.to_csv('merged_ph_veg.csv', index=False)