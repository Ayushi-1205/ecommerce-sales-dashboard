with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'f"2023: ${yoy[\'revenue_2023\']:,.0f}  →  2024: ${yoy[\'revenue_2024\']:,.0f}"'
new = 'f"Prev Year: ${yoy[\'revenue_2023\']:,.0f}  →  Latest: ${yoy[\'revenue_2024\']:,.0f}"'

result = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(result)
print("app.py updated!")