# pyclone-learning

Learning notes and reproducible reanalysis of a single-sample experiment with **original PyClone**, using the PyClone 0.13.1 command-line interface. This project does not use PyClone-VI or infer an evolutionary tree.

## What this repository contains

The input, four original analysis scripts, configuration, result tables, figures, and complete compressed MCMC traces were recovered from the original local project. The working scripts retain the original analysis logic and add configurable paths and validation. Recovered scripts are retained in `provenance/original_scripts/`; private absolute paths in two scripts have been replaced with generic placeholders. Their analysis logic is unchanged.

The shared path helper, ARI calculation, approximate ESS calculation, joint-event diagnostics, and shell workflow are **reconstructed additions**. The data and traces are real archived files, not synthetic replacements.

## Main findings

- **134 mutations** and **6 clusters** in the archived final partition.
- Donor-label adjusted Rand index: **0.6980826145**.
- The selected mutation pair co-clusters in **412/800 retained states (0.515)**.
- Beta-binomial precision drifts substantially. Convergence has **not** been established.

The six clusters are a post-processing partition, not six proven cancer clones. The input is a mixture of healthy donors, and ARI is not classification accuracy.

## Quick start: reanalyze archived results

Run from the repository root in a separate Python 3.12 analysis environment:

```sh
python -m venv .venv
# Linux/WSL: source .venv/bin/activate
# Windows PowerShell: .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python scripts/plot_pyclone_single.py
python scripts/validate_pyclone_clusters.py
python scripts/examine_cluster1.py
python scripts/check_mcmc_trace.py
```

These commands read the included `data/` and `evidence/single_test/` files and write to `results/review/`. PyClone itself is not required for this reanalysis. Generated `results/` files are ignored by Git; archived evidence is tracked.

To use an external original project without copying its official PyClone checkout:

```sh
python scripts/validate_pyclone_clusters.py --data-root /path/to/pyclone-project
python scripts/check_mcmc_trace.py --data-root /path/to/pyclone-project
python scripts/plot_pyclone_single.py --result-dir /path/to/run --output-dir results/new-review
```

`--result-dir` identifies a directory containing `tables/` and/or `trace/`, as required by the selected script. `--input` overrides the raw TSV. `--sample` defaults to `SRR385938`. The trace script also accepts `--burnin`, `--thin`, `--mutation1`, and `--mutation2`. Quote paths containing spaces. Use `--help` for details.

## Reading guide

1. [Background and data provenance](docs/01-background.md)
2. [The PyClone model](docs/02-pyclone-model.md)
3. [Single-sample analysis and configuration](docs/03-single-sample-analysis.md)
4. [Validation and the confusion matrix](docs/04-results-validation.md)
5. [MCMC diagnostics and uncertainty](docs/05-mcmc-diagnostics.md)

See [environment.md](environment.md) for dependencies and a fresh-inference workflow. `reports/` contains verified reanalysis outputs, environment versions, and test records. `provenance/manifest.json` records project-relative source paths and SHA-256 checksums, including original hashes for path-sanitized files.

```text
data/                  One real example input TSV
docs/                  English learning notes
scripts/               Configurable analysis scripts and reconstructed runner
evidence/single_test/  Archived configuration, YAML, tables, traces, and figures
provenance/            Path-sanitized recovered scripts and upstream attribution
reports/               Verified reanalysis outputs and test records
```

## Reproducibility and attribution

Reanalysis reproduces summaries of the archived run. A fresh MCMC run is stochastic and need not reproduce its partition. The original seed and full legacy environment were not recovered, and fresh PyClone inference was not executed during preparation of this repository.

Upstream data and PyClone-related materials retain their existing restrictions; see `provenance/PyClone-LICENSE.md` and the [official repository](https://github.com/Roth-Lab/pyclone). This project does not grant a new license to upstream materials.
