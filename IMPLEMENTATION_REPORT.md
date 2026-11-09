# Phase 1 delivery

Implemented the complete modular Python subsystem: physical motion and LVDT
windings, optional nonlinearity and phase, additive noise/interference/drift,
saturating ADC, signed HEX and Q1.14 LUT generation, floating and exact integer
lock-in references, exported ground truth and expected results, CLI workflows,
numerical studies, tests, and eight static engineering plots.

The complete source/output repository tree, all physical equations, configuration
keys, data contracts, installation instructions, and HDL timing are in [README.md](README.md).

## Executed commands

Executed from `C:\Projects\LVDT_Digital_LockIN\lvdt_project` using Python 3.12.7.
Existing NumPy 1.26.4, Matplotlib 3.9.2, pytest 7.4.4 were reused offline:

```powershell
python -m venv .venv --system-site-packages
.\.venv\Scripts\python.exe -m pip install -e . --no-build-isolation --no-deps --disable-pip-version-check
.\.venv\Scripts\python.exe scripts\generate_scenarios.py --config configs\baseline.json --all
.\.venv\Scripts\python.exe scripts\generate_scenarios.py --config configs\baseline.json
.\.venv\Scripts\python.exe scripts\generate_scenarios.py --config configs\noisy.json
.\.venv\Scripts\python.exe scripts\generate_scenarios.py --config configs\dynamic.json
.\.venv\Scripts\python.exe scripts\generate_hdl_vectors.py --config configs\calibration.json
.\.venv\Scripts\python.exe scripts\run_validation.py
.\.venv\Scripts\python.exe scripts\generate_diagnostic_plots.py
.\.venv\Scripts\python.exe scripts\audit_exports.py
```

The initial attempt at an editable installation outside the virtual environment
was denied by filesystem permissions. Installation inside `.venv` succeeded.
All project CLI commands above completed successfully. No network package
download was required. The automated suite was run during implementation stages
(21, then 24, then 32, then 56 tests) and finally with added reproducibility and
accepted-sample timing checks: **58 passed, 0 failed, 0 errors, 0 skipped**.
The numerical study runner passed **23 acceptance checks**. All eight generated
PNG layouts were visually inspected.

## Representative results

One 200-sample clean window, default configuration:

| True position (mm) | Floating estimate (mm) | Fixed estimate (mm) | Absolute fixed error (mm) | Exact integer sum |
|---:|---:|---:|---:|---:|
| +2 | +2.000000000 | +1.999789228 | 0.000210772 | +644177200 |
| -2 | -2.000000000 | -1.999789228 | 0.000210772 | -644177200 |
| 0 | 0.000000000 | 0.000000000 | 0.000000000 | 0 |

Calibration over -5 through +5 mm: sensitivity **0.239985242757 Vpeak/mm**,
offset approximately **0 mm**, R² **0.999999964171**, maximum absolute error
**0.001050249 mm**, mean absolute error **0.000449626 mm**.

Monte Carlo used 1,000 independent 200-sample windows at each of five Gaussian
noise levels. At sigma=0.4 V, measured RMSE was **0.1639279 mm**, compared with
unclipped white-noise theory standard deviation **0.1666667 mm**. Individual trial
estimates, mean confidence intervals, bias, RMSE, standard deviations, and
clipping statistics are saved in the reports.

At +2 mm, a 0.24 Vpeak 1 kHz interferer at zero phase produces approximately
+3 mm. At 30 degrees it causes **+0.8660254 mm** floating-reference bias. Nearby
950/1050 Hz tones cause beating; their RMS errors over 100 windows are
**0.3262083/0.3108099 mm** for the tested 0.24 Vpeak, 30-degree conditions.
The overrange scenario clipped **10,000 of 20,000 samples (50%)**.

## Generated deliverables

`output/vectors/<scenario>/` contains `adc_samples.hex`, `reference_lut.hex`,
`expected_results.csv`, and `metadata.json`. `output/ground_truth/<scenario>/`
contains the matching `ground_truth.csv`. Thirteen scenario directories exist:
null, positive, negative, calibration, high_noise, step, sinusoidal,
phase_mismatch, adc_overrange, same_frequency_interference, baseline, noisy,
dynamic. The calibration stream has 11,000 samples and 55 results; the other
streams each have 20,000 samples and 100 results.

The independent export audit decoded **251,000 samples** and checked all
**1,255 integer sums** against the emitted CSVs, with exact agreement and
correct sample order/sign extension. Hashes are in `output/reports/export_audit.json`.

Eight PNG diagnostics are under `output/diagnostics/`. Numerical Markdown/JSON,
calibration CSV, 5,000 Monte Carlo trial estimates, noise summary, JUnit XML,
and machine-readable test counts are under `output/reports/`.

## HDL integration

Reset for each scenario; load both HEX files as signed 16-bit words. Reference
entry 0 multiplies ADC sample 0. Advance reference/count only on sample_valid.
Accumulate signed products in at least 40 bits. Include accepted sample 199
before latching the first sum, then start the next window without resetting
reference phase. Arbitrary sample-valid gaps must not advance counters. Compare
each completed signed integer output exactly with expected_accumulator in the
corresponding expected_results.csv. Reset clears accumulation/count/phase.

Conservative product magnitude bound: 33,554,432. Conservative 200-sample sum
magnitude bound: 6,710,886,400. This needs 34 signed bits; 40 is safely sufficient.

## Remaining limits

No unresolved Phase 1 test or export failures. Execution was verified on Windows;
Linux-compatible pathlib/standard-library code is supplied but was not executed
on Linux in this session. This is a sampled teaching model, without analog
anti-alias filtering or hardware validation. Uncompensated phase causes cosine
gain error, coherent interference remains ambiguous, saturation distorts
measurements, and changing displacement is sine-squared weighted over each
measurement window. Nonlinear response is not inverted. No GUI, dashboard,
Verilog RTL, or deployment was implemented.
