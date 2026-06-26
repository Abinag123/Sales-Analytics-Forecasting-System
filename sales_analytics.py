import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_data(num_rows=1000):
    """Generates a realistic synthetic sales transactional dataset."""
    np.random.seed(42)
    categories = ['Electronics', 'Clothing', 'Home Appliances', 'Books', 'Office Supplies']
    products = {
        'Electronics': ['Laptop', 'Smartphone', 'Headphones', 'Smartwatch', 'Tablet'],
        'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Socks'],
        'Home Appliances': ['Microwave', 'Blender', 'Coffee Maker', 'Toaster', 'Air Fryer'],
        'Books': ['Fiction Novel', 'Science Textbook', 'Biography', 'Self-Help Book', 'Comic'],
        'Office Supplies': ['Notebook', 'Desk Organizer', 'Gel Pen Set', 'Whiteboard', 'Stapler']
    }
    prices = {
        'Laptop': 999.99, 'Smartphone': 699.99, 'Headphones': 99.99, 'Smartwatch': 199.99, 'Tablet': 299.99,
        'T-Shirt': 19.99, 'Jeans': 49.99, 'Jacket': 89.99, 'Sneakers': 79.99, 'Socks': 9.99,
        'Microwave': 129.99, 'Blender': 39.99, 'Coffee Maker': 59.99, 'Toaster': 24.99, 'Air Fryer': 89.99,
        'Fiction Novel': 14.99, 'Science Textbook': 79.99, 'Biography': 24.99, 'Self-Help Book': 19.99, 'Comic': 9.99,
        'Notebook': 4.99, 'Desk Organizer': 19.99, 'Gel Pen Set': 12.99, 'Whiteboard': 29.99, 'Stapler': 8.99
    }
    
    start_date = datetime(2025, 1, 1)
    
    data = []
    for i in range(num_rows):
        tx_id = f"TX{10000 + i}"
        cust_id = f"CUST{np.random.randint(100, 500)}"
        cat = np.random.choice(categories)
        prod = np.random.choice(products[cat])
        price = prices[prod]
        qty = np.random.randint(1, 6)
        
        # Random date within 18 months
        days_offset = np.random.randint(0, 500)
        date = start_date + timedelta(days=days_offset)
        
        data.append([tx_id, cust_id, date, cat, prod, price, qty])
        
    df = pd.DataFrame(data, columns=['TransactionID', 'CustomerID', 'Date', 'Category', 'Product', 'UnitPrice', 'Quantity'])
    return df

def run_etl_pipeline(df):
    """Executes ETL: Data Cleaning, Transform (Total Revenue), and Type Parsing."""
    # Cleaning check: Drop duplicates or nulls if present
    df = df.drop_duplicates()
    
    # Transformation: Calculate TotalRevenue
    df['TotalRevenue'] = df['UnitPrice'] * df['Quantity']
    
    # Parse date column
    df['Date'] = pd.to_datetime(df['Date'])
    df['YearMonth'] = df['Date'].dt.to_period('M')
    return df

def analyze_sales(df):
    """Generates summary statistics and trend metrics from data."""
    print("========================================")
    # 1. High-Level Metrics
    total_sales = df['TotalRevenue'].sum()
    total_tx = df['TransactionID'].nunique()
    avg_order_value = total_sales / total_tx
    
    print("      SALES EXECUTIVE SUMMARY REPORT    ")
    print("========================================")
    print(f"Total Combined Revenue : ${total_sales:,.2f}")
    print(f"Total Transactions     : {total_tx}")
    print(f"Average Order Value    : ${avg_order_value:.2f}\n")
    
    # 2. Performance by Product Category
    print("--- REVENUE BY CATEGORY ---")
    cat_summary = df.groupby('Category')['TotalRevenue'].sum().sort_values(ascending=False)
    for cat, rev in cat_summary.items():
        print(f"{cat:<20}: ${rev:,.2f}")
    print()
    
    # 3. Monthly Sales and 3-Month Moving Average Forecasting
    print("--- MONTHLY SALES TRENDS & FORECASTING ---")
    monthly_sales = df.groupby('YearMonth')['TotalRevenue'].sum().reset_index()
    monthly_sales['Date_Parsed'] = monthly_sales['YearMonth'].dt.to_timestamp()
    monthly_sales = monthly_sales.sort_values('Date_Parsed')
    
    # Compute 3-Month Moving Average
    monthly_sales['3MA_Forecast'] = monthly_sales['TotalRevenue'].rolling(window=3).mean()
    
    for _, row in monthly_sales.tail(6).iterrows():
        ym = str(row['YearMonth'])
        rev = row['TotalRevenue']
        fc = row['3MA_Forecast']
        fc_str = f"${fc:,.2f}" if not pd.isna(fc) else "N/A"
        print(f"Month: {ym} | Revenue: ${rev:,.2f} | 3-Month MA Forecast: {fc_str}")

def main():
    # 1. Extract
    raw_data = generate_synthetic_data(1200)
    
    # 2. Transform
    clean_data = run_etl_pipeline(raw_data)
    
    # 3. Load & Analyze
    analyze_sales(clean_data)
    
    # Save output to Excel
    output_filename = "Sales_Analytics_Output.xlsx"
    clean_data.to_excel(output_filename, index=False)
    print(f"\n[SUCCESS] Cleaned and compiled sales database saved to: {output_filename}")

if __name__ == "__main__":
    main()
