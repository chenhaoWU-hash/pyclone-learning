# 03 · Single-sample analysis

## Configuration recovered from the archived run

Source: `evidence/single_test/config.yaml`.

|Parameter|Archived value|
|---|---|
|Sample|SRR385938|
|Density|pyclone_beta_binomial|
|Iterations|1000|
|Initialization|disconnected|
|Tumor content|1.0|
|Error rate|0.001|
|Beta base measure: alpha, beta|1, 1|
|Initial concentration|1.0|
|Concentration Gamma prior: shape, rate|1.0, 0.001|
|Initial beta-binomial precision|1000|
|Precision Gamma prior: shape, rate|1.0, 0.001|
|Precision proposal precision|0.01|

Gamma parameters use shape/rate, not shape/scale. The archived configuration contains the original WSL working path and mutation-file layout. Preserve it as evidence; generate a new configuration for a new run.

The diagnostic analysis uses saved trace rows 200–999 inclusive (zero-based), burn-in 200, and thinning 1: 800 retained states. The historical `build_table` command was not recovered. The reconstructed workflow explicitly uses these burn-in/thinning values but does not claim to recover the original command. The historical seed and input-prior CLI choice were not saved in the configuration; the archived mutation YAML preserves the actual feasible states.

## Two levels of reproduction

**Archived-result reanalysis:** use the README commands in a modern Python environment to redraw figures and recompute cluster/trace metrics. This requires neither the official source checkout nor legacy PyClone inference dependencies.

**Fresh inference:** use `scripts/run_single_sample.sh` in a separate Linux/WSL legacy PyClone environment. This is a reconstructed, reviewable workflow. Its `major_copy_number` prior and seed 101 are explicit new-experiment choices, not recovered historical settings. Compare generated hyperparameters with the table above. To preserve the exact historical feasible states, explicitly configure a new run to use the archived mutation YAML at its absolute path after checking its read counts and sample information.

```sh
bash scripts/run_single_sample.sh
python scripts/validate_pyclone_clusters.py --result-dir results/pyclone/single_test
python scripts/check_mcmc_trace.py --result-dir results/pyclone/single_test
```

The archived loci table retains 134 mutations. Final cluster sizes are 32, 48, 38, 10, 5, and 1. Longer runs with independent seeds are the next convergence investigation; they need not produce the same cluster count or numbering.
