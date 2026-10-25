#!/usr/bin/env bash
# Reconstructed workflow, not the recovered historical shell command.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INPUT="${1:-$REPO/data/SRR385938.tsv}"
WORK="${2:-$REPO/results/pyclone/single_test}"
INPUT="$(realpath "$INPUT")"
WORK="$(realpath -m "$WORK")"
if [[ -e "$WORK" ]]; then echo "Choose a new output directory: $WORK exists" >&2; exit 1; fi
mkdir -p "$WORK"
PyClone setup_analysis --in_files "$INPUT" --working_dir "$WORK" --samples SRR385938 --tumour_contents 1.0 --density pyclone_beta_binomial --init_method disconnected --num_iters "${NUM_ITERS:-1000}" --prior major_copy_number
PyClone run_analysis --config_file "$WORK/config.yaml" --seed "${SEED:-101}"
for TYPE in loci cluster; do
  PyClone build_table --config_file "$WORK/config.yaml" --table_type "$TYPE" --out_file "$WORK/$TYPE.tsv" --burnin "${BURNIN:-200}" --thin "${THIN:-1}"
done
mkdir -p "$WORK/tables"
mv "$WORK/loci.tsv" "$WORK/cluster.tsv" "$WORK/tables/"
