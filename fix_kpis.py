with open('src/kpis.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    rev_2023 = yearly.get(2023, 0)
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
    }'''

new = '''    years = sorted(yearly.index.tolist())
    if len(years) >= 2:
        prev_year = years[-2]
        curr_year = years[-1]
    elif len(years) == 1:
        prev_year = years[0]
        curr_year = years[0]
    else:
        prev_year = curr_year = 0

    rev_prev = yearly.get(prev_year, 0)
    rev_curr = yearly.get(curr_year, 0)

    if rev_prev == 0:
        growth_pct = 0.0
    else:
        growth_pct = round(((rev_curr - rev_prev) / rev_prev) * 100, 2)

    return {
        "revenue_2023" : round(rev_prev, 2),
        "revenue_2024" : round(rev_curr, 2),
        "growth_pct"   : growth_pct,
        "direction"    : "Growth" if growth_pct >= 0 else "Decline",
    }'''

with open('src/kpis.py', 'w', encoding='utf-8') as f:
    f.write(content.replace(old, new))
print("kpis.py updated!")