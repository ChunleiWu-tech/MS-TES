# Upstream reproducible code

Release: `TES-PUB-V10.1.0-MANUSCRIPT-AUDITED-20260816`

This is the source-only upstream package for the manuscript "Validity-domain auditing and engineering evidence reshape service-specific molten-salt rankings for thermal energy storage". It contains the complete model code, registered inputs, raw database archives, provenance ledgers, configuration, dependency locks and deterministic seed rules.

Generated tables and quality-control outputs are intentionally excluded from this archive. A registered full run recreates them under `outputs/`. The exclusion removes approximately 341 MB of reproducible output, including a 285 MB draw-level Monte Carlo table, without removing scientific inputs.

## Registered scope

- Official database screen: 976 raw composition records, followed by 937 records with melting data, 250 application-compatible records and 74 records meeting minimum thermophysical coverage.
- Curated exact-composition library: 142 candidates evaluated across seven services, giving 994 candidate-service pairs.
- Formal engineering model: frozen 15-candidate registry with 20,000 Monte Carlo draws.
- Expanded opportunity layer: 142 candidates with 20,000 matched candidate-keyed draws.
- Candidates outside the frozen engineering registry receive no formal-selection or formal-failure assignment.

## Requirements

- 64-bit CPython 3.12
- Exact packages in `requirements-lock.txt`
- At least 4 GB available RAM
- At least 1 GB free disk space for the environment and approximately 350 MB of generated tables and QC outputs

Arial is not required for upstream calculation. It is required only by the final post-processing renderer.

## Full registered run

Windows PowerShell:

```powershell
cd upstream_reproducible_code
.\SETUP_ENV.bat
.\RUN_FULL_RECOMPUTE.bat
```

Linux or macOS:

```bash
cd upstream_reproducible_code
./SETUP_ENV.sh
./RUN_FULL_RECOMPUTE.sh
```

The run is complete only when the terminal reports that the upstream full recompute completed successfully and `outputs/qc/UPSTREAM_RELEASE_STATUS.json` reports `PASS`, `science_changed: false` and `mc_iterations: 20000`.

## Scientific boundary

The expanded library is an opportunity screen. Formal evidence-bounded selection remains restricted to the frozen engineering registry. A thermophysically promising composition is not described as formally rejected when its corrosion, cycling, containment or replication evidence has not been registered.

