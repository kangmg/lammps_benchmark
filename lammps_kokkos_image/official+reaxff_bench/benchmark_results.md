# LAMMPS Benchmark Results

## System Information

- **Date**: Sun Jan  4 04:03:57 UTC 2026
- **Hostname**: d5d8d63e09f8
- **OS**: Linux 6.6.87.2-microsoft-standard-WSL2
- **Architecture**: x86_64
- **CPU**: 12th Gen Intel(R) Core(TM) i9-12900
- **CPU Cores**: 24

## Benchmark Configurations

1. **CPU-1**: `lmp_kokkos -in <input_file>`
2. **CPU-4**: `mpirun -np 4 lmp_kokkos -in <input_file>`
3. **CPU-8**: `mpirun -np 8 lmp_kokkos -in <input_file>`
4. **CPU-12**: `mpirun -np 12 lmp_kokkos -in <input_file>`
5. **KOKKOS-GPU-MPI1**: `mpirun -np 1 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input_file>`
6. **KOKKOS-GPU-MPI8**: `mpirun -np 8 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input_file>`
7. **KOKKOS-GPU-MPI12**: `mpirun -np 12 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input_file>`

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
| CPU-1 | 0.81978 | 121.984 | - | - | 3903488 | 32000 |
| CPU-4 | 0.226154 | 442.176 | - | - | 14149632 | 32000 |
| CPU-8 | 0.18084 | 552.974 | - | - | 17695168 | 32000 |
| CPU-12 | 0.15362 | 650.956 | - | - | 20830592 | 32000 |
| KOKKOS-GPU-MPI1 | 0.05741 | 1741.857 | - | - | 55739424 | 32000 |
| KOKKOS-GPU-MPI8 | 0.369951 | 270.306 | - | - | 8649792 | 32000 |
| KOKKOS-GPU-MPI12 | 0.537119 | 186.178 | - | - | 5957696 | 32000 |

### EAM Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 2.24527 | 44.538 | 19.240 | 1.247 | 1425216 | 32000 |
| CPU-4 | 0.629438 | 158.872 | 68.633 | 0.350 | 5083904 | 32000 |
| CPU-8 | 0.496782 | 201.296 | 86.960 | 0.276 | 6441472 | 32000 |
| CPU-12 | 0.4193 | 238.493 | 103.029 | 0.233 | 7631776 | 32000 |
| KOKKOS-GPU-MPI1 | 0.221557 | 451.350 | 194.983 | 0.123 | 14443200 | 32000 |
| KOKKOS-GPU-MPI8 | 0.838448 | 119.268 | 51.524 | 0.466 | 3816576 | 32000 |
| KOKKOS-GPU-MPI12 | 1.22667 | 81.522 | 35.217 | 0.681 | 2608704 | 32000 |

### CHAIN Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 0.523404 | 191.057 | - | - | 6113824 | 32000 |
| CPU-4 | 0.147159 | 679.538 | - | - | 21745216 | 32000 |
| CPU-8 | 0.112884 | 885.865 | - | - | 28347680 | 32000 |
| CPU-12 | 0.0820852 | 1218.246 | - | - | 38983872 | 32000 |
| KOKKOS-GPU-MPI1 | 0.0874262 | 1143.823 | - | - | 36602336 | 32000 |
| KOKKOS-GPU-MPI8 | 0.89348 | 111.922 | - | - | 3581504 | 32000 |
| KOKKOS-GPU-MPI12 | 1.32452 | 75.499 | - | - | 2415968 | 32000 |

### RHODO Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 12.6335 | 7.915 | 1.368 | 17.546 | 253280 | 32000 |
| CPU-4 | 3.49573 | 28.606 | 4.943 | 4.855 | 915392 | 32000 |
| CPU-8 | 2.51279 | 39.796 | 6.877 | 3.490 | 1273472 | 32000 |
| CPU-12 | 2.01696 | 49.579 | 8.567 | 2.801 | 1586528 | 32000 |
| KOKKOS-GPU-MPI1 | 3.1979 | 31.271 | 5.404 | 4.442 | 1000672 | 32000 |
| KOKKOS-GPU-MPI8 | 20.6257 | 4.848 | 0.838 | 28.647 | 155136 | 32000 |
| KOKKOS-GPU-MPI12 | 35.0444 | 2.854 | 0.493 | 48.673 | 91328 | 32000 |

### REAXFF Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| CPU-1 | 11.3389 | 8.819 | 0.076 | 314.970 | 21447 | 2432 |
| CPU-4 | 4.55899 | 21.935 | 0.190 | 126.638 | 53345 | 2432 |
| CPU-8 | 3.7858 | 26.414 | 0.228 | 105.161 | 64238 | 2432 |
| CPU-12 | 3.59125 | 27.845 | 0.241 | 99.757 | 67719 | 2432 |
| KOKKOS-GPU-MPI1 | 3.51019 | 28.489 | 0.246 | 97.505 | 69285 | 2432 |
| KOKKOS-GPU-MPI8 | 21.6973 | 4.609 | 0.040 | 602.703 | 11209 | 2432 |
| KOKKOS-GPU-MPI12 | 32.7795 | 3.051 | 0.026 | 910.542 | 7420 | 2432 |

## Speedup Analysis

Speedup is calculated relative to the first configuration for each benchmark.

### LJ Speedup

Baseline: CPU-1 (0.81978 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 0.81978 | 1.00x |
| CPU-4 | 0.226154 | 3.62x |
| CPU-8 | 0.18084 | 4.53x |
| CPU-12 | 0.15362 | 5.33x |
| KOKKOS-GPU-MPI1 | 0.05741 | 14.27x |
| KOKKOS-GPU-MPI8 | 0.369951 | 2.21x |
| KOKKOS-GPU-MPI12 | 0.537119 | 1.52x |

### EAM Speedup

Baseline: CPU-1 (2.24527 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 2.24527 | 1.00x |
| CPU-4 | 0.629438 | 3.56x |
| CPU-8 | 0.496782 | 4.51x |
| CPU-12 | 0.4193 | 5.35x |
| KOKKOS-GPU-MPI1 | 0.221557 | 10.13x |
| KOKKOS-GPU-MPI8 | 0.838448 | 2.67x |
| KOKKOS-GPU-MPI12 | 1.22667 | 1.83x |

### CHAIN Speedup

Baseline: CPU-1 (0.523404 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 0.523404 | 1.00x |
| CPU-4 | 0.147159 | 3.55x |
| CPU-8 | 0.112884 | 4.63x |
| CPU-12 | 0.0820852 | 6.37x |
| KOKKOS-GPU-MPI1 | 0.0874262 | 5.98x |
| KOKKOS-GPU-MPI8 | 0.89348 | .58x |
| KOKKOS-GPU-MPI12 | 1.32452 | .39x |

### RHODO Speedup

Baseline: CPU-1 (12.6335 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 12.6335 | 1.00x |
| CPU-4 | 3.49573 | 3.61x |
| CPU-8 | 2.51279 | 5.02x |
| CPU-12 | 2.01696 | 6.26x |
| KOKKOS-GPU-MPI1 | 3.1979 | 3.95x |
| KOKKOS-GPU-MPI8 | 20.6257 | .61x |
| KOKKOS-GPU-MPI12 | 35.0444 | .36x |

### REAXFF Speedup

Baseline: CPU-1 (11.3389 seconds)

| Configuration | Time (s) | Speedup |
|---------------|----------|---------|
| CPU-1 | 11.3389 | 1.00x |
| CPU-4 | 4.55899 | 2.48x |
| CPU-8 | 3.7858 | 2.99x |
| CPU-12 | 3.59125 | 3.15x |
| KOKKOS-GPU-MPI1 | 3.51019 | 3.23x |
| KOKKOS-GPU-MPI8 | 21.6973 | .52x |
| KOKKOS-GPU-MPI12 | 32.7795 | .34x |

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

