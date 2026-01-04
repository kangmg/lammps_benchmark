#!/bin/bash

################################################################################
# ReaxFF Replicate Scaling Benchmark
# Tests ReaxFF performance with different system sizes (3x3x3 to 6x6x6)
################################################################################

echo "==========================================="
echo "ReaxFF Replicate Scaling Benchmark"
echo "==========================================="
echo "Date: $(date)"
echo ""

# Configuration
BENCH_DIR="lammps_benchmarks"
RESULT_FILE="reaxff_scaling_results.md"
LAMMPS_REAXFF_URL="https://raw.githubusercontent.com/lammps/lammps/stable/examples/reaxff/HNS"

# Base atoms in unit cell (304 atoms)
BASE_ATOMS=304

# Replicate sizes to test
REPLICATES=("3 3 3" "4 4 4" "5 5 5" "6 6 6")
REPLICATE_NAMES=("3x3x3" "4x4x4" "5x5x5" "6x6x6")

# Benchmark configurations
# Format: "name|command"
declare -a BENCHMARK_CONFIGS=(
    "CPU-1|lmp_gpu -in"
    "CPU-4|mpirun -np 4 lmp_gpu -in"
    "CPU-8|mpirun -np 8 lmp_gpu -in"
    "CPU-12|mpirun -np 12 lmp_gpu -in"
    "GPU-1|lmp_gpu -sf gpu -pk gpu 1 -in"
    "GPU-MPI4|mpirun -np 4 lmp_gpu -sf gpu -pk gpu 1 -in"
)

# Download ReaxFF files
download_files() {
    echo "Downloading ReaxFF HNS files..."
    mkdir -p "$BENCH_DIR"
    
    if ! pushd "$BENCH_DIR" > /dev/null 2>&1; then
        echo "Error: Cannot change to $BENCH_DIR"
        exit 1
    fi
    
    local files=("data.hns-equil" "ffield.reax.hns")
    for file in "${files[@]}"; do
        echo -n "  $file ... "
        if [ -f "$file" ]; then
            echo "✓ (exists)"
        elif wget -q "${LAMMPS_REAXFF_URL}/${file}" -O "$file" 2>/dev/null; then
            echo "✓"
        else
            echo "✗ (failed)"
            popd > /dev/null 2>&1
            exit 1
        fi
    done
    
    popd > /dev/null 2>&1
    echo ""
}

# Create input file for specific replicate
create_input_file() {
    local rep=$1  # e.g., "3 3 3"
    local name=$2 # e.g., "3x3x3"
    
    cat > "$BENCH_DIR/in.reaxff_${name}" << EOF
# ReaxFF HNS Benchmark - Replicate ${name}
units             real
atom_style        charge
atom_modify       sort 100 0.0
dimension         3
boundary          p p p

read_data         data.hns-equil
replicate         ${rep} bbox

pair_style        reaxff NULL
pair_coeff        * * ffield.reax.hns C H O N

compute           reax all pair reaxff

neighbor          1.0 bin
neigh_modify      every 20 delay 0 check no

timestep          0.1

thermo_style      custom step temp pe press evdwl ecoul vol
thermo_modify     norm yes
thermo            10

velocity          all create 300.0 41279 loop geom

fix               1 all nve
fix               2 all qeq/reax 1 0.0 10.0 1e-6 reaxff

run               100
EOF
}

# Extract metrics from log
extract_metrics() {
    local logfile=$1
    
    if [ ! -f "$logfile" ]; then
        echo "ERROR"
        return
    fi
    
    if ! grep -q "Loop time of" "$logfile"; then
        echo "ERROR"
        return
    fi
    
    local loop_line=$(grep "Loop time of" "$logfile" | head -1)
    local loop_time=$(echo "$loop_line" | awk '{print $4}')
    local atoms=$(echo "$loop_line" | awk '{for(i=1;i<=NF;i++) if($i=="atoms") print $(i-1)}')
    
    local perf_line=$(grep "Performance:" "$logfile" | head -1)
    local timesteps_sec="-"
    if [ -n "$perf_line" ]; then
        timesteps_sec=$(echo "$perf_line" | awk -F'[, ]+' '{for(i=1;i<=NF;i++) if($i~/timesteps/) print $(i-1)}')
    fi
    
    echo "${loop_time}|${atoms}|${timesteps_sec}"
}

# Run single benchmark
run_benchmark() {
    local rep_name=$1
    local config_name=$2
    local command=$3
    local input_file="in.reaxff_${rep_name}"
    
    local logfile="log.reaxff_${rep_name}_${config_name}"
    
    echo -n "  $config_name ... "
    
    if ! pushd "$BENCH_DIR" > /dev/null 2>&1; then
        echo "✗ (dir error)"
        return
    fi
    
    local exit_code=0
    $command $input_file -log "../$logfile" > /dev/null 2>&1 || exit_code=$?
    
    popd > /dev/null 2>&1
    
    if [ $exit_code -ne 0 ]; then
        echo "✗ (exit: $exit_code)"
        echo "${rep_name}|${config_name}|-|-|-" >> .scaling_data.tmp
        return
    fi
    
    local metrics=$(extract_metrics "$logfile")
    if [ "$metrics" = "ERROR" ]; then
        echo "✗ (parse error)"
        echo "${rep_name}|${config_name}|-|-|-" >> .scaling_data.tmp
        return
    fi
    
    IFS='|' read -r loop_time atoms ts_sec <<< "$metrics"
    echo "✓ (${loop_time}s, ${atoms} atoms)"
    echo "${rep_name}|${config_name}|${loop_time}|${atoms}|${ts_sec}" >> .scaling_data.tmp
}

# Initialize markdown
init_markdown() {
    cat > "$RESULT_FILE" << 'EOF'
# ReaxFF Replicate Scaling Benchmark

## Test Configuration
- **System**: HNS (Hexanitrostilbene) energetic crystal
- **Potential**: ReaxFF with charge equilibration (QEq)
- **Timesteps**: 100
- **Base unit cell**: 304 atoms

EOF
    echo "- **Date**: $(date)" >> "$RESULT_FILE"
    echo "" >> "$RESULT_FILE"
    
    echo "## System Sizes" >> "$RESULT_FILE"
    echo "" >> "$RESULT_FILE"
    echo "| Replicate | Calculation | Atoms |" >> "$RESULT_FILE"
    echo "|-----------|-------------|-------|" >> "$RESULT_FILE"
    for i in "${!REPLICATES[@]}"; do
        local rep="${REPLICATES[$i]}"
        local name="${REPLICATE_NAMES[$i]}"
        # Calculate atoms
        IFS=' ' read -r x y z <<< "$rep"
        local atoms=$((BASE_ATOMS * x * y * z))
        echo "| $name | 304 × $x × $y × $z | $atoms |" >> "$RESULT_FILE"
    done
    echo "" >> "$RESULT_FILE"
}

# Generate results
generate_results() {
    echo "## Performance Results" >> "$RESULT_FILE"
    echo "" >> "$RESULT_FILE"
    
    for rep_name in "${REPLICATE_NAMES[@]}"; do
        if grep -q "^${rep_name}|" .scaling_data.tmp 2>/dev/null; then
            echo "### Replicate ${rep_name}" >> "$RESULT_FILE"
            echo "" >> "$RESULT_FILE"
            echo "| Config | Loop Time (s) | Atoms | Timesteps/s |" >> "$RESULT_FILE"
            echo "|--------|---------------|-------|-------------|" >> "$RESULT_FILE"
            
            grep "^${rep_name}|" .scaling_data.tmp | while IFS='|' read -r rn cfg loop atoms ts; do
                echo "| $cfg | $loop | $atoms | $ts |" >> "$RESULT_FILE"
            done
            echo "" >> "$RESULT_FILE"
        fi
    done
    
    # GPU vs CPU comparison
    echo "## GPU Speedup Analysis" >> "$RESULT_FILE"
    echo "" >> "$RESULT_FILE"
    echo "| Replicate | Atoms | CPU-1 (s) | GPU-1 (s) | Speedup |" >> "$RESULT_FILE"
    echo "|-----------|-------|-----------|-----------|---------|" >> "$RESULT_FILE"
    
    for rep_name in "${REPLICATE_NAMES[@]}"; do
        local cpu1=$(grep "^${rep_name}|CPU-1|" .scaling_data.tmp 2>/dev/null | cut -d'|' -f3)
        local gpu1=$(grep "^${rep_name}|GPU-1|" .scaling_data.tmp 2>/dev/null | cut -d'|' -f3)
        local atoms=$(grep "^${rep_name}|CPU-1|" .scaling_data.tmp 2>/dev/null | cut -d'|' -f4)
        
        if [ -n "$cpu1" ] && [ -n "$gpu1" ] && [ "$cpu1" != "-" ] && [ "$gpu1" != "-" ]; then
            local speedup=$(echo "scale=2; $cpu1 / $gpu1" | bc 2>/dev/null || echo "-")
            echo "| $rep_name | $atoms | $cpu1 | $gpu1 | ${speedup}x |" >> "$RESULT_FILE"
        else
            echo "| $rep_name | ${atoms:-?} | ${cpu1:--} | ${gpu1:--} | - |" >> "$RESULT_FILE"
        fi
    done
    echo "" >> "$RESULT_FILE"
}

# Main
main() {
    download_files
    
    # Create input files for each replicate
    echo "Creating input files..."
    for i in "${!REPLICATES[@]}"; do
        create_input_file "${REPLICATES[$i]}" "${REPLICATE_NAMES[$i]}"
        echo "  in.reaxff_${REPLICATE_NAMES[$i]} ✓"
    done
    echo ""
    
    # Initialize
    rm -f .scaling_data.tmp
    init_markdown
    
    # Run benchmarks
    echo "==========================================="
    echo "Running Benchmarks"
    echo "==========================================="
    echo ""
    
    for i in "${!REPLICATES[@]}"; do
        local rep_name="${REPLICATE_NAMES[$i]}"
        IFS=' ' read -r x y z <<< "${REPLICATES[$i]}"
        local atoms=$((BASE_ATOMS * x * y * z))
        
        echo "=== Replicate $rep_name ($atoms atoms) ==="
        
        for config in "${BENCHMARK_CONFIGS[@]}"; do
            IFS='|' read -r cfg_name command <<< "$config"
            run_benchmark "$rep_name" "$cfg_name" "$command"
        done
        echo ""
    done
    
    # Generate report
    generate_results
    
    # Cleanup
    rm -f .scaling_data.tmp
    
    echo "==========================================="
    echo "✓ Results saved to: $RESULT_FILE"
    echo "==========================================="
}

main
