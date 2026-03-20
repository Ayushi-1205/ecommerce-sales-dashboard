import pandas as pd

# Try different encodings as Superstore CSV often has encoding issues
for enc in ['utf-8', 'latin-1', 'cp1252']:
    try:
        df = pd.read_csv('data/superstore.csv', encoding=enc)
        print(f"Successfully read with encoding: {enc}")
        print(f"Shape: {df.shape}")
        print(f"\nColumns: {df.columns.tolist()}")
        print(f"\nFirst row:\n{df.head(1).to_string()}")
        break
    except Exception as e:
        print(f"Failed with {enc}: {e}")