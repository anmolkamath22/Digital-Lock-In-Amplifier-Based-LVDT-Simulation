import numpy as np
from lvdt_sim.reference import sine_lut, reference_samples, Q_SCALE


def test_lut_contract():
    r = sine_lut()
    assert len(r) == 20 and r[0] == 0 and r[10] == 0
    assert np.all(r[1:10] > 0) and np.all(r[11:] < 0)
    assert r[5] == 16384 and r[15] == -16384
    np.testing.assert_array_equal(r[1:10], -r[11:])
    np.testing.assert_allclose(r / Q_SCALE, np.sin(2*np.pi*np.arange(20)/20), atol=.5/Q_SCALE)
    np.testing.assert_array_equal(reference_samples(47, start_sample=13), np.tile(r, 3)[13:60])
