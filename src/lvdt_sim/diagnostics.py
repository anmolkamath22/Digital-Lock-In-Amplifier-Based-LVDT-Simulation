"""Headless static engineering diagnostics; no GUI or interactive dashboard."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .config import Config
from .pipeline import run, standard_scenarios


def generate(output_dir: str | Path, report: dict) -> list[str]:
    root = Path(output_dir) / "diagnostics"
    root.mkdir(parents=True, exist_ok=True)
    paths = []
    def save(name: str, title: str, xlabel: str, ylabel: str) -> None:
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(alpha=.3)
        plt.legend()
        plt.tight_layout()
        path = root / f"{name}.png"
        plt.savefig(path, dpi=160)
        plt.close()
        paths.append(str(path))
    s = run(Config(duration_s=.02, noise_std_v=.2, hum_peak_v=.1))
    short = slice(0, 100)
    ms = s.time_s[short]*1000
    plt.figure(figsize=(9, 4))
    for name, values in (("Primary", s.sensor.primary_v), ("Secondary 1", s.sensor.secondary_1_v), ("Secondary 2", s.sensor.secondary_2_v)):
        plt.plot(ms, values[short], label=name)
    save("01_windings", "LVDT winding voltages at +2 mm", "Time (ms)", "Voltage (V)")
    plt.figure(figsize=(9, 4))
    plt.plot(ms, s.sensor.differential_v[short], label="V1 - V2")
    save("02_differential", "Differential sensor output", "Time (ms)", "Voltage (V)")
    plt.figure(figsize=(9, 4))
    plt.plot(ms, s.measured_v[short], label="Measured (noise + hum)", alpha=.8)
    plt.plot(ms, s.sensor.differential_v[short], label="Clean")
    save("03_clean_noisy", "Additive measurement interference", "Time (ms)", "Voltage (V)")
    plt.figure(figsize=(9, 4))
    plt.plot(s.time_s*1000, (s.adc.reconstructed_v-s.measured_v)*1000, ".", label="ADC reconstruction error", markersize=3)
    half_lsb = s.config.adc_full_scale_v/2048/2*1000
    plt.axhline(half_lsb, color="red", linestyle="--", label="+/- half LSB")
    plt.axhline(-half_lsb, color="red", linestyle="--")
    save("04_quantization", "Quantization error (no saturation in this trace)", "Time (ms)", "Error (mV)")
    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    configs = standard_scenarios()
    for ax, name in zip(axes, ("sinusoidal", "step")):
        d = run(configs[name])
        ax.plot(d.time_s, d.displacement_mm, label="True trajectory")
        ax.plot(d.fixed.center_time_s, d.fixed.displacement_mm, ".", label="Fixed estimate at window center")
        ax.set_ylabel("Displacement (mm)")
        ax.set_title(name.capitalize())
        ax.grid(alpha=.3)
        ax.legend()
    axes[-1].set_xlabel("Time (s)")
    fig.tight_layout()
    path = root / "05_displacement.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    paths.append(str(path))
    cal = run(configs["calibration"])
    plt.figure(figsize=(7, 5))
    plt.plot(cal.true_window_mean_mm, cal.fixed.displacement_mm, "o", label="Fixed-point estimates")
    plt.plot([-5, 5], [-5, 5], "--", label="Ideal")
    save("06_calibration", "Signed displacement calibration", "True displacement (mm)", "Estimated displacement (mm)")
    plt.figure(figsize=(7, 5))
    levels = [r["sigma_v"] for r in report["noise"]]
    plt.plot(levels, [r["rmse_mm"] for r in report["noise"]], "o-", label="Monte Carlo fixed-point RMSE")
    plt.plot(levels, [r["theoretical_std_mm"] for r in report["noise"]], "--", label="Unclipped white-noise theory")
    save("07_noise_error", f"Noise robustness ({report['trials_per_noise_level']} trials per level)", "Gaussian sigma (V)", "Displacement error (mm)")
    plt.figure(figsize=(7, 5))
    phases = [r["phase_deg"] for r in report["phase"]]
    plt.plot(phases, [r["fixed_mm"] for r in report["phase"]], "o", label="Fixed-point estimate")
    angle = np.linspace(0, 90, 200)
    plt.plot(angle, 2*np.cos(np.deg2rad(angle)), "--", label="2 cos(phase)")
    save("08_phase_error", "Uncompensated phase sensitivity at +2 mm", "Sensor phase (degrees)", "Estimated displacement (mm)")
    return paths
