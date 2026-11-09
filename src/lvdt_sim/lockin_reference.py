"""Rectangular, single-channel synchronous detection; incomplete tails discarded."""

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from .config import Config
from .reference import Q_SCALE, reference_samples


@dataclass(frozen=True)
class LockInResult:
    start_sample: NDArray
    end_sample: NDArray
    center_time_s: NDArray
    displacement_mm: NDArray
    accumulator: NDArray | None = None


def _windows(values: NDArray, config: Config, start_sample: int) -> tuple[NDArray, NDArray, NDArray, NDArray]:
    a = np.asarray(values)
    if a.ndim != 1 or not np.all(np.isfinite(a)):
        raise ValueError("Lock-in input must be a finite vector")
    if type(start_sample) is not int or start_sample < 0 or start_sample % config.window_samples:
        raise ValueError("start_sample must be a nonnegative measurement-window boundary")
    count = a.size // config.window_samples
    start = start_sample + np.arange(count, dtype=np.int64) * config.window_samples
    end = start + config.window_samples - 1
    center = (start + end) / (2 * config.fs_hz)
    return a[:count * config.window_samples].reshape(count, config.window_samples), start, end, center


def floating(voltage_v: NDArray, config: Config, start_sample: int = 0) -> LockInResult:
    """Use measured analog-equivalent volts, not reconstructed ADC volts."""
    windows, start, end, center = _windows(voltage_v, config, start_sample)
    ref = reference_samples(windows.size, config.lut_length, start_sample, fixed=False).reshape(windows.shape)
    amplitude_v = 2 * np.sum(windows * ref, axis=1) / config.window_samples
    return LockInResult(start, end, center, amplitude_v / config.sensitivity_v_per_mm)


def accumulator_to_mm(accumulator: NDArray, config: Config) -> NDArray:
    """Only the final engineering-unit conversion uses floating point."""
    return (2 * np.asarray(accumulator, dtype=np.float64) / (config.window_samples * Q_SCALE)
            * config.adc_full_scale_v / (1 << (config.adc_bits - 1)) / config.sensitivity_v_per_mm)


def fixed(codes: NDArray, config: Config, start_sample: int = 0) -> LockInResult:
    a = np.asarray(codes)
    limit = 1 << (config.adc_bits - 1)
    if a.dtype.kind not in "iu" or np.any(a < -limit) or np.any(a >= limit):
        raise ValueError("Fixed lock-in requires valid signed ADC integer codes")
    max_sum = config.window_samples * limit * Q_SCALE
    if max_sum > np.iinfo(np.int64).max:
        raise ValueError("Configured window could overflow int64 accumulation")
    windows, start, end, center = _windows(a, config, start_sample)
    ref = reference_samples(windows.size, config.lut_length, start_sample).reshape(windows.shape)
    sums = np.sum(windows.astype(np.int64) * ref.astype(np.int64), axis=1, dtype=np.int64)
    return LockInResult(start, end, center, accumulator_to_mm(sums, config), sums)
