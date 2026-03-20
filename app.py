import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from data_loader import load_data
from kpis        import get_all_kpis
from charts      import (
    chart_monthly_trend,
    chart_revenue_by_category,
    chart_revenue_by_region,
    chart_yoy_comparison,
    chart_top_products,
    chart_discount_impact,
    chart_forecast,
    chart_heatmap,
)

# ── Bootstrap the app ────────────────────────────────────────
app = dash.Dash(__name__, title="E-Commerce Dashboard")
server = app.server

# ── Load base data ───────────────────────────────────────────
df_base = load_data()

# ── Dropdown Options ─────────────────────────────────────────
region_options = [{"label": "All Regions", "value": "ALL"}] + [
    {"label": r, "value": r} for r in sorted(df_base["region"].unique())
]
category_options = [{"label": "All Categories", "value": "ALL"}] + [
    {"label": c, "value": c} for c in sorted(df_base["category"].unique())
]
year_options = [{"label": "All Years", "value": "ALL"}] + [
    {"label": str(y), "value": y} for y in sorted(df_base["year"].unique())
]

# ─────────────────────────────────────────────────────────────
#  LAYOUT
# ─────────────────────────────────────────────────────────────
app.layout = html.Div([

    # ── Header ───────────────────────────────────────────────
    html.Div([
        html.H1("📊 E-Commerce Sales Dashboard"),
        html.P("Interactive data storytelling — Revenue, Trends & Insights"),
    ], className="header"),

    # ── Filter Bar ───────────────────────────────────────────
    html.Div([
        html.Div([
            html.Div("🌍 Region", className="filter-label"),
            dcc.Dropdown(
                id        = "filter-region",
                options   = region_options,
                value     = "ALL",
                clearable = False,
                style     = {"width": "180px", "color": "#0F172A"},
            ),
        ]),
        html.Div([
            html.Div("🏷️ Category", className="filter-label"),
            dcc.Dropdown(
                id        = "filter-category",
                options   = category_options,
                value     = "ALL",
                clearable = False,
                style     = {"width": "200px", "color": "#0F172A"},
            ),
        ]),
        html.Div([
            html.Div("📅 Year", className="filter-label"),
            dcc.Dropdown(
                id        = "filter-year",
                options   = year_options,
                value     = "ALL",
                clearable = False,
                style     = {"width": "150px", "color": "#0F172A"},
            ),
        ]),
    ], className="filter-bar"),

    # ── KPI Cards ────────────────────────────────────────────
    html.Div(id="kpi-cards", className="kpi-container"),

    # ── Charts ───────────────────────────────────────────────
    html.Div([

        # Row 1 — Full width trend
        html.Div(
            html.Div(
                dcc.Graph(id="chart-trend", config={"displayModeBar": False}),
                className="chart-card"
            ),
            className="chart-row-full"
        ),

        # Row 2 — Category + Region
        html.Div([
            html.Div(
                dcc.Graph(id="chart-category", config={"displayModeBar": False}),
                className="chart-card"
            ),
            html.Div(
                dcc.Graph(id="chart-region", config={"displayModeBar": False}),
                className="chart-card"
            ),
        ], className="chart-row-half"),

        # Row 3 — Full width YoY
        html.Div(
            html.Div(
                dcc.Graph(id="chart-yoy", config={"displayModeBar": False}),
                className="chart-card"
            ),
            className="chart-row-full"
        ),

        # Row 4 — Top Products + Discount
        html.Div([
            html.Div(
                dcc.Graph(id="chart-products", config={"displayModeBar": False}),
                className="chart-card"
            ),
            html.Div(
                dcc.Graph(id="chart-discount", config={"displayModeBar": False}),
                className="chart-card"
            ),
        ], className="chart-row-half"),

        # Row 5 — Forecast full width
        html.Div(
            html.Div(
                dcc.Graph(id="chart-forecast", config={"displayModeBar": False}),
                className="chart-card"
            ),
            className="chart-row-full"
        ),

        # Row 6 — Heatmap full width
        html.Div(
            html.Div(
                dcc.Graph(id="chart-heatmap", config={"displayModeBar": False}),
                className="chart-card"
            ),
            className="chart-row-full"
        ),

    ], className="charts-container"),

    # ── Narrative Section ────────────────────────────────────
    html.Div([
        html.H3("📖 Data Story & Insights"),
        html.Div(id="narrative-content"),
    ], className="narrative-section"),

])


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────
def _kpi_card(label, value, sub, value_class=""):
    return html.Div([
        html.Div(label, className="kpi-label"),
        html.Div(value, className=f"kpi-value {value_class}"),
        html.Div(sub,   className="kpi-sub"),
    ], className="kpi-card")


def _narrative_item(icon, text):
    return html.Div([
        html.Span(icon, style={"fontSize": "20px", "minWidth": "28px"}),
        html.Span(text, style={"lineHeight": "1.6", "color": "#CBD5E1"}),
    ], className="narrative-item")


# ─────────────────────────────────────────────────────────────
#  CALLBACK
# ─────────────────────────────────────────────────────────────
@callback(
    Output("kpi-cards",         "children"),
    Output("chart-trend",       "figure"),
    Output("chart-category",    "figure"),
    Output("chart-region",      "figure"),
    Output("chart-yoy",         "figure"),
    Output("chart-products",    "figure"),
    Output("chart-discount",    "figure"),
    Output("chart-forecast",    "figure"),
    Output("chart-heatmap",     "figure"),
    Output("narrative-content", "children"),
    Input("filter-region",      "value"),
    Input("filter-category",    "value"),
    Input("filter-year",        "value"),
)
def update_dashboard(region, category, year):

    # ── Apply Filters ─────────────────────────────────────────
    df = df_base.copy()
    if region   != "ALL": df = df[df["region"]   == region]
    if category != "ALL": df = df[df["category"] == category]
    if year     != "ALL": df = df[df["year"]      == year]

    # ── Compute KPIs ──────────────────────────────────────────
    kpis = get_all_kpis(df)
    yoy  = kpis["yoy_growth"]

    growth_color = "kpi-positive" if yoy["growth_pct"] >= 0 else "kpi-negative"
    growth_arrow = "▲" if yoy["growth_pct"] >= 0 else "▼"

    # ── KPI Cards ─────────────────────────────────────────────
    kpi_cards = [
        _kpi_card("💰 Total Revenue",
                  f"${kpis['total_revenue']:,.0f}",
                  "Gross revenue across all orders"),
        _kpi_card("📦 Total Orders",
                  f"{kpis['total_orders']:,}",
                  "Unique transactions"),
        _kpi_card("🛒 Avg Order Value",
                  f"${kpis['aov']:,.2f}",
                  "Revenue per order"),
        _kpi_card("📈 YoY Growth",
                  f"{growth_arrow} {abs(yoy['growth_pct'])}%",
                  f"Prev Year: ${yoy['revenue_2023']:,.0f}  →  Latest: ${yoy['revenue_2024']:,.0f}",
                  value_class=growth_color),
    ]

    # ── Narrative ─────────────────────────────────────────────
    top_cat    = kpis["top_category"]
    top_reg    = kpis["top_region"]
    trend      = kpis["monthly_trend"]
    peak_month = trend.loc[trend["total_revenue"].idxmax(), "year_month"]

    narrative = [
        _narrative_item("🏆", f"{top_cat['name']} is the top category with "
            f"{top_cat['revenue_share']} of total revenue. "
            f"Increase inventory and ad spend here."),
        _narrative_item("🌍", f"{top_reg['name']} leads all regions with "
            f"{top_reg['revenue_share']} of revenue. "
            f"Replicate this strategy in underperforming regions."),
        _narrative_item("📅", f"Revenue peaked in {peak_month}. "
            f"Plan promotions and stock replenishment before this period next year."),
        _narrative_item("📈",
            f"Year-over-Year growth is {yoy['growth_pct']}%. " +
            ("Business is expanding — maintain momentum." if yoy["growth_pct"] >= 0
             else "Revenue declined — investigate top drop-off categories immediately.")),
        _narrative_item("🛒", f"Average Order Value is ${kpis['aov']:,.2f}. "
            f"Introduce product bundles and free shipping thresholds to increase AOV."),
    ]

    return (
        kpi_cards,
        chart_monthly_trend(df),
        chart_revenue_by_category(df),
        chart_revenue_by_region(df),
        chart_yoy_comparison(df),
        chart_top_products(df),
        chart_discount_impact(df),
        chart_forecast(df),
        chart_heatmap(df),
        narrative,
    )


# ─────────────────────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Dashboard starting...")
    print("📊 Open your browser at: http://127.0.0.1:8050\n")
    app.run(debug=True)