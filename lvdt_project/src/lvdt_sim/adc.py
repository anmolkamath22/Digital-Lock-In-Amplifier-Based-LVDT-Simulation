"""Bipolar ADC: NumPy rint (ties to even), saturation, signed int16 container."""

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from .config import Config


@dataclass(frozen=True)
class ADCResult:
    codes: NDArray[np.int16]
    reconstructed_v: NDArray[np.float64]
    clipped_mask: NDArray[np.bool_]
    analog_overrange_mask: NDArray[np.bool_]

    @property
    def clipped_count(self) -> int:
        return int(np.count_nonzero(self.clipped_mask))

    @property
    def clipped_percent(self) -> float:
        return 100 * self.clipped_count / self.codes.size if self.codes.size else 0.0


def codes_to_voltage(codes: NDArray, config: Config) -> NDArray:
    codes = np.asarray(codes)
    limit = 1 << (config.adc_bits - 1)
    if codes.dtype.kind not in "iu" or np.any(codes < -limit) or np.any(codes >= limit):
        raise ValueError("ADC codes must be signed-range integers")
    return codes.astype(np.float64) * (config.adc_full_scale_v / limit)


def quantize(voltage_v: NDArray, config: Config) -> ADCResult:
    """Clipped includes rounded codes outside range; overrange means |v| > F.

    +F rounds to +2048 and saturates to +2047; -F is representable exactly.
    Analog bounds are applied before scaling to avoid numerical overflow.
    """
    v = np.asarray(voltage_v, dtype=np.float64)
    if v.ndim != 1 or not np.all(np.isfinite(v)):
        raise ValueError("ADC input must be a finite one-dimensional voltage vector")
    f = config.adc_full_scale_v
    limit = 1 << (config.adc_bits - 1)
    overrange = (v < -f) | (v > f)
    rounded = np.rint(np.clip(v, -f, f) * (limit / f))
    clipped = overrange | (rounded < -limit) | (rounded > limit - 1)
    codes = np.clip(rounded, -limit, limit - 1).astype(np.int16)
    return ADCResult(codes, codes_to_voltage(codes, config), clipped, overrange)
