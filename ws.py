import pandas as pd

df = pd.read_csv("cleaned_DataCoSupplyChainDataset.csv", encoding='ISO-8859-1')

def count_unValues(df, String):
    ## Count unique values in a column
    unique_values = df[String].unique()
    value_counts = df[String].value_counts()

    print("Number of Unique", String + ":", len(unique_values))
    print("\nValue Counts for each", String + ":")
    print(value_counts)

def find_order_by_orderId(df, order_id):
    # Filter the dataset based on the Order ID
    order = df[df['Order Id'] == order_id]
    
    # If the order is found, return the order details, otherwise return None
    if not order.empty:
        print("Order Information:")
        print(order)
        return order
    else:
        print("Order not found.")
        return None

def find_smallest_and_newest_order_date(df):
    df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
    
    # Find the earliest order date
    smallest_order_date = df['order date (DateOrders)'].min()
    
    # Find the latest order date
    newest_order_date = df['order date (DateOrders)'].max()
    
    print("Smallest (Earliest) Order Date:", smallest_order_date)
    print("Newest (Latest) Order Date:", newest_order_date)

