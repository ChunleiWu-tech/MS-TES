# Upstream reproducible code

This source-only package regenerates all scientific tables used by the manuscript from the included registered inputs and raw database archives. It contains **no generated result tables** and no font files.

## Requirements

- 64-bit CPython 3.12
- Exact packages in `requirements-lock.txt`
- At least 4 GB available RAM
- Sufficient free disk space for the approximately 200 MB draw-level CSV and downstream tables

Arial is not required for upstream calculation. Its availability is reported only for handoff to the post-processing package, where Arial is mandatory.

## Windows PowerShell / VS Code

```powershell
cd "$env:USERPROFILE\Desktop\upstream_reproducible_code"
.\SETUP_ENV.bat
.\RUN_FULL_RECOMPUTE.bat
```

The formal runner always forces the registered **20,000 Monte Carlo draws**, enables Python fault handling, and limits OpenMP/OpenBLAS/MKL/NumExpr to one thread.

The run is complete only when the terminal prints:

```text
Upstream full recompute completed successfully.
```

The canonical final status is:

```text
outputs\qc\UPSTREAM_RELEASE_STATUS.json
```

It must contain:

```json
{
  "status": "PASS",
  "science_changed": false,
  "mc_iterations": 20000
}
```

`submission_UPSTREAM_STATUS.json` is retained only as an identical compatibility alias. `validate_release_contract.py` fails the run if the two files disagree or any producer/consumer filename is missing.

## Linux/macOS

```bash
./SETUP_ENV.sh
./RUN_FULL_RECOMPUTE.sh
```

## Non-publication smoke test

```powershell
.\RUN_SMOKE_TEST.bat
```

The smoke test uses 500 draws and now exercises the contract-table and independent scoring-audit stages in addition to the core calculation. Its outputs must never be synchronised into the submission post-processing package.

## Windows stability implementation

Draw-level rows are streamed candidate by candidate with Python's standard-library `csv` writer in bounded 2,000-row slices. The high-frequency draw export no longer calls `pandas.DataFrame.to_csv()`, thereby bypassing pandas' native `get_values_for_csv` conversion path that triggered Windows heap-corruption failures such as `0xC0000374`. Gate-reason and rank counts remain computed directly with NumPy.

## Scientific boundaries

The workflow preserves strict-complete service assessment, non-compensatory evidence gating, the registered ≥1% formal-selection threshold, separate continuous-variance and categorical-information attribution, and the registered evidence-action DAG. Model-estimated values remain outside formal evidence-bounded selection and are used only for audit or information extension.
