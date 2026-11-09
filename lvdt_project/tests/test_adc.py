import numpy as np
import pytest
from lvdt_sim.config import Config
from lvdt_sim.adc import quantize, codes_to_voltage


def test_extremes_and_rounding():
    c = Config()
    lsb = 2.5 / 2048
    a = quantize(np.array([0, lsb, -lsb, 2.5, -2.5, 3, -3, .5*lsb, 1.5*lsb, -.5*lsb, -1.5*lsb]), c)
    np.testing.assert_array_equal(a.codes, [0, 1, -1, 2047, -2048, 2047, -2048, 0, 2, 0, -2])
    assert a.codes.dtype == np.int16
    assert a.clipped_count == 3
    assert np.count_nonzero(a.analog_overrange_mask) == 2
    assert a.clipped_percent == 100*3/11
    np.testing.assert_allclose(codes_to_voltage(a.codes, c), a.codes * lsb)


def test_quantization_bound():
    c = Config()
    v = np.linspace(-3, 3, 100001)
    a = quantize(v, c)
    assert np.max(np.abs(a.reconstructed_v[~a.clipped_mask] - v[~a.clipped_mask])) <= 2.5/4096 + 1e-15


def test_invalid_adc():
    with pytest.raises(ValueError):
        quantize(np.array([np.nan]), Config())
    with pytest.raises(ValueError):
        codes_to_voltage(np.array([2048]), Config())
