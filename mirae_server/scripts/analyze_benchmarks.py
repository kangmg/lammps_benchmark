#!/usr/bin/env python3
"""
LAMMPS Benchmark Results Analyzer for Mirae Server

Compares conda LAMMPS (lmp_mpi_conda) vs optimized LAMMPS (lmp) performance
across different MPI × OpenMP configurations on 48-core CPU system.
"""

import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# ============================================================================
# Configuration
# ============================================================================

# Color scheme
BINARY_COLORS = {
    "conda": "#3498db",    # Blue
    "opt": "#e74c3c",      # Red (optimized)
}

CONFIG_ORDER = [
    "serial",
    "mpi48-omp1",
    "mpi24-omp2", 
    "mpi12-omp4",
    "mpi6-omp8",
    "mpi1-omp48"
]

BENCHMARKS = ['LJ', 'EAM', 'CHAIN', 'RHODO', 'REAXFF']


# ============================================================================
# Parsing Functions
# ============================================================================

def parse_benchmark_file(filepath: Path) -> dict:
    """Parse benchmark results from markdown file."""
    content = filepath.read_text(encoding='utf-8')
    
    results = {}
    
    for bench in BENCHMARKS:
        pattern = rf'### {bench} Benchmark'
        match = re.search(pattern, content, re.IGNORECASE)
        
        if match:
            # Find the table after the header
            section = content[match.start():match.start() + 3000]
            
            # Parse table rows
            rows = []
            for line in section.split('\n'):
                if '|' in line and 'Configuration' not in line and '---' not in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 2 and parts[0] in [
                        'conda-serial', 'opt-serial',
                        'conda-mpi48-omp1', 'conda-mpi24-omp2', 'conda-mpi12-omp4', 
                        'conda-mpi6-omp8', 'conda-mpi1-omp48',
                        'opt-mpi48-omp1', 'opt-mpi24-omp2', 'opt-mpi12-omp4',
                        'opt-mpi6-omp8', 'opt-mpi1-omp48'
                    ]:
                        try:
                            config = parts[0]
                            loop_time = float(parts[1])
                            
                            # Parse binary and config type
                            if config.startswith('conda-'):
                                binary = 'conda'
                                cfg = config.replace('conda-', '')
                            else:
                                binary = 'opt'
                                cfg = config.replace('opt-', '')
                            
                            rows.append({
                                'config': config,
                                'binary': binary,
                                'cfg_type': cfg,
                                'loop_time': loop_time
                            })
                        except (ValueError, IndexError):
                            pass
            
            if rows:
                results[bench] = rows
    
    return results


def parse_scaling_file(filepath: Path) -> pd.DataFrame:
    """Parse ReaxFF scaling benchmark results."""
    content = filepath.read_text(encoding='utf-8')
    
    all_data = []
    replicates = ['3x3x3', '4x4x4', '5x5x5', '6x6x6']
    atoms_map = {'3x3x3': 8208, '4x4x4': 19456, '5x5x5': 38000, '6x6x6': 65664}
    
    for rep in replicates:
        pattern = rf'### Replicate {rep}'
        match = re.search(pattern, content)
        
        if match:
            section = content[match.start():match.start() + 1500]
            
            for line in section.split('\n'):
                if '|' in line and 'Config' not in line and '---' not in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 3:
                        try:
                            config = parts[0]
                            loop_time = float(parts[1])
                            
                            if config.startswith('conda-'):
                                binary = 'conda'
                                cfg = config.replace('conda-', '')
                            elif config.startswith('opt-'):
                                binary = 'opt'
                                cfg = config.replace('opt-', '')
                            else:
                                continue
                            
                            all_data.append({
                                'replicate': rep,
                                'atoms': atoms_map.get(rep, 0),
                                'config': config,
                                'binary': binary,
                                'cfg_type': cfg,
                                'loop_time': loop_time
                            })
                        except (ValueError, IndexError):
                            pass
    
    return pd.DataFrame(all_data)


# ============================================================================
# Plotting Functions
# ============================================================================

def plot_benchmark_speedup(data: dict, output_dir: Path):
    """Create speedup plot for official benchmarks."""
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    for idx, bench in enumerate(BENCHMARKS):
        ax = axes[idx]
        bench_data = data.get(bench, [])
        
        if not bench_data:
            ax.set_visible(False)
            continue
        
        # Get serial baselines
        conda_serial = next((d['loop_time'] for d in bench_data 
                            if d['config'] == 'conda-serial'), None)
        opt_serial = next((d['loop_time'] for d in bench_data 
                          if d['config'] == 'opt-serial'), None)
        
        if not conda_serial or not opt_serial:
            ax.set_visible(False)
            continue
        
        # Calculate speedups relative to own serial
        config_order = ['mpi48-omp1', 'mpi24-omp2', 'mpi12-omp4', 'mpi6-omp8', 'mpi1-omp48']
        x = np.arange(len(config_order))
        width = 0.35
        
        conda_speedups = []
        opt_speedups = []
        
        for cfg in config_order:
            conda_time = next((d['loop_time'] for d in bench_data 
                              if d['config'] == f'conda-{cfg}'), None)
            opt_time = next((d['loop_time'] for d in bench_data 
                            if d['config'] == f'opt-{cfg}'), None)
            
            conda_speedups.append(conda_serial / conda_time if conda_time else 0)
            opt_speedups.append(opt_serial / opt_time if opt_time else 0)
        
        bars1 = ax.bar(x - width/2, conda_speedups, width, label='conda (lmp_mpi_conda)', 
                      color=BINARY_COLORS['conda'], edgecolor='black')
        bars2 = ax.bar(x + width/2, opt_speedups, width, label='opt (lmp)', 
                      color=BINARY_COLORS['opt'], edgecolor='black')
        
        # Add value labels
        for bar, speedup in zip(bars1, conda_speedups):
            if speedup > 0:
                ax.annotate(f'{speedup:.1f}x', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                           xytext=(0, 3), textcoords="offset points", ha='center', fontsize=7)
        for bar, speedup in zip(bars2, opt_speedups):
            if speedup > 0:
                ax.annotate(f'{speedup:.1f}x', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                           xytext=(0, 3), textcoords="offset points", ha='center', fontsize=7)
        
        ax.set_xticks(x)
        ax.set_xticklabels(['48×1', '24×2', '12×4', '6×8', '1×48'], fontsize=9)
        ax.set_xlabel('MPI × OMP', fontsize=10)
        ax.set_ylabel('Speedup (vs Serial)', fontsize=10)
        ax.set_title(f'{bench}', fontsize=12, fontweight='bold')
        ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(fontsize=8)
    
    # Hide 6th subplot
    axes[5].set_visible(False)
    
    plt.suptitle('Benchmark 1: Official LAMMPS + ReaxFF - MPI/OMP Hybrid Scaling\n(Speedup vs Serial, Higher is Better)', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    plt.savefig(output_dir / 'benchmark1_speedup.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: benchmark1_speedup.png")


def plot_scaling_results(scaling_data: pd.DataFrame, output_dir: Path):
    """Create ReaxFF scaling plot."""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    replicates = ['3x3x3', '4x4x4', '5x5x5', '6x6x6']
    atoms = [8208, 19456, 38000, 65664]
    
    # Left: Execution time comparison (best config each)
    ax1 = axes[0]
    
    for binary, color in BINARY_COLORS.items():
        # Use 6×8 config (best for opt, good for conda)
        times = []
        for rep in replicates:
            cfg = 'mpi6-omp8'
            rep_data = scaling_data[(scaling_data['replicate'] == rep) & 
                                   (scaling_data['binary'] == binary) &
                                   (scaling_data['cfg_type'] == cfg)]
            if not rep_data.empty:
                times.append(rep_data['loop_time'].values[0])
            else:
                times.append(np.nan)
        
        label = 'conda (lmp_mpi_conda)' if binary == 'conda' else 'opt (lmp)'
        ax1.plot(atoms, times, 'o-', color=color, linewidth=2, markersize=8, label=label)
    
    ax1.set_xlabel('Number of Atoms', fontsize=12)
    ax1.set_ylabel('Loop Time (s)', fontsize=12)
    ax1.set_title('Execution Time vs System Size (6 MPI × 8 OMP)', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_xticks(atoms)
    ax1.set_xticklabels([f'{a//1000}k' for a in atoms])
    
    # Right: Binary comparison speedup
    ax2 = axes[1]
    
    x = np.arange(len(replicates))
    width = 0.5
    
    speedups = []
    for rep in replicates:
        conda_data = scaling_data[(scaling_data['replicate'] == rep) & 
                                  (scaling_data['config'] == 'conda-mpi48-omp1')]
        opt_data = scaling_data[(scaling_data['replicate'] == rep) & 
                               (scaling_data['config'] == 'opt-mpi6-omp8')]
        
        if not conda_data.empty and not opt_data.empty:
            speedup = conda_data['loop_time'].values[0] / opt_data['loop_time'].values[0]
            speedups.append(speedup)
        else:
            speedups.append(0)
    
    bars = ax2.bar(x, speedups, width, color=BINARY_COLORS['opt'], edgecolor='black')
    
    for bar, speedup in zip(bars, speedups):
        if speedup > 0:
            ax2.annotate(f'{speedup:.1f}x', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10, fontweight='bold')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{rep}\n({a//1000}k atoms)' for rep, a in zip(replicates, atoms)])
    ax2.set_ylabel('Speedup (opt vs conda baseline)', fontsize=12)
    ax2.set_title('Optimized Binary Speedup\n(vs conda 48 MPI × 1 OMP)', fontsize=12, fontweight='bold')
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Benchmark 2: ReaxFF Scaling Performance\n(Higher is Better)', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    plt.savefig(output_dir / 'benchmark2_scaling.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: benchmark2_scaling.png")


# ============================================================================
# Summary Generation
# ============================================================================

def generate_summary_tables(bench_data: dict, scaling_data: pd.DataFrame):
    """Generate verified summary tables for README."""
    
    print("\n" + "=" * 60)
    print("VERIFIED SUMMARY DATA FOR README")
    print("=" * 60)
    
    # Benchmark 1: Best configs
    print("\n### Benchmark 1: Best Configuration by Benchmark\n")
    print("| Benchmark | Best conda | Speedup | Best opt | Speedup | opt vs conda |")
    print("|-----------|------------|---------|----------|---------|--------------|")
    
    for bench in BENCHMARKS:
        bench_results = bench_data.get(bench, [])
        if not bench_results:
            continue
        
        # Get serial baselines
        conda_serial = next((d['loop_time'] for d in bench_results if d['config'] == 'conda-serial'), None)
        opt_serial = next((d['loop_time'] for d in bench_results if d['config'] == 'opt-serial'), None)
        
        if not conda_serial or not opt_serial:
            continue
        
        # Find best conda config
        conda_configs = [d for d in bench_results if d['binary'] == 'conda' and d['cfg_type'] != 'serial']
        best_conda = min(conda_configs, key=lambda x: x['loop_time'])
        conda_speedup = conda_serial / best_conda['loop_time']
        conda_cfg = best_conda['cfg_type'].replace('mpi', '').replace('omp', '×')
        
        # Find best opt config
        opt_configs = [d for d in bench_results if d['binary'] == 'opt' and d['cfg_type'] != 'serial']
        best_opt = min(opt_configs, key=lambda x: x['loop_time'])
        opt_speedup = opt_serial / best_opt['loop_time']
        opt_cfg = best_opt['cfg_type'].replace('mpi', '').replace('omp', '×')
        
        # opt vs conda (best vs best time comparison)
        opt_vs_conda = best_conda['loop_time'] / best_opt['loop_time']
        
        print(f"| **{bench}** | {conda_cfg} | {conda_speedup:.1f}x | {opt_cfg} | {opt_speedup:.1f}x | **{opt_vs_conda:.1f}x faster** |")
    
    # Benchmark 2: Scaling
    print("\n### Benchmark 2: ReaxFF Scaling (Best Configs)\n")
    print("| System | Atoms | conda 1×48 (s) | opt 6×8 (s) | opt Speedup |")
    print("|--------|-------|----------------|-------------|-------------|")
    
    replicates = ['3x3x3', '4x4x4', '5x5x5', '6x6x6']
    atoms_map = {'3x3x3': 8208, '4x4x4': 19456, '5x5x5': 38000, '6x6x6': 65664}
    
    for rep in replicates:
        conda_data = scaling_data[(scaling_data['replicate'] == rep) & 
                                  (scaling_data['config'] == 'conda-mpi1-omp48')]
        opt_data = scaling_data[(scaling_data['replicate'] == rep) & 
                               (scaling_data['config'] == 'opt-mpi6-omp8')]
        
        if not conda_data.empty and not opt_data.empty:
            conda_time = conda_data['loop_time'].values[0]
            opt_time = opt_data['loop_time'].values[0]
            speedup = conda_time / opt_time
            atoms = atoms_map[rep]
            print(f"| {rep} | {atoms:,} | {conda_time:.2f} | {opt_time:.2f} | **{speedup:.1f}x** |")
    
    print("\n" + "=" * 60)


# ============================================================================
# Main
# ============================================================================

def main():
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / 'figures'
    output_dir.mkdir(exist_ok=True)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    print("=" * 60)
    print("LAMMPS Benchmark Results Analyzer - Mirae Server")
    print("=" * 60)
    
    # Parse benchmark 1 data
    print("\n[1/2] Parsing official+reaxff benchmark...")
    bench_path = base_dir / 'official+reaxff' / 'benchmark_results.md'
    bench_data = parse_benchmark_file(bench_path)
    print(f"  Found: {list(bench_data.keys())}")
    
    # Parse benchmark 2 data
    print("\n[2/2] Parsing ReaxFF scaling benchmark...")
    scaling_path = base_dir / 'reaxff_scailing' / 'reaxff_scaling_results.md'
    scaling_data = parse_scaling_file(scaling_path)
    print(f"  Scaling data: {len(scaling_data)} rows")
    
    # Generate figures
    print("\n[3/3] Generating figures...")
    plot_benchmark_speedup(bench_data, output_dir)
    plot_scaling_results(scaling_data, output_dir)
    
    # Generate summary tables
    generate_summary_tables(bench_data, scaling_data)
    
    print(f"\nFigures saved to: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()

