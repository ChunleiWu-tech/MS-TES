# Post-processing reproducible code

Release: `TES-PUB-V10.1.0-MANUSCRIPT-AUDITED-20260816`

This source-only package renders and validates six main figures and twelve supplementary figures from a sibling upstream release. It contains the current publication renderer, figure-support code, captions, panel logic, validation rules and exact dependency lock.

The archive intentionally excludes:

- the local Python environment;
- upstream tables synchronized during a previous run;
- generated PNG and PDF figures;
- generated contact sheets and QC outputs.

These files are recreated locally. The sibling upstream package must first complete its registered 20,000-draw full run.

## Directory arrangement

Unpack both source archives side by side:

```text
working_directory/
  upstream_reproducible_code/
  postprocess_reproducible_code/
```

## Final figure run

Windows PowerShell:

```powershell
cd postprocess_reproducible_code
.\SETUP_ENV.bat
.\RUN_POSTPROCESS.bat
```

Linux or macOS:

```bash
cd postprocess_reproducible_code
./SETUP_ENV.sh
./RUN_POSTPROCESS.sh
```

A release render requires 64-bit CPython 3.12, the exact versions in `requirements-lock.txt` and a real local Arial installation. The current validated renderer produces 6 main figures, 12 supplementary figures and passes 42 scientific, semantic and visual checks.

## Current visual QA additions

- Figure 4 uses aligned outer axes, visible capped 5-95% intervals and collision-tested direct labels.
- Supplementary Figure 5 separates coverage labels from overclaim values around each sphere.
- Supplementary Figure 11c places exact synergy values below their spheres.
- Supplementary Figure 11d uses a wider quantitative axis and keeps the 98% endpoint badge inside the axis.

