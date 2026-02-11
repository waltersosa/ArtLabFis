import pandas as pd
import numpy as np
from pathlib import Path
import sys

base_dir = Path(r'C:\Articulo\analysis_output')

# Collect data
data_presencial = {1: [], 2: [], 3: [], 4: []}
data_remote = {1: [], 2: [], 3: [], 4: []}

print("Reading data...")
for i in range(1, 36):  # 35 trials each
    # Presencial
    try:
        csv_file = base_dir / f'prueba_{i}_presencial' / 'csv' / 'raw_sensors_data.csv'
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            sensor_id = int(row['sensor_id'])
            time_s = float(row['time_s'])
            data_presencial[sensor_id].append(time_s)
    except Exception as e:
        print(f"Error reading presencial {i}: {e}")
    
    # Remote
    try:
        csv_file = base_dir / f'prueba_{i}_remoto' / 'csv' / 'raw_sensors_data.csv'
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            sensor_id = int(row['sensor_id'])
            time_s = float(row['time_s'])
            data_remote[sensor_id].append(time_s)
    except Exception as e:
        print(f"Error reading remote {i}: {e}")

print("\n" + "="*60)
print("STATISTICS SUMMARY")
print("="*60)

# Print statistics
for sensor in [1, 2, 3, 4]:
    print(f"\n--- SENSOR S{sensor} ---")
    
    # Presencial
    pres_data = np.array(data_presencial[sensor])
    pres_mean = np.mean(pres_data)
    pres_std = np.std(pres_data, ddof=1)
    pres_n = len(pres_data)
    
    print(f"Presencial: {pres_mean:.2f} & {pres_std:.2f} & {pres_n}")
    
    # Remote
    rem_data = np.array(data_remote[sensor])
    rem_mean = np.mean(rem_data)
    rem_std = np.std(rem_data, ddof=1)
    rem_n = len(rem_data)
    
    print(f"Remote:     {rem_mean:.2f} & {rem_std:.2f} & {rem_n}")

print("\n" + "="*60)
sys.stdout.flush()
