from dataclasses import replace
import numpy as np
import pytest
from lvdt_sim.config import Config
from lvdt_sim.trajectories import generate, time_vector


@pytest.mark.parametrize("mode", ["static", "step", "sine", "ramp"])
def test_modes(mode):
    c = Config(trajectory={"mode": mode})
    x = generate(c)
    assert len(x) == 20000
    np.testing.assert_array_equal(time_vector(c), np.arange(20000) / 20000)
    assert np.min(x) >= -5 and np.max(x) <= 5


def test_calibration_and_step():
    c = Config(duration_s=.06, trajectory={"mode": "calibration", "values_mm": [-2, 0, 2], "hold_windows": 2})
    np.testing.assert_array_equal(generate(c), np.repeat([-2, 0, 2], 400))
    s = generate(Config(trajectory={"mode": "step", "step_s": .5}))
    assert s[9999] == -3 and s[10000] == 3
    with pytest.raises(ValueError):
        generate(replace(c, duration_s=.1))


def test_custom(tmp_path):
    path = tmp_path / "motion.csv"
    path.write_text("time_s,displacement_mm\n0,-1\n1,1\n")
    c = Config(trajectory={"mode": "custom", "csv_path": str(path)})
    np.testing.assert_allclose(generate(c), -1 + 2 * time_vector(c))
    path.write_text("time_s,displacement_mm\n0,0\n0,1\n")
    with pytest.raises(ValueError):
        generate(c)


@pytest.mark.parametrize("trajectory", [{"mode": "static", "value_mm": 6}, {"mode": "sine", "amplitude_mm": 6}, {"mode": "bogus"}])
def test_invalid_motion(trajectory):
    with pytest.raises(ValueError):
        generate(Config(trajectory=trajectory))


@pytest.mark.parametrize("kwargs", [{"fs_hz": 19000}, {"duration_s": .00001}, {"seed": -1}, {"noise_std_v": -1}, {"secondary_null_v": .1}, {"phase_deg": float("nan")}])
def test_invalid_config(kwargs):
    with pytest.raises(ValueError):
        Config(**kwargs)
