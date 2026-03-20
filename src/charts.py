import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = {
    "primary"    : "#4F46E5",
    "secondary"  : "#7C3AED",
    "success"    : "#10B981",
    "warning"    : "#F59E0B",
    "danger"     : "#EF4444",
    "background" : "#0F172A",
    "card"       : "#1E293B",
    "text"       : "#F1F5F9",
    "muted"      : "#94A3B8",
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


def chart_monthly_trend(df):
    trend = df.groupby("year_month")["revenue"].sum().reset_index().sort_values("year_month")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend["year_month"], y=trend["revenue"],
        mode="lines+markers", name="Monthly Revenue",
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=6, color=COLORS["primary"]),
        fill="tozeroy", fillcolor="rgba(79, 70, 229, 0.15)",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="📈 Monthly Revenue Trend", font=dict(size=18)),
        xaxis=dict(title="Month", showgrid=False, color=COLORS["muted"]),
        yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
    )
    return fig


def chart_revenue_by_category(df):
    cat = df.groupby("category")["revenue"].sum().reset_index().sort_values("revenue", ascending=True)
    fig = go.Figure(go.Bar(
        x=cat["revenue"], y=cat["category"], orientation="h",
        marker_color=[CATEGORY_COLORS.get(c, COLORS["primary"]) for c in cat["category"]],
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="🏆 Revenue by Category", font=dict(size=18)),
        xaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
        yaxis=dict(title="", color=COLORS["muted"]),
    )
    return fig


def chart_revenue_by_region(df):
    reg = df.groupby("region")["revenue"].sum().reset_index()
    fig = go.Figure(go.Pie(
        labels=reg["region"], values=reg["revenue"], hole=0.55,
        marker=dict(colors=[REGION_COLORS.get(r, COLORS["primary"]) for r in reg["region"]]),
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="🌍 Revenue by Region", font=dict(size=18)),
    )
    return fig


def chart_yoy_comparison(df):
    monthly = df.groupby(["year", "month_name", "month"])["revenue"].sum().reset_index().sort_values("month")
    fig = go.Figure()
    for year, color in [(2023, COLORS["primary"]), (2024, COLORS["success"])]:
        data = monthly[monthly["year"] == year]
        fig.add_trace(go.Bar(
            x=data["month_name"], y=data["revenue"],
            name=str(year), marker_color=color,
            hovertemplate=f"<b>%{{x}} {year}</b><br>Revenue: $%{{y:,.2f}}<extra></extra>",
        ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="📊 2023 vs 2024 Monthly Revenue", font=dict(size=18)),
        barmode="group",
        xaxis=dict(title="Month", color=COLORS["muted"]),
        yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
    )
    return fig


def chart_top_products(df):
    prod = df.groupby("product")["revenue"].sum().reset_index().sort_values("revenue", ascending=False).head(10).sort_values("revenue", ascending=True)
    fig = go.Figure(go.Bar(
        x=prod["revenue"], y=prod["product"], orientation="h",
        marker_color=COLORS["secondary"],
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="🥇 Top 10 Products by Revenue", font=dict(size=18)),
        xaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
        yaxis=dict(color=COLORS["muted"]),
    )
    return fig


def chart_discount_impact(df):
    fig = px.scatter(
        df, x="discount", y="revenue", color="category",
        size="quantity", hover_data=["product", "region"],
        color_discrete_map=CATEGORY_COLORS,
        labels={"discount": "Discount Rate", "revenue": "Revenue ($)"},
    )
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="🔍 Discount Impact on Revenue", font=dict(size=18)),
        xaxis=dict(tickformat=".0%", color=COLORS["muted"]),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
    )
    return fig


def chart_forecast(df):
    daily = df.groupby("order_date")["revenue"].sum().reset_index().sort_values("order_date")
    daily["moving_avg"] = daily["revenue"].rolling(window=30, min_periods=1).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["order_date"], y=daily["revenue"],
        mode="lines", name="Daily Revenue",
        line=dict(color="rgba(79,70,229,0.25)", width=1),
        hovertemplate="<b>%{x}</b><br>Daily: $%{y:,.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=daily["order_date"], y=daily["moving_avg"],
        mode="lines", name="30-Day Moving Avg",
        line=dict(color=COLORS["success"], width=3),
        hovertemplate="<b>%{x}</b><br>30D Avg: $%{y:,.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=daily["order_date"], y=daily["moving_avg"],
        fill="tozeroy", fillcolor="rgba(16,185,129,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        showlegend=False, hoverinfo='skip',
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="📉 Revenue Trend & 30-Day Moving Average", font=dict(size=18)),
        xaxis=dict(title="Date", showgrid=False, color=COLORS["muted"]),
        yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="rgba(148,163,184,0.1)", color=COLORS["muted"]),
    )
    return fig


def chart_heatmap(df):
    df = df.copy()
    df["day_of_week"] = df["order_date"].dt.day_name()
    df["month_name"]  = df["order_date"].dt.strftime("%b")
    df["month_num"]   = df["order_date"].dt.month
    pivot = df.groupby(["day_of_week", "month_name", "month_num"])["revenue"].sum().reset_index()
    day_order   = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    pivot  = pivot[pivot["day_of_week"].isin(day_order)]
    matrix = pivot.pivot_table(
        index="day_of_week", columns="month_name", values="revenue", aggfunc="sum",
    ).reindex(index=day_order, columns=month_order).fillna(0)
    fig = go.Figure(go.Heatmap(
        z=matrix.values,
        x=matrix.columns.tolist(),
        y=matrix.index.tolist(),
        colorscale=[
            [0.0,  "#0F172A"],
            [0.25, "#1E3A5F"],
            [0.5,  "#1D4ED8"],
            [0.75, "#4F46E5"],
            [1.0,  "#A78BFA"],
        ],
        hovertemplate="<b>%{y} — %{x}</b><br>Revenue: $%{z:,.0f}<extra></extra>",
        showscale=True,
        colorbar=dict(title=dict(text="Revenue", font=dict(color=COLORS["muted"])), tickfont=dict(color=COLORS["muted"]), tickprefix="$"),
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="🗓️ Revenue Heatmap — Day of Week vs Month", font=dict(size=18)),
        xaxis=dict(title="Month", color=COLORS["muted"], side="bottom"),
        yaxis=dict(title="Day of Week", color=COLORS["muted"]),
    )
    return fig
