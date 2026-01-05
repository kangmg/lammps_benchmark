# LAMMPS Benchmark Results

## System Information

- **Date**: Sun Jan  4 21:40:54 KST 2026
- **Hostname**: n06
- **OS**: Linux 3.10.0-1160.el7.x86_64
- **Architecture**: x86_64
- **CPU**: Intel(R) Xeon(R) Gold 6342 CPU @ 2.80GHz
- **CPU Cores**: 48

## Benchmark Configurations

1. **conda-serial**: `1|lmp_mpi_conda -in <input_file>`
2. **opt-serial**: `1|lmp -in <input_file>`
3. **conda-mpi48-omp1**: `1|mpirun -np 48 lmp_mpi_conda -sf omp -pk omp 1 -in <input_file>`
4. **conda-mpi24-omp2**: `2|mpirun -np 24 lmp_mpi_conda -sf omp -pk omp 2 -in <input_file>`
5. **conda-mpi12-omp4**: `4|mpirun -np 12 lmp_mpi_conda -sf omp -pk omp 4 -in <input_file>`
6. **conda-mpi6-omp8**: `8|mpirun -np 6 lmp_mpi_conda -sf omp -pk omp 8 -in <input_file>`
7. **conda-mpi1-omp48**: `48|lmp_mpi_conda -sf omp -pk omp 48 -in <input_file>`
8. **opt-mpi48-omp1**: `1|mpirun -np 48 lmp -sf omp -pk omp 1 -in <input_file>`
9. **opt-mpi24-omp2**: `2|mpirun -np 24 lmp -sf omp -pk omp 2 -in <input_file>`
10. **opt-mpi12-omp4**: `4|mpirun -np 12 lmp -sf omp -pk omp 4 -in <input_file>`
11. **opt-mpi6-omp8**: `8|mpirun -np 6 lmp -sf omp -pk omp 8 -in <input_file>`
12. **opt-mpi1-omp48**: `48|lmp -sf omp -pk omp 48 -in <input_file>`

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
| conda-serial | 1.65599 | 60.387 | - | - | 1932384 | 32000 |
| opt-serial | 1.56518 | 63.890 | - | - | 2044480 | 32000 |
| conda-mpi48-omp1 | 1.60651 | 62.247 | - | - | 1991904 | 32000 |
| conda-mpi24-omp2 | 0.791097 | 126.407 | - | - | 4045024 | 32000 |
| conda-mpi12-omp4 | 0.415072 | 240.922 | - | - | 7709504 | 32000 |
| conda-mpi6-omp8 | 0.229382 | 435.954 | - | - | 13950528 | 32000 |
| conda-mpi1-omp48 | 0.142949 | 699.549 | - | - | 22385568 | 32000 |
| opt-mpi48-omp1 | 0.0362516 | 2758.498 | - | - | 88271936 | 32000 |
| opt-mpi24-omp2 | 0.0373826 | 2675.042 | - | - | 85601344 | 32000 |
| opt-mpi12-omp4 | 0.0408348 | 2448.894 | - | - | 78364608 | 32000 |
| opt-mpi6-omp8 | 0.0514631 | 1943.142 | - | - | 62180544 | 32000 |
| opt-mpi1-omp48 | 0.184945 | 540.700 | - | - | 17302400 | 32000 |

### EAM Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| conda-serial | 4.49448 | 22.250 | 9.612 | 2.497 | 712000 | 32000 |
| opt-serial | 4.10767 | 24.345 | 10.517 | 2.282 | 779040 | 32000 |
| conda-mpi48-omp1 | 4.34943 | 22.992 | 9.932 | 2.416 | 735744 | 32000 |
| conda-mpi24-omp2 | 2.18279 | 45.813 | 19.791 | 1.213 | 1466016 | 32000 |
| conda-mpi12-omp4 | 1.13353 | 88.220 | 38.111 | 0.630 | 2823040 | 32000 |
| conda-mpi6-omp8 | 0.605186 | 165.238 | 71.383 | 0.336 | 5287616 | 32000 |
| conda-mpi1-omp48 | 0.250703 | 398.879 | 172.316 | 0.139 | 12764128 | 32000 |
| opt-mpi48-omp1 | 0.0980264 | 1020.133 | 440.698 | 0.054 | 32644256 | 32000 |
| opt-mpi24-omp2 | 0.0996395 | 1003.618 | 433.563 | 0.055 | 32115776 | 32000 |
| opt-mpi12-omp4 | 0.104293 | 958.841 | 414.219 | 0.058 | 30682912 | 32000 |
| opt-mpi6-omp8 | 0.120302 | 831.242 | 359.096 | 0.067 | 26599744 | 32000 |
| opt-mpi1-omp48 | 0.374767 | 266.833 | 115.272 | 0.208 | 8538656 | 32000 |

### CHAIN Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| conda-serial | 0.956817 | 104.513 | - | - | 3344416 | 32000 |
| opt-serial | 0.818799 | 122.130 | - | - | 3908160 | 32000 |
| conda-mpi48-omp1 | 0.9485 | 105.430 | - | - | 3373760 | 32000 |
| conda-mpi24-omp2 | 0.608408 | 164.363 | - | - | 5259616 | 32000 |
| conda-mpi12-omp4 | 0.417158 | 239.718 | - | - | 7670976 | 32000 |
| conda-mpi6-omp8 | 0.323554 | 309.067 | - | - | 9890144 | 32000 |
| conda-mpi1-omp48 | 0.338546 | 295.380 | - | - | 9452160 | 32000 |
| opt-mpi48-omp1 | 0.025724 | 3887.424 | - | - | 124397568 | 32000 |
| opt-mpi24-omp2 | 0.0283725 | 3524.535 | - | - | 112785120 | 32000 |
| opt-mpi12-omp4 | 0.0343989 | 2907.068 | - | - | 93026176 | 32000 |
| opt-mpi6-omp8 | 0.048115 | 2078.354 | - | - | 66507328 | 32000 |
| opt-mpi1-omp48 | 0.289328 | 345.629 | - | - | 11060128 | 32000 |

### RHODO Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| conda-serial | 26.6546 | 3.752 | 0.648 | 37.020 | 120064 | 32000 |
| opt-serial | 23.7221 | 4.215 | 0.728 | 32.947 | 134880 | 32000 |
| conda-mpi48-omp1 | 25.0996 | 3.984 | 0.688 | 34.861 | 127488 | 32000 |
| conda-mpi24-omp2 | 12.8106 | 7.806 | 1.349 | 17.792 | 249792 | 32000 |
| conda-mpi12-omp4 | 6.67915 | 14.972 | 2.587 | 9.277 | 479104 | 32000 |
| conda-mpi6-omp8 | 3.73168 | 26.798 | 4.631 | 5.183 | 857536 | 32000 |
| conda-mpi1-omp48 | 1.47647 | 67.729 | 11.704 | 2.051 | 2167328 | 32000 |
| opt-mpi48-omp1 | 0.581423 | 171.992 | 29.720 | 0.808 | 5503744 | 32000 |
| opt-mpi24-omp2 | 0.605127 | 165.255 | 28.556 | 0.840 | 5288160 | 32000 |
| opt-mpi12-omp4 | 0.627175 | 159.445 | 27.552 | 0.871 | 5102240 | 32000 |
| opt-mpi6-omp8 | 0.706416 | 141.560 | 24.461 | 0.981 | 4529920 | 32000 |
| opt-mpi1-omp48 | 1.49698 | 66.801 | 11.543 | 2.079 | 2137632 | 32000 |

### REAXFF Benchmark

| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |
|---------------|---------------|---------------|--------|----------|----------------|-------|
| conda-serial | 544.277 | 0.184 | 0.002 | 15118.812 | 6992 | 38000 |
| opt-serial | 456.179 | 0.219 | 0.002 | 12671.628 | 8322 | 38000 |
| conda-mpi48-omp1 | 580.38 | 0.172 | 0.001 | 16121.672 | 6536 | 38000 |
| conda-mpi24-omp2 | 310.783 | 0.322 | 0.003 | 8632.859 | 12236 | 38000 |
| conda-mpi12-omp4 | 168.589 | 0.593 | 0.005 | 4683.031 | 22534 | 38000 |
| conda-mpi6-omp8 | 97.8064 | 1.022 | 0.009 | 2716.843 | 38836 | 38000 |
| conda-mpi1-omp48 | 54.8882 | 1.822 | 0.016 | 1524.672 | 69236 | 38000 |
| opt-mpi48-omp1 | 17.6005 | 5.682 | 0.049 | 488.901 | 215916 | 38000 |
| opt-mpi24-omp2 | 15.4268 | 6.482 | 0.056 | 428.523 | 246316 | 38000 |
| opt-mpi12-omp4 | 14.5025 | 6.895 | 0.060 | 402.846 | 262010 | 38000 |
| opt-mpi6-omp8 | 13.7808 | 7.256 | 0.063 | 382.800 | 275728 | 38000 |
| opt-mpi1-omp48 | 30.4082 | 3.289 | 0.028 | 844.673 | 124982 | 38000 |

## Speedup Analysis

Speedup is calculated relative to serial (single-core) execution for each binary.
Speedup = Serial time / Parallel time (higher is better)

### LJ Speedup

| Binary | Serial (s) | Configuration | Time (s) | Speedup |
|--------|------------|---------------|----------|---------|
| conda | 1.65599 | conda-serial | 1.65599 | 1.00x |
| conda | 1.65599 | conda-mpi48-omp1 | 1.60651 | 1.03x |
| conda | 1.65599 | conda-mpi24-omp2 | 0.791097 | 2.09x |
| conda | 1.65599 | conda-mpi12-omp4 | 0.415072 | 3.98x |
| conda | 1.65599 | conda-mpi6-omp8 | 0.229382 | 7.21x |
| conda | 1.65599 | conda-mpi1-omp48 | 0.142949 | 11.58x |
| opt | 1.56518 | opt-serial | 1.56518 | 1.00x |
| opt | 1.56518 | opt-mpi48-omp1 | 0.0362516 | 43.17x |
| opt | 1.56518 | opt-mpi24-omp2 | 0.0373826 | 41.86x |
| opt | 1.56518 | opt-mpi12-omp4 | 0.0408348 | 38.32x |
| opt | 1.56518 | opt-mpi6-omp8 | 0.0514631 | 30.41x |
| opt | 1.56518 | opt-mpi1-omp48 | 0.184945 | 8.46x |

### EAM Speedup

| Binary | Serial (s) | Configuration | Time (s) | Speedup |
|--------|------------|---------------|----------|---------|
| conda | 4.49448 | conda-serial | 4.49448 | 1.00x |
| conda | 4.49448 | conda-mpi48-omp1 | 4.34943 | 1.03x |
| conda | 4.49448 | conda-mpi24-omp2 | 2.18279 | 2.05x |
| conda | 4.49448 | conda-mpi12-omp4 | 1.13353 | 3.96x |
| conda | 4.49448 | conda-mpi6-omp8 | 0.605186 | 7.42x |
| conda | 4.49448 | conda-mpi1-omp48 | 0.250703 | 17.92x |
| opt | 4.10767 | opt-serial | 4.10767 | 1.00x |
| opt | 4.10767 | opt-mpi48-omp1 | 0.0980264 | 41.90x |
| opt | 4.10767 | opt-mpi24-omp2 | 0.0996395 | 41.22x |
| opt | 4.10767 | opt-mpi12-omp4 | 0.104293 | 39.38x |
| opt | 4.10767 | opt-mpi6-omp8 | 0.120302 | 34.14x |
| opt | 4.10767 | opt-mpi1-omp48 | 0.374767 | 10.96x |

### CHAIN Speedup

| Binary | Serial (s) | Configuration | Time (s) | Speedup |
|--------|------------|---------------|----------|---------|
| conda | 0.956817 | conda-serial | 0.956817 | 1.00x |
| conda | 0.956817 | conda-mpi48-omp1 | 0.9485 | 1.00x |
| conda | 0.956817 | conda-mpi24-omp2 | 0.608408 | 1.57x |
| conda | 0.956817 | conda-mpi12-omp4 | 0.417158 | 2.29x |
| conda | 0.956817 | conda-mpi6-omp8 | 0.323554 | 2.95x |
| conda | 0.956817 | conda-mpi1-omp48 | 0.338546 | 2.82x |
| opt | 0.818799 | opt-serial | 0.818799 | 1.00x |
| opt | 0.818799 | opt-mpi48-omp1 | 0.025724 | 31.83x |
| opt | 0.818799 | opt-mpi24-omp2 | 0.0283725 | 28.85x |
| opt | 0.818799 | opt-mpi12-omp4 | 0.0343989 | 23.80x |
| opt | 0.818799 | opt-mpi6-omp8 | 0.048115 | 17.01x |
| opt | 0.818799 | opt-mpi1-omp48 | 0.289328 | 2.83x |

### RHODO Speedup

| Binary | Serial (s) | Configuration | Time (s) | Speedup |
|--------|------------|---------------|----------|---------|
| conda | 26.6546 | conda-serial | 26.6546 | 1.00x |
| conda | 26.6546 | conda-mpi48-omp1 | 25.0996 | 1.06x |
| conda | 26.6546 | conda-mpi24-omp2 | 12.8106 | 2.08x |
| conda | 26.6546 | conda-mpi12-omp4 | 6.67915 | 3.99x |
| conda | 26.6546 | conda-mpi6-omp8 | 3.73168 | 7.14x |
| conda | 26.6546 | conda-mpi1-omp48 | 1.47647 | 18.05x |
| opt | 23.7221 | opt-serial | 23.7221 | 1.00x |
| opt | 23.7221 | opt-mpi48-omp1 | 0.581423 | 40.80x |
| opt | 23.7221 | opt-mpi24-omp2 | 0.605127 | 39.20x |
| opt | 23.7221 | opt-mpi12-omp4 | 0.627175 | 37.82x |
| opt | 23.7221 | opt-mpi6-omp8 | 0.706416 | 33.58x |
| opt | 23.7221 | opt-mpi1-omp48 | 1.49698 | 15.84x |

### REAXFF Speedup

| Binary | Serial (s) | Configuration | Time (s) | Speedup |
|--------|------------|---------------|----------|---------|
| conda | 544.277 | conda-serial | 544.277 | 1.00x |
| conda | 544.277 | conda-mpi48-omp1 | 580.38 | .93x |
| conda | 544.277 | conda-mpi24-omp2 | 310.783 | 1.75x |
| conda | 544.277 | conda-mpi12-omp4 | 168.589 | 3.22x |
| conda | 544.277 | conda-mpi6-omp8 | 97.8064 | 5.56x |
| conda | 544.277 | conda-mpi1-omp48 | 54.8882 | 9.91x |
| opt | 456.179 | opt-serial | 456.179 | 1.00x |
| opt | 456.179 | opt-mpi48-omp1 | 17.6005 | 25.91x |
| opt | 456.179 | opt-mpi24-omp2 | 15.4268 | 29.57x |
| opt | 456.179 | opt-mpi12-omp4 | 14.5025 | 31.45x |
| opt | 456.179 | opt-mpi6-omp8 | 13.7808 | 33.10x |
| opt | 456.179 | opt-mpi1-omp48 | 30.4082 | 15.00x |

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
- **Typical atoms**: ~38,000 (5x5x5 replicate)
- **Use Case**: Reactive MD simulations, bond breaking/forming

---

## Reference

- **Official LAMMPS benchmarks**: https://www.lammps.org/bench.html
- **LAMMPS documentation**: https://docs.lammps.org
- **Benchmark source**: https://github.com/lammps/lammps/tree/stable/bench

