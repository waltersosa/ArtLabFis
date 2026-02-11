import os
import pandas as pd
import numpy as np

# Define the root directory containing the experiment folders
root_dir = r"C:\Articulo\analysis_output"
output_file = r"C:\Articulo\final_stats.txt"

def calculate_stats():
    all_data = []

    with open(output_file, "w") as f_out:
        f_out.write(f"Scanning directory: {root_dir}\n")

        # Walk through the directory structure
        count = 0
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "raw_sensors_data.csv":
                    file_path = os.path.join(dirpath, filename)
                    try:
                        df = pd.read_csv(file_path)
                        all_data.append(df)
                        count += 1
                    except Exception as e:
                        f_out.write(f"Error reading {file_path}: {e}\n")
        
        f_out.write(f"Found {count} files.\n")

        if not all_data:
            f_out.write("No data found.\n")
            return

        # Combine all dataframes
        full_df = pd.concat(all_data, ignore_index=True)

        # Filter out failed experiments if the column exists
        if 'failed' in full_df.columns:
            full_df = full_df[full_df['failed'] == False]

        # Ensure numeric types
        full_df['time_s'] = pd.to_numeric(full_df['time_s'], errors='coerce')
        full_df['sensor_id'] = pd.to_numeric(full_df['sensor_id'], errors='coerce')

        # Group by mode and sensor_id, then calculate stats
        stats = full_df.groupby(['mode', 'sensor_id'])['time_s'].agg(['mean', 'std', 'count']).reset_index()

        # Round values for display
        stats['mean'] = stats['mean'].round(2)
        stats['std'] = stats['std'].round(2)

        f_out.write("\n--- Calculated Statistics ---\n")
        f_out.write(stats.to_string())
        f_out.write("\n")

        # Formatted output for easy copy-pasting
        f_out.write("\n\n--- formatted for LaTeX ---\n")
        for sensor_id in sorted(stats['sensor_id'].unique()):
            f_out.write(f"Sensor S{int(sensor_id)}:\n")
            sensor_data = stats[stats['sensor_id'] == sensor_id]
            for _, row in sensor_data.iterrows():
                f_out.write(f"  {row['mode']}: Mean={row['mean']:.2f}, Std={row['std']:.2f}, N={int(row['count'])}\n")

if __name__ == "__main__":
    calculate_stats()
