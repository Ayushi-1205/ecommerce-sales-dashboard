new_code = '''import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "superstore_clean.csv")

def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["quantity"]   = df["quantity"].astype(int)
    df["discount"]   = df["discount"].fillna(0.0)
    df["region"]     = df["region"].fillna("Unknown")
    df["year"]       = df["order_date"].dt.year
    df["month"]      = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.strftime("%b")
    df["quarter"]    = df["order_date"].dt.quarter
    df["week"]       = df["order_date"].dt.isocalendar().week.astype(int)
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df

def get_summary(df):
    return {
        "total_rows"  : len(df),
        "date_range"  : f"{df[\'order_date\'].min().date()} to {df[\'order_date\'].max().date()}",
        "categories"  : df["category"].unique().tolist(),
        "regions"     : df["region"].unique().tolist(),
        "total_revenue": f"${df[\'revenue\'].sum():,.2f}",
    }

if __name__ == "__main__":
    df = load_data()
    print("Shape:", df.shape)
    print("Years:", sorted(df["year"].unique().tolist()))
    print("Revenue: $", df["revenue"].sum().round(2))
'''

with open('src/data_loader.py', 'w', encoding='utf-8') as f:
    f.write(new_code)
print("data_loader.py updated!")