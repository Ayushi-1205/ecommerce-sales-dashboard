with open('src/charts.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'colorbar=dict(title="Revenue", titlefont=dict(color=COLORS["muted"]), tickfont=dict(color=COLORS["muted"]), tickprefix="$"),'
new = 'colorbar=dict(title=dict(text="Revenue", font=dict(color=COLORS["muted"])), tickfont=dict(color=COLORS["muted"]), tickprefix="$"),'

fixed = content.replace(old, new)

with open('src/charts.py', 'w', encoding='utf-8') as f:
    f.write(fixed)

print("Done! Check if replaced:", old not in fixed)