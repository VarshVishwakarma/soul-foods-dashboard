import pandas as pd
import numpy as np

# Create sample data
dates = pd.date_range(start="2024-01-01", periods=100, freq='D')
regions = ['north', 'east', 'south', 'west']
data = []

for date in dates:
    for region in regions:
        data.append({
            "sales": round(np.random.uniform(100, 1000), 2),
            "date": date.strftime("%Y-%m-%d"),
            "region": region,
            "product": "pink morsel"
        })

# Write to CSV
df = pd.DataFrame(data)
df.to_csv("pink_morsels_sales.csv", index=False)

print("---")
print("✅ SUCCESS: Data has been written to pink_morsels_sales.csv")
print(f"Total rows created: {len(df)}")
print("---")