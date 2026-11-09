"""Exported sine reference is the sole Q1.14 rounding authority for RTL."""

import numpy as np
from numpy.typing import NDArray

Q_SCALE = 1 << 14


def sine_lut(length: int = 20) -> NDArray[np.int16]:
    if type(length) is not int or length < 4:
        raise ValueError("LUT length must be an integer >= 4")
    return np.rint(Q_SCALE * np.sin(2 * np.pi * np.arange(length) / length)).astype(np.int16)


def reference_samples(count: int, length: int = 20, start_sample: int = 0, fixed: bool = True) -> NDArray:
    """Global accepted-sample indexing; independent streams start at sample zero."""
    if type(count) is not int or count < 0 or type(start_sample) is not int or start_sample < 0:
        raise ValueError("count and start_sample must be nonnegative integers")
    lut = sine_lut(length)
    index = (np.arange(count) + start_sample) % length
    return lut[index] if fixed else np.sin(2 * np.pi * index / length)
