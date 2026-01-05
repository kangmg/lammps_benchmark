#!/usr/bin/env python3
"""
LAMMPS Benchmark Results Analyzer

Groups results into 4 execution categories:
1. lmp_gpu - MPI only (CPU parallel)
2. lmp_gpu - w/ CUDA (GPU package)
3. lmp_kokkos - MPI only (CPU parallel)  
4. lmp_kokkos - w/ KOKKOS (CUDA backend)

All speedups are calculated relative to CPU-1 (Serial) baseline.
"""

import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# ============================================================================
# Configuration Aliases and Commands
# ============================================================================

COMMAND_ALIASES = {
    # lmp_gpu image - MPI only
    "GPU-CPU-1": {
        "group": "lmp_gpu (MPI)",
        "alias": "CPU-1",
        "command": "lmp_gpu -in <input>",
        "cores": 1,
        "gpu": False
    },
    "GPU-CPU-4": {
        "group": "lmp_gpu (MPI)",
        "alias": "CPU-4",
        "command": "mpirun -np 4 lmp_gpu -in <input>",
        "cores": 4,
        "gpu": False
    },
    "GPU-CPU-8": {
        "group": "lmp_gpu (MPI)",
        "alias": "CPU-8",
        "command": "mpirun -np 8 lmp_gpu -in <input>",
        "cores": 8,
        "gpu": False
    },
    "GPU-CPU-12": {
        "group": "lmp_gpu (MPI)",
        "alias": "CPU-12",
        "command": "mpirun -np 12 lmp_gpu -in <input>",
        "cores": 12,
        "gpu": False
    },
    # lmp_gpu image - w/ CUDA
    "GPU-CUDA-1": {
        "group": "lmp_gpu (CUDA)",
        "alias": "CUDA-1",
        "command": "lmp_gpu -sf gpu -pk gpu 1 -in <input>",
        "cores": 1,
        "gpu": True
    },
    "GPU-CUDA-MPI4": {
        "group": "lmp_gpu (CUDA)",
        "alias": "CUDA-MPI4",
        "command": "mpirun -np 4 lmp_gpu -sf gpu -pk gpu 1 -in <input>",
        "cores": 4,
        "gpu": True
    },
    "GPU-CUDA-MPI12": {
        "group": "lmp_gpu (CUDA)",
        "alias": "CUDA-MPI12",
        "command": "mpirun -np 12 lmp_gpu -sf gpu -pk gpu 1 -in <input>",
        "cores": 12,
        "gpu": True
    },
    # lmp_kokkos image - MPI only
    "KK-CPU-1": {
        "group": "lmp_kokkos (MPI)",
        "alias": "CPU-1",
        "command": "lmp_kokkos -in <input>",
        "cores": 1,
        "gpu": False
    },
    "KK-CPU-4": {
        "group": "lmp_kokkos (MPI)",
        "alias": "CPU-4",
        "command": "mpirun -np 4 lmp_kokkos -in <input>",
        "cores": 4,
        "gpu": False
    },
    "KK-CPU-8": {
        "group": "lmp_kokkos (MPI)",
        "alias": "CPU-8",
        "command": "mpirun -np 8 lmp_kokkos -in <input>",
        "cores": 8,
        "gpu": False
    },
    "KK-CPU-12": {
        "group": "lmp_kokkos (MPI)",
        "alias": "CPU-12",
        "command": "mpirun -np 12 lmp_kokkos -in <input>",
        "cores": 12,
        "gpu": False
    },
    # lmp_kokkos image - w/ KOKKOS (CUDA backend)
    "KK-GPU-1": {
        "group": "lmp_kokkos (KOKKOS)",
        "alias": "KOKKOS-1",
        "command": "mpirun -np 1 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input>",
        "cores": 1,
        "gpu": True
    },
    "KK-GPU-MPI8": {
        "group": "lmp_kokkos (KOKKOS)",
        "alias": "KOKKOS-MPI8",
        "command": "mpirun -np 8 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input>",
        "cores": 8,
        "gpu": True
    },
    "KK-GPU-MPI12": {
        "group": "lmp_kokkos (KOKKOS)",
        "alias": "KOKKOS-MPI12",
        "command": "mpirun -np 12 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input>",
        "cores": 12,
        "gpu": True
    },
}

# Color scheme for groups
GROUP_COLORS = {
    "lmp_gpu (MPI)": "#3498db",      # Blue
    "lmp_gpu (CUDA)": "#e74c3c",     # Red
    "lmp_kokkos (MPI)": "#9b59b6",   # Purple
    "lmp_kokkos (KOKKOS)": "#27ae60" # Green
}

# ============================================================================
# Parsing Functions
# ============================================================================

def parse_markdown_table(content: str, start_pattern: str) -> list[dict]:
    """Parse a markdown table following a specific pattern."""
    lines = content.split('\n')
    results = []
    in_table = False
    headers = []
    
    for i, line in enumerate(lines):
        if start_pattern in line and '|' in line:
            in_table = True
            headers = [h.strip() for h in line.split('|') if h.strip()]
            continue
        
        if in_table:
            if '---' in line:
                continue
            if not line.strip() or '|' not in line:
                break
            
            values = [v.strip() for v in line.split('|') if v.strip()]
            if len(values) == len(headers):
                row = dict(zip(headers, values))
                results.append(row)
    
    return results


def parse_benchmark_file(filepath: Path, image_type: str) -> dict:
    """Parse benchmark results and normalize configuration names."""
    content = filepath.read_text(encoding='utf-8')
    
    results = {}
    benchmarks = ['LJ', 'EAM', 'CHAIN', 'RHODO', 'REAXFF']
    
    for bench in benchmarks:
        pattern = rf'### {bench} Benchmark'
        if pattern.lower().replace(' benchmark', '') in content.lower():
            # Find table
            match = re.search(rf'### {bench}[^\n]*\n\n\|', content, re.IGNORECASE)
            if match:
                section = content[match.start():match.start() + 2000]
                table_data = parse_markdown_table(section, 'Configuration')
                
                if table_data:
                    # Normalize configuration names
                    normalized_data = []
                    for row in table_data:
                        config = row.get('Configuration', '')
                        loop_time = float(row.get('Loop Time (s)', 0))
                        
                        # Map to unified config names
                        unified_config = normalize_config(config, image_type)
                        if unified_config:
                            normalized_data.append({
                                'config': unified_config,
                                'loop_time': loop_time,
                                'original': config
                            })
                    
                    results[bench] = normalized_data
    
    return results


def normalize_config(config: str, image_type: str) -> str:
    """Map original config names to unified names."""
    if image_type == "cuda":
        mapping = {
            "CPU-1": "GPU-CPU-1",
            "CPU-4": "GPU-CPU-4",
            "CPU-8": "GPU-CPU-8",
            "CPU-12": "GPU-CPU-12",
            "GPU-1": "GPU-CUDA-1",
            "GPU-MPI4": "GPU-CUDA-MPI4",
            "GPU-MPI12": "GPU-CUDA-MPI12",
        }
    else:  # kokkos
        mapping = {
            "CPU-1": "KK-CPU-1",
            "CPU-4": "KK-CPU-4",
            "CPU-8": "KK-CPU-8",
            "CPU-12": "KK-CPU-12",
            "KOKKOS-GPU-MPI1": "KK-GPU-1",
            "KOKKOS-GPU-MPI8": "KK-GPU-MPI8",
            "KOKKOS-GPU-MPI12": "KK-GPU-MPI12",
        }
    return mapping.get(config)


def parse_scaling_file(filepath: Path, image_type: str) -> pd.DataFrame:
    """Parse scaling benchmark results."""
    content = filepath.read_text(encoding='utf-8')
    
    all_data = []
    replicates = ['3x3x3', '4x4x4', '5x5x5', '6x6x6']
    atoms_map = {'3x3x3': 8208, '4x4x4': 19456, '5x5x5': 38000, '6x6x6': 65664}
    
    for rep in replicates:
        pattern = rf'### Replicate {rep}'
        match = re.search(pattern, content)
        
        if match:
            section = content[match.start():match.start() + 1000]
            table_data = parse_markdown_table(section, 'Config')
            
            for row in table_data:
                config = row.get('Config', '')
                loop_time = float(row.get('Loop Time (s)', 0))
                
                unified_config = normalize_scaling_config(config, image_type)
                if unified_config:
                    all_data.append({
                        'replicate': rep,
                        'atoms': atoms_map[rep],
                        'config': unified_config,
                        'loop_time': loop_time,
                        'group': COMMAND_ALIASES.get(unified_config, {}).get('group', 'Unknown')
                    })
    
    return pd.DataFrame(all_data)


def normalize_scaling_config(config: str, image_type: str) -> str:
    """Map scaling config names to unified names."""
    if image_type == "cuda":
        mapping = {
            "CPU-1": "GPU-CPU-1",
            "CPU-4": "GPU-CPU-4",
            "CPU-8": "GPU-CPU-8",
            "CPU-12": "GPU-CPU-12",
            "GPU-1": "GPU-CUDA-1",
            "GPU-MPI4": "GPU-CUDA-MPI4",
        }
    else:  # kokkos
        mapping = {
            "CPU-1": "KK-CPU-1",
            "CPU-4": "KK-CPU-4",
            "CPU-8": "KK-CPU-8",
            "CPU-12": "KK-CPU-12",
            "KOKKOS-GPU-MPI1": "KK-GPU-1",
            "KOKKOS-GPU-MPI2": "KK-GPU-MPI2",
        }
    return mapping.get(config)


# ============================================================================
# Plotting Functions
# ============================================================================

def plot_benchmark_speedup(cuda_data: dict, kokkos_data: dict, output_dir: Path):
    """Create speedup plot for official benchmarks + ReaxFF."""
    
    benchmarks = ['LJ', 'EAM', 'CHAIN', 'RHODO', 'REAXFF']
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    for idx, bench in enumerate(benchmarks):
        ax = axes[idx]
        
        # Combine data from both images
        cuda_bench = cuda_data.get(bench, [])
        kokkos_bench = kokkos_data.get(bench, [])
        
        # Get CPU-1 baseline (from cuda image)
        baseline = None
        for item in cuda_bench:
            if item['config'] == 'GPU-CPU-1':
                baseline = item['loop_time']
                break
        
        if baseline is None:
            ax.set_visible(False)
            continue
        
        # Organize by group
        groups = {
            "lmp_gpu (MPI)": [],
            "lmp_gpu (CUDA)": [],
            "lmp_kokkos (MPI)": [],
            "lmp_kokkos (KOKKOS)": []
        }
        
        for item in cuda_bench:
            config_info = COMMAND_ALIASES.get(item['config'])
            if config_info:
                speedup = baseline / item['loop_time']
                groups[config_info['group']].append({
                    'alias': config_info['alias'],
                    'speedup': speedup,
                    'cores': config_info['cores']
                })
        
        for item in kokkos_bench:
            config_info = COMMAND_ALIASES.get(item['config'])
            if config_info:
                speedup = baseline / item['loop_time']
                groups[config_info['group']].append({
                    'alias': config_info['alias'],
                    'speedup': speedup,
                    'cores': config_info['cores']
                })
        
        # Plot grouped bars
        x_pos = 0
        x_ticks = []
        x_labels = []
        
        for group_name, items in groups.items():
            if not items:
                continue
            
            # Sort by cores
            items = sorted(items, key=lambda x: x['cores'])
            
            for item in items:
                bar = ax.bar(x_pos, item['speedup'], 
                           color=GROUP_COLORS[group_name],
                           edgecolor='black', linewidth=0.5, width=0.8)
                
                # Add value label
                ax.annotate(f'{item["speedup"]:.1f}x',
                           xy=(x_pos, item['speedup']),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=7,
                           fontweight='bold')
                
                x_ticks.append(x_pos)
                x_labels.append(item['alias'])
                x_pos += 1
            
            x_pos += 0.5  # Gap between groups
        
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('Speedup (vs CPU-1 Serial)', fontsize=10)
        ax.set_title(f'{bench}', fontsize=12, fontweight='bold')
        ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, None)
    
    # Hide 6th subplot
    axes[5].set_visible(False)
    
    # Add legend
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, label=name, edgecolor='black')
                      for name, color in GROUP_COLORS.items()]
    fig.legend(handles=legend_elements, loc='lower right', 
               bbox_to_anchor=(0.95, 0.12), fontsize=10)
    
    plt.suptitle('Benchmark 1: Official LAMMPS + ReaxFF Performance\n(Speedup vs CPU-1 Serial, Higher is Better)', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    plt.savefig(output_dir / 'benchmark1_speedup.png', dpi=150, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: benchmark1_speedup.png")


def plot_scaling_speedup(cuda_scaling: pd.DataFrame, kokkos_scaling: pd.DataFrame, output_dir: Path):
    """Create scaling speedup plot for ReaxFF."""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Combine data
    all_data = pd.concat([cuda_scaling, kokkos_scaling], ignore_index=True)
    
    replicates = ['3x3x3', '4x4x4', '5x5x5', '6x6x6']
    atoms = [8208, 19456, 38000, 65664]
    
    # Left plot: Execution time comparison
    ax1 = axes[0]
    
    for group_name, color in GROUP_COLORS.items():
        group_data = all_data[all_data['group'] == group_name]
        
        # Get single-GPU or best config for this group
        if 'CUDA' in group_name or 'KOKKOS' in group_name:
            # GPU groups - use single GPU config
            if 'CUDA' in group_name:
                config_filter = 'GPU-CUDA-1'
            else:
                config_filter = 'KK-GPU-1'
        else:
            # CPU groups - use 1 core
            if 'lmp_gpu' in group_name:
                config_filter = 'GPU-CPU-1'
            else:
                config_filter = 'KK-CPU-1'
        
        filtered = group_data[group_data['config'] == config_filter]
        if not filtered.empty:
            times = [filtered[filtered['replicate'] == rep]['loop_time'].values[0] 
                    if not filtered[filtered['replicate'] == rep].empty else np.nan 
                    for rep in replicates]
            ax1.plot(atoms, times, 'o-', color=color, linewidth=2, 
                    markersize=8, label=group_name)
    
    ax1.set_xlabel('Number of Atoms', fontsize=12)
    ax1.set_ylabel('Loop Time (s)', fontsize=12)
    ax1.set_title('Execution Time vs System Size', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)
    ax1.set_xticks(atoms)
    ax1.set_xticklabels([f'{a//1000}k' for a in atoms])
    
    # Right plot: Speedup vs CPU-1
    ax2 = axes[1]
    
    # Get GPU-CPU-1 baseline for each replicate
    baselines = {}
    for rep in replicates:
        cpu1_data = all_data[(all_data['replicate'] == rep) & 
                             (all_data['config'] == 'GPU-CPU-1')]
        if not cpu1_data.empty:
            baselines[rep] = cpu1_data['loop_time'].values[0]
    
    # Plot speedup for GPU configs only
    gpu_groups = ["lmp_gpu (CUDA)", "lmp_kokkos (KOKKOS)"]
    gpu_configs = {'lmp_gpu (CUDA)': 'GPU-CUDA-1', 'lmp_kokkos (KOKKOS)': 'KK-GPU-1'}
    
    x = np.arange(len(replicates))
    width = 0.35
    
    for i, (group_name, config) in enumerate(gpu_configs.items()):
        speedups = []
        for rep in replicates:
            gpu_data = all_data[(all_data['replicate'] == rep) & 
                               (all_data['config'] == config)]
            if not gpu_data.empty and rep in baselines:
                speedup = baselines[rep] / gpu_data['loop_time'].values[0]
                speedups.append(speedup)
            else:
                speedups.append(0)
        
        bars = ax2.bar(x + (i - 0.5) * width, speedups, width, 
                      label=group_name, color=GROUP_COLORS[group_name], edgecolor='black')
        
        # Add value labels
        for bar, speedup in zip(bars, speedups):
            if speedup > 0:
                height = bar.get_height()
                ax2.annotate(f'{speedup:.1f}x',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax2.set_xlabel('System Size', fontsize=12)
    ax2.set_ylabel('Speedup (vs CPU-1 Serial)', fontsize=12)
    ax2.set_title('GPU Speedup by System Size', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{rep}\n({a//1000}k atoms)' for rep, a in zip(replicates, atoms)])
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    
    plt.suptitle('Benchmark 2: ReaxFF Scaling Performance\n(Speedup vs CPU-1 Serial, Higher is Better)', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    plt.savefig(output_dir / 'benchmark2_scaling.png', dpi=150, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: benchmark2_scaling.png")


def generate_command_reference() -> str:
    """Generate command reference table in markdown."""
    
    lines = [
        "## Command Reference",
        "",
        "| Group | Alias | Command |",
        "|-------|-------|---------|"
    ]
    
    # Sort by group
    for group in ["lmp_gpu (MPI)", "lmp_gpu (CUDA)", "lmp_kokkos (MPI)", "lmp_kokkos (KOKKOS)"]:
        for config_id, info in COMMAND_ALIASES.items():
            if info['group'] == group:
                lines.append(f"| {group} | {info['alias']} | `{info['command']}` |")
    
    return "\n".join(lines)


def generate_benchmark1_tables(cuda_data: dict, kokkos_data: dict) -> str:
    """Generate Benchmark 1 result tables in markdown."""
    
    benchmarks = ['LJ', 'EAM', 'CHAIN', 'RHODO', 'REAXFF']
    lines = ["## Benchmark 1: Parsed Results (for README)", ""]
    
    for bench in benchmarks:
        cuda_bench = cuda_data.get(bench, [])
        kokkos_bench = kokkos_data.get(bench, [])
        
        # Get CPU-1 baseline (from cuda image)
        baseline = None
        for item in cuda_bench:
            if item['config'] == 'GPU-CPU-1':
                baseline = item['loop_time']
                break
        
        if baseline is None:
            continue
        
        lines.append(f"### {bench}")
        lines.append("")
        lines.append("| Group | Config | Loop Time (s) | Speedup |")
        lines.append("|-------|--------|---------------|---------|")
        
        # Combine and sort by group
        all_items = []
        for item in cuda_bench:
            config_info = COMMAND_ALIASES.get(item['config'])
            if config_info:
                speedup = baseline / item['loop_time']
                all_items.append({
                    'group': config_info['group'],
                    'alias': config_info['alias'],
                    'loop_time': item['loop_time'],
                    'speedup': speedup,
                    'cores': config_info['cores']
                })
        
        for item in kokkos_bench:
            config_info = COMMAND_ALIASES.get(item['config'])
            if config_info:
                speedup = baseline / item['loop_time']
                all_items.append({
                    'group': config_info['group'],
                    'alias': config_info['alias'],
                    'loop_time': item['loop_time'],
                    'speedup': speedup,
                    'cores': config_info['cores']
                })
        
        # Sort by group order then cores
        group_order = ["lmp_gpu (MPI)", "lmp_gpu (CUDA)", "lmp_kokkos (MPI)", "lmp_kokkos (KOKKOS)"]
        all_items.sort(key=lambda x: (group_order.index(x['group']), x['cores']))
        
        for item in all_items:
            lines.append(f"| {item['group']} | {item['alias']} | {item['loop_time']:.4f} | {item['speedup']:.2f}x |")
        
        lines.append("")
    
    return "\n".join(lines)


def generate_scaling_table(cuda_scaling: pd.DataFrame, kokkos_scaling: pd.DataFrame) -> str:
    """Generate Benchmark 2 scaling result tables in markdown."""
    
    lines = ["## Benchmark 2: ReaxFF Scaling Parsed Results", ""]
    
    # Combine data
    all_data = pd.concat([cuda_scaling, kokkos_scaling], ignore_index=True)
    
    replicates = ['3x3x3', '4x4x4', '5x5x5', '6x6x6']
    
    # Get baselines
    baselines = {}
    for rep in replicates:
        cpu1_data = all_data[(all_data['replicate'] == rep) & 
                             (all_data['config'] == 'GPU-CPU-1')]
        if not cpu1_data.empty:
            baselines[rep] = cpu1_data['loop_time'].values[0]
    
    lines.append("### Summary Table (GPU Speedup)")
    lines.append("")
    lines.append("| Replicate | Atoms | CPU-1 (s) | CUDA GPU-1 (s) | CUDA Speedup | KOKKOS GPU-1 (s) | KOKKOS Speedup |")
    lines.append("|-----------|-------|-----------|----------------|--------------|------------------|----------------|")
    
    for rep in replicates:
        atoms = all_data[all_data['replicate'] == rep]['atoms'].values[0] if not all_data[all_data['replicate'] == rep].empty else 0
        
        # CPU-1 baseline
        cpu1_time = baselines.get(rep, 0)
        
        # CUDA GPU-1
        cuda_gpu = all_data[(all_data['replicate'] == rep) & (all_data['config'] == 'GPU-CUDA-1')]
        cuda_time = cuda_gpu['loop_time'].values[0] if not cuda_gpu.empty else 0
        cuda_speedup = cpu1_time / cuda_time if cuda_time > 0 else 0
        
        # KOKKOS GPU-1
        kokkos_gpu = all_data[(all_data['replicate'] == rep) & (all_data['config'] == 'KK-GPU-1')]
        kokkos_time = kokkos_gpu['loop_time'].values[0] if not kokkos_gpu.empty else 0
        kokkos_speedup = cpu1_time / kokkos_time if kokkos_time > 0 else 0
        
        lines.append(f"| {rep} | {atoms:,} | {cpu1_time:.2f} | {cuda_time:.2f} | {cuda_speedup:.2f}x | {kokkos_time:.2f} | {kokkos_speedup:.2f}x |")
    
    lines.append("")
    
    # Detailed tables per replicate
    for rep in replicates:
        rep_data = all_data[all_data['replicate'] == rep]
        baseline = baselines.get(rep, 1)
        
        lines.append(f"### {rep} Details")
        lines.append("")
        lines.append("| Group | Config | Loop Time (s) | Speedup |")
        lines.append("|-------|--------|---------------|---------|")
        
        for _, row in rep_data.iterrows():
            config_info = COMMAND_ALIASES.get(row['config'], {})
            alias = config_info.get('alias', row['config'])
            group = row.get('group', 'Unknown')
            speedup = baseline / row['loop_time'] if row['loop_time'] > 0 else 0
            lines.append(f"| {group} | {alias} | {row['loop_time']:.2f} | {speedup:.2f}x |")
        
        lines.append("")
    
    return "\n".join(lines)


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
    print("LAMMPS Benchmark Results Analyzer")
    print("=" * 60)
    
    # Parse benchmark 1 data
    print("\n[1/4] Parsing CUDA image benchmark...")
    cuda_bench_path = base_dir / 'lammps_cuda_image' / 'official+reaxff_bench' / 'benchmark_results.md'
    cuda_data = parse_benchmark_file(cuda_bench_path, "cuda")
    print(f"  Found: {list(cuda_data.keys())}")
    
    print("\n[2/4] Parsing KOKKOS image benchmark...")
    kokkos_bench_path = base_dir / 'lammps_kokkos_image' / 'official+reaxff_bench' / 'benchmark_results.md'
    kokkos_data = parse_benchmark_file(kokkos_bench_path, "kokkos")
    print(f"  Found: {list(kokkos_data.keys())}")
    
    # Parse benchmark 2 data
    print("\n[3/4] Parsing scaling benchmarks...")
    cuda_scaling_path = base_dir / 'lammps_cuda_image' / 'reaxff_scaling_bench' / 'reaxff_scaling_results.md'
    cuda_scaling = parse_scaling_file(cuda_scaling_path, "cuda")
    print(f"  CUDA scaling: {len(cuda_scaling)} rows")
    
    kokkos_scaling_path = base_dir / 'lammps_kokkos_image' / 'reaxff_scaling' / 'reaxff_scaling_results.md'
    kokkos_scaling = parse_scaling_file(kokkos_scaling_path, "kokkos")
    print(f"  KOKKOS scaling: {len(kokkos_scaling)} rows")
    
    # Generate figures
    print("\n[4/4] Generating figures...")
    plot_benchmark_speedup(cuda_data, kokkos_data, output_dir)
    plot_scaling_speedup(cuda_scaling, kokkos_scaling, output_dir)
    
    # Print parsed data tables
    print("\n" + "=" * 60)
    print("PARSED DATA TABLES (Copy to README)")
    print("=" * 60)
    
    print("\n" + generate_benchmark1_tables(cuda_data, kokkos_data))
    print("\n" + generate_scaling_table(cuda_scaling, kokkos_scaling))
    print("\n" + generate_command_reference())
    
    print("\n" + "=" * 60)
    print(f"Figures saved to: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()

