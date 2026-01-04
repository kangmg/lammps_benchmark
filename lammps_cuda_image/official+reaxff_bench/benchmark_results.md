# LAMMPS Benchmark Results

## System Information

- **Date**: Sun Jan  4 03:30:26 UTC 2026
- **Hostname**: 82522b431e63
- **OS**: Linux 6.6.87.2-microsoft-standard-WSL2
- **Architecture**: x86_64
- **CPU**: 12th Gen Intel(R) Core(TM) i9-12900
- **CPU Cores**: 24

## Benchmark Configurations

1. **CPU-1**: `lmp_gpu -in <input_file>`
2. **CPU-4**: `mpirun -np 4 lmp_gpu -in <input_file>`
3. **CPU-8**: `mpirun -np 8 lmp_gpu -in <input_file>`
4. **CPU-12**: `mpirun -np 12 lmp_gpu -in <input_file>`
5. **GPU-1**: `lmp_gpu -sf gpu -pk gpu 1 -in <input_file>`
6. **GPU-MPI4**: `mpirun -np 4 lmp_gpu -sf gpu -pk gpu 1 -in <input_file>`
7. **GPU-MPI12**: `mpirun -np 12 lmp_gpu -sf gpu -pk gpu 1 -in <input_file>`

---

## Performance Results

### Metrics Explanation

- **Loop Time**: Total execution time for benchmark (seconds, **lower is better**)
- **Timesteps/sec**: Rate of timestep calculation (**higher is better**)
- **ns/day**: Nanoseconds of simulation per day of runtime (**higher is better**)
- **hours/ns**: Hours needed to simulate 1 nanosecond (**lower is better**)
- **atom-steps/sec**: Atoms × timesteps per second (**higher is better**)

### LJ Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 0.813897 | 122.866 | - | - | 3931712 | 32000 |
| CPU-4 | 0.229262 | 436.181 | - | - | 13957792 | 32000 |
| CPU-8 | 0.193452 | 516.923 | - | - | 16541536 | 32000 |
| CPU-12 | 0.15162 | 659.543 | - | - | 21105376 | 32000 |
| GPU-1 | 0.0572396 | 1747.041 | - | - | 55905312 | 32000 |
| GPU-MPI4 | 0.0771064 | 1296.909 | - | - | 41501088 | 32000 |
| GPU-MPI12 | 0.185354 | 539.509 | - | - | 17264288 | 32000 |

### EAM Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 2.26361 | 44.177 | 19.085 | 1.258 | 1413664 | 32000 |
| CPU-4 | 0.611481 | 163.537 | 70.648 | 0.340 | 5233184 | 32000 |
| CPU-8 | 0.527477 | 189.582 | 81.899 | 0.293 | 6066624 | 32000 |
| CPU-12 | 0.420497 | 237.814 | 102.736 | 0.234 | 7610048 | 32000 |
| GPU-1 | 0.0798932 | 1251.671 | 540.722 | 0.044 | 40053472 | 32000 |
| GPU-MPI4 | 0.14317 | 698.469 | 301.739 | 0.080 | 22351008 | 32000 |
| GPU-MPI12 | 0.348996 | 286.536 | 123.784 | 0.194 | 9169152 | 32000 |

### CHAIN Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 0.527457 | 189.589 | - | - | 6066848 | 32000 |
| CPU-4 | 0.144875 | 690.250 | - | - | 22088000 | 32000 |
| CPU-8 | 0.102943 | 971.412 | - | - | 31085184 | 32000 |
| CPU-12 | 0.080619 | 1240.402 | - | - | 39692864 | 32000 |
| GPU-1 | 0.186773 | 535.409 | - | - | 17133088 | 32000 |
| GPU-MPI4 | 0.141189 | 708.271 | - | - | 22664672 | 32000 |
| GPU-MPI12 | 0.285788 | 349.910 | - | - | 11197120 | 32000 |

### RHODO Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 12.6577 | 7.900 | 1.365 | 17.580 | 252800 | 32000 |
| CPU-4 | 3.42744 | 29.176 | 5.042 | 4.760 | 933632 | 32000 |
| CPU-8 | 2.45637 | 40.710 | 7.035 | 3.412 | 1302720 | 32000 |
| CPU-12 | 2.07222 | 48.257 | 8.339 | 2.878 | 1544224 | 32000 |
| GPU-1 | 0.862555 | 115.935 | 20.033 | 1.198 | 3709920 | 32000 |
| GPU-MPI4 | 0.640194 | 156.203 | 26.992 | 0.889 | 4998496 | 32000 |
| GPU-MPI12 | 1.09794 | 91.079 | 15.738 | 1.525 | 2914528 | 32000 |

### REAXFF Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 11.4439 | 8.738 | 0.075 | 317.886 | 21250 | 2432 |
| CPU-4 | 4.4569 | 22.437 | 0.194 | 123.803 | 54566 | 2432 |
| CPU-8 | 3.79995 | 26.316 | 0.227 | 105.554 | 64000 | 2432 |
| CPU-12 | 3.79446 | 26.354 | 0.228 | 105.402 | 64092 | 2432 |
| GPU-1 | 11.5593 | 8.651 | 0.075 | 321.091 | 21039 | 2432 |
| GPU-MPI4 | 4.48702 | 22.287 | 0.193 | 124.639 | 54201 | 2432 |
| GPU-MPI12 | 3.98751 | 25.078 | 0.217 | 110.764 | 60989 | 2432 |

## Speedup Analysis

Speedup is calculated relative to the first configuration for each benchmark.

### LJ Speedup

Baseline: CPU-1 (0.813897 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 0.813897 | 1.00x |
| CPU-4 | 0.229262 | 3.55x |
| CPU-8 | 0.193452 | 4.20x |
| CPU-12 | 0.15162 | 5.36x |
| GPU-1 | 0.0572396 | 14.21x |
| GPU-MPI4 | 0.0771064 | 10.55x |
| GPU-MPI12 | 0.185354 | 4.39x |

### EAM Speedup

Baseline: CPU-1 (2.26361 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 2.26361 | 1.00x |
| CPU-4 | 0.611481 | 3.70x |
| CPU-8 | 0.527477 | 4.29x |
| CPU-12 | 0.420497 | 5.38x |
| GPU-1 | 0.0798932 | 28.33x |
| GPU-MPI4 | 0.14317 | 15.81x |
| GPU-MPI12 | 0.348996 | 6.48x |

### CHAIN Speedup

Baseline: CPU-1 (0.527457 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 0.527457 | 1.00x |
| CPU-4 | 0.144875 | 3.64x |
| CPU-8 | 0.102943 | 5.12x |
| CPU-12 | 0.080619 | 6.54x |
| GPU-1 | 0.186773 | 2.82x |
| GPU-MPI4 | 0.141189 | 3.73x |
| GPU-MPI12 | 0.285788 | 1.84x |

### RHODO Speedup

Baseline: CPU-1 (12.6577 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 12.6577 | 1.00x |
| CPU-4 | 3.42744 | 3.69x |
| CPU-8 | 2.45637 | 5.15x |
| CPU-12 | 2.07222 | 6.10x |
| GPU-1 | 0.862555 | 14.67x |
| GPU-MPI4 | 0.640194 | 19.77x |
| GPU-MPI12 | 1.09794 | 11.52x |

### REAXFF Speedup

Baseline: CPU-1 (11.4439 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 11.4439 | 1.00x |
| CPU-4 | 4.4569 | 2.56x |
| CPU-8 | 3.79995 | 3.01x |
| CPU-12 | 3.79446 | 3.01x |
| GPU-1 | 11.5593 | .99x |
| GPU-MPI4 | 4.48702 | 2.55x |
| GPU-MPI12 | 3.98751 | 2.86x |

---

## Benchmark Descriptions

### LJ (Lennard-Jones)
- **System**: Liquid argon-like atomic fluid
- **Potential**: Lennard-Jones with 2.5 cutoff
- **Typical atoms**: ~32,000
- **Use Case**: Most common benchmark, baseline for comparisons

### EAM (Embedded Atom Method)
- **System**: Copper (Cu) metallic solid
- **Potential**: EAM metallic potential
- **Typical atoms**: ~32,000
- **Use Case**: Metal simulations, ~2.6x slower than LJ

### Chain (Polymer)
- **System**: Bead-spring polymer melt (100-mer chains)
- **Potential**: FENE bonds + LJ interactions
- **Typical atoms**: ~32,000
- **Use Case**: Molecular dynamics, ~2x faster than LJ

### Rhodo (Rhodopsin)
- **System**: Rhodopsin protein in solvated lipid bilayer
- **Potential**: CHARMM force field + PPPM long-range
- **Typical atoms**: ~32,000
- **Use Case**: Biomolecular simulations, ~16x slower than LJ

### ReaxFF (Reactive Force Field)
- **System**: HNS (Hexanitrostilbene) energetic crystal
- **Potential**: ReaxFF reactive potential with charge equilibration
- **Typical atoms**: ~6,720 (2x2x2 replicate)
- **Use Case**: Reactive MD simulations, bond breaking/forming

---

## Reference

- **Official LAMMPS benchmarks**: https://www.lammps.org/bench.html
- **LAMMPS documentation**: https://docs.lammps.org
- **Benchmark source**: https://github.com/lammps/lammps/tree/stable/bench

