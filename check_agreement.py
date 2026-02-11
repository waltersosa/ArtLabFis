import os
import pandas as pd
import numpy as np

root_dir = r"c:\Articulo\analysis_output"
all_data = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    if "raw_sensors_data.csv" in filenames:
        try:
            df = pd.read_csv(os.path.join(dirpath, "raw_sensors_data.csv"))
            all_data.append(df)
        except:
            pass

if not all_data:
    print("No data found.")
    exit()

df = pd.concat(all_data)
df = df[df['failed'] == False]

# Aggregated Stats
stats = df.groupby(['mode', 'sensor_id'])['time_s'].agg(['mean', 'std', 'count']).unstack('mode')
print("--- Aggregated Stats ---")
print(stats)

# Correlation
df['trial'] = df['experiment_id'].str.extract('(\d+)').astype(int)
pivot = df.pivot(index=['trial', 'sensor_id'], columns='mode', values='time_s').reset_index()

print("\n--- Pearson Correlation ---")
for s in sorted(df['sensor_id'].unique()):
    s_data = pivot[pivot['sensor_id'] == s].dropna()
    if len(s_data) > 1:
        corr = np.corrcoef(s_data['presential'], s_data['remote'])[0, 1]
        print(f"Sensor {s}: r = {corr:.4f} (n={len(s_data)})")
    else:
        print(f"Sensor {s}: n={len(s_data)}")
