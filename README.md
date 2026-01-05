# LAMMPS Benchmark

GPU & CPU parallelization benchmark for LAMMPS molecular dynamics simulations.

---

## Benchmark Environments

| Environment | Hardware | Acceleration |
|-------------|----------|--------------|
| **Local Desktop** | i9-12900 (24 cores) + RTX 3080 | GPU (CUDA/KOKKOS) |
| **Mirae Server** | Xeon Gold 6342 (48 cores) | CPU (MPI+OpenMP) |

---

## Official Benchmarks (32,000 atoms each)

> Note: REAXFF excluded - different system sizes (Local: 2,432 / Server: 38,000 atoms)

### Local Desktop - CUDA Image

| Config | LJ (s) | EAM (s) | CHAIN (s) | RHODO (s) |
|--------|--------|---------|-----------|-----------|
| CPU-1 | 0.814 | 2.264 | 0.527 | 12.658 |
| CPU-4 | 0.229 | 0.611 | 0.145 | 3.427 |
| CPU-8 | 0.193 | 0.527 | 0.103 | 2.456 |
| CPU-12 | 0.152 | 0.420 | 0.081 | 2.072 |
| GPU-1 | **0.057** | **0.080** | 0.187 | 0.863 |
| GPU-MPI4 | 0.077 | 0.143 | 0.141 | **0.640** |
| GPU-MPI12 | 0.185 | 0.349 | 0.286 | 1.098 |

### Local Desktop - KOKKOS Image

| Config | LJ (s) | EAM (s) | CHAIN (s) | RHODO (s) |
|--------|--------|---------|-----------|-----------|
| CPU-1 | 0.820 | 2.245 | 0.523 | 12.634 |
| CPU-4 | 0.226 | 0.629 | 0.147 | 3.496 |
| CPU-8 | 0.181 | 0.497 | 0.113 | 2.513 |
| CPU-12 | 0.154 | 0.419 | 0.082 | 2.017 |
| KOKKOS-1 | **0.057** | 0.222 | **0.087** | 3.198 |
| KOKKOS-MPI8 | 0.370 | 0.838 | 0.893 | 20.626 |
| KOKKOS-MPI12 | 0.537 | 1.227 | 1.325 | 35.044 |

### Mirae Server - conda (lmp_mpi_conda)

| Config | LJ (s) | EAM (s) | CHAIN (s) | RHODO (s) |
|--------|--------|---------|-----------|-----------|
| serial | 1.656 | 4.494 | 0.957 | 26.655 |
| 48×1 | 1.607 | 4.349 | 0.949 | 25.100 |
| 24×2 | 0.791 | 2.183 | 0.608 | 12.811 |
| 12×4 | 0.415 | 1.134 | 0.417 | 6.679 |
| 6×8 | 0.229 | 0.605 | 0.324 | 3.732 |
| 1×48 | 0.143 | 0.251 | 0.339 | 1.476 |

### Mirae Server - opt (lmp)

| Config | LJ (s) | EAM (s) | CHAIN (s) | RHODO (s) |
|--------|--------|---------|-----------|-----------|
| serial | 1.565 | 4.108 | 0.819 | 23.722 |
| 48×1 | **0.036** | **0.098** | **0.026** | **0.581** |
| 24×2 | 0.037 | 0.100 | 0.028 | 0.605 |
| 12×4 | 0.041 | 0.104 | 0.034 | 0.627 |
| 6×8 | 0.051 | 0.120 | 0.048 | 0.706 |
| 1×48 | 0.185 | 0.375 | 0.289 | 1.497 |

---

## ReaxFF Scaling Benchmark (HNS system, 100 timesteps)

### Local Desktop - CUDA Image

| System | Atoms | CPU-1 | CPU-4 | CPU-8 | CPU-12 | GPU-1 | GPU-MPI4 |
|--------|-------|-------|-------|-------|--------|-------|----------|
| 3×3×3 | 8,208 | 34.13 | 11.37 | 8.73 | 8.54 | 34.56 | 11.35 |
| 4×4×4 | 19,456 | 77.21 | 24.65 | 17.32 | 15.31 | 77.30 | 25.04 |
| 5×5×5 | 38,000 | 147.69 | 44.89 | 30.31 | 26.45 | 147.42 | 45.29 |
| 6×6×6 | 65,664 | 251.10 | 76.08 | 49.16 | 42.01 | 248.23 | 75.79 |

### Local Desktop - KOKKOS Image

| System | Atoms | CPU-1 | CPU-4 | CPU-8 | CPU-12 | KOKKOS-1 | KOKKOS-MPI2 |
|--------|-------|-------|-------|-------|--------|----------|-------------|
| 3×3×3 | 8,208 | 34.59 | 11.40 | 8.73 | 8.16 | **4.03** | 6.79 |
| 4×4×4 | 19,456 | 76.12 | 25.28 | 17.78 | 15.49 | **6.74** | 10.24 |
| 5×5×5 | 38,000 | 146.43 | 44.91 | 30.07 | 26.01 | **9.05** | 15.22 |
| 6×6×6 | 65,664 | 246.04 | 74.64 | 48.61 | 43.36 | **13.39** | 20.19 |

> ⚠️ **CUDA GPU has no effect on ReaxFF** (~1.0x). Use **KOKKOS** for GPU acceleration (8.5x-18.8x).

### Mirae Server - conda (lmp_mpi_conda)

| System | Atoms | 48×1 | 24×2 | 12×4 | 6×8 | 1×48 |
|--------|-------|------|------|------|-----|------|
| 3×3×3 | 8,208 | 132.32 | 74.64 | 41.72 | 23.85 | 13.22 |
| 4×4×4 | 19,456 | 299.52 | 165.27 | 91.24 | 53.19 | 29.86 |
| 5×5×5 | 38,000 | 594.44 | 309.25 | 168.67 | 97.96 | 52.95 |
| 6×6×6 | 65,664 | 984.35 | 524.80 | 288.02 | 161.90 | 79.07 |

### Mirae Server - opt (lmp)

| System | Atoms | 48×1 | 24×2 | 12×4 | 6×8 | 1×48 |
|--------|-------|------|------|------|-----|------|
| 3×3×3 | 8,208 | 6.09 | 4.90 | 4.23 | **3.82** | 9.12 |
| 4×4×4 | 19,456 | 10.95 | 9.20 | 8.40 | **7.81** | 17.56 |
| 5×5×5 | 38,000 | 17.59 | 15.46 | 14.49 | **13.79** | 30.39 |
| 6×6×6 | 65,664 | 27.63 | 25.27 | 24.10 | **23.21** | 50.07 |

---

## Key Findings

### Local Desktop (GPU)
- **LJ, EAM**: CUDA GPU best (14-28x speedup)
- **CHAIN**: CPU-12 competitive with GPU
- **RHODO**: CUDA GPU-MPI4 best (20x speedup)
- **ReaxFF**: KOKKOS only (CUDA ineffective), 8.5x-18.8x speedup
- Details: [local_desktop/summary.md](local_desktop/summary.md)

### Mirae Server (CPU)
- **Optimized binary** 2.5x-12.6x faster than conda
- **Simple potentials**: opt 48×1 best
- **ReaxFF**: opt 6×8 best
- Details: [mirae_server/summary.md](mirae_server/summary.md)

---

## References

- [LAMMPS Official Benchmarks](https://www.lammps.org/bench.html)
- [LAMMPS GPU Package](https://docs.lammps.org/Speed_gpu.html)
- [LAMMPS KOKKOS Package](https://docs.lammps.org/Speed_kokkos.html)
- [LAMMPS OpenMP Package](https://docs.lammps.org/Speed_omp.html)
