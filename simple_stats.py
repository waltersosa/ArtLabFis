import csv
from pathlib import Path

base_dir = Path(r'C:\Articulo\analysis_output')

# Collect all time values for each sensor and mode
pres = {1:[], 2:[], 3:[], 4:[]}
rem = {1:[], 2:[], 3:[], 4:[]}

for i in range(1, 36):
    # Presencial
    f = base_dir / f'prueba_{i}_presencial' / 'csv' / 'raw_sensors_data.csv'
    if f.exists():
        with open(f) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sid = int(row['sensor_id'])
                t = float(row['time_s'])
                pres[sid].append(t)
    
    # Remote
    f = base_dir / f'prueba_{i}_remoto' / 'csv' / 'raw_sensors_data.csv'
    if f.exists():
        with open(f) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sid = int(row['sensor_id'])
                t = float(row['time_s'])
                rem[sid].append(t)

# Calculate stats
import math

def stats(data):
    n = len(data)
    if n == 0:
        return 0, 0, 0
    mean = sum(data) / n
    if n > 1:
        variance = sum((x - mean)**2 for x in data) / (n - 1)
        std = math.sqrt(variance)
    else:
        std = 0
    return mean, std, n

# Print results in LaTeX format
for s in [1,2,3,4]:
    print(f"\n% Sensor S{s}")
    pm, ps, pn = stats(pres[s])
    rm, rs, rn = stats(rem[s])
    print(f"Presencial & {pm:.2f} & {ps:.2f} & {pn} \\\\")
    print(f"Remote     & {rm:.2f} & {rs:.2f} & {rn} \\\\")
