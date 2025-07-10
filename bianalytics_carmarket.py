import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('Dataset_carmarket.csv')

"""## 1. Basic Visualizations (Matplotlib/Seaborn)"""

# 1.1 Price distribution
plt.figure(figsize=(12, 6))
sns.histplot(df['Price'], bins=50, kde=True, color='royalblue')
plt.title('Vehicle Price Distribution', fontsize=14)
plt.xlabel('Price', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.axvline(df['Price'].median(), color='red', linestyle='--', label=f'Median: {df["Price"].median():,.0f}')
plt.legend()
plt.show()

# 1.2 Top 10 brands by listing count
plt.figure(figsize=(12, 6))
brand_counts = df['Brand'].value_counts().nlargest(10)
sns.barplot(x=brand_counts.values, y=brand_counts.index, palette='viridis')
plt.title('Top 10 Brands by Listing Count', fontsize=14)
plt.xlabel('Number of Listings', fontsize=12)
plt.ylabel('Brand', fontsize=12)
plt.show()

"""## 2. Multivariate Analysis"""

# 2.1 Price vs Year by Fuel Type
plt.figure(figsize=(14, 8))
sns.scatterplot(data=df, x='Year', y='Price', hue='FuelType', 
                palette='Set2', alpha=0.7, size='EnginePower(HP)', sizes=(20, 200))
plt.title('Price vs Year by Fuel Type and Engine Power', fontsize=14)
plt.xlabel('Manufacturing Year', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 2.2 Correlation matrix
numeric_cols = df.select_dtypes(include=np.number).columns
plt.figure(figsize=(12, 8))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Numerical Features Correlation Matrix', fontsize=14)
plt.show()

"""## 3. Interactive Visualizations (Plotly)"""

# 3.1 Interactive price distribution by brand
fig = px.box(df, x='Brand', y='Price', color='TransmissionType',
             title='Price Distribution by Brand and Transmission Type',
             labels={'Price': 'Price', 'Brand': 'Brand'},
             hover_data=['Year', 'Mileage(km)'],
             log_y=True)
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()

# 3.2 Geographic distribution of listings
city_counts = df['City'].value_counts().reset_index()
fig = px.scatter_geo(city_counts, 
                    locations='City', 
                    locationmode='country names',
                    size='count',
                    hover_name='City',
                    projection="natural earth",
                    title='Geographic Distribution of Listings')
fig.show()

# 3.3 3D Visualization: Power-Engine Size-Price
fig = px.scatter_3d(df, x='EnginePower(HP)', y='EngineSize(cc)', z='Price',
                   color='FuelType', symbol='DriveTrain',
                   hover_name='Brand', opacity=0.7,
                   title='3D Analysis: Power vs Engine Size vs Price')
fig.update_layout(margin=dict(l=0, r=0, b=0, t=30))
fig.show()

"""## 4. Composite Dashboard Visualizations"""

# 4.1 Metrics dashboard
fig = make_subplots(rows=2, cols=2, 
                   subplot_titles=('Average Price by Brand', 
                                  'Mileage Distribution',
                                  'Fuel Type Composition',
                                  'Price vs Manufacturing Year'))

# Plot 1
avg_price = df.groupby('Brand')['Price'].mean().sort_values(ascending=False).nlargest(10)
fig.add_trace(go.Bar(x=avg_price.index, y=avg_price.values), row=1, col=1)

# Plot 2
fig.add_trace(go.Histogram(x=df['Mileage(km)'], nbinsx=50), row=1, col=2)

# Plot 3
fuel_counts = df['FuelType'].value_counts()
fig.add_trace(go.Pie(labels=fuel_counts.index, values=fuel_counts.values), row=2, col=1)

# Plot 4
fig.add_trace(go.Scatter(x=df['Year'], y=df['Price'], mode='markers', 
                        marker=dict(size=5, opacity=0.5)), row=2, col=2)

fig.update_layout(height=800, width=1000, title_text="Vehicle Market Analysis Dashboard", showlegend=False)
fig.show()

"""## 5. Time Series Analysis"""

# 5.1 Listing activity over time
df['ListingDate'] = pd.to_datetime(df['ListingDate'])
listings_by_date = df.resample('W', on='ListingDate').size()

fig = px.line(listings_by_date, x=listings_by_date.index, y=listings_by_date.values,
             title='Weekly Listing Activity Trend',
             labels={'x': 'Date', 'y': 'Number of Listings'})
fig.add_vrect(x0="2023-01-01", x1="2023-01-31", 
             annotation_text="January Dip", fillcolor="red", opacity=0.2)
fig.show()

"""## 6. Advanced Custom Visualizations"""

# 6.1 Vehicle specification radar chart
def plot_radar_chart(brand):
    brand_data = df[df['Brand'] == brand].agg({
        'Price': 'median',
        'EnginePower(HP)': 'median',
        'Year': 'median',
        'Mileage(km)': 'median',
        'EngineSize(cc)': 'median'
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=brand_data.values,
        theta=brand_data.index,
        fill='toself',
        name=brand
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(brand_data.values)*1.1]
            )),
        title=f'Brand Specifications: {brand}'
    )
    return fig

plot_radar_chart('BMW').show()

# 6.2 Animated scatter plot by year
px.scatter(df, x='EnginePower(HP)', y='Price', animation_frame='Year',
          color='FuelType', size='EngineSize(cc)',
          hover_name='Brand', size_max=60,
          range_x=[50, df['EnginePower(HP)'].max()],
          range_y=[1000, df['Price'].quantile(0.95)],
          title='Evolution of Power-Price Relationship Over Years')

# 6.3 Sunburst chart of vehicle hierarchy
fig = px.sunburst(df, path=['Brand', 'Series', 'Model'], 
                 values='Price', color='EnginePower(HP)',
                 title='Vehicle Hierarchy by Brand-Series-Model')
fig.show()
