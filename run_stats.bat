@echo off
python calculate_stats.py > final_stats.txt 2>&1
if %errorlevel% neq 0 (
    echo Python failed with error level %errorlevel% >> final_stats.txt
    py calculate_stats.py >> final_stats.txt 2>&1
)
