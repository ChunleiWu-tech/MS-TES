# MS-TES: evidence-bounded molten-salt screening for thermal energy storage

This repository contains release `v10.1.0` of the reproducible code for the manuscript "Validity-domain auditing and engineering evidence reshape service-specific molten-salt rankings for thermal energy storage".

## What changed in v10.1.0

The codebase now implements one traceable scientific chain:

1. Screen official composition records without pooling incompatible evidence objects.
2. Canonically deduplicate the expanded library into 142 exact compositions.
3. Evaluate 994 candidate-service pairs across seven TES duties.
4. Separate physical-window compatibility, quantitative thermophysical coverage, service-domain support and linkage to the frozen engineering registry.
5. Preserve a strict boundary between thermophysical opportunity and formal evidence-bounded selection.
6. Trace decision uncertainty back to registered properties, evidence gaps and precedence-valid research actions.

The resulting contraction is 142 candidates to 994 pairs, 76 physically compatible pairs, 18 quantitative pairs, 11 service-domain-supported pairs and 8 pairs linked to the frozen engineering registry.

A newly documented 2025 NaCl-KCl-CaCl2 composition reaches a 23.48% PCM500 thermophysical rank-1 frequency in the opportunity layer. It is outside the frozen engineering registry, so no formal outcome is assigned. This counterexample supports the central conclusion: there is no universal best salt, and thermophysical rank alone is not a decision.

## Download files

- `TES_v10.1.0_upstream_source_only.zip`: complete model code, registered inputs, raw database archives and provenance. Generated 20,000-draw tables are omitted and recreated by the registered run.
- `TES_v10.1.0_postprocess_source_only.zip`: current figure renderer and publication QA. It synchronizes the sibling upstream results at run time.
- `SHA256SUMS.txt`: integrity hashes for all release files.

The source-only split keeps the repository compact. The omitted upstream output directory is approximately 341 MB and is entirely regenerable from the included inputs and code.

## Reproduce the release

Unpack the two archives side by side. On Windows:

```powershell
cd upstream_reproducible_code
.\SETUP_ENV.bat
.\RUN_FULL_RECOMPUTE.bat

cd ..\postprocess_reproducible_code
.\SETUP_ENV.bat
.\RUN_POSTPROCESS.bat
```

On Linux or macOS, use the corresponding `.sh` wrappers.

Release requirements:

- 64-bit CPython 3.12;
- exact packages from `requirements-lock.txt`;
- at least 4 GB RAM and 1 GB free disk space;
- Arial installed locally for final figure export.

The registered upstream workflow uses 20,000 Monte Carlo draws. The current post-processing release generates six main figures and twelve supplementary figures and passes 42 scientific, semantic and visual checks.

## Citation and versions

For exact reproducibility, cite the DOI of the specific archived version. The Zenodo Concept DOI may be used when the intention is to resolve to the latest version of this evolving codebase. Previous releases remain available and are not overwritten.

## Licences

Project code is released under the MIT License. Project-authored derived data and evidence classifications are released under CC BY 4.0. Third-party database and literature content retains its original terms; provenance and source boundaries are recorded in the included ledgers.

