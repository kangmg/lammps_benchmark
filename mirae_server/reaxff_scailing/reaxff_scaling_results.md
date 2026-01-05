# ReaxFF Replicate Scaling Benchmark

## Test Configuration
- **System**: HNS (Hexanitrostilbene) energetic crystal
- **Potential**: ReaxFF with charge equilibration (QEq)
- **Timesteps**: 100
- **Base unit cell**: 304 atoms

- **Date**: Sun Jan  4 22:24:06 KST 2026

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
| conda-mpi48-omp1 | 132.323 | 8208 | 0.756 |
| conda-mpi24-omp2 | 74.643 | 8208 | 1.340 |
| conda-mpi12-omp4 | 41.7178 | 8208 | 2.397 |
| conda-mpi6-omp8 | 23.8461 | 8208 | 4.194 |
| conda-mpi1-omp48 | 13.2164 | 8208 | 7.566 |
| opt-mpi48-omp1 | 6.09123 | 8208 | 16.417 |
| opt-mpi24-omp2 | 4.89595 | 8208 | 20.425 |
| opt-mpi12-omp4 | 4.23156 | 8208 | 23.632 |
| opt-mpi6-omp8 | 3.81953 | 8208 | 26.181 |
| opt-mpi1-omp48 | 9.11659 | 8208 | 10.969 |

### Replicate 4x4x4

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| conda-mpi48-omp1 | 299.518 | 19456 | 0.334 |
| conda-mpi24-omp2 | 165.271 | 19456 | 0.605 |
| conda-mpi12-omp4 | 91.2448 | 19456 | 1.096 |
| conda-mpi6-omp8 | 53.1851 | 19456 | 1.880 |
| conda-mpi1-omp48 | 29.8562 | 19456 | 3.349 |
| opt-mpi48-omp1 | 10.9497 | 19456 | 9.133 |
| opt-mpi24-omp2 | 9.20041 | 19456 | 10.869 |
| opt-mpi12-omp4 | 8.40461 | 19456 | 11.898 |
| opt-mpi6-omp8 | 7.80615 | 19456 | 12.810 |
| opt-mpi1-omp48 | 17.5619 | 19456 | 5.694 |

### Replicate 5x5x5

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| conda-mpi48-omp1 | 594.437 | 38000 | 0.168 |
| conda-mpi24-omp2 | 309.25 | 38000 | 0.323 |
| conda-mpi12-omp4 | 168.673 | 38000 | 0.593 |
| conda-mpi6-omp8 | 97.9638 | 38000 | 1.021 |
| conda-mpi1-omp48 | 52.9455 | 38000 | 1.889 |
| opt-mpi48-omp1 | 17.5914 | 38000 | 5.685 |
| opt-mpi24-omp2 | 15.4599 | 38000 | 6.468 |
| opt-mpi12-omp4 | 14.4863 | 38000 | 6.903 |
| opt-mpi6-omp8 | 13.7873 | 38000 | 7.253 |
| opt-mpi1-omp48 | 30.3861 | 38000 | 3.291 |

### Replicate 6x6x6

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| conda-mpi48-omp1 | 984.351 | 65664 | 0.102 |
| conda-mpi24-omp2 | 524.796 | 65664 | 0.191 |
| conda-mpi12-omp4 | 288.016 | 65664 | 0.347 |
| conda-mpi6-omp8 | 161.896 | 65664 | 0.618 |
| conda-mpi1-omp48 | 79.0715 | 65664 | 1.265 |
| opt-mpi48-omp1 | 27.6277 | 65664 | 3.620 |
| opt-mpi24-omp2 | 25.2685 | 65664 | 3.958 |
| opt-mpi12-omp4 | 24.0994 | 65664 | 4.149 |
| opt-mpi6-omp8 | 23.2139 | 65664 | 4.308 |
| opt-mpi1-omp48 | 50.0703 | 65664 | 1.997 |

## Speedup Analysis (vs 48 MPI × 1 OMP)

Baseline = 48 MPI × 1 OMP (pure MPI)

Speedup = Baseline time / Config time (>1 means faster than baseline)

### lmp_mpi_conda Speedup

| Replicate | Atoms | Baseline (s) | Config | Time (s) | Speedup |
|-----------|-------|--------------|--------|----------|---------|
| 3x3x3 | 8208 | 132.323 | conda-mpi48-omp1 | 132.323 | 1.00x |
| 3x3x3 | 8208 | 132.323 | conda-mpi24-omp2 | 74.643 | 1.77x |
| 3x3x3 | 8208 | 132.323 | conda-mpi12-omp4 | 41.7178 | 3.17x |
| 3x3x3 | 8208 | 132.323 | conda-mpi6-omp8 | 23.8461 | 5.54x |
| 3x3x3 | 8208 | 132.323 | conda-mpi1-omp48 | 13.2164 | 10.01x |
| 4x4x4 | 19456 | 299.518 | conda-mpi48-omp1 | 299.518 | 1.00x |
| 4x4x4 | 19456 | 299.518 | conda-mpi24-omp2 | 165.271 | 1.81x |
| 4x4x4 | 19456 | 299.518 | conda-mpi12-omp4 | 91.2448 | 3.28x |
| 4x4x4 | 19456 | 299.518 | conda-mpi6-omp8 | 53.1851 | 5.63x |
| 4x4x4 | 19456 | 299.518 | conda-mpi1-omp48 | 29.8562 | 10.03x |
| 5x5x5 | 38000 | 594.437 | conda-mpi48-omp1 | 594.437 | 1.00x |
| 5x5x5 | 38000 | 594.437 | conda-mpi24-omp2 | 309.25 | 1.92x |
| 5x5x5 | 38000 | 594.437 | conda-mpi12-omp4 | 168.673 | 3.52x |
| 5x5x5 | 38000 | 594.437 | conda-mpi6-omp8 | 97.9638 | 6.06x |
| 5x5x5 | 38000 | 594.437 | conda-mpi1-omp48 | 52.9455 | 11.22x |
| 6x6x6 | 65664 | 984.351 | conda-mpi48-omp1 | 984.351 | 1.00x |
| 6x6x6 | 65664 | 984.351 | conda-mpi24-omp2 | 524.796 | 1.87x |
| 6x6x6 | 65664 | 984.351 | conda-mpi12-omp4 | 288.016 | 3.41x |
| 6x6x6 | 65664 | 984.351 | conda-mpi6-omp8 | 161.896 | 6.08x |
| 6x6x6 | 65664 | 984.351 | conda-mpi1-omp48 | 79.0715 | 12.44x |

### lmp (optimized) Speedup

| Replicate | Atoms | Baseline (s) | Config | Time (s) | Speedup |
|-----------|-------|--------------|--------|----------|---------|
| 3x3x3 | 8208 | 6.09123 | opt-mpi48-omp1 | 6.09123 | 1.00x |
| 3x3x3 | 8208 | 6.09123 | opt-mpi24-omp2 | 4.89595 | 1.24x |
| 3x3x3 | 8208 | 6.09123 | opt-mpi12-omp4 | 4.23156 | 1.43x |
| 3x3x3 | 8208 | 6.09123 | opt-mpi6-omp8 | 3.81953 | 1.59x |
| 3x3x3 | 8208 | 6.09123 | opt-mpi1-omp48 | 9.11659 | .66x |
| 4x4x4 | 19456 | 10.9497 | opt-mpi48-omp1 | 10.9497 | 1.00x |
| 4x4x4 | 19456 | 10.9497 | opt-mpi24-omp2 | 9.20041 | 1.19x |
| 4x4x4 | 19456 | 10.9497 | opt-mpi12-omp4 | 8.40461 | 1.30x |
| 4x4x4 | 19456 | 10.9497 | opt-mpi6-omp8 | 7.80615 | 1.40x |
| 4x4x4 | 19456 | 10.9497 | opt-mpi1-omp48 | 17.5619 | .62x |
| 5x5x5 | 38000 | 17.5914 | opt-mpi48-omp1 | 17.5914 | 1.00x |
| 5x5x5 | 38000 | 17.5914 | opt-mpi24-omp2 | 15.4599 | 1.13x |
| 5x5x5 | 38000 | 17.5914 | opt-mpi12-omp4 | 14.4863 | 1.21x |
| 5x5x5 | 38000 | 17.5914 | opt-mpi6-omp8 | 13.7873 | 1.27x |
| 5x5x5 | 38000 | 17.5914 | opt-mpi1-omp48 | 30.3861 | .57x |
| 6x6x6 | 65664 | 27.6277 | opt-mpi48-omp1 | 27.6277 | 1.00x |
| 6x6x6 | 65664 | 27.6277 | opt-mpi24-omp2 | 25.2685 | 1.09x |
| 6x6x6 | 65664 | 27.6277 | opt-mpi12-omp4 | 24.0994 | 1.14x |
| 6x6x6 | 65664 | 27.6277 | opt-mpi6-omp8 | 23.2139 | 1.19x |
| 6x6x6 | 65664 | 27.6277 | opt-mpi1-omp48 | 50.0703 | .55x |

## Binary Comparison: conda vs optimized (48 MPI × 1 OMP)

Speedup = conda time / optimized time (>1 means optimized is faster)

| Replicate | Atoms | conda (s) | optimized (s) | Speedup |
|-----------|-------|-----------|---------------|---------|
| 3x3x3 | 8208 | 132.323 | 6.09123 | 21.72x |
| 4x4x4 | 19456 | 299.518 | 10.9497 | 27.35x |
| 5x5x5 | 38000 | 594.437 | 17.5914 | 33.79x |
| 6x6x6 | 65664 | 984.351 | 27.6277 | 35.62x |

