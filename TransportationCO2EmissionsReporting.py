# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import warnings
import os
import matplotlib.pyplot as plt

absolute_path = os.path.dirname(__file__)


pd.set_option('display.max_colwidth', 0)
pd.set_option('display.max_columns', None)
pd.options.display.max_seq_items = 2000
warnings.filterwarnings('ignore')

# + language="html"
# <style>
# .dataframe td {
#     white-space: nowrap;
# }
# </style>
# -

# ### Initial Datasets Import
# #### Import Shipped Order Lines

df_lines = pd.read_csv(os.path.join(absolute_path,'data/order_lines.csv'), index_col = 0)
print("{:,} order lines to process".format(len(df_lines)))
df_lines.head()

# #### Import Master Data: Unit of Measure Conversions to (kg)

# +
df_uom = pd.read_csv(os.path.join(absolute_path,'data/uom_conversions.csv'), index_col = 0)
print("{:,} Unit of Measure Conversions".format(len(df_uom)))

# Join
df_join = df_lines.copy()
COLS_JOIN = ['Item Code']
df_join = pd.merge(df_join, df_uom, on=COLS_JOIN, how='left', suffixes=('', '_y'))
df_join.drop(df_join.filter(regex='_y$').columns.tolist(),axis=1, inplace=True)
print("{:,} records".format(len(df_join)))
df_join.head()
# -

# #### Import Distances

df_dist = pd.read_csv(os.path.join(absolute_path,'data/' + 'distances.csv'), index_col = 0)
# Location
df_dist['Location'] = df_dist['Customer Country'].astype(str) + ', ' + df_dist['Customer City'].astype(str)
df_dist.head()

# #### Import Cities GPS Locations

df_gps = pd.read_csv(os.path.join(absolute_path,'Data/' + 'gps_locations.csv'), index_col = 0)
print("{:,} Locations".format(len(df_gps)))
df_gps.head()



# ### Data Processing
# #### Merge Distance with GPS Locations

df_dist = pd.merge(df_dist, df_gps, on='Location', how='left', suffixes=('', '_y'))
df_dist.drop(df_dist.filter(regex='_y$').columns.tolist(),axis=1, inplace=True)
df_dist

# #### Final Join to build records

COLS_JOIN = ['Warehouse Code', 'Customer Code']
df_join = pd.merge(df_join, df_dist, on = COLS_JOIN, how='left', suffixes=('', '_y'))
df_join.drop(df_join.filter(regex='_y$').columns.tolist(),axis=1, inplace=True)
print("{:,} records".format(len(df_join)))
df_join



# ### Calculation at order line level

# Calculation of 'KG' column should be before its usage
df_join['KG'] = df_join['Units'] * df_join['Conversion Ratio']

# +
# Calculation @ line level
df_line = df_join.copy()

dict_co2e = dict(zip(['Air' ,'Sea', 'Road', 'Rail'], [2.1, 0.01, 0.096, 0.028]))
MODES = ['Road', 'Rail','Sea', 'Air']
for mode in MODES:
    df_line['CO2 ' + mode] = df_line['KG'].astype(float)/1000 * df_line[mode].astype(float) * dict_co2e[mode]
df_line['CO2 Total'] = df_line[['CO2 ' + mode for mode in MODES]].sum(axis = 1)
df_line.to_csv(os.path.join(absolute_path,'data/detailed_report.csv'))
df_line.head()
# -



# ### Calculation at order level

# +

# Agg by order
GPBY_ORDER = ['Date', 'Month-Year', 
        'Warehouse Code', 'Warehouse Name', 'Warehouse Country', 'Warehouse City',
        'Customer Code', 'Customer Country', 'Customer City','Location', 'GPS 1', 'GPS 2', 
        'Road', 'Rail', 'Sea', 'Air',
        'Order Number']
df_agg = pd.DataFrame(df_join.groupby(GPBY_ORDER)[['Units', 'KG']].sum())
df_agg.reset_index(inplace = True)
df_agg.head()
# -



# #### Calculate CO2 = f(KG, Ratios)

# CO2 Emissions
dict_co2e = dict(zip(['Air' ,'Sea', 'Road', 'Rail'], [2.1, 0.01, 0.096, 0.028]))
MODES = ['Road', 'Rail','Sea', 'Air']
for mode in MODES:
    df_agg['CO2 ' + mode] = df_agg['KG'].astype(float)/1000 * df_agg[mode].astype(float) * dict_co2e[mode]
df_agg['CO2 Total'] = df_agg[['CO2 ' + mode for mode in MODES]].sum(axis = 1)
df_agg.head()

# #### Final mapping for visualization

# Mapping the delivery Mode
df_agg['Delivery Mode'] = df_agg[MODES].astype(float).apply(
    lambda t: [mode if t[mode]>0 else '-' for mode in MODES], axis = 1)
dict_map = dict(zip(df_agg['Delivery Mode'].astype(str).unique(), 
  [i.replace(", '-'",'').replace("'-'",'').replace("'",'') for i in df_agg['Delivery Mode'].astype(str).unique()]))
df_agg['Delivery Mode'] = df_agg['Delivery Mode'].astype(str).map(dict_map)
df_agg

# Save Final Report
df_agg.to_csv(os.path.join(absolute_path,'data/final_report.csv'))

def plot_co2_emissions(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Calculate the sum of CO2 emissions for each transportation mode
    total_co2_road = df['CO2 Road'].sum()
    total_co2_rail = df['CO2 Rail'].sum()
    total_co2_sea = df['CO2 Sea'].sum()
    total_co2_air = df['CO2 Air'].sum()
    total_co2 = df['CO2 Total'].sum()
    
    # Data to plot
    modes = ['Road', 'Rail', 'Sea', 'Air', 'Total']
    emissions = [total_co2_road, total_co2_rail, total_co2_sea, total_co2_air, total_co2]
    
    # Create a bar diagram
    plt.figure(figsize=(10, 6))
    plt.bar(modes, emissions, color=['blue', 'orange', 'green', 'red', 'purple'])
    
    # Adding labels and title
    plt.xlabel('Transportation Mode')
    plt.ylabel('CO2 Emissions (kg CO2e)')
    plt.title('Total CO2 Emissions by Transportation Mode')
    
    # Display numeric labels on each bar
    for i, v in enumerate(emissions):
        plt.text(i, v + max(emissions) * 0.01, f"{v:.2f}", ha='center', va='bottom')
    
    # Show plot
    plt.tight_layout()
    plt.show()

# Assuming your CSV file is in the same directory as the script
# If it's in a different directory, provide the full path to the CSV file
csv_file_path = os.path.join(absolute_path, 'data/final_report.csv')

# Call the function to plot the CO2 emissions
plot_co2_emissions(csv_file_path)