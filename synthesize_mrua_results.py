"""
Script de síntesis y agregación de resultados de experimentos MRUA
Agrega datos de múltiples ensayos por modalidad (remoto vs presencial)
y genera métricas estadísticas globales y visualizaciones consolidadas.

Autor: Sistema de análisis MRUA
Fecha: 2026
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


# ============ CONFIGURACIÓN ============
BASE_DIR = Path(__file__).parent
ANALYSIS_OUTPUT_DIR = BASE_DIR / "analysis_output"
SUMMARY_OUTPUT_DIR = ANALYSIS_OUTPUT_DIR / "summary_results"
SUMMARY_CSV_DIR = SUMMARY_OUTPUT_DIR / "csv"
SUMMARY_GRAPHS_DIR = SUMMARY_OUTPUT_DIR / "graphs"


# ============ FUNCIONES DE LECTURA DE DATOS ============

def find_experiment_folders(base_dir: Path) -> Dict[str, List[Path]]:
    """
    Encuentra todas las carpetas de experimentos y las agrupa por modalidad.
    Limita a 70 ensayos por modalidad.
    
    Args:
        base_dir: Directorio base donde buscar carpetas de experimentos
        
    Returns:
        Diccionario con listas de rutas agrupadas por modalidad (máximo 30 por modalidad)
        {'remote': [Path, ...], 'presential': [Path, ...]}
    """
    folders = {'remote': [], 'presential': []}
    
    if not base_dir.exists():
        print(f"[WARNING] Directorio no encontrado: {base_dir}")
        return folders
    
    for folder in base_dir.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name.lower()
        
        if 'remoto' in folder_name:
            folders['remote'].append(folder)
        elif 'presencial' in folder_name:
            folders['presential'].append(folder)
    
    # Ordenar por número de prueba
    for mode in folders:
        folders[mode].sort(key=lambda x: int(''.join(filter(str.isdigit, x.name))) if any(c.isdigit() for c in x.name) else 0)
    
    # Filtrar solo carpetas con datos válidos primero
    valid_folders = {'remote': [], 'presential': []}
    
    for mode in folders:
        for folder in folders[mode]:
            # Verificar si existe el archivo de aceleraciones y no está vacío
            accel_path = folder / "csv" / "accelerations.csv"
            if accel_path.exists() and accel_path.stat().st_size > 0:
                try:
                    # Lectura rápida para confirmar
                    df_check = pd.read_csv(accel_path, nrows=1)
                    if not df_check.empty:
                        valid_folders[mode].append(folder)
                except:
                    pass
    
    folders = valid_folders

    # Limitar a 70 ensayos por modalidad
    MAX_EXPERIMENTS_PER_MODE = 70
    for mode in folders:
        if len(folders[mode]) > MAX_EXPERIMENTS_PER_MODE:
            print(f"[INFO] Limitando {mode} a {MAX_EXPERIMENTS_PER_MODE} ensayos validos (encontrados {len(folders[mode])})")
            folders[mode] = folders[mode][:MAX_EXPERIMENTS_PER_MODE]
    
    return folders


def load_csv_from_folder(folder_path: Path, filename: str) -> pd.DataFrame:
    """
    Carga un archivo CSV desde una carpeta de experimento.
    
    Args:
        folder_path: Ruta a la carpeta del experimento
        filename: Nombre del archivo CSV
        
    Returns:
        DataFrame con los datos, o DataFrame vacío si no existe
    """
    csv_path = folder_path / "csv" / filename
    
    if not csv_path.exists():
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(csv_path)
        # Agregar identificador del experimento
        df['experiment_folder'] = folder_path.name
        return df
    except Exception as e:
        print(f"[WARNING] Error leyendo {csv_path}: {e}")
        return pd.DataFrame()


def aggregate_raw_sensors_data(folders: Dict[str, List[Path]]) -> pd.DataFrame:
    """
    Agrega todos los datos crudos de sensores de todos los ensayos.
    
    Args:
        folders: Diccionario con carpetas agrupadas por modalidad
        
    Returns:
        DataFrame consolidado con todos los datos de sensores
    """
    all_data = []
    
    for mode, folder_list in folders.items():
        for folder in folder_list:
            df = load_csv_from_folder(folder, "raw_sensors_data.csv")
            if not df.empty:
                # Asegurar que el modo esté correcto
                df['mode'] = mode
                all_data.append(df)
    
    if not all_data:
        return pd.DataFrame()
    
    return pd.concat(all_data, ignore_index=True)


def aggregate_velocities(folders: Dict[str, List[Path]]) -> pd.DataFrame:
    """
    Agrega todos los datos de velocidades de todos los ensayos.
    
    Args:
        folders: Diccionario con carpetas agrupadas por modalidad
        
    Returns:
        DataFrame consolidado con todas las velocidades
    """
    all_data = []
    
    for mode, folder_list in folders.items():
        for folder in folder_list:
            df = load_csv_from_folder(folder, "velocities.csv")
            if not df.empty:
                df['mode'] = mode
                all_data.append(df)
    
    if not all_data:
        return pd.DataFrame()
    
    return pd.concat(all_data, ignore_index=True)


def aggregate_accelerations(folders: Dict[str, List[Path]]) -> pd.DataFrame:
    """
    Agrega todos los datos de aceleraciones de todos los ensayos.
    
    Args:
        folders: Diccionario con carpetas agrupadas por modalidad
        
    Returns:
        DataFrame consolidado con todas las aceleraciones
    """
    all_data = []
    
    for mode, folder_list in folders.items():
        for folder in folder_list:
            df = load_csv_from_folder(folder, "accelerations.csv")
            if not df.empty:
                df['mode'] = mode
                # Filtrar solo aceleraciones promedio (sin sensor_from/sensor_to)
                df_avg = df[df['sensor_from'].isna() | (df['sensor_from'].isnull())]
                if not df_avg.empty:
                    all_data.append(df_avg)
    
    if not all_data:
        return pd.DataFrame()
    
    return pd.concat(all_data, ignore_index=True)


def aggregate_comparison_data(folders: Dict[str, List[Path]]) -> pd.DataFrame:
    """
    Agrega todos los datos de comparación remoto vs presencial.
    
    Args:
        folders: Diccionario con carpetas agrupadas por modalidad
        
    Returns:
        DataFrame consolidado con datos de comparación
    """
    all_data = []
    
    for mode, folder_list in folders.items():
        for folder in folder_list:
            df = load_csv_from_folder(folder, "comparison_remote_vs_presential.csv")
            if not df.empty:
                all_data.append(df)
    
    if not all_data:
        return pd.DataFrame()
    
    return pd.concat(all_data, ignore_index=True)


def aggregate_failure_statistics(folders: Dict[str, List[Path]]) -> pd.DataFrame:
    """
    Agrega todas las estadísticas de fallos de todos los ensayos.
    
    Args:
        folders: Diccionario con carpetas agrupadas por modalidad
        
    Returns:
        DataFrame consolidado con estadísticas de fallos
    """
    all_data = []
    
    for mode, folder_list in folders.items():
        for folder in folder_list:
            df = load_csv_from_folder(folder, "failure_statistics.csv")
            if not df.empty:
                # Asegurar que el modo esté correcto
                df['mode'] = mode
                all_data.append(df)
    
    if not all_data:
        return pd.DataFrame()
    
    return pd.concat(all_data, ignore_index=True)


# ============ CÁLCULO DE MÉTRICAS ESTADÍSTICAS ============

def calculate_time_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas de tiempo por sensor y modalidad.
    
    Args:
        df: DataFrame con datos de sensores agregados
        
    Returns:
        DataFrame con estadísticas (media, std, count) por sensor y modalidad
    """
    if df.empty:
        return pd.DataFrame()
    
    stats = df.groupby(['sensor_id', 'mode'])['time_s'].agg([
        'mean', 'std', 'count'
    ]).reset_index()
    
    stats.columns = ['sensor_id', 'mode', 'time_mean', 'time_std', 'count']
    stats['time_std'] = stats['time_std'].fillna(0)
    
    return stats


def calculate_relative_error_statistics(comparison_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas de error relativo por sensor.
    
    Args:
        comparison_df: DataFrame con datos de comparación
        
    Returns:
        DataFrame con error relativo promedio y desviación estándar por sensor
    """
    if comparison_df.empty or 'error_relativo_pct' not in comparison_df.columns:
        return pd.DataFrame()
    
    # Agrupar por sensor y calcular estadísticas
    stats = comparison_df.groupby('sensor_id')['error_relativo_pct'].agg([
        'mean', 'std', 'count'
    ]).reset_index()
    
    stats.columns = ['sensor_id', 'error_mean', 'error_std', 'count']
    stats['error_std'] = stats['error_std'].fillna(0)
    
    return stats


def calculate_velocity_statistics(velocities_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas de velocidad por posición del sensor.
    
    Args:
        velocities_df: DataFrame con velocidades agregadas
        
    Returns:
        DataFrame con velocidad promedio y desviación estándar por posición
    """
    if velocities_df.empty:
        return pd.DataFrame()
    
    stats = velocities_df.groupby(['position_cm', 'mode'])['velocity_ms'].agg([
        'mean', 'std', 'count'
    ]).reset_index()
    
    stats.columns = ['position_cm', 'mode', 'velocity_mean', 'velocity_std', 'count']
    stats['velocity_std'] = stats['velocity_std'].fillna(0)
    
    return stats


def calculate_acceleration_statistics(accelerations_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas de aceleración por modalidad.
    
    Args:
        accelerations_df: DataFrame con aceleraciones agregadas
        
    Returns:
        DataFrame con aceleración promedio y desviación estándar por modalidad
    """
    if accelerations_df.empty:
        return pd.DataFrame()
    
    # Filtrar solo aceleraciones promedio (sin sensor_from/sensor_to)
    df_clean = accelerations_df[
        accelerations_df['sensor_from'].isna() | 
        accelerations_df['sensor_from'].isnull()
    ].copy()
    
    if df_clean.empty:
        return pd.DataFrame()
    
    stats = df_clean.groupby('mode')['acceleration_ms2'].agg([
        'mean', 'std', 'count'
    ]).reset_index()
    
    stats.columns = ['mode', 'acceleration_mean', 'acceleration_std', 'count']
    stats['acceleration_std'] = stats['acceleration_std'].fillna(0)
    
    return stats


def calculate_failure_statistics_summary(failure_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas globales de fallos por modalidad.
    
    Args:
        failure_df: DataFrame con estadísticas de fallos agregadas
        
    Returns:
        DataFrame con estadísticas globales de fallos
    """
    if failure_df.empty:
        return pd.DataFrame()
    
    # Agrupar por modalidad y sumar
    summary = failure_df.groupby('mode').agg({
        'total_experiments': 'sum',
        'failed_count': 'sum',
        'success_count': 'sum'
    }).reset_index()
    
    # Calcular tasa de fallos
    summary['failure_rate_pct'] = (summary['failed_count'] / summary['total_experiments'] * 100).round(2)
    summary['success_rate_pct'] = (summary['success_count'] / summary['total_experiments'] * 100).round(2)
    
    return summary


# ============ GENERACIÓN DE GRÁFICAS ============

def plot_time_vs_sensor_summary(stats_df: pd.DataFrame, output_path: Path):
    """
    Gráfica: Tiempo de paso vs sensor (promedio ± desviación estándar).
    
    Args:
        stats_df: DataFrame con estadísticas de tiempo
        output_path: Ruta donde guardar la gráfica
    """
    if stats_df.empty:
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    remote = stats_df[stats_df['mode'] == 'remote']
    presential = stats_df[stats_df['mode'] == 'presential']
    
    if not remote.empty:
        ax.errorbar(
            remote['sensor_id'],
            remote['time_mean'],
            yerr=remote['time_std'],
            marker='o',
            linestyle='--',
            label='Remoto',
            capsize=5,
            capthick=2,
            markersize=8
        )
    
    if not presential.empty:
        ax.errorbar(
            presential['sensor_id'],
            presential['time_mean'],
            yerr=presential['time_std'],
            marker='s',
            linestyle='--',
            label='Presencial',
            capsize=5,
            capthick=2,
            markersize=8
        )
    
    ax.set_xlabel('Número de Sensor', fontsize=12)
    ax.set_ylabel('Tiempo de Paso (s)', fontsize=12)
    ax.set_title('Tiempo de Paso vs Sensor: Promedio ± Desviación Estándar', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Gráfica guardada: {output_path}")


def plot_failure_statistics_summary(failure_stats: pd.DataFrame, output_path: Path):
    """
    Gráfica: Intentos totales y fallos por modalidad (remoto vs presencial).
    
    Args:
        failure_stats: DataFrame con estadísticas de fallos por modalidad
        output_path: Ruta donde guardar la gráfica
    """
    if failure_stats.empty:
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Preparar datos
    modes = failure_stats['mode'].values
    total_experiments = failure_stats['total_experiments'].values
    failed_count = failure_stats['failed_count'].values
    success_count = failure_stats['success_count'].values
    
    # Mapear modos a etiquetas
    mode_labels = ['Remoto' if m == 'remote' else 'Presencial' for m in modes]
    colors = ['#3498db', '#e74c3c']  # Azul para remoto, rojo para presencial
    
    # Gráfica 1: Barras apiladas (Total, Exitosos, Fallidos)
    x_pos = np.arange(len(mode_labels))
    width = 0.6
    
    bars1 = ax1.bar(x_pos, success_count, width, label='Exitosos', color='#2ecc71', alpha=0.8)
    bars2 = ax1.bar(x_pos, failed_count, width, bottom=success_count, label='Fallidos', color='#e74c3c', alpha=0.8)
    
    # Anotar valores en las barras
    for i, (total, success, failed) in enumerate(zip(total_experiments, success_count, failed_count)):
        ax1.text(i, total + 1, f'Total: {int(total)}', ha='center', va='bottom', fontweight='bold')
        ax1.text(i, success/2, f'{int(success)}', ha='center', va='center', fontweight='bold', color='white')
        if failed > 0:
            ax1.text(i, success + failed/2, f'{int(failed)}', ha='center', va='center', fontweight='bold', color='white')
    
    ax1.set_xlabel('Modalidad', fontsize=12)
    ax1.set_ylabel('Número de Experimentos', fontsize=12)
    ax1.set_title('Intentos Totales y Fallos por Modalidad', fontsize=14, fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(mode_labels)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Gráfica 2: Tasa de fallos (%)
    failure_rates = failure_stats['failure_rate_pct'].values
    success_rates = failure_stats['success_rate_pct'].values
    
    bars3 = ax2.bar(x_pos, success_rates, width, label='Tasa de Éxito (%)', color='#2ecc71', alpha=0.8)
    bars4 = ax2.bar(x_pos, failure_rates, width, bottom=success_rates, label='Tasa de Fallo (%)', color='#e74c3c', alpha=0.8)
    
    # Anotar valores
    for i, (success_rate, failure_rate) in enumerate(zip(success_rates, failure_rates)):
        ax2.text(i, success_rate/2, f'{success_rate:.1f}%', ha='center', va='center', fontweight='bold', color='white')
        if failure_rate > 0:
            ax2.text(i, success_rate + failure_rate/2, f'{failure_rate:.1f}%', ha='center', va='center', fontweight='bold', color='white')
    
    ax2.set_xlabel('Modalidad', fontsize=12)
    ax2.set_ylabel('Porcentaje (%)', fontsize=12)
    ax2.set_title('Tasa de Éxito y Fallo por Modalidad', fontsize=14, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(mode_labels)
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Gráfica guardada: {output_path}")


def plot_velocity_vs_position_summary(velocity_stats: pd.DataFrame, output_path: Path):
    """
    Gráfica: Velocidad promedio vs posición del sensor.
    
    Args:
        velocity_stats: DataFrame con estadísticas de velocidad
        output_path: Ruta donde guardar la gráfica
    """
    if velocity_stats.empty:
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    remote = velocity_stats[velocity_stats['mode'] == 'remote']
    presential = velocity_stats[velocity_stats['mode'] == 'presential']
    
    if not remote.empty:
        ax.errorbar(
            remote['position_cm'],
            remote['velocity_mean'],
            yerr=remote['velocity_std'],
            marker='o',
            linestyle='--',
            label='Remoto',
            capsize=5,
            capthick=2,
            markersize=8
        )
    
    if not presential.empty:
        ax.errorbar(
            presential['position_cm'],
            presential['velocity_mean'],
            yerr=presential['velocity_std'],
            marker='s',
            linestyle='--',
            label='Presencial',
            capsize=5,
            capthick=2,
            markersize=8
        )
    
    ax.set_xlabel('Posición del Sensor (cm)', fontsize=12)
    ax.set_ylabel('Velocidad Promedio (m/s)', fontsize=12)
    ax.set_title('Velocidad Promedio vs Posición del Sensor', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Gráfica guardada: {output_path}")


def plot_acceleration_distribution(accelerations_df: pd.DataFrame, accel_stats: pd.DataFrame, output_path: Path):
    """
    Gráfica: Distribución de aceleración (boxplot remoto vs presencial).
    
    Args:
        accelerations_df: DataFrame con todas las aceleraciones
        accel_stats: DataFrame con estadísticas de aceleración
        output_path: Ruta donde guardar la gráfica
    """
    if accelerations_df.empty:
        return
    
    # Filtrar solo aceleraciones promedio
    df_clean = accelerations_df[
        accelerations_df['sensor_from'].isna() | 
        accelerations_df['sensor_from'].isnull()
    ].copy()
    
    if df_clean.empty:
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    remote_acc = df_clean[df_clean['mode'] == 'remote']['acceleration_ms2'].dropna()
    presential_acc = df_clean[df_clean['mode'] == 'presential']['acceleration_ms2'].dropna()
    
    data_to_plot = []
    labels = []
    
    if not remote_acc.empty:
        data_to_plot.append(remote_acc)
        labels.append('Remoto')
    
    if not presential_acc.empty:
        data_to_plot.append(presential_acc)
        labels.append('Presencial')
    
    if not data_to_plot:
        return
    
    bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True, widths=0.6)
    
    # Colorear cajas
    colors = ['lightblue', 'lightcoral']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Agregar estadísticas como texto
    if not accel_stats.empty:
        for i, (mode, row) in enumerate(accel_stats.iterrows()):
            mode_label = 'Remoto' if row['mode'] == 'remote' else 'Presencial'
            mean_val = row['acceleration_mean']
            std_val = row['acceleration_std']
            count_val = int(row['count'])
            ax.text(i + 1, mean_val, f'μ={mean_val:.3f}\nσ={std_val:.3f}\nn={count_val}',
                   ha='center', va='bottom', fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_ylabel('Aceleración (m/s²)', fontsize=12)
    ax.set_title('Distribución de Aceleración: Remoto vs Presencial', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Gráfica guardada: {output_path}")


def plot_experimental_vs_theoretical_summary(raw_df: pd.DataFrame, output_path: Path):
    """
    Gráfica: Comparación experimental promedio vs modelo teórico MRUA.
    
    Args:
        raw_df: DataFrame con datos de sensores agregados
        output_path: Ruta donde guardar la gráfica
    """
    if raw_df.empty:
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Calcular promedios por modalidad y sensor
    summary = raw_df.groupby(['mode', 'sensor_id']).agg({
        'time_s': 'mean',
        'distance_cm': 'mean'
    }).reset_index()
    
    # Calcular aceleración promedio por modalidad
    accel_by_mode = {}
    for mode in summary['mode'].unique():
        mode_data = summary[summary['mode'] == mode].sort_values('sensor_id')
        if len(mode_data) >= 2:
            # Calcular aceleración usando v = d/t y a = Δv/Δt
            times = mode_data['time_s'].values
            distances = mode_data['distance_cm'].values / 100.0  # Convertir a metros
            
            if len(times) >= 3 and all(t > 0 for t in times[1:]):
                velocities = []
                for i in range(1, len(times)):
                    if times[i] - times[i-1] > 0:
                        v = (distances[i] - distances[i-1]) / (times[i] - times[i-1])
                        velocities.append(v)
                
                if len(velocities) >= 2:
                    accelerations = []
                    for i in range(1, len(velocities)):
                        if times[i+1] - times[i] > 0:
                            a = (velocities[i] - velocities[i-1]) / (times[i+1] - times[i])
                            accelerations.append(a)
                    
                    if accelerations:
                        accel_by_mode[mode] = np.mean(accelerations)
    
    # Graficar datos experimentales
    for mode in summary['mode'].unique():
        mode_data = summary[summary['mode'] == mode].sort_values('sensor_id')
        label_mode = 'Remoto' if mode == 'remote' else 'Presencial'
        marker = 'o' if mode == 'remote' else 's'
        
        ax.scatter(
            mode_data['time_s'],
            mode_data['distance_cm'] / 100.0,
            marker=marker,
            s=100,
            label=f'{label_mode} - Experimental',
            alpha=0.7,
            edgecolors='black',
            linewidths=1.5
        )
        
        # Modelo teórico si tenemos aceleración
        if mode in accel_by_mode:
            a = accel_by_mode[mode]
            t_max = mode_data['time_s'].max()
            t_theoretical = np.linspace(0, t_max, 100)
            x_theoretical = 0.5 * a * t_theoretical ** 2
            
            ax.plot(
                t_theoretical,
                x_theoretical,
                linestyle='--',
                linewidth=2,
                label=f'{label_mode} - Teórico (a={a:.3f} m/s²)',
                alpha=0.8
            )
    
    ax.set_xlabel('Tiempo (s)', fontsize=12)
    ax.set_ylabel('Distancia (m)', fontsize=12)
    ax.set_title('Comparación Experimental Promedio vs Modelo Teórico MRUA', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Gráfica guardada: {output_path}")


# ============ EXPORTACIÓN DE RESULTADOS ============

def export_summary_csvs(
    time_stats: pd.DataFrame,
    error_stats: pd.DataFrame,
    velocity_stats: pd.DataFrame,
    accel_stats: pd.DataFrame,
    failure_stats: pd.DataFrame,
    output_dir: Path
):
    """
    Exporta todas las tablas resumen a CSV.
    
    Args:
        time_stats: Estadísticas de tiempo
        error_stats: Estadísticas de error relativo
        velocity_stats: Estadísticas de velocidad
        accel_stats: Estadísticas de aceleración
        failure_stats: Estadísticas de fallos
        output_dir: Directorio donde guardar los CSV
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not time_stats.empty:
        csv_path = output_dir / "summary_time_by_sensor.csv"
        time_stats.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"[OK] CSV guardado: {csv_path}")
    
    if not error_stats.empty:
        csv_path = output_dir / "summary_relative_error.csv"
        error_stats.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"[OK] CSV guardado: {csv_path}")
    
    if not velocity_stats.empty:
        csv_path = output_dir / "summary_velocity.csv"
        velocity_stats.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"[OK] CSV guardado: {csv_path}")
    
    if not accel_stats.empty:
        csv_path = output_dir / "summary_acceleration.csv"
        accel_stats.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"[OK] CSV guardado: {csv_path}")
    
    if not failure_stats.empty:
        csv_path = output_dir / "summary_failure_statistics.csv"
        failure_stats.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"[OK] CSV guardado: {csv_path}")


def export_individual_sensor_tables(raw_df: pd.DataFrame, output_dir: Path):
    """
    Genera y exporta tablas individuales por cada sensor con todos los ensayos (N=70+).
    Formato científico detallado.
    
    Args:
        raw_df: DataFrame con todos los datos crudos
        output_dir: Directorio de salida
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if raw_df.empty:
        return

    print("\n[INFO] Generando tablas individuales por sensor...")
    
    # Mapeo de nombres de columnas para presentación
    col_map = {
        'experiment_id': 'ID Ensayo',
        'time_s': 'Tiempo (s)',
        'mode': 'Modalidad',
        'distance_cm': 'Distancia (cm)'
    }
    
    for sensor_id in sorted(raw_df['sensor_id'].unique()):
        # Filtrar datos del sensor
        sensor_data = raw_df[raw_df['sensor_id'] == sensor_id].copy()
        
        # Seleccionar y renombrar columnas
        table = sensor_data[['experiment_id', 'mode', 'time_s', 'distance_cm']].copy()
        table.rename(columns=col_map, inplace=True)
        
        # Ordenar para presentación limpia
        table.sort_values(by=['Modalidad', 'ID Ensayo'], inplace=True)
        
        # Exportar
        filename = f"sensor_S{int(sensor_id)}_individual_results.csv"
        csv_path = output_dir / filename
        table.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"[OK] Tabla individual guardada: {csv_path} (N={len(table)})")


def plot_sensor_correlation_graphs(raw_df: pd.DataFrame, output_dir: Path):
    """
    Genera gráficos de correlación científica por sensor.
    1. Scatter plot: Presencial vs Remoto (Time) con Pearson r.
    
    Args:
        raw_df: DataFrame con todos los datos crudos
        output_dir: Directorio de salida
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if raw_df.empty:
        return
        
    print("\n[INFO] Generando gráficos de correlación científica...")
    
    # Asegurar que tenemos un identificador común para el "número de prueba"
    # Asumimos que el experiment_id contiene algo como "prueba_X_..." o que podemos extraer un índice
    # Para simplificar, agruparemos por el orden de aparición o un índice extraído si es posible.
    # Dado que los IDs son generados, vamos a intentar usar un índice secuencial por modalidad.
    
    # Crear un índice secuencial por (sensor, mode)
    raw_df['seq_index'] = raw_df.groupby(['sensor_id', 'mode']).cumcount()
    
    # Pivotar para tener presencial y remoto alineados por índice secuencial
    pivot_df = raw_df.pivot_table(
        index=['sensor_id', 'seq_index'], 
        columns='mode', 
        values='time_s'
    ).reset_index()
    
    # Solo si tenemos ambas modalidades
    if 'presential' not in pivot_df.columns or 'remote' not in pivot_df.columns:
        print("[WARNING] No se pueden generar correlaciones: falta una de las modalidades.")
        return

    pivot_df.dropna(subset=['presential', 'remote'], inplace=True)
    
    for sensor_id in sorted(pivot_df['sensor_id'].unique()):
        sensor_data = pivot_df[pivot_df['sensor_id'] == sensor_id]
        
        if len(sensor_data) < 5:
            continue
            
        x = sensor_data['presential'].values.astype(float)
        y = sensor_data['remote'].values.astype(float)
        
        # Verificar varianza para evitar errores de LinAlg
        x_std = np.std(x)
        y_std = np.std(y)
        
        r, m, b = 0, 0, 0
        r_sq = 0
        has_stats = False

        if x_std > 1e-9 and y_std > 1e-9:
            try:
                # Calcular Pearson r y regresión lineal con Numpy
                # Pendiente (m) y corte (b)
                m, b = np.polyfit(x, y, 1)
                
                # Pearson r
                r = np.corrcoef(x, y)[0, 1]
                r_sq = r**2
                has_stats = True
            except Exception as e:
                print(f"[WARNING] Error calculando regresión para Sensor {sensor_id}: {e}")
        else:
            print(f"[INFO] Saltando regresión para Sensor {sensor_id} (varianza cero)")
            
        # Gráfico
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Puntos
        ax.scatter(x, y, alpha=0.7, c='navy', edgecolors='white', s=60, label='Ensayos Experimentales')
        
        if has_stats:
            # Línea de tendencia
            line = m * x + b
            ax.plot(x, line, 'r--', label=f'Tendencia (y={m:.2f}x + {b:.2f})')
        
            # Textos
            stats_text = (f"Pearson r = {r:.4f}\n"
                          f"R² = {r_sq:.4f}\n"
                          f"N = {len(sensor_data)}")
            
            ax.text(0.05, 0.95, stats_text, transform=ax.transAxes, 
                    fontsize=11, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        else:
            # Si no hay estadísticas (ej. datos constantes), mostrar solo N
            stats_text = f"N = {len(sensor_data)}\nData Constante"
            ax.text(0.05, 0.95, stats_text, transform=ax.transAxes, 
                    fontsize=11, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        # Línea de identidad perfecta (y=x)
        min_val = min(x.min(), y.min())
        max_val = max(x.max(), y.max())
        # Evitar rango cero para graficar
        if min_val == max_val:
            min_val -= 1
            max_val += 1
            
        ax.plot([min_val, max_val], [min_val, max_val], 'k:', alpha=0.5, label='Identidad (y=x)')
        
        ax.set_title(f"Correlación Remoto vs Presencial - Sensor {int(sensor_id)}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Tiempo Presencial (s)", fontsize=12)
        ax.set_ylabel("Tiempo Remoto (s)", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='lower right')
        
        # Guardar
        filename = f"correlation_sensor_S{int(sensor_id)}.png"
        path = output_dir / filename
        plt.tight_layout()
        plt.savefig(path, dpi=300)
        plt.close()
        print(f"[OK] Gráfico correlación guardado: {path}")


# ============ FUNCIÓN PRINCIPAL ============

def main():
    """
    Función principal que ejecuta todo el pipeline de síntesis.
    """
    print("=" * 60)
    print("SÍNTESIS DE RESULTADOS MRUA")
    print("=" * 60)
    
    # 1. Encontrar todas las carpetas de experimentos
    print("\n[INFO] Buscando carpetas de experimentos...")
    folders = find_experiment_folders(ANALYSIS_OUTPUT_DIR)
    
    remote_count = len(folders['remote'])
    presential_count = len(folders['presential'])
    
    print(f"[OK] Encontradas {remote_count} pruebas remotas y {presential_count} pruebas presenciales")
    
    if remote_count == 0 and presential_count == 0:
        print("[ERROR] No se encontraron carpetas de experimentos")
        return
    
    # 2. Agregar datos de todos los ensayos
    print("\n[INFO] Agregando datos de todos los ensayos...")
    
    raw_df = aggregate_raw_sensors_data(folders)
    velocities_df = aggregate_velocities(folders)
    accelerations_df = aggregate_accelerations(folders)
    comparison_df = aggregate_comparison_data(folders)
    failure_df = aggregate_failure_statistics(folders)
    
    print(f"[OK] Datos agregados:")
    print(f"   - Sensores: {len(raw_df)} registros")
    print(f"   - Velocidades: {len(velocities_df)} registros")
    print(f"   - Aceleraciones: {len(accelerations_df)} registros")
    print(f"   - Comparaciones: {len(comparison_df)} registros")
    print(f"   - Estadísticas de fallos: {len(failure_df)} registros")
    
    # 3. Calcular métricas estadísticas globales
    print("\n[INFO] Calculando métricas estadísticas globales...")
    
    time_stats = calculate_time_statistics(raw_df)
    error_stats = calculate_relative_error_statistics(comparison_df)
    velocity_stats = calculate_velocity_statistics(velocities_df)
    accel_stats = calculate_acceleration_statistics(accelerations_df)
    failure_stats = calculate_failure_statistics_summary(failure_df)
    
    # Mostrar resumen
    print("\n--- Resumen de Tiempos por Sensor ---")
    if not time_stats.empty:
        print(time_stats.to_string(index=False))
    
    print("\n--- Resumen de Error Relativo ---")
    if not error_stats.empty:
        print(error_stats.to_string(index=False))
        
    # 4. Exportar resultados (tablas resumen)
    print("\n[INFO] Exportando tablas resumen...")
    export_summary_csvs(
        time_stats, 
        error_stats, 
        velocity_stats, 
        accel_stats, 
        failure_stats, 
        SUMMARY_CSV_DIR
    )
    
    # 5. Exportar TABLAS CIENTÍFICAS DETALLADAS (Nuevos requerimientos)
    print("\n[INFO] Generando reportes científicos detallados...")
    export_individual_sensor_tables(raw_df, SUMMARY_CSV_DIR)
    
    # 6. Generar gráficas resumen estándar
    print("\n[INFO] Generando gráficas resumen...")
    plot_time_vs_sensor_summary(time_stats, SUMMARY_GRAPHS_DIR / "time_vs_sensor_summary.png")
    plot_failure_statistics_summary(failure_stats, SUMMARY_GRAPHS_DIR / "failure_statistics_summary.png")
    plot_velocity_vs_position_summary(velocity_stats, SUMMARY_GRAPHS_DIR / "velocity_vs_position_summary.png")
    plot_acceleration_distribution(accelerations_df, accel_stats, SUMMARY_GRAPHS_DIR / "acceleration_distribution.png")
    plot_experimental_vs_theoretical_summary(raw_df, SUMMARY_GRAPHS_DIR / "experimental_vs_theoretical_summary.png")
    
    # 7. Generar GRÁFICAS DE CORRELACIÓN (Nuevos requerimientos)
    plot_sensor_correlation_graphs(raw_df, SUMMARY_GRAPHS_DIR)
    
    print("\n" + "=" * 60)
    print("SÍNTESIS CIENTÍFICA COMPLETADA")
    print(f"   - Tablas detalladas: {SUMMARY_CSV_DIR}")
    print(f"   - Gráficas de correlación: {SUMMARY_GRAPHS_DIR}")
    print("=" * 60)    
    print("\n--- Resumen de Estadísticas de Fallos ---")
    if not failure_stats.empty:
        print(failure_stats.to_string(index=False))
    
    print("\n--- Resumen de Velocidades ---")
    if not velocity_stats.empty:
        print(velocity_stats.to_string(index=False))
    
    print("\n--- Resumen de Aceleraciones ---")
    if not accel_stats.empty:
        print(accel_stats.to_string(index=False))
    
    # 4. Crear directorios de salida
    os.makedirs(SUMMARY_CSV_DIR, exist_ok=True)
    os.makedirs(SUMMARY_GRAPHS_DIR, exist_ok=True)
    
    print(f"\n[INFO] Directorios creados:")
    print(f"   - CSV: {SUMMARY_CSV_DIR}")
    print(f"   - Gráficas: {SUMMARY_GRAPHS_DIR}")
    
    # 5. Generar gráficas agregadas
    print("\n[INFO] Generando gráficas agregadas...")
    
    plot_time_vs_sensor_summary(time_stats, SUMMARY_GRAPHS_DIR / "time_vs_sensor_summary.png")
    plot_failure_statistics_summary(failure_stats, SUMMARY_GRAPHS_DIR / "failure_statistics_summary.png")
    plot_velocity_vs_position_summary(velocity_stats, SUMMARY_GRAPHS_DIR / "velocity_vs_position_summary.png")
    plot_acceleration_distribution(accelerations_df, accel_stats, SUMMARY_GRAPHS_DIR / "acceleration_distribution.png")
    plot_experimental_vs_theoretical_summary(raw_df, SUMMARY_GRAPHS_DIR / "experimental_vs_theoretical_summary.png")
    
    # 6. Exportar tablas resumen a CSV
    print("\n[INFO] Exportando tablas resumen a CSV...")
    export_summary_csvs(time_stats, error_stats, velocity_stats, accel_stats, failure_stats, SUMMARY_CSV_DIR)
    
    print("\n" + "=" * 60)
    print("[OK] Síntesis de resultados completada!")
    print(f"   - Resultados guardados en: {SUMMARY_OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
