"""Additive voltage components, using local reproducible independent RNG streams."""

import numpy as np
from numpy.typing import NDArray
from .config import Config


def gaussian(count: int, std_v: float, seed: int, stream_id: int = 0) -> NDArray:
    """SeedSequence [seed, stream_id] separates scenarios without global RNG state."""
    if type(count) is not int or count < 0 or not np.isfinite(std_v) or std_v < 0:
        raise ValueError("count and standard deviation must be nonnegative")
    if type(seed) is not int or type(stream_id) is not int or min(seed, stream_id) < 0:
        raise ValueError("seed and stream_id must be nonnegative integers")
    return np.random.default_rng(np.random.SeedSequence([seed, stream_id])).normal(0, std_v, count)


def components(t_s: NDArray, config: Config, stream_id: int = 0) -> dict[str, NDArray]:
    """Noise acts on the differential measurement after the ideal sensor."""
    t = np.asarray(t_s, dtype=float)
    if t.ndim != 1 or not np.all(np.isfinite(t)):
        raise ValueError("time must be a finite vector")
    def tone(peak: float, hz: float, phase_deg: float = 0) -> NDArray:
        return peak * np.sin(2 * np.pi * hz * t + np.deg2rad(phase_deg))
    return {
        "gaussian_v": gaussian(t.size, config.noise_std_v, config.seed, stream_id),
        "hum_v": tone(config.hum_peak_v, config.hum_hz, config.hum_phase_deg),
        "dc_v": np.full(t.size, config.dc_offset_v),
        "interference_v": tone(config.interference_peak_v, config.interference_hz, config.interference_phase_deg),
        "drift_v": tone(config.drift_peak_v, config.drift_hz),
    }
