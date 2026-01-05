#!/bin/bash
#$ -q all.q
#$ -pe mpi_48 48
#$ -N reaxff_scaling
#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -l hostname=n06

echo "=========================================="
echo "ReaxFF Scaling Benchmark - Node: $(hostname)"
echo "Date: $(date)"
echo "Slots: $NSLOTS"
echo "=========================================="

module load gcc/11.3.0

export OMP_NUM_THREADS=1
cd $SGE_O_WORKDIR

./reaxff_scaling_bench.sh

echo "=========================================="
echo "Completed: $(date)"
echo "=========================================="

