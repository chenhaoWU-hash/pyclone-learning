# Environment and reproduction

## Modern analysis environment

The four Python analysis scripts were tested with Python 3.12. Dependencies are pandas, NumPy, Matplotlib, and scikit-learn. `requirements.txt` provides compatible version ranges; `reports/tested-environment.txt` records the actual platform and main versions, and `reports/requirements-tested.txt` records the installed analysis dependencies.

```sh
python -m venv .venv
source .venv/bin/activate  # Windows: .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python scripts/plot_pyclone_single.py
python scripts/validate_pyclone_clusters.py
python scripts/examine_cluster1.py
python scripts/check_mcmc_trace.py
```

Run these commands from the repository root. They default to the included archived input/results. To analyze a new run, add `--result-dir results/pyclone/single_test`; to read the external original project, add `--data-root /path/to/pyclone-project`. Input and result paths can be overridden separately. No official Git checkout needs to be committed. Figures use the noninteractive Agg backend.

For the exact installed versions recorded during preparation, use `python -m pip install -r reports/requirements-tested.txt` in a compatible Python/platform environment. Version ranges alone do not guarantee future dependency resolution will select those versions.

## Separate legacy PyClone inference environment

The original complete installation record was not recovered. The local source declares a PyClone 0.13.1 interface and uses Python-2-era dependencies and old pandas APIs. Keep it separate from the modern analysis environment.

The following Linux/WSL conda setup is a **candidate reconstruction**, not a tested installation. PyClone inference was not installed or run during repository preparation, and solver/platform availability is unverified:

```sh
conda create -n pyclone-original -c conda-forge -c bioconda python=2.7 pyclone=0.13.1
conda activate pyclone-original
PyClone --version
PyClone setup_analysis --help
PyClone build_table --help
bash scripts/run_single_sample.sh
conda list --explicit > results/pyclone-conda-explicit.txt
```

If old packages cannot be resolved, inspect the [upstream recipe](https://github.com/Roth-Lab/pyclone/blob/master/conda/recipe/meta.yaml) and record the actual environment and any patches. PyClone-VI is not a substitute implementation for reproducing this experiment. See the [official installation guide](https://github.com/Roth-Lab/pyclone#installation).

The runner requires bash, `realpath`, and `PyClone` on PATH. It is not a native PowerShell script. It generates a new configuration using absolute paths and defaults to 1000 iterations, seed 101, `major_copy_number` prior, burn-in 200, and thinning 1. Override these using `NUM_ITERS`, `SEED`, `BURNIN`, and `THIN`. The first and second positional arguments override the input and output directory. Existing output directories are rejected to avoid overwriting a run.

Fresh inference is a new experiment and need not match the old chain. Use distinct output directories and seeds for longer, independent runs. The reconstructed runner's shell syntax was checked, but inference was not executed.

## Repository contents and publishing

Track the notes, working scripts, one small example input, archived evidence, and verified reports. Do not commit the official source checkout, virtual environments, or unrelated external data. `evidence/` and `reports/` are intentionally tracked, while generated `results/` is ignored.

All project documentation is in English. Recovered scripts are retained as source evidence, with private paths sanitized where necessary; upstream notices are unchanged. No new license is granted to upstream materials; review the included attribution and upstream terms before redistributing or reusing them.
