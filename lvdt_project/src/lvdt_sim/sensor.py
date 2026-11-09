"""Symmetric differential transformer model, not a commercial sensor specification."""

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from .config import Config
from .trajectories import validate_displacement


@dataclass(frozen=True)
class SensorSignals:
    primary_v: NDArray
    secondary_1_v: NDArray
    secondary_2_v: NDArray
    differential_v: NDArray


def simulate(t_s: NDArray, displacement_mm: NDArray, config: Config) -> SensorSignals:
    """V1,2 = (A0 +/- (K*x + alpha*x**3)/2) sin(w*t + phase)."""
    x = validate_displacement(displacement_mm, config)
    t = np.asarray(t_s, dtype=float)
    if t.shape != x.shape or not np.all(np.isfinite(t)):
        raise ValueError("time and displacement must have matching finite vectors")
    angle = 2 * np.pi * config.fc_hz * t
    carrier = np.sin(angle + np.deg2rad(config.phase_deg))
    amplitude = config.sensitivity_v_per_mm * x + config.cubic_v_per_mm3 * x**3
    v1 = (config.secondary_null_v + amplitude / 2) * carrier
    v2 = (config.secondary_null_v - amplitude / 2) * carrier
    return SensorSignals(config.primary_peak_v * np.sin(angle), v1, v2, v1 - v2)
