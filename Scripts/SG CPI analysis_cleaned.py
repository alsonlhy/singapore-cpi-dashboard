import pandas as pd

df_price= pd.read_csv('Consumer_Items_Avg.csv')
df_cpi = pd.read_csv('cpi_2019base.csv')

#Mapping Dictonary for DataSeries
series_mapping = {
    'Bread': ('Bread', 'Ordinary White Bread (Per 400 Gram)', 'Vitamin Enriched Bread (Per 400 Gram)', 'Wholemeal Bread (Per 400 Gram)'),
    'Rice': ('Rice', 'Premium Thai Rice (Per 5 Kilogram)'),
    'Noodles & Pasta': ('Noodles & Pasta', 'Instant Noodles (Per 5 Packets)'),
    'Pork, Chilled': ('Pork, Chilled', 'Lean Pork, Chilled (Per Kilogram)', 'Streaky Pork, Chilled (Per Kilogram)', 'Pork Rib Bones, Chilled (Per Kilogram)'),
    'Beef, Chilled': ('Beef, Chilled', 'Beef, Chilled (Per Kilogram)'),
    'Mutton, Chilled': ('Mutton, Chilled', 'Mutton, Chilled (Per Kilogram)'),
    'Poultry, Chilled': ('Poultry, Chilled', 'Whole Chicken, Chilled (Per Kilogram)', 'Chicken Wing, Chilled (Per Kilogram)', 'Duck, Chilled (Per Kilogram)'),
    'Meat, Frozen': ('Meat, Frozen', 'Beef Cube, Frozen (Per 500 Gram)', 'Lean Pork, Frozen (Per 500 Gram)', 'Pork Rib Bones, Frozen (Per 500 Gram)', 'Whole Chicken, Frozen (Each)', 'Chicken Wing, Frozen (Per 2 Kilogram)'),
    'Fish & Seafood': ('Fish & Seafood', 'Cod Fish (Per Kilogram)', 'Gold Banded Scad (Kuning) (Per Kilogram)', 'Flowery Grouper (Per Kilogram)', 'White Pomfret (Per Kilogram)', 'Salmon (Per Kilogram)', 'Sea Bass (Per Kilogram)', 'Sea Bream (Ang Ko Li) (Per Kilogram)', 'Golden Snapper (Per Kilogram)', 'Spanish Mackerel (Batang) (Per Kilogram)', 'Threadfin (Kurau) (Per Kilogram)', 'Small Prawns (Per Kilogram)', 'Medium Prawns (Per Kilogram)', 'Squids (Per Kilogram)'),
    'Milk, Cheese & Eggs': ('Milk, Cheese & Eggs', 'Fresh Milk (Per Litre)', 'Cheese (Per 12 Slices)'),
    'Formula Milk Powder': ('Formula Milk Powder', 'Infant Milk Powder (Per 100 Gram)'),
    'Eggs': ('Eggs', 'Hen Eggs (Per 10)'),
    'Cooking Oils': ('Cooking Oils', 'Cooking Oil (Per 2 Kilogram)'),
    'Fruits': ('Fruits', 'Bananas (Per Kilogram)', 'Papaya (Per Kilogram)', 'Watermelon (Per Kilogram)', 'Grapes (Per Kilogram)', 'Orange (Each)', 'Apple (Each)', 'Pear (Each)',),
    'Vegetables': ('Vegetables', 'Broccoli (Per Kilogram)', 'Cabbage (Per Kilogram)', 'Chinese Kale (Kailan) (Per Kilogram)', 'Small Mustard (Chye Sim) (Per Kilogram)', 'Spinach (Bayam) (Per Kilogram)', 'Tomatoes (Per Kilogram)', 'Potatoes (Per Kilogram)', 'Carrots (Per Kilogram)'),
    'Coffee & Tea':('Coffee & Tea', 'Instant Coffee (Per 200 Gram)'),
    'Sugar': ('Sugar', 'White Sugar (Per 2 Kilogram)'),
    'Soft Drinks': ('Soft Drinks', 'Aerated Soft Drinks (Per 4 Cans)', 'Non-Aerated Soft Drinks (Per 6 Packets)'),
    'Beer': ('Beer', 'Beer (Per 6 Cans)'),
    'Cigarettes': ('Cigarettes', 'Cigarettes (Per Pack)'),
    'Petrol': ('Petrol', 'Diesel (Per Litre)', 'Petrol, 98 Octane (Per Litre)', 'Petrol, 95 Octane (Per Litre)', 'Petrol, 92 Octane (Per Litre)', 'Liquefied Petroleum Gas (LPG) (Per Kilogram)'),
    'Food Courts & Coffee Shops':('Food Courts & Coffee Shops', 'Coffee/Tea Without Milk (Per Cup)', 'Coffee/Tea With Milk (Per Cup)', 'Fishball Noodle (Per Bowl)', 'Mee Rebus (Per Bowl)', 'Chicken Rice (Per Plate)', 'Economical Rice (1 Meat & 2 Vegetables) (Per Plate)', 'Roti Prata (Plain) (Per Piece)', 'Fried Carrot Cake (Per Plate)', 'Ice Kachang (Per Bowl)', 'Chicken Nasi Briyani (Per Plate)')
}

def standardize_series(series):
    for category, items in series_mapping.items():
        if series in items:
            return category
    return series  # Return the original if no match found



# Data Cleaning for df_price
date_columns = [col for col in df_price.columns if col != 'DataSeries']

df_price[date_columns] = df_price[date_columns].apply(pd.to_numeric, errors='coerce')

df_price_long = pd.melt(df_price, id_vars=['DataSeries'],
                        value_vars=date_columns, var_name='Date',
                        value_name='Price_Index')

df_price_long['Date'] = pd.to_datetime(df_price_long['Date'], format='%Y%b', errors='coerce')

df_price_long['StandardSeries'] = df_price_long['DataSeries'].apply(standardize_series)

df_price_long = df_price_long.sort_values(['StandardSeries', 'Date'])

df_price_long['Price_Index'].fillna(df_price_long['Price_Index'].median(), inplace=True)

df_price_long['Year'] = df_price_long['Date'].dt.year
df_price_long['Month'] = df_price_long['Date'].dt.month

df_price_long = df_price_long[df_price_long['Year'] >= 2014]

# Data Cleaning for df_cpi
date_columns = [col for col in df_cpi.columns if col != 'DataSeries']

df_cpi[date_columns] = df_cpi[date_columns].apply(pd.to_numeric, errors='coerce')

df_cpi_long = pd.melt(df_cpi, id_vars=['DataSeries'],
                      value_vars=date_columns, var_name='Date',
                      value_name='CPI_Index')

df_cpi_long['Date'] = pd.to_datetime(df_cpi_long['Date'], format='%Y%b', errors='coerce')

df_cpi_long['StandardSeries'] = df_cpi_long['DataSeries'].apply(standardize_series)

df_cpi_long = df_cpi_long.sort_values(['StandardSeries', 'Date'])

df_cpi_long['CPI_Index'].fillna(df_cpi_long['CPI_Index'].median(), inplace=True)

df_cpi_long['Year'] = df_cpi_long['Date'].dt.year
df_cpi_long['Month'] = df_cpi_long['Date'].dt.month

df_cpi_long = df_cpi_long[df_cpi_long['Year'] >= 2014]

print(df_cpi_long.head())

# Ensure StandardSeries has consistent formatting
df_price_long['StandardSeries'] = df_price_long['StandardSeries'].str.strip()
df_cpi_long['StandardSeries'] = df_cpi_long['StandardSeries'].str.strip()

# 4. Merge the two dataframes
df_merged = pd.merge(df_price_long, df_cpi_long[['StandardSeries', 'Year', 'Month', 'CPI_Index']],
                     on=['StandardSeries', 'Year', 'Month'],
                     how='left')  # Use 'left' to keep only matches for df_price_long


# Sort the merged dataframe
df_merged = df_merged.sort_values(['StandardSeries', 'Year', 'Month'])

#Real Price
df_merged['Real Price'] = df_merged['Price_Index'] / df_merged['CPI_Index'] * 100

# Rename columns appropriately
df_merged = df_merged[['DataSeries', 'Price_Index', 'Real Price', 'CPI_Index', 'Year', 'Month', 'StandardSeries']]
df_merged.columns = ['DataSeries', 'Nominal Price', 'Real Price', 'CPI', 'Year', 'Month', 'StandardSeries']

# Save the merged dataframe to CSV
df_merged.to_csv('tableau_data.csv', index=False)
print(df_merged.head())