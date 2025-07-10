import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('/Dataset_carmarket.csv', sep=',')

# Basic exploration
df.head()
df.info()
df.isna().sum()

# Statistics
df.describe()

"""# Research"""

# Group analysis
df.groupby('Brand')['Price'].mean()
df.groupby('City')['SellerType'].value_counts()

# Vehicle configuration filters
df['Powerful_German'] = np.where((df['Brand'].isin(['BMW', 'Mercedes', 'Audi'])) & 
                               (df['EnginePower(HP)'] > 300), 1, 0)
df[df.Powerful_German == 1]

df['Efficient_Compact'] = np.where((df['BodyType'] == 'Hatchback') & 
                                 (df['FuelType'].isin(['Hybrid', 'BEV'])) & 
                                 (df['Price'] < 30000), 1, 0)
df[df.Efficient_Compact == 1]

# Sorting by key metrics
df.sort_values(by=['Price']).head(10)  # Cheapest vehicles
df.sort_values(by=['Year'], ascending=False).head(10)  # Newest vehicles
df.sort_values(by=['Mileage(km)']).head(10)  # Lowest mileage

# Catalog analysis
df.Brand.value_counts()
df.FuelType.value_counts()
df.groupby('Brand').BodyType.value_counts()

"""# Pivot Tables"""

# Average price by brand and fuel type
price_table = pd.pivot_table(df, values='Price', 
                           index=['Brand'], 
                           columns=['FuelType'], 
                           aggfunc=np.mean)
price_table

# Mileage distribution by body type and drivetrain
mileage_table = pd.pivot_table(df, values='Mileage(km)', 
                             index=['BodyType'], 
                             columns=['DriveTrain'], 
                             aggfunc=np.median)
mileage_table

"""# Visualizations"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Price distribution by brand
plt.figure(figsize=(12,6))
sns.boxplot(x='Brand', y='Price', data=df)
plt.xticks(rotation=45)
plt.title('Price Distribution by Brand')

# Age vs Mileage
plt.scatter(2025-df['Year'], df['Mileage(km)'], alpha=0.3)
plt.title('Vehicle Age vs Mileage')
plt.xlabel('Age (years)')
plt.ylabel('Mileage (km)')

# Interactive plot of Price vs Power with filters
px.scatter(df, x='EnginePower(HP)', y='Price', 
          color='FuelType', 
          hover_name='ListingTitle',
          animation_frame='Year',
          size='EngineSize(cc)',
          facet_col='TransmissionType',
          log_y=True)

# Heatmap of average prices
pivot = df.pivot_table(index=['Brand'], 
                      columns=['BodyType'], 
                      values='Price', 
                      aggfunc=np.median)
sns.heatmap(pivot, cmap='YlOrRd')
plt.title('Median Price by Brand and Body Type')

"""# Vehicle Search Tools"""

# Search by parameters
min_year = int(input('Minimum year: '))
max_price = int(input('Maximum price: '))
max_mileage = int(input('Maximum mileage: '))
fuel_type = input('Fuel type (or leave blank): ')

query = (df['Year'] >= min_year) & \
        (df['Price'] <= max_price) & \
        (df['Mileage(km)'] <= max_mileage)

if fuel_type:
    query &= (df['FuelType'] == fuel_type)
    
df[query].sort_values(by=['Price'])

# Create a dream garage
garage_brands = input('Enter preferred brands (comma separated): ').split(',')
garage_bodytypes = input('Enter preferred body types (comma separated): ').split(',')

df['Dream_Garage'] = np.where((df['Brand'].isin(garage_brands)) & 
                            (df['BodyType'].isin(garage_bodytypes)) & 
                            (df['Price'] <= 50000), 1, 0)
df[df.Dream_Garage == 1].sort_values(by=['EnginePower(HP)'], ascending=False)

"""# Market Analysis"""

# Price trends by year
px.line(df.groupby('Year')['Price'].median().reset_index(), 
       x='Year', y='Price', 
       title='Median Price by Model Year')

# Fuel type distribution over time
pd.crosstab(df['Year'], df['FuelType']).plot(kind='area', stacked=True)
plt.title('Fuel Type Distribution Over Time')

"""# Conclusions"""
