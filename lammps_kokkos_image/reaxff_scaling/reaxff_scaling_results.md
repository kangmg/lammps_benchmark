# ReaxFF Replicate Scaling Benchmark

## Test Configuration
- **System**: HNS (Hexanitrostilbene) energetic crystal
- **Potential**: ReaxFF with charge equilibration (QEq)
- **Timesteps**: 100
- **Base unit cell**: 304 atoms

- **Date**: Sun Jan  4 04:12:40 UTC 2026

## System Sizes

| Replicate | Calculation | Atoms |
|-----------|-------------|-------|
| 3x3x3 | 304 × 3 × 3 × 3 | 8208 |
| 4x4x4 | 304 × 4 × 4 × 4 | 19456 |
| 5x5x5 | 304 × 5 × 5 × 5 | 38000 |
| 6x6x6 | 304 × 6 × 6 × 6 | 65664 |

## Performance Results

### Replicate 3x3x3

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| CPU-1 | 34.5919 | 8208 | 2.891 |
| CPU-4 | 11.4032 | 8208 | 8.769 |
| CPU-8 | 8.73163 | 8208 | 11.453 |
| CPU-12 | 8.16476 | 8208 | 12.248 |
| KOKKOS-GPU-MPI1 | 4.03022 | 8208 | 24.813 |
| KOKKOS-GPU-MPI2 | 6.78711 | 8208 | 14.734 |

### Replicate 4x4x4

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| CPU-1 | 76.116 | 19456 | 1.314 |
| CPU-4 | 25.2799 | 19456 | 3.956 |
| CPU-8 | 17.7755 | 19456 | 5.626 |
| CPU-12 | 15.4891 | 19456 | 6.456 |
| KOKKOS-GPU-MPI1 | 6.73786 | 19456 | 14.842 |
| KOKKOS-GPU-MPI2 | 10.2418 | 19456 | 9.764 |

### Replicate 5x5x5

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| CPU-1 | 146.428 | 38000 | 0.683 |
| CPU-4 | 44.9089 | 38000 | 2.227 |
| CPU-8 | 30.0718 | 38000 | 3.325 |
| CPU-12 | 26.0056 | 38000 | 3.845 |
| KOKKOS-GPU-MPI1 | 9.05478 | 38000 | 11.044 |
| KOKKOS-GPU-MPI2 | 15.215 | 38000 | 6.572 |

### Replicate 6x6x6

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| CPU-1 | 246.041 | 65664 | 0.406 |
| CPU-4 | 74.6426 | 65664 | 1.340 |
| CPU-8 | 48.6094 | 65664 | 2.057 |
| CPU-12 | 43.3562 | 65664 | 2.306 |
| KOKKOS-GPU-MPI1 | 13.3894 | 65664 | 7.469 |
| KOKKOS-GPU-MPI2 | 20.1918 | 65664 | 4.953 |

## KOKKOS GPU Speedup Analysis

| Replicate | Atoms | CPU-1 (s) | KOKKOS-GPU-MPI1 (s) | Speedup |
|-----------|-------|-----------|---------------------|---------|
| 3x3x3 | 8208 | 34.5919 | 4.03022 | 8.58x |
| 4x4x4 | 19456 | 76.116 | 6.73786 | 11.29x |
| 5x5x5 | 38000 | 146.428 | 9.05478 | 16.17x |
| 6x6x6 | 65664 | 246.041 | 13.3894 | 18.37x |

