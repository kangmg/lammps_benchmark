# LAMMPS 벤치마크

[![English](https://img.shields.io/badge/lang-English-red.svg)](README.md)

LAMMPS 분자동역학 시뮬레이션을 위한 GPU & MPI 가속 벤치마크

---

## 목적

이 레포지토리는 LAMMPS 시뮬레이션의 **병렬화 및 GPU 가속 설정을 평가**하기 위한 벤치마크 결과를 포함합니다. 주요 초점은 **ReaxFF** 반응성 포텐셜 성능입니다.

주요 목표:
- CPU 전용 vs GPU 가속 성능 비교
- CUDA GPU 패키지 vs KOKKOS GPU 가속 비교
- 시스템 크기 증가에 따른 스케일링 분석
- ReaxFF 시뮬레이션을 위한 최적 설정 도출

---

## 벤치마크 시스템

### 1. 공식 LAMMPS 벤치마크
[LAMMPS 벤치마크 페이지](https://www.lammps.org/bench.html)의 표준 벤치마크 문제들:

| 벤치마크 | 설명 |
|---------|------|
| **LJ (Lennard-Jones)** | Lennard-Jones 포텐셜을 사용한 원자 유체 |
| **Chain (Polymer)** | 100-mer 체인의 비드-스프링 폴리머 용융체 |
| **EAM (Metal)** | EAM 포텐셜을 사용한 금속 고체 |
| **Chute (Granular)** | 과립 슈트 흐름 |
| **Rhodo (Protein)** | 용매화된 지질 이중층 내 로돕신 단백질 |

### 2. ReaxFF VOH 시스템 (주요 관심사)
ReaxFF 반응성 포텐셜을 사용한 [바나듐 산화물 수산화물 (VOH) 시스템](https://github.com/ovilab/atomify-lammps-examples/tree/master/examples/reaxff/VOH)

> **참고**: ReaxFF는 계산 비용이 높으며, 주요 병목은 보통 **QEq (전하 평형화)** 계산에서 발생합니다. KOKKOS 가속은 이 작업 부하에서 상당한 개선을 보여줍니다.

> **참고**: KOKKOS 패키지의 일부 pair 스타일들 (예: `snap`, `mliap`, `reaxff`)은 GPU와 CPU에 대해 광범위한 최적화 및 특수화가 이루어져 있습니다. ([ref](https://docs.lammps.org/Speed_compare.html))

---

## 테스트 환경

### 하드웨어
| 구성요소 | 사양 |
|---------|------|
| **CPU** | Intel Core i9-12900 |
| **GPU** | NVIDIA RTX 3080 |
| **OS** | Windows (Docker Ubuntu 컨테이너) |

### 소프트웨어 / Docker 이미지

| 소프트웨어 | 버전 |
|-----------|------|
| **LAMMPS** | 29 Aug 2024 - Update 3 |

두 가지 GPU 가속 전략을 비교하기 위해 두 개의 Docker 이미지를 사용했습니다:

| 이미지 | 설명 | Dockerfile |
|--------|------|------------|
| **GPU (CUDA)** | GPU 패키지를 사용한 LAMMPS (CUDA 가속) | [Dockerfile](https://github.com/kangmg/environment_archive/blob/main/maximal_lammps_gpu_env/Dockerfile) |
| **KOKKOS-GPU** | KOKKOS 패키지를 사용한 LAMMPS (CUDA 백엔드) | [Dockerfile](https://github.com/kangmg/environment_archive/blob/main/maximal_lammps_gpu_kokkos_env/Dockerfile) |

---

## 수행된 벤치마크

### 벤치마크 1: 공식 LAMMPS + ReaxFF 성능 비교
다양한 가속 방법에 따른 실행 시간 비교:
- CPU 전용 (직렬)
- MPI 병렬화를 사용한 CPU
- GPU 패키지 (CUDA)
- KOKKOS-GPU (CUDA 백엔드)

### 벤치마크 2: ReaxFF 스케일링 테스트
replica 확장을 통한 ReaxFF VOH 시스템의 시스템 크기 스케일링 테스트:

| Replica | 원자 수 (약) |
|---------|-------------|
| 3×3×3 | ~8,000 |
| 4×4×4 | ~19,000 |
| 5×5×5 | ~38,000 |
| 6×6×6 | ~65,000 |

이 테스트는 시스템 크기가 증가함에 따라 GPU 가속의 이점이 어떻게 스케일링되는지 평가합니다.

---

## 결과

모든 속도 향상은 **CPU-1 Serial** (단일 코어, GPU 없음) 기준으로 계산됩니다.

### 실행 그룹

| 그룹 | 설명 | 실행 파일 |
|------|------|-----------|
| **lmp_gpu (MPI)** | MPI 병렬화를 사용한 CPU 전용 | `lmp_gpu` |
| **lmp_gpu (CUDA)** | CUDA GPU 패키지를 통한 GPU 가속 | `lmp_gpu -sf gpu -pk gpu 1` |
| **lmp_kokkos (MPI)** | MPI 병렬화를 사용한 CPU 전용 | `lmp_kokkos` |
| **lmp_kokkos (KOKKOS)** | KOKKOS (CUDA 백엔드)를 통한 GPU 가속 | `lmp_kokkos -k on g 1 -sf kk` |

### 벤치마크 1: 공식 LAMMPS + ReaxFF

![Benchmark 1 Speedup](figures/benchmark1_speedup.png)

#### 주요 관찰 결과 (벤치마크 데이터에서 파싱)

| 벤치마크 | 최고 CPU (MPI) | 최고 CUDA GPU | 최고 KOKKOS GPU | 권장 |
|----------|----------------|---------------|-----------------|------|
| **LJ** | CPU-12 (5.30x) | CUDA-1 (14.22x) | KOKKOS-1 (14.18x) | CUDA/KOKKOS |
| **EAM** | CPU-12 (5.38x) | CUDA-1 (28.33x) | KOKKOS-1 (10.22x) | CUDA |
| **CHAIN** | CPU-12 (6.54x) | CUDA-MPI4 (3.74x) | KOKKOS-1 (6.03x) | CPU 또는 KOKKOS |
| **RHODO** | CPU-12 (6.11x) | CUDA-MPI4 (19.77x) | KOKKOS-1 (3.96x) | CUDA |
| **REAXFF** | CPU-12 (3.02x) | CUDA-1 (0.99x) | KOKKOS-1 (3.26x) | **KOKKOS 필수** ⚠️ |

> ⚠️ **ReaxFF 중요**: CUDA GPU 패키지는 **가속 효과 없음** (0.99x), KOKKOS는 3.26x 속도 향상 제공. GPU 최적화된 QEq 구현 때문.

### 벤치마크 2: ReaxFF 스케일링

![Benchmark 2 Scaling](figures/benchmark2_scaling.png)

#### 시스템 크기별 GPU 속도 향상 (벤치마크 데이터에서 파싱)

| 시스템 크기 | 원자 수 | CPU-1 (s) | CUDA GPU-1 (s) | CUDA 속도향상 | KOKKOS GPU-1 (s) | KOKKOS 속도향상 |
|-------------|---------|-----------|----------------|---------------|------------------|-----------------|
| 3×3×3 | 8,208 | 34.13 | 34.56 | 0.99x | 4.03 | **8.47x** |
| 4×4×4 | 19,456 | 77.21 | 77.30 | 1.00x | 6.74 | **11.46x** |
| 5×5×5 | 38,000 | 147.69 | 147.42 | 1.00x | 9.05 | **16.31x** |
| 6×6×6 | 65,664 | 251.10 | 248.23 | 1.01x | 13.39 | **18.75x** |

> 📈 **핵심 발견**: KOKKOS GPU 가속은 **시스템 크기에 따라 스케일링**됩니다. 큰 시스템일수록 GPU 가속 효과가 큽니다 (8.5x → 18.8x).

### 결론

1. **단순 포텐셜 (LJ, EAM)**: CUDA GPU 패키지가 최고 성능
2. **ReaxFF 시뮬레이션**: **KOKKOS 필수** - CUDA GPU 패키지는 효과 없음 (0.99x)
3. **ReaxFF 스케일링**: 큰 시스템일수록 더 나은 GPU 속도 향상 (8.5x → 18.8x)
4. **ReaxFF 최적 설정**: 단일 MPI 랭크 + 1 GPU (KOKKOS)

---

## 레포지토리 구조

```
lammps_benchmark/
├── README.md / README_ko.md     # 문서
├── figures/                     # 생성된 플롯
│   ├── benchmark1_speedup.png
│   └── benchmark2_scaling.png
├── scripts/
│   └── analyze_benchmarks.py    # 분석 스크립트
├── lammps_cuda_image/           # CUDA 이미지 결과
└── lammps_kokkos_image/         # KOKKOS 이미지 결과
```

---

## 명령어 참조

| 그룹 | 별칭 | 명령어 |
|------|------|--------|
| lmp_gpu (MPI) | CPU-1 | `lmp_gpu -in <input>` |
| lmp_gpu (MPI) | CPU-4 | `mpirun -np 4 lmp_gpu -in <input>` |
| lmp_gpu (MPI) | CPU-8 | `mpirun -np 8 lmp_gpu -in <input>` |
| lmp_gpu (MPI) | CPU-12 | `mpirun -np 12 lmp_gpu -in <input>` |
| lmp_gpu (CUDA) | CUDA-1 | `lmp_gpu -sf gpu -pk gpu 1 -in <input>` |
| lmp_gpu (CUDA) | CUDA-MPI4 | `mpirun -np 4 lmp_gpu -sf gpu -pk gpu 1 -in <input>` |
| lmp_gpu (CUDA) | CUDA-MPI12 | `mpirun -np 12 lmp_gpu -sf gpu -pk gpu 1 -in <input>` |
| lmp_kokkos (MPI) | CPU-1 | `lmp_kokkos -in <input>` |
| lmp_kokkos (MPI) | CPU-4 | `mpirun -np 4 lmp_kokkos -in <input>` |
| lmp_kokkos (MPI) | CPU-8 | `mpirun -np 8 lmp_kokkos -in <input>` |
| lmp_kokkos (MPI) | CPU-12 | `mpirun -np 12 lmp_kokkos -in <input>` |
| lmp_kokkos (KOKKOS) | KOKKOS-1 | `mpirun -np 1 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input>` |
| lmp_kokkos (KOKKOS) | KOKKOS-MPI8 | `mpirun -np 8 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input>` |
| lmp_kokkos (KOKKOS) | KOKKOS-MPI12 | `mpirun -np 12 lmp_kokkos -k on g 1 -sf kk -pk kokkos neigh half newton on -in <input>` |

---

## 참고 자료

- [LAMMPS 공식 벤치마크](https://www.lammps.org/bench.html)
- [ReaxFF VOH 예제](https://github.com/ovilab/atomify-lammps-examples/tree/master/examples/reaxff/VOH)
- [LAMMPS GPU 패키지 문서](https://docs.lammps.org/Speed_gpu.html)
- [LAMMPS KOKKOS 패키지 문서](https://docs.lammps.org/Speed_kokkos.html)

