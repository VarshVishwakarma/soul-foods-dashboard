import pandas as pd
import numpy as np
import os

# Define the file name
file_name = "pink_morsels_sales.csv"

# Create fake data
dates = pd.date_range(start="2024-01-01", periods=100, freq='D')
regions = ['north', 'east', 'south', 'west']
data = []

for date in dates:
    for region in regions:
        data.append({
            "sales": round(np.random.uniform(50, 500), 2),
            "date": date.strftime("%Y-%m-%d"),
            "region": region,
            "product": "pink morsel"
        })

# Create DataFrame
df = pd.DataFrame(data)

# Write to CSV - This will overwrite the empty file
df.to_csv(file_name, index=False)

if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
    print(f"✅ Success! {file_name} now contains {len(df)} rows of data.")
else:
    print("❌ Something went wrong. The file is still empty.")