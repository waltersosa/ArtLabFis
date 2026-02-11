import pandas as pd
import numpy as np
from pathlib import Path

# Directories
base_dir = Path(r'C:\Articulo\analysis_output')
output_dir = base_dir / 'summary_results' / 'csv'
output_dir.mkdir(parents=True, exist_ok=True)

# Collect all data
all_data = []

for trial_dir in base_dir.glob('prueba_*'):
    csv_file = trial_dir / 'csv' / 'raw_sensors_data.csv'
    if csv_file.exists():
        df = pd.read_csv(csv_file)
        all_data.append(df)

# Combine all data
combined_df = pd.concat(all_data, ignore_index=True)

print("=" * 80)
print("ANÁLISIS DE DATOS EXPERIMENTALES")
print("=" * 80)

# Calculate statistics for each sensor and mode
results = []

for mode in ['presential', 'remote']:
    mode_data = combined_df[combined_df['mode'] == mode]
    
    for sensor in [1, 2, 3, 4]:
        sensor_data = mode_data[mode_data['sensor_id'] == sensor]
        
        if len(sensor_data) > 0:
            stats = {
                'Mode': 'Presencial' if mode == 'presential' else 'Remote',
                'Sensor': f'S{sensor}',
                'Mean (s)': sensor_data['time_s'].mean(),
                'Std (s)': sensor_data['time_s'].std(),
                'N': len(sensor_data)
            }
            results.append(stats)
            
            print(f"\n{stats['Mode']} - Sensor {sensor}:")
            print(f"  Mean: {stats['Mean (s)']:.4f} s")
            print(f"  Std:  {stats['Std (s)']:.4f} s")
            print(f"  N:    {stats['N']}")

# Create results DataFrame
results_df = pd.DataFrame(results)

# Save to CSV
results_csv = output_dir / 'statistics_summary.csv'
results_df.to_csv(results_csv, index=False)
print(f"\n✓ Saved statistics to: {results_csv}")

# Generate LaTeX table format
print("\n" + "=" * 80)
print("LATEX TABLE FORMAT")
print("=" * 80)

for sensor_num in [1, 2, 3, 4]:
    print(f"\n% Sensor S{sensor_num}")
    print(f"\\begin{{table}}[H]")
    print(f"\t\\caption{{Statistical results for Sensor S{sensor_num}.}}")
    print(f"\t\\label{{tab:s{sensor_num}_results}}")
    print(f"\t\\centering")
    print(f"\t\\small")
    print(f"\t\\begin{{tabular}}{{lccc}}")
    print(f"\t\t\\toprule")
    print(f"\t\t\\textbf{{Modality}} & \\textbf{{\\(\\bar{{x}}\\) (s)}} & \\textbf{{\\(s\\) (s)}} & \\textbf{{\\(n\\)}} \\\\")
    print(f"\t\t\\midrule")
    
    for mode in ['Presencial', 'Remote']:
        row = results_df[(results_df['Sensor'] == f'S{sensor_num}') & (results_df['Mode'] == mode)]
        if not row.empty:
            mean_val = row['Mean (s)'].values[0]
            std_val = row['Std (s)'].values[0]
            n_val = int(row['N'].values[0])
            print(f"\t\t{mode:10s} & {mean_val:.2f} & {std_val:.2f} & {n_val} \\\\")
    
    print(f"\t\t\\bottomrule")
    print(f"\t\\end{{tabular}}")
    print(f"\\end{{table}}")

print("\n" + "=" * 80)
print("DONE!")
print("=" * 80)
