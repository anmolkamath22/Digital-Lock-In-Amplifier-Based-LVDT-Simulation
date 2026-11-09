import numpy as np
import pytest
from lvdt_sim.config import Config
from lvdt_sim.trajectories import time_vector
from lvdt_sim.sensor import simulate


@pytest.mark.parametrize("position", [-5, -2, 0, 2, 5])
def test_linear_identity(position):
    c = Config(duration_s=.01)
    t = time_vector(c)
    s = simulate(t, np.full(t.size, position), c)
    np.testing.assert_allclose(s.differential_v, .24 * position * np.sin(2*np.pi*1000*t), atol=1e-15)
    assert 2 - abs(.24 * position) / 2 > 0
    if position:
        assert np.sign(np.dot(s.differential_v, s.primary_v)) == np.sign(position)


def test_nonlinear_symmetric():
    c = Config(duration_s=.01, cubic_v_per_mm3=.002, phase_deg=30)
    t = time_vector(c)
    s = simulate(t, np.full(t.size, 2), c)
    np.testing.assert_allclose(s.differential_v, (.48 + .002*8)*np.sin(2*np.pi*1000*t + np.pi/6), atol=1e-15)
    np.testing.assert_allclose(s.secondary_1_v + s.secondary_2_v, 4*np.sin(2*np.pi*1000*t + np.pi/6), atol=1e-15)
