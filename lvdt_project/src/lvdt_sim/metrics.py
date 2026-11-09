"""Numerical calibration, estimation error, and Monte Carlo summary metrics."""

import numpy as np
from numpy.typing import NDArray


def error_metrics(truth: NDArray, estimate: NDArray) -> dict[str, float]:
    a, b = np.asarray(truth, dtype=float), np.asarray(estimate, dtype=float)
    if a.shape != b.shape or a.size == 0 or not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("metrics require matching nonempty finite inputs")
    e = b - a
    return {"bias_mm": float(np.mean(e)), "rmse_mm": float(np.sqrt(np.mean(e**2))),
            "mae_mm": float(np.mean(np.abs(e))), "max_absolute_error_mm": float(np.max(np.abs(e))),
            "std_mm": float(np.std(e))}


def calibration(truth_mm: NDArray, estimate_mm: NDArray, sensitivity_v_per_mm: float) -> dict[str, float]:
    result = error_metrics(truth_mm, estimate_mm)
    x, y = np.asarray(truth_mm), np.asarray(estimate_mm)
    if np.unique(x).size < 2:
        raise ValueError("Calibration requires at least two distinct positions")
    slope, offset = np.polyfit(x, y, 1)
    residual = np.sum((y - (slope*x + offset))**2)
    total = np.sum((y - np.mean(y))**2)
    result.update(slope_mm_per_mm=float(slope), offset_mm=float(offset),
                  estimated_sensitivity_v_per_mm=float(slope * sensitivity_v_per_mm),
                  r_squared=float(1 - residual/total) if total else 0.0)
    return result
