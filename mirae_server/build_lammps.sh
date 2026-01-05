#!/bin/bash
#
# LAMMPS 2025 Build Script
# Intel oneAPI 2022 + Ice Lake optimization + most packages
#

set -e

# Download and extract LAMMPS
PROGRAMS_DIR="$HOME/programs"
LAMMPS_VERSION="stable_22Jul2025_update2"
LAMMPS_TARBALL="lammps-src-22Jul2025_update2.tar.gz"
LAMMPS_URL="https://github.com/lammps/lammps/releases/download/${LAMMPS_VERSION}/${LAMMPS_TARBALL}"

mkdir -p ${PROGRAMS_DIR}
cd ${PROGRAMS_DIR}

if [ ! -f "${LAMMPS_TARBALL}" ]; then
    echo "Downloading LAMMPS ${LAMMPS_VERSION}..."
    wget ${LAMMPS_URL}
fi

if [ ! -d "lammps-22Jul2025" ]; then
    echo "Extracting LAMMPS..."
    tar -xzf ${LAMMPS_TARBALL}
fi

# Load modules
module purge
module load gcc/11.3.0
module load intel/2022.2/compiler/2022.1.0
module load intel/2022.2/mkl/2022.1.0
module load intel/2022.2/tbb/2021.6.0
module load intel/2022.2/mpi/2021.6.0

# Force Intel MPI to use LLVM-based compilers
export I_MPI_CC=icx
export I_MPI_CXX=icpx
export I_MPI_FC=ifx
export I_MPI_F90=ifx
export I_MPI_F77=ifx

# Set directories
LAMMPS_SRC="$HOME/programs/lammps-22Jul2025"
INSTALL_DIR="$HOME/local"

# Create install directory
mkdir -p ${INSTALL_DIR}

# Check source exists
if [ ! -d "${LAMMPS_SRC}" ]; then
    echo "ERROR: LAMMPS source not found at ${LAMMPS_SRC}"
    exit 1
fi

cd ${LAMMPS_SRC}

# Prepare build directory
rm -rf build
mkdir build
cd build

# Configure with CMake (oneAPI + most packages + Ice Lake optimization)
cmake \
  -C ../cmake/presets/oneapi.cmake \
  -C ../cmake/presets/most.cmake \
  -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_COMPILER=icpx \
  -DCMAKE_C_COMPILER=icx \
  -DCMAKE_Fortran_COMPILER=ifx \
  -DMPI_CXX_COMPILER=mpiicpc \
  -DMPI_C_COMPILER=mpiicc \
  -DMPI_Fortran_COMPILER=mpiifort \
  -DCMAKE_CXX_STANDARD=17 \
  -DCMAKE_CXX_FLAGS_RELEASE="-O3 -xCORE-AVX512 -qopenmp -fp-model fast=2 -DNDEBUG" \
  -DCMAKE_C_FLAGS_RELEASE="-O3 -xCORE-AVX512 -qopenmp -fp-model fast=2 -DNDEBUG" \
  -DCMAKE_Fortran_FLAGS_RELEASE="-O3 -xCORE-AVX512 -qopenmp -fp-model fast=2 -DNDEBUG" \
  -DFFT=MKL \
  -DPKG_COLVARS=no \
  -DPKG_MACHDYN=no \
  -DPKG_EXTRA-FIX=no \
  -DFFT_SINGLE=yes \
  -DBUILD_MPI=yes \
  -DBUILD_OMP=yes \
  -DBUILD_TOOLS=yes \
  ../cmake

[ $? -ne 0 ] && echo "ERROR: CMake failed" && exit 1

# Build (using 4 cores)
make -j 4 2>&1 | tee build.log

[ $? -ne 0 ] && echo "ERROR: Build failed" && exit 1

# Install
make install

[ ! -f ${INSTALL_DIR}/bin/lmp ] && echo "ERROR: Installation failed" && exit 1

# Cleanup
echo "Cleaning up..."
cd ${PROGRAMS_DIR}
rm -rf ${LAMMPS_SRC}/build
rm -f ${LAMMPS_TARBALL}

# Save build info
BUILD_INFO="${INSTALL_DIR}/build_info.txt"
cat > ${BUILD_INFO} << EOF
LAMMPS Build Information
========================
Build Date: $(date)
Version: 22Jul2025
Hostname: $(hostname)
Preset: oneapi.cmake + most.cmake
Optimization: -O3 -xCORE-AVX512 -fp-model fast=2
FFT: Intel MKL
Parallel: MPI + OpenMP
Build Log: ${LAMMPS_SRC}/build/build.log
EOF

echo "Build completed successfully!"
echo "Executable: ${INSTALL_DIR}/bin/lmp"
echo "Build info: ${BUILD_INFO}"