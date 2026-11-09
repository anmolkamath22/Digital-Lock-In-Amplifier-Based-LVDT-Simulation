"""End-to-end independent simulation streams and self-describing HDL exports."""

from dataclasses import dataclass, replace
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from .config import Config
from . import trajectories, sensor, noise, adc, reference, lockin_reference, export


@dataclass(frozen=True)
class Simulation:
    config: Config
    stream_id: int
    time_s: NDArray
    displacement_mm: NDArray
    sensor: sensor.SensorSignals
    noise_components: dict[str, NDArray]
    measured_v: NDArray
    adc: adc.ADCResult
    floating: lockin_reference.LockInResult
    fixed: lockin_reference.LockInResult
    true_window_mean_mm: NDArray


def run(config: Config, stream_id: int = 0) -> Simulation:
    t = trajectories.time_vector(config)
    x = trajectories.generate(config)
    signals = sensor.simulate(t, x, config)
    components = noise.components(t, config, stream_id)
    measured = signals.differential_v + sum(components.values())
    digitized = adc.quantize(measured, config)
    fp = lockin_reference.floating(measured, config)
    fx = lockin_reference.fixed(digitized.codes, config)
    complete = len(fx.start_sample) * config.window_samples
    mean = x[:complete].reshape(-1, config.window_samples).mean(axis=1)
    return Simulation(config, stream_id, t, x, signals, components, measured, digitized, fp, fx, mean)


def export_simulation(sim: Simulation, output_dir: str | Path, name: str = "baseline") -> dict[str, str]:
    """Each named scenario is an independently reset stream with its own metadata."""
    if not name or Path(name).name != name or name in {".", ".."}:
        raise ValueError("scenario name must be a single safe path component")
    root = Path(output_dir)
    vectors, truth = root / "vectors" / name, root / "ground_truth" / name
    vectors.mkdir(parents=True, exist_ok=True)
    truth.mkdir(parents=True, exist_ok=True)
    c, fx = sim.config, sim.fixed
    export.write_hex(vectors / "adc_samples.hex", sim.adc.codes)
    export.write_hex(vectors / "reference_lut.hex", reference.sine_lut(c.lut_length))
    columns = [np.arange(c.sample_count), sim.time_s, sim.displacement_mm, sim.sensor.primary_v,
               sim.sensor.secondary_1_v, sim.sensor.secondary_2_v, sim.sensor.differential_v,
               sim.measured_v, sim.adc.codes]
    export.write_csv(truth / "ground_truth.csv", dict(zip(export.GROUND_TRUTH_COLUMNS, columns)))
    expected = [np.arange(len(fx.start_sample)), fx.start_sample, fx.end_sample, fx.center_time_s,
                fx.accumulator, fx.displacement_mm, sim.true_window_mean_mm,
                np.abs(fx.displacement_mm - sim.true_window_mean_mm)]
    export.write_csv(vectors / "expected_results.csv", dict(zip(export.EXPECTED_COLUMNS, expected)))
    limit = 1 << (c.adc_bits - 1)
    product_bound = limit * reference.Q_SCALE
    sum_bound = c.window_samples * product_bound
    metadata = {
        "data_contract_version": "1.0.0", "configuration": c.to_dict(),
        "units": {"displacement": "mm", "voltage": "V", "time": "s", "frequency": "Hz"},
        "sampling_frequency_hz": c.fs_hz, "excitation_frequency_hz": c.fc_hz,
        "adc": {"nominal_bits": c.adc_bits, "full_scale_v": c.adc_full_scale_v,
                "code_min": -limit, "code_max": limit-1, "volts_per_code": c.adc_full_scale_v/limit,
                "word_format": "signed 16-bit two's complement, four uppercase HEX characters",
                "rounding": "numpy.rint, nearest ties to even",
                "clipped_count": sim.adc.clipped_count, "clipped_percent": sim.adc.clipped_percent,
                "analog_overrange_count": int(np.count_nonzero(sim.adc.analog_overrange_mask))},
        "reference": {"length": c.lut_length, "scale": reference.Q_SCALE, "format": "signed 16-bit Q1.14",
                      "initial_index": 0, "phase": "continuous across windows; advance only on accepted samples"},
        "window_samples": c.window_samples, "number_of_samples": c.sample_count,
        "number_of_windows": len(fx.start_sample), "discarded_trailing_samples": c.sample_count % c.window_samples,
        "end_sample_convention": "inclusive", "timestamp": "midpoint of first and last accepted sample times",
        "random_seed": c.seed, "rng_stream_id": sim.stream_id, "rng": "default_rng(SeedSequence([seed, stream_id]))",
        "width_bounds": {"maximum_absolute_product": product_bound, "conservative_absolute_sum": sum_bound,
                         "minimum_signed_accumulator_bits": sum_bound.bit_length()+1,
                         "recommended_accumulator_bits": max(40, sum_bound.bit_length()+1)},
        "ground_truth_columns": export.GROUND_TRUTH_COLUMNS, "expected_results_columns": export.EXPECTED_COLUMNS,
        "known_limitations": ["single in-phase channel has cosine phase error", "coherent interference is inseparable",
                              "changing motion is sine-squared weighted within a window; arithmetic truth mean is diagnostic",
                              "rectangular windows cause frequency leakage", "analog-equivalent sampled model; no analog anti-alias filter",
                              "ADC quantization and saturation; positive full scale is asymmetric",
                              "cubic nonlinearity is not inverted by the linear estimator",
                              "non-integral-cycle windows can have gain ripple and DC leakage"],
    }
    export.write_json(vectors / "metadata.json", metadata)
    return {"vectors": str(vectors), "ground_truth": str(truth)}


def standard_scenarios(base: Config | None = None) -> dict[str, Config]:
    """Clean default instruments; override only common acquisition/physics with base.

    Scenario-specific noise and trajectories are explicit to prevent accidental
    contamination of baseline cases by a noisy configuration.
    """
    c = base or Config()
    clean = replace(c, noise_std_v=0, hum_peak_v=0, dc_offset_v=0, interference_peak_v=0,
                    drift_peak_v=0, phase_deg=0, cubic_v_per_mm3=0)
    def static(x: float, **kwargs) -> Config:
        return replace(clean, trajectory={"mode": "static", "value_mm": x}, **kwargs)
    return {
        "null": static(0), "positive": static(2), "negative": static(-2),
        "calibration": replace(clean, duration_s=11*5*c.window_samples/c.fs_hz,
                               trajectory={"mode": "calibration", "values_mm": list(range(-5, 6)), "hold_windows": 5}),
        "high_noise": static(2, noise_std_v=.4, hum_peak_v=.1),
        "step": replace(clean, trajectory={"mode": "step", "before_mm": -3, "after_mm": 3, "step_s": c.duration_s/2}),
        "sinusoidal": replace(clean, trajectory={"mode": "sine", "amplitude_mm": 3, "frequency_hz": 2}),
        "phase_mismatch": static(2, phase_deg=45),
        "adc_overrange": static(2, interference_peak_v=3, interference_hz=c.fc_hz),
        "same_frequency_interference": static(2, interference_peak_v=.24, interference_hz=c.fc_hz),
    }
