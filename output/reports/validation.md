# Phase 1 numerical validation

All 23 numerical checks passed; seed 42.

## Static positions

| Truth (mm) | Fixed estimate (mm) | Absolute error (mm) | Integer sum |
|---:|---:|---:|---:|
| 0 | 0.000000000 | 0.000000000 | 0 |
| 2 | 1.999789228 | 0.000210772 | 644177200 |
| -2 | -1.999789228 | 0.000210772 | -644177200 |

## Calibration

- bias_mm: 0
- rmse_mm: 0.000629328094141
- mae_mm: 0.000449625831662
- max_absolute_error_mm: 0.0010502487421
- std_mm: 0.000629328094141
- slope_mm_per_mm: 0.999938511487
- offset_mm: 1.35437186514e-18
- estimated_sensitivity_v_per_mm: 0.239985242757
- r_squared: 0.999999964171

## Gaussian Monte Carlo (1000 independent windows per level)

| Sigma (V) | Bias (mm) | RMSE (mm) | Std (mm) | Theory std (mm) |
|---:|---:|---:|---:|---:|
| 0 | -0.0002108 | 0.0002108 | 0.0000000 | 0.0000000 |
| 0.05 | 0.0001453 | 0.0211879 | 0.0211874 | 0.0208333 |
| 0.1 | -0.0013333 | 0.0430393 | 0.0430186 | 0.0416667 |
| 0.2 | 0.0026625 | 0.0809440 | 0.0809002 | 0.0833333 |
| 0.4 | 0.0000555 | 0.1639279 | 0.1639279 | 0.1666667 |

## Interference (0.24 Vpeak, 30 degree phase)

| Frequency (Hz) | Mean bias (mm) | RMS error (mm) |
|---:|---:|---:|
| 400 | 0.0000000 | 0.0000000 |
| 950 | 0.0000000 | 0.3262083 |
| 1000 | 0.8660254 | 0.8660254 |
| 1050 | -0.0000000 | 0.3108099 |
| 1600 | 0.0000000 | 0.0000000 |

Near-carrier interference beats across windows. Same-frequency interference persists as a signed projection.
No phase correction, noise removal guarantee, or hardware accuracy claim is implied.
