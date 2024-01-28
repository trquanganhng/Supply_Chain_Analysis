# source Case Study: https://data.mendeley.com/datasets/8gx2fvg2k6/5

import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pio.templates.default = "plotly_white"

data = pd.read_csv("cleaned_DataCoSupplyChainDataset.csv", encoding='ISO-8859-1')

## 1 Days for Shipping vs. Days for Shipment (Scheduled)
def analyze_shipping_times():
    # Filter rows where 'Days for shipping (real)' and 'Days for shipment (scheduled)' are greater than 0
    filtered_data = data[(data['Days for shipping (real)'] > 0) & (data['Days for shipment (scheduled)'] > 0)]
    
    # Remove duplicate OrderID cases
    filtered_data = filtered_data.drop_duplicates(subset=['Order Id'])
    
    # Create a scatter plot
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1,
                        specs=[[{"type": "scatter"}], [{"type": "table"}]],
                        subplot_titles=("Actual vs. Scheduled Days for Shipping", "Details of the combination"))
    
    # Add scatter plot to the first subplot
    fig.add_trace(go.Scatter(x=filtered_data['Days for shipment (scheduled)'],
                             y=filtered_data['Days for shipping (real)'],
                             mode='markers',
                             name='Orders',
                             marker=dict(color='blue', size=5)),
                 row=1, col=1)
    
    # Add diagonal line for reference to the first subplot
    fig.add_trace(go.Scatter(x=[filtered_data['Days for shipment (scheduled)'].min(), filtered_data['Days for shipment (scheduled)'].max()],
                             y=[filtered_data['Days for shipment (scheduled)'].min(), filtered_data['Days for shipment (scheduled)'].max()],
                             mode='lines',
                             name='Ideal'),
                 row=1, col=1)

    # Create a table with the number of orders for each plot and add it to the second subplot
    order_counts = filtered_data.groupby(['Days for shipment (scheduled)', 'Days for shipping (real)']).size().reset_index(name='Count')
    fig.add_trace(go.Table(header=dict(values=['Scheduled Days', 'Actual Days', 'Count']),
                            cells=dict(values=[order_counts['Days for shipment (scheduled)'],
                                               order_counts['Days for shipping (real)'],
                                               order_counts['Count']])),
                 row=2, col=1)
    
    # Update layout
    fig.update_layout(title_text="Actual vs. Scheduled Days for Shipping with Order Counts",
                      showlegend=False)
    
    # Show plot
    fig.show()

## 2 Late Delivery Risk
def analyze_late_delivery_risk():
    # Filter rows where 'Days for shipping (real)' and 'Days for shipment (scheduled)' are greater than 0
    filtered_data = data[(data['Days for shipping (real)'] > 0) & (data['Days for shipment (scheduled)'] > 0)]
    
    # Filter late deliveries
    late_deliveries = filtered_data[filtered_data['Days for shipping (real)'] > filtered_data['Days for shipment (scheduled)']]
    
    # Calculate the total number of unique OrderIDs
    total_unique_orders = len(filtered_data['Order Id'].unique())
    
    # Calculate the total number of unique delayed OrderIDs
    total_unique_delayed_orders = len(late_deliveries['Order Id'].unique())
    
    # Calculate the percentage of delayed occurrence for all orders
    percentage_delayed_all_orders = round((total_unique_delayed_orders / total_unique_orders) * 100, 2) if total_unique_orders > 0 else 0
    
    # Print the total unique orders, total unique delayed orders, and the percentage delayed for all orders
    print("Total Orders counted:", total_unique_orders)
    print("Total Delayed Orders counted:", total_unique_delayed_orders)
    print("Percentage Delayed of all Orders:", f"{percentage_delayed_all_orders}%")

## 3 Distribution of Customer Segments
def distribution_Customer_Segments():
    # Remove duplicate OrderID cases
    unique_data = data.drop_duplicates(subset=['Order Id'])
    
    # Calculate the quantity of each Customer Segment
    segment_counts = unique_data['Customer Segment'].value_counts().reset_index()
    segment_counts.columns = ['Customer Segment', 'Quantity']

    # Create a pie chart for the Customer Segment column with quantity
    fig = px.pie(segment_counts, names='Customer Segment', values='Quantity', title='Distribution of Customer Segments')
    fig.show()

## 4 Distribution of Category
def distribution_Category():
    # Count the occurrences of each category
    value_counts = data['Category Name'].value_counts().reset_index()
    value_counts.columns = ['Category Name', 'Quantity']

    # Create a bar chart
    fig = px.bar(value_counts, x='Category Name', y='Quantity', title='Distribution of Product Categories')
    fig.update_xaxes(title='Category Name')
    fig.update_yaxes(title='Quantity')
    fig.show()

## 5 Distribution of Department
def distribution_Department():
    # Count the occurrences of each department
    value_counts = data['Department Name'].value_counts().reset_index()
    value_counts.columns = ['Department Name', 'Quantity']

    # Create a bar chart for the Department Name column
    fig = px.bar(value_counts, x='Department Name', y='Quantity', title='Distribution of Department Names')
    fig.update_xaxes(title='Department Name')
    fig.update_yaxes(title='Quantity')
    fig.show()

## 6 Correlation between category and department
def Category_Department():
    # Pivot the data to create a matrix of department and category counts
    pivot_data = data.pivot_table(index='Department Name', columns='Category Name', aggfunc='size', fill_value=0)

    # Create a heatmap
    fig = px.imshow(pivot_data,
                labels=dict(x="Category Name", y="Department Name", color="Number of Orders"),
                x=pivot_data.columns,
                y=pivot_data.index,
                color_continuous_scale='Viridis',
                title='Correlation between Department and Category (Heatmap)')
    fig.update_xaxes(side="top")
    fig.show()

## 7 Correlation between orders and regions
def bublemap_orders_by_region():
    # Aggregate order quantity by region
    region_order_quantity = data.groupby('Order Country')['Order Item Quantity'].sum().reset_index()

    # Create a bubble map
    fig = px.scatter_geo(region_order_quantity,
                        locations='Order Country',
                        locationmode='country names',
                        size='Order Item Quantity',
                        hover_name='Order Country',
                        projection='natural earth',
                        title='Order Quantity by Country',
                        color='Order Item Quantity',
                        color_continuous_scale='Viridis',
                        size_max=50)
    fig.show()

## 8 Summary of orders and sales in 2015, 2016, and 2017
def visualize_orders_sales():
    # Convert 'order date (DateOrders)' column to datetime format
    data['order date (DateOrders)'] = pd.to_datetime(data['order date (DateOrders)'])

    # Extract year and month from the 'order date (DateOrders)' column
    data['Year'] = data['order date (DateOrders)'].dt.year
    data['Month'] = data['order date (DateOrders)'].dt.month

    # Remove duplicate Order IDs
    unique_data = data.drop_duplicates(subset=['Order Id'])

    # Group data by year and month and calculate the number of orders and sales
    yearly_sales_data = data.groupby(['Year', 'Month']).agg({'Sales': 'sum'}).reset_index()
    yearly_orders_data = unique_data.groupby(['Year', 'Month']).agg({'Order Id': 'count'}).reset_index()

    # Create figure with subplots
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05,
                        subplot_titles=('Number of Orders', 'Sales'))

    # Add traces for each year
    for year in [2015, 2016, 2017]:
        yearly_sales_data_year = yearly_sales_data[yearly_sales_data['Year'] == year]
        yearly_orders_data_year = yearly_orders_data[yearly_orders_data['Year'] == year]

        fig.add_trace(go.Scatter(x=yearly_orders_data_year['Month'], y=yearly_orders_data_year['Order Id'],
                                 mode='lines+markers', name=f'Orders {year}', line=dict(color='blue')),
                      row=1, col=1)

        fig.add_trace(go.Scatter(x=yearly_sales_data_year['Month'], y=yearly_sales_data_year['Sales'],
                                 mode='lines+markers', name=f'Sales {year}', line=dict(color='green')),
                      row=2, col=1)

    # Update layout
    fig.update_xaxes(title_text='Month', row=2, col=1)
    fig.update_yaxes(title_text='Number of Orders', row=1, col=1)
    fig.update_yaxes(title_text='Sales', row=2, col=1)

    # Define steps for the slider
    steps = []
    for year in [2015, 2016, 2017]:
        step = dict(
            method="update",
            args=[{"visible": [year == y for y in [2015, 2016, 2017]]}],
            label=str(year)
        )
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Year: "},
        pad={"t": 50},
        steps=steps
    )]

    # Update layout with slider
    fig.update_layout(height=800, showlegend=True,
                      title_text="Summary of orders and sales in 2015, 2016, and 2017",
                      sliders=sliders)

    fig.show()

## 9 Assess the profitability of each order
def analyze_profitability():
    # Calculate the benefit per order
    data['Benefit per Order'] = data['Order Profit Per Order'] / data['Order Item Quantity']

    # Sort orders by benefit per order in descending order
    sorted_orders = data.sort_values(by='Benefit per Order', ascending=False)

    # Calculate total benefit and average benefit per order
    total_benefit = sorted_orders['Order Profit Per Order'].sum()
    avg_benefit_per_order = sorted_orders['Benefit per Order'].mean()

    # Display top 10 most profitable orders
    top_profitable_orders = sorted_orders.head(10)

    print("Total Benefit:", total_benefit)
    print("Average Benefit per Order:", avg_benefit_per_order)
    print("\nTop 10 Most Profitable Orders:")
    print(top_profitable_orders[['Order Id', 'Order Profit Per Order', 'Benefit per Order']])

## 10 Segment customers based on their sales volume
def segment_customers_by_sales():
    # Calculate sales per customer
    sales_per_customer = data.groupby('Customer Id')['Sales'].sum().reset_index()

    # Segment customers based on their sales volume
    quartiles = sales_per_customer['Sales'].quantile([0.25, 0.5, 0.75])
    sales_per_customer['Customer Segment'] = pd.cut(sales_per_customer['Sales'], bins=[0, quartiles[0.25], quartiles[0.5], quartiles[0.75], float('inf')],
                                                    labels=['Low-Value', 'Mid-Value', 'High-Value', 'Very High-Value'], include_lowest=True)

    # Display segmented customers
    print("Segmented Customers:")
    print(sales_per_customer.head(10))

## 11 Analyze product performance
def analyze_product_performance():
    # Calculate sales volume per product
    sales_volume_per_product = data.groupby('Product Name')['Order Item Quantity'].sum().reset_index()

    # Calculate profit margins per product
    profit_margins_per_product = data.groupby('Product Name')['Order Item Profit Ratio'].mean().reset_index()

    # Calculate popularity of each product (total sales)
    popularity_per_product = data.groupby('Product Name')['Sales'].sum().reset_index()

    # Merge the metrics into a single dataframe
    product_performance = pd.merge(sales_volume_per_product, profit_margins_per_product, on='Product Name')
    product_performance = pd.merge(product_performance, popularity_per_product, on='Product Name')

    # Rename columns for clarity
    product_performance.columns = ['Product Name', 'Sales Volume', 'Profit Margin', 'Total Sales']

    # Sort products by total sales in descending order
    product_performance = product_performance.sort_values(by='Total Sales', ascending=False)

    # Display product performance metrics
    print("Product Performance:")
    print(product_performance.head())

## 12 Analyze indicators over a period of time
def analyze_time_period(start_date=None, end_date=None):
    # Convert 'order date (DateOrders)' column to datetime format
    data['order date (DateOrders)'] = pd.to_datetime(data['order date (DateOrders)'])

    # Set default start date and end date if not provided
    if start_date is None:
        start_date = data['order date (DateOrders)'].min().strftime('%Y-%m-%d')
    if end_date is None:
        end_date = data['order date (DateOrders)'].max().strftime('%Y-%m-%d')

    # Filter data for the specified time period
    filtered_data = data[(data['order date (DateOrders)'] >= start_date) & (data['order date (DateOrders)'] <= end_date)]

    # Number of orders in the specified time period
    orders_count = filtered_data['Order Id'].nunique()

    # Total income in the specified time period
    total_income = filtered_data['Sales'].sum()

    # Number of products sold in the specified time period
    products_sold = filtered_data['Order Item Id'].nunique()

    # Customer with the highest total sales in the specified time period
    top_customer = filtered_data.groupby('Customer Id')['Sales'].sum().idxmax()

    # Best-selling product in the specified time period
    best_selling_product = filtered_data['Product Name'].value_counts().idxmax()

    # Print information
    print(f"Number of orders in the time period from {start_date} to {end_date}: {orders_count}")
    print(f"Total income in the time period from {start_date} to {end_date}: {total_income}")
    print(f"Number of products sold in the time period from {start_date} to {end_date}: {products_sold}")
    print(f"CustomerID with the highest total sales in the time period from {start_date} to {end_date}: {top_customer}")
    print(f"Best-selling product in the time period from {start_date} to {end_date}: {best_selling_product}")

