import os
import pandas as pd
import numpy as np

base_dir = r"c:\Articulo\analysis_output"
all_data = []

for root, dirs, files in os.walk(base_dir):
    if "raw_sensors_data.csv" in files:
        file_path = os.path.join(root, "raw_sensors_data.csv")
        try:
            df = pd.read_csv(file_path)
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

if not all_data:
    print("No data found.")
else:
    full_df = pd.concat(all_data, ignore_index=True)
    
    # Filter out failed trials
    full_df = full_df[full_df['failed'] == False]
    
    # Map 'presential' and 'remote' to match document terms if needed
    # (The CSV uses 'presential' and 'remote')
    
    stats = full_df.groupby(['mode', 'sensor_id'])['time_s'].agg(['mean', 'std', 'count']).reset_index()
    print("Summary Statistics:")
    print(stats)
    
    # Prepare data for correlation analysis
    # We need to match trials. In this dataset, trial i presencial vs trial i remote
    # are separate folders: prueba_i_presencial and prueba_i_remoto.
    # The experiment_id looks like 'sim_presential_1' or 'sim_remote_1'.
    
    full_df['trial_number'] = full_df['experiment_id'].str.extract('(\d+)').astype(int)
    
    pivot_df = full_df.pivot(index=['trial_number', 'sensor_id'], columns='mode', values='time_s').reset_index()
    
    print("\nCorrelation by Sensor:")
    for sensor in sorted(full_df['sensor_id'].unique()):
        sensor_data = pivot_df[pivot_df['sensor_id'] == sensor].dropna()
        if len(sensor_data) > 1:
            corr = np.corrcoef(sensor_data['presential'], sensor_data['remote'])[0, 1]
            print(f"Sensor {sensor}: r = {corr:.4f} (n={len(sensor_data)})")
        else:
            print(f"Sensor {sensor}: Not enough data for correlation.")
