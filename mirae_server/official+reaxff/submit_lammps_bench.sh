#!/bin/bash
#$ -q all.q
#$ -pe mpi_48 48
#$ -N official_bench
#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -l hostname=n06

echo "=========================================="
echo "LAMMPS Official Benchmark - Node: $(hostname)"
echo "Date: $(date)"
echo "Slots: $NSLOTS"
echo "=========================================="

module load gcc/11.3.0

cd $SGE_O_WORKDIR

./lammps_bench.sh \
  -c "conda-serial|1|lmp_mpi_conda -in" \
  -c "opt-serial|1|lmp -in" \
  -c "conda-mpi48-omp1|1|mpirun -np 48 lmp_mpi_conda -sf omp -pk omp 1 -in" \
  -c "conda-mpi24-omp2|2|mpirun -np 24 lmp_mpi_conda -sf omp -pk omp 2 -in" \
  -c "conda-mpi12-omp4|4|mpirun -np 12 lmp_mpi_conda -sf omp -pk omp 4 -in" \
  -c "conda-mpi6-omp8|8|mpirun -np 6 lmp_mpi_conda -sf omp -pk omp 8 -in" \
  -c "conda-mpi1-omp48|48|lmp_mpi_conda -sf omp -pk omp 48 -in" \
  -c "opt-mpi48-omp1|1|mpirun -np 48 lmp -sf omp -pk omp 1 -in" \
  -c "opt-mpi24-omp2|2|mpirun -np 24 lmp -sf omp -pk omp 2 -in" \
  -c "opt-mpi12-omp4|4|mpirun -np 12 lmp -sf omp -pk omp 4 -in" \
  -c "opt-mpi6-omp8|8|mpirun -np 6 lmp -sf omp -pk omp 8 -in" \
  -c "opt-mpi1-omp48|48|lmp -sf omp -pk omp 48 -in"

echo "=========================================="
echo "Completed: $(date)"
echo "=========================================="

