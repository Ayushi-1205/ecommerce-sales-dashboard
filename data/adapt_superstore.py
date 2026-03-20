import pandas as pd
import os

def adapt_superstore():
    print("Loading Superstore dataset...")
    df = pd.read_csv('data/superstore.csv', encoding='latin-1')

    print(f"Raw shape: {df.shape}")

    # ── Rename columns to match our dashboard schema ──────────
    df = df.rename(columns={
        'Order ID'    : 'order_id',
        'Order Date'  : 'order_date',
        'Region'      : 'region',
        'Category'    : 'category',
        'Sub-Category': 'product',
        'Product Name': 'product_name',
        'Sales'       : 'revenue',
        'Quantity'    : 'quantity',
        'Discount'    : 'discount',
        'Profit'      : 'profit',
    })

    # ── Keep only columns our dashboard needs ─────────────────
    df = df[[
        'order_id', 'order_date', 'region',
        'category', 'product', 'quantity',
        'discount', 'revenue', 'profit'
    ]]

    # ── Fix data types ────────────────────────────────────────
    df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y')
    df['quantity']   = df['quantity'].astype(int)
    df['discount']   = df['discount'].astype(float)
    df['revenue']    = df['revenue'].astype(float).round(2)

    # ── Handle missing values ─────────────────────────────────
    df['region']   = df['region'].fillna('Unknown')
    df['discount'] = df['discount'].fillna(0.0)

    # ── Feature Engineering ───────────────────────────────────
    df['year']       = df['order_date'].dt.year
    df['month']      = df['order_date'].dt.month
    df['month_name'] = df['order_date'].dt.strftime('%b')
    df['quarter']    = df['order_date'].dt.quarter
    df['week']       = df['order_date'].dt.isocalendar().week.astype(int)
    df['year_month'] = df['order_date'].dt.to_period('M').astype(str)

    # ── Derived metrics ───────────────────────────────────────
    df['unit_price']    = (df['revenue'] / df['quantity']).round(2)
    df['profit_margin'] = df['profit'].round(2)

    # ── Save as new CSV ───────────────────────────────────────
    output_path = 'data/superstore_clean.csv'
    df.to_csv(output_path, index=False)

    print(f"\n✅ Clean dataset saved: {output_path}")
    print(f"   Shape : {df.shape}")
    print(f"   Years : {sorted(df['year'].unique().tolist())}")
    print(f"   Regions   : {df['region'].unique().tolist()}")
    print(f"   Categories: {df['category'].unique().tolist()}")
    print(f"   Revenue   : ${df['revenue'].sum():,.2f}")
    print(f"\nSample:\n{df.head(3).to_string()}")

if __name__ == "__main__":
    adapt_superstore()