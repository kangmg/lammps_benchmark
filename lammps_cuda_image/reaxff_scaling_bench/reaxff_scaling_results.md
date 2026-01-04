# ReaxFF Replicate Scaling Benchmark

## Test Configuration
- **System**: HNS (Hexanitrostilbene) energetic crystal
- **Potential**: ReaxFF with charge equilibration (QEq)
- **Timesteps**: 100
- **Base unit cell**: 304 atoms

- **Date**: Sun Jan  4 03:33:39 UTC 2026

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
| CPU-1 | 34.1324 | 8208 | 2.930 |
| CPU-4 | 11.367 | 8208 | 8.797 |
| CPU-8 | 8.73075 | 8208 | 11.454 |
| CPU-12 | 8.54005 | 8208 | 11.710 |
| GPU-1 | 34.5569 | 8208 | 2.894 |
| GPU-MPI4 | 11.3535 | 8208 | 8.808 |

### Replicate 4x4x4

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| CPU-1 | 77.2107 | 19456 | 1.295 |
| CPU-4 | 24.6462 | 19456 | 4.057 |
| CPU-8 | 17.3194 | 19456 | 5.774 |
| CPU-12 | 15.3088 | 19456 | 6.532 |
| GPU-1 | 77.2951 | 19456 | 1.294 |
| GPU-MPI4 | 25.0363 | 19456 | 3.994 |

### Replicate 5x5x5

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| CPU-1 | 147.687 | 38000 | 0.677 |
| CPU-4 | 44.889 | 38000 | 2.228 |
| CPU-8 | 30.3053 | 38000 | 3.300 |
| CPU-12 | 26.4494 | 38000 | 3.781 |
| GPU-1 | 147.42 | 38000 | 0.678 |
| GPU-MPI4 | 45.2934 | 38000 | 2.208 |

### Replicate 6x6x6

| Config | Loop Time (s) | Atoms | Timesteps/s |
|--------|---------------|-------|-------------|
| CPU-1 | 251.104 | 65664 | 0.398 |
| CPU-4 | 76.0793 | 65664 | 1.314 |
| CPU-8 | 49.1624 | 65664 | 2.034 |
| CPU-12 | 42.0138 | 65664 | 2.380 |
| GPU-1 | 248.228 | 65664 | 0.403 |
| GPU-MPI4 | 75.7907 | 65664 | 1.319 |

## GPU Speedup Analysis

| Replicate | Atoms | CPU-1 (s) | GPU-1 (s) | Speedup |
|-----------|-------|-----------|-----------|---------|
| 3x3x3 | 8208 | 34.1324 | 34.5569 | .98x |
| 4x4x4 | 19456 | 77.2107 | 77.2951 | .99x |
| 5x5x5 | 38000 | 147.687 | 147.42 | 1.00x |
| 6x6x6 | 65664 | 251.104 | 248.228 | 1.01x |

