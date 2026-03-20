import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# ── Shared Color Theme ────────────────────────────────────────
COLORS = {
    "primary"    : "#4F46E5",   # Indigo
    "secondary"  : "#7C3AED",   # Purple
    "success"    : "#10B981",   # Green
    "warning"    : "#F59E0B",   # Amber
    "danger"     : "#EF4444",   # Red
    "background" : "#0F172A",   # Dark navy
    "card"       : "#1E293B",   # Card background
    "text"       : "#F1F5F9",   # Light text
    "muted"      : "#94A3B8",   # Muted text
}

CATEGORY_COLORS = {
    "Electronics"    : "#4F46E5",
    "Clothing"       : "#7C3AED",
    "Home & Kitchen" : "#10B981",
    "Sports"         : "#F59E0B",
    "Books"          : "#EF4444",
}

REGION_COLORS = {
    "North"   : "#4F46E5",
    "South"   : "#10B981",
    "East"    : "#F59E0B",
    "West"    : "#EF4444",
    "Unknown" : "#94A3B8",
}

LAYOUT_BASE = dict(
    paper_bgcolor = COLORS["background"],
    plot_bgcolor  = COLORS["background"],
    font          = dict(color=COLORS["text"], family="Inter, sans-serif"),
    margin        = dict(l=40, r=40, t=60, b=40),
    legend        = dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
)


# ─────────────────────────────────────────────────────────────
# CHART 1 — Monthly Revenue Trend (Line Chart)
# ─────────────────────────────────────────────────────────────
def chart_monthly_trend(df: pd.DataFrame) -> go.Figure:
    """
    Line chart showing revenue month-by-month.
    Story: Reveals seasonality peaks and dips.
    """
    trend = (
        df.groupby("year_month")["revenue"]
        .sum()
        .reset_index()
        .sort_values("year_month")
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x          = trend["year_month"],
        y          = trend["revenue"],
        mode       = "lines+markers",
        name       = "Monthly Revenue",
        line       = dict(color=COLORS["primary"], width=3),
        marker     = dict(size=6, color=COLORS["primary"]),
        fill       = "tozeroy",
        fillcolor  = "rgba(79, 70, 229, 0.15)",
        hovertemplate = "<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>",
    ))

    fig.update_layout(
        **LAYOUT_BASE,
        title = dict(text="📈 Monthly Revenue Trend", font=dict(size=18)),
        xaxis = dict(title="Month", showgrid=False, color=COLORS["muted"]),
        yaxis = dict(title="Revenue ($)", showgrid=True,
                     gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# CHART 2 — Revenue by Category (Bar Chart)
# ─────────────────────────────────────────────────────────────
def chart_revenue_by_category(df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart — category vs revenue.
    Story: Which category should get more marketing budget?
    """
    cat = (
        df.groupby("category")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=True)
    )

    fig = go.Figure(go.Bar(
        x             = cat["revenue"],
        y             = cat["category"],
        orientation   = "h",
        marker_color  = [CATEGORY_COLORS.get(c, COLORS["primary"]) for c in cat["category"]],
        hovertemplate = "<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>",
    ))

    fig.update_layout(
        **LAYOUT_BASE,
        title = dict(text="🏆 Revenue by Category", font=dict(size=18)),
        xaxis = dict(title="Revenue ($)", showgrid=True,
                     gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
        yaxis = dict(title="", color=COLORS["muted"]),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# CHART 3 — Revenue by Region (Donut Chart)
# ─────────────────────────────────────────────────────────────
def chart_revenue_by_region(df: pd.DataFrame) -> go.Figure:
    """
    Donut chart — regional revenue share.
    Story: Which region is dominating? Which needs attention?
    """
    reg = (
        df.groupby("region")["revenue"]
        .sum()
        .reset_index()
    )

    fig = go.Figure(go.Pie(
        labels    = reg["region"],
        values    = reg["revenue"],
        hole      = 0.55,
        marker    = dict(colors=[REGION_COLORS.get(r, COLORS["primary"]) for r in reg["region"]]),
        hovertemplate = "<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>",
    ))

    fig.update_layout(
        **LAYOUT_BASE,
        title = dict(text="🌍 Revenue by Region", font=dict(size=18)),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# CHART 4 — YoY Revenue Comparison (Grouped Bar)
# ─────────────────────────────────────────────────────────────
def chart_yoy_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Side-by-side bars comparing 2023 vs 2024 by month.
    Story: Are we growing month-by-month vs last year?
    """
    monthly = (
        df.groupby(["year", "month_name", "month"])["revenue"]
        .sum()
        .reset_index()
        .sort_values("month")
    )

    fig = go.Figure()

    for year, color in [(2023, COLORS["primary"]), (2024, COLORS["success"])]:
        data = monthly[monthly["year"] == year]
        fig.add_trace(go.Bar(
            x             = data["month_name"],
            y             = data["revenue"],
            name          = str(year),
            marker_color  = color,
            hovertemplate = f"<b>%{{x}} {year}</b><br>Revenue: $%{{y:,.2f}}<extra></extra>",
        ))

    fig.update_layout(
        **LAYOUT_BASE,
        title    = dict(text="📊 2023 vs 2024 Monthly Revenue", font=dict(size=18)),
        barmode  = "group",
        xaxis    = dict(title="Month", color=COLORS["muted"]),
        yaxis    = dict(title="Revenue ($)", showgrid=True,
                        gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# CHART 5 — Top 10 Products (Bar Chart)
# ─────────────────────────────────────────────────────────────
def chart_top_products(df: pd.DataFrame) -> go.Figure:
    """
    Top 10 products by revenue.
    Story: What are customers actually buying the most?
    """
    prod = (
        df.groupby("product")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(10)
        .sort_values("revenue", ascending=True)
    )

    fig = go.Figure(go.Bar(
        x             = prod["revenue"],
        y             = prod["product"],
        orientation   = "h",
        marker_color  = COLORS["secondary"],
        hovertemplate = "<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>",
    ))

    fig.update_layout(
        **LAYOUT_BASE,
        title = dict(text="🥇 Top 10 Products by Revenue", font=dict(size=18)),
        xaxis = dict(title="Revenue ($)", showgrid=True,
                     gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
        yaxis = dict(color=COLORS["muted"]),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# CHART 6 — Discount vs Revenue Scatter
# ─────────────────────────────────────────────────────────────
def chart_discount_impact(df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot — does giving discounts actually increase revenue?
    Story: High discount + low revenue = discounts are hurting us.
    """
    fig = px.scatter(
        df,
        x         = "discount",
        y         = "revenue",
        color     = "category",
        size      = "quantity",
        hover_data= ["product", "region"],
        color_discrete_map = CATEGORY_COLORS,
        labels    = {"discount": "Discount Rate", "revenue": "Revenue ($)"},
    )

    fig.update_layout(
        **LAYOUT_BASE,
        title = dict(text="🔍 Discount Impact on Revenue", font=dict(size=18)),
        xaxis = dict(tickformat=".0%", color=COLORS["muted"]),
        yaxis = dict(showgrid=True, gridcolor="rgba(148,163,184,0.1)",
                     color=COLORS["muted"]),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# TEST — preview all charts
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from data_loader import load_data

    df = load_data()
    print("🎨 Rendering all charts in browser...")

    chart_monthly_trend(df).show()
    chart_revenue_by_category(df).show()
    chart_revenue_by_region(df).show()
    chart_yoy_comparison(df).show()
    chart_top_products(df).show()
    chart_discount_impact(df).show()

    print("✅ All 6 charts rendered successfully!")