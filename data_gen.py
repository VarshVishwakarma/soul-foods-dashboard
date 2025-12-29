import pandas as pd
import numpy as np

# Create a range of dates for the last year
dates = pd.date_range(start="2024-01-01", end="2024-12-31")
regions = ['north', 'east', 'south', 'west']

data = []

# Generate random sales data for each region and date
for date in dates:
    for region in regions:
        # Base sales + some random noise + a slight upward trend
        sales = 100 + np.random.randint(0, 50) + (date.dayofyear * 0.2)
        data.append({
            "sales": round(sales, 2),
            "date": date.strftime("%Y-%m-%d"),
            "region": region,
            "product": "pink morsel"
        })

# Write to your existing file
df = pd.DataFrame(data)
df.to_csv("pink_morsels_sales.csv", index=False)

print("Successfully populated pink_morsels_sales.csv with data!")