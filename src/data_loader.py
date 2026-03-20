import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ecommerce_sales.csv")

def load_data() -> pd.DataFrame:
    """
    Loads the raw CSV, cleans it, and engineers new columns.
    Returns a fully analysis-ready DataFrame.
    """
    # ── 1. Load ───────────────────────────────────────────────
    df = pd.read_csv(DATA_PATH)

    # ── 2. Fix Data Types ─────────────────────────────────────
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["quantity"]   = df["quantity"].astype(int)

    # ── 3. Handle Missing Values ──────────────────────────────
    df["region"]   = df["region"].fillna("Unknown")
    df["discount"] = df["discount"].fillna(0.0)

    # Recalculate revenue where discount was missing
    df["revenue"]  = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)

    # ── 4. Feature Engineering ────────────────────────────────
    df["year"]          = df["order_date"].dt.year
    df["month"]         = df["order_date"].dt.month
    df["month_name"]    = df["order_date"].dt.strftime("%b")   # Jan, Feb ...
    df["quarter"]       = df["order_date"].dt.quarter
    df["week"]          = df["order_date"].dt.isocalendar().week.astype(int)
    df["year_month"]    = df["order_date"].dt.to_period("M").astype(str)  # 2023-01

    # ── 5. Derived Metrics ────────────────────────────────────
    df["profit_margin"] = (df["revenue"] * 0.35).round(2)   # Simulated 35% margin

    return df


def get_summary(df: pd.DataFrame) -> dict:
    """Returns a quick health-check summary of the dataset."""
    return {
        "total_rows"    : len(df),
        "date_range"    : f"{df['order_date'].min().date()} → {df['order_date'].max().date()}",
        "missing_values": df.isnull().sum().to_dict(),
        "categories"    : df["category"].unique().tolist(),
        "regions"       : df["region"].unique().tolist(),
        "total_revenue" : f"${df['revenue'].sum():,.2f}",
    }


if __name__ == "__main__":
    df = load_data()
    summary = get_summary(df)
    print("\n📊 Dataset Summary:")
    for key, value in summary.items():
        print(f"  {key:20} : {value}")
    print(f"\n✅ Cleaned DataFrame shape: {df.shape}")
    print(df.dtypes)