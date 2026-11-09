"""Ground-truth trajectories on t[n] = n/fs, with explicit physical bounds."""

from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from .config import Config


def time_vector(config: Config) -> NDArray[np.float64]:
    return np.arange(config.sample_count, dtype=np.float64) / config.fs_hz


def validate_displacement(x_mm: NDArray, config: Config) -> NDArray[np.float64]:
    x = np.asarray(x_mm, dtype=np.float64)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("displacement must be a nonempty finite one-dimensional array")
    if np.any(x < config.min_mm) or np.any(x > config.max_mm):
        raise ValueError(f"displacement outside [{config.min_mm}, {config.max_mm}] mm")
    return x


def generate(config: Config) -> NDArray[np.float64]:
    """Generate static, step, sine, ramp, calibration, or interpolated custom motion.

    Ramps include both endpoints at the first/last sample. CSV requires strictly
    increasing time_s and displacement_mm columns covering all requested times;
    linear interpolation is used, with no extrapolation.
    """
    t = time_vector(config)
    p = dict(config.trajectory)
    mode = p.pop("mode", "static")
    allowed = {
        "static": {"value_mm"}, "step": {"before_mm", "after_mm", "step_s"},
        "sine": {"center_mm", "amplitude_mm", "frequency_hz", "phase_deg"},
        "ramp": {"start_mm", "end_mm"}, "calibration": {"values_mm", "hold_windows"},
        "custom": {"csv_path"},
    }
    if mode not in allowed or set(p) - allowed[mode]:
        raise ValueError(f"Unknown trajectory mode or parameters: {mode}, {set(p)}")
    if mode == "static":
        x = np.full(t.size, p.get("value_mm", 0.0))
    elif mode == "step":
        step_s = p.get("step_s", 0.5)
        if not np.isfinite(step_s) or not 0 <= step_s <= config.duration_s:
            raise ValueError("step_s must be within the simulated interval")
        x = np.where(t < step_s, p.get("before_mm", -3.0), p.get("after_mm", 3.0))
    elif mode == "sine":
        amplitude = p.get("amplitude_mm", 3.0)
        frequency = p.get("frequency_hz", 2.0)
        center = p.get("center_mm", 0.0)
        if not np.isfinite(amplitude) or amplitude < 0 or not np.isfinite(frequency) or not 0 <= frequency < config.fs_hz / 2:
            raise ValueError("Invalid mechanical amplitude or frequency")
        if center - amplitude < config.min_mm or center + amplitude > config.max_mm:
            raise ValueError("Sinusoid envelope exceeds the displacement range")
        x = center + amplitude * np.sin(2 * np.pi * frequency * t + np.deg2rad(p.get("phase_deg", 0.0)))
    elif mode == "ramp":
        x = np.linspace(p.get("start_mm", -5.0), p.get("end_mm", 5.0), t.size)
    elif mode == "calibration":
        values = validate_displacement(p.get("values_mm", [-5, -3, -1, 0, 1, 3, 5]), config)
        hold = p.get("hold_windows", 5)
        if type(hold) is not int or hold < 1:
            raise ValueError("hold_windows must be a positive integer")
        x = np.repeat(values, hold * config.window_samples)
        if x.size != t.size:
            raise ValueError("Calibration duration must equal values * hold_windows * window_samples / fs_hz")
    else:
        data = np.genfromtxt(Path(p["csv_path"]), delimiter=",", names=True)
        if not data.dtype.names or not {"time_s", "displacement_mm"} <= set(data.dtype.names):
            raise ValueError("Custom CSV requires time_s,displacement_mm columns")
        times = np.atleast_1d(data["time_s"])
        values = validate_displacement(np.atleast_1d(data["displacement_mm"]), config)
        if times.size < 2 or not np.all(np.isfinite(times)) or np.any(np.diff(times) <= 0):
            raise ValueError("Custom CSV times must be finite and strictly increasing")
        if times[0] > t[0] or times[-1] < t[-1]:
            raise ValueError("Custom CSV does not cover requested sample times")
        x = np.interp(t, times, values)
    return validate_displacement(x, config)
