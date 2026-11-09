"""Reproducible engineering studies with explicit numerical acceptance checks."""

from dataclasses import replace
from pathlib import Path
import numpy as np
from .config import Config
from .pipeline import run, standard_scenarios
from .adc import quantize
from .lockin_reference import fixed
from .noise import gaussian
from .metrics import calibration, error_metrics
from .export import write_json, write_csv


def studies(output_dir: str | Path, trials: int = 1000) -> dict:
    """Monte Carlo uses one independent 200-sample observation per trial."""
    if type(trials) is not int or trials < 200:
        raise ValueError("At least 200 Monte Carlo trials are required")
    out = Path(output_dir) / "reports"
    out.mkdir(parents=True, exist_ok=True)
    c = Config(duration_s=.01)
    checks = []
    def require(name: str, condition: bool) -> None:
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise RuntimeError(f"Numerical validation failed: {name}")

    static_results = []
    for x in (0, 2, -2):
        sim = run(replace(c, trajectory={"mode": "static", "value_mm": x}))
        estimate = float(sim.fixed.displacement_mm[0])
        static_results.append({"true_mm": x, "float_mm": float(sim.floating.displacement_mm[0]),
                               "fixed_mm": estimate, "absolute_error_mm": abs(estimate-x),
                               "accumulator": int(sim.fixed.accumulator[0])})
        require(f"static {x} mm", abs(estimate-x) < .003)
    cal = run(standard_scenarios()["calibration"])
    cal_metrics = calibration(cal.true_window_mean_mm, cal.fixed.displacement_mm, .24)
    require("calibration linearity", cal_metrics["r_squared"] > .999999 and cal_metrics["max_absolute_error_mm"] < .003)
    write_csv(out / "calibration.csv", {"true_mm": cal.true_window_mean_mm,
                                      "estimated_mm": cal.fixed.displacement_mm})
    n = np.arange(c.window_samples)
    clean = .48 * np.sin(2*np.pi*n/20)
    noise_results = []
    distribution = {"sigma_v": [], "trial_index": [], "estimated_mm": []}
    for level, sigma in enumerate((0, .05, .1, .2, .4)):
        v = np.tile(clean, trials) + gaussian(trials*200, sigma, c.seed, 10000+level)
        digitized = quantize(v, c)
        estimates = fixed(digitized.codes, c).displacement_mm
        metrics = error_metrics(np.full(trials, 2.0), estimates)
        theory = sigma / (c.sensitivity_v_per_mm*np.sqrt(c.window_samples/2))
        metrics.update(sigma_v=sigma, trials=trials, theoretical_std_mm=float(theory),
                       mean_estimate_mm=float(np.mean(estimates)),
                       mean_95_percent_halfwidth_mm=float(1.96*np.std(estimates, ddof=1)/np.sqrt(trials)),
                       clipped_count=digitized.clipped_count)
        noise_results.append(metrics)
        require(f"Monte Carlo sigma={sigma} bias", abs(metrics["bias_mm"]) < 5*theory/np.sqrt(trials)+.003)
        if sigma:
            require(f"Monte Carlo sigma={sigma} variance", abs(metrics["std_mm"]-theory) < .15*theory)
        distribution["sigma_v"].extend([sigma]*trials)
        distribution["trial_index"].extend(range(trials))
        distribution["estimated_mm"].extend(estimates)
    write_csv(out / "monte_carlo_trials.csv", distribution)
    write_csv(out / "noise_summary.csv", {key: [row[key] for row in noise_results] for key in noise_results[0]})
    phase_results = []
    for phase in (0, 15, 30, 45, 90):
        s = run(replace(c, phase_deg=phase))
        expected = 2*np.cos(np.deg2rad(phase))
        phase_results.append({"phase_deg": phase, "expected_mm": float(expected),
                              "floating_mm": float(s.floating.displacement_mm[0]),
                              "fixed_mm": float(s.fixed.displacement_mm[0])})
        require(f"phase {phase} cosine response", abs(s.floating.displacement_mm[0]-expected) < 1e-12)
    interference = []
    for frequency in (400, 950, 1000, 1050, 1600):
        # 1 s demonstrates the beating of nearby tones across 100 windows.
        s = run(replace(c, duration_s=1, interference_peak_v=.24, interference_hz=frequency,
                        interference_phase_deg=30))
        error = s.floating.displacement_mm - 2
        interference.append({"frequency_hz": frequency, "interference_phase_deg": 30,
                             "mean_bias_mm": float(error.mean()), "rms_error_mm": float(np.sqrt(np.mean(error**2))),
                             "max_absolute_error_mm": float(np.max(np.abs(error)))})
        if frequency == 1000:
            require("same-frequency interference bias", abs(error.mean()-np.cos(np.pi/6)) < 1e-12)
    dynamic = run(standard_scenarios()["sinusoidal"])
    ref = np.sin(2*np.pi*np.arange(dynamic.config.sample_count)/20)
    weighted = (2*dynamic.displacement_mm*ref**2).reshape(-1, 200).mean(axis=1)
    require("dynamic sine-squared window interpretation", np.max(np.abs(dynamic.floating.displacement_mm-weighted)) < 2e-12)
    dc = run(replace(c, dc_offset_v=.6))
    require("complete-cycle DC rejection", abs(dc.floating.displacement_mm[0]-2) < 1e-12)
    over = run(standard_scenarios()["adc_overrange"])
    require("overrange reported", over.adc.clipped_count > 0)
    rng = np.random.default_rng(99)
    codes = rng.integers(-2048, 2048, size=400, dtype=np.int16)
    # Deliberately independent scalar integer correlation.
    from .reference import sine_lut
    lut = [int(x) for x in sine_lut()]
    expected_sums = [sum(int(codes[i])*lut[i % 20] for i in range(start, start+200)) for start in (0, 200)]
    require("exact independent integer accumulators", np.array_equal(fixed(codes, c).accumulator, expected_sums))
    report = {"status": "passed", "seed": c.seed, "trials_per_noise_level": trials,
              "static": static_results, "calibration": cal_metrics, "noise": noise_results,
              "phase": phase_results, "interference": interference,
              "dynamic": error_metrics(dynamic.true_window_mean_mm, dynamic.fixed.displacement_mm),
              "overrange_clipped_count": over.adc.clipped_count, "checks": checks}
    write_json(out / "validation.json", report)
    lines = ["# Phase 1 numerical validation", "", f"All {len(checks)} numerical checks passed; seed 42.", "",
             "## Static positions", "", "| Truth (mm) | Fixed estimate (mm) | Absolute error (mm) | Integer sum |",
             "|---:|---:|---:|---:|"]
    lines += [f"| {r['true_mm']} | {r['fixed_mm']:.9f} | {r['absolute_error_mm']:.9f} | {r['accumulator']} |" for r in static_results]
    lines += ["", "## Calibration", ""] + [f"- {k}: {v:.12g}" for k, v in cal_metrics.items()]
    lines += ["", f"## Gaussian Monte Carlo ({trials} independent windows per level)", "",
              "| Sigma (V) | Bias (mm) | RMSE (mm) | Std (mm) | Theory std (mm) |", "|---:|---:|---:|---:|---:|"]
    lines += [f"| {r['sigma_v']} | {r['bias_mm']:.7f} | {r['rmse_mm']:.7f} | {r['std_mm']:.7f} | {r['theoretical_std_mm']:.7f} |" for r in noise_results]
    lines += ["", "## Interference (0.24 Vpeak, 30 degree phase)", "",
              "| Frequency (Hz) | Mean bias (mm) | RMS error (mm) |", "|---:|---:|---:|"]
    lines += [f"| {r['frequency_hz']} | {r['mean_bias_mm']:.7f} | {r['rms_error_mm']:.7f} |" for r in interference]
    lines += ["", "Near-carrier interference beats across windows. Same-frequency interference persists as a signed projection.",
              "No phase correction, noise removal guarantee, or hardware accuracy claim is implied.", ""]
    (out / "validation.md").write_text("\n".join(lines), encoding="utf-8")
    return report
