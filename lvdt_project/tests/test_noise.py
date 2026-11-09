import numpy as np
import pytest
from lvdt_sim.config import Config
from lvdt_sim.noise import components, gaussian


def test_gaussian_statistics_and_streams():
    a = gaussian(500000, .2, 42)
    assert abs(np.mean(a)) < .001
    assert abs(np.var(a) - .04) < .0003
    np.testing.assert_array_equal(a, gaussian(500000, .2, 42))
    assert not np.array_equal(a, gaussian(500000, .2, 42, 1))


def test_components():
    t = np.arange(10000) / 20000
    c = Config(hum_peak_v=.3, hum_phase_deg=17, dc_offset_v=.2,
               interference_peak_v=.4, interference_hz=950, interference_phase_deg=21,
               drift_peak_v=.1, drift_hz=.2)
    v = components(t, c)
    np.testing.assert_array_equal(v["gaussian_v"], 0)
    np.testing.assert_allclose(v["hum_v"], .3*np.sin(2*np.pi*50*t + np.deg2rad(17)))
    np.testing.assert_allclose(v["dc_v"], .2)
    np.testing.assert_allclose(v["interference_v"], .4*np.sin(2*np.pi*950*t + np.deg2rad(21)))
    np.testing.assert_allclose(v["drift_v"], .1*np.sin(2*np.pi*.2*t))


def test_invalid_noise():
    with pytest.raises(ValueError):
        gaussian(10, -.1, 42)
