# LAMMPS 벤치마크 - 미래 서버

[![English](https://img.shields.io/badge/lang-English-red.svg)](summary.md)

48코어 HPC 서버에서의 CPU 전용 MPI/OpenMP 하이브리드 병렬화 벤치마크.

---

## 목적

48코어 CPU 전용 시스템에서 다양한 MPI × OpenMP 구성을 사용하여 **conda LAMMPS** (`lmp_mpi_conda`) vs **최적화 LAMMPS** (`lmp`) 바이너리 성능 비교.

---

## 테스트 환경

### 하드웨어
| 구성요소 | 사양 |
|---------|------|
| **CPU** | Intel Xeon Gold 6342 @ 2.80GHz |
| **코어** | 48 |
| **노드** | n06 |
| **GPU** | 없음 (CPU 전용) |

### 소프트웨어

| 바이너리 | 설명 |
|----------|------|
| `lmp_mpi_conda` | Conda 설치 LAMMPS (기본 빌드) |
| `lmp` | 커스텀 최적화 빌드 ([빌드 스크립트](build_lammps.sh)) |

#### 최적화 빌드 구성

`lmp` 바이너리는 Intel oneAPI 2022와 Ice Lake 최적화로 빌드:

```
컴파일러: Intel icpx (oneAPI 2022)
최적화: -O3 -xCORE-AVX512 -fp-model fast=2
FFT: Intel MKL
패키지: most.cmake 프리셋
병렬화: MPI + OpenMP
```

### 병렬화 구성

모든 구성은 총 48개 스레드 사용 (MPI 랭크 × OpenMP 스레드):

| 구성 | MPI | OMP | 명령어 패턴 |
|------|-----|-----|-------------|
| 48×1 | 48 | 1 | `mpirun -np 48 lmp -sf omp -pk omp 1` |
| 24×2 | 24 | 2 | `mpirun -np 24 lmp -sf omp -pk omp 2` |
| 12×4 | 12 | 4 | `mpirun -np 12 lmp -sf omp -pk omp 4` |
| 6×8 | 6 | 8 | `mpirun -np 6 lmp -sf omp -pk omp 8` |
| 1×48 | 1 | 48 | `lmp -sf omp -pk omp 48` |

---

## 주요 결과

### 벤치마크 1: 공식 LAMMPS + ReaxFF

![Benchmark 1 Speedup](figures/benchmark1_speedup.png)

#### 벤치마크별 최적 구성

| 벤치마크 | 최적 conda | 속도향상 | 최적 opt | 속도향상 | opt vs conda |
|----------|------------|----------|----------|----------|--------------|
| **LJ** | 1×48 | 11.6x | 48×1 | 60.8x | **5.6배 빠름** |
| **EAM** | 1×48 | 17.9x | 48×1 | 159.7x | **9.7배 빠름** |
| **CHAIN** | 6×8 | 3.0x | 48×1 | 31.8x | **12.6배 빠름** |
| **RHODO** | 1×48 | 18.1x | 48×1 | 40.8x | **2.5배 빠름** |
| **REAXFF** | 1×48 | 9.9x | 6×8 | 33.1x | **4.0배 빠름** |

#### 관찰 결과

1. **최적화 바이너리가 훨씬 빠름** (2.5x ~ 12.6x) - 모든 벤치마크에서
2. **conda는 OpenMP 선호** (1×48 또는 6×8 최적)
3. **opt는 MPI 선호** (대부분 48×1 최적, ReaxFF는 6×8)

### 벤치마크 2: ReaxFF 스케일링

![Benchmark 2 Scaling](figures/benchmark2_scaling.png)

#### 시스템 크기별 스케일링 (최적 구성)

| 시스템 | 원자 수 | conda 1×48 (s) | opt 6×8 (s) | opt 속도향상 |
|--------|---------|----------------|-------------|--------------|
| 3×3×3 | 8,208 | 13.22 | 3.82 | **3.5배** |
| 4×4×4 | 19,456 | 29.86 | 7.81 | **3.8배** |
| 5×5×5 | 38,000 | 52.95 | 13.79 | **3.8배** |
| 6×6×6 | 65,664 | 79.07 | 23.21 | **3.4배** |

---

## 결론

1. **항상 최적화 바이너리 사용** (`lmp`) - conda보다 2.5x ~ 11x 빠름
2. **최적화 바이너리**: 단순 포텐셜은 **고 MPI** (48×1), ReaxFF는 **하이브리드 6×8**
3. **conda 바이너리**: **고 OpenMP** (1×48)가 최적
4. **ReaxFF**: 최적 구성은 최적화 바이너리 + **6 MPI × 8 OMP**

---

## 레포지토리 구조

```
mirae_server/
├── summary.md              # 이 파일
├── figures/                # 생성된 플롯
├── scripts/
│   └── analyze_benchmarks.py
├── official+reaxff/        # 공식 벤치마크 결과
└── reaxff_scailing/        # ReaxFF 스케일링 결과
```

---

## 참고 자료

- [LAMMPS 공식 벤치마크](https://www.lammps.org/bench.html)
- [LAMMPS OpenMP 패키지](https://docs.lammps.org/Speed_omp.html)
- [LAMMPS 성능 팁](https://docs.lammps.org/Speed.html)
