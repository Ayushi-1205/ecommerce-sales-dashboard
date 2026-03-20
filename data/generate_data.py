import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ── Reproducibility ──────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ── Lookup Tables ────────────────────────────────────────────
REGIONS     = ["North", "South", "East", "West"]
CATEGORIES  = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books"]
PRODUCTS    = {
    "Electronics"   : ["Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch"],
    "Clothing"      : ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers"],
    "Home & Kitchen": ["Blender", "Coffee Maker", "Air Fryer", "Vacuum", "Toaster"],
    "Sports"        : ["Yoga Mat", "Dumbbells", "Cycling Helmet", "Tennis Racket", "Running Shoes"],
    "Books"         : ["Fiction Novel", "Self-Help", "Science", "History", "Cookbook"],
}
PRICE_RANGE = {
    "Electronics"   : (200, 1500),
    "Clothing"      : (20,  200),
    "Home & Kitchen": (30,  300),
    "Sports"        : (15,  250),
    "Books"         : (5,   50),
}

# ── Date Range: Jan 2023 → Dec 2024 ──────────────────────────
START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2024, 12, 31)
DATE_RANGE = (END_DATE - START_DATE).days

# ── Generate 1500 Rows ────────────────────────────────────────
rows = []
for order_id in range(1001, 2501):          # 1500 orders
    category    = random.choice(CATEGORIES)
    product     = random.choice(PRODUCTS[category])
    region      = random.choice(REGIONS)
    order_date  = START_DATE + timedelta(days=random.randint(0, DATE_RANGE))
    quantity    = random.randint(1, 5)
    unit_price  = round(random.uniform(*PRICE_RANGE[category]), 2)
    discount    = random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20])  # 0 weighted heavily
    revenue     = round(quantity * unit_price * (1 - discount), 2)

    # Inject ~3% missing values for realism
    if random.random() < 0.03:
        region = np.nan
    if random.random() < 0.03:
        discount = np.nan

    rows.append({
        "order_id"   : f"ORD-{order_id}",
        "order_date" : order_date.strftime("%Y-%m-%d"),
        "region"     : region,
        "category"   : category,
        "product"    : product,
        "quantity"   : quantity,
        "unit_price" : unit_price,
        "discount"   : discount,
        "revenue"    : revenue,
    })

df = pd.DataFrame(rows)
df.to_csv("data/ecommerce_sales.csv", index=False)
print(f"✅ Dataset created: {len(df)} rows × {len(df.columns)} columns")
print(df.head())