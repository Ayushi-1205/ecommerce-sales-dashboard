import pandas as pd


# ─────────────────────────────────────────────
# 1. TOTAL REVENUE
# ─────────────────────────────────────────────
def get_total_revenue(df: pd.DataFrame) -> float:
    """
    Sum of all revenue across the entire dataset.
    Story: Tells us the overall business size.
    """
    return round(df["revenue"].sum(), 2)


# ─────────────────────────────────────────────
# 2. TOTAL ORDERS
# ─────────────────────────────────────────────
def get_total_orders(df: pd.DataFrame) -> int:
    """
    Count of unique orders.
    Story: Tells us transaction volume — are we busy?
    """
    return df["order_id"].nunique()


# ─────────────────────────────────────────────
# 3. AVERAGE ORDER VALUE (AOV)
# ─────────────────────────────────────────────
def get_aov(df: pd.DataFrame) -> float:
    """
    Average Revenue per Order.
    Formula: Total Revenue / Total Orders
    Story: Higher AOV = customers buying more per visit.
    """
    total_orders = get_total_orders(df)
    if total_orders == 0:
        return 0.0
    return round(get_total_revenue(df) / total_orders, 2)


# ─────────────────────────────────────────────
# 4. YEAR-OVER-YEAR (YoY) REVENUE GROWTH
# ─────────────────────────────────────────────
def get_yoy_growth(df: pd.DataFrame) -> dict:
    """
    Compares 2024 revenue vs 2023 revenue.
    Formula: ((2024 - 2023) / 2023) * 100
    Story: The single most important business health metric.
            Positive = growing. Negative = shrinking.
    """
    yearly = df.groupby("year")["revenue"].sum()

    rev_2023 = yearly.get(2023, 0)
    rev_2024 = yearly.get(2024, 0)

    if rev_2023 == 0:
        growth_pct = 0.0
    else:
        growth_pct = round(((rev_2024 - rev_2023) / rev_2023) * 100, 2)

    return {
        "revenue_2023" : round(rev_2023, 2),
        "revenue_2024" : round(rev_2024, 2),
        "growth_pct"   : growth_pct,
        "direction"    : "📈 Growth" if growth_pct >= 0 else "📉 Decline",
    }


# ─────────────────────────────────────────────
# 5. TOP PERFORMING CATEGORY
# ─────────────────────────────────────────────
def get_top_category(df: pd.DataFrame) -> dict:
    """
    Category with the highest total revenue.
    Story: Where should we invest more marketing budget?
    """
    cat_revenue = (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )
    top_name    = cat_revenue.index[0]
    top_revenue = cat_revenue.iloc[0]
    top_share   = round((top_revenue / get_total_revenue(df)) * 100, 2)

    return {
        "name"           : top_name,
        "revenue"        : top_revenue,
        "revenue_share"  : f"{top_share}%",
        "all_categories" : cat_revenue.to_dict(),
    }


# ─────────────────────────────────────────────
# 6. TOP PERFORMING REGION
# ─────────────────────────────────────────────
def get_top_region(df: pd.DataFrame) -> dict:
    """
    Region with the highest total revenue.
    Story: Which geography drives our business?
    """
    reg_revenue = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )
    top_name    = reg_revenue.index[0]
    top_revenue = reg_revenue.iloc[0]
    top_share   = round((top_revenue / get_total_revenue(df)) * 100, 2)

    return {
        "name"        : top_name,
        "revenue"     : top_revenue,
        "revenue_share": f"{top_share}%",
        "all_regions" : reg_revenue.to_dict(),
    }


# ─────────────────────────────────────────────
# 7. MONTHLY REVENUE TREND
# ─────────────────────────────────────────────
def get_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Revenue grouped by year_month.
    Story: Reveals seasonality — which months peak?
            Use this to plan promotions and inventory.
    """
    trend = (
        df.groupby("year_month")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
        .sort_values("year_month")
    )
    trend["total_revenue"] = trend["total_revenue"].round(2)
    return trend


# ─────────────────────────────────────────────
# 8. MASTER KPI SUMMARY (used by dashboard)
# ─────────────────────────────────────────────
def get_all_kpis(df: pd.DataFrame) -> dict:
    """
    Single function that returns ALL KPIs at once.
    The dashboard calls only this one function.
    """
    return {
        "total_revenue" : get_total_revenue(df),
        "total_orders"  : get_total_orders(df),
        "aov"           : get_aov(df),
        "yoy_growth"    : get_yoy_growth(df),
        "top_category"  : get_top_category(df),
        "top_region"    : get_top_region(df),
        "monthly_trend" : get_monthly_trend(df),
    }


# ─────────────────────────────────────────────
# TEST — run directly to verify
# ─────────────────────────────────────────────
if __name__ == "__main__":
    from data_loader import load_data

    df   = load_data()
    kpis = get_all_kpis(df)

    print("\n" + "="*50)
    print("       📊 E-COMMERCE KPI REPORT")
    print("="*50)
    print(f"  💰 Total Revenue     : ${kpis['total_revenue']:>12,.2f}")
    print(f"  📦 Total Orders      : {kpis['total_orders']:>12,}")
    print(f"  🛒 Avg Order Value   : ${kpis['aov']:>12,.2f}")
    print(f"  📈 YoY Growth        : {kpis['yoy_growth']['growth_pct']:>11}%  {kpis['yoy_growth']['direction']}")
    print(f"  🏆 Top Category      : {kpis['top_category']['name']} ({kpis['top_category']['revenue_share']})")
    print(f"  🌍 Top Region        : {kpis['top_region']['name']} ({kpis['top_region']['revenue_share']})")
    print("="*50)

    print("\n📅 Monthly Revenue Trend (first 6 months):")
    print(kpis["monthly_trend"].head(6).to_string(index=False))