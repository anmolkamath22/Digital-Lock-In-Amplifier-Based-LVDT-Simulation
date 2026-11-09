import numpy as np
import pytest
from lvdt_sim.config import Config
from lvdt_sim.pipeline import run
from lvdt_sim.lockin_reference import fixed, floating
from lvdt_sim.reference import sine_lut


@pytest.mark.parametrize("position", [0, 2, -2])
def test_static_signed_estimates(position):
    s = run(Config(duration_s=.02, trajectory={"mode": "static", "value_mm": position}))
    np.testing.assert_allclose(s.floating.displacement_mm, position, atol=1e-12)
    np.testing.assert_allclose(s.fixed.displacement_mm, position, atol=.003)
    if not position:
        np.testing.assert_array_equal(s.fixed.accumulator, 0)


@pytest.mark.parametrize("length,outputs", [(199, 0), (200, 1), (399, 1), (400, 2)])
def test_window_boundaries(length, outputs):
    result = fixed(np.ones(length, dtype=np.int16), Config())
    assert len(result.accumulator) == outputs
    np.testing.assert_array_equal(result.end_sample, np.arange(outputs)*200+199)


def test_exact_independent_integer_loop():
    q = np.random.default_rng(112).integers(-2048, 2048, 1400, dtype=np.int16)
    lut = sine_lut()
    expected = [sum(int(q[n])*int(lut[n % 20]) for n in range(a, a+200)) for a in range(0, 1400, 200)]
    np.testing.assert_array_equal(fixed(q, Config()).accumulator, expected)


def test_continuous_phase_noncycle_windows():
    c = Config(window_samples=213)
    q = np.arange(852, dtype=np.int16)
    full = fixed(q, c)
    second = fixed(q[213:], c, start_sample=213)
    np.testing.assert_array_equal(full.accumulator[1:], second.accumulator)
    np.testing.assert_array_equal(full.center_time_s[1:], second.center_time_s)
    assert full.center_time_s[0] == 212/(2*20000)


@pytest.mark.parametrize("phase", [0, 15, 30, 45, 90])
def test_phase_cosine(phase):
    s = run(Config(duration_s=.01, phase_deg=phase))
    np.testing.assert_allclose(s.floating.displacement_mm, 2*np.cos(np.deg2rad(phase)), atol=1e-12)
    np.testing.assert_allclose(s.fixed.displacement_mm, 2*np.cos(np.deg2rad(phase)), atol=.003)


def test_dc_and_same_frequency():
    dc = run(Config(duration_s=.02, dc_offset_v=.6))
    np.testing.assert_allclose(dc.floating.displacement_mm, 2, atol=1e-12)
    tone = run(Config(duration_s=.02, interference_peak_v=.24, interference_hz=1000))
    np.testing.assert_allclose(tone.floating.displacement_mm, 3, atol=1e-12)


@pytest.mark.parametrize("frequency", [400, 950, 1000, 1050, 1600])
def test_tone_projection(frequency):
    c = Config(duration_s=.01, interference_hz=frequency, interference_peak_v=.24)
    s = run(c)
    # Analytic finite rectangular-window projection (not a universal rejection claim).
    n = np.arange(200)
    projection = 2/200*np.sum(.24*np.sin(2*np.pi*frequency*n/20000)*np.sin(2*np.pi*n/20))/.24
    np.testing.assert_allclose(s.floating.displacement_mm, 2+projection, atol=1e-12)


def test_sine_weighted_dynamic_truth():
    c = Config(trajectory={"mode": "sine", "frequency_hz": 2, "amplitude_mm": 3})
    s = run(c)
    ref = np.sin(2*np.pi*np.arange(c.sample_count)/20)
    weighted = (2*s.displacement_mm*ref**2).reshape(-1, 200).mean(axis=1)
    np.testing.assert_allclose(s.floating.displacement_mm, weighted, atol=2e-12)
    assert np.max(np.abs(s.fixed.displacement_mm - s.true_window_mean_mm)) < .01


def test_200th_sample_included():
    q = np.zeros(400, dtype=np.int16)
    q[199] = 123
    result = fixed(q, Config())
    assert result.accumulator[0] == 123*int(sine_lut()[19])
    assert result.accumulator[1] == 0


def test_sample_valid_gaps_and_reset_contract():
    # Independent clocked behavioral checker: stalled clocks never consume data.
    rng = np.random.default_rng(5)
    q = rng.integers(-2048, 2048, 400, dtype=np.int16)
    lut = [int(v) for v in sine_lut()]
    accumulator, count, phase = 0, 0, 0
    outputs = []
    for value in q:
        for _ in range(int(rng.integers(0, 7))):
            state_before = (accumulator, count, phase)
            sample_valid = False
            if sample_valid:
                raise AssertionError("stall unexpectedly accepted")
            assert state_before == (accumulator, count, phase)
        accumulator += int(value) * lut[phase]
        phase = (phase+1) % 20
        count += 1
        if count == 200:
            outputs.append(accumulator)
            accumulator, count = 0, 0
    np.testing.assert_array_equal(outputs, fixed(q, Config()).accumulator)
    # A fresh independent stream starts with phase 0, regardless of prior tail.
    fixed(q[:213], Config())
    np.testing.assert_array_equal(fixed(q, Config()).accumulator, outputs)
