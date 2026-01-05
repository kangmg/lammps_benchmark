#!/bin/bash

################################################################################
# LAMMPS Benchmark Runner with Custom Execution Commands
# Allows testing different LAMMPS binaries with custom MPI configurations
################################################################################

# Note: set -e removed to allow proper error handling in functions
# Each critical section handles errors explicitly

echo "=========================================="
echo "LAMMPS Custom Benchmark Suite"
echo "=========================================="
echo "Date: $(date)"
echo ""

# Configuration
BENCH_DIR="lammps_benchmarks"
RESULT_FILE="benchmark_results.md"
LAMMPS_BENCH_URL="https://raw.githubusercontent.com/lammps/lammps/stable/bench"

# Benchmark configurations to test
# Format: "name|command"
# Example: "Serial|lmp_serial -in"
#          "MPI-20|mpirun -np 20 lmp_serial -in"
#          "GPU|lmp_gpu -sf gpu -pk gpu 1 -in"
declare -a BENCHMARK_CONFIGS

# Function to show usage
show_usage() {
    cat << 'EOF'
Usage: ./lammps_official_bench.sh [options]

Options:
  -c, --config <command>    Add benchmark configuration
                           Format: "NAME|COMMAND"
                           Example: "conda-1|lmp_mpi_conda -in"
                                   "opt-48|mpirun -np 48 lmp -in"
  -h, --help               Show this help message

Examples:
  # Compare lmp_mpi_conda vs lmp (optimized) on 48-core CPU system
  ./lammps_official_bench.sh \
    -c "conda-1|lmp_mpi_conda -in" \
    -c "conda-12|mpirun -np 12 lmp_mpi_conda -in" \
    -c "conda-24|mpirun -np 24 lmp_mpi_conda -in" \
    -c "conda-48|mpirun -np 48 lmp_mpi_conda -in" \
    -c "opt-1|lmp -in" \
    -c "opt-12|mpirun -np 12 lmp -in" \
    -c "opt-24|mpirun -np 24 lmp -in" \
    -c "opt-48|mpirun -np 48 lmp -in"

Note: The command should end with '-in' as the input file will be appended automatically.
EOF
}

# Parse command line arguments
parse_arguments() {
    if [ $# -eq 0 ]; then
        echo "Error: No benchmark configurations specified"
        echo ""
        show_usage
        exit 1
    fi
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--config)
                BENCHMARK_CONFIGS+=("$2")
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    if [ ${#BENCHMARK_CONFIGS[@]} -eq 0 ]; then
        echo "Error: No benchmark configurations specified"
        echo ""
        show_usage
        exit 1
    fi
}

# Download benchmarks
download_benchmarks() {
    echo "=========================================="
    echo "Downloading LAMMPS Official Benchmarks"
    echo "=========================================="
    echo ""
    
    if ! command -v wget &> /dev/null; then
        echo "Error: wget is required but not found"
        exit 1
    fi
    
    mkdir -p "$BENCH_DIR"
    
    # Use pushd/popd for safe directory handling
    if ! pushd "$BENCH_DIR" > /dev/null 2>&1; then
        echo "Error: Cannot change to directory $BENCH_DIR"
        exit 1
    fi
    
    # Benchmark files to download
    local files=(
        "in.lj"
        "in.chain"
        "in.eam"
        "in.rhodo"
        "Cu_u3.eam"
        "data.chain"
        "data.rhodo"
    )
    
    # ReaxFF files from examples directory (different URL)
    local reaxff_files=(
        "in.reaxff.hns"
        "data.hns-equil"
        "ffield.reax.hns"
    )
    local LAMMPS_REAXFF_URL="https://raw.githubusercontent.com/lammps/lammps/stable/examples/reaxff/HNS"
    
    echo "Downloading benchmark files..."
    local downloaded=0
    
    for file in "${files[@]}"; do
        echo -n "  $file ... "
        if wget -q "${LAMMPS_BENCH_URL}/${file}" -O "$file" 2>/dev/null; then
            echo "✓"
            ((downloaded++)) || true  # Prevent exit on arithmetic
        else
            echo "✗ (skipped)"
        fi
    done
    
    # Download ReaxFF files from examples directory
    echo ""
    echo "Downloading ReaxFF benchmark files..."
    for file in "${reaxff_files[@]}"; do
        echo -n "  $file ... "
        if wget -q "${LAMMPS_REAXFF_URL}/${file}" -O "$file" 2>/dev/null; then
            echo "✓"
            ((downloaded++)) || true
        else
            echo "✗ (skipped)"
        fi
    done
    
    # Create ReaxFF benchmark input file (optimized for benchmarking)
    if [ -f "data.hns-equil" ] && [ -f "ffield.reax.hns" ]; then
        cat > "in.reaxff" << 'REAXFF_EOF'
# ReaxFF HNS Benchmark for LAMMPS
# Based on official LAMMPS examples/reaxff/HNS
# 5x5x5 replicate (~38,000 atoms), 100 timesteps

units             real
atom_style        charge
atom_modify       sort 100 0.0
dimension         3
boundary          p p p

read_data         data.hns-equil
replicate         5 5 5 bbox

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
REAXFF_EOF
        echo ""
        echo "✓ Created in.reaxff benchmark file"
    fi
    
    popd > /dev/null 2>&1
    
    echo ""
    echo "✓ Downloaded $downloaded files"
    echo ""
}

# Extract performance metrics from LAMMPS log
extract_metrics() {
    local logfile=$1
    
    # Check if log file exists and has content
    if [ ! -f "$logfile" ]; then
        echo "ERROR=Log file not found"
        return
    fi
    
    # Check for successful completion
    if ! grep -q "Loop time of" "$logfile"; then
        echo "ERROR=No timing data found"
        return
    fi
    
    # Extract loop time info
    # Format: "Loop time of 0.178921 on 1 procs for 100 steps with 32000 atoms"
    #          $1   $2   $3    $4      $5 $6  $7    $8  $9   $10   $11   $12   $13
    local loop_line=$(grep "Loop time of" "$logfile" | head -1)
    local loop_time=$(echo "$loop_line" | awk '{print $4}')
    local timesteps=$(echo "$loop_line" | awk '{for(i=1;i<=NF;i++) if($i=="steps") print $(i-1)}')
    local atoms=$(echo "$loop_line" | awk '{for(i=1;i<=NF;i++) if($i=="atoms") print $(i-1)}')
    
    # Extract performance metrics
    # Format: "Performance: 558.985 tau/day, 64.7437 timesteps/s, 2.072 Matom-step/s"
    # OR:     "Performance: 64.7437 timesteps/s, 2.072 Matom-step/s" (without tau/day)
    local perf_line=$(grep "Performance:" "$logfile" | head -1)
    
    if [ -n "$perf_line" ]; then
        # Extract timesteps/s by finding the field before "timesteps/s"
        local timestep_per_sec=$(echo "$perf_line" | awk -F'[, ]+' '{for(i=1;i<=NF;i++) if($i~/timesteps/) print $(i-1)}')
        # Extract ns/day if present
        local ns_per_day=$(echo "$perf_line" | awk -F'[, ]+' '{for(i=1;i<=NF;i++) if($i~/ns\/day/) print $(i-1)}')
        # Extract hours/ns if present  
        local hours_per_ns=$(echo "$perf_line" | awk -F'[, ]+' '{for(i=1;i<=NF;i++) if($i~/hours\/ns/) print $(i-1)}')
        
        # Default to "-" if not found
        [ -z "$timestep_per_sec" ] && timestep_per_sec="-"
        [ -z "$ns_per_day" ] && ns_per_day="-"
        [ -z "$hours_per_ns" ] && hours_per_ns="-"
    else
        local timestep_per_sec="-"
        local ns_per_day="-"
        local hours_per_ns="-"
    fi
    
    # Calculate atom-steps per second
    local atom_steps_sec="-"
    if [ ! -z "$atoms" ] && [ "$timestep_per_sec" != "-" ]; then
        atom_steps_sec=$(echo "scale=0; $atoms * $timestep_per_sec / 1" | bc 2>/dev/null || echo "-")
    fi
    
    echo "LOOP_TIME=$loop_time"
    echo "TIMESTEPS=$timesteps"
    echo "ATOMS=$atoms"
    echo "TIMESTEP_PER_SEC=$timestep_per_sec"
    echo "NS_PER_DAY=$ns_per_day"
    echo "HOURS_PER_NS=$hours_per_ns"
    echo "ATOM_STEPS_SEC=$atom_steps_sec"
}

# Run a single benchmark
run_benchmark() {
    local bench_type=$1      # e.g., "lj", "eam"
    local config_name=$2     # e.g., "MPI-20"
    local omp_threads=$3     # e.g., "4"
    local command=$4         # e.g., "mpirun -np 20 lmp_serial -in"
    local input_file=$5      # e.g., "in.lj"
    
    local full_name="${bench_type}_${config_name}"
    local logfile="log.${full_name}"
    local description="${bench_type^^} - ${config_name}"
    
    echo "----------------------------------------"
    echo "Running: $description (OMP=$omp_threads)"
    echo "Input: $input_file"
    echo "Command: OMP_NUM_THREADS=$omp_threads $command $input_file"
    echo ""
    
    # Check if input file exists
    if [ ! -f "$BENCH_DIR/$input_file" ]; then
        echo "⚠ Skipping: $input_file not found"
        echo ""
        return 1
    fi
    
    # Run benchmark with safe directory handling
    if ! pushd "$BENCH_DIR" > /dev/null 2>&1; then
        echo "❌ Failed (cannot change to $BENCH_DIR)"
        echo ""
        return 0  # Return 0 to continue with other benchmarks
    fi
    
    # Execute command with input file (avoiding eval for security)
    # Split command into array for safer execution
    local log_path="../$logfile"
    local exit_code=0
    
    # Set OMP_NUM_THREADS and execute command
    export OMP_NUM_THREADS=$omp_threads
    $command $input_file -log "$log_path" > /dev/null 2>&1 || exit_code=$?
    
    popd > /dev/null 2>&1
    
    # Check for errors
    if [ $exit_code -ne 0 ]; then
        echo "❌ Failed (exit code: $exit_code)"
        echo ""
        return 0  # Return 0 to continue with other benchmarks
    fi
    
    if [ ! -f "$logfile" ]; then
        echo "❌ Failed (no log file created)"
        echo ""
        return 0  # Return 0 to continue with other benchmarks
    fi
    
    # Extract metrics
    local metrics=$(extract_metrics "$logfile")
    
    if echo "$metrics" | grep -q "ERROR="; then
        local error_msg=$(echo "$metrics" | grep "ERROR=" | cut -d= -f2)
        echo "❌ Failed: $error_msg"
        echo ""
        return 0  # Return 0 to continue with other benchmarks
    fi
    
    # Parse metrics
    eval "$metrics"
    
    # Display results
    echo "✓ Completed successfully"
    echo ""
    echo "  Performance Metrics:"
    [ ! -z "$LOOP_TIME" ] && [ "$LOOP_TIME" != "-" ] && echo "    Loop time:        $LOOP_TIME seconds"
    [ ! -z "$ATOMS" ] && [ "$ATOMS" != "-" ] && echo "    Atoms:            $ATOMS"
    [ ! -z "$TIMESTEPS" ] && [ "$TIMESTEPS" != "-" ] && echo "    Timesteps:        $TIMESTEPS"
    [ ! -z "$TIMESTEP_PER_SEC" ] && [ "$TIMESTEP_PER_SEC" != "-" ] && echo "    Timesteps/sec:    $TIMESTEP_PER_SEC"
    [ ! -z "$NS_PER_DAY" ] && [ "$NS_PER_DAY" != "-" ] && echo "    ns/day:           $NS_PER_DAY"
    [ ! -z "$HOURS_PER_NS" ] && [ "$HOURS_PER_NS" != "-" ] && echo "    hours/ns:         $HOURS_PER_NS"
    [ ! -z "$ATOM_STEPS_SEC" ] && [ "$ATOM_STEPS_SEC" != "-" ] && echo "    atom-steps/sec:   $ATOM_STEPS_SEC"
    echo ""
    
    # Store for markdown (format: bench_type|config_name|metrics...)
    echo "${bench_type}|${description}|$LOOP_TIME|$TIMESTEP_PER_SEC|$NS_PER_DAY|$HOURS_PER_NS|$ATOM_STEPS_SEC|$ATOMS" >> .benchmark_data.tmp
    
    return 0
}

# Initialize markdown results
init_markdown() {
    cat > "$RESULT_FILE" << 'EOF'
# LAMMPS Benchmark Results

## System Information

EOF
    
    echo "- **Date**: $(date)" >> "$RESULT_FILE"
    echo "- **Hostname**: $(hostname)" >> "$RESULT_FILE"
    echo "- **OS**: $(uname -s) $(uname -r)" >> "$RESULT_FILE"
    echo "- **Architecture**: $(uname -m)" >> "$RESULT_FILE"
    
    # CPU info
    if [ -f /proc/cpuinfo ]; then
        local cpu_model=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)
        local cpu_cores=$(grep -c "^processor" /proc/cpuinfo)
        echo "- **CPU**: $cpu_model" >> "$RESULT_FILE"
        echo "- **CPU Cores**: $cpu_cores" >> "$RESULT_FILE"
    fi
    
    echo "" >> "$RESULT_FILE"
    echo "## Benchmark Configurations" >> "$RESULT_FILE"
    echo "" >> "$RESULT_FILE"
    
    local idx=1
    for config in "${BENCHMARK_CONFIGS[@]}"; do
        IFS='|' read -r name command <<< "$config"
        echo "$idx. **$name**: \`$command <input_file>\`" >> "$RESULT_FILE"
        ((idx++))
    done
    
    echo "" >> "$RESULT_FILE"
    echo "---" >> "$RESULT_FILE"
    echo "" >> "$RESULT_FILE"
}

# Add results to markdown
add_results_to_markdown() {
    cat >> "$RESULT_FILE" << 'EOF'
## Performance Results

### Metrics Explanation

- **Loop Time**: Total execution time for benchmark (seconds, **lower is better**)
- **Timesteps/sec**: Rate of timestep calculation (**higher is better**)
- **ns/day**: Nanoseconds of simulation per day of runtime (**higher is better**)
- **hours/ns**: Hours needed to simulate 1 nanosecond (**lower is better**)
- **atom-steps/sec**: Atoms × timesteps per second (**higher is better**)

EOF

    # Group results by benchmark type
    for bench_type in lj eam chain rhodo reaxff; do
        if grep -q "^${bench_type}|" .benchmark_data.tmp 2>/dev/null; then
            echo "### ${bench_type^^} Benchmark" >> "$RESULT_FILE"
            echo "" >> "$RESULT_FILE"
            echo "| Configuration | Loop Time (s) | Timesteps/sec | ns/day | hours/ns | atom-steps/sec | Atoms |" >> "$RESULT_FILE"
            echo "|---------------|---------------|---------------|--------|----------|----------------|-------|" >> "$RESULT_FILE"
            
            grep "^${bench_type}|" .benchmark_data.tmp | while IFS='|' read -r bt desc loop ts_sec ns_day hrs_ns atom_steps atoms; do
                # Extract just the config name (after " - ")
                config=$(echo "$desc" | sed 's/^.*- //')
                
                # Format values
                [ -z "$loop" ] && loop="-"
                [ -z "$ts_sec" ] && ts_sec="-"
                [ -z "$ns_day" ] && ns_day="-"
                [ -z "$hrs_ns" ] && hrs_ns="-"
                [ -z "$atom_steps" ] && atom_steps="-"
                [ -z "$atoms" ] && atoms="-"
                
                echo "| $config | $loop | $ts_sec | $ns_day | $hrs_ns | $atom_steps | $atoms |" >> "$RESULT_FILE"
            done
            
            echo "" >> "$RESULT_FILE"
        fi
    done
}

# Add speedup analysis
add_speedup_analysis() {
    cat >> "$RESULT_FILE" << 'EOF'
## Speedup Analysis

Speedup is calculated relative to serial (single-core) execution for each binary.
Speedup = Serial time / Parallel time (higher is better)

EOF

    for bench_type in lj eam chain rhodo reaxff; do
        if grep -q "^${bench_type}|" .benchmark_data.tmp 2>/dev/null; then
            echo "### ${bench_type^^} Speedup" >> "$RESULT_FILE"
            echo "" >> "$RESULT_FILE"
            
            # Get conda-serial baseline
            local conda_serial=$(grep "^${bench_type}|.*conda-serial" .benchmark_data.tmp | head -1)
            local opt_serial=$(grep "^${bench_type}|.*opt-serial" .benchmark_data.tmp | head -1)
            
            IFS='|' read -r bt1 desc1 conda_baseline rest1 <<< "$conda_serial"
            IFS='|' read -r bt2 desc2 opt_baseline rest2 <<< "$opt_serial"
            
            echo "| Binary | Serial (s) | Configuration | Time (s) | Speedup |" >> "$RESULT_FILE"
            echo "|--------|------------|---------------|----------|---------|" >> "$RESULT_FILE"
            
            # conda speedup (relative to conda-serial)
            if [ -n "$conda_baseline" ] && [ "$conda_baseline" != "-" ]; then
                grep "^${bench_type}|.*conda-" .benchmark_data.tmp | while IFS='|' read -r bt desc time rest; do
                    config=$(echo "$desc" | sed 's/^.*- //')
                    if [ -z "$time" ] || [ "$time" = "-" ]; then
                        speedup="-"
                    else
                        speedup=$(echo "scale=2; $conda_baseline / $time" | bc 2>/dev/null || echo "-")
                    fi
                    echo "| conda | $conda_baseline | $config | $time | ${speedup}x |" >> "$RESULT_FILE"
                done
            fi
            
            # opt speedup (relative to opt-serial)
            if [ -n "$opt_baseline" ] && [ "$opt_baseline" != "-" ]; then
                grep "^${bench_type}|.*opt-" .benchmark_data.tmp | while IFS='|' read -r bt desc time rest; do
                    config=$(echo "$desc" | sed 's/^.*- //')
                    if [ -z "$time" ] || [ "$time" = "-" ]; then
                        speedup="-"
                    else
                        speedup=$(echo "scale=2; $opt_baseline / $time" | bc 2>/dev/null || echo "-")
                    fi
                    echo "| opt | $opt_baseline | $config | $time | ${speedup}x |" >> "$RESULT_FILE"
                done
            fi
            
            echo "" >> "$RESULT_FILE"
        fi
    done
}

# Add benchmark info
add_benchmark_info() {
    cat >> "$RESULT_FILE" << 'EOF'
---

## Benchmark Descriptions

### LJ (Lennard-Jones)
- **System**: Liquid argon-like atomic fluid
- **Potential**: Lennard-Jones with 2.5 cutoff
- **Typical atoms**: ~32,000
- **Use Case**: Most common benchmark, baseline for comparisons

### EAM (Embedded Atom Method)
- **System**: Copper (Cu) metallic solid
- **Potential**: EAM metallic potential
- **Typical atoms**: ~32,000
- **Use Case**: Metal simulations, ~2.6x slower than LJ

### Chain (Polymer)
- **System**: Bead-spring polymer melt (100-mer chains)
- **Potential**: FENE bonds + LJ interactions
- **Typical atoms**: ~32,000
- **Use Case**: Molecular dynamics, ~2x faster than LJ

### Rhodo (Rhodopsin)
- **System**: Rhodopsin protein in solvated lipid bilayer
- **Potential**: CHARMM force field + PPPM long-range
- **Typical atoms**: ~32,000
- **Use Case**: Biomolecular simulations, ~16x slower than LJ

### ReaxFF (Reactive Force Field)
- **System**: HNS (Hexanitrostilbene) energetic crystal
- **Potential**: ReaxFF reactive potential with charge equilibration
- **Typical atoms**: ~38,000 (5x5x5 replicate)
- **Use Case**: Reactive MD simulations, bond breaking/forming

---

## Reference

- **Official LAMMPS benchmarks**: https://www.lammps.org/bench.html
- **LAMMPS documentation**: https://docs.lammps.org
- **Benchmark source**: https://github.com/lammps/lammps/tree/stable/bench

EOF
}

# Main execution
main() {
    # Parse arguments
    parse_arguments "$@"
    
    # Show configuration
    echo "Benchmark configurations to test:"
    for config in "${BENCHMARK_CONFIGS[@]}"; do
        IFS='|' read -r name command <<< "$config"
        echo "  - $name: $command"
    done
    echo ""
    
    # Download benchmarks
    download_benchmarks
    
    # Initialize results (clean temp file BEFORE init to avoid stale data)
    rm -f .benchmark_data.tmp
    init_markdown
    
    # Run benchmarks
    echo "=========================================="
    echo "Running Benchmarks"
    echo "=========================================="
    echo ""
    
    # Available benchmark types
    local bench_types=("lj" "eam" "chain" "rhodo" "reaxff")
    local bench_inputs=("in.lj" "in.eam" "in.chain" "in.rhodo" "in.reaxff")
    
    for i in "${!bench_types[@]}"; do
        local bench_type="${bench_types[$i]}"
        local input_file="${bench_inputs[$i]}"
        
        if [ ! -f "$BENCH_DIR/$input_file" ]; then
            echo "⚠ Skipping ${bench_type^^}: $input_file not found"
            echo ""
            continue
        fi
        
        echo "=== ${bench_type^^} Benchmark ==="
        echo ""
        
        # Run with each configuration
        for config in "${BENCHMARK_CONFIGS[@]}"; do
            IFS='|' read -r name omp_threads command <<< "$config"
            run_benchmark "$bench_type" "$name" "$omp_threads" "$command" "$input_file"
        done
        
        echo ""
    done
    
    # Generate markdown report
    echo "=========================================="
    echo "Generating Report"
    echo "=========================================="
    echo ""
    
    add_results_to_markdown
    add_speedup_analysis
    add_benchmark_info
    
    # Cleanup
    rm -f .benchmark_data.tmp
    
    echo "✓ Results saved to: $RESULT_FILE"
    echo ""
    echo "=========================================="
    echo "Benchmark Complete!"
    echo "=========================================="
}

# Run main with all arguments
main "$@"
