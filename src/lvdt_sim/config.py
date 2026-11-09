"""Validated configuration. Frequencies in Hz, time in s, displacement in mm."""

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
import math


@dataclass(frozen=True)
class Config:
    fs_hz: float = 20000.0
    fc_hz: float = 1000.0
    duration_s: float = 1.0
    sensitivity_v_per_mm: float = 0.24
    secondary_null_v: float = 2.0
    primary_peak_v: float = 5.0
    min_mm: float = -5.0
    max_mm: float = 5.0
    phase_deg: float = 0.0
    cubic_v_per_mm3: float = 0.0
    adc_full_scale_v: float = 2.5
    adc_bits: int = 12
    lut_length: int = 20
    window_samples: int = 200
    seed: int = 42
    noise_std_v: float = 0.0
    hum_peak_v: float = 0.0
    hum_hz: float = 50.0
    hum_phase_deg: float = 0.0
    dc_offset_v: float = 0.0
    interference_peak_v: float = 0.0
    interference_hz: float = 400.0
    interference_phase_deg: float = 0.0
    drift_peak_v: float = 0.0
    drift_hz: float = 0.1
    trajectory: dict = field(default_factory=lambda: {"mode": "static", "value_mm": 2.0})

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if name != "trajectory" and (not isinstance(value, (int, float)) or not math.isfinite(value)):
                raise ValueError(f"{name} must be a finite number")
        for name in ("fs_hz", "fc_hz", "duration_s", "sensitivity_v_per_mm", "secondary_null_v",
                     "primary_peak_v", "adc_full_scale_v"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")
        for name in ("adc_bits", "lut_length", "window_samples", "seed"):
            if type(getattr(self, name)) is not int:
                raise ValueError(f"{name} must be an integer")
        if not 2 <= self.adc_bits <= 16 or self.lut_length < 4 or self.window_samples < 1 or self.seed < 0:
            raise ValueError("Invalid ADC bits, LUT length, window length or seed")
        if self.min_mm >= self.max_mm:
            raise ValueError("min_mm must be less than max_mm")
        if not math.isclose(self.fs_hz / self.fc_hz, self.lut_length, rel_tol=0, abs_tol=1e-10):
            raise ValueError("Coherent reference requires fs_hz / fc_hz == lut_length")
        if not math.isclose(self.duration_s * self.fs_hz, round(self.duration_s * self.fs_hz), abs_tol=1e-8):
            raise ValueError("duration_s must contain an integral number of samples")
        if self.sample_count < 1:
            raise ValueError("duration must contain at least one sample")
        for name in ("noise_std_v", "hum_peak_v", "interference_peak_v", "drift_peak_v"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be nonnegative")
        for name in ("hum_hz", "interference_hz", "drift_hz"):
            if not 0 <= getattr(self, name) < self.fs_hz / 2:
                raise ValueError(f"{name} must be below Nyquist and nonnegative")
        if not isinstance(self.trajectory, dict):
            raise ValueError("trajectory must be a JSON object")
        # Check endpoints AND stationary points of the cubic across the full range.
        points = [self.min_mm, self.max_mm]
        if self.cubic_v_per_mm3 < 0:
            root = math.sqrt(-self.sensitivity_v_per_mm / (3 * self.cubic_v_per_mm3))
            points += [p for p in (-root, root) if self.min_mm <= p <= self.max_mm]
        if any(abs(self.sensitivity_v_per_mm * p + self.cubic_v_per_mm3 * p**3)
               >= 2 * self.secondary_null_v for p in points):
            raise ValueError("Differential amplitude would make a secondary amplitude nonpositive")

    @property
    def sample_count(self) -> int:
        return round(self.duration_s * self.fs_hz)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def load(cls, path: str | Path) -> "Config":
        """Resolve a custom trajectory CSV relative to its configuration file."""
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        trajectory = data.get("trajectory", {})
        if trajectory.get("mode") == "custom" and "csv_path" in trajectory:
            csv_path = Path(trajectory["csv_path"])
            if not csv_path.is_absolute():
                trajectory["csv_path"] = str((path.parent / csv_path).resolve())
        return cls(**data)
